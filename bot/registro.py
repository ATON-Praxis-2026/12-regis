#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Registro das conversas da Regis.

Um arquivo só resolve dois problemas que na verdade são o mesmo:

1. **Memória recente.** A Regis precisa saber o que acabou de ser dito. Sem
   isso ela responde bem uma pergunta e esquece a própria resposta na pergunta
   seguinte, porque cada chamada ao modelo ia sozinha, sem nada antes dela.
2. **Análise depois.** Toda mensagem, dos dois lados, vira uma linha no
   arquivo. Depois dá para ler tudo e descobrir o que as pessoas realmente
   perguntam, quais perguntas a Regis não soube responder e quanto cada
   conversa custou.

O formato é JSONL, uma linha JSON por mensagem. Escrever é sempre append, então
nenhuma gravação reescreve o que já está lá e o arquivo aguenta o bot morrer no
meio sem corromper o histórico.

Não confundir com `memoria.json`, que guarda outra coisa: as contrapartes que a
pessoa já disse conhecer. Aquilo é o que a Regis aprendeu. Isto é o que foi dito.
"""

import html
import json
import os
import re
import threading
import time

AQUI = os.path.dirname(os.path.abspath(__file__))

# No VPS isso mora no mesmo volume da memória, para sobreviver a deploy.
_MEMORIA = os.environ.get("REGIS_MEMORIA") or os.path.join(AQUI, "memoria.json")
ARQUIVO = os.environ.get("REGIS_CONVERSAS") or os.path.join(
    os.path.dirname(_MEMORIA) or AQUI, "conversas.jsonl")

# Quantas mensagens de histórico a Regis leva para o modelo. 20 é mais ou menos
# dez idas e voltas, o suficiente para ela acompanhar um assunto que muda de
# rumo no meio sem perder o começo. Dá para mexer sem tocar no código, pela
# variável REGIS_HISTORICO, que está no docker-compose.
LIMITE = int(os.environ.get("REGIS_HISTORICO", "20") or 20)

# Corta fala muito longa antes de mandar para o modelo. O registro guarda
# inteiro, só o histórico é que anda enxuto.
MAX_CARACTERES = 1500

_trava = threading.Lock()
_recentes = {}


# ---------------------------------------------------------------------------
# Limpeza
# ---------------------------------------------------------------------------

_TAG = re.compile(r"<[^>]+>")


def sem_html(texto):
    """
    Tira a marcação das mensagens do bot.

    O bot fala em HTML porque o Telegram pede, mas nem o registro nem o modelo
    querem ver <b> no meio da frase.
    """
    limpo = _TAG.sub("", str(texto or ""))
    return html.unescape(limpo).strip()


# ---------------------------------------------------------------------------
# Escrever
# ---------------------------------------------------------------------------

def anotar(chat, papel, texto, via="", nome="", extra=None):
    """
    Grava uma mensagem e guarda ela na memória recente.

    `papel` é "pessoa" ou "regis". `via` diz de onde a resposta saiu
    (comando, determinístico ou ia), que é justamente o que interessa na
    análise: quanto do produto o código resolve sozinho.
    """
    limpo = sem_html(texto)
    if not limpo:
        return

    linha = {
        "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "chat": str(chat),
        "papel": papel,
        "texto": limpo,
    }
    if nome:
        linha["nome"] = nome
    if via:
        linha["via"] = via
    if extra:
        linha.update(extra)

    with _trava:
        _guardar_na_memoria(str(chat), papel, limpo)
        try:
            with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
                arquivo.write(json.dumps(linha, ensure_ascii=False) + "\n")
        except Exception as erro:
            # Registro nunca derruba conversa. Se não deu para gravar, a Regis
            # continua respondendo e o problema aparece no log.
            print("[regis] não consegui registrar a conversa: %s" % erro)


def _guardar_na_memoria(chat, papel, texto):
    fila = _recentes.setdefault(chat, [])
    fila.append({"papel": papel, "texto": texto})
    # Guarda folga em relação ao limite, porque a fusão de falas seguidas
    # encolhe a lista depois.
    del fila[: max(0, len(fila) - LIMITE * 3)]


def esquecer(chat):
    """
    Apaga a memória recente de um chat.

    O arquivo não perde nada, ele ganha uma marca de recomeço. Assim a análise
    continua com a conversa inteira, e o `hidratar` da próxima subida sabe que
    dali para trás não conta mais como contexto. Sem essa marca, o /esquecer
    era desfeito pelo primeiro restart do bot.
    """
    with _trava:
        _recentes.pop(str(chat), None)
        try:
            with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
                arquivo.write(json.dumps({
                    "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "chat": str(chat),
                    "papel": "marca",
                    "texto": "recomeço",
                }, ensure_ascii=False) + "\n")
        except Exception as erro:
            print("[regis] não consegui marcar o recomeço: %s" % erro)


# ---------------------------------------------------------------------------
# Ler
# ---------------------------------------------------------------------------

def conversa(chat, limite=None):
    """
    Devolve o histórico no formato que a API espera.

    Funde falas seguidas do mesmo lado numa mensagem só (o bot manda três
    balões, para o modelo é um turno), garante que começa na pessoa e devolve
    no máximo `limite` mensagens.
    """
    limite = limite or LIMITE
    with _trava:
        bruto = list(_recentes.get(str(chat), []))

    fundido = []
    for item in bruto:
        papel = "user" if item["papel"] == "pessoa" else "assistant"
        texto = item["texto"][:MAX_CARACTERES]
        if fundido and fundido[-1]["role"] == papel:
            fundido[-1]["content"] += "\n\n" + texto
        else:
            fundido.append({"role": papel, "content": texto})

    # A conversa tem que abrir com a pessoa falando.
    while fundido and fundido[0]["role"] != "user":
        fundido.pop(0)

    if len(fundido) > limite:
        fundido = fundido[-limite:]
        while fundido and fundido[0]["role"] != "user":
            fundido.pop(0)

    return fundido


def hidratar():
    """
    Relê o arquivo na subida do bot, para a Regis não perder o fio depois de
    um deploy. Só a cauda importa, então lê tudo e fica com o fim.
    """
    if not os.path.exists(ARQUIVO):
        return 0
    lidas = 0
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                try:
                    item = json.loads(linha)
                except Exception:
                    continue
                if not item.get("texto") or not item.get("chat"):
                    continue
                if item.get("papel") == "marca":
                    # /esquecer: daqui para trás não é mais contexto.
                    _recentes.pop(str(item["chat"]), None)
                    continue
                _guardar_na_memoria(str(item["chat"]), item.get("papel", "pessoa"), item["texto"])
                lidas += 1
    except Exception as erro:
        print("[regis] não consegui reler o registro: %s" % erro)
    return lidas


def resumo():
    """Números do registro, para o log da subida e para conferir rápido."""
    total = 0
    chats = set()
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if not linha.strip():
                    continue
                total += 1
                try:
                    chats.add(json.loads(linha).get("chat"))
                except Exception:
                    pass
    except Exception:
        pass
    return {"mensagens": total, "conversas": len(chats), "arquivo": ARQUIVO}
