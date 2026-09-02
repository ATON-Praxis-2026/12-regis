"""Identificação de contraparte.

Traduz o descritor sujo do extrato ("PAG*BELEZANET", "MP *SALAO", "CIELO*CRED 4829")
no nome que a pessoa reconhece. É a peça número 1 da ordem de construção do briefing,
porque todos os outros detectores dependem de saber quem é quem.

Determinístico de propósito. Usa três fontes de sinal, nesta ordem:
  1. padrões de descritor (gateway, imposto, tarifa, antecipação, Pix de QR)
  2. o histórico declarado em contexto.contrapartes_conhecidas
  3. o canal da transação cruzado com os contratos do contexto (adquirente, marketplace)
"""

try:
    from .dados import normalizar
except ImportError:  # execução direta, sem pacote
    from dados import normalizar

# Prefixos de gateway de pagamento. O nome do estabelecimento vem depois do asterisco
# e quase nunca é o nome que a pessoa conhece.
GATEWAYS = {
    "PAG": "PagSeguro",
    "PAGS": "PagSeguro",
    "MP": "Mercado Pago",
    "MERCPAGO": "Mercado Pago",
    "PICPAY": "PicPay",
    "IUGU": "Iugu",
    "STONE": "Stone",
    "EBANX": "EBANX",
    "SUMUP": "SumUp",
}

# Palavras que o banco escreve e que não dizem quem é a contraparte.
RUIDO = {
    "PIX", "ENV", "ENVIADO", "ENVIO", "REC", "RECEBIDO", "RECEB", "QR", "QRS",
    "ESTATICO", "DINAMICO", "CPF", "CNPJ", "PAGTO", "PAGAMENTO", "BOLETO",
    "DEB", "DEBITO", "CRED", "CREDITO", "AUT", "AUTOMATICO", "TED", "DOC",
    "TRANSF", "TRANSFERENCIA", "COMPRA", "CARTAO", "TAR", "TARIFA", "MANUT",
    "MANUTENCAO", "PACOTE", "PARC", "LOJA", "BRA", "BR",
}

# Rótulo legível para o canal, para o texto não falar em snake_case com a pessoa.
CANAL_LEGIVEL = {
    "maquininha_credito": "maquininha, crédito",
    "maquininha_debito": "maquininha, débito",
    "marketplace": "marketplace",
    "pix": "Pix",
    "boleto": "boleto",
    "debito_automatico": "débito automático",
}


def identificar(descritor_bruto, canal=None, contexto=None, tipo=None):
    """Devolve quem é a contraparte por trás de um descritor de extrato.

    Retorna um dicionário com nome, canal legível, gateway, natureza,
    grau de confiança, a pista que levou até ali e se já tem histórico.
    """
    contexto = contexto or {}
    conhecidas = contexto.get("contrapartes_conhecidas", []) or []
    bruto = descritor_bruto or ""
    texto = normalizar(bruto)
    gateway, nucleo = _separar_gateway(texto)
    tokens = _tokens_uteis(nucleo)

    especial = (
        _regra_imposto(texto, contexto)
        or _regra_tarifa_da_conta(texto, contexto)
        or _regra_antecipacao(texto, contexto)
    )
    if especial:
        especial.update(_moldura(bruto, canal, gateway))
        especial["conhecida"] = _tem_historico(especial["nome"], conhecidas)
        return especial

    nome, pontuacao = _casar_com_historico(tokens, nucleo, conhecidas)
    if nome:
        resultado = {
            "nome": nome,
            "natureza": "empresa",
            "confianca": "alta" if pontuacao >= 0.99 else "media",
            "pista": _pista_historico(gateway, pontuacao),
        }
        resultado.update(_moldura(bruto, canal, gateway))
        resultado["conhecida"] = True
        return resultado

    entrada_de_pix_sem_nome = (
        canal == "pix" and tipo == "entrada" and not tokens
    )
    if entrada_de_pix_sem_nome or (canal == "pix" and tipo == "entrada" and _so_numero(nucleo)):
        resultado = {
            "nome": "Cliente do salão",
            "natureza": "cliente",
            "confianca": "media",
            "pista": "Pix recebido no QR do balcão, o extrato não traz o nome de quem pagou",
        }
        resultado.update(_moldura(bruto, canal, gateway))
        resultado["conhecida"] = True
        return resultado

    por_canal = _regra_por_canal(canal, contexto)
    if por_canal:
        por_canal.update(_moldura(bruto, canal, gateway))
        por_canal["conhecida"] = _tem_historico(por_canal["nome"], conhecidas)
        return por_canal

    if tokens:
        resultado = {
            "nome": _capitalizar(tokens),
            "natureza": "pessoa" if _parece_pessoa(tokens) else "empresa",
            "confianca": "baixa",
            "pista": "nome lido direto do descritor, sem nenhuma passagem anterior no extrato",
        }
        resultado.update(_moldura(bruto, canal, gateway))
        resultado["conhecida"] = False
        return resultado

    resultado = {
        "nome": "Contraparte não identificada",
        "natureza": "desconhecida",
        "confianca": "baixa",
        "pista": "o descritor não traz nome nenhum",
    }
    resultado.update(_moldura(bruto, canal, gateway))
    resultado["conhecida"] = False
    return resultado


def identificar_todas(transacoes, contexto):
    """Roda a identificação em todo o extrato. Devolve id da transação para identificação."""
    mapa = {}
    cache = {}
    for transacao in transacoes:
        chave = (transacao.get("descritor_bruto"), transacao.get("canal"), transacao.get("tipo"))
        if chave not in cache:
            cache[chave] = identificar(
                transacao.get("descritor_bruto"),
                canal=transacao.get("canal"),
                contexto=contexto,
                tipo=transacao.get("tipo"),
            )
        mapa[transacao["id"]] = cache[chave]
    return mapa


# ---------------------------------------------------------------- regras


def _regra_imposto(texto, contexto):
    # Teste por token, e não por substring, senão AGENDASALAO passaria por DAS.
    if not any(token in ("DAS", "SIMEI", "GPS") for token in texto.split()):
        return None
    competencia = _competencia(texto)
    return {
        "nome": "Receita Federal (DAS SIMEI)",
        "natureza": "orgao",
        "confianca": "alta",
        "pista": "descritor de guia do Simples Nacional",
        "competencia": competencia,
    }


def _regra_tarifa_da_conta(texto, contexto):
    tem_tarifa = "TAR" in texto.split() or "TARIFA" in texto
    if not (tem_tarifa and ("CONTA" in texto or "MANUT" in texto)):
        return None
    banco = (contexto.get("conta_pj", {}) or {}).get("banco", "o banco da conta")
    return {
        "nome": "%s (conta PJ)" % banco,
        "natureza": "banco",
        "confianca": "alta",
        "pista": "tarifa lançada pelo próprio banco onde a conta está",
    }


def _regra_antecipacao(texto, contexto):
    if "ANTECIP" not in texto:
        return None
    adquirente = (contexto.get("maquininha", {}) or {}).get("adquirente", "a adquirente")
    return {
        "nome": "%s (maquininha)" % adquirente,
        "natureza": "adquirente",
        "confianca": "alta",
        "pista": "desconto de antecipação lançado pela adquirente",
        "natureza_do_lancamento": "antecipacao",
    }


def _regra_por_canal(canal, contexto):
    if canal == "marketplace":
        nome = (contexto.get("marketplace", {}) or {}).get("nome")
        if nome:
            return {
                "nome": "%s (marketplace de agendamento)" % nome,
                "natureza": "marketplace",
                "confianca": "media",
                "pista": "descritor de gateway sem nome legível, e o único marketplace contratado é %s" % nome,
            }
    if canal in ("maquininha_credito", "maquininha_debito"):
        adquirente = (contexto.get("maquininha", {}) or {}).get("adquirente")
        if adquirente:
            return {
                "nome": "%s (maquininha)" % adquirente,
                "natureza": "adquirente",
                "confianca": "media",
                "pista": "lançamento de maquininha e a adquirente contratada é a %s" % adquirente,
            }
    return None


# ---------------------------------------------------------------- apoio


def _separar_gateway(texto):
    """Separa o prefixo de gateway do núcleo do descritor.

    A normalização já trocou o asterisco por espaço, então o teste é por token.
    PAG*BELEZANET vira PAG BELEZANET, e o que interessa é o que vem depois.
    """
    partes = texto.split()
    if len(partes) > 1 and partes[0] in GATEWAYS:
        return GATEWAYS[partes[0]], " ".join(partes[1:])
    return None, texto


def _tokens_uteis(nucleo):
    tokens = []
    for token in nucleo.split():
        if token in RUIDO:
            continue
        if token in GATEWAYS:
            continue
        if token.isdigit():
            continue
        if len(token) < 2:
            continue
        tokens.append(token)
    return tokens


def _casar_com_historico(tokens, nucleo, conhecidas):
    """Casa o descritor com a lista de contrapartes que já têm histórico."""
    if not tokens:
        return None, 0.0
    concatenado = "".join(tokens)
    melhor_nome = None
    melhor_pontuacao = 0.0

    for nome in conhecidas:
        base = nome.split("(")[0]
        tokens_nome = [t for t in normalizar(base).split() if len(t) > 1]
        if not tokens_nome:
            continue

        acertos = 0
        primeiro_bateu = False
        for posicao, alvo in enumerate(tokens_nome):
            for token in tokens:
                if _mesma_raiz(alvo, token):
                    acertos += 1
                    if posicao == 0:
                        primeiro_bateu = True
                    break
        pontuacao = acertos / float(len(tokens_nome))

        if not primeiro_bateu or pontuacao < 0.6:
            # Segunda chance: descritor que gruda as palavras, como AGENDASALAO.
            grudado = "".join(tokens_nome)
            if len(concatenado) >= 6 and (
                grudado.startswith(concatenado) or concatenado.startswith(grudado)
            ):
                pontuacao = 0.95
            else:
                continue

        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_nome = nome

    return melhor_nome, melhor_pontuacao


def _mesma_raiz(alvo, token):
    if alvo == token:
        return True
    menor = min(len(alvo), len(token))
    if menor < 3:
        return False
    return alvo.startswith(token) or token.startswith(alvo)


def _tem_historico(nome, conhecidas):
    return nome in conhecidas


def _pista_historico(gateway, pontuacao):
    if gateway:
        return "descritor de gateway %s, e o nome depois do asterisco bate com o histórico" % gateway
    if pontuacao >= 0.99:
        return "o nome do descritor bate com uma contraparte que já aparece no histórico"
    return "o nome do descritor é uma abreviação de uma contraparte do histórico"


def _competencia(texto):
    """Extrai a competência fiscal do descritor do DAS. 062026 ou 05 2026."""
    tokens = texto.split()
    for token in tokens:
        if token.isdigit() and len(token) == 6:
            mes, ano = token[:2], token[2:]
            if 1 <= int(mes) <= 12:
                return "%s-%s" % (ano, mes)
    for indice in range(len(tokens) - 1):
        mes, ano = tokens[indice], tokens[indice + 1]
        if mes.isdigit() and ano.isdigit() and len(mes) == 2 and len(ano) == 4:
            if 1 <= int(mes) <= 12:
                return "%s-%s" % (ano, mes)
    return None


def _so_numero(nucleo):
    return all(token.isdigit() or token in RUIDO for token in nucleo.split())


def _parece_pessoa(tokens):
    sufixos = {"LTDA", "ME", "EIRELI", "SA", "COM", "COMERCIO", "DISTRIBUIDORA", "CIA"}
    if any(token in sufixos for token in tokens):
        return False
    return 2 <= len(tokens) <= 4


def _capitalizar(tokens):
    """Vira nome de gente. Descarta inicial solta do meio, MARIA S SOUZA vira Maria Souza."""
    limpos = [t for t in tokens if len(t) > 1]
    return " ".join(t.capitalize() for t in limpos) or " ".join(tokens)


def canal_legivel(canal):
    return CANAL_LEGIVEL.get(canal, canal or "conta")


def _moldura(bruto, canal, gateway):
    return {
        "descritor_bruto": bruto,
        "canal": canal_legivel(canal),
        "gateway": gateway,
    }
