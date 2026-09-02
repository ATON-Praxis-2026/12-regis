---
titulo: Regis · Financial Anomaly Autopilot
tipo: indice
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: Por onde começar no repositório, o que é a Regis em um parágrafo e como atualizar as respostas do forms.
---

# Regis · Financial Anomaly Autopilot

Hackathon Vanguarda · Time 12 · Tema 20 (Financeiro) · 29 e 30 de agosto de 2026

Regis é uma agente no chat (Telegram no MVP, WhatsApp no produto) que lê as movimentações financeiras de quem trabalha sozinho, encontra dinheiro vazando na despesa e na receita, e age de acordo com a certeza: resolve o que é fato, encaminha o que é regra, pergunta o que é suspeita.

A Regis não mexe no seu dinheiro. Ela mexe no seu tempo.

## Comece por aqui

- [BRIEFING.md](BRIEFING.md) · o briefing completo: desafio, time, síntese da pesquisa, decisões, solução, escopo de 24h, cronograma, pitch e riscos. Também em [PDF](BRIEFING.pdf).
- `pesquisa do grupo/` · toda a pesquisa (enquadramento, catálogo de anomalias, universo MEI, entrevistas, custo por conta, respostas do forms).

## As telas

Abra **[`ui/index.html`](ui/index.html)** no navegador e navegue por tudo de um lugar só. Não precisa instalar nada, tudo roda offline.

- `ui/regis-conversa.html` · a conversa no WhatsApp, animada em loop. É a tela da hero.
- `ui/regis-app.html` · o app de apoio, um arquivo só, responsivo: abas embaixo no celular, sidebar no computador.
- `ui/regis-telas.html` · as cinco telas anotadas, para discutir UX.
- `ui/_padrao-conversa-whatsapp.html` · o template. **Toda tela nova de conversa sai daqui.**

## Pesquisa com MEIs (forms)

Para atualizar as respostas: baixe o CSV do Google Forms, salve em `pesquisa do grupo/respostas-forms/` e rode

```
python3 "pesquisa do grupo/respostas-forms/gerar-markdown.py"
```

O CSV bruto fica fora do git (está no `.gitignore`). Só o markdown anonimizado é versionado.

## Sobre esta versão pública

Esta é a versão pública do repositório do hackathon, com o conteúdo congelado no último commit de domingo, 30 de agosto de 2026. Antes de publicar, o repositório passou por uma limpeza:

- Os 14 entrevistados da pesquisa aparecem como **E1** a **E14**. Os relatos, as citações e os números continuam íntegros, só a identificação saiu.
- Endereço do VPS, senha da demo, caminhos de cofre de senhas e e-mails de contato viraram marcadores de exemplo (`SEU_IP_DO_VPS`, `TROQUE_ESTA_SENHA`, `contato@exemplo.com.br`). Para rodar de verdade, preencha as variáveis de ambiente descritas em `bot/.env.exemplo` e em `deploy/README.md`.
- Os dados financeiros em `dados/` sempre foram sintéticos, gerados por `dados/gerar.py`. Nenhum extrato real entrou aqui.
- Angela é uma persona fictícia, criada para a demo.

Os nomes do time seguem nos créditos, por escolha nossa.

## Time

Kysa Robert (motor, agente, canal) · Ana Silveira (conversa e app) · Gabriel Hardt (narrativa e pitch) · Márcio Modonezi (marca e visual)
