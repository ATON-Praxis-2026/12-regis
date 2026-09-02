#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A conversa inteira da Regis, no terminal, sem token e sem rede.

Serve para duas coisas:

1. Ensaiar a demo quantas vezes quiser, sem depender do Telegram.
2. Ser o plano B se o wi-fi do evento cair na hora do pitch. O que aparece
   aqui é exatamente o que apareceria no chat, porque as mensagens saem das
   mesmas funções de `regis_bot.py`.

Rodar:

    python3 bot/simular.py              # com as pausas, do jeito da demo
    python3 bot/simular.py --rapido     # sem pausa, para conferir o texto
    python3 bot/simular.py --sem-cor    # sem cor, para colar em slide

A memória usada aqui é um arquivo separado (bot/memoria-simulacao.json),
zerado a cada execução. A simulação nunca mexe na memória do bot de verdade.
"""

import os
import re
import shutil
import sys
import textwrap
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import regis_bot as bot  # noqa: E402

MEMORIA_SIMULACAO = os.path.join(AQUI, "memoria-simulacao.json")

RAPIDO = "--rapido" in sys.argv or "-r" in sys.argv
COR = "--sem-cor" not in sys.argv and sys.stdout.isatty()

LARGURA = min(shutil.get_terminal_size((80, 24)).columns, 78)

NEGRITO = "\033[1m" if COR else ""
FIM = "\033[0m" if COR else ""
CINZA = "\033[90m" if COR else ""
AZUL = "\033[36m" if COR else ""
VERDE = "\033[32m" if COR else ""


def dormir(segundos):
    if not RAPIDO:
        time.sleep(segundos)


def limpar_html(texto):
    texto = texto.replace("<pre>", "").replace("</pre>", "")
    texto = re.sub(r"<b>(.*?)</b>", NEGRITO + r"\1" + FIM, texto, flags=re.S)
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = texto.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return texto


def escrever_linhas(texto, prefixo="  "):
    largura = LARGURA - len(prefixo)
    for paragrafo in texto.split("\n"):
        if not paragrafo.strip():
            print(prefixo)
            continue
        for linha in textwrap.wrap(paragrafo, width=largura) or [""]:
            print(prefixo + linha)


def mostrar_digitando():
    if RAPIDO:
        return
    sys.stdout.write(CINZA + "  %s está digitando..." % bot.PERSONA["nome"] + FIM)
    sys.stdout.flush()
    time.sleep(0.7)
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()


def falar_regis(mensagem):
    mostrar_digitando()
    print(AZUL + "  " + bot.PERSONA["nome"] + FIM)
    escrever_linhas(limpar_html(mensagem["texto"]))
    for linha in mensagem.get("botoes") or []:
        rotulos = "   ".join("[ %s ]" % b["texto"] for b in linha)
        print(CINZA + "  " + rotulos + FIM)
    print()
    dormir(min(mensagem.get("pausa", 1.0), 2.0))


def falar_regis_varias(mensagens):
    for mensagem in mensagens:
        falar_regis(mensagem)


def falar_cleide(texto, clique=False):
    dormir(0.9)
    rotulo = "Angela toca no botão" if clique else "Angela"
    print(VERDE + "  " + rotulo + FIM)
    escrever_linhas(texto if not clique else "%s" % texto)
    print()
    dormir(0.5)


def titulo(texto):
    print()
    print(CINZA + "  " + "·" * (LARGURA - 2) + FIM)
    print(CINZA + "  " + texto + FIM)
    print(CINZA + "  " + "·" * (LARGURA - 2) + FIM)
    print()


def achar_fato_com_acao(resultado, preferido="AN-02"):
    fatos = bot.por_certeza(resultado, "fato")
    for achado in fatos:
        if achado.get("id") == preferido and achado.get("acao"):
            return achado
    for achado in fatos:
        if achado.get("acao"):
            return achado
    return fatos[0] if fatos else None


def primeira_suspeita(resultado, memoria):
    for achado in bot.por_certeza(resultado, "suspeita"):
        if not memoria.ja_respondeu(achado.get("id")) and not memoria.conhece(bot.contraparte_de(achado)):
            return achado
    return None


def main():
    if os.path.exists(MEMORIA_SIMULACAO):
        os.remove(MEMORIA_SIMULACAO)
    memoria = bot.Memoria(MEMORIA_SIMULACAO)
    resultado = bot.rodar_motor()

    print()
    print(NEGRITO + "  %s, simulação da conversa" % bot.PERSONA["nome"] + FIM)
    print(CINZA + "  Sem token e sem rede. Motor: %s. Dados sintéticos." % bot.FONTE_MOTOR + FIM)

    titulo("1. A primeira mensagem revela um número")
    falar_cleide("/start")
    falar_regis_varias(bot.roteiro_start(resultado))

    titulo("2. A conferência, ganho antes de má notícia")
    falar_cleide("Ver o que eu achei", clique=True)
    falar_regis_varias(bot.roteiro_conferir(resultado, memoria))

    achado = achar_fato_com_acao(resultado)
    if achado:
        titulo("3. O texto pronto, quem envia é ela")
        falar_cleide((achado.get("acao") or {}).get("titulo", "Ver o texto"), clique=True)
        falar_regis_varias(bot.roteiro_acao(achado))

    suspeita = primeira_suspeita(resultado, memoria)
    if suspeita:
        titulo("4. A pergunta, e a Regis aprendendo com a resposta")
        falar_cleide("Foi eu", clique=True)
        falar_regis_varias(bot.roteiro_foi_eu(suspeita, memoria))
        falar_regis_varias(bot.roteiro_proxima_pergunta(resultado, memoria))

    titulo("5. A Regis não pergunta de novo sobre quem a Angela já apresentou")
    falar_cleide("/conferir")
    conferencia = bot.roteiro_conferir(resultado, memoria)
    falar_regis_varias(conferencia[-2:])
    print(CINZA + "  (os achados de fato e de regra vieram iguais, "
                  "só a pergunta mudou)" + FIM)
    print()

    titulo("6. O que ela achou e escolheu não mandar")
    falar_cleide("o que você deixou passar?")
    falar_regis_varias(bot.roteiro_livre("o que você deixou passar?", resultado, memoria))

    titulo("7. O resumo para encaminhar para a contadora")
    falar_cleide("/resumo")
    falar_regis_varias(bot.roteiro_resumo(resultado))

    titulo("8. Conversa solta, sem menu de ajuda")
    for pergunta in ("quanto falta pro teto?", "paga isso pra mim"):
        falar_cleide(pergunta)
        falar_regis_varias(bot.roteiro_livre(pergunta, resultado, memoria))

    print(CINZA + "  Fim da simulação. Memória gravada em %s" % MEMORIA_SIMULACAO + FIM)
    print(CINZA + "  Conhecidos agora: %s" % (
        ", ".join(memoria.dados["contrapartes_conhecidas"]) or "ninguém") + FIM)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
