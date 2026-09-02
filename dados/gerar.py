#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do dataset sintetico da Regis.

Persona (ICP fechado no BRIEFING.md, secoes 3.9 e Decisao 3):
Cabeleireira MEI que atende a propria clientela dentro de um salao em Campinas
(SP), alugando cadeira. Ela nao e dona do salao. Recebe por maquininha (credito
e debito) e por marketplace de agendamento, com Pix como minoria.
Volume alto de transacoes, concentrado nas sextas e nos sabados.

O script e deterministico (random.seed fixo). Rodar de novo produz exatamente
os mesmos arquivos, entao os ids do gabarito continuam validos.

Saida em dados/:
  transacoes.json           extrato da conta PJ, 01/06/2026 a 29/08/2026
  vendas.json               registro de vendas do lado dela, a agenda de atendimentos
  anomalias-esperadas.json  gabarito das anomalias plantadas

Uso:
    python3 dados/gerar.py
"""

import json
import random
from datetime import date, datetime, time, timedelta
from pathlib import Path

# --------------------------------------------------------------------------
# Configuracao
# --------------------------------------------------------------------------

SEED = 20260829
random.seed(SEED)

RAIZ = Path(__file__).resolve().parent
TZ = "-03:00"

INICIO = date(2026, 6, 1)
FIM = date(2026, 8, 29)          # sabado, dia da demo

TETO_MEI = 81000.00
SALARIO_MINIMO_2026 = 1621.00
DAS_MENSAL = 87.05               # 5% do salario minimo + R$ 1 ICMS + R$ 5 ISS

TAXA_CREDITO_CONTRATADA = 0.0289
TAXA_CREDITO_APLICADA_APOS_17_08 = 0.0349   # reajuste silencioso da adquirente
TAXA_DEBITO_CONTRATADA = 0.0149
TAXA_ANTECIPACAO = 0.0299
COMISSAO_MARKETPLACE = 0.12

DATA_VIRADA_TAXA = date(2026, 8, 17)
ANTECIPACAO_ATIVA_DESDE = date(2026, 3, 2)

# Faturamento bruto por mes. Jan a mai entram como consolidado (sem detalhe de
# transacao), jun a ago sao gerados transacao por transacao.
# 30.000 (jan a mai) + 28.400 (jun a ago) = 58.400 ate 29/08/2026.
FATURAMENTO_ANTERIOR = [
    ("2026-01", 5100.00),
    ("2026-02", 5500.00),
    ("2026-03", 6000.00),
    ("2026-04", 6500.00),
    ("2026-05", 6900.00),
]
META_MES = {6: 8200.00, 7: 9400.00, 8: 10800.00}

FERIADOS = {
    date(2026, 6, 4): "Corpus Christi",
    date(2026, 7, 9): "Revolução Constitucionalista (SP)",
}

# Quantas vendas por dia da semana, por mes. 0 = fechado.
# Segunda e domingo o salao nao abre.
VENDAS_POR_DIA = {
    6: {0: 0, 1: 2, 2: 2, 3: 3, 4: 7, 5: 8, 6: 0},
    7: {0: 0, 1: 2, 2: 3, 3: 3, 4: 8, 5: 9, 6: 0},
    8: {0: 0, 1: 2, 2: 3, 3: 4, 4: 10, 5: 12, 6: 0},
}

# (servico, preco, peso)
MENU = [
    ("Esmaltação simples", 35, 8),
    ("Manicure", 40, 12),
    ("Pé e mão", 65, 10),
    ("Design de sobrancelha", 45, 9),
    ("Escova", 55, 10),
    ("Escova com hidratação", 95, 6),
    ("Corte feminino", 70, 7),
    ("Corte masculino", 45, 6),
    ("Hidratação", 60, 5),
    ("Depilação", 50, 5),
    ("Coloração de raiz", 150, 4),
    ("Penteado", 120, 3),
    ("Maquiagem", 130, 2),
    ("Alongamento de unhas", 160, 3),
    ("Shampoo profissional (produto)", 78, 3),
    ("Kit de tratamento capilar (produto)", 145, 2),
    ("Botox capilar", 250, 2),
    ("Progressiva", 280, 2),
    ("Luzes", 320, 1),
    ("Mechas", 380, 1),
]
MENU_NOMES = [m[0] for m in MENU]
MENU_PRECOS = [m[1] for m in MENU]
MENU_PESOS = [m[2] for m in MENU]

# A Angela aluga cadeira no Studio Bella e divide o salao com outras tres
# profissionais. Elas faturam no CNPJ delas e nao entram nesta conta, entao
# toda venda de vendas.json e atendimento dela.
COLEGAS_DE_SALAO = ["Jéssica", "Tainara", "Simone"]

# O nome repetido quatro vezes e proposital: mantem o sorteio consumindo o seed
# exatamente como na geracao original, que e o que preserva os ids TX- e VD-.
ATENDE = ["Angela"] * 4

CLIENTES = [
    "Adriana R.", "Beatriz M.", "Camila S.", "Daniela P.", "Elaine T.",
    "Fabiana L.", "Gisele A.", "Helena C.", "Íris N.", "Juliana F.",
    "Kelly O.", "Larissa V.", "Márcia D.", "Nathália B.", "Otávia G.",
    "Patrícia H.", "Renata Q.", "Sabrina E.", "Tatiane I.", "Vanessa U.",
    "Wilma J.", "Yara K.", "Zilda X.", "Amanda W.", "Bruna Y.",
]

CANAIS_VENDA = [
    ("maquininha_credito", 42),
    ("maquininha_debito", 28),
    ("marketplace", 22),
    ("pix", 8),
]

DESCRITORES_CREDITO = ["CIELO 4829", "CIELO*CRED 4829", "REC CARTAO CIELO 4829"]
DESCRITORES_DEBITO = ["CIELO DEB 4829", "CIELO*DEB 4829"]
DESCRITORES_PIX_ENTRADA = [
    "PIX QR ESTATICO 8812",
    "PIX RECEBIDO CPF ***.412.***-**",
    "PIX REC 8812 QRS",
]


def dinheiro(valor):
    return round(valor + 1e-9, 2)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + TZ


def hora_de_atendimento(dia):
    """Sabado abre mais cedo e fecha mais cedo."""
    if dia.weekday() == 5:
        h = random.randint(8, 17)
    else:
        h = random.randint(9, 18)
    return time(h, random.choice([0, 10, 15, 20, 30, 40, 45, 50]))


def dias_do_periodo():
    d = INICIO
    while d <= FIM:
        yield d
        d += timedelta(days=1)


# --------------------------------------------------------------------------
# 1. Vendas do salao
# --------------------------------------------------------------------------

def gerar_vendas():
    """Gera as vendas mes a mes, fechando o faturamento bruto no valor alvo."""
    vendas = []
    for mes in (6, 7, 8):
        dias_abertos = [
            d for d in dias_do_periodo()
            if d.month == mes
            and VENDAS_POR_DIA[mes][d.weekday()] > 0
            and d not in FERIADOS
        ]
        do_mes = []
        for d in dias_abertos:
            qtd = VENDAS_POR_DIA[mes][d.weekday()]
            if random.random() < 0.35:
                qtd += random.choice([-1, 1])
            qtd = max(1, qtd)
            for _ in range(qtd):
                servico = random.choices(MENU_NOMES, weights=MENU_PESOS, k=1)[0]
                preco = MENU_PRECOS[MENU_NOMES.index(servico)]
                do_mes.append({"data": d, "servico": servico, "valor": float(preco)})

        alvo = META_MES[mes]
        # Ajusta a quantidade ate sobrar uma folga que caiba em uma venda so.
        while alvo - sum(v["valor"] for v in do_mes) > 400:
            d = random.choice(dias_abertos)
            servico = random.choices(MENU_NOMES, weights=MENU_PESOS, k=1)[0]
            preco = MENU_PRECOS[MENU_NOMES.index(servico)]
            do_mes.append({"data": d, "servico": servico, "valor": float(preco)})
        while alvo - sum(v["valor"] for v in do_mes) < 35:
            do_mes.pop(random.randrange(len(do_mes)))

        # A ultima venda do mes fecha a conta no centavo.
        folga = alvo - sum(v["valor"] for v in do_mes)
        idx = min(range(len(MENU_PRECOS)), key=lambda i: abs(MENU_PRECOS[i] - folga))
        do_mes.append({
            "data": random.choice(dias_abertos),
            "servico": MENU_NOMES[idx],
            "valor": float(folga),
        })

        assert abs(sum(v["valor"] for v in do_mes) - alvo) < 0.005
        vendas.extend(do_mes)

    # Canal, horario, cliente e profissional.
    nomes_canais = [c[0] for c in CANAIS_VENDA]
    pesos_canais = [c[1] for c in CANAIS_VENDA]
    for v in vendas:
        canal = random.choices(nomes_canais, weights=pesos_canais, k=1)[0]
        # Nos dias 28 e 29/08 nada de marketplace: o ultimo repasse ja saiu em
        # 28/08 e assim nao fica venda pendente de repasse dentro da janela.
        if canal == "marketplace" and v["data"] >= date(2026, 8, 28):
            canal = random.choices(["maquininha_credito", "maquininha_debito", "pix"],
                                   weights=[50, 35, 15], k=1)[0]
        v["canal"] = canal
        v["hora"] = hora_de_atendimento(v["data"])
        v["cliente"] = random.choice(CLIENTES)
        v["profissional"] = random.choice(ATENDE)

    vendas.sort(key=lambda v: (v["data"], v["hora"]))
    for i, v in enumerate(vendas, start=1):
        v["id"] = "VD-%04d" % i
    return vendas


# --------------------------------------------------------------------------
# 2. Transacoes do extrato
# --------------------------------------------------------------------------

def nova(tipo, dt, canal, descritor, valor, contraparte, categoria,
         valor_bruto_venda=None, tag=None, extras=None):
    t = {
        "id": None,
        "data": iso(dt),
        "tipo": tipo,
        "canal": canal,
        "descritor_bruto": descritor,
        "valor": dinheiro(valor),
        "valor_bruto_venda": dinheiro(valor_bruto_venda) if valor_bruto_venda is not None else None,
        "contraparte": contraparte,
        "categoria": categoria,
    }
    if extras:
        t.update(extras)
    t["_dt"] = dt
    t["_tag"] = tag
    return t


def taxa_credito_do_dia(d):
    return TAXA_CREDITO_APLICADA_APOS_17_08 if d >= DATA_VIRADA_TAXA else TAXA_CREDITO_CONTRATADA


def gerar_transacoes(vendas):
    txs = []

    # 2.1 Entradas de cartao e Pix, uma linha por venda.
    for v in vendas:
        dt = datetime.combine(v["data"], v["hora"])
        if v["canal"] == "maquininha_credito":
            taxa = taxa_credito_do_dia(v["data"])
            liquido = dinheiro(v["valor"] * (1 - taxa))
            tag = "taxa_efetiva" if v["data"] >= DATA_VIRADA_TAXA else None
            txs.append(nova("entrada", dt, "maquininha_credito",
                            random.choice(DESCRITORES_CREDITO), liquido,
                            "Cielo (maquininha)", "venda",
                            valor_bruto_venda=v["valor"], tag=tag,
                            extras={"venda_ids": [v["id"]]}))
            v["_tx"] = txs[-1]
        elif v["canal"] == "maquininha_debito":
            liquido = dinheiro(v["valor"] * (1 - TAXA_DEBITO_CONTRATADA))
            txs.append(nova("entrada", dt, "maquininha_debito",
                            random.choice(DESCRITORES_DEBITO), liquido,
                            "Cielo (maquininha)", "venda",
                            valor_bruto_venda=v["valor"],
                            extras={"venda_ids": [v["id"]]}))
            v["_tx"] = txs[-1]
        elif v["canal"] == "pix":
            txs.append(nova("entrada", dt, "pix",
                            random.choice(DESCRITORES_PIX_ENTRADA), v["valor"],
                            v["cliente"], "venda",
                            extras={"venda_ids": [v["id"]]}))
            v["_tx"] = txs[-1]

    # 2.2 Repasses do marketplace: toda sexta, cobrindo sexta anterior a quinta.
    mkt = [v for v in vendas if v["canal"] == "marketplace"]
    sextas = [d for d in dias_do_periodo() if d.weekday() == 4]
    pendentes = list(mkt)
    for sexta in sextas:
        corte = sexta - timedelta(days=1)
        lote = [v for v in pendentes if v["data"] <= corte]
        if not lote:
            continue
        pendentes = [v for v in pendentes if v["data"] > corte]
        bruto = dinheiro(sum(v["valor"] for v in lote))
        esperado = dinheiro(bruto * (1 - COMISSAO_MARKETPLACE))
        tag = None
        valor = esperado
        if sexta == date(2026, 8, 28):
            valor = dinheiro(esperado - 38.00)   # repasse curto, sem explicacao
            tag = "repasse_curto"
        dt = datetime.combine(sexta, time(10, 12))
        txs.append(nova("entrada", dt, "marketplace",
                        random.choice(["PAG*BELEZANET", "MP *SALAO", "BELEZANET REPASSE"]),
                        valor, "BelezaNet (marketplace de agendamento)", "repasse",
                        valor_bruto_venda=bruto, tag=tag,
                        extras={"venda_ids": [v["id"] for v in lote],
                                "qtd_vendas": len(lote)}))
        for v in lote:
            v["_tx"] = txs[-1]
    assert not pendentes, "sobrou venda de marketplace sem repasse"

    # 2.3 Antecipacao automatica: desconto diario sobre o credito do dia.
    por_dia = {}
    for v in vendas:
        if v["canal"] == "maquininha_credito":
            por_dia.setdefault(v["data"], 0.0)
            por_dia[v["data"]] += v["valor"]
    for d in sorted(por_dia):
        valor = dinheiro(por_dia[d] * TAXA_ANTECIPACAO)
        if valor < 0.01:
            continue
        txs.append(nova("saida", datetime.combine(d, time(23, 50)),
                        "maquininha_credito", "CIELO ANTECIP AUTOM D+0",
                        valor, "Cielo (maquininha)", "antecipacao",
                        tag="antecipacao"))

    # 2.4 Despesas fixas dela.
    for mes in (6, 7, 8):
        ano = 2026

        def em(dia, hora=None):
            return datetime.combine(date(ano, mes, dia),
                                    hora or time(random.randint(8, 20), random.choice([5, 17, 23, 41, 58])))

        # Aluguel da cadeira, pago ao salao que ela nao e dona
        txs.append(nova("saida", em(5, time(9, 22)), "pix", "PIX ENVIADO STUDIO BELLA LTDA",
                        1850.00, "Studio Bella (aluguel de cadeira)", "aluguel"))
        # Energia
        txs.append(nova("saida", em(12, time(6, 3)), "debito_automatico", "CPFL PAULISTA DEB AUT",
                        {6: 268.44, 7: 291.10, 8: 312.77}[mes],
                        "CPFL Paulista (energia)", "utilidade"))
        # Internet
        txs.append(nova("saida", em(10, time(6, 3)), "debito_automatico", "VIVO FIBRA 400 DEB AUT",
                        119.90, "Vivo Fibra (internet)", "utilidade"))
        # Som ambiente: reajuste silencioso em agosto
        valor_som = 32.90 if mes < 8 else 47.90
        txs.append(nova("saida", em(8, time(6, 12)), "debito_automatico", "SOMPRO*MUSICA AMBIENT",
                        valor_som, "SomPro Música Ambiente", "assinatura",
                        tag="reajuste" if mes == 8 else None))
        # App de agenda: cancelado em 12/06 e continua cobrando
        txs.append(nova("saida", em(22, time(6, 41)), "debito_automatico", "PAG*AGENDASALAO",
                        39.90, "Agenda Salão App", "assinatura", tag="pos_cancelamento"))
        # Streaming (assinatura pessoal paga na conta PJ)
        txs.append(nova("saida", em(12, time(9, 14)), "debito_automatico", "NETFLIX.COM 5511",
                        55.90, "Netflix", "assinatura",
                        tag="streaming_dup_original" if mes == 8 else None))
        # Fornecedor de cosmeticos, duas compras por mes
        base = {6: (512.40, 386.20), 7: (487.60, 402.90), 8: (534.80, 419.30)}[mes]
        txs.append(nova("saida", em(14, time(9, 12)), "boleto", "BELEZA DISTRIB LTDA 001",
                        base[0], "Beleza Distribuidora LTDA", "insumo",
                        tag="fornecedor_dup_original" if mes == 7 else None))
        txs.append(nova("saida", em(24, time(15, 40)), "boleto", "PAG*BELEZADIST",
                        base[1], "Beleza Distribuidora LTDA", "insumo"))
        # Descartaveis
        txs.append(nova("saida", em(18, time(11, 5)), "pix", "PIX ENV DESCARTA MAIS COM",
                        {6: 214.00, 7: 236.50, 8: 248.90}[mes],
                        "Descarta Mais Comércio", "insumo"))
        # Combustivel e conveniencia (mistura de contas, aparece na pesquisa)
        for _ in range(3):
            dia = random.randint(2, 27)
            txs.append(nova("saida", em(dia), "pix",
                            random.choice(["PIX ENV SUPERM BOM PRECO",
                                           "PIX ENV DROGARIA SAO PAULO",
                                           "PIX ENV POSTO IPIRANGA 12"]),
                            round(random.uniform(48, 260), 2),
                            random.choice(["Supermercado Bom Preço",
                                           "Drogaria São Paulo",
                                           "Posto Ipiranga"]),
                            "pessoal"))

    # 2.5 DAS. Julho paga duas vezes a mesma competencia.
    txs.append(nova("saida", datetime(2026, 6, 18, 10, 40), "boleto",
                    "PAGTO BOLETO GPS/DAS 05/2026", DAS_MENSAL,
                    "Receita Federal (DAS SIMEI)", "imposto",
                    extras={"competencia": "2026-05"}))
    txs.append(nova("saida", datetime(2026, 7, 17, 8, 55), "boleto",
                    "DAS SIMEI 062026", DAS_MENSAL,
                    "Receita Federal (DAS SIMEI)", "imposto",
                    tag="das_dup_a", extras={"competencia": "2026-06"}))
    txs.append(nova("saida", datetime(2026, 7, 20, 19, 26), "boleto",
                    "PAGTO BOLETO GPS/DAS 06/2026", DAS_MENSAL,
                    "Receita Federal (DAS SIMEI)", "imposto",
                    tag="das_dup_b", extras={"competencia": "2026-06"}))
    txs.append(nova("saida", datetime(2026, 8, 18, 9, 31), "boleto",
                    "DAS SIMEI 072026", DAS_MENSAL,
                    "Receita Federal (DAS SIMEI)", "imposto",
                    extras={"competencia": "2026-07"}))

    # 2.6 Anomalias pontuais.
    # Cobranca duplicada do fornecedor, 7h36 depois da primeira.
    txs.append(nova("saida", datetime(2026, 7, 14, 16, 48), "boleto",
                    "BELEZA DISTRIB LTDA 001", 487.60,
                    "Beleza Distribuidora LTDA", "insumo", tag="fornecedor_dup_copia"))
    # Assinatura de streaming cobrada duas vezes no mesmo dia.
    txs.append(nova("saida", datetime(2026, 8, 12, 21, 47), "debito_automatico",
                    "NETFLIX.COM 5511", 55.90, "Netflix", "assinatura",
                    tag="streaming_dup_copia"))
    # Tarifa de conta PJ que deixou de ser gratuita.
    txs.append(nova("saida", datetime(2026, 8, 5, 6, 22), "debito_automatico",
                    "TAR MANUT CONTA PJ PACOTE 2", 29.90,
                    "Banco Sudeste (conta PJ)", "tarifa", tag="tarifa_pj"))
    # Pagamento para contraparte sem historico.
    txs.append(nova("saida", datetime(2026, 8, 3, 18, 9), "pix",
                    "PIX ENVIADO MARIA S SOUZA", 340.00,
                    "Maria Souza", "nao_classificado", tag="contraparte_nova"))
    # Transacao em horario atipico, madrugada de domingo.
    txs.append(nova("saida", datetime(2026, 7, 19, 3, 41), "pix",
                    "PIX ENV BELEZA DISTRIB LTDA", 268.00,
                    "Beleza Distribuidora LTDA", "insumo", tag="horario_atipico"))

    # 2.7 Ordena e numera.
    txs.sort(key=lambda t: (t["_dt"], t["descritor_bruto"]))
    for i, t in enumerate(txs, start=1):
        t["id"] = "TX-%04d" % i
    return txs


# --------------------------------------------------------------------------
# 3. Montagem dos arquivos
# --------------------------------------------------------------------------

def por_tag(txs, tag):
    return [t for t in txs if t["_tag"] == tag]


def id_da_tag(txs, tag):
    achados = por_tag(txs, tag)
    assert len(achados) == 1, "tag %s apareceu %d vezes" % (tag, len(achados))
    return achados[0]["id"]


def limpar(txs):
    saida = []
    for t in txs:
        t = dict(t)
        t.pop("_dt", None)
        t.pop("_tag", None)
        saida.append(t)
    return saida


def projetar_teto(faturamento_mensal):
    """Projeta o estouro do teto pela tendencia dos tres ultimos meses."""
    jun, jul, ago = 8200.00, 9400.00, 10800.00
    passo = ((jul - jun) + (ago - jul)) / 2.0
    acumulado = faturamento_mensal
    mes_nomes = {9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}
    proximo = ago
    for m in (9, 10, 11, 12):
        proximo += passo
        anterior = acumulado
        acumulado += proximo
        if acumulado > TETO_MEI:
            falta = TETO_MEI - anterior
            dia = max(1, min(28, int(round(falta / (proximo / 30.0)))))
            return {
                "mes": mes_nomes[m],
                "data_estimada": "2026-%02d-%02d" % (m, dia),
                "acumulado_projetado_no_fim_do_mes": dinheiro(acumulado),
                "receita_mensal_projetada": dinheiro(proximo),
            }
    return None


def main():
    vendas = gerar_vendas()
    txs = gerar_transacoes(vendas)

    faturamento_periodo = dinheiro(sum(v["valor"] for v in vendas))
    faturamento_anterior = dinheiro(sum(v for _, v in FATURAMENTO_ANTERIOR))
    faturamento_ano = dinheiro(faturamento_anterior + faturamento_periodo)

    entradas = [t for t in txs if t["tipo"] == "entrada"]
    saidas = [t for t in txs if t["tipo"] == "saida"]
    recebido_liquido = dinheiro(sum(t["valor"] for t in entradas))
    total_saidas = dinheiro(sum(t["valor"] for t in saidas))

    # ---- transacoes.json --------------------------------------------------
    doc_tx = {
        "meta": {
            "produto": "Regis · Financial Anomaly Autopilot",
            "arquivo": "transacoes.json",
            "descricao": "Extrato da conta PJ da Angela, transação por transação.",
            "aviso": "Dados sintéticos, gerados por dados/gerar.py. Nenhuma pessoa ou empresa real.",
            "seed": SEED,
            "moeda": "BRL",
            "fuso": "America/Sao_Paulo",
            "periodo_detalhado": {"inicio": INICIO.isoformat(), "fim": FIM.isoformat()},
            "convencao_de_sinal": "valor é sempre positivo, a direção está em tipo (entrada ou saida)",
            "persona": {
                "nome": "Angela Nogueira",
                "negocio": "cabeleireira MEI no Studio Bella",
                "regime": "MEI",
                "cnae": "9602-5/01 cabeleireiros, manicure e pedicure",
                "cidade": "Campinas, SP",
                "vinculo": "aluga cadeira no Studio Bella, não é dona do salão",
                "atende": "terça a sábado, fechado segunda e domingo",
                "divide_o_salao_com": COLEGAS_DE_SALAO,
                "recebe_por": ["maquininha_credito", "maquininha_debito", "marketplace", "pix"],
                "controla_em": "caderno",
            },
        },
        "contexto": {
            "explicacao": "O que o motor precisa saber para transformar número em anomalia. Tudo aqui é contrato ou evento declarado, não é inferência.",
            "teto_mei_anual": TETO_MEI,
            "das": {
                "valor_mensal": DAS_MENSAL,
                "base": "5%% do salário mínimo de R$ %.2f, mais R$ 1,00 de ICMS e R$ 5,00 de ISS" % SALARIO_MINIMO_2026,
                "vencimento_dia": 20,
                "regra": "um pagamento por competência, competência do mês anterior",
            },
            "maquininha": {
                "adquirente": "Cielo",
                "terminal": "4829",
                "taxa_credito_contratada": TAXA_CREDITO_CONTRATADA,
                "taxa_debito_contratada": TAXA_DEBITO_CONTRATADA,
                "liquidacao": "D+0 para crédito (antecipação ligada) e D+0 para débito",
            },
            "antecipacao_automatica": {
                "ativa": True,
                "ativa_desde": ANTECIPACAO_ATIVA_DESDE.isoformat(),
                "taxa": TAXA_ANTECIPACAO,
                "contratada_conscientemente_pela_titular": False,
                "descritor": "CIELO ANTECIP AUTOM D+0",
            },
            "marketplace": {
                "nome": "BelezaNet",
                "comissao_contratada": COMISSAO_MARKETPLACE,
                "ciclo_de_repasse": "toda sexta, cobrindo as vendas de sexta anterior até quinta",
            },
            "conta_pj": {
                "banco": "Banco Sudeste",
                "pacote": "PJ Essencial",
                "tarifa_mensal_isenta_ate": "2026-07-31",
                "tarifa_mensal_a_partir_de": {"data": "2026-08-01", "valor": 29.90},
                "aviso_recebido_pela_titular": False,
            },
            "assinaturas_declaradas": [
                {"contraparte": "Agenda Salão App", "valor": 39.90, "dia_do_ciclo": 22,
                 "inicio": "2026-01-22", "cancelada_em": "2026-06-12",
                 "protocolo_de_cancelamento": "AGS-2026-88421"},
                {"contraparte": "SomPro Música Ambiente", "valor_contratado": 32.90,
                 "dia_do_ciclo": 8, "inicio": "2025-11-08", "cancelada_em": None,
                 "reajuste_avisado": False},
                {"contraparte": "Netflix", "valor": 55.90, "dia_do_ciclo": 12,
                 "inicio": "2024-03-12", "cancelada_em": None,
                 "observacao": "assinatura pessoal paga pela conta PJ"},
            ],
            "contrapartes_conhecidas": sorted({
                t["contraparte"] for t in txs
                if t["_tag"] != "contraparte_nova" and t["contraparte"] != "Maria Souza"
            }),
            "horario_habitual_de_movimento": {"inicio": "06:00", "fim": "23:59"},
            "feriados_no_periodo": [
                {"data": d.isoformat(), "nome": n} for d, n in sorted(FERIADOS.items())
            ],
        },
        "acumulado_anterior": {
            "explicacao": "Janeiro a maio de 2026 entram consolidados por mês, sem detalhe de transação. É o histórico que o motor fiscal soma ao período detalhado para chegar no acumulado do ano.",
            "meses": [
                {"mes": m, "faturamento_bruto": v} for m, v in FATURAMENTO_ANTERIOR
            ],
            "faturamento_bruto_total": faturamento_anterior,
            "das_pagos": ["2026-01", "2026-02", "2026-03", "2026-04"],
        },
        "totais": {
            "qtd_transacoes": len(txs),
            "qtd_entradas": len(entradas),
            "qtd_saidas": len(saidas),
            "faturamento_bruto_do_periodo": faturamento_periodo,
            "recebido_liquido_no_periodo": recebido_liquido,
            "saidas_no_periodo": total_saidas,
            "faturamento_bruto_acumulado_2026": faturamento_ano,
            "percentual_do_teto": round(faturamento_ano / TETO_MEI * 100, 1),
            "falta_para_o_teto": dinheiro(TETO_MEI - faturamento_ano),
        },
        "transacoes": limpar(txs),
    }

    # ---- vendas.json ------------------------------------------------------
    mapa_tx = {t["id"]: t for t in txs}
    lista_vendas = []
    for v in vendas:
        tx = v["_tx"]
        registro = {
            "id": v["id"],
            "data": iso(datetime.combine(v["data"], v["hora"])),
            "cliente": v["cliente"],
            "profissional": v["profissional"],
            "servico": v["servico"],
            "valor_venda": dinheiro(v["valor"]),
            "forma_recebimento": v["canal"],
            "transacao_id": tx["id"],
        }
        if v["canal"] == "marketplace":
            registro["marketplace"] = "BelezaNet"
            registro["repasse_previsto"] = dinheiro(v["valor"] * (1 - COMISSAO_MARKETPLACE))
            registro["data_repasse_previsto"] = tx["data"][:10]
        elif v["canal"] == "maquininha_credito":
            registro["taxa_contratada"] = TAXA_CREDITO_CONTRATADA
            registro["liquido_previsto"] = dinheiro(v["valor"] * (1 - TAXA_CREDITO_CONTRATADA))
        elif v["canal"] == "maquininha_debito":
            registro["taxa_contratada"] = TAXA_DEBITO_CONTRATADA
            registro["liquido_previsto"] = dinheiro(v["valor"] * (1 - TAXA_DEBITO_CONTRATADA))
        else:
            registro["liquido_previsto"] = dinheiro(v["valor"])
        lista_vendas.append(registro)

    por_canal = {}
    for v in vendas:
        por_canal.setdefault(v["canal"], {"qtd": 0, "bruto": 0.0})
        por_canal[v["canal"]]["qtd"] += 1
        por_canal[v["canal"]]["bruto"] += v["valor"]
    for c in por_canal:
        por_canal[c]["bruto"] = dinheiro(por_canal[c]["bruto"])
        por_canal[c]["participacao"] = round(por_canal[c]["bruto"] / faturamento_periodo * 100, 1)

    por_mes = {}
    for v in vendas:
        chave = v["data"].strftime("%Y-%m")
        por_mes.setdefault(chave, {"qtd": 0, "bruto": 0.0})
        por_mes[chave]["qtd"] += 1
        por_mes[chave]["bruto"] += v["valor"]
    for m in por_mes:
        por_mes[m]["bruto"] = dinheiro(por_mes[m]["bruto"])

    doc_vendas = {
        "meta": {
            "produto": "Regis · Financial Anomaly Autopilot",
            "arquivo": "vendas.json",
            "descricao": "Registro de atendimentos do lado da Angela. É o lado que permite cruzar o que foi vendido com o que caiu na conta.",
            "aviso": "Dados sintéticos, gerados por dados/gerar.py.",
            "seed": SEED,
            "moeda": "BRL",
            "periodo": {"inicio": INICIO.isoformat(), "fim": FIM.isoformat()},
            "como_cruzar": "cada venda aponta a transação que a liquidou em transacao_id. Cartão e Pix são um para um. Marketplace é muitos para um: várias vendas caem no mesmo repasse semanal.",
        },
        "totais": {
            "qtd_vendas": len(lista_vendas),
            "faturamento_bruto": faturamento_periodo,
            "ticket_medio": dinheiro(faturamento_periodo / len(lista_vendas)),
            "ticket_minimo": dinheiro(min(v["valor"] for v in vendas)),
            "ticket_maximo": dinheiro(max(v["valor"] for v in vendas)),
            "por_canal": por_canal,
            "por_mes": {m: por_mes[m] for m in sorted(por_mes)},
        },
        "vendas": lista_vendas,
    }

    # ---- anomalias-esperadas.json ----------------------------------------
    tx_forn_a = id_da_tag(txs, "fornecedor_dup_original")
    tx_forn_b = id_da_tag(txs, "fornecedor_dup_copia")
    tx_net_a = id_da_tag(txs, "streaming_dup_original")
    tx_net_b = id_da_tag(txs, "streaming_dup_copia")
    tx_agenda = [t["id"] for t in por_tag(txs, "pos_cancelamento")]
    tx_reajuste = id_da_tag(txs, "reajuste")
    tx_repasse = id_da_tag(txs, "repasse_curto")
    tx_das_a = id_da_tag(txs, "das_dup_a")
    tx_das_b = id_da_tag(txs, "das_dup_b")
    tx_antec = [t["id"] for t in por_tag(txs, "antecipacao")]
    tx_tarifa = id_da_tag(txs, "tarifa_pj")
    tx_taxa = [t["id"] for t in por_tag(txs, "taxa_efetiva")]
    tx_maria = id_da_tag(txs, "contraparte_nova")
    tx_madrugada = id_da_tag(txs, "horario_atipico")

    repasse = mapa_tx[tx_repasse]
    vendas_do_repasse = repasse["venda_ids"]

    total_antecipacao = dinheiro(sum(mapa_tx[i]["valor"] for i in tx_antec))
    excedente_taxa = dinheiro(sum(
        mapa_tx[i]["valor_bruto_venda"] * (TAXA_CREDITO_APLICADA_APOS_17_08 - TAXA_CREDITO_CONTRATADA)
        for i in tx_taxa))
    bruto_credito_pos = dinheiro(sum(mapa_tx[i]["valor_bruto_venda"] for i in tx_taxa))

    projecao = projetar_teto(faturamento_ano)

    anomalias = [
        {
            "id": "AN-01",
            "catalogo": "Cobrança duplicada do mesmo fornecedor em janela curta",
            "tipo": "duplicidade",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "Boleto do fornecedor pago duas vezes no mesmo dia",
            "descricao": "O boleto de R$ 487,60 da Beleza Distribuidora foi pago às 09:12 e de novo às 16:48 do dia 14/07/2026, 7 horas e 36 minutos depois.",
            "transacoes": [tx_forn_a, tx_forn_b],
            "valor_impacto": 487.60,
            "janela_horas": 7.6,
            "sinal_de_deteccao": "mesma contraparte, mesmo valor exato, intervalo menor que 24 horas, categoria sem repetição legítima",
            "acao_do_regis": "prepara o pedido de devolução para o fornecedor",
        },
        {
            "id": "AN-02",
            "catalogo": "Cobrança duplicada do mesmo fornecedor em janela curta",
            "tipo": "duplicidade",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "Assinatura cobrada duas vezes no dia 12",
            "descricao": "A Netflix cobrou R$ 55,90 às 09:14 e de novo às 21:47 do dia 12/08/2026. É a mesma competência cobrada duas vezes.",
            "transacoes": [tx_net_a, tx_net_b],
            "valor_impacto": 55.90,
            "janela_horas": 12.55,
            "sinal_de_deteccao": "mesma contraparte, mesmo valor, intervalo menor que 24 horas, e a série mensal já tem uma cobrança no ciclo",
            "acao_do_regis": "redige a contestação para o cartão",
        },
        {
            "id": "AN-03",
            "catalogo": "Serviço cancelado que continua sendo cobrado",
            "tipo": "recorrencia",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "Assinatura do app de agenda segue cobrando depois do cancelamento",
            "descricao": "O Agenda Salão App foi cancelado em 12/06/2026 (protocolo AGS-2026-88421) e continuou cobrando R$ 39,90 em 22/06, 22/07 e 22/08.",
            "transacoes": tx_agenda,
            "valor_impacto": dinheiro(39.90 * len(tx_agenda)),
            "sinal_de_deteccao": "série mensal de 28 a 31 dias com valor constante, com data de cancelamento anterior registrada em contexto.assinaturas_declaradas",
            "contexto_necessario": "contexto.assinaturas_declaradas[Agenda Salao App].cancelada_em",
            "acao_do_regis": "redige a contestação das três cobranças e cobra o cancelamento",
        },
        {
            "id": "AN-04",
            "catalogo": "Assinatura ou serviço que subiu de preço sem aviso",
            "tipo": "valor",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "Reajuste silencioso do som ambiente",
            "descricao": "SomPro Música Ambiente cobrava R$ 32,90 em junho e julho. Em 08/08/2026 cobrou R$ 47,90, alta de 45,6% sem aviso.",
            "transacoes": [tx_reajuste],
            "transacoes_de_referencia": [t["id"] for t in txs
                                         if t["contraparte"] == "SomPro Música Ambiente"
                                         and t["id"] != tx_reajuste],
            "valor_impacto": 15.00,
            "valor_impacto_anualizado": 180.00,
            "sinal_de_deteccao": "série mensal da mesma contraparte com valor constante que salta acima de 10% em uma parcela",
            "acao_do_regis": "mostra o antes e depois e escreve o pedido de explicação ou cancelamento",
        },
        {
            "id": "AN-05",
            "catalogo": "Repasse de marketplace menor que a venda, sem comissão ou retenção explicada",
            "tipo": "conciliacao",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "Repasse da BelezaNet veio R$ 38,00 menor que o previsto",
            "descricao": "O repasse de sexta 28/08/2026 cobriu %d vendas que somam R$ %.2f. Com a comissão contratada de 12%% deveriam ter caído R$ %.2f, e caíram R$ %.2f. Faltam R$ 38,00 sem retenção ou comissão explicada." % (
                len(vendas_do_repasse), repasse["valor_bruto_venda"],
                dinheiro(repasse["valor_bruto_venda"] * (1 - COMISSAO_MARKETPLACE)),
                repasse["valor"]),
            "transacoes": [tx_repasse],
            "vendas": vendas_do_repasse,
            "valor_bruto_das_vendas": repasse["valor_bruto_venda"],
            "repasse_esperado": dinheiro(repasse["valor_bruto_venda"] * (1 - COMISSAO_MARKETPLACE)),
            "repasse_recebido": repasse["valor"],
            "valor_impacto": 38.00,
            "sinal_de_deteccao": "soma das vendas do ciclo menos a comissão contratada, comparada com o valor creditado",
            "contexto_necessario": "contexto.marketplace.comissao_contratada e vendas.json",
            "acao_do_regis": "escreve a cobrança do repasse para o marketplace",
        },
        {
            "id": "AN-06",
            "catalogo": "DAS pago duas vezes no mesmo mês",
            "tipo": "duplicidade",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "DAS da competência 06/2026 pago duas vezes",
            "descricao": "O DAS de R$ 87,05 da competência 06/2026 foi pago em 17/07 e de novo em 20/07. A duplicidade não cabe na janela de 24 horas, ela se detecta pela competência.",
            "transacoes": [tx_das_a, tx_das_b],
            "competencia": "2026-06",
            "valor_impacto": DAS_MENSAL,
            "sinal_de_deteccao": "dois pagamentos com a mesma competência fiscal no mesmo mês de caixa",
            "acao_do_regis": "monta o pedido de restituição ou compensação do DAS",
        },
        {
            "id": "AN-07",
            "catalogo": "Antecipação automática ligada sem a pessoa ter percebido",
            "tipo": "valor",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "Antecipação automática descontando das vendas todo dia",
            "descricao": "A antecipação automática está ligada desde 02/03/2026 e desconta %.2f%% do crédito todo dia. No período detalhado são %d descontos que somam R$ %.2f." % (
                TAXA_ANTECIPACAO * 100, len(tx_antec), total_antecipacao),
            "transacoes": tx_antec,
            "qtd_lancamentos": len(tx_antec),
            "valor_impacto": total_antecipacao,
            "taxa": TAXA_ANTECIPACAO,
            "sinal_de_deteccao": "lançamento diário da adquirente proporcional ao volume de crédito do dia, com descritor de antecipação",
            "contexto_necessario": "contexto.antecipacao_automatica.contratada_conscientemente_pela_titular",
            "acao_do_regis": "soma o custo, mostra o total e entrega o passo a passo para desligar",
        },
        {
            "id": "AN-08",
            "catalogo": "Tarifa de conta PJ que deixou de ser gratuita",
            "tipo": "valor",
            "certeza": "fato",
            "comportamento_esperado": "resolve",
            "titulo": "Tarifa nova de manutenção da conta PJ",
            "descricao": "A conta era isenta até 31/07/2026. Em 05/08 apareceu a primeira tarifa de manutenção de R$ 29,90, sem aviso recebido.",
            "transacoes": [tx_tarifa],
            "valor_impacto": 29.90,
            "valor_impacto_anualizado": 358.80,
            "sinal_de_deteccao": "cobrança do próprio banco sem nenhuma ocorrência anterior na série histórica",
            "contexto_necessario": "contexto.conta_pj.tarifa_mensal_isenta_ate",
            "acao_do_regis": "mostra o custo anual e escreve o pedido de isenção ou a comparação de contas",
        },
        {
            "id": "AN-09",
            "catalogo": "Faturamento acumulado em ritmo de estourar o teto anual",
            "tipo": "fiscal",
            "certeza": "regra",
            "comportamento_esperado": "encaminha",
            "titulo": "No ritmo atual o teto de R$ 81.000 estoura em %s" % (projecao["mes"] if projecao else "não estoura no ano"),
            "descricao": "Faturamento bruto acumulado de 2026 até 29/08: R$ %.2f, que é %.1f%% do teto. Faltam R$ %.2f. A série de junho, julho e agosto cresce em média R$ %.2f por mês." % (
                faturamento_ano, faturamento_ano / TETO_MEI * 100,
                TETO_MEI - faturamento_ano, 1300.00),
            "transacoes": [],
            "valor_impacto": 0.00,
            "observacao_sobre_o_impacto": "aqui não há dinheiro perdido. O que está em jogo é o regime: passar do teto significa desenquadramento retroativo a janeiro, multa de 0,33% ao dia e juros Selic.",
            "escopo": "todas as entradas de venda do ano, somando o acumulado de janeiro a maio",
            "faturamento_acumulado": faturamento_ano,
            "teto": TETO_MEI,
            "percentual_do_teto": round(faturamento_ano / TETO_MEI * 100, 1),
            "falta_para_o_teto": dinheiro(TETO_MEI - faturamento_ano),
            "projecao": projecao,
            "sinal_de_deteccao": "soma da receita bruta do ano contra o teto, com projeção pela tendência dos três últimos meses",
            "acao_do_regis": "encaminha a decisão. Explica as opções: segurar faturamento, migrar para ME ou se preparar para o desenquadramento",
        },
        {
            "id": "AN-10",
            "catalogo": "Taxa efetiva da maquininha diferente da contratada",
            "tipo": "valor",
            "certeza": "regra",
            "comportamento_esperado": "encaminha",
            "titulo": "A maquininha passou a descontar 3,49% em vez de 2,89%",
            "descricao": "De 17/08 a 29/08/2026 as vendas no crédito vieram com desconto efetivo de 3,49%%, contra os 2,89%% contratados. São %d vendas, R$ %.2f de volume bruto e R$ %.2f cobrados a mais." % (
                len(tx_taxa), bruto_credito_pos, excedente_taxa),
            "transacoes": tx_taxa,
            "qtd_transacoes": len(tx_taxa),
            "taxa_contratada": TAXA_CREDITO_CONTRATADA,
            "taxa_efetiva_observada": TAXA_CREDITO_APLICADA_APOS_17_08,
            "volume_bruto_afetado": bruto_credito_pos,
            "valor_impacto": excedente_taxa,
            "sinal_de_deteccao": "1 menos (valor recebido dividido por valor_bruto_venda) comparado com a taxa contratada, agrupado por período",
            "contexto_necessario": "contexto.maquininha.taxa_credito_contratada",
            "acao_do_regis": "encaminha, porque depende do contrato da titular com a adquirente. Mostra a diferença e escreve a contestação para a Cielo",
        },
        {
            "id": "AN-11",
            "catalogo": "Pagamento para contraparte sem nenhum histórico",
            "tipo": "contraparte",
            "certeza": "suspeita",
            "comportamento_esperado": "pergunta",
            "titulo": "Pix de R$ 340,00 para Maria Souza",
            "descricao": "Em 03/08/2026 saiu um Pix de R$ 340,00 para Maria Souza. Não existe nenhum pagamento anterior para essa contraparte no histórico. Na demo a resposta é legítima: é a manicure nova.",
            "transacoes": [tx_maria],
            "valor_impacto": 0.00,
            "resposta_esperada_na_demo": "foi eu, é a manicure nova",
            "sinal_de_deteccao": "contraparte que não aparece em contexto.contrapartes_conhecidas nem em nenhuma transação anterior",
            "acao_do_regis": "pergunta uma vez e registra a resposta. Não pergunta de novo sobre a mesma contraparte",
        },
        {
            "id": "AN-12",
            "catalogo": "Transação de madrugada, fim de semana ou feriado",
            "tipo": "comportamento",
            "certeza": "suspeita",
            "comportamento_esperado": "pergunta",
            "titulo": "Pix de R$ 268,00 às 03:41 de um domingo",
            "descricao": "Em 19/07/2026, um domingo, saiu um Pix de R$ 268,00 às 03:41 para a Beleza Distribuidora. A contraparte é conhecida, o horário não. Todo o resto do extrato acontece entre 06:00 e 23:59.",
            "transacoes": [tx_madrugada],
            "valor_impacto": 0.00,
            "sinal_de_deteccao": "horário fora da faixa de movimento habitual, em dia sem expediente",
            "acao_do_regis": "registra em silêncio ou pergunta junto com outra suspeita. Nunca alarma sozinho",
        },
    ]

    total_fato = dinheiro(sum(a["valor_impacto"] for a in anomalias if a["certeza"] == "fato"))
    total_regra = dinheiro(sum(a["valor_impacto"] for a in anomalias if a["certeza"] == "regra"))

    doc_anomalias = {
        "meta": {
            "produto": "Regis · Financial Anomaly Autopilot",
            "arquivo": "anomalias-esperadas.json",
            "descricao": "Gabarito. Quais anomalias foram plantadas, em quais transações, de que tipo e com que nível de certeza. Serve para testar o motor de detecção.",
            "aviso": "Dados sintéticos, gerados por dados/gerar.py.",
            "seed": SEED,
            "referencia": "catálogo em pesquisa do grupo/catalogo-anomalias_mei.html, tese em BRIEFING.md seção 3.2",
            "tese": "a autonomia do autopilot varia com a certeza. Fato ele resolve, regra ele encaminha, suspeita ele pergunta.",
        },
        "resumo": {
            "total_de_anomalias": len(anomalias),
            "por_certeza": {
                "fato": len([a for a in anomalias if a["certeza"] == "fato"]),
                "regra": len([a for a in anomalias if a["certeza"] == "regra"]),
                "suspeita": len([a for a in anomalias if a["certeza"] == "suspeita"]),
            },
            "por_tipo": {
                t: len([a for a in anomalias if a["tipo"] == t])
                for t in sorted({a["tipo"] for a in anomalias})
            },
            "dinheiro_recuperavel_fato": total_fato,
            "dinheiro_em_jogo_regra": total_regra,
            "qtd_transacoes_marcadas": len({i for a in anomalias for i in a["transacoes"]}),
        },
        "anomalias": anomalias,
        "falsos_positivos_esperados": [
            {
                "titulo": "Aluguel de cadeira de R$ 1.850,00 todo dia 5",
                "por_que_parece": "é o maior valor que sai no mês",
                "por_que_nao_e": "série mensal estável, valor idêntico, contraparte conhecida",
            },
            {
                "titulo": "Duas compras no mesmo fornecedor dentro do mesmo mês",
                "por_que_parece": "mesma contraparte repetida",
                "por_que_nao_e": "valores diferentes e intervalo de 10 dias, é o ritmo normal de reposição",
            },
            {
                "titulo": "Vendas de R$ 250,00 a R$ 380,00 em química",
                "por_que_parece": "ticket muito acima da média de R$ 85",
                "por_que_nao_e": "acontecem toda semana e sempre em serviço de química",
            },
            {
                "titulo": "DAS pago todo mês",
                "por_que_parece": "cobrança recorrente do governo",
                "por_que_nao_e": "é obrigação mensal. Só a competência repetida em julho é anomalia",
            },
            {
                "titulo": "Pico de movimento nas sextas e sábados",
                "por_que_parece": "volume muito acima dos outros dias",
                "por_que_nao_e": "é o padrão da agenda dela em todas as semanas do período",
            },
            {
                "titulo": "Pix único para o Supermercado Bom Preço",
                "por_que_parece": "aparece uma vez só no período, então poderia passar por contraparte nova",
                "por_que_nao_e": "está em contexto.contrapartes_conhecidas. É a diferença entre contraparte nova e contraparte pouco frequente",
            },
            {
                "titulo": "Taxa de 1,49% no débito",
                "por_que_parece": "desconto sobre a venda",
                "por_que_nao_e": "bate com a taxa contratada, então a Regis confere e cala",
            },
        ],
    }

    # ---- escrita ----------------------------------------------------------
    def salvar(nome, doc):
        caminho = RAIZ / nome
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return caminho

    salvar("transacoes.json", doc_tx)
    salvar("vendas.json", doc_vendas)
    salvar("anomalias-esperadas.json", doc_anomalias)

    # ---- conferencia ------------------------------------------------------
    print("=" * 68)
    print("REGIS · dataset sintetico gerado")
    print("=" * 68)
    print("periodo detalhado ......... %s a %s" % (INICIO, FIM))
    print("transacoes ................ %d (%d entradas, %d saidas)"
          % (len(txs), len(entradas), len(saidas)))
    print("vendas .................... %d" % len(lista_vendas))
    print("ticket medio .............. R$ %.2f (min R$ %.2f, max R$ %.2f)"
          % (faturamento_periodo / len(vendas),
             min(v["valor"] for v in vendas), max(v["valor"] for v in vendas)))
    print("-" * 68)
    for m in sorted(por_mes):
        print("faturamento %s ........ R$ %10.2f  (%d vendas)"
              % (m, por_mes[m]["bruto"], por_mes[m]["qtd"]))
    print("jan a mai (consolidado) ... R$ %10.2f" % faturamento_anterior)
    print("-" * 68)
    print("FATURAMENTO BRUTO 2026 .... R$ %10.2f   (alvo R$ 58.400,00)" % faturamento_ano)
    print("percentual do teto ........ %.1f%%" % (faturamento_ano / TETO_MEI * 100))
    print("falta para o teto ......... R$ %10.2f" % (TETO_MEI - faturamento_ano))
    if projecao:
        print("estoura o teto em ......... %s (%s)" % (projecao["mes"], projecao["data_estimada"]))
    print("-" * 68)
    print("recebido liquido (jun-ago). R$ %10.2f" % recebido_liquido)
    print("saidas (jun-ago) .......... R$ %10.2f" % total_saidas)
    print("-" * 68)
    for c in sorted(por_canal, key=lambda k: -por_canal[k]["bruto"]):
        print("canal %-20s R$ %10.2f  (%.1f%%, %d vendas)"
              % (c, por_canal[c]["bruto"], por_canal[c]["participacao"], por_canal[c]["qtd"]))
    print("-" * 68)
    print("anomalias plantadas ....... %d (%d fato, %d regra, %d suspeita)"
          % (len(anomalias),
             doc_anomalias["resumo"]["por_certeza"]["fato"],
             doc_anomalias["resumo"]["por_certeza"]["regra"],
             doc_anomalias["resumo"]["por_certeza"]["suspeita"]))
    print("recuperavel (fato) ........ R$ %10.2f" % total_fato)
    print("-" * 68)
    for a in anomalias:
        ids = ", ".join(a["transacoes"][:4])
        if len(a["transacoes"]) > 4:
            ids += ", ... (+%d)" % (len(a["transacoes"]) - 4)
        print("%s %-9s %-28s %s" % (a["id"], a["certeza"], a["titulo"][:28], ids or "(agregado)"))
    print("=" * 68)

    # travas
    assert abs(faturamento_ano - 58400.00) < 0.01, "faturamento do ano nao fechou"
    assert len(vendas) == len(lista_vendas)
    for v, registro in zip(vendas, lista_vendas):
        tx = mapa_tx[registro["transacao_id"]]
        if v["canal"] == "marketplace":
            assert registro["id"] in tx["venda_ids"], "venda de marketplace ligada ao repasse errado"
            assert tx["data"][:10] >= v["data"].isoformat(), "repasse anterior a venda"
        else:
            assert tx["venda_ids"] == [registro["id"]], "venda ligada a transacao errada"
            assert tx["data"][:10] == v["data"].isoformat(), "data da transacao nao bate com a venda"
            assert abs((tx["valor_bruto_venda"] or tx["valor"]) - v["valor"]) < 0.005
    print("conferencia OK: faturamento fecha em R$ 58.400,00 e toda venda aponta uma transacao.")


if __name__ == "__main__":
    main()
