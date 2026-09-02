# -*- coding: utf-8 -*-
"""
Conversa livre da Regis, com IA e ferramentas.

O bot continua determinístico onde já era. Este módulo entra só quando a pessoa
pergunta uma coisa que os comandos não cobrem.

A regra que manda aqui: **a Regis nunca inventa um número**. O modelo não recebe
resumo mastigado no prompt, ele recebe ferramentas que leem `motor/` e `dados/`
e devolvem texto curto e factual. Se as ferramentas não respondem, ela diz que
não sabe. É por isso que a resposta é tool use e não geração livre.

Como usar:

    from conversa_ia import disponivel, responder
    if disponivel():
        texto = responder("quanto entrou por maquininha em agosto?", quem=chat_id)

`responder` devolve:

  * o texto da Regis, quando deu certo
  * uma frase educada, quando o teto de gasto estourou
  * uma frase honesta, quando o modelo recusou
  * `None`, quando faltou chave, faltou rede, o SDK não está instalado ou deu
    erro. Nesse caso quem chamou volta para a resposta determinística de hoje.

O SDK é opcional de propósito. Sem `pip install anthropic` o módulo importa,
`disponivel()` devolve False e o bot roda igual ao que rodava antes.

Variáveis de ambiente:

    ANTHROPIC_API_KEY    a chave. Sem ela, a IA fica desligada.
    REGIS_LIMITE_HORA    chamadas por pessoa por hora, padrão 20
    REGIS_TETO_USD       teto de gasto estimado da sessão, padrão 5.00
"""

import os
import sys
import time
import unicodedata

# ---------------------------------------------------------------------------
# 0. O SDK é opcional. Sem ele o bot continua de pé, só sem conversa livre.
# ---------------------------------------------------------------------------

try:
    import anthropic
    from anthropic import beta_tool
    SDK_PRESENTE = True
except Exception:  # SDK não instalado, ou instalado quebrado
    anthropic = None
    SDK_PRESENTE = False

    def beta_tool(funcao):
        """Decorador de mentira, só para o módulo importar sem o SDK."""
        return funcao


AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PASTA_DADOS = os.path.join(RAIZ, "dados")

MODELO = "claude-opus-5"
MAX_TOKENS = 16000
MAX_ITERACOES = 8

# Preço do Opus 5, dólares por milhão de tokens.
PRECO_ENTRADA = 5.00
PRECO_SAIDA = 25.00


def _inteiro_do_ambiente(nome, padrao):
    try:
        return max(0, int(float(os.environ.get(nome, padrao))))
    except (TypeError, ValueError):
        return padrao


def _decimal_do_ambiente(nome, padrao):
    try:
        return max(0.0, float(os.environ.get(nome, padrao)))
    except (TypeError, ValueError):
        return padrao


LIMITE_HORA = _inteiro_do_ambiente("REGIS_LIMITE_HORA", 20)
TETO_USD = _decimal_do_ambiente("REGIS_TETO_USD", 5.00)


# ---------------------------------------------------------------------------
# 1. Os dados, carregados uma vez só
# ---------------------------------------------------------------------------
#
# Ferramenta não abre arquivo. Ela pergunta para o cache do módulo, que carrega
# na primeira vez e guarda. São 367 transações, não faz sentido reler a cada
# chamada de tool dentro da mesma resposta.

_cache = {"pacote": None, "identificacoes": None, "motor": None}
_motor_ok = {"valor": None}


def _importar_motor():
    if RAIZ not in sys.path:
        sys.path.insert(0, RAIZ)
    from motor import dados as motor_dados          # noqa: WPS433
    from motor.detectar import detectar             # noqa: WPS433
    from motor.identificar import identificar_todas  # noqa: WPS433
    return motor_dados, detectar, identificar_todas


def _carregar():
    """Carrega extrato, vendas e identificação de contraparte. Uma vez por processo."""
    if _cache["pacote"] is None:
        motor_dados, _, identificar_todas = _importar_motor()
        pacote = motor_dados.carregar(PASTA_DADOS)
        _cache["pacote"] = pacote
        _cache["identificacoes"] = identificar_todas(pacote["transacoes"], pacote["contexto"])
    return _cache["pacote"], _cache["identificacoes"]


def _achados():
    """Roda o motor uma vez e guarda o resultado."""
    if _cache["motor"] is None:
        _, detectar, _ = _importar_motor()
        _cache["motor"] = detectar(PASTA_DADOS)
    return _cache["motor"]


def motor_disponivel():
    """True quando dá para ler os dados de verdade. Sem isso não existe conversa com IA."""
    if _motor_ok["valor"] is None:
        try:
            _carregar()
            _achados()
            _motor_ok["valor"] = True
        except Exception as erro:
            print("[regis-ia] sem motor para as ferramentas (%s)" % erro)
            _motor_ok["valor"] = False
    return _motor_ok["valor"]


# ---------------------------------------------------------------------------
# 2. Formatação e filtros, compartilhados pelas ferramentas
# ---------------------------------------------------------------------------

MESES_PT = ("janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")


def _moeda(valor):
    from motor.dados import moeda
    return moeda(valor or 0)


def _data_br(iso):
    return "%s/%s/%s" % (iso[8:10], iso[5:7], iso[0:4])


def _percentual(valor):
    """72,1% em vez de 72.1%, porque a pessoa lê com vírgula."""
    return ("%.1f%%" % (valor or 0)).replace(".", ",")


def _plural(quantidade, singular, plural):
    return "%s %s" % (quantidade, singular if quantidade == 1 else plural)


def _sem_acento(texto):
    limpo = unicodedata.normalize("NFKD", str(texto or ""))
    return "".join(c for c in limpo if not unicodedata.combining(c)).lower()


def _nome(transacao):
    """Quem está do outro lado, já traduzido pelo motor. O campo cru do extrato mente às vezes."""
    _, identificacoes = _carregar()
    identificacao = identificacoes.get(transacao["id"])
    if identificacao and identificacao.get("nome"):
        return identificacao["nome"]
    return transacao.get("contraparte") or transacao.get("descritor_bruto") or "sem nome"


def _mes_da(transacao):
    return transacao["data"][:7]


def _normalizar_mes(mes):
    """Aceita 2026-08, 08, agosto ou todos. Devolve 2026-08 ou None para o período inteiro."""
    pacote, _ = _carregar()
    ano = pacote["data_referencia"].year
    bruto = _sem_acento(mes).strip()
    if not bruto or bruto in ("todos", "todo", "tudo", "ano", "periodo", "geral", str(ano)):
        return None
    partes = bruto.split("-")
    if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
        return "%04d-%02d" % (int(partes[0]), int(partes[1]))
    if bruto.isdigit() and 1 <= int(bruto) <= 12:
        return "%04d-%02d" % (ano, int(bruto))
    for numero, nome in enumerate(MESES_PT, start=1):
        if _sem_acento(nome) in bruto:
            return "%04d-%02d" % (ano, numero)
    return None


def _mes_por_extenso(chave):
    ano, _, mes = chave.partition("-")
    return "%s de %s" % (MESES_PT[int(mes) - 1], ano)


def _no_mes(transacoes, chave):
    if not chave:
        return list(transacoes)
    return [t for t in transacoes if _mes_da(t) == chave]


def _rotulo_do_periodo(chave):
    if chave:
        return _mes_por_extenso(chave)
    pacote, _ = _carregar()
    periodo = pacote["meta"].get("periodo_detalhado", {})
    if periodo:
        return "%s a %s" % (_data_br(periodo["inicio"]), _data_br(periodo["fim"]))
    return "o período do extrato"


CANAL_LEGIVEL = {
    "maquininha_credito": "maquininha (crédito)",
    "maquininha_debito": "maquininha (débito)",
    "marketplace": "marketplace BelezaNet",
    "pix": "Pix",
    "boleto": "boleto",
    "debito_automatico": "débito automático",
}


CATEGORIA_LEGIVEL = {
    "venda": "venda",
    "repasse": "repasse do marketplace",
    "antecipacao": "taxa de antecipação",
    "insumo": "fornecedor de insumo",
    "assinatura": "assinatura",
    "pessoal": "gasto pessoal",
    "utilidade": "conta de consumo",
    "imposto": "imposto",
    "aluguel": "aluguel",
    "tarifa": "tarifa do banco",
    "nao_classificado": "sem categoria",
}


# ---------------------------------------------------------------------------
# 3. As ferramentas
# ---------------------------------------------------------------------------
#
# Cada uma devolve texto curto e factual. Nenhuma inventa, nenhuma estima e
# nenhuma move dinheiro. Quando não tem o dado, ela diz que não tem.

@beta_tool
def resumo_do_ano() -> str:
    """Números do ano fechados pelo motor.

    Use quando a pessoa perguntar quanto faturou, quanto falta para o teto do MEI,
    quando o teto estoura ou quanto ela tem para recuperar. É a primeira ferramenta
    a chamar quando a pergunta for ampla, do tipo "como estou".
    """
    resultado = _achados()
    resumo = resultado.get("resumo", {})
    pacote, _ = _carregar()
    periodo = pacote["meta"].get("periodo_detalhado", {})
    projecao = resumo.get("projecao_estouro")

    linhas = [
        "Faturamento acumulado em 2026: %s, que é %s do teto de %s."
        % (_moeda(resumo.get("faturamento_acumulado")),
           _percentual(resumo.get("percentual_do_teto")),
           _moeda(resumo.get("teto"))),
        "Falta %s para bater o teto." % _moeda(resumo.get("falta_para_o_teto")),
        "Projeção de estouro no ritmo dos últimos três meses: %s."
        % (_data_br(projecao) if projecao else "não estoura neste ano"),
        "Total recuperável hoje, somando só os achados de certeza fato: %s."
        % _moeda(resumo.get("total_recuperavel")),
        "Transações conferidas: %s." % resumo.get("qtd_transacoes_conferidas"),
    ]
    if periodo:
        linhas.append(
            "O extrato detalhado vai de %s a %s. Janeiro a maio entram consolidados por mês."
            % (_data_br(periodo["inicio"]), _data_br(periodo["fim"])))
    return "\n".join(linhas)


@beta_tool
def listar_achados(certeza: str = "todos") -> str:
    """Os achados do motor, com título, explicação e valor.

    Use quando a pessoa pedir o que você achou, pedir explicação de uma cobrança,
    de uma taxa, de uma assinatura ou de uma duplicidade. A explicação já vem
    pronta e checada, não reescreva o número.

    Args:
        certeza: "fato" para o que é certo, "regra" para o que a lei ou o contrato
            diz, "suspeita" para o que precisa da confirmação dela, "todos" para tudo.
    """
    resultado = _achados()
    filtro = _sem_acento(certeza).strip() or "todos"
    itens = resultado.get("achados", [])
    if filtro in ("fato", "regra", "suspeita"):
        itens = [a for a in itens if a.get("certeza") == filtro]

    if not itens:
        return "Não tem achado nenhum nessa faixa de certeza."

    blocos = []
    for item in itens:
        valor = _moeda(item["valor"]) if item.get("valor") is not None else "sem valor direto"
        cabeca = "[%s] certeza %s, tipo %s, %s" % (
            item["id"], item["certeza"], item["tipo"], valor)
        corpo = "%s\n%s" % (item["titulo"], item["explicacao"])
        if item.get("acao"):
            corpo += "\nAção pronta para a pessoa enviar: %s" % item["acao"]["titulo"]
        blocos.append("%s\n%s" % (cabeca, corpo))
    return "\n\n".join(blocos)


@beta_tool
def total_por_canal(mes: str = "todos") -> str:
    """Quanto dinheiro entrou por cada canal: maquininha, marketplace, Pix, boleto.

    Use quando a pergunta for sobre origem do faturamento, do tipo "quanto entrou
    por maquininha", "quanto veio do BelezaNet" ou "quanto foi no Pix". Devolve o
    valor bruto (o que a cliente pagou) e o líquido (o que caiu na conta).

    Args:
        mes: "2026-08" para um mês só, ou "todos" para o extrato detalhado inteiro.
    """
    pacote, _ = _carregar()
    chave = _normalizar_mes(mes)
    entradas = [t for t in _no_mes(pacote["transacoes"], chave) if t["tipo"] == "entrada"]

    if not entradas:
        return "Não tem entrada nenhuma em %s dentro do extrato que eu li." % _rotulo_do_periodo(chave)

    por_canal = {}
    for transacao in entradas:
        bolso = por_canal.setdefault(transacao["canal"], {"qtd": 0, "bruto": 0.0, "liquido": 0.0})
        bolso["qtd"] += 1
        bolso["liquido"] += transacao["valor"]
        bolso["bruto"] += transacao.get("valor_bruto_venda") or transacao["valor"]

    ordem = sorted(por_canal.items(), key=lambda par: -par[1]["bruto"])
    linhas = ["Entradas em %s:" % _rotulo_do_periodo(chave)]
    for canal, bolso in ordem:
        linhas.append("%s: %s, %s bruto, %s caiu na conta"
                      % (CANAL_LEGIVEL.get(canal, canal),
                         _plural(bolso["qtd"], "lançamento", "lançamentos"),
                         _moeda(bolso["bruto"]), _moeda(bolso["liquido"])))
    linhas.append("Total: %s bruto, %s caiu na conta"
                  % (_moeda(sum(b["bruto"] for _, b in ordem)),
                     _moeda(sum(b["liquido"] for _, b in ordem))))
    linhas.append("Bruto é o que a cliente pagou. Líquido é o que sobrou depois da taxa.")
    return "\n".join(linhas)


@beta_tool
def maiores_saidas(quantidade: int = 5, mes: str = "todos") -> str:
    """As maiores saídas do período, com data, contraparte, valor e categoria.

    Use quando a pergunta for sobre gasto: maior gasto, com quem ela mais gastou,
    para onde o dinheiro foi. Junto vem o total por categoria do período, que serve
    para responder quanto ela gastou com fornecedor, com assinatura ou com imposto.

    Args:
        quantidade: quantas saídas listar, da maior para a menor.
        mes: "2026-08" para um mês só, ou "todos" para o extrato detalhado inteiro.
    """
    pacote, _ = _carregar()
    chave = _normalizar_mes(mes)
    saidas = [t for t in _no_mes(pacote["transacoes"], chave) if t["tipo"] == "saida"]

    if not saidas:
        return "Não tem saída nenhuma em %s dentro do extrato que eu li." % _rotulo_do_periodo(chave)

    quantas = max(1, min(int(quantidade or 5), len(saidas)))
    ordenadas = sorted(saidas, key=lambda t: -t["valor"])[:quantas]

    linhas = ["As %s maiores saídas de %s:" % (quantas, _rotulo_do_periodo(chave))]
    for transacao in ordenadas:
        linhas.append("%s, %s, %s (%s)" % (
            _data_br(transacao["data"]), _nome(transacao), _moeda(transacao["valor"]),
            CATEGORIA_LEGIVEL.get(transacao["categoria"], transacao["categoria"])))

    por_categoria = {}
    for transacao in saidas:
        bolso = por_categoria.setdefault(transacao["categoria"], {"qtd": 0, "total": 0.0})
        bolso["qtd"] += 1
        bolso["total"] += transacao["valor"]

    linhas.append("")
    linhas.append("Total de saídas em %s: %s em %s."
                  % (_rotulo_do_periodo(chave),
                     _moeda(sum(t["valor"] for t in saidas)),
                     _plural(len(saidas), "lançamento", "lançamentos")))
    linhas.append("Por categoria:")
    for categoria, bolso in sorted(por_categoria.items(), key=lambda par: -par[1]["total"]):
        linhas.append("%s: %s em %s"
                      % (CATEGORIA_LEGIVEL.get(categoria, categoria),
                         _moeda(bolso["total"]),
                         _plural(bolso["qtd"], "lançamento", "lançamentos")))
    return "\n".join(linhas)


@beta_tool
def buscar_transacoes(termo: str, limite: int = 10) -> str:
    """Procura lançamentos por nome de contraparte ou por descritor do extrato.

    Use quando a pessoa citar um nome, uma loja, uma empresa ou um pedaço do
    descritor e você precisar ver os lançamentos antes de responder.

    Args:
        termo: o nome ou pedaço de texto a procurar, por exemplo "cielo" ou "netflix".
        limite: quantos lançamentos devolver, do mais recente para o mais antigo.
    """
    pacote, _ = _carregar()
    alvo = _sem_acento(termo).strip()
    if not alvo:
        return "Preciso de um termo para procurar."

    encontradas = []
    for transacao in pacote["transacoes"]:
        campos = " ".join([
            _sem_acento(_nome(transacao)),
            _sem_acento(transacao.get("descritor_bruto")),
            _sem_acento(transacao.get("contraparte")),
        ])
        if alvo in campos:
            encontradas.append(transacao)

    if not encontradas:
        return "Não achei nenhum lançamento com \"%s\" no extrato que eu li." % termo

    quantas = max(1, min(int(limite or 10), len(encontradas)))
    recentes = sorted(encontradas, key=lambda t: t["data"], reverse=True)[:quantas]

    linhas = ["%s lançamentos casam com \"%s\". Mostrando %s, do mais recente:"
              % (len(encontradas), termo, quantas)]
    for transacao in recentes:
        linhas.append("%s, %s, %s de %s, %s (%s)" % (
            transacao["id"], _data_br(transacao["data"]), transacao["tipo"],
            _moeda(transacao["valor"]), _nome(transacao),
            CATEGORIA_LEGIVEL.get(transacao["categoria"], transacao["categoria"])))
    entradas = sum(t["valor"] for t in encontradas if t["tipo"] == "entrada")
    saidas = sum(t["valor"] for t in encontradas if t["tipo"] == "saida")
    linhas.append("Somando todos os %s: %s de entrada e %s de saída."
                  % (len(encontradas), _moeda(entradas), _moeda(saidas)))
    return "\n".join(linhas)


@beta_tool
def gastos_com(contraparte: str) -> str:
    """Quanto ela já pagou para uma contraparte no período, e quantas vezes.

    Use quando a pergunta for "quanto eu já paguei para X" ou "quanto a X me
    custou". Só conta saída. Se aquela contraparte também mandou dinheiro, isso
    aparece no fim, separado.

    Args:
        contraparte: o nome de quem recebeu, por exemplo "Beleza Distribuidora".
    """
    pacote, _ = _carregar()
    alvo = _sem_acento(contraparte).strip()
    if not alvo:
        return "Preciso do nome de quem recebeu."

    casadas = [t for t in pacote["transacoes"]
               if alvo in _sem_acento(_nome(t)) or alvo in _sem_acento(t.get("descritor_bruto"))]
    saidas = [t for t in casadas if t["tipo"] == "saida"]

    if not saidas:
        if casadas:
            return ("Não saiu nada para \"%s\" no extrato que eu li. Ela só aparece "
                    "recebendo, em %s." % (contraparte,
                                           _plural(len(casadas), "lançamento", "lançamentos")))
        return "Não achei \"%s\" no extrato que eu li." % contraparte

    nomes = sorted({_nome(t) for t in saidas})
    total = sum(t["valor"] for t in saidas)
    datas = sorted(t["data"] for t in saidas)
    valores = sorted(t["valor"] for t in saidas)

    linhas = [
        "Saídas para %s em %s:" % (", ".join(nomes), _rotulo_do_periodo(None)),
        "Total: %s em %s." % (_moeda(total), _plural(len(saidas), "pagamento", "pagamentos")),
        "Primeiro em %s, último em %s." % (_data_br(datas[0]), _data_br(datas[-1])),
        "Menor pagamento %s, maior %s." % (_moeda(valores[0]), _moeda(valores[-1])),
    ]
    for transacao in sorted(saidas, key=lambda t: t["data"], reverse=True)[:10]:
        linhas.append("%s, %s (%s)" % (
            _data_br(transacao["data"]), _moeda(transacao["valor"]),
            CATEGORIA_LEGIVEL.get(transacao["categoria"], transacao["categoria"])))
    entradas = [t for t in casadas if t["tipo"] == "entrada"]
    if entradas:
        linhas.append("Essa mesma contraparte também mandou %s para você, em %s."
                      % (_moeda(sum(t["valor"] for t in entradas)),
                         _plural(len(entradas), "lançamento", "lançamentos")))
    return "\n".join(linhas)


@beta_tool
def o_que_calei() -> str:
    """O que o motor conferiu, achou normal e escolheu não falar, com o motivo.

    Use quando a pessoa perguntar o que você deixou passar, o que você escondeu,
    o que estava tudo certo ou o que você conferiu e não mandou.
    """
    resultado = _achados()
    silenciados = resultado.get("silenciados", [])
    if not silenciados:
        return "Não silenciei nada neste período."
    linhas = ["Conferi e escolhi não falar, porque estava tudo dentro do combinado:"]
    for item in silenciados:
        motivo = item.get("motivo") or item.get("explicacao") or ""
        linhas.append("[%s] %s\n%s" % (item["id"], item["titulo"], motivo))
    return "\n".join(linhas)


FERRAMENTAS = [
    resumo_do_ano,
    listar_achados,
    total_por_canal,
    maiores_saidas,
    buscar_transacoes,
    gastos_com,
    o_que_calei,
]


# ---------------------------------------------------------------------------
# 4. O prompt de sistema
# ---------------------------------------------------------------------------

PROMPT_SISTEMA = """Você é a Regis. Você confere o dinheiro que entra e sai da conta de quem trabalha por conta própria como MEI, e avisa quando alguma coisa não bate.

Nunca se chame de autopilot, de agente, de assistente virtual, de IA ou de bot. Ninguém fala assim, e quem está do outro lado não quer saber o que você é, quer saber o que você faz por ela. Se perguntarem quem você é, responda pelo que você faz: você lê o extrato dela todo dia e avisa quando cobram errado.

Quem está do outro lado é Angela Nogueira, cabeleireira MEI em Campinas (SP). Ela não é dona de salão: aluga uma cadeira no Studio Bella e atende a própria clientela lá dentro, então o aluguel de R$ 1.850 que sai todo dia 5 é o aluguel da cadeira dela. Trate por você, no feminino. Os dados são de uma persona de demonstração, sintéticos, mas você responde como se fossem dela.

Como você fala:
Português do Brasil, direto, curto. Isso é WhatsApp, não relatório. Duas ou três frases resolvem quase tudo, e cinco já é longo demais. Nada de lista com marcador, nada de título, nada de markdown, nada de HTML. Texto corrido.
Você fala como gente: "achei R$ 47 saindo à toa", nunca "detectamos uma anomalia". Sem jargão de banco, sem "conforme identificado", sem "prezada".
Nunca use travessão nem hífen separando frases. Use vírgula, parênteses ou ponto final.
Uma pergunta por vez, no máximo. Melhor nenhuma.

O que você não faz:
Você nunca inventa um número. Todo valor que sair da sua boca veio de uma ferramenta que acabou de ler os dados reais. Se a ferramenta não devolveu aquele número, você não tem aquele número, e diz isso sem rodeio: "isso eu não sei te dizer". Não estime, não arredonde por conta própria, não some cabeça com cabeça.
Você não move dinheiro. Não paga, não transfere, não cancela cartão e não abre contestação no banco. O que você faz é deixar o texto pronto para a pessoa só apertar enviar. Se pedirem para você pagar, transferir ou resolver com o banco, recuse com naturalidade e ofereça o texto pronto.
Você não dá conselho de investimento. Não fala se vale a pena comprar, aplicar ou investir em nada, nem em cripto, nem em ação, nem em fundo. Diz que isso não é a sua praia e volta para o que você faz, que é conferir o dinheiro que entra e sai.
Você não julga e não acusa. Quando achar algo estranho, desarma em vez de alarmar: pode ter sido ela mesma, pode ter sido agendamento. Você mostra e pergunta, não aponta o dedo.

Como você trabalha:
Antes de responder qualquer coisa que envolva número, chame as ferramentas. Chame quantas precisar. Só depois escreva.
Existem três níveis de certeza nos achados. Fato é o que é certo, você fala com confiança. Regra é o que a lei ou o contrato diz, você fala com tom de "você decide". Suspeita é o que depende da confirmação dela, você pergunta com leveza.
Quando um valor der para recuperar, diga isso, porque é a boa notícia.
Se a pergunta não tiver nada a ver com o dinheiro dela, responda curto e traga de volta para o que você faz."""


# ---------------------------------------------------------------------------
# 5. Teto de gasto
# ---------------------------------------------------------------------------
#
# A chave é do time. Depois que o link do bot circular, qualquer pessoa gasta o
# crédito do time. São poucas linhas e evitam acordar com o crédito zerado.

_gasto = {"usd": 0.0, "chamadas": 0}
_janela = {}  # quem -> lista de instantes das chamadas da última hora


def _liberar(quem):
    """Devolve (pode, frase). A frase só existe quando não pode."""
    agora = time.time()
    recentes = [t for t in _janela.get(quem, []) if agora - t < 3600]
    _janela[quem] = recentes

    if LIMITE_HORA and len(recentes) >= LIMITE_HORA:
        return False, ("Falei bastante nesta última hora. Daqui a pouco eu volto a "
                       "responder pergunta solta. Os comandos continuam valendo, "
                       "pode mandar /conferir ou /resumo.")

    if TETO_USD and _gasto["usd"] >= TETO_USD:
        return False, ("Por hoje eu já usei o que tinha para conversar solta. "
                       "Os comandos continuam de pé, manda /conferir ou /resumo "
                       "que eu te mostro tudo.")

    return True, None


def _contabilizar(entrada, saida):
    custo = (entrada / 1000000.0) * PRECO_ENTRADA + (saida / 1000000.0) * PRECO_SAIDA
    _gasto["usd"] += custo
    _gasto["chamadas"] += 1
    print("[regis-ia] entrada %s tokens, saída %s tokens, custo estimado US$ %.4f, "
          "acumulado US$ %.4f de US$ %.2f"
          % (entrada, saida, custo, _gasto["usd"], TETO_USD))
    return custo


def gasto_estimado():
    """Quanto a sessão já gastou, em dólar. Serve para log e para teste."""
    return dict(_gasto)


# ---------------------------------------------------------------------------
# 6. A chamada
# ---------------------------------------------------------------------------

_cliente = {"valor": None}


def _obter_cliente():
    if _cliente["valor"] is None:
        _cliente["valor"] = anthropic.Anthropic()
    return _cliente["valor"]


def disponivel():
    """True quando dá para chamar a IA: SDK instalado, chave no ambiente e motor de pé."""
    if not SDK_PRESENTE:
        return False
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        return False
    return motor_disponivel()


def _texto_da(mensagem):
    if mensagem is None:
        return ""
    pedacos = []
    for bloco in getattr(mensagem, "content", []) or []:
        if getattr(bloco, "type", None) == "text":
            pedacos.append(bloco.text)
    return "\n\n".join(p.strip() for p in pedacos if p and p.strip()).strip()


def _montar_mensagens(pergunta, historico):
    """
    Monta a conversa que vai para o modelo.

    Sem histórico, manda só a pergunta, que era o comportamento antigo. Com
    histórico, ele já vem fundido e alternado do `registro`, e a última fala
    dele é a pergunta atual. Se por algum motivo não for, a pergunta entra no
    fim, porque a conversa precisa terminar com a pessoa falando.
    """
    mensagens = [m for m in (historico or []) if m.get("content")]
    if not mensagens or mensagens[-1].get("role") != "user":
        mensagens.append({"role": "user", "content": pergunta})
    return mensagens


def responder(pergunta, quem="anonimo", historico=None):
    """
    Responde uma pergunta livre usando as ferramentas.

    `historico` são os turnos anteriores desta mesma conversa. Sem ele a Regis
    não lembra do que acabou de dizer, e "e o outro?" vira uma pergunta sem
    sentido para o modelo.

    Devolve texto quando tem o que dizer, e None quando quem chamou deve voltar
    para a resposta determinística.
    """
    if not disponivel():
        return None

    pergunta = (pergunta or "").strip()
    if not pergunta:
        return None

    pode, recado = _liberar(quem)
    if not pode:
        return recado

    _janela.setdefault(quem, []).append(time.time())

    entrada_total = 0
    saida_total = 0
    ultima = None

    try:
        runner = _obter_cliente().beta.messages.tool_runner(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            system=PROMPT_SISTEMA,
            tools=FERRAMENTAS,
            messages=_montar_mensagens(pergunta, historico),
            output_config={"effort": "low"},
            max_iterations=MAX_ITERACOES,
        )
        for mensagem in runner:
            ultima = mensagem
            uso = getattr(mensagem, "usage", None)
            if uso is not None:
                entrada_total += getattr(uso, "input_tokens", 0) or 0
                saida_total += getattr(uso, "output_tokens", 0) or 0
    except Exception as erro:
        if entrada_total or saida_total:
            _contabilizar(entrada_total, saida_total)
        print("[regis-ia] a chamada falhou (%s). Voltando para o determinístico." % erro)
        return None

    _contabilizar(entrada_total, saida_total)

    # A última mensagem que o runner rendeu já é a resposta final. O `messages`
    # é só uma rede de segurança para versão futura do SDK, e só vale se o que
    # está lá no fim for mesmo uma fala dela.
    final = ultima
    guardadas = getattr(runner, "messages", None)
    if guardadas and getattr(guardadas[-1], "role", None) == "assistant":
        final = guardadas[-1]

    parada = getattr(final, "stop_reason", None)
    if parada == "refusal":
        return ("Essa eu prefiro não responder. Sobre o dinheiro que entra e sai da "
                "sua conta eu falo à vontade, é pra isso que eu estou aqui.")

    texto = _texto_da(final)
    if not texto:
        return None
    return texto
