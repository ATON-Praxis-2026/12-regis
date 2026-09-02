"""Carregamento dos arquivos e utilidades comuns do motor.

Só stdlib. Nada de rede, nada de dependência externa.
"""

import json
import os
import unicodedata
from datetime import datetime, timedelta

MESES_PT = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]

DIAS_PT = [
    "segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo",
]


def carregar(dir_dados="dados"):
    """Lê transacoes.json e vendas.json e devolve um pacote pronto para os detectores."""
    caminho_tx = os.path.join(dir_dados, "transacoes.json")
    caminho_vd = os.path.join(dir_dados, "vendas.json")

    with open(caminho_tx, encoding="utf-8") as arq:
        bruto_tx = json.load(arq)
    with open(caminho_vd, encoding="utf-8") as arq:
        bruto_vd = json.load(arq)

    transacoes = bruto_tx["transacoes"]
    vendas = bruto_vd["vendas"]

    vendas_por_transacao = {}
    for venda in vendas:
        alvo = venda.get("transacao_id")
        if alvo:
            vendas_por_transacao.setdefault(alvo, []).append(venda)

    return {
        "meta": bruto_tx.get("meta", {}),
        "contexto": bruto_tx.get("contexto", {}),
        "acumulado_anterior": bruto_tx.get("acumulado_anterior", {}),
        "totais": bruto_tx.get("totais", {}),
        "transacoes": transacoes,
        "transacoes_por_id": {t["id"]: t for t in transacoes},
        "vendas": vendas,
        "vendas_por_transacao": vendas_por_transacao,
        "data_referencia": max(quando(t) for t in transacoes),
    }


def quando(transacao):
    """Data e hora da transação, já com fuso."""
    return datetime.fromisoformat(transacao["data"])


def dia(transacao):
    """Só a data, sem hora."""
    return quando(transacao).date()


def horas_entre(a, b):
    """Distância em horas entre duas transações, sempre positiva."""
    return abs((quando(b) - quando(a)).total_seconds()) / 3600.0


def normalizar(texto):
    """Tira acento, sobe para maiúscula e troca pontuação por espaço."""
    if not texto:
        return ""
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    limpo = []
    for caractere in sem_acento.upper():
        limpo.append(caractere if caractere.isalnum() else " ")
    return " ".join("".join(limpo).split())


SUFIXOS_DE_RAZAO_SOCIAL = {"LTDA", "ME", "SA", "EIRELI", "MEI", "EPP", "CIA"}


def nome_curto(nome):
    """Vira o nome que a pessoa usa. 'Beleza Distribuidora LTDA' vira 'Beleza Distribuidora'."""
    base = (nome or "").split("(")[0].strip()
    tokens = base.split()
    while tokens and tokens[-1].upper().strip(".") in SUFIXOS_DE_RAZAO_SOCIAL:
        tokens.pop()
    return " ".join(tokens) or base


def moeda(valor):
    """Formata em real brasileiro. R$ 1.145,15"""
    if valor is None:
        return "R$ 0,00"
    negativo = valor < 0
    inteiro = "{:,.2f}".format(abs(valor))
    inteiro = inteiro.replace(",", "@").replace(".", ",").replace("@", ".")
    return ("R$ -" if negativo else "R$ ") + inteiro


def data_br(valor):
    """14/07/2026 a partir de string ISO, date ou datetime."""
    momento = _para_data(valor)
    return momento.strftime("%d/%m/%Y")


def dia_mes(valor):
    """14/07 a partir de string ISO, date ou datetime."""
    return _para_data(valor).strftime("%d/%m")


def hora_br(valor):
    """09:12 a partir de string ISO ou datetime."""
    if isinstance(valor, str):
        valor = datetime.fromisoformat(valor)
    return valor.strftime("%H:%M")


def mes_por_extenso(numero):
    return MESES_PT[numero - 1]


def dia_da_semana(valor):
    return DIAS_PT[_para_data(valor).weekday()]


def dias_no_mes(ano, mes):
    if mes == 12:
        proximo = datetime(ano + 1, 1, 1)
    else:
        proximo = datetime(ano, mes + 1, 1)
    return (proximo - timedelta(days=1)).day


def _para_data(valor):
    if isinstance(valor, str):
        return datetime.fromisoformat(valor).date()
    if isinstance(valor, datetime):
        return valor.date()
    return valor


def achado(
    identificador,
    certeza,
    tipo,
    titulo,
    explicacao,
    valor=None,
    transacoes=None,
    acao=None,
):
    """Monta o dicionário de achado no formato combinado com a interface pública."""
    return {
        "id": identificador,
        "certeza": certeza,
        "tipo": tipo,
        "titulo": titulo,
        "explicacao": explicacao,
        "valor": valor,
        "transacoes": list(transacoes or []),
        "acao": acao,
    }


def acao(tipo, titulo, texto):
    """Monta a ação pronta para a pessoa copiar e enviar."""
    return {"tipo": tipo, "titulo": titulo, "texto": texto.strip()}
