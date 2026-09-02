"""Detector de duplicidade.

Duas regras, e elas não se confundem:

1. Janela curta. Par (contraparte, valor) com menos de 24 horas de distância,
   fora das categorias em que repetir é vida normal (venda, repasse, antecipação).
2. Competência fiscal. O mesmo DAS pago duas vezes, sem janela de tempo, porque
   os dois pagamentos podem estar a dias de distância e ainda assim serem o mesmo
   imposto pago duas vezes.
"""

try:
    from .dados import (achado, acao, data_br, dia_mes, hora_br, horas_entre,
                        moeda, nome_curto, quando)
    from .textos import assinatura, numero
except ImportError:  # execução direta, sem pacote
    from dados import (achado, acao, data_br, dia_mes, hora_br, horas_entre,
                       moeda, nome_curto, quando)
    from textos import assinatura, numero

# Onde repetir o mesmo valor no mesmo dia é o normal do negócio.
CATEGORIAS_COM_REPETICAO_LEGITIMA = {"venda", "repasse", "antecipacao"}

JANELA_HORAS = 24.0


def detectar(pacote, identificacoes):
    """Devolve (achados, silenciados)."""
    achados = []
    achados.extend(_janela_curta(pacote, identificacoes))
    achados.extend(_das_por_competencia(pacote, identificacoes))
    return achados, []


def _janela_curta(pacote, identificacoes):
    candidatas = [
        t for t in pacote["transacoes"]
        if t["tipo"] == "saida"
        and t.get("categoria") not in CATEGORIAS_COM_REPETICAO_LEGITIMA
        and (identificacoes[t["id"]].get("natureza_do_lancamento") != "antecipacao")
    ]
    candidatas.sort(key=quando)

    achados = []
    ja_usadas = set()
    for indice, primeira in enumerate(candidatas):
        if primeira["id"] in ja_usadas:
            continue
        for segunda in candidatas[indice + 1:]:
            if segunda["id"] in ja_usadas:
                continue
            mesma_contraparte = (
                identificacoes[primeira["id"]]["nome"] == identificacoes[segunda["id"]]["nome"]
            )
            mesmo_valor = abs(primeira["valor"] - segunda["valor"]) < 0.01
            if not (mesma_contraparte and mesmo_valor):
                continue
            distancia = horas_entre(primeira, segunda)
            if distancia > JANELA_HORAS:
                continue
            ja_usadas.add(primeira["id"])
            ja_usadas.add(segunda["id"])
            achados.append(_montar_par(pacote, identificacoes, primeira, segunda, distancia))
            break
    return achados


def _montar_par(pacote, identificacoes, primeira, segunda, distancia):
    nome = identificacoes[primeira["id"]]["nome"]
    curto = nome_curto(nome)
    valor = round(segunda["valor"], 2)
    categoria = primeira.get("categoria")
    e_assinatura = categoria == "assinatura"

    if e_assinatura:
        titulo = "%s cobrada duas vezes no dia %s" % (curto, dia_mes(primeira["data"]))
        explicacao = (
            "A %s veio duas vezes no dia %s, %s cada, uma às %s e outra às %s. "
            "São %s horas de diferença e a mesma mensalidade. Esse dinheiro volta."
            % (
                curto,
                dia_mes(primeira["data"]),
                moeda(valor),
                hora_br(primeira["data"]),
                hora_br(segunda["data"]),
                numero(distancia, 1),
            )
        )
    else:
        titulo = "Pagamento para %s saiu duas vezes no mesmo dia" % curto
        explicacao = (
            "Achei %s saindo duas vezes para a %s no dia %s, uma às %s e outra às %s, "
            "com %s horas de diferença. Mesmo valor, mesmo fornecedor, então foi o mesmo "
            "boleto pago duas vezes. Dá para pedir de volta."
            % (
                moeda(valor),
                curto,
                dia_mes(primeira["data"]),
                hora_br(primeira["data"]),
                hora_br(segunda["data"]),
                numero(distancia, 1),
            )
        )

    if e_assinatura:
        acao_pronta = acao(
            "contestacao",
            "Contestação da cobrança repetida",
            _texto_contestacao_assinatura(pacote, curto, primeira, segunda, valor),
        )
    else:
        acao_pronta = acao(
            "cobranca",
            "Pedido de devolução para o fornecedor",
            _texto_devolucao_fornecedor(pacote, curto, primeira, segunda, valor),
        )

    return achado(
        "DUP-JANELA-%s" % primeira["id"],
        "fato",
        "duplicidade",
        titulo,
        explicacao,
        valor=valor,
        transacoes=[primeira["id"], segunda["id"]],
        acao=acao_pronta,
    )


def _texto_contestacao_assinatura(pacote, curto, primeira, segunda, valor):
    return """Olá, tudo bem?

Sou %s e tenho a assinatura da %s cobrada na conta do meu CNPJ.

No dia %s a cobrança de %s foi lançada duas vezes, às %s e às %s, com o mesmo valor. É a mesma mensalidade cobrada em duplicidade.

Peço o estorno de uma delas, no valor de %s, e a confirmação por escrito de que a assinatura segue com uma cobrança só por mês.

Fico no aguardo. Obrigada.

%s""" % (
        (pacote["meta"].get("persona", {}) or {}).get("nome", ""),
        curto,
        data_br(primeira["data"]),
        moeda(valor),
        hora_br(primeira["data"]),
        hora_br(segunda["data"]),
        moeda(valor),
        assinatura(pacote["meta"]),
    )


def _texto_devolucao_fornecedor(pacote, curto, primeira, segunda, valor):
    return """Olá, bom dia.

Aqui é %s, %s.

Identifiquei que o pagamento de %s para vocês saiu duas vezes no dia %s, às %s e às %s. Os dois foram debitados da minha conta, com o mesmo valor.

Foi um pagamento em duplicidade da minha parte. Peço a devolução de %s, por Pix ou como for melhor para vocês, ou o crédito desse valor no próximo pedido.

Consigo enviar os dois comprovantes agora. Me avisem qual das duas opções preferem.

Obrigada.

%s""" % (
        (pacote["meta"].get("persona", {}) or {}).get("nome", ""),
        (pacote["meta"].get("persona", {}) or {}).get("negocio", ""),
        moeda(valor),
        data_br(primeira["data"]),
        hora_br(primeira["data"]),
        hora_br(segunda["data"]),
        moeda(valor),
        assinatura(pacote["meta"]),
    )


def _das_por_competencia(pacote, identificacoes):
    """DAS pago duas vezes na mesma competência. Aqui a janela de 24 horas não serve."""
    por_competencia = {}
    for transacao in pacote["transacoes"]:
        if transacao["tipo"] != "saida":
            continue
        identificacao = identificacoes[transacao["id"]]
        competencia = identificacao.get("competencia") or transacao.get("competencia")
        if identificacao["nome"] != "Receita Federal (DAS SIMEI)" or not competencia:
            continue
        por_competencia.setdefault(competencia, []).append(transacao)

    achados = []
    for competencia in sorted(por_competencia):
        pagamentos = sorted(por_competencia[competencia], key=quando)
        if len(pagamentos) < 2:
            continue
        repetidos = pagamentos[1:]
        valor = round(sum(p["valor"] for p in repetidos), 2)
        rotulo = _competencia_legivel(competencia)
        datas = ", ".join(data_br(p["data"]) for p in pagamentos[:-1])
        explicacao = (
            "O DAS da competência %s foi pago duas vezes, em %s e de novo em %s, "
            "%s cada. É a mesma guia paga em dobro, e esse valor volta como restituição "
            "ou entra como crédito no próximo DAS."
            % (
                rotulo,
                datas,
                data_br(pagamentos[-1]["data"]),
                moeda(pagamentos[0]["valor"]),
            )
        )
        achados.append(
            achado(
                "DUP-DAS-%s" % competencia,
                "fato",
                "duplicidade",
                "DAS da competência %s pago duas vezes" % rotulo,
                explicacao,
                valor=valor,
                transacoes=[p["id"] for p in pagamentos],
                acao=acao(
                    "cobranca",
                    "Pedido de restituição do DAS pago em duplicidade",
                    _texto_restituicao_das(pacote, rotulo, pagamentos, valor),
                ),
            )
        )
    return achados


def _texto_restituicao_das(pacote, rotulo, pagamentos, valor):
    persona = pacote["meta"].get("persona", {}) or {}
    linhas = "\n".join(
        "%s, %s" % (data_br(p["data"]), moeda(p["valor"])) for p in pagamentos
    )
    return """Assunto: pedido de restituição de DAS pago em duplicidade, competência %s

Sou %s, MEI, e pago o DAS do SIMEI todo mês.

A guia da competência %s foi paga duas vezes:

%s

São dois pagamentos da mesma guia, no mesmo valor. Peço a restituição de %s pelo Pedido Eletrônico de Restituição, ou a compensação desse valor no próximo DAS, o que for mais rápido.

Os dois comprovantes de pagamento estão anexados.

%s""" % (
        rotulo,
        persona.get("nome", ""),
        rotulo,
        linhas,
        moeda(valor),
        assinatura(pacote["meta"]),
    )


def _competencia_legivel(competencia):
    ano, mes = competencia.split("-")
    return "%s/%s" % (mes, ano)
