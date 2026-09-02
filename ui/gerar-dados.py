#!/usr/bin/env python3
"""
Roda o motor e escreve ui/dados.json, que é o que as telas leem.

Assim o número que aparece no app é o mesmo que a Regis calcula no Telegram.
Rode sempre que o dataset ou o motor mudarem:

    python3 ui/gerar-dados.py
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from motor.detectar import detectar  # noqa: E402


def moeda(valor):
    """1180.0 vira '1.180,00'."""
    if valor is None:
        return None
    texto = "%.2f" % float(valor)
    inteiro, centavos = texto.split(".")
    negativo = inteiro.startswith("-")
    inteiro = inteiro.lstrip("-")
    partes = []
    while len(inteiro) > 3:
        partes.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    partes.insert(0, inteiro)
    return ("-" if negativo else "") + ".".join(partes) + "," + centavos


MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def mes_por_extenso(data_iso):
    if not data_iso:
        return None
    try:
        _, mes, _ = str(data_iso).split("-")
        return MESES[int(mes) - 1]
    except Exception:
        return None


def main():
    resultado = detectar(os.path.join(RAIZ, "dados"))
    resumo = resultado["resumo"]

    transacoes = json.load(open(os.path.join(RAIZ, "dados", "transacoes.json"),
                                encoding="utf-8"))
    perfil = transacoes.get("contexto", {}).get("perfil", {}) or {}
    meta = transacoes.get("meta", {}) or {}
    if not perfil:
        for bloco in (meta, transacoes):
            if isinstance(bloco, dict) and bloco.get("nome"):
                perfil = bloco
                break

    faturado = float(resumo.get("faturamento_acumulado") or 0)
    teto = float(resumo.get("teto") or 81000)

    saida = {
        "gerado_em": meta.get("gerado_em") or "",
        "perfil": {
            "nome": perfil.get("nome") or "Angela Nogueira",
            "primeiro_nome": (perfil.get("nome") or "Angela").split()[0],
            "negocio": perfil.get("negocio") or "cabeleireira MEI no Studio Bella",
        },
        "resumo": {
            "faturado": faturado,
            "faturado_txt": moeda(faturado),
            "teto": teto,
            "teto_txt": moeda(teto),
            "percentual": round(faturado / teto * 100, 1) if teto else 0,
            "falta": float(resumo.get("falta_para_o_teto") or 0),
            "falta_txt": moeda(resumo.get("falta_para_o_teto")),
            "estouro": resumo.get("projecao_estouro"),
            "estouro_mes": mes_por_extenso(resumo.get("projecao_estouro")),
            "recuperavel": float(resumo.get("total_recuperavel") or 0),
            "recuperavel_txt": moeda(resumo.get("total_recuperavel")),
            "transacoes_conferidas": resumo.get("qtd_transacoes_conferidas"),
        },
        "achados": [],
        "silenciados": [],
    }

    for achado in resultado.get("achados", []):
        saida["achados"].append({
            "id": achado.get("id"),
            "certeza": achado.get("certeza"),
            "tipo": achado.get("tipo"),
            "titulo": achado.get("titulo"),
            "explicacao": achado.get("explicacao"),
            "valor": achado.get("valor"),
            "valor_txt": moeda(achado.get("valor")),
            "tem_acao": bool(achado.get("acao")),
            "acao_titulo": (achado.get("acao") or {}).get("titulo"),
        })

    for silenciado in resultado.get("silenciados", []):
        saida["silenciados"].append({
            "titulo": silenciado.get("titulo"),
            "explicacao": silenciado.get("explicacao"),
        })

    por_certeza = {}
    for achado in saida["achados"]:
        por_certeza[achado["certeza"]] = por_certeza.get(achado["certeza"], 0) + 1
    saida["contagem"] = {
        "fatos": por_certeza.get("fato", 0),
        "regras": por_certeza.get("regra", 0),
        "suspeitas": por_certeza.get("suspeita", 0),
        "silenciados": len(saida["silenciados"]),
    }

    destino = os.path.join(RAIZ, "ui", "dados.json")
    with open(destino, "w", encoding="utf-8") as arquivo:
        json.dump(saida, arquivo, ensure_ascii=False, indent=2)

    print("ui/dados.json gerado")
    print("  %s, %s" % (saida["perfil"]["nome"], saida["perfil"]["negocio"]))
    print("  faturado R$ %s de R$ %s (%.1f%%), faltam R$ %s"
          % (saida["resumo"]["faturado_txt"], saida["resumo"]["teto_txt"],
             saida["resumo"]["percentual"], saida["resumo"]["falta_txt"]))
    print("  estouro em %s" % (saida["resumo"]["estouro_mes"] or "sem projeção"))
    print("  %d fatos, %d regras, %d suspeitas, %d silenciados"
          % (saida["contagem"]["fatos"], saida["contagem"]["regras"],
             saida["contagem"]["suspeitas"], saida["contagem"]["silenciados"]))
    print("  recuperável R$ %s" % saida["resumo"]["recuperavel_txt"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
