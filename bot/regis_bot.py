#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regis no Telegram.

Python 3 e biblioteca padrão, nada de pip install. Fala com a Bot API por
urllib e recebe as mensagens por long polling (getUpdates).

Rodar:

    TELEGRAM_TOKEN=123456:ABC... python3 bot/regis_bot.py

O passo a passo completo está em bot/README.md.

Duas coisas que este arquivo garante, porque são a tese do produto:

1. A ordem das mensagens é número, ganho, má notícia, pergunta. Uma pergunta
   por vez, nunca duas.
2. A Regis não move dinheiro. Ela prepara o texto e quem envia é a pessoa.
   Nenhuma mensagem daqui pode sugerir o contrário.

As funções de roteiro (as que montam as mensagens) não sabem que o Telegram
existe. É de propósito: `simular.py` usa as mesmas funções sem rede, e o dia
que virar WhatsApp só a classe Telegram muda.
"""

import json
import os
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

# A conversa livre com IA é opcional. Sem o SDK da Anthropic instalado, sem
# chave no ambiente ou sem os dados, o import falha aqui e o bot segue inteiro
# no caminho determinístico, que é o que a demo por comandos usa.
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import conversa_ia  # type: ignore
except Exception as _erro_ia:  # noqa: N816
    conversa_ia = None
    print("[regis] conversa com IA desligada (%s). Só o determinístico." % _erro_ia)

# ---------------------------------------------------------------------------
# 0. Quem fala
# ---------------------------------------------------------------------------
#
# A Regis é no feminino, decisão do time. O gênero aparece em toda mensagem que
# a pessoa lê, então mora aqui em um campo só. Trocar PERSONA["artigo"] para "o"
# ajusta o artigo e as contrações de uma vez, sem caçar texto pelo arquivo.

PERSONA = {
    "nome": "Regis",
    "artigo": "a",
    "pronome": "ela",
}

# As contrações que o português exige. Saem do artigo, não são campo à parte.
_CONTRACOES = {"de": {"a": "da", "o": "do"}, "por": {"a": "pela", "o": "pelo"}}


def com_artigo(preposicao=None, maiuscula=False):
    """
    O nome com o artigo certo: a Regis, A Regis no começo da frase, da Regis e
    pela Regis quando vem preposição.
    """
    artigo = PERSONA["artigo"]
    if preposicao:
        artigo = _CONTRACOES[preposicao][artigo]
    return "%s %s" % (artigo.capitalize() if maiuscula else artigo, PERSONA["nome"])


AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PASTA_DADOS = os.path.join(RAIZ, "dados")
# No VPS a memória mora num volume, para sobreviver a atualização do código.
# Sem a variável, fica ao lado do script, como sempre foi.
ARQUIVO_MEMORIA = os.environ.get("REGIS_MEMORIA") or os.path.join(AQUI, "memoria.json")

# O registro guarda o que foi dito, dos dois lados. É a memória recente dela e
# é também o material para analisarmos as conversas depois.
sys.path.insert(0, AQUI)
import registro  # noqa: E402

API = "https://api.telegram.org/bot{token}/{metodo}"
TIMEOUT_POLL = 25          # quanto o Telegram segura a conexão esperando mensagem
TIMEOUT_HTTP = 40          # tem que ser maior que o de cima
# Teto de mensagens seguidas. Catorze balões de uma vez assustam, e assustar
# é o oposto do que a Regis existe pra fazer.
MAX_MENSAGENS = int(os.environ.get("REGIS_MAX_MENSAGENS") or 3)
PAUSA_CURTA = 1.0
PAUSA_LONGA = 1.8


# ---------------------------------------------------------------------------
# 1. O motor
# ---------------------------------------------------------------------------

def carregar_motor():
    """
    Devolve (funcao_detectar, nome_da_fonte).

    Tenta o motor de verdade. Se ele ainda não existe, ou se quebra na hora de
    importar, cai no stub local e o bot continua de pé. O bot nunca morre por
    causa do motor.
    """
    if RAIZ not in sys.path:
        sys.path.insert(0, RAIZ)
    try:
        from motor.detectar import detectar  # type: ignore
        return detectar, "motor"
    except Exception as erro:
        print("[regis] motor real indisponível (%s). Usando bot/stub_motor.py." % erro)
        if AQUI not in sys.path:
            sys.path.insert(0, AQUI)
        from stub_motor import detectar  # type: ignore
        return detectar, "stub"


_detectar, FONTE_MOTOR = carregar_motor()
_cache = {"resultado": None}


def rodar_motor(recarregar=False):
    """Roda o motor e guarda o resultado. Se o motor quebrar, cai no stub."""
    global _detectar, FONTE_MOTOR
    if _cache["resultado"] is not None and not recarregar:
        return _cache["resultado"]
    try:
        try:
            resultado = _detectar(PASTA_DADOS)
        except TypeError:
            # O motor pode ter nascido sem argumento nenhum. Isso não é motivo para cair.
            resultado = _detectar()
        if not isinstance(resultado, dict):
            raise ValueError("o motor devolveu %s no lugar de um dicionário" % type(resultado).__name__)
    except Exception as erro:
        print("[regis] motor falhou ao rodar (%s). Caindo no stub." % erro)
        if AQUI not in sys.path:
            sys.path.insert(0, AQUI)
        from stub_motor import detectar as detectar_stub
        _detectar, FONTE_MOTOR = detectar_stub, "stub"
        resultado = detectar_stub(PASTA_DADOS)
    resultado.setdefault("resumo", {})
    resultado.setdefault("achados", [])
    resultado.setdefault("silenciados", [])
    _cache["resultado"] = resultado
    return resultado


def achado_por_id(identificador):
    for achado in rodar_motor().get("achados", []):
        if achado.get("id") == identificador:
            return achado
    return None


def por_certeza(resultado, certeza):
    return [a for a in resultado.get("achados", []) if a.get("certeza") == certeza]


def nome_da_contraparte(achado):
    """
    O nome de quem está do outro lado, quando o motor mandou. O contrato não
    obriga esse campo, então aqui a resposta pode ser None, e quem chama
    escreve a frase de outro jeito.
    """
    for chave in ("contraparte", "quem", "nome"):
        valor = achado.get(chave)
        if valor:
            return str(valor)
    meta = achado.get("meta") or {}
    if isinstance(meta, dict) and meta.get("contraparte"):
        return str(meta["contraparte"])
    return None


def contraparte_de(achado):
    """
    A chave que a memória usa para não perguntar duas vezes sobre a mesma
    pessoa. Se o motor não mandou o nome, o título do achado serve, porque o
    que importa é a pergunta não voltar.
    """
    return nome_da_contraparte(achado) or str(
        achado.get("titulo") or achado.get("id") or "essa cobrança")


# ---------------------------------------------------------------------------
# 2. A memória (é aqui que ela aprende)
# ---------------------------------------------------------------------------

class Memoria:
    """
    Guarda o que a pessoa já respondeu, em bot/memoria.json.

    Uma resposta "foi eu" registra a contraparte como conhecida, e a partir
    daí a Regis não pergunta mais sobre ela. Esse arquivo é o produto
    aprendendo, então ele é gravado na hora, não no fim.
    """

    def __init__(self, caminho=ARQUIVO_MEMORIA):
        self.caminho = caminho
        self.dados = {"contrapartes_conhecidas": [], "contrapartes_negadas": [], "respostas": {}}
        self.carregar()

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                guardado = json.load(arquivo)
            if isinstance(guardado, dict):
                self.dados.update(guardado)
        except Exception:
            pass
        self.dados.setdefault("contrapartes_conhecidas", [])
        self.dados.setdefault("contrapartes_negadas", [])
        self.dados.setdefault("respostas", {})
        return self.dados

    def gravar(self):
        """
        Grava num arquivo temporário e troca no lugar.

        O app web lê este mesmo arquivo de 3 em 3 segundos. Abrir em "w"
        trunca antes de escrever, e nessa janela o web lia memória vazia.
        Com os.replace a troca é atômica: ou o web vê o arquivo velho
        inteiro, ou o novo inteiro, nunca um pedaço.
        """
        temporario = self.caminho + ".tmp"
        try:
            with open(temporario, "w", encoding="utf-8") as arquivo:
                json.dump(self.dados, arquivo, ensure_ascii=False, indent=2)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, self.caminho)
        except Exception as erro:
            print("[regis] não consegui gravar a memória: %s" % erro)
            try:
                os.remove(temporario)
            except OSError:
                pass

    @staticmethod
    def _chave(nome):
        texto = unicodedata.normalize("NFKD", str(nome or ""))
        texto = "".join(c for c in texto if not unicodedata.combining(c))
        return texto.strip().lower()

    def conhece(self, nome):
        alvo = self._chave(nome)
        return any(self._chave(n) == alvo for n in self.dados["contrapartes_conhecidas"])

    def ja_respondeu(self, identificador):
        return identificador in self.dados["respostas"]

    def registrar(self, achado, resposta):
        nome = contraparte_de(achado)
        self.dados["respostas"][achado.get("id", nome)] = {
            "contraparte": nome,
            "resposta": resposta,
            "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        lista = "contrapartes_conhecidas" if resposta == "foi_eu" else "contrapartes_negadas"
        if not any(self._chave(n) == self._chave(nome) for n in self.dados[lista]):
            self.dados[lista].append(nome)
        self.gravar()
        return nome


# ---------------------------------------------------------------------------
# 3. Formatação
# ---------------------------------------------------------------------------

def moeda(valor):
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return "R$ 0,00"
    parte_inteira, centavos = ("%.2f" % abs(numero)).split(".")
    partes = []
    while len(parte_inteira) > 3:
        partes.insert(0, parte_inteira[-3:])
        parte_inteira = parte_inteira[:-3]
    partes.insert(0, parte_inteira)
    return "R$ %s,%s" % (".".join(partes), centavos)


def inteiro(valor):
    """O motor pode mandar número como texto, ou não mandar. Nenhum dos dois derruba a mensagem."""
    try:
        return int(float(valor))
    except (TypeError, ValueError):
        return 0


def escapar(texto):
    return (str(texto).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


EMOJI = {"fato": "✅", "regra": "⚠️", "suspeita": "❓"}


def msg(texto, botoes=None, pausa=PAUSA_CURTA, generico=False):
    """
    `generico` marca a resposta de quando ela não entendeu a pergunta. É o único
    ponto onde a IA entra: se a mensagem está marcada, o bot tenta a conversa
    livre antes de mandar essa resposta. Todo o resto continua determinístico.
    """
    return {"texto": texto, "botoes": botoes or [], "pausa": pausa, "generico": generico}


def botao(rotulo, dado):
    return [{"texto": rotulo, "data": dado}]


MESES = ("janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")


def data_por_extenso(valor):
    """
    O motor pode mandar a projeção como 2026-10-24 ou como outubro de 2026.
    Ninguém fala data em ISO, então aqui ela vira 24 de outubro de 2026.
    Qualquer outro formato passa direto, sem estragar a frase.
    """
    texto = str(valor or "").strip()
    partes = texto.split("-")
    if len(partes) == 3 and len(partes[0]) == 4:
        try:
            ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2][:2])
            return "%d de %s de %d" % (dia, MESES[mes - 1], ano)
        except (ValueError, IndexError):
            return texto
    return texto


def primeira_frase(texto):
    """A primeira frase de uma explicação longa. Serve para a lista do silêncio caber na tela."""
    limpo = str(texto or "").strip()
    if not limpo:
        return ""
    corte = limpo.find(". ")
    return limpo[:corte + 1] if corte > 0 else limpo


def sem_acento(texto):
    limpo = unicodedata.normalize("NFKD", str(texto or ""))
    return "".join(c for c in limpo if not unicodedata.combining(c)).lower()


# ---------------------------------------------------------------------------
# 4. Os roteiros (montam as mensagens, não sabem o que é Telegram)
# ---------------------------------------------------------------------------

def roteiro_start(resultado, recomecando=False):
    """
    Primeira interação. Revela um número antes de pedir qualquer coisa.

    `recomecando` é o /esquecer: ela apagou o que aprendeu, então volta a se
    apresentar. Apagar a memória e continuar como se nada tivesse acontecido
    deixa a pessoa sem saber em que pé a conversa ficou.
    """
    resumo = resultado.get("resumo", {})
    faturado = moeda(resumo.get("faturamento_acumulado", 0))
    falta = moeda(resumo.get("falta_para_o_teto", 0))
    teto = moeda(resumo.get("teto", 81000))
    percentual = resumo.get("percentual_do_teto", 0)
    quantidade = inteiro(resumo.get("qtd_transacoes_conferidas"))

    if recomecando:
        abertura = ("Pronto, esqueci tudo que você já me contou.\n\n"
                    "Vamos do começo. Eu sou %s, e cuido do dinheiro que entra e sai da sua "
                    "conta para você não precisar cuidar. Já li o seu extrato." % com_artigo())
    else:
        abertura = ("Oi, eu sou %s. Cuido do dinheiro que entra e sai da sua conta "
                    "para você não precisar cuidar.\n\n"
                    "Já li o seu extrato, então começo pelo que interessa." % com_artigo())

    return [
        msg(abertura),
        msg("Você já faturou <b>%s</b> este ano.\nFaltam <b>%s</b> pro teto do MEI, "
            "que é de %s." % (faturado, falta, teto), pausa=PAUSA_LONGA),
        msg("Isso é %s%% do teto, somando %d movimentações de janeiro pra cá. "
            "Nada pra você preencher, eu contei." % (
                str(percentual).replace(".", ","), quantidade),
            botoes=[botao("Ver o que eu achei", "conferir")],
            pausa=PAUSA_LONGA),
    ]


def frase_do_valor(achado):
    """
    Dinheiro pago duas vezes volta. Taxa nova e reajuste não voltam, eles
    param de sangrar. Dizer "de volta" nos dois casos seria promessa falsa.
    """
    valor = float(achado.get("valor") or 0)
    if valor <= 0:
        return ""
    if moeda(valor) in (achado.get("explicacao") or ""):
        # O motor já disse o número na explicação. Repetir soa a robô.
        return ""
    quando = achado.get("periodicidade")
    sufixo = " %s" % escapar(quando) if quando else ""
    recuperavel = achado.get("recuperavel")
    if recuperavel is None:
        tipo = sem_acento(achado.get("tipo", ""))
        if tipo in [sem_acento(t) for t in RECUPERAVEIS]:
            recuperavel = True
        elif tipo == "valor":
            recuperavel = False
    if recuperavel is True:
        return "\nDá <b>%s</b> de volta pro seu bolso." % moeda(valor)
    if recuperavel is False:
        return "\nIsso está te custando <b>%s</b>%s." % (moeda(valor), sufixo)
    return "\nSão <b>%s</b> em jogo." % moeda(valor)


def frase_da_acao(acao):
    tipo = (acao.get("tipo") or "").lower()
    if tipo in ("instrucao", "instrução"):
        return "\nJá deixei o passo a passo pronto."
    if tipo in ("opcoes", "opções"):
        return "\nQuem decide é você, eu deixo o material pronto."
    return "\nJá escrevi o que você precisa mandar."


def mensagem_de_fato(achado):
    corpo = "%s <b>%s</b>\n%s" % (
        EMOJI["fato"], escapar(achado.get("titulo", "")), escapar(achado.get("explicacao", "")))
    corpo += frase_do_valor(achado)
    acao = achado.get("acao")
    botoes = []
    if acao:
        corpo += frase_da_acao(acao)
        botoes = [botao(acao.get("titulo") or "Ver o texto", "ver:%s" % achado.get("id"))]
    return msg(corpo, botoes=botoes, pausa=PAUSA_LONGA)


def mensagem_de_regra(achado):
    corpo = "%s <b>%s</b>\n%s" % (
        EMOJI["regra"], escapar(achado.get("titulo", "")), escapar(achado.get("explicacao", "")))
    acao = achado.get("acao")
    botoes = []
    if acao:
        corpo += "\nQuem decide é você, eu deixo o material pronto."
        botoes = [botao(acao.get("titulo") or "Ver as opções", "ver:%s" % achado.get("id"))]
    return msg(corpo, botoes=botoes, pausa=PAUSA_LONGA)


def mensagem_de_suspeita(achado):
    corpo = "%s %s\n%s\nFoi você?" % (
        EMOJI["suspeita"], escapar(achado.get("titulo", "")), escapar(achado.get("explicacao", "")))
    identificador = achado.get("id")
    botoes = [[
        {"texto": "Foi eu", "data": "sim:%s" % identificador},
        {"texto": "Não fui eu", "data": "nao:%s" % identificador},
    ]]
    return msg(corpo, botoes=botoes, pausa=PAUSA_LONGA)


def roteiro_acao(achado):
    """O texto pronto. A Regis escreve, a pessoa envia. Ela não envia no lugar da pessoa."""
    acao = achado.get("acao") or {}
    texto = acao.get("texto") or "Ainda não escrevi esse texto."
    mensagens = [msg("<pre>%s</pre>" % escapar(texto), pausa=PAUSA_LONGA)]
    tipo = (acao.get("tipo") or "").lower()
    if tipo in ("instrucao", "opcoes"):
        mensagens.append(msg("É só seguir esses passos. Se travar em algum, me chama que eu explico."))
    else:
        mensagens.append(msg(
            "É só copiar e mandar. Eu não envio no seu nome e não mexo na sua conta, "
            "então quem aperta enviar é você."))
    mensagens.append(msg("Me avisa quando mandar. Se o dinheiro não voltar em 10 dias, eu te lembro."))
    return mensagens


def roteiro_conferir(resultado, memoria):
    """
    A conferência inteira em três mensagens.

    Antes ela mandava uma mensagem por achado, o que dava catorze balões
    seguidos. Quem testou se assustou e pediu pra ela parar, e com razão: um
    autopilot que despeja catorze mensagens é um relatório com pressa, não uma
    assistente. A ordem da pesquisa continua a mesma, ganho primeiro, má
    notícia depois, uma pergunta só no fim. O que muda é que cada etapa cabe
    numa mensagem, e o detalhe fica a um botão de distância.
    """
    resumo = resultado.get("resumo", {})
    fatos = por_certeza(resultado, "fato")
    regras = por_certeza(resultado, "regra")
    silenciados = resultado.get("silenciados", [])

    suspeitas = [a for a in por_certeza(resultado, "suspeita")
                 if not memoria.conhece(contraparte_de(a)) and not memoria.ja_respondeu(a.get("id"))]

    total = resumo.get("total_recuperavel")
    if total is None:
        total = sum(float(a.get("valor") or 0) for a in fatos)
    quantidade = inteiro(resumo.get("qtd_transacoes_conferidas"))

    mensagens = []

    # 1. O ganho. Os três maiores por extenso, o resto contado.
    linhas = ["Conferi %d movimentações da sua conta." % quantidade]
    if fatos:
        linhas.append("")
        linhas.append("✅ Achei <b>%s</b> saindo à toa." % moeda(total))
        for achado in fatos[:3]:
            linhas.append("• <b>%s</b> · %s" % (moeda(achado.get("valor")),
                                                escapar(achado.get("titulo") or "")))
        sobraram = len(fatos) - 3
        if sobraram > 0:
            linhas.append("")
            linhas.append("Tem mais %d, todos menores. Te mostro um por um se quiser." % sobraram)
    else:
        linhas.append("")
        linhas.append("✅ Não achei nada saindo à toa. Está tudo batendo.")

    botoes = []
    if fatos:
        # A ação do maior fato é o que ela já deixou pronto, e é o que
        # interessa: a pessoa não quer a lista, quer resolver.
        if fatos[0].get("acao"):
            botoes = [botao("Ver o que eu escrevi", "ver:%s" % fatos[0].get("id"))]
    mensagens.append(msg("\n".join(linhas), botoes=botoes, pausa=PAUSA_LONGA))

    # 2. O que você decide, mais o que eu calei. Cabe numa mensagem só.
    linhas = []
    for achado in regras:
        linhas.append("⚠️ <b>%s</b>" % escapar(achado.get("titulo") or ""))
        explicacao = achado.get("explicacao")
        if explicacao:
            linhas.append(escapar(explicacao))
        linhas.append("")
    if silenciados:
        linhas.append("Outras %d coisas apareceram e eu deixei passar, são normais pro seu "
                      "histórico. Se quiser ver, me peça o silêncio." % len(silenciados))
    if linhas:
        mensagens.append(msg("\n".join(linhas).strip(), pausa=PAUSA_LONGA))

    # 3. Uma pergunta, uma só.
    if suspeitas:
        mensagens.append(mensagem_de_suspeita(suspeitas[0]))
    elif len(mensagens) < 2:
        mensagens.append(msg(
            "Não tenho pergunta pra você desta vez. O que sobrou é gente que você já me apresentou."))

    return mensagens[:MAX_MENSAGENS]


def roteiro_foi_eu(achado, memoria):
    memoria.registrar(achado, "foi_eu")
    nome = nome_da_contraparte(achado)
    if nome:
        segunda = msg("<b>%s</b> agora está na sua lista de conhecidos. "
                      "Se aparecer de novo, eu passo batida." % escapar(nome))
    else:
        segunda = msg("Guardei na sua lista de conhecidos. "
                      "Se esse pagamento voltar a aparecer, eu passo batida.")
    return [msg("Perfeito. Anotei, não pergunto mais sobre ela."), segunda]


_transacoes = {"por_id": None}


def valor_da_transacao(identificadores):
    """
    Soma o valor das transações citadas num achado.

    Suspeita não tem campo `valor`, e faz sentido: o motor só soma valor no que
    é fato, porque suspeita não é dinheiro a recuperar. Só que a contestação
    precisa dizer quanto foi, então aqui o valor vem da transação em si.
    """
    if _transacoes["por_id"] is None:
        indice = {}
        try:
            with open(os.path.join(PASTA_DADOS, "transacoes.json"), "r", encoding="utf-8") as arquivo:
                bruto = json.load(arquivo)
            for transacao in (bruto.get("transacoes") if isinstance(bruto, dict) else bruto) or []:
                if transacao.get("id"):
                    indice[transacao["id"]] = abs(float(transacao.get("valor") or 0))
        except Exception as erro:
            print("[regis] não consegui ler as transações: %s" % erro)
        _transacoes["por_id"] = indice
    return sum(_transacoes["por_id"].get(i, 0.0) for i in (identificadores or []))


def roteiro_nao_fui_eu(achado, memoria):
    memoria.registrar(achado, "nao_fui_eu")
    nome = nome_da_contraparte(achado) or achado.get("titulo") or "não reconhecido"
    transacoes_ids = achado.get("transacoes") or []
    # Fato já traz o valor pronto. Suspeita não traz, e aí a contestação saía
    # com R$ 0,00, que é justamente o documento que a pessoa manda pro banco.
    valor = moeda(achado.get("valor") or valor_da_transacao(transacoes_ids))
    transacoes = ", ".join(transacoes_ids) or "sem identificador"
    texto = (
        "Contestação de transação não reconhecida\n\n"
        "Titular: Angela Nogueira, cabeleireira MEI.\n"
        "Lançamento: %s, no valor de %s.\n"
        "Referência no extrato: %s.\n\n"
        "Não reconheço essa movimentação e não autorizei essa transferência. "
        "Solicito a contestação e o estorno do valor, além do bloqueio preventivo "
        "de novas transferências para esse destinatário.\n\n"
        "Aguardo o número de protocolo." % (nome, valor, transacoes)
    )
    return [
        msg("Entendi, então vale contestar."),
        msg("<pre>%s</pre>" % escapar(texto), pausa=PAUSA_LONGA),
        msg("Manda isso pro seu banco pelo app ou pelo 0800. Eu não abro contestação no seu lugar, "
            "quem fala com o banco é você."),
        msg("Quando você mandar, me avisa. Eu marco a data e cobro se o estorno não cair em 10 dias."),
    ]


def roteiro_resumo(resultado):
    """O resumo do mês, pronto para a pessoa encaminhar para a contadora."""
    resumo = resultado.get("resumo", {})
    fatos = por_certeza(resultado, "fato")
    total = resumo.get("total_recuperavel")
    if total is None:
        total = sum(float(a.get("valor") or 0) for a in fatos)

    linhas = [
        "<b>Angela Nogueira, resumo do mês</b>",
        "",
        "Faturamento acumulado em 2026: <b>%s</b>" % moeda(resumo.get("faturamento_acumulado", 0)),
        "Teto do MEI: %s" % moeda(resumo.get("teto", 81000)),
        "Já usei: %s%% do teto" % str(resumo.get("percentual_do_teto", 0)).replace(".", ","),
        "Ainda cabe: <b>%s</b>" % moeda(resumo.get("falta_para_o_teto", 0)),
    ]
    if resumo.get("projecao_estouro"):
        linhas.append("No ritmo atual, o teto chega em <b>%s</b>"
                      % escapar(data_por_extenso(resumo["projecao_estouro"])))
    linhas += [
        "Movimentações conferidas: %d" % inteiro(resumo.get("qtd_transacoes_conferidas")),
        "Dinheiro saindo à toa, somado: <b>%s</b>" % moeda(total),
        "",
        "<b>O que precisa de atenção</b>",
    ]
    for achado in fatos + por_certeza(resultado, "regra"):
        marca = EMOJI.get(achado.get("certeza"), "•")
        valor = float(achado.get("valor") or 0)
        # Vários títulos já trazem o número dentro. Repetir no fim da linha polui.
        ja_tem = moeda(valor) in (achado.get("titulo") or "")
        sufixo = ", %s" % moeda(valor) if valor > 0 and not ja_tem else ""
        linhas.append("%s %s%s" % (marca, escapar(achado.get("titulo", "")), sufixo))
    linhas += ["", "Conferido %s. Os valores saem direto do extrato." % com_artigo("por")]

    return [
        msg("\n".join(linhas), pausa=PAUSA_LONGA),
        msg("Esse aqui é pra encaminhar pra sua contadora, do jeito que está. "
            "Se ela pedir os lançamentos, eu mando a lista."),
    ]


def roteiro_silencio(resultado):
    silenciados = resultado.get("silenciados", [])
    if not silenciados:
        mensagens = [msg("Desta vez não deixei nada de fora.")]
        return mensagens
    linhas = ["Coisas que apareceram e eu <b>não</b> te mandei, porque são normais pra você:", ""]
    for item in silenciados:
        titulo = escapar(item.get("titulo", ""))
        motivo = item.get("motivo") or primeira_frase(item.get("explicacao", ""))
        linhas.append("• <b>%s</b>\n%s" % (titulo, escapar(motivo)) if motivo else "• <b>%s</b>" % titulo)
    return [
        msg("\n".join(linhas), pausa=PAUSA_LONGA),
        msg("Conferir e ficar quieto também é trabalho. Você só ouve de mim o que muda alguma coisa."),
    ]


def roteiro_teto(resultado):
    resumo = resultado.get("resumo", {})
    mensagens = [
        msg("Você já faturou <b>%s</b> este ano, e ainda cabem <b>%s</b> até o teto." % (
            moeda(resumo.get("faturamento_acumulado", 0)), moeda(resumo.get("falta_para_o_teto", 0))))
    ]
    if resumo.get("projecao_estouro"):
        mensagens.append(msg("No ritmo dos últimos três meses, isso acaba em <b>%s</b>. "
                             "Dá tempo de decidir com calma."
                             % escapar(data_por_extenso(resumo["projecao_estouro"]))))
    return mensagens


def roteiro_livre(texto, resultado, memoria):
    """
    Qualquer outra mensagem. Sem menu de ajuda, sem lista de comandos secos.
    Ela entende a intenção e responde com um número ou com uma oferta.
    """
    limpo = sem_acento(texto)
    palavras_soltas = set(
        limpo.replace(",", " ").replace(".", " ").replace("?", " ").replace("!", " ").split())

    def tem(*pedacos):
        """Casa pedaço de palavra. Serve para raiz, tipo confer em conferir e conferiu."""
        return any(p in limpo for p in pedacos)

    def tem_palavra(*palavras):
        """Casa palavra inteira. Serve para palavra curta, que como pedaço casaria errado."""
        return any(p in palavras_soltas for p in palavras)

    if tem("obrigad", "valeu", "show", "otimo", "perfeito"):
        return [msg("De nada. Eu fico de olho, você cuida das suas clientes.")]

    pediu_para_agir = (
        (tem("pra mim", "por mim", "pra min")
         and tem("paga", "pague", "transf", "cancel", "contest", "manda", "envia", "resolv"))
        or tem("faz o pix", "faz um pix", "mexe na minha conta", "tira o dinheiro",
               "entra na minha conta", "paga o boleto", "paga o das")
    )
    if pediu_para_agir:
        return [
            msg("Isso eu não faço. Eu não mexo no seu dinheiro, não pago, não transfiro e não contesto "
                "no banco por você."),
            msg("O que eu faço é deixar tudo pronto pra você só apertar enviar. "
                "Quer que eu escreva o texto?"),
        ]

    if tem("teto", "fatur", "quanto entrou", "quanto ganhei", "quanto vendi", "quanto recebi"):
        # "quanto entrou por maquininha" não é pergunta de teto, é pergunta de
        # canal, e a IA responde isso com o número certo por canal. Com a IA
        # desligada nada muda: o teto continua sendo a melhor resposta que o bot
        # tem sozinho, e é ela que sai.
        pergunta_de_canal = tem("maquininha", "marketplace", "belezanet", "pix",
                                "boleto", "cartao", "credito", "debito", "canal")
        if not (pergunta_de_canal and ia_ligada()):
            return roteiro_teto(resultado)
        return roteiro_generico(resultado)

    if tem("silencio", "deixou passar", "nao mandou", "escondeu", "filtrou"):
        return roteiro_silencio(resultado)

    if tem("resumo", "contadora", "contador", "relatorio", "fechamento"):
        return roteiro_resumo(resultado)

    if tem("confer", "extrato", "achou", "achado", "olha ai", "ve ai", "print", "comprovante"):
        return roteiro_conferir(resultado, memoria)

    if tem_palavra("das", "imposto", "guia") or tem("imposto"):
        return roteiro_das(resultado)

    if tem_palavra("oi", "ola", "opa") or tem("bom dia", "boa tarde", "boa noite", "e ai"):
        resumo = resultado.get("resumo", {})
        return [
            msg("Oi. Tudo conferido por aqui."),
            msg("Você está com <b>%s</b> faturados no ano, e achei <b>%s</b> saindo à toa. "
                "Quer ver?" % (
                    moeda(resumo.get("faturamento_acumulado", 0)),
                    moeda(resumo.get("total_recuperavel", 0))),
                botoes=[botao("Ver o que eu achei", "conferir")]),
        ]

    return roteiro_generico(resultado)


def roteiro_generico(resultado):
    """
    A resposta de quando ela não entendeu. Fica marcada com generico=True, que é
    a deixa para o bot tentar a IA antes de mandar isso. Se a IA não estiver de
    pé, é exatamente a resposta que o bot já dava.
    """
    resumo = resultado.get("resumo", {})
    return [
        msg("Não peguei essa, mas te digo o que eu tenho na mão agora.", generico=True),
        msg("Faturou <b>%s</b> este ano e tem <b>%s</b> saindo à toa da sua conta. "
            "Posso abrir os achados, ou montar o resumo pra sua contadora." % (
                moeda(resumo.get("faturamento_acumulado", 0)),
                moeda(resumo.get("total_recuperavel", 0))),
            botoes=[botao("Ver o que eu achei", "conferir")],
            generico=True),
    ]


def roteiro_das(resultado):
    """O DAS sai dos achados, nunca de estimativa. Se o motor não falou, a Regis não sabe."""
    achados_das = [a for a in resultado.get("achados", [])
                   if "das" in sem_acento(a.get("titulo", "")).split()
                   or "das" in sem_acento(a.get("tipo", ""))]
    if achados_das:
        achado = achados_das[0]
        return [
            msg("Conferi os DAS do período e um deles precisa da sua atenção."),
            mensagem_de_fato(achado) if achado.get("certeza") == "fato" else mensagem_de_regra(achado),
        ]
    return [
        msg("Conferi os DAS do período e está tudo pago, um por competência."),
        msg("O do mês vence dia 20. Se chegar o dia 18 sem pagamento, eu te lembro sem você pedir."),
    ]


def roteiro_proxima_pergunta(resultado, memoria):
    """Depois que ela responde uma suspeita, a próxima entra. Uma de cada vez."""
    for achado in por_certeza(resultado, "suspeita"):
        if memoria.ja_respondeu(achado.get("id")) or memoria.conhece(contraparte_de(achado)):
            continue
        return [msg("Já que você está aqui, tem mais uma."), mensagem_de_suspeita(achado)]
    return []


# ---------------------------------------------------------------------------
# 5. A camada de canal (só aqui existe Telegram)
# ---------------------------------------------------------------------------

class Telegram:
    def __init__(self, token):
        self.token = token

    def chamar(self, metodo, **parametros):
        url = API.format(token=self.token, metodo=metodo)
        corpo = json.dumps(parametros).encode("utf-8")
        requisicao = urllib.request.Request(
            url, data=corpo, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(requisicao, timeout=TIMEOUT_HTTP) as resposta:
                return json.loads(resposta.read().decode("utf-8"))
        except urllib.error.HTTPError as erro:
            detalhe = ""
            try:
                detalhe = json.loads(erro.read().decode("utf-8")).get("description", "")
            except Exception:
                pass
            print("[regis] %s falhou: HTTP %s %s" % (metodo, erro.code, detalhe))
        except Exception as erro:
            print("[regis] %s falhou: %s" % (metodo, erro))
        return None

    def teclado(self, botoes):
        if not botoes:
            return None
        linhas = []
        for linha in botoes:
            linhas.append([{"text": b["texto"], "callback_data": b["data"]} for b in linha])
        return {"inline_keyboard": linhas}

    def enviar(self, chat_id, mensagem):
        parametros = {
            "chat_id": chat_id,
            "text": mensagem["texto"],
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        teclado = self.teclado(mensagem.get("botoes"))
        if teclado:
            parametros["reply_markup"] = teclado
        return self.chamar("sendMessage", **parametros)

    def digitando(self, chat_id):
        self.chamar("sendChatAction", chat_id=chat_id, action="typing")

    def responder_callback(self, callback_id, texto=None):
        parametros = {"callback_query_id": callback_id}
        if texto:
            parametros["text"] = texto
        self.chamar("answerCallbackQuery", **parametros)

    def updates(self, offset):
        return self.chamar(
            "getUpdates", offset=offset, timeout=TIMEOUT_POLL,
            allowed_updates=["message", "callback_query"])

    def registrar_comandos(self):
        self.chamar("setMyCommands", commands=[
            {"command": "start", "description": "quanto você já faturou este ano"},
            {"command": "conferir", "description": "o que eu achei no seu extrato"},
            {"command": "resumo", "description": "o resumo do mês pra sua contadora"},
            {"command": "teto", "description": "quanto ainda cabe antes do teto do MEI"},
            {"command": "silencio", "description": "o que eu achei e não te mandei"},
        ])


def ritmo():
    """
    REGIS_RITMO controla a pausa entre as mensagens. 1 é o ritmo de conversa,
    0 manda tudo de uma vez. Use 0.3 se o pitch estiver apertado de tempo.
    """
    try:
        return max(0.0, float(os.environ.get("REGIS_RITMO", "1")))
    except ValueError:
        return 1.0


def enviar_roteiro(telegram, chat_id, mensagens, via="deterministico"):
    """
    Manda o roteiro e registra cada fala.

    O registro acontece aqui, num lugar só, porque toda mensagem que a Regis
    manda passa por esta função. Assim nenhuma resposta escapa do histórico.
    """
    fator = ritmo()
    for mensagem in mensagens:
        pausa = mensagem.get("pausa", PAUSA_CURTA) * fator
        if pausa:
            telegram.digitando(chat_id)
            time.sleep(min(pausa, 2.5))
        telegram.enviar(chat_id, mensagem)
        registro.anotar(chat_id, "regis", mensagem.get("texto", ""), via=via)


# ---------------------------------------------------------------------------
# 6. A conversa livre com IA
# ---------------------------------------------------------------------------
#
# Ela só entra quando o determinístico não entendeu. Se falhar por qualquer
# motivo, o bot manda a resposta de sempre. A demo por comandos não depende
# disso em momento nenhum.

def ia_ligada():
    try:
        return conversa_ia is not None and conversa_ia.disponivel()
    except Exception as erro:
        print("[regis] conversa com IA indisponível (%s)." % erro)
        return False


def roteiro_ia(telegram, chat_id, texto):
    """
    Devolve as mensagens da IA, ou None para quem chamou voltar ao determinístico.

    O `digitando` sai antes da chamada porque a resposta demora alguns segundos,
    e sem ele a conversa parece travada.
    """
    if not ia_ligada():
        return None
    try:
        telegram.digitando(chat_id)
        resposta = conversa_ia.responder(
            texto, quem=str(chat_id), historico=registro.conversa(chat_id))
    except Exception as erro:
        print("[regis] a IA quebrou (%s). Voltando para o determinístico." % erro)
        return None
    if not resposta:
        return None
    # A IA escreve texto puro, sem marcação. O escape é obrigatório porque o
    # bot manda com parse_mode HTML.
    return [msg(escapar(resposta), pausa=0)]


# ---------------------------------------------------------------------------
# 7. Quem responde o quê
# ---------------------------------------------------------------------------

def tratar_mensagem(telegram, memoria, mensagem):
    chat_id = mensagem["chat"]["id"]
    texto = (mensagem.get("text") or mensagem.get("caption") or "").strip()
    resultado = rodar_motor()

    # Registra a fala da pessoa antes de responder. A ordem importa: o
    # histórico que vai para a IA precisa terminar na pergunta atual.
    quem = mensagem.get("from") or {}
    registro.anotar(chat_id, "pessoa", texto or "[anexo]",
                    nome=(quem.get("first_name") or ""),
                    via="anexo" if (mensagem.get("photo") or mensagem.get("document")) else "")

    if mensagem.get("photo") or mensagem.get("document"):
        enviar_roteiro(telegram, chat_id, [
            msg("Recebi. Deixa eu ler isso aqui."),
        ])
        enviar_roteiro(telegram, chat_id, roteiro_conferir(resultado, memoria))
        return

    comando = texto.split()[0].lower().split("@")[0] if texto.startswith("/") else ""

    if comando == "/start":
        enviar_roteiro(telegram, chat_id, roteiro_start(resultado), via=comando)
    elif comando == "/conferir":
        enviar_roteiro(telegram, chat_id, roteiro_conferir(resultado, memoria), via=comando)
    elif comando == "/resumo":
        enviar_roteiro(telegram, chat_id, roteiro_resumo(resultado), via=comando)
    elif comando in ("/silencio", "/silêncio"):
        enviar_roteiro(telegram, chat_id, roteiro_silencio(resultado), via="/silencio")
    elif comando == "/teto":
        enviar_roteiro(telegram, chat_id, roteiro_teto(resultado), via=comando)
    elif comando == "/esquecer":
        memoria.dados = {"contrapartes_conhecidas": [], "contrapartes_negadas": [], "respostas": {}}
        memoria.gravar()
        registro.esquecer(chat_id)
        enviar_roteiro(telegram, chat_id,
                       roteiro_start(resultado, recomecando=True), via=comando)
    else:
        mensagens = roteiro_livre(texto, resultado, memoria)
        via = "deterministico"
        # Só o caso genérico vira pergunta para a IA. Saudação, teto, DAS,
        # resumo e conferir continuam saindo do código, na velocidade de sempre.
        if any(m.get("generico") for m in mensagens):
            da_ia = roteiro_ia(telegram, chat_id, texto)
            if da_ia:
                mensagens = da_ia
                via = "ia"
            else:
                # Caiu no genérico e a IA não respondeu. É exatamente o que
                # interessa achar depois: pergunta que a Regis ainda não cobre.
                via = "sem_resposta"
        enviar_roteiro(telegram, chat_id, mensagens, via=via)


# O que cada botão quer dizer em português. Serve para o registro e para o
# histórico: no arquivo tem que estar escrito "Foi eu", não "sim:abc123".
FALA_DO_BOTAO = {
    "conferir": "Pode conferir",
    "ver": "Quero ver o texto",
    "sim": "Foi eu",
    "nao": "Não fui eu",
}


def tratar_callback(telegram, memoria, callback):
    dado = callback.get("data") or ""
    chat_id = callback["message"]["chat"]["id"]
    resultado = rodar_motor()

    quem = callback.get("from") or {}
    registro.anotar(chat_id, "pessoa",
                    FALA_DO_BOTAO.get(dado.partition(":")[0], dado),
                    nome=(quem.get("first_name") or ""), via="botao")

    if dado == "conferir":
        telegram.responder_callback(callback["id"])
        enviar_roteiro(telegram, chat_id, roteiro_conferir(resultado, memoria), via="botao")
        return

    acao, _, identificador = dado.partition(":")
    achado = achado_por_id(identificador)
    if not achado:
        telegram.responder_callback(callback["id"], "Esse achado sumiu, roda /conferir de novo.")
        return

    if acao == "ver":
        telegram.responder_callback(callback["id"])
        enviar_roteiro(telegram, chat_id, roteiro_acao(achado), via="botao")
    elif acao == "sim":
        telegram.responder_callback(callback["id"], "Anotado")
        enviar_roteiro(telegram, chat_id, roteiro_foi_eu(achado, memoria), via="botao")
        enviar_roteiro(telegram, chat_id, roteiro_proxima_pergunta(resultado, memoria), via="botao")
    elif acao == "nao":
        telegram.responder_callback(callback["id"])
        enviar_roteiro(telegram, chat_id, roteiro_nao_fui_eu(achado, memoria), via="botao")
        enviar_roteiro(telegram, chat_id, roteiro_proxima_pergunta(resultado, memoria), via="botao")
    else:
        telegram.responder_callback(callback["id"])


# ---------------------------------------------------------------------------
# 8. Long polling
# ---------------------------------------------------------------------------

def main():
    token = os.environ.get("TELEGRAM_TOKEN", "").strip()
    if not token:
        print("Falta o token. Rode assim:\n")
        print("    TELEGRAM_TOKEN=123456:ABC... python3 bot/regis_bot.py\n")
        print("O passo a passo para criar o bot está em bot/README.md.")
        return 1

    telegram = Telegram(token)
    eu = telegram.chamar("getMe")
    if not eu or not eu.get("ok"):
        print("O Telegram não aceitou esse token. Confira se copiou inteiro, "
              "incluindo os números antes dos dois pontos.")
        return 1
    usuario = eu["result"].get("username", "?")
    print("[regis] conectado como @%s, motor: %s" % (usuario, FONTE_MOTOR))

    rodar_motor()
    telegram.registrar_comandos()
    memoria = Memoria()
    print("[regis] memória em %s" % ARQUIVO_MEMORIA)
    lidas = registro.hidratar()
    numeros = registro.resumo()
    print("[regis] registro em %s (%s mensagens, %s conversas, %s recarregadas)"
          % (numeros["arquivo"], numeros["mensagens"], numeros["conversas"], lidas))
    print("[regis] escutando. Abra o Telegram, procure @%s e mande /start." % usuario)

    offset = 0
    espera = 1
    while True:
        try:
            resposta = telegram.updates(offset)
            if not resposta or not resposta.get("ok"):
                time.sleep(espera)
                espera = min(espera * 2, 30)
                continue
            espera = 1
            for update in resposta.get("result", []):
                offset = update["update_id"] + 1
                try:
                    if "message" in update:
                        tratar_mensagem(telegram, memoria, update["message"])
                    elif "callback_query" in update:
                        tratar_callback(telegram, memoria, update["callback_query"])
                except Exception as erro:
                    print("[regis] erro tratando update %s: %s" % (update.get("update_id"), erro))
        except KeyboardInterrupt:
            print("\n[regis] até logo.")
            return 0
        except Exception as erro:
            print("[regis] erro no loop: %s" % erro)
            time.sleep(2)


if __name__ == "__main__":
    sys.exit(main())
