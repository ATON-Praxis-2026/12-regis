---
titulo: Roteiro de mensagens da Regis (demo)
tipo: copy
status: vigente
atualizado: 2026-08-29
autor: Ana · Time 12
resumo: A copy dos balões da demo, derivada das 5 decisões do wireframe e alinhada ao dataset da Kysa. Fonte única da conversa do pitch. Alimenta regis/data/roteiro-demo.json (seção 10 do PRD) e a animação de WhatsApp.
---

# Roteiro de mensagens da Regis

Este é o texto de cada balão da demo, na voz do Anexo A do PRD (frases curtas, sem travessão, sem jargão, no máximo três linhas). É a fonte única: a animação de WhatsApp e o `/demo` do bot leem a mesma coisa. Os valores estão alinhados ao gabarito em `dados/anomalias-esperadas.json`. O bloco JSON no fim vai para `regis/data/roteiro-demo.json`, que é território do PRD, então quem cola lá é o agente executor, não este arquivo.

**Persona:** Angela, cabeleireira MEI. Não é dona de salão, aluga uma cadeira no Studio Bella e atende a própria clientela. Recebe por duas maquininhas (crédito e débito) e um marketplace de agendamento (BelezaNet), com Pix minoritário. Faturou R$ 58.400 no ano (72% do teto). O nome Angela está alinhado com o dataset da Kysa.

## As 5 decisões do wireframe, viradas em fala

| Decisão travada | Onde aparece no roteiro |
|---|---|
| 1 · A abertura afirma o número | Beat 1: "Você já faturou R$ 58.400 este ano." Nenhuma pergunta antes. |
| 2 · Ganho antes do alerta | Beat 2 (recupera a duplicata) vem antes do Beat 3 (o teto). |
| 3 · Tom do teto neutro e factual | Beat 3: "chega no teto", "o imposto muda", fecha na contadora como ajuda. |
| 4 · O padrão define o tom | Beat 2 é fato (duplicata no mesmo dia). Beat 4 é suspeita (Pix novo, ela pergunta). |
| 5 · A Regis vigia o dinheiro | Beat 2 promete acompanhar. Fechamento 1 mostra o estorno caindo sozinho. |

## O roteiro, beat a beat

Legenda de tom: **número** (âncora), **fato** (verde, resolve), **regra** (neutro, encaminha), **suspeita** (âmbar, pergunta).

### Beat 1 · O número (decisão 1)

- **Regis** (número): Oi, Angela. Li sua conta.
- **Regis** (número): Você já faturou R$ 58.400 este ano.

> Afirma, não pergunta. O "Li sua conta" antes do número revela sem parecer vigilância.

### Beat 2 · O ganho (decisões 2, 4 e 5) · AN-02

- **Regis** (fato): Achei a Netflix cobrada duas vezes no mesmo dia 12, R$ 55,90 cada. É cobrança em duplicidade.
- **Regis** (fato): Já preparei a contestação pra você conferir. → botões: `Ver contestação` · `Foi eu` · `Ignorar`
- **Angela**: Ver contestação
- **Regis** (fato): [envia `contestacao.pdf`]
- **Regis** (fato): É só conferir e mandar pro seu cartão. Quando o estorno cair, eu te aviso.

> "No mesmo dia" é o que autoriza o tom fato (decisão 4). O último balão é o limite visível ("é só você mandar") mais a promessa de vigiar o dinheiro (decisão 5).

### Beat 3 · O teto (decisão 3) · AN-09

- **Regis** (regra): No seu ritmo, você chega no teto de R$ 81 mil por volta de outubro. Passando dele, o imposto muda, por isso vale saber antes.
- **Regis** (regra): Preparei um resumo pra sua contadora te ajudar a decidir. → botões: `Ver as opções` · `Manda pra contadora` · `Depois`
- **Angela**: Manda pra contadora
- **Regis** (regra): [envia `resumo-contadora.pdf`]
- **Regis** (regra): Mandei. Já vem tudo somado, você não precisou fazer conta.

> Tom factual, sem "muda seu regime". Quem aperta "Manda" é ela, porque expor dado pra fora é decisão dela.

### Beat 4 · A pergunta (decisão 4) · AN-11

- **Regis** (suspeita): Caiu um Pix de R$ 340 de um nome novo, a Maria Souza. Foi venda? → botões: `Foi venda` · `Foi pessoal` · `Não sei`
- **Angela**: Foi venda
- **Regis** (suspeita): Anotei, somei no seu faturamento do ano. Não te pergunto de novo sobre a Maria.

> Uma pergunta por vez. A resposta atualiza o número e ensina a Regis (não repete a contraparte).

## Os três fechamentos obrigatórios (a palavra autopilot)

Vêm da seção 10 do PRD. São o que separa autopilot de relatório agendado.

### Fechamento 1 · Ela fala sem ninguém pedir (fecha o loop da decisão 5)

- **Regis** (fato): Lembra da cobrança repetida? O estorno de R$ 55,90 caiu na sua conta. Fechei, sem você precisar cobrar.
- **Regis** (número): E toda segunda eu te mando o resumo, sem você pedir. Seu caixa está tranquilo.

### Fechamento 2 · Ela fecha algo em silêncio · AN-05

- **Regis** (fato): Conferi seus repasses do marketplace esta semana. Quase todos bateram.
- **Regis** (fato): Um veio R$ 38 menor que as vendas, sem comissão explicada. Já preparei a mensagem pra adquirente. → botões: `Ver mensagem` · `Ignorar`

### Fechamento 3 · Ela mostra o que achou e escolheu não mandar (`/silencio`) · AN-12

- **Regis** (suspeita): Essa semana teve uma coisa que eu não te mandei, porque não valia seu tempo.
- **Regis** (suspeita): Um Pix de R$ 268 caiu às 3h40 de um domingo, de alguém que você já conhece. Fora de hora, mas nada de errado. Fica registrado, se quiser ver é só pedir.

## Bloco pronto para `regis/data/roteiro-demo.json`

Formato da seção 10. O agente executor cola isto no arquivo do PRD. `pausa_ms` é sugestão de ritmo para a animação.

```json
[
  { "de": "regis", "tom": "numero", "texto": "Oi, Angela. Li sua conta.", "pausa_ms": 900 },
  { "de": "regis", "tom": "numero", "texto": "Você já faturou R$ 58.400 este ano.", "pausa_ms": 1400 },

  { "de": "regis", "tom": "fato", "texto": "Achei a Netflix cobrada duas vezes no mesmo dia 12, R$ 55,90 cada. É cobrança em duplicidade.", "pausa_ms": 1000 },
  { "de": "regis", "tom": "fato", "texto": "Já preparei a contestação pra você conferir.", "botoes": ["Ver contestação", "Foi eu", "Ignorar"] },
  { "de": "usuario", "texto": "Ver contestação" },
  { "de": "regis", "tom": "fato", "arquivo": "contestacao.pdf" },
  { "de": "regis", "tom": "fato", "texto": "É só conferir e mandar pro seu cartão. Quando o estorno cair, eu te aviso.", "pausa_ms": 1200 },

  { "de": "regis", "tom": "regra", "texto": "No seu ritmo, você chega no teto de R$ 81 mil por volta de outubro. Passando dele, o imposto muda, por isso vale saber antes.", "pausa_ms": 1000 },
  { "de": "regis", "tom": "regra", "texto": "Preparei um resumo pra sua contadora te ajudar a decidir.", "botoes": ["Ver as opções", "Manda pra contadora", "Depois"] },
  { "de": "usuario", "texto": "Manda pra contadora" },
  { "de": "regis", "tom": "regra", "arquivo": "resumo-contadora.pdf" },
  { "de": "regis", "tom": "regra", "texto": "Mandei. Já vem tudo somado, você não precisou fazer conta.", "pausa_ms": 1200 },

  { "de": "regis", "tom": "suspeita", "texto": "Caiu um Pix de R$ 340 de um nome novo, a Maria Souza. Foi venda?", "botoes": ["Foi venda", "Foi pessoal", "Não sei"] },
  { "de": "usuario", "texto": "Foi venda" },
  { "de": "regis", "tom": "suspeita", "texto": "Anotei, somei no seu faturamento do ano. Não te pergunto de novo sobre a Maria.", "pausa_ms": 1400 },

  { "de": "regis", "tom": "fato", "texto": "Lembra da cobrança repetida? O estorno de R$ 55,90 caiu na sua conta. Fechei, sem você precisar cobrar.", "pausa_ms": 1200 },
  { "de": "regis", "tom": "numero", "texto": "E toda segunda eu te mando o resumo, sem você pedir. Seu caixa está tranquilo.", "pausa_ms": 1400 },

  { "de": "regis", "tom": "fato", "texto": "Conferi seus repasses do marketplace esta semana. Quase todos bateram.", "pausa_ms": 900 },
  { "de": "regis", "tom": "fato", "texto": "Um veio R$ 38 menor que as vendas, sem comissão explicada. Já preparei a mensagem pra adquirente.", "botoes": ["Ver mensagem", "Ignorar"] },

  { "de": "regis", "tom": "suspeita", "texto": "Essa semana teve uma coisa que eu não te mandei, porque não valia seu tempo.", "pausa_ms": 900 },
  { "de": "regis", "tom": "suspeita", "texto": "Um Pix de R$ 268 caiu às 3h40 de um domingo, de alguém que você já conhece. Fora de hora, mas nada de errado. Fica registrado, se quiser ver é só pedir.", "pausa_ms": 1200 }
]
```

## Para quem vai integrar (Kysa)

- Este arquivo é copy, mora na raiz (território da Ana). O JSON acima é que vira `regis/data/roteiro-demo.json`.
- Valores alinhados ao `dados/anomalias-esperadas.json`: Netflix R$ 55,90 (AN-02), teto R$ 58.400 (AN-09), Pix da Maria R$ 340 (AN-11), repasse R$ 38 menor (AN-05, fechou em silêncio), Pix de R$ 268 às 3h40 (AN-12, só no `/silencio`).
- Dois PDFs são citados: `contestacao.pdf` e `resumo-contadora.pdf`.
- Nome da persona: **resolvido**, a Kysa regenerou o dataset com Angela.
- Copy do teto no app: **resolvido**, a Kysa aplicou a decisão 3 ("chega no teto") no app, hoje unificado em `ui/regis-app.html`.
