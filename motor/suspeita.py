"""Detector de suspeita.

Aqui a Regis não afirma nada. Ela pergunta uma vez, registra a resposta e não
volta ao assunto. São dois sinais:

1. Contraparte sem nenhum histórico, nem na lista de conhecidas nem em qualquer
   lançamento anterior do extrato.
2. Transação fora da faixa de horário em que o negócio se move.

A diferença entre contraparte nova e contraparte pouco frequente é o que separa
uma pergunta útil de um alarme falso. O supermercado que aparece uma vez só no
período é conhecido, e sobre ele a Regis fica quieta.
"""

from datetime import time

try:
    from .dados import (achado, data_br, dia_da_semana, hora_br, moeda,
                        nome_curto, quando)
    from .textos import numero
except ImportError:  # execução direta, sem pacote
    from dados import (achado, data_br, dia_da_semana, hora_br, moeda,
                       nome_curto, quando)
    from textos import numero

VALOR_MINIMO_PARA_PERGUNTAR = 50.0


def detectar(pacote, identificacoes):
    """Devolve (achados, silenciados)."""
    achados = []
    silenciados = []

    novas, conhecidas_raras = _contraparte_sem_historico(pacote, identificacoes)
    achados.extend(novas)
    silenciados.extend(conhecidas_raras)

    achados.extend(_horario_atipico(pacote, identificacoes))
    return achados, silenciados


def _contraparte_sem_historico(pacote, identificacoes):
    contexto = pacote["contexto"]
    conhecidas = set(contexto.get("contrapartes_conhecidas", []) or [])
    transacoes = sorted(pacote["transacoes"], key=quando)

    ja_vistas = set()
    achados = []
    raras = {}

    for transacao in transacoes:
        identificacao = identificacoes[transacao["id"]]
        nome = identificacao["nome"]
        primeira_vez = nome not in ja_vistas
        ja_vistas.add(nome)

        if transacao["tipo"] != "saida":
            continue
        if nome in conhecidas or identificacao.get("conhecida"):
            # Banco, adquirente, marketplace e Receita não entram na conta de
            # "contraparte pouco frequente". Eles têm detector próprio.
            if identificacao.get("natureza") in ("empresa", "pessoa"):
                raras.setdefault(nome, []).append(transacao)
            continue
        if not primeira_vez:
            continue
        if transacao["valor"] < VALOR_MINIMO_PARA_PERGUNTAR:
            continue

        curto = nome_curto(nome)
        explicacao = (
            "Saiu um %s de %s para %s em %s, e essa é a primeira vez que esse nome "
            "aparece na sua conta. Pode ser gente nova trabalhando com você, pode ser "
            "compra pontual. Se foi você, me diz que eu registro e não pergunto de novo."
            % (
                identificacao.get("canal", "pagamento"),
                moeda(transacao["valor"]),
                curto,
                data_br(transacao["data"]),
            )
        )
        achados.append(
            achado(
                "SUS-CONTRAPARTE-%s" % transacao["id"],
                "suspeita",
                "contraparte",
                "%s de %s para %s, nome novo na conta"
                % (identificacao.get("canal", "Pagamento").capitalize(),
                   moeda(transacao["valor"]),
                   curto),
                explicacao,
                valor=None,
                transacoes=[transacao["id"]],
                acao=None,
            )
        )

    silenciados = _conhecidas_pouco_frequentes(raras)
    return achados, silenciados


def _conhecidas_pouco_frequentes(raras):
    """Contraparte pouco frequente não é contraparte nova, e essa diferença evita alarme falso."""
    poucas = [(nome, lista) for nome, lista in sorted(raras.items()) if len(lista) <= 2]
    if not poucas:
        return []
    nomes = ", ".join(nome_curto(nome) for nome, _ in poucas)
    return [
        achado(
            "SIL-CONTRAPARTE-RARA",
            "suspeita",
            "contraparte",
            "Contrapartes que aparecem pouco, e são suas conhecidas",
            "No período, %s nomes receberam pagamento uma ou duas vezes só: %s. "
            "Eles já estão no seu histórico, então é contraparte pouco frequente, "
            "não contraparte nova. Não vou te perguntar sobre eles."
            % (numero(len(poucas), 0), nomes),
            valor=None,
            transacoes=[t["id"] for _, lista in poucas for t in lista],
            acao=None,
        )
    ]


def _horario_atipico(pacote, identificacoes):
    faixa = pacote["contexto"].get("horario_habitual_de_movimento", {}) or {}
    inicio = _hora(faixa.get("inicio"), time(6, 0))
    fim = _hora(faixa.get("fim"), time(23, 59))

    achados = []
    for transacao in sorted(pacote["transacoes"], key=quando):
        momento = quando(transacao)
        if inicio <= momento.time() <= fim:
            continue
        identificacao = identificacoes[transacao["id"]]
        curto = nome_curto(identificacao["nome"])
        conhecida = "para %s, que você conhece" % curto if identificacao.get("conhecida") \
            else "para %s" % curto
        explicacao = (
            "Em %s, um %s, saiu %s às %s %s. Todo o resto da sua conta acontece entre "
            "%s e %s. Pode ter sido agendamento, pode ter sido você mesma. "
            "Só quero ouvir de você antes de deixar passar."
            % (
                data_br(transacao["data"]),
                dia_da_semana(transacao["data"]),
                moeda(transacao["valor"]),
                hora_br(transacao["data"]),
                conhecida,
                faixa.get("inicio", "06:00"),
                faixa.get("fim", "23:59"),
            )
        )
        achados.append(
            achado(
                "SUS-HORARIO-%s" % transacao["id"],
                "suspeita",
                "comportamento",
                "%s de %s às %s de um %s" % (
                    identificacao.get("canal", "Pagamento").capitalize(),
                    moeda(transacao["valor"]),
                    hora_br(transacao["data"]),
                    dia_da_semana(transacao["data"]),
                ),
                explicacao,
                valor=None,
                transacoes=[transacao["id"]],
                acao=None,
            )
        )
    return achados


def _hora(texto, padrao):
    if not texto:
        return padrao
    partes = texto.split(":")
    try:
        return time(int(partes[0]), int(partes[1]))
    except (ValueError, IndexError):
        return padrao
