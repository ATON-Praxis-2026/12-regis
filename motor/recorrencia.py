"""Detector de recorrência.

Monta a série mensal de cada contraparte que sai da conta. Série é intervalo de
28 a 31 dias entre uma cobrança e a seguinte. Com a série montada, duas coisas
aparecem quase de graça:

1. Assinatura que continua cobrando depois da data de cancelamento declarada.
2. Reajuste silencioso, a mesma série com o valor mudando sem aviso.

E uma terceira, que é metade da tese do produto: a série que está certa e sobre
a qual a Regis não fala nada.
"""

from datetime import date

try:
    from .dados import achado, acao, data_br, dia, moeda, nome_curto, normalizar, quando
    from .textos import assinatura, lista_de_datas, numero, percentual
except ImportError:  # execução direta, sem pacote
    from dados import achado, acao, data_br, dia, moeda, nome_curto, normalizar, quando
    from textos import assinatura, lista_de_datas, numero, percentual

INTERVALO_MINIMO = 28
INTERVALO_MAXIMO = 31
SALTO_QUE_IMPORTA = 0.10  # 10% para cima já merece explicação

# Categorias em que o valor variar mês a mês é o esperado, porque é consumo.
CATEGORIAS_DE_CONSUMO = {"utilidade"}


def detectar(pacote, identificacoes):
    """Devolve (achados, silenciados)."""
    series = montar_series(pacote, identificacoes)
    contexto = pacote["contexto"]

    achados = []
    tratadas = set()

    for item in _canceladas_que_seguem_cobrando(pacote, series, contexto):
        achados.append(item["achado"])
        tratadas.add(item["contraparte"])

    for item in _reajuste_silencioso(pacote, series, tratadas):
        achados.append(item["achado"])
        tratadas.add(item["contraparte"])

    silenciados = _series_que_conferem(pacote, series, tratadas)
    return achados, silenciados


def montar_series(pacote, identificacoes):
    """Agrupa as saídas por contraparte e devolve só as que têm cara de mensalidade."""
    por_contraparte = {}
    for transacao in pacote["transacoes"]:
        if transacao["tipo"] != "saida":
            continue
        identificacao = identificacoes[transacao["id"]]
        if identificacao.get("natureza_do_lancamento") == "antecipacao":
            continue
        if transacao.get("categoria") in ("venda", "repasse"):
            continue
        por_contraparte.setdefault(identificacao["nome"], []).append(transacao)

    series = {}
    for nome, transacoes in por_contraparte.items():
        transacoes = sorted(transacoes, key=quando)
        unicas = _uma_por_dia(transacoes)
        if len(unicas) < 2:
            continue
        intervalos = [
            (dia(unicas[i + 1]) - dia(unicas[i])).days for i in range(len(unicas) - 1)
        ]
        mensais = [i for i in intervalos if INTERVALO_MINIMO <= i <= INTERVALO_MAXIMO]
        if not mensais or len(mensais) < len(intervalos):
            continue
        series[nome] = {
            "contraparte": nome,
            "transacoes": unicas,
            "todas": transacoes,
            "intervalos": intervalos,
            "valores": [t["valor"] for t in unicas],
            "categoria": unicas[-1].get("categoria"),
        }
    return series


def _uma_por_dia(transacoes):
    """Colapsa cobranças do mesmo dia, senão a duplicidade quebraria a série."""
    vistas = {}
    for transacao in transacoes:
        chave = dia(transacao)
        if chave not in vistas:
            vistas[chave] = transacao
    return [vistas[c] for c in sorted(vistas)]


# ------------------------------------------------- assinatura cancelada


def _canceladas_que_seguem_cobrando(pacote, series, contexto):
    resultados = []
    for declarada in contexto.get("assinaturas_declaradas", []) or []:
        cancelada_em = declarada.get("cancelada_em")
        if not cancelada_em:
            continue
        nome = declarada["contraparte"]
        serie = _serie_de(series, nome)
        if not serie:
            continue
        corte = date.fromisoformat(cancelada_em)
        depois = [t for t in serie["todas"] if dia(t) > corte]
        if not depois:
            continue

        valor = round(sum(t["valor"] for t in depois), 2)
        mensal = depois[0]["valor"]
        protocolo = declarada.get("protocolo_de_cancelamento")
        curto = nome_curto(nome)

        explicacao = (
            "Você cancelou a %s em %s%s, e mesmo assim ela cobrou %s em %s. "
            "São %s que saíram depois do cancelamento, e esse dinheiro volta."
            % (
                curto,
                data_br(cancelada_em),
                (", protocolo %s" % protocolo) if protocolo else "",
                moeda(mensal),
                lista_de_datas([t["data"] for t in depois]),
                moeda(valor),
            )
        )

        resultados.append({
            "contraparte": nome,
            "achado": achado(
                "REC-CANCELADA-%s" % normalizar(curto).replace(" ", "-"),
                "fato",
                "recorrencia",
                "A %s continua cobrando depois do cancelamento" % curto,
                explicacao,
                valor=valor,
                transacoes=[t["id"] for t in depois],
                acao=acao(
                    "contestacao",
                    "Cobrança do estorno e da baixa do cancelamento",
                    _texto_cancelamento_nao_honrado(
                        pacote, curto, declarada, depois, valor, mensal
                    ),
                ),
            ),
        })
    return resultados


def _texto_cancelamento_nao_honrado(pacote, curto, declarada, depois, valor, mensal):
    persona = pacote["meta"].get("persona", {}) or {}
    protocolo = declarada.get("protocolo_de_cancelamento")
    linhas = "\n".join(
        "%s, %s" % (data_br(t["data"]), moeda(t["valor"])) for t in depois
    )
    return """Assunto: cobranças após cancelamento%s

Olá,

Sou %s, %s. Cancelei a assinatura da %s em %s%s.

Mesmo com o cancelamento registrado, a cobrança de %s continuou saindo da minha conta:

%s

São %s cobrados depois do pedido de cancelamento. Peço duas coisas:

1. O estorno de %s na conta de origem.
2. A confirmação por escrito de que a assinatura está encerrada e de que não haverá nova cobrança.

Se preferirem, envio os comprovantes de cada débito. Fico no aguardo do retorno.

%s""" % (
        (", protocolo %s" % protocolo) if protocolo else "",
        persona.get("nome", ""),
        persona.get("negocio", ""),
        curto,
        data_br(declarada.get("cancelada_em")),
        (", protocolo %s" % protocolo) if protocolo else "",
        moeda(mensal),
        linhas,
        moeda(valor),
        moeda(valor),
        assinatura(pacote["meta"]),
    )


# ------------------------------------------------- reajuste silencioso


def _reajuste_silencioso(pacote, series, tratadas):
    resultados = []
    for nome, serie in sorted(series.items()):
        if nome in tratadas:
            continue
        if serie["categoria"] in CATEGORIAS_DE_CONSUMO:
            continue
        valores = serie["valores"]
        if len(valores) < 3:
            continue
        anteriores = valores[:-1]
        if len(set(round(v, 2) for v in anteriores)) != 1:
            continue  # série que já variava, aqui não dá para afirmar nada
        antigo = round(anteriores[0], 2)
        novo = round(valores[-1], 2)
        if antigo <= 0:
            continue
        if novo <= antigo * (1 + SALTO_QUE_IMPORTA):
            continue
        diferenca = round(novo - antigo, 2)
        alta = (novo - antigo) / antigo
        ultima = serie["transacoes"][-1]
        curto = nome_curto(nome)

        explicacao = (
            "A %s cobrava %s por mês e em %s passou a cobrar %s, uma alta de %s "
            "sem nenhum aviso. São %s a mais por mês, %s no ano se ficar assim."
            % (
                curto,
                moeda(antigo),
                data_br(ultima["data"]),
                moeda(novo),
                percentual(alta),
                moeda(diferenca),
                moeda(round(diferenca * 12, 2)),
            )
        )

        resultados.append({
            "contraparte": nome,
            "achado": achado(
                "REC-REAJUSTE-%s" % normalizar(curto).replace(" ", "-"),
                "fato",
                "valor",
                "A %s subiu de preço sem avisar" % curto,
                explicacao,
                valor=diferenca,
                transacoes=[ultima["id"]],
                acao=acao(
                    "cancelamento",
                    "Pedido de explicação ou cancelamento",
                    _texto_reajuste(pacote, curto, serie, antigo, novo, diferenca, alta),
                ),
            ),
        })
    return resultados


def _texto_reajuste(pacote, curto, serie, antigo, novo, diferenca, alta):
    persona = pacote["meta"].get("persona", {}) or {}
    anteriores = serie["transacoes"][:-1]
    ultima = serie["transacoes"][-1]
    linhas = "\n".join(
        "%s, %s" % (data_br(t["data"]), moeda(t["valor"])) for t in anteriores
    )
    return """Olá, tudo bem?

Sou %s, %s, e sou assinante da %s.

A mensalidade vinha assim:

%s

E em %s foi cobrado %s, uma diferença de %s, alta de %s. Não recebi nenhum aviso de reajuste, nem por mensagem nem pelo aplicativo.

Peço que me informem:

1. Qual foi o motivo e a data do reajuste.
2. Se houve comunicação prévia, para qual contato ela foi enviada.
3. Se é possível manter o valor anterior de %s.

Se não for possível manter o valor anterior, considerem esta mensagem como pedido de cancelamento da assinatura, com a confirmação por escrito.

Obrigada.

%s""" % (
        persona.get("nome", ""),
        persona.get("negocio", ""),
        curto,
        linhas,
        data_br(ultima["data"]),
        moeda(novo),
        moeda(diferenca),
        percentual(alta),
        moeda(antigo),
        assinatura(pacote["meta"]),
    )


# ------------------------------------------------- o que ele confere e cala


def _series_que_conferem(pacote, series, tratadas):
    silenciados = []
    contador = 0
    for nome, serie in sorted(series.items()):
        if nome in tratadas:
            continue
        valores = [round(v, 2) for v in serie["valores"]]
        if len(set(valores)) != 1:
            continue
        contador += 1
        curto = nome_curto(nome)
        silenciados.append(
            achado(
                "SIL-SERIE-%02d" % contador,
                "fato",
                "recorrencia",
                "%s, mensalidade estável" % curto,
                "Sai %s todo mês, %s vezes seguidas, sempre no mesmo dia e no mesmo valor. "
                "É contraparte conhecida e o valor não mudou, então não tem por que te avisar."
                % (moeda(valores[0]), numero(len(valores), 0)),
                valor=None,
                transacoes=[t["id"] for t in serie["transacoes"]],
                acao=None,
            )
        )
    return silenciados


def _serie_de(series, nome):
    if nome in series:
        return series[nome]
    alvo = normalizar(nome.split("(")[0])
    for chave, serie in series.items():
        if normalizar(chave.split("(")[0]) == alvo:
            return serie
    return None
