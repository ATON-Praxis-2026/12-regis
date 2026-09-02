"""Detector de valor.

Três coisas que mexem no valor sem mexer no número de lançamentos, e por isso
passam despercebidas:

1. Taxa efetiva da maquininha diferente da contratada.
2. Antecipação automática ligada, descontando todo dia.
3. Tarifa que deixou de ser isenta.

A primeira é regra e não fato, porque depende do contrato da titular com a
adquirente. As outras duas são fato: o contexto declara a isenção e declara que
a antecipação não foi contratada de forma consciente.
"""

from datetime import date

try:
    from .dados import achado, acao, data_br, dia, moeda, quando
    from .textos import assinatura, numero, percentual
except ImportError:  # execução direta, sem pacote
    from dados import achado, acao, data_br, dia, moeda, quando
    from textos import assinatura, numero, percentual

# Arredondamento de centavo faz a taxa oscilar na terceira casa. Só acima disso é sinal.
TOLERANCIA_DE_TAXA = 0.002

CANAIS_DE_CARTAO = {
    "maquininha_credito": ("crédito", "taxa_credito_contratada"),
    "maquininha_debito": ("débito", "taxa_debito_contratada"),
}


def detectar(pacote, identificacoes):
    """Devolve (achados, silenciados)."""
    achados = []
    silenciados = []

    de_taxa, calados_de_taxa = _taxa_da_maquininha(pacote)
    achados.extend(de_taxa)
    silenciados.extend(calados_de_taxa)

    da_antecipacao = _antecipacao_automatica(pacote, identificacoes)
    achados.extend(da_antecipacao)

    da_tarifa = _tarifa_que_deixou_de_ser_isenta(pacote, identificacoes)
    achados.extend(da_tarifa)

    return achados, silenciados


# ------------------------------------------------- taxa da maquininha


def _taxa_da_maquininha(pacote):
    maquininha = pacote["contexto"].get("maquininha", {}) or {}
    adquirente = maquininha.get("adquirente", "a adquirente")
    achados = []
    silenciados = []

    for canal, (rotulo, chave) in sorted(CANAIS_DE_CARTAO.items()):
        contratada = maquininha.get(chave)
        if contratada is None:
            continue
        vendas = [
            t for t in pacote["transacoes"]
            if t["tipo"] == "entrada"
            and t.get("canal") == canal
            and t.get("categoria") == "venda"
            and t.get("valor_bruto_venda")
        ]
        if not vendas:
            continue

        fora = [
            t for t in sorted(vendas, key=quando)
            if abs(_taxa_efetiva(t) - contratada) > TOLERANCIA_DE_TAXA
        ]
        if not fora:
            silenciados.append(_taxa_confere(canal, rotulo, contratada, vendas, adquirente))
            continue

        achados.append(_taxa_diferente(pacote, rotulo, contratada, fora, adquirente))
    return achados, silenciados


def _taxa_efetiva(transacao):
    return 1 - (transacao["valor"] / transacao["valor_bruto_venda"])


def _taxa_confere(canal, rotulo, contratada, vendas, adquirente):
    volume = round(sum(t["valor_bruto_venda"] for t in vendas), 2)
    return achado(
        "SIL-TAXA-%s" % canal.upper(),
        "fato",
        "valor",
        "A taxa do %s está batendo com o contrato" % rotulo,
        "Conferi as %s vendas no %s do período, %s de volume, e o desconto da %s foi de %s "
        "em todas. É exatamente a taxa contratada, então não tem nada a fazer aqui."
        % (
            numero(len(vendas), 0),
            rotulo,
            moeda(volume),
            adquirente,
            percentual(contratada, 2),
        ),
        valor=None,
        transacoes=[t["id"] for t in vendas],
        acao=None,
    )


def _taxa_diferente(pacote, rotulo, contratada, fora, adquirente):
    volume = round(sum(t["valor_bruto_venda"] for t in fora), 2)
    efetiva = round(sum(_taxa_efetiva(t) for t in fora) / len(fora), 4)
    impacto = round(volume * (efetiva - contratada), 2)
    inicio = fora[0]
    fim = fora[-1]

    explicacao = (
        "De %s até %s as vendas no %s vieram com desconto de %s, e o seu contrato com a %s "
        "diz %s. São %s vendas, %s de volume, e %s a mais de taxa nesse período. "
        "Vale conferir com a %s antes que vire mês cheio."
        % (
            data_br(inicio["data"]),
            data_br(fim["data"]),
            rotulo,
            percentual(efetiva, 2),
            adquirente,
            percentual(contratada, 2),
            numero(len(fora), 0),
            moeda(volume),
            moeda(impacto),
            adquirente,
        )
    )

    return achado(
        "VAL-TAXA-%s" % inicio["id"],
        "regra",
        "valor",
        "A maquininha passou a descontar %s em vez de %s"
        % (percentual(efetiva, 2), percentual(contratada, 2)),
        explicacao,
        valor=impacto,
        transacoes=[t["id"] for t in fora],
        acao=acao(
            "contestacao",
            "Contestação da taxa para a adquirente",
            _texto_taxa(pacote, rotulo, contratada, efetiva, fora, volume, impacto, adquirente),
        ),
    )


def _texto_taxa(pacote, rotulo, contratada, efetiva, fora, volume, impacto, adquirente):
    persona = pacote["meta"].get("persona", {}) or {}
    maquininha = pacote["contexto"].get("maquininha", {}) or {}
    terminal = maquininha.get("terminal", "")
    return """Assunto: taxa de %s cobrada acima da contratada, terminal %s

Olá, equipe %s.

Sou %s, %s, e uso a maquininha de vocês no terminal %s.

Minha taxa contratada de %s é %s. Nas vendas de %s até %s o desconto aplicado foi de %s.

São %s vendas, %s de volume bruto, e %s cobrados acima do contrato nesse período.

Peço que verifiquem qual taxa está ativa no meu terminal, o motivo da alteração e a data em que ela passou a valer. Se a alteração não foi contratada por mim, peço o retorno para %s e o estorno da diferença.

Tenho o extrato com todas as vendas do período e envio se ajudar na conferência.

%s""" % (
        rotulo,
        terminal,
        adquirente,
        persona.get("nome", ""),
        persona.get("negocio", ""),
        terminal,
        rotulo,
        percentual(contratada, 2),
        data_br(fora[0]["data"]),
        data_br(fora[-1]["data"]),
        percentual(efetiva, 2),
        numero(len(fora), 0),
        moeda(volume),
        moeda(impacto),
        percentual(contratada, 2),
        assinatura(pacote["meta"]),
    )


# ------------------------------------------------- antecipação automática


def _antecipacao_automatica(pacote, identificacoes):
    config = pacote["contexto"].get("antecipacao_automatica", {}) or {}
    if not config.get("ativa"):
        return []

    lancamentos = [
        t for t in pacote["transacoes"]
        if t["tipo"] == "saida"
        and (
            identificacoes[t["id"]].get("natureza_do_lancamento") == "antecipacao"
            or t.get("categoria") == "antecipacao"
        )
    ]
    if not lancamentos:
        return []

    lancamentos = sorted(lancamentos, key=quando)
    total = round(sum(t["valor"] for t in lancamentos), 2)
    taxa = config.get("taxa")
    desde = config.get("ativa_desde")
    consciente = config.get("contratada_conscientemente_pela_titular", True)
    adquirente = (pacote["contexto"].get("maquininha", {}) or {}).get("adquirente", "a adquirente")
    por_mes = round(total / _meses_do_periodo(lancamentos), 2)

    explicacao = (
        "A antecipação automática está ligada desde %s e desconta %s de todo crédito, "
        "todo dia. No extrato que li são %s descontos que somam %s, cerca de %s por mês. "
        "É o preço de receber hoje o que cairia amanhã%s."
        % (
            data_br(desde) if desde else "o começo do período",
            percentual(taxa, 2) if taxa else "uma taxa fixa",
            numero(len(lancamentos), 0),
            moeda(total),
            moeda(por_mes),
            "" if consciente else ", e pelo que consta ninguém te avisou que estava ligada",
        )
    )

    return [
        achado(
            "VAL-ANTECIPACAO",
            "fato",
            "valor",
            "A antecipação automática levou %s do seu crédito" % moeda(total),
            explicacao,
            valor=total,
            transacoes=[t["id"] for t in lancamentos],
            acao=acao(
                "orientacao",
                "Como desligar a antecipação automática",
                _texto_antecipacao(pacote, adquirente, taxa, total, por_mes, lancamentos, desde),
            ),
        )
    ]


def _meses_do_periodo(lancamentos):
    meses = {t["data"][:7] for t in lancamentos}
    return max(len(meses), 1)


def _texto_antecipacao(pacote, adquirente, taxa, total, por_mes, lancamentos, desde):
    maquininha = pacote["contexto"].get("maquininha", {}) or {}
    terminal = maquininha.get("terminal", "")
    anual = round(por_mes * 12, 2)
    return """O que está acontecendo

A antecipação automática da %s está ligada no seu terminal %s desde %s. Toda venda no crédito cai na hora, e por isso a %s desconta %s de cada uma.

No período que eu li foram %s descontos, %s no total, cerca de %s por mês. Mantendo esse ritmo, dá perto de %s por ano.

Se você precisa do dinheiro no mesmo dia, isso é um custo justo. Se dá para esperar um dia, é dinheiro que fica com você.

Como desligar, leva dois minutos

1. Abra o aplicativo da %s e entre com o seu CNPJ.
2. Vá em Menu, depois Recebimentos, depois Antecipação automática.
3. Desligue a chave de antecipação automática e confirme.
4. Guarde o protocolo que aparece na tela.

Se preferir pelo telefone, ligue na central da %s, peça o desligamento da antecipação automática do terminal %s e anote o número do protocolo.

Depois de desligar, o crédito passa a cair em um dia útil e o desconto de %s some. Me avise quando fizer que eu confiro no próximo extrato se parou mesmo.""" % (
        adquirente,
        terminal,
        data_br(desde) if desde else "o começo do período",
        adquirente,
        percentual(taxa, 2) if taxa else "uma taxa",
        numero(len(lancamentos), 0),
        moeda(total),
        moeda(por_mes),
        moeda(anual),
        adquirente,
        adquirente,
        terminal,
        percentual(taxa, 2) if taxa else "antecipação",
    )


# ------------------------------------------------- tarifa que deixou de ser isenta


def _tarifa_que_deixou_de_ser_isenta(pacote, identificacoes):
    conta = pacote["contexto"].get("conta_pj", {}) or {}
    isenta_ate = conta.get("tarifa_mensal_isenta_ate")
    banco = conta.get("banco", "o banco")

    cobrancas = sorted(
        [
            t for t in pacote["transacoes"]
            if t["tipo"] == "saida"
            and identificacoes[t["id"]].get("natureza") == "banco"
        ],
        key=quando,
    )
    if not cobrancas:
        return []

    if isenta_ate:
        corte = date.fromisoformat(isenta_ate)
        novas = [t for t in cobrancas if dia(t) > corte]
    else:
        novas = cobrancas

    if not novas:
        return []

    primeira = novas[0]
    valor = round(primeira["valor"], 2)
    anual = round(valor * 12, 2)
    avisada = conta.get("aviso_recebido_pela_titular", True)

    explicacao = (
        "A sua conta no %s era isenta de tarifa até %s. Em %s entrou a primeira cobrança "
        "de manutenção, %s%s. Se ficar assim, são %s por ano numa conta que era de graça."
        % (
            banco,
            data_br(isenta_ate) if isenta_ate else "agora",
            data_br(primeira["data"]),
            moeda(valor),
            "" if avisada else ", sem aviso que tenha chegado até você",
            moeda(anual),
        )
    )

    return [
        achado(
            "VAL-TARIFA-%s" % primeira["id"],
            "fato",
            "valor",
            "Sua conta PJ deixou de ser gratuita, %s por mês" % moeda(valor),
            explicacao,
            valor=valor,
            transacoes=[t["id"] for t in novas],
            acao=acao(
                "contestacao",
                "Pedido de isenção da tarifa",
                _texto_tarifa(pacote, banco, primeira, valor, anual, isenta_ate),
            ),
        )
    ]


def _texto_tarifa(pacote, banco, primeira, valor, anual, isenta_ate):
    persona = pacote["meta"].get("persona", {}) or {}
    pacote_conta = (pacote["contexto"].get("conta_pj", {}) or {}).get("pacote", "")
    return """Assunto: cobrança de tarifa de manutenção na conta PJ

Olá,

Sou %s, %s, titular da conta PJ no %s, pacote %s.

Minha conta era isenta de tarifa de manutenção até %s. Em %s foi debitada a primeira tarifa, no valor de %s, e eu não recebi nenhuma comunicação prévia sobre o fim da isenção.

Peço:

1. A informação de quando e por qual canal a mudança foi comunicada.
2. A manutenção da isenção da tarifa mensal, considerando o meu tempo de conta e a movimentação mensal do negócio.
3. Se a isenção não for possível, o estorno da tarifa de %s e a informação de quais pacotes sem tarifa vocês oferecem para MEI.

Como referência, essa tarifa representa %s por ano, e existem contas PJ sem tarifa no mercado. Prefiro continuar com vocês, mas preciso dessa resposta para decidir.

%s""" % (
        persona.get("nome", ""),
        persona.get("negocio", ""),
        banco,
        pacote_conta,
        data_br(isenta_ate) if isenta_ate else "este mês",
        data_br(primeira["data"]),
        moeda(valor),
        moeda(valor),
        moeda(anual),
        assinatura(pacote["meta"]),
    )
