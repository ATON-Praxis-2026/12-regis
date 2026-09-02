"""Apoio para a redação dos achados e das ações.

O tom vem da seção 3.7 do briefing. A Regis desarma, não acusa. Ela diz
"achei R$ 47 saindo à toa", nunca "detectamos anomalia". Quem lê é a Angela,
não um analista de risco.
"""

try:
    from .dados import data_br, moeda
except ImportError:  # execução direta, sem pacote
    from dados import data_br, moeda


def assinatura(meta):
    """Fecho das mensagens, com o nome do negócio da persona."""
    persona = (meta or {}).get("persona", {})
    nome = persona.get("nome", "")
    negocio = persona.get("negocio", "")
    if nome and negocio:
        return "%s\n%s" % (nome, negocio)
    return nome or negocio or ""


def lista_de_datas(datas):
    """Vira '22/06/2026, 22/07/2026 e 22/08/2026'."""
    formatadas = [data_br(d) for d in datas]
    if len(formatadas) == 1:
        return formatadas[0]
    return ", ".join(formatadas[:-1]) + " e " + formatadas[-1]


def lista_de_valores(valores):
    formatados = [moeda(v) for v in valores]
    if len(formatados) == 1:
        return formatados[0]
    return ", ".join(formatados[:-1]) + " e " + formatados[-1]


def percentual(fracao, casas=1):
    """0.0349 vira '3,49%'. Usa vírgula, que é como a pessoa lê."""
    texto = ("{:." + str(casas) + "f}").format(fracao * 100)
    return texto.replace(".", ",") + "%"


def numero(valor, casas=2):
    texto = ("{:." + str(casas) + "f}").format(valor)
    return texto.replace(".", ",")
