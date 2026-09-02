"""Detector de conciliação.

Cruza o que a Angela vendeu (vendas.json) com o que o marketplace repassou.
A conta é pública e simples: soma das vendas do ciclo, menos a comissão
contratada, é o que deveria ter caído. Se caiu menos, falta dinheiro e o
achado é fato, não suspeita.

Este é o detector que só existe porque temos os dois lados. Sem vendas.json
o repasse curto é invisível, e é exatamente por isso que a pessoa nunca vê.
"""

try:
    from .dados import achado, acao, data_br, moeda
    from .textos import assinatura, numero, percentual
except ImportError:  # execução direta, sem pacote
    from dados import achado, acao, data_br, moeda
    from textos import assinatura, numero, percentual

TOLERANCIA = 0.01  # centavo de arredondamento não é anomalia


def detectar(pacote, identificacoes):
    """Devolve (achados, silenciados)."""
    contexto = pacote["contexto"]
    marketplace = contexto.get("marketplace", {}) or {}
    comissao = marketplace.get("comissao_contratada")
    if comissao is None:
        return [], []

    nome_marketplace = marketplace.get("nome", "o marketplace")
    achados = []
    conferidos = []

    for transacao in pacote["transacoes"]:
        if transacao["tipo"] != "entrada":
            continue
        if transacao.get("canal") != "marketplace":
            continue
        vendas = pacote["vendas_por_transacao"].get(transacao["id"], [])
        if not vendas:
            continue

        bruto = round(sum(v["valor_venda"] for v in vendas), 2)
        esperado = round(bruto * (1 - comissao), 2)
        recebido = round(transacao["valor"], 2)
        diferenca = round(esperado - recebido, 2)

        if diferenca <= TOLERANCIA:
            conferidos.append((transacao, bruto, esperado, recebido))
            continue

        achados.append(
            _montar(pacote, transacao, vendas, bruto, esperado, recebido, diferenca,
                    comissao, nome_marketplace)
        )

    silenciados = _resumo_dos_que_batem(conferidos, nome_marketplace, comissao)
    return achados, silenciados


def _montar(pacote, transacao, vendas, bruto, esperado, recebido, diferenca,
            comissao, nome_marketplace):
    explicacao = (
        "O repasse da %s que caiu em %s cobriu %s atendimentos que somam %s. "
        "Com a comissão de %s que está no contrato deveriam ter caído %s, e caíram %s. "
        "Faltam %s sem nenhuma retenção explicada."
        % (
            nome_marketplace,
            data_br(transacao["data"]),
            numero(len(vendas), 0),
            moeda(bruto),
            percentual(comissao, 0),
            moeda(esperado),
            moeda(recebido),
            moeda(diferenca),
        )
    )
    return achado(
        "CON-REPASSE-%s" % transacao["id"],
        "fato",
        "conciliacao",
        "O repasse da %s veio %s menor" % (nome_marketplace, moeda(diferenca)),
        explicacao,
        valor=diferenca,
        transacoes=[transacao["id"]],
        acao=acao(
            "cobranca",
            "Cobrança da diferença do repasse",
            _texto_cobranca(pacote, transacao, vendas, bruto, esperado, recebido,
                            diferenca, comissao, nome_marketplace),
        ),
    )


def _texto_cobranca(pacote, transacao, vendas, bruto, esperado, recebido, diferenca,
                    comissao, nome_marketplace):
    persona = pacote["meta"].get("persona", {}) or {}
    linhas = "\n".join(
        "%s, %s, %s, %s" % (
            data_br(v["data"]),
            v.get("cliente", ""),
            v.get("servico", ""),
            moeda(v["valor_venda"]),
        )
        for v in sorted(vendas, key=lambda v: v["data"])
    )
    return """Assunto: diferença no repasse de %s

Olá, equipe %s.

Sou %s, %s, parceira de vocês na plataforma.

Conferi o repasse que caiu em %s e a conta não fechou.

Atendimentos do ciclo, %s no total:

%s

Soma dos atendimentos: %s
Comissão contratada de %s: %s
Repasse esperado: %s
Repasse recebido: %s
Diferença: %s

Não localizei nenhuma retenção, estorno ou taxa extra que explique a diferença. Peço a conferência do ciclo e o repasse dos %s que faltam, ou o detalhamento do que foi descontado.

Fico no aguardo do retorno.

%s""" % (
        data_br(transacao["data"]),
        nome_marketplace,
        persona.get("nome", ""),
        persona.get("negocio", ""),
        data_br(transacao["data"]),
        numero(len(vendas), 0),
        linhas,
        moeda(bruto),
        percentual(comissao, 0),
        moeda(round(bruto - esperado, 2)),
        moeda(esperado),
        moeda(recebido),
        moeda(diferenca),
        moeda(diferenca),
        assinatura(pacote["meta"]),
    )


def _resumo_dos_que_batem(conferidos, nome_marketplace, comissao):
    if not conferidos:
        return []
    total = round(sum(c[3] for c in conferidos), 2)
    return [
        achado(
            "SIL-REPASSE-OK",
            "fato",
            "conciliacao",
            "Os outros repasses da %s bateram" % nome_marketplace,
            "Conferi %s repasses do período, %s no total, contra as vendas de cada ciclo. "
            "Todos fecharam certinho com a comissão de %s. Nada para te avisar aqui."
            % (numero(len(conferidos), 0), moeda(total), percentual(comissao, 0)),
            valor=None,
            transacoes=[c[0]["id"] for c in conferidos],
            acao=None,
        )
    ]
