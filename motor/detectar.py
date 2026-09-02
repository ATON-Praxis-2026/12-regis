"""Interface pública do motor de detecção da Regis.

    from motor.detectar import detectar
    resultado = detectar("dados")

Roda a identificação de contraparte primeiro, porque todo o resto depende dela,
e depois os detectores na ordem da seção 3.8 do briefing. Devolve resumo,
achados ordenados por certeza e a lista do que ele achou e escolheu não falar.

Python 3, só stdlib, sem rede.
"""

import json
import sys

try:
    from . import conciliacao, duplicidade, fiscal, recorrencia, suspeita, valor
    from .dados import carregar, nome_curto
    from .identificar import identificar_todas
except ImportError:  # execução direta, sem pacote
    import conciliacao
    import duplicidade
    import fiscal
    import recorrencia
    import suspeita
    import valor
    from dados import carregar, nome_curto
    from identificar import identificar_todas

# A ordem é a da ordem de construção do briefing. Identificação vem antes de tudo.
DETECTORES = [
    ("duplicidade", duplicidade),
    ("recorrencia", recorrencia),
    ("conciliacao", conciliacao),
    ("valor", valor),
    ("fiscal", fiscal),
    ("suspeita", suspeita),
]

PESO_DA_CERTEZA = {"fato": 0, "regra": 1, "suspeita": 2}


def detectar(dir_dados="dados"):
    """Roda todos os detectores e devolve os achados."""
    pacote = carregar(dir_dados)
    identificacoes = identificar_todas(pacote["transacoes"], pacote["contexto"])

    achados = []
    silenciados = []
    for _, detector in DETECTORES:
        encontrados, calados = detector.detectar(pacote, identificacoes)
        achados.extend(encontrados)
        silenciados.extend(calados)

    achados = _ordenar(achados)
    silenciados = _limpar_silenciados(silenciados, achados)
    achados = _renumerar(achados)
    _nomear_contrapartes(achados + silenciados, identificacoes)

    return {
        "resumo": _resumo(pacote, achados),
        "achados": achados,
        "silenciados": silenciados,
    }


def _ordenar(achados):
    """Fato primeiro, depois regra, depois suspeita. Dentro de cada faixa, o maior valor na frente."""
    return sorted(
        achados,
        key=lambda a: (
            PESO_DA_CERTEZA.get(a["certeza"], 9),
            -(a["valor"] or 0),
            a["id"],
        ),
    )


def _renumerar(achados):
    """Dá ao achado um id curto e estável para a interface, na ordem em que ele será mostrado."""
    for posicao, item in enumerate(achados, start=1):
        item["id"] = "AN-%02d" % posicao
    return achados


def _limpar_silenciados(silenciados, achados):
    """Nada entra na lista de silenciados se encostar numa transação que virou achado.

    Sem isso a Regis diria, na mesma tela, que a assinatura está estável e que ela
    foi cobrada duas vezes. As duas coisas são verdade, mas juntas confundem.
    """
    marcadas = set()
    for item in achados:
        marcadas.update(item["transacoes"])

    limpos = []
    for posicao, item in enumerate(silenciados, start=1):
        if marcadas.intersection(item["transacoes"]):
            continue
        item["id"] = "SIL-%02d" % (len(limpos) + 1)
        limpos.append(item)
    return limpos


def _nomear_contrapartes(itens, identificacoes):
    """Campo extra, fora do contrato mínimo, porque a tela precisa de um nome para mostrar.

    É a contraparte que mais aparece entre as transações do achado. Fica None quando
    o achado é agregado e não aponta para transação nenhuma, como o do teto.
    """
    for item in itens:
        contagem = {}
        for identificador in item["transacoes"]:
            identificacao = identificacoes.get(identificador)
            if not identificacao:
                continue
            nome = nome_curto(identificacao["nome"])
            contagem[nome] = contagem.get(nome, 0) + 1
        if contagem:
            item["contraparte"] = max(sorted(contagem), key=lambda n: contagem[n])
        else:
            item["contraparte"] = None
    return itens


def _resumo(pacote, achados):
    teto = fiscal.calcular_teto(pacote)
    recuperavel = round(
        sum(a["valor"] or 0 for a in achados if a["certeza"] == "fato"), 2
    )
    return {
        "faturamento_acumulado": teto["acumulado"],
        "teto": teto["teto"],
        "percentual_do_teto": teto["percentual_do_teto"],
        "falta_para_o_teto": teto["falta"],
        "projecao_estouro": teto["projecao"].get("data"),
        "total_recuperavel": recuperavel,
        "qtd_transacoes_conferidas": len(pacote["transacoes"]),
    }


def _imprimir(resultado):
    resumo = resultado["resumo"]
    print("Regis, motor de detecção")
    print("Transações conferidas: %s" % resumo["qtd_transacoes_conferidas"])
    print("Faturamento acumulado: R$ %.2f (%.1f%% do teto)"
          % (resumo["faturamento_acumulado"], resumo["percentual_do_teto"]))
    print("Projeção de estouro: %s" % (resumo["projecao_estouro"] or "não estoura no ritmo atual"))
    print("Total recuperável: R$ %.2f" % resumo["total_recuperavel"])
    print("")
    for item in resultado["achados"]:
        valor_texto = "R$ %.2f" % item["valor"] if item["valor"] is not None else "sem valor direto"
        print("[%s] %s · %s · %s" % (item["id"], item["certeza"], item["tipo"], valor_texto))
        print("  %s" % item["titulo"])
        print("  %s" % item["explicacao"])
        if item["acao"]:
            print("  ação (%s): %s" % (item["acao"]["tipo"], item["acao"]["titulo"]))
        print("")
    print("Silenciados, o que ele conferiu e escolheu não falar:")
    for item in resultado["silenciados"]:
        print("  [%s] %s" % (item["id"], item["titulo"]))


if __name__ == "__main__":
    argumentos = [a for a in sys.argv[1:] if not a.startswith("-")]
    diretorio = argumentos[0] if argumentos else "dados"
    saida = detectar(diretorio)
    if "--json" in sys.argv:
        print(json.dumps(saida, ensure_ascii=False, indent=2))
    else:
        _imprimir(saida)
