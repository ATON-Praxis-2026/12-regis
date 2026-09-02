---
titulo: Guia do repositório para agentes
tipo: referencia
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: Onde está cada coisa do repositório, quais decisões não se reabrem e como regerar o PDF e as respostas do forms.
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este repositório

Projeto de hackathon de 24h (Vanguarda, 29 e 30 de agosto de 2026, Time 12, tema 20 "Financial Anomaly Autopilot"). O produto se chama **Regis** (de registro e gargalo).

Hoje o repositório é **só pesquisa e briefing**. Não há código de aplicação, build, testes ou dependências. Se for pedido para construir o produto, ler `BRIEFING.md` inteiro antes: ele contém as decisões já fechadas e o escopo, e vale mais que qualquer suposição sobre o que "faria sentido".

## Comandos

Regerar `pesquisa do grupo/respostas-forms.md` depois de baixar um CSV novo do Google Forms para `pesquisa do grupo/respostas-forms/`:

```bash
python3 "pesquisa do grupo/respostas-forms/gerar-markdown.py"
```

Regerar `BRIEFING.pdf` a partir de `BRIEFING.md` (não há pandoc nem wkhtmltopdf na máquina; a conversão é markdown para HTML por script próprio e depois Chrome headless):

```bash
python3 <script md2html>            # gera BRIEFING.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="$PWD/BRIEFING.pdf" "file://$PWD/BRIEFING.html"
rm BRIEFING.html
```

O script de conversão vive no scratchpad da sessão, não no repositório. Se precisar de novo, reescrever: ele trata tabelas, headings, listas, blockquote e negrito/itálico, e injeta um CSS de impressão A4.

## Onde está cada coisa da pesquisa

`pesquisa do grupo/` guarda documentos HTML autocontidos, um por frente. Cada um responde uma pergunta diferente, e a distinção importa quando surgir uma dúvida de produto:

| Documento | Responde |
|---|---|
| `enquadramento-problema.html` | Qual etapa do vazamento atacar (o ciclo de 6 etapas e os 4 enquadramentos) |
| `catalogo-anomalias.html` e `catalogo-anomalias_mei.html` | Que anomalias existem, classificadas por tipo e por **certeza** (fato, regra, suspeita) |
| `insights-mei.html` | Por que o ICP é MEI, números de mercado e hipóteses a validar |
| `posicionamento.html` | O que dizer: níveis de consciência, sofisticação e as três camadas de concorrentes |
| `custo-por-conta.html` | Quanto custa ler cada conta via Open Finance |
| `relatorio-pesquisa-14-conversas.html` | Entrevistas com 14 pessoas físicas |
| `respostas-forms.md` | Respostas do forms com MEIs, anonimizadas |

`BRIEFING.md` é a síntese de todos eles mais as decisões. Quando um documento novo entrar na pasta, ele precisa ser integrado ao briefing (nova subseção em "3. O que a pesquisa já nos disse") e o PDF regerado, senão o briefing sai de sincronia com a pesquisa.

## Decisões já travadas (não reabrir sem o time pedir)

- **ICP:** MEI. Resolve o impasse PF versus PJ porque a camada de regra é lei pública, sem configuração.
- **Tese do produto:** autonomia proporcional à certeza. Fato a Regis resolve, regra ela encaminha, suspeita ela pergunta.
- **Limite duro:** a Regis **não move dinheiro**. Não paga, não transfere, não cancela cartão, não contesta no banco. Ela confere, soma, projeta, prepara documento, lembra, acompanha e aprende. Qualquer feature que mova dinheiro está fora.
- **Canal:** o agente vive no chat. Telegram no MVP (API imediata), WhatsApp no produto. O app web é apoio e o usuário pode nunca abrir.
- **Zero entrada manual no fluxo principal.** O concorrente é o caderno, não outro app. Cadastro recorrente (digitar venda, categorizar) está proibido. Encaminhar o extrato uma vez é aceitável; alimentar sistema não é.
- **A primeira interação revela um número**, não pede configuração.
- **Promessa do pitch:** "Você sabe quanto já faturou este ano?" A palavra autopilot e a IA entram depois, explicando o mecanismo.

## Telas do pitch: use o padrão, não invente outro

Toda tela de conversa para a apresentação parte de **`ui/_padrao-conversa-whatsapp.html`**. O time aprovou esse padrão e ele não se reabre a cada tela nova. Copie o arquivo, troque só o que está entre `<!-- CONTEUDO -->` e `<!-- FIM CONTEUDO -->`.

O padrão é: um WhatsApp fiel (paleta oficial, doodles de fundo, rabicho na bolha, botões de resposta rápida do WhatsApp Business, gaveta de lista que sobe) com a conversa se montando sozinha em loop. A mecânica veio do site `frontseat.com.br`, que a usuária fez, e está documentada no topo do arquivo: multiplicador de 1.25 nos delays, "digitando" proporcional ao tamanho do texto, checks virando azul, `IntersectionObserver` com threshold 0.25, loop infinito e atalho para `prefers-reduced-motion`.

Regras do padrão que não se quebram:
- **Quem começa a conversa é sempre a Regis**, nunca a pessoa. É a tese do produto: um autopilot que espera ser aberto não é autopilot.
- **Ganho antes de má notícia.** Fato primeiro, regra depois, suspeita por último.
- **Uma pergunta por vez.**
- Níveis marcados por emoji, porque no WhatsApp real não dá para colorir bolha: ✅ fato, ⚠️ regra, ❓ suspeita.

Telas existentes: `ui/regis-conversa.html` (hero com a conversa), `ui/regis-app.html` (o app de apoio, um arquivo só e responsivo), `ui/regis-telas.html` (as cinco telas anotadas para discussão de UX).

## Dados sensíveis

- `relatorio-pesquisa-14-conversas.html` contém **nomes reais, bancos e valores** de participantes. O repositório é privado por causa dele. Não publicar, não colar em slide sem anonimizar, não subir para artifact ou serviço externo.
- O CSV bruto do forms fica fora do git (`.gitignore`). Só o markdown anonimizado (R1, R2...) é versionado. Ao gerar qualquer material derivado, manter a anonimização.

## Escrita dos documentos

Estes arquivos são lidos por pessoas (time, jurados). Vale a regra global do usuário: **nada de travessão nem hífen separando frases** em texto corrido, títulos ou copy. Usar vírgula, parênteses ou ponto final. A exceção é sintaxe técnica (nomes de arquivo em kebab-case, flags, CSS), onde o hífen é obrigatório.

Antes de commitar um markdown novo, conferir com `grep -c "—" arquivo.md` (o esperado é 0).
