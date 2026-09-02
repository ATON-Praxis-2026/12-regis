#!/usr/bin/env python3
"""
Gera os QR codes da Regis.

    python3 idv/qr/gerar.py

Precisa da biblioteca segno:  python3 -m pip install --user segno

Sai um SVG (para imprimir e para slide, escala sem perder) e um PNG
(para mandar no WhatsApp e colar em qualquer lugar) de cada link.
"""
import os
import sys

try:
    import segno
except ImportError:
    sys.exit("falta a biblioteca: python3 -m pip install --user segno")

AQUI = os.path.dirname(os.path.abspath(__file__))

VERDE = "#00C46C"
PRETO = "#0B100D"

LINKS = [
    ("telegram", "https://t.me/ChamaARegisBot", "Falar com a Regis"),
    ("site", "https://regis.ia.br", "regis.ia.br"),
    # o do pitch: leva a pagina que explica os comandos e tem o botao do Telegram
    ("jurados", "https://regis.ia.br/jurados", "regis.ia.br/jurados"),
]


def gerar(nome, url, rotulo):
    # correção alta, para o QR continuar lendo mesmo sujo, dobrado ou com logo em cima
    qr = segno.make(url, error="h")

    # claro: preto no branco, é o que lê melhor em papel e em slide
    qr.save(os.path.join(AQUI, "%s.svg" % nome), scale=10, border=3,
            dark=PRETO, light="#FFFFFF")
    qr.save(os.path.join(AQUI, "%s.png" % nome), scale=14, border=3,
            dark=PRETO, light="#FFFFFF")

    # escuro: para telão e para as telas do produto
    qr.save(os.path.join(AQUI, "%s-escuro.svg" % nome), scale=10, border=3,
            dark=VERDE, light=PRETO)
    qr.save(os.path.join(AQUI, "%s-escuro.png" % nome), scale=14, border=3,
            dark=VERDE, light=PRETO)

    print("  %-9s %s" % (nome, url))
    print("            %s.svg, %s.png, %s-escuro.svg, %s-escuro.png"
          % (nome, nome, nome, nome))


def main():
    print("QR codes da Regis:")
    for nome, url, rotulo in LINKS:
        gerar(nome, url, rotulo)
    print()
    print("Os claros são para papel e slide. Os escuros são para telão e para o app.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
