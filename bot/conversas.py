#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lê o registro de conversas da Regis.

O bot grava tudo em conversas.jsonl. Este script é o outro lado: transforma
aquele arquivo em coisa que dá para ler e decidir.

    python3 bot/conversas.py                    resumo do que aconteceu
    python3 bot/conversas.py --ler              a conversa inteira, legível
    python3 bot/conversas.py --ler 123456       só a conversa daquele chat
    python3 bot/conversas.py --buracos          o que ela não soube responder
    python3 bot/conversas.py --perguntas        tudo que as pessoas perguntaram

O arquivo vem de REGIS_CONVERSAS, ou de bot/conversas.jsonl. Para ler o do
servidor, baixe antes com deploy/conversas.sh.
"""

import collections
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.environ.get("REGIS_CONVERSAS") or os.path.join(AQUI, "conversas.jsonl")

# De onde a resposta saiu. É a leitura mais útil do registro: mostra quanto do
# produto o código resolve sozinho e quanto depende do modelo.
ROTULOS = {
    "ia": "conversa livre (IA)",
    "deterministico": "resposta do código",
    "sem_resposta": "não soube responder",
    "botao": "botão",
    "anexo": "print ou documento",
}


def carregar(caminho=None):
    caminho = caminho or ARQUIVO
    if not os.path.exists(caminho):
        print("Não achei %s.\nSe o bot roda no servidor, baixe antes:"
              "\n    bash deploy/conversas.sh" % caminho)
        sys.exit(1)
    linhas = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            try:
                linhas.append(json.loads(linha))
            except Exception:
                continue
    return linhas


def resumo(linhas):
    chats = collections.Counter(l["chat"] for l in linhas)
    vias = collections.Counter(l.get("via") for l in linhas if l["papel"] == "regis")
    perguntas = [l for l in linhas if l["papel"] == "pessoa"]
    dias = sorted({l["quando"][:10] for l in linhas})

    print("REGISTRO DA REGIS")
    print("=" * 52)
    print("arquivo      %s" % ARQUIVO)
    print("período      %s" % (" a ".join([dias[0], dias[-1]]) if dias else "vazio"))
    print("mensagens    %d" % len(linhas))
    print("conversas    %d" % len(chats))
    print("perguntas    %d" % len(perguntas))
    if chats:
        print("média        %.1f mensagens por conversa" % (len(linhas) / len(chats)))

    print("\nDE ONDE SAIU A RESPOSTA")
    print("-" * 52)
    total = sum(vias.values()) or 1
    for via, quantas in vias.most_common():
        rotulo = ROTULOS.get(via, via or "comando")
        print("  %-24s %4d   %5.1f%%" % (rotulo, quantas, quantas * 100.0 / total))

    mudas = [l for l in linhas if l.get("via") == "sem_resposta"]
    if mudas:
        print("\n%d respostas em que ela não soube o que dizer."
              " Rode --buracos para ver as perguntas." % len(mudas))


def ler(linhas, chat=None):
    if chat:
        linhas = [l for l in linhas if str(l["chat"]) == str(chat)]
    atual = None
    for l in linhas:
        if l["chat"] != atual:
            atual = l["chat"]
            print("\n" + "=" * 52)
            print("conversa %s" % atual)
            print("=" * 52)
        quem = (l.get("nome") or "pessoa") if l["papel"] == "pessoa" else "Regis"
        marca = "" if l["papel"] == "pessoa" else "  [%s]" % ROTULOS.get(l.get("via"), l.get("via") or "")
        print("\n%s  %s%s" % (l["quando"][11:16], quem, marca))
        for pedaco in l["texto"].split("\n"):
            print("   %s" % pedaco)


def buracos(linhas):
    """
    As perguntas que vieram logo antes de uma resposta genérica.

    É o material mais valioso do registro: é a lista do que o produto ainda
    não cobre, escrita pelas próprias pessoas.
    """
    achados = []
    for anterior, atual in zip(linhas, linhas[1:]):
        if (atual.get("via") == "sem_resposta" and anterior["papel"] == "pessoa"
                and anterior["chat"] == atual["chat"]):
            achados.append(anterior)
    if not achados:
        print("Nenhuma. Ela respondeu tudo que perguntaram.")
        return
    print("O QUE ELA NÃO SOUBE RESPONDER (%d)" % len(achados))
    print("=" * 52)
    for l in achados:
        print("  %s  %s" % (l["quando"][:16].replace("T", " "), l["texto"]))


def perguntas(linhas):
    todas = [l for l in linhas if l["papel"] == "pessoa" and l.get("via") != "botao"]
    print("PERGUNTAS DAS PESSOAS (%d)" % len(todas))
    print("=" * 52)
    for texto, quantas in collections.Counter(l["texto"] for l in todas).most_common():
        print("  %2dx  %s" % (quantas, texto) if quantas > 1 else "       %s" % texto)


def main():
    argumentos = sys.argv[1:]
    linhas = carregar()
    if not argumentos:
        resumo(linhas)
    elif argumentos[0] == "--ler":
        ler(linhas, argumentos[1] if len(argumentos) > 1 else None)
    elif argumentos[0] == "--buracos":
        buracos(linhas)
    elif argumentos[0] == "--perguntas":
        perguntas(linhas)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
