"""Motor fiscal do MEI.

Aritmética sobre regra pública, que é o que torna o MEI o ICP certo: o teto de
receita bruta e o DAS mensal valem para todo mundo, sem configuração.

Duas contas:

1. Receita bruta acumulada no ano contra o teto, com projeção linear pela
   tendência dos últimos meses, para dizer a data em que estoura.
2. DAS por competência. Toda competência vencida precisa ter um pagamento.

Detalhe que muda o número: o que conta para o teto é a receita bruta, o valor da
venda, e não o que sobrou depois da taxa da maquininha.
"""

from datetime import date

try:
    from .dados import (achado, acao, data_br, dias_no_mes, mes_por_extenso,
                        moeda)
    from .textos import percentual
except ImportError:  # execução direta, sem pacote
    from dados import (achado, acao, data_br, dias_no_mes, mes_por_extenso,
                       moeda)
    from textos import percentual

MESES_DE_TENDENCIA = 3


def detectar(pacote, identificacoes):
    """Devolve (achados, silenciados)."""
    resumo = calcular_teto(pacote)
    achados = [_achado_do_teto(pacote, resumo)]
    do_das, calados = _das_por_competencia(pacote, identificacoes)
    achados.extend(do_das)
    return achados, calados


def calcular_teto(pacote):
    """Soma a receita bruta do ano e projeta quando ela passa do teto."""
    contexto = pacote["contexto"]
    teto = contexto.get("teto_mei_anual", 81000.0)

    anterior = pacote["acumulado_anterior"] or {}
    acumulado_anterior = anterior.get("faturamento_bruto_total", 0.0)

    por_mes = {}
    for venda in pacote["vendas"]:
        mes = venda["data"][:7]
        por_mes[mes] = round(por_mes.get(mes, 0.0) + venda["valor_venda"], 2)

    for registro in anterior.get("meses", []) or []:
        por_mes.setdefault(registro["mes"], registro["faturamento_bruto"])

    detalhado = round(sum(v["valor_venda"] for v in pacote["vendas"]), 2)
    acumulado = round(acumulado_anterior + detalhado, 2)
    percentual_do_teto = round(acumulado / teto * 100, 1)
    falta = round(teto - acumulado, 2)

    meses_ordenados = sorted(m for m in por_mes if m >= "2026-01")
    ultimos = meses_ordenados[-MESES_DE_TENDENCIA:]
    serie = [por_mes[m] for m in ultimos]
    crescimento = _crescimento_medio(serie)

    projecao = _projetar_estouro(
        acumulado, teto, ultimos[-1], serie[-1], crescimento
    )

    return {
        "teto": teto,
        "acumulado": acumulado,
        "acumulado_anterior": acumulado_anterior,
        "detalhado": detalhado,
        "percentual_do_teto": percentual_do_teto,
        "falta": falta,
        "por_mes": por_mes,
        "meses_da_tendencia": ultimos,
        "serie_da_tendencia": serie,
        "crescimento_mensal": crescimento,
        "projecao": projecao,
    }


def _crescimento_medio(serie):
    if len(serie) < 2:
        return 0.0
    return round((serie[-1] - serie[0]) / (len(serie) - 1), 2)


def _projetar_estouro(acumulado, teto, ultimo_mes, ultima_receita, crescimento):
    """Projeção linear. Devolve a data estimada e a receita projetada de cada mês."""
    if acumulado >= teto:
        return {"data": None, "ja_estourou": True, "meses": []}
    if crescimento <= 0 and ultima_receita <= 0:
        return {"data": None, "ja_estourou": False, "meses": []}

    ano, mes = (int(p) for p in ultimo_mes.split("-"))
    corrente = acumulado
    receita = ultima_receita
    meses = []

    for passo in range(1, 25):
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1
        receita = round(receita + crescimento, 2)
        if receita <= 0:
            break
        if corrente + receita < teto:
            corrente = round(corrente + receita, 2)
            meses.append({"mes": "%04d-%02d" % (ano, mes), "receita": receita,
                          "acumulado": corrente})
            continue

        falta = teto - corrente
        total_dias = dias_no_mes(ano, mes)
        por_dia = receita / total_dias
        dia_do_estouro = int(round(falta / por_dia)) if por_dia else total_dias
        dia_do_estouro = max(1, min(total_dias, dia_do_estouro))
        corrente = round(corrente + receita, 2)
        meses.append({"mes": "%04d-%02d" % (ano, mes), "receita": receita,
                      "acumulado": corrente})
        return {
            "data": date(ano, mes, dia_do_estouro).isoformat(),
            "mes": mes,
            "ano": ano,
            "receita_do_mes": receita,
            "acumulado_no_fim_do_mes": corrente,
            "ja_estourou": False,
            "meses": meses,
        }

    return {"data": None, "ja_estourou": False, "meses": meses}


def _achado_do_teto(pacote, resumo):
    projecao = resumo["projecao"]
    data_estouro = projecao.get("data")
    referencia = pacote["data_referencia"]

    if data_estouro:
        mes_nome = mes_por_extenso(projecao["mes"])
        titulo = "No ritmo de hoje o teto estoura em %s" % mes_nome
        fecho = (
            "Se o movimento seguir crescendo como nos últimos três meses, o teto de %s "
            "é alcançado por volta de %s."
            % (moeda(resumo["teto"]), data_br(data_estouro))
        )
    else:
        titulo = "Você já usou %s do teto do MEI" % percentual(
            resumo["percentual_do_teto"] / 100.0
        )
        fecho = "No ritmo de hoje o ano fecha dentro do teto."

    explicacao = (
        "Até %s você já faturou %s neste ano, que é %s do teto de %s. Faltam %s. %s "
        "Não é dinheiro perdido, é uma decisão para tomar com antecedência."
        % (
            data_br(referencia),
            moeda(resumo["acumulado"]),
            percentual(resumo["percentual_do_teto"] / 100.0),
            moeda(resumo["teto"]),
            moeda(resumo["falta"]),
            fecho,
        )
    )

    return achado(
        "FIS-TETO",
        "regra",
        "fiscal",
        titulo,
        explicacao,
        valor=None,
        transacoes=[],
        acao=acao(
            "resumo",
            "As três saídas, para decidir com calma",
            _texto_do_teto(pacote, resumo),
        ),
    )


def _texto_do_teto(pacote, resumo):
    projecao = resumo["projecao"]
    linhas = []
    for mes in resumo["meses_da_tendencia"]:
        linhas.append("%s: %s" % (_mes_legivel(mes), moeda(resumo["por_mes"][mes])))
    historico = "\n".join(linhas)

    futuras = []
    for passo in projecao.get("meses", [])[:3]:
        futuras.append("%s: %s" % (_mes_legivel(passo["mes"]), moeda(passo["receita"])))
    projetadas = "\n".join(futuras) if futuras else "sem projeção de crescimento"

    quando_estoura = (
        "por volta de %s" % data_br(projecao["data"]) if projecao.get("data")
        else "não estoura dentro deste ano no ritmo atual"
    )

    return """Onde você está

Faturamento bruto de 2026 até %s: %s
Teto do MEI: %s
Já usado: %s
Falta: %s

Como o movimento vem crescendo

%s

Projetando o mesmo ritmo

%s

Nesse ritmo o teto é alcançado %s.

Vale lembrar que o que conta para o teto é a receita bruta, o valor cheio da venda, e não o que sobra depois da taxa da maquininha e da comissão do marketplace. Por isso o número aqui é maior do que o que entra na conta.

O que dá para fazer, e é uma decisão sua

1. Segurar o faturamento no fim do ano. Funciona, mas significa recusar trabalho, e nem sempre é o que você quer.

2. Migrar para ME antes de estourar. O imposto passa a ser calculado sobre o faturamento, entra a obrigação de contador, e o limite sobe muito. É a saída de quem está crescendo de verdade.

3. Se preparar para o desenquadramento. Passar do teto em até 20%%, ou seja até %s, faz o desenquadramento valer no ano seguinte. Passar de %s desenquadra de forma retroativa a janeiro, com recolhimento da diferença.

Não precisa decidir hoje. Precisa decidir antes de %s, e é por isso que estou te avisando agora e não em dezembro.""" % (
        data_br(pacote["data_referencia"]),
        moeda(resumo["acumulado"]),
        moeda(resumo["teto"]),
        percentual(resumo["percentual_do_teto"] / 100.0),
        moeda(resumo["falta"]),
        historico,
        projetadas,
        quando_estoura,
        moeda(round(resumo["teto"] * 1.2, 2)),
        moeda(round(resumo["teto"] * 1.2, 2)),
        data_br(projecao["data"]) if projecao.get("data") else "o fim do ano",
    )


# ------------------------------------------------- DAS por competência


def _das_por_competencia(pacote, identificacoes):
    contexto = pacote["contexto"]
    das = contexto.get("das", {}) or {}
    vencimento_dia = das.get("vencimento_dia", 20)
    valor_mensal = das.get("valor_mensal")
    referencia = pacote["data_referencia"].date()

    pagas = set(( pacote["acumulado_anterior"] or {}).get("das_pagos", []) or [])
    pagamentos = {}
    for transacao in pacote["transacoes"]:
        if transacao["tipo"] != "saida":
            continue
        identificacao = identificacoes[transacao["id"]]
        competencia = identificacao.get("competencia") or transacao.get("competencia")
        if identificacao["nome"] != "Receita Federal (DAS SIMEI)" or not competencia:
            continue
        pagamentos.setdefault(competencia, []).append(transacao)
        pagas.add(competencia)

    em_aberto = []
    for competencia in _competencias_vencidas(pacote, vencimento_dia, referencia):
        if competencia not in pagas:
            em_aberto.append(competencia)

    achados = []
    if em_aberto:
        atrasadas = ", ".join(_competencia_legivel(c) for c in em_aberto)
        total = round((valor_mensal or 0) * len(em_aberto), 2)
        achados.append(
            achado(
                "FIS-DAS-ABERTO",
                "fato",
                "fiscal",
                "Tem DAS em aberto, competência %s" % atrasadas,
                "Não achei o pagamento do DAS da competência %s, que já venceu. "
                "São %s de guia, e o atraso rende multa e juros até acertar. "
                "A guia sai na hora no portal do Simples Nacional."
                % (atrasadas, moeda(total)),
                valor=total,
                transacoes=[],
                acao=acao(
                    "orientacao",
                    "Como emitir a guia atrasada",
                    _texto_das_em_aberto(pacote, em_aberto, valor_mensal),
                ),
            )
        )

    silenciados = []
    if pagamentos and not em_aberto:
        competencias = sorted(pagamentos)
        silenciados.append(
            achado(
                "SIL-DAS-EM-DIA",
                "fato",
                "fiscal",
                "O DAS está em dia",
                "Conferi as competências de %s a %s e todas têm pagamento. "
                "O DAS todo mês é obrigação, não é anomalia, então não te aviso a cada mês."
                % (
                    _competencia_legivel(competencias[0]),
                    _competencia_legivel(competencias[-1]),
                ),
                valor=None,
                transacoes=[t["id"] for lista in pagamentos.values() for t in lista],
                acao=None,
            )
        )
    return achados, silenciados


def _competencias_vencidas(pacote, vencimento_dia, referencia):
    """Competências do ano cujo vencimento, dia 20 do mês seguinte, já passou."""
    meses = set()
    for registro in (pacote["acumulado_anterior"] or {}).get("meses", []) or []:
        meses.add(registro["mes"])
    for venda in pacote["vendas"]:
        meses.add(venda["data"][:7])

    vencidas = []
    for mes in sorted(meses):
        ano, numero_do_mes = (int(p) for p in mes.split("-"))
        seguinte_ano, seguinte_mes = (ano + 1, 1) if numero_do_mes == 12 else (ano, numero_do_mes + 1)
        vencimento = date(seguinte_ano, seguinte_mes, min(vencimento_dia, 28))
        if vencimento <= referencia:
            vencidas.append(mes)
    return vencidas


def _texto_das_em_aberto(pacote, em_aberto, valor_mensal):
    lista = "\n".join(_competencia_legivel(c) for c in em_aberto)
    return """O que falta

Não localizei no extrato o pagamento do DAS destas competências:

%s

Cada guia é de %s, e o atraso soma multa de 0,33%% ao dia, limitada a 20%%, mais juros pela Selic.

Como resolver, leva cinco minutos

1. Entre no portal do Simples Nacional, na área do MEI, com o seu CNPJ.
2. Escolha Pagamento de guia DAS, opção PGMEI.
3. Selecione o ano de apuração e marque a competência em aberto.
4. Emita a guia, que já vem com multa e juros calculados, e pague no aplicativo do banco.
5. Guarde o comprovante.

Se você tiver o comprovante e ele simplesmente não passou por esta conta, me manda que eu registro e paro de cobrar.""" % (
        lista,
        moeda(valor_mensal or 0),
    )


def _competencia_legivel(competencia):
    ano, mes = competencia.split("-")
    return "%s/%s" % (mes, ano)


def _mes_legivel(competencia):
    ano, mes = competencia.split("-")
    return "%s de %s" % (mes_por_extenso(int(mes)), ano)
