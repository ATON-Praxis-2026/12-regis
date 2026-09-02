"""Validação do motor contra o gabarito.

Roda o motor contra dados/anomalias-esperadas.json e responde três perguntas:

1. Quantas das 12 anomalias plantadas o motor encontrou.
2. Quantos falsos positivos ele produziu, conferindo também a lista de
   falsos_positivos_esperados do gabarito, que são as seis coisas que parecem
   anomalia e não são.
3. Qual a precisão.

Uso:

    python3 motor/testar.py
    python3 -m motor.testar
    python3 motor/testar.py dados

O casamento entre achado e gabarito é feito por tipo mais interseção de
transações, nunca por id. O id do achado é posicional, ele não é a resposta.
"""

import json
import os
import sys

try:
    from .detectar import detectar
    from .dados import carregar
    from .identificar import identificar_todas
except ImportError:  # execução direta, sem pacote
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from detectar import detectar
    from dados import carregar
    from identificar import identificar_todas

LARGURA = 78

# Como reconhecer, no extrato, cada um dos falsos positivos que o gabarito lista.
# Se o motor gritar em cima de uma destas transações, ele errou.
ARMADILHAS = [
    {
        "titulo": "Aluguel de cadeira de R$ 1.850,00 todo dia 5",
        "regra": lambda t: t.get("categoria") == "aluguel",
    },
    {
        "titulo": "Duas compras no mesmo fornecedor dentro do mesmo mês",
        "regra": lambda t: t.get("categoria") == "insumo",
        "excecoes": ("TX-0165", "TX-0167"),
    },
    {
        "titulo": "Vendas de R$ 250,00 a R$ 380,00 em química",
        "regra": lambda t: (
            t["tipo"] == "entrada"
            and t.get("categoria") == "venda"
            and (t.get("valor_bruto_venda") or t["valor"]) >= 250.0
        ),
    },
    {
        "titulo": "DAS pago todo mês",
        "regra": lambda t: t.get("categoria") == "imposto",
        "excecoes": ("TX-0175", "TX-0193"),
    },
    {
        "titulo": "Pico de movimento nas sextas e sábados",
        "regra": lambda t: (
            t["tipo"] == "entrada" and t.get("categoria") == "venda"
        ),
    },
    {
        "titulo": "Pix único para o Supermercado Bom Preço",
        "regra": lambda t: t.get("categoria") == "pessoal",
    },
    {
        "titulo": "Taxa de 1,49% no débito",
        "regra": lambda t: t.get("canal") == "maquininha_debito",
        "excecoes": (),
    },
]


def rodar(dir_dados="dados"):
    """Roda o motor, compara com o gabarito e devolve o placar."""
    caminho_gabarito = os.path.join(dir_dados, "anomalias-esperadas.json")
    with open(caminho_gabarito, encoding="utf-8") as arq:
        gabarito = json.load(arq)

    resultado = detectar(dir_dados)
    achados = resultado["achados"]
    silenciados = resultado["silenciados"]

    encontradas = []
    perdidas = []
    usados = set()

    for esperada in gabarito["anomalias"]:
        candidato = _casar(esperada, achados, usados)
        if candidato:
            usados.add(candidato["id"])
            encontradas.append((esperada, candidato, _cobertura(esperada, candidato)))
        else:
            calado = _casar(esperada, silenciados, set())
            perdidas.append((esperada, calado))

    falsos_positivos = [a for a in achados if a["id"] not in usados]
    armadilhas = _conferir_armadilhas(dir_dados, achados, gabarito)

    total_esperado = len(gabarito["anomalias"])
    precisao = (len(encontradas) / float(len(achados))) * 100 if achados else 0.0
    recall = (len(encontradas) / float(total_esperado)) * 100 if total_esperado else 0.0

    return {
        "resultado": resultado,
        "gabarito": gabarito,
        "encontradas": encontradas,
        "perdidas": perdidas,
        "falsos_positivos": falsos_positivos,
        "armadilhas": armadilhas,
        "precisao": round(precisao, 1),
        "recall": round(recall, 1),
    }


def _casar(esperada, candidatos, usados):
    """Casa por tipo mais interseção de transações. Sem transação, casa só por tipo."""
    esperadas = set(esperada.get("transacoes") or [])
    melhor = None
    melhor_intersecao = 0
    for candidato in candidatos:
        if candidato["id"] in usados:
            continue
        if candidato["tipo"] != esperada["tipo"]:
            continue
        if not esperadas:
            return candidato
        intersecao = len(esperadas.intersection(candidato["transacoes"]))
        if intersecao > melhor_intersecao:
            melhor_intersecao = intersecao
            melhor = candidato
    return melhor


def _cobertura(esperada, candidato):
    esperadas = set(esperada.get("transacoes") or [])
    if not esperadas:
        return 1.0
    return len(esperadas.intersection(candidato["transacoes"])) / float(len(esperadas))


def _conferir_armadilhas(dir_dados, achados, gabarito):
    """Confere se o motor gritou em cima de alguma das seis coisas que são normais."""
    pacote = carregar(dir_dados)
    marcadas = set()
    for item in achados:
        marcadas.update(item["transacoes"])

    # Transações que o gabarito reconhece como anomalia de verdade.
    legitimas = set()
    for anomalia in gabarito["anomalias"]:
        legitimas.update(anomalia.get("transacoes") or [])

    relatorio = []
    for armadilha in ARMADILHAS:
        excecoes = set(armadilha.get("excecoes", ()))
        alvo = [
            t for t in pacote["transacoes"]
            if armadilha["regra"](t) and t["id"] not in excecoes and t["id"] not in legitimas
        ]
        acusadas = sorted(t["id"] for t in alvo if t["id"] in marcadas)
        relatorio.append({
            "titulo": armadilha["titulo"],
            "conferidas": len(alvo),
            "acusadas": acusadas,
            "passou": not acusadas,
        })
    return relatorio


# ---------------------------------------------------------------- relatório


def imprimir(placar):
    gabarito = placar["gabarito"]
    resultado = placar["resultado"]
    achados = resultado["achados"]
    total_esperado = len(gabarito["anomalias"])

    _titulo("Regis, validação do motor contra o gabarito")
    print("Anomalias plantadas no dataset : %s" % total_esperado)
    print("Achados que o motor reportou   : %s" % len(achados))
    print("Silenciados                    : %s" % len(resultado["silenciados"]))
    print("")

    _titulo("1. Anomalias encontradas")
    for esperada, candidato, cobertura in placar["encontradas"]:
        print("  ok  %s  %s" % (esperada["id"], esperada["titulo"]))
        print("      motor: [%s] %s" % (candidato["id"], candidato["titulo"]))
        print("      certeza esperada %s, motor %s. Transações cobertas: %d%%"
              % (esperada["certeza"], candidato["certeza"], round(cobertura * 100)))
        _conferir_valor(esperada, candidato)
    for esperada, calado in placar["perdidas"]:
        print("  NAO %s  %s" % (esperada["id"], esperada["titulo"]))
        if calado:
            print("      atenção: caiu na lista de silenciados como [%s] %s"
                  % (calado["id"], calado["titulo"]))
    print("")
    print("  Encontradas: %s de %s. Recall %.1f%%"
          % (len(placar["encontradas"]), total_esperado, placar["recall"]))
    print("")

    _titulo("2. Falsos positivos")
    if placar["falsos_positivos"]:
        for item in placar["falsos_positivos"]:
            print("  FP  [%s] %s · %s · %s"
                  % (item["id"], item["titulo"], item["certeza"], item["transacoes"][:4]))
    else:
        print("  Nenhum achado sobrando. Todo achado do motor casa com uma anomalia do gabarito.")
    print("")
    print("  Contra a lista de falsos_positivos_esperados do gabarito:")
    for linha in placar["armadilhas"]:
        marca = "ok " if linha["passou"] else "FP "
        print("  %s %s (%s transações conferidas)"
              % (marca, linha["titulo"], linha["conferidas"]))
        if not linha["passou"]:
            print("      o motor acusou: %s" % ", ".join(linha["acusadas"]))
    print("")

    _titulo("3. Precisão")
    print("  Precisão : %.1f%% (%s achados certos em %s reportados)"
          % (placar["precisao"], len(placar["encontradas"]), len(achados)))
    print("  Recall   : %.1f%% (%s de %s anomalias plantadas)"
          % (placar["recall"], len(placar["encontradas"]), total_esperado))
    falsos = len(placar["falsos_positivos"]) + sum(
        0 if l["passou"] else 1 for l in placar["armadilhas"]
    )
    print("  Falsos positivos: %s" % falsos)
    print("")

    _titulo("4. Números do resumo, contra o gabarito")
    _comparar_resumo(placar)
    print("")

    _titulo("5. Identificação de contraparte")
    _relatorio_de_identificacao(placar)
    print("")

    _titulo("6. Ações escritas")
    _relatorio_de_acoes(achados)
    print("")

    aprovado = (
        len(placar["encontradas"]) == total_esperado
        and not placar["falsos_positivos"]
        and all(l["passou"] for l in placar["armadilhas"])
    )
    print("RESULTADO: %s" % (
        "as %s anomalias, zero falso positivo." % total_esperado if aprovado
        else "ainda falta ajustar, veja as linhas marcadas acima."
    ))
    return aprovado


def _conferir_valor(esperada, candidato):
    esperado = esperada.get("valor_impacto")
    obtido = candidato.get("valor")
    if not esperado or obtido is None:
        return
    if abs(esperado - obtido) <= max(0.02, esperado * 0.01):
        print("      valor: R$ %.2f, bate com o gabarito" % obtido)
    else:
        print("      valor: R$ %.2f, o gabarito diz R$ %.2f" % (obtido, esperado))


def _comparar_resumo(placar):
    resumo = placar["resultado"]["resumo"]
    esperado = None
    for anomalia in placar["gabarito"]["anomalias"]:
        if anomalia["tipo"] == "fiscal":
            esperado = anomalia
            break
    alvo = {
        "faturamento_acumulado": esperado.get("faturamento_acumulado") if esperado else None,
        "teto": esperado.get("teto") if esperado else None,
        "percentual_do_teto": esperado.get("percentual_do_teto") if esperado else None,
        "falta_para_o_teto": esperado.get("falta_para_o_teto") if esperado else None,
        "projecao_estouro": (esperado.get("projecao") or {}).get("data_estimada") if esperado else None,
        "total_recuperavel": placar["gabarito"]["resumo"].get("dinheiro_recuperavel_fato"),
    }
    for chave, valor_esperado in alvo.items():
        obtido = resumo.get(chave)
        if valor_esperado is None:
            print("  %-22s %s" % (chave, obtido))
            continue
        bate = obtido == valor_esperado or (
            isinstance(obtido, float) and isinstance(valor_esperado, float)
            and abs(obtido - valor_esperado) < 0.01
        )
        print("  %s %-22s motor %s, gabarito %s"
              % ("ok " if bate else "DIF", chave, obtido, valor_esperado))
    print("  %-26s %s" % ("qtd_transacoes_conferidas", resumo["qtd_transacoes_conferidas"]))


def _relatorio_de_identificacao(placar):
    """Compara o nome deduzido do descritor com o campo contraparte do dataset.

    Dois grupos ficam de fora da conta, e por motivo declarado:
    o Pix recebido no QR, em que o extrato não traz o nome de quem pagou, e as
    nove saídas pessoais em que gerar.py sorteia descritor e contraparte de forma
    independente, o que faz o próprio dataset discordar de si mesmo.
    """
    dir_dados = placar.get("dir_dados", "dados")
    pacote = carregar(dir_dados)
    identificacoes = identificar_todas(pacote["transacoes"], pacote["contexto"])

    conferidas = 0
    certas = 0
    divergentes = []
    for transacao in pacote["transacoes"]:
        if transacao.get("categoria") == "pessoal":
            continue
        identificacao = identificacoes[transacao["id"]]
        if identificacao["nome"] == "Cliente do salão":
            continue
        conferidas += 1
        if identificacao["nome"] == transacao["contraparte"]:
            certas += 1
        else:
            divergentes.append((transacao["descritor_bruto"], identificacao["nome"],
                                transacao["contraparte"]))

    taxa = (certas / float(conferidas) * 100) if conferidas else 0.0
    print("  Descritores traduzidos corretamente: %s de %s (%.1f%%)"
          % (certas, conferidas, taxa))
    for descritor, deduzido, verdadeiro in divergentes[:5]:
        print("      %s lido como %s, dataset diz %s" % (descritor, deduzido, verdadeiro))
    print("  Fora da conta, por motivo declarado: Pix recebido no QR, em que o extrato")
    print("  não traz o nome, e as saídas pessoais, em que o gerador sorteia descritor")
    print("  e contraparte separado e o próprio dataset discorda de si mesmo.")


def _relatorio_de_acoes(achados):
    fatos = [a for a in achados if a["certeza"] == "fato"]
    com_acao = [a for a in fatos if a.get("acao") and a["acao"].get("texto")]
    print("  Achados de certeza fato: %s. Com ação pronta para enviar: %s"
          % (len(fatos), len(com_acao)))
    for item in achados:
        if item.get("acao"):
            print("      [%s] %s · %s · %s caracteres"
                  % (item["id"], item["acao"]["tipo"], item["acao"]["titulo"],
                     len(item["acao"]["texto"])))
        else:
            print("      [%s] sem ação, é %s e a Regis pergunta antes"
                  % (item["id"], item["certeza"]))


def _titulo(texto):
    print(texto)
    print("=" * min(LARGURA, len(texto)))


if __name__ == "__main__":
    diretorio = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "dados"
    placar = rodar(diretorio)
    placar["dir_dados"] = diretorio
    ok = imprimir(placar)
    sys.exit(0 if ok else 1)
