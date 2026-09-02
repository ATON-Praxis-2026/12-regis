---
titulo: Copy dos comandos do bot da Regis
tipo: copy
status: vigente
atualizado: 2026-08-29
autor: Ana · Time 12
resumo: O texto de cada comando do bot (/start, /resumo, /teto, /das, /contador, /silencio, /reset), na voz do Anexo A e com os valores do dataset. Complementa o roteiro-demo.md, que cobre só o /demo.
---

# Copy dos comandos do bot

O `roteiro-demo.md` já cobre o `/demo`. Aqui está o texto dos comandos avulsos (seção 9 do PRD). Mesma voz do Anexo A: feminino, frases curtas, sem travessão, sem jargão, no máximo três linhas por mensagem, no máximo um emoji. Cada `-` é uma mensagem separada no chat. Os valores batem com `dados/anomalias-esperadas.json`.

Isto é copy, mora na raiz (território da Ana). Quem liga no bot (`bot/`, território da Kysa) é o lado dela.

## /start

Apresenta a Regis e conecta a conta. Não pede configuração.

- Oi! Eu sou a Regis. Eu leio o que entra e o que sai da sua conta, confiro tudo e só te chamo quando precisa de você.
- Conecte sua conta que eu somo tudo e te digo quanto você já faturou este ano. É você que autoriza, no seu banco.
- botões: `Conectar conta` · `Usar um exemplo`

> A conexão é via Open Finance, a Angela autoriza no próprio banco, nada de mandar arquivo. Se tocar em "Usar um exemplo", cai no `/demo` com o dataset. Só depois disso vem o número, nunca antes.

## /teto

Faturamento do ano e distância do teto. É a promessa do pitch.

- Você já faturou R$ 58.400 este ano.
- Faltam R$ 22.600 pro teto de R$ 81 mil. No seu ritmo, você chega por volta de outubro.
- botões: `Ver as opções` · `Manda pra contadora`

> Tom da decisão 3: "chega no teto", factual, sem "passa do teto" nem "muda seu regime".

## /das

Situação do DAS do mês, e o que eu achei nele.

- Seu DAS de agosto está pago. Caiu em 18/08 e baixou certo, não precisa fazer nada.
- Mas achei uma coisa: a competência de junho foi paga duas vezes, R$ 87,05. Já preparei o pedido de restituição.
- botões: `Ver o pedido` · `Depois`
- O de setembro vence dia 20. Eu te lembro dia 18, sem você precisar anotar.

> A duplicidade do DAS é a AN-06. O lembrete do dia 18 é a proatividade da seção 9.

## /resumo

Resumo de tranquilidade agora, sem esperar segunda.

- Tudo conferido por aqui.
- Achei R$ 93,90 que ficou pelo caminho, uma cobrança dobrada e um repasse curto, e já deixei as ações prontas.
- Seu faturamento do ano está em R$ 58.400 e o caixa está tranquilo.

> Os R$ 93,90 são a Netflix dobrada (R$ 55,90, AN-02) mais o repasse curto (R$ 38, AN-05).

## /contador

Gera e manda o resumo para quem organiza. Nenhum concorrente faz.

- Preparei um resumo do ano pra sua contadora: faturamento, distância do teto e o que está pendente.
- Já vem tudo somado, você não precisa fazer conta nenhuma. Mando pra ela agora?
- botões: `Mandar pra contadora` · `Baixar o PDF`

> Quem confirma o envio é a usuária, porque expor dado financeiro pra fora é decisão dela. Gera o `resumo-contadora.pdf`.

## /silencio

O que eu achei e escolhi não mandar. É o momento que prova a tese no pitch.

- Essa semana eu vi algumas coisas e escolhi não te mandar, porque nenhuma virava problema:
- um Pix de R$ 268 que caiu às 3h40 de domingo, mas de alguém que você já conhece.
- e umas saídas que parecem estranhas e são normais pro seu histórico: o aluguel, o pico de sábado, o DAS do mês.
- Nada virou alarme. Se quiser ver tudo, é só falar.

> O Pix de madrugada é a AN-12 (suspeita agrupada). As "normais" são os falsos positivos esperados do dataset. É o que separa autopilot de feed de alertas.

## /reset

Zera o estado daquele chat, para repetir a demo.

- Pronto, zerei tudo. Podemos começar de novo.
- Conecte sua conta, ou toca em usar um exemplo.

## Para quem vai integrar (Kysa)

- Copy na voz do Anexo A, feminino, sem travessão, valores do `dados/anomalias-esperadas.json`.
- Botões seguem a seção 9: fato (`Ver contestação` · `Foi eu` · `Ignorar`), regra (`Ver as opções` · `Manda pra contadora` · `Depois`), suspeita (`Foi venda` · `Foi pessoal` · `Não sei`). Os comandos usam variações em linguagem de pessoa.
- Se o nome da persona fechar como Angela, o `/start` e o `/contador` não citam nome, então não muda nada aqui.
- Se algum valor mudar no dataset, me avisa que eu ajusto.
