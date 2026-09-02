---
titulo: QR codes da Regis
tipo: referencia
status: vigente
atualizado: 2026-08-30
autor: Time 12 · Hackathon Vanguarda
resumo: Os dois QR codes do projeto, para que serve cada versão e como regerar se um link mudar.
---

# QR codes

| Arquivo | Para onde leva | Para que serve |
|---|---|---|
| `telegram.*` | https://t.me/ChamaARegisBot | Cai direto na conversa com a Regis |
| `site.*` | https://regis.ia.br | A raiz, que leva ao app e pede login |
| `jurados.*` | https://regis.ia.br/jurados | **O do pitch.** Explica os comandos e tem o botão do Telegram, sem login |

Cada um tem quatro versões:

| Versão | Onde usar |
|---|---|
| `nome.svg` | **impressão e slide.** Vetor, aumenta sem borrar |
| `nome.png` | WhatsApp, e-mail, qualquer lugar que não aceite SVG |
| `nome-escuro.svg` | telão de fundo escuro, e dentro do produto |
| `nome-escuro.png` | o mesmo, em imagem |

## Na hora de usar

**Prefira os claros** (preto no branco) para qualquer coisa que alguém vá apontar a câmera. É a combinação que a câmera lê mais rápido, inclusive com pouca luz e em papel amassado.

Os escuros (verde no preto) são bonitos no telão e combinam com as telas, mas têm a polaridade invertida, ou seja, módulo claro sobre fundo escuro. Testamos: o código está correto (decodifica perfeitamente quando a imagem é invertida, e o contraste é de 8,3 para 1), mas nem todo leitor aceita polaridade invertida. A câmera nativa do iPhone e do Android costuma aceitar, leitores mais simples não. **Se o QR for a única forma de a pessoa entrar, use o claro.**

**Tamanho mínimo:** 3 cm impresso, ou 250 pixels na tela. Menor que isso a câmera sofre.

**Deixe margem branca em volta**, pelo menos a largura de quatro quadradinhos. Os arquivos já vêm com essa margem, então não recorte.

Os dois foram gerados com correção de erro alta, então continuam legíveis mesmo sujos, dobrados ou com um logo pequeno no centro.

## Regerar

Se algum link mudar:

```bash
python3 -m pip install --user segno    # só na primeira vez
python3 idv/qr/gerar.py
```

Os links ficam no topo do `gerar.py`, na lista `LINKS`.
