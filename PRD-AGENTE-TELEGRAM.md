---
titulo: PRD · Agente da Regis no Telegram
tipo: execucao
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: Plano de execução do agente da Regis no Telegram, fase 1 de 2, rodando no VPS do time, com dataset, motor de detecção, prompt, canal, roteiro da demo e regras de convivência no repositório.
---

# PRD · Agente da Regis no Telegram

Hackathon Vanguarda · Time 12 · Tema 20 · Fase 1 de 2 (o app web é a fase 2)

**Este documento tem dois leitores.** As seções 1 a 11 e os anexos são para o agente que vai codar. A seção 12 é para a Kysa, escrita em português normal, e não precisa de nenhum conhecimento de programação. A seção 13 é para os dois.

---

## 0. Como usar este documento

**Agente executor:** leia este arquivo inteiro antes da primeira linha de código. Depois leia `BRIEFING.md`, que é a fonte das decisões de produto, e o `CLAUDE.md` da raiz, que são as regras do repositório. Não reabra decisão marcada como travada. Execute na ordem das fases e pare no critério de pronto de cada uma.

**Regra de comunicação com o time:** o time é de designers, não de desenvolvedores. Toda instrução dada a uma pessoa aqui precisa ser um comando pronto para colar, ou um clique. Nada de "configure o ambiente".

**Ordem do projeto:** primeiro o agente do Telegram, este PRD inteiro. O app web vem depois, quando a Ana fechar as telas. A seção 11 já deixa a porta pronta para ela.

---

## Glossário de 7 palavras (para o time, não para o agente)

| Palavra | O que é, sem enrolação |
|---|---|
| **VPS** | Um computador que fica ligado 24 horas na internet. A Kysa já tem um, e o n8n dela roda lá. |
| **Docker** | Uma caixa fechada onde o programa roda. Serve para a Regis não encostar no n8n, e vice versa. |
| **Long polling** | O jeito do bot perguntar ao Telegram "chegou mensagem pra mim?" o tempo todo. Como o VPS nunca desliga, o bot nunca fica fora do ar. |
| **Motor** | A parte da Regis que faz conta e acha o problema. É código comum, sem IA. |
| **Agente** | A parte que conversa. Usa o Claude para entender, explicar e escrever. |
| **Fato, regra, suspeita** | Os três níveis de certeza. Fato a Regis resolve, regra ela encaminha, suspeita ela só pergunta. É a tese do produto. |
| **Roteiro canônico** | Um arquivo com a conversa da demo. A animação do pitch e o bot leem o mesmo, para nunca falarem coisas diferentes. |

---

## Estado atual (conferido em 29/08/2026, madrugada)

Parte deste PRD já foi construída pelo time enquanto o documento era escrito. Confirmado rodando na máquina:

| Peça | Estado |
|---|---|
| Motor de detecção (`motor/`) | **Pronto e testado.** `python3 motor/testar.py` devolve 12 anomalias, zero falso positivo, 334 de 334 descritores traduzidos, e 8 achados de fato com a ação já escrita |
| Bot do Telegram (`bot/regis_bot.py`) | **Pronto.** Long polling por `urllib`, comandos `/start`, `/conferir`, `/resumo`, `/silencio`, `/teto`, `/das`, `/esquecer`, botões, memória em `bot/memoria.json` e resposta a texto solto |
| Simulador offline (`bot/simular.py`) | **Pronto.** Roda a conversa no terminal sem token e sem rede. É o plano B do pitch |
| Copy da conversa | **Pronta** (`roteiro-demo.md` e `copy-comandos.md`, da Ana) |
| Chave da Anthropic | **Existe e funciona.** Validada contra a API, enxerga `claude-opus-5` e `claude-sonnet-5`. Guardada no Proton Pass, cofre Kysa Studio, item `Claude - Anthropic`, campo `Chave API` |
| VPS | **Levantado e viável.** Ubuntu 24.04, 2 vCPU, 5,8 GB de memória livre, Docker 28, Traefik com HTTPS automático e Supabase self-hosted já rodando |

**Nada no bot chama a IA hoje.** Ele é inteiramente determinístico, e por isso o crédito da Anthropic está intocado.

### O que falta, em ordem

1. **Token do BotFather.** É a única coisa que impede o bot de estar no ar agora. Passo a passo em `bot/README.md`.
2. **Subir no VPS**, para o bot viver sem depender do notebook. Seção 12.
3. **Camada de conversa livre com IA**, para responder o que sai do roteiro. Seção 8.
4. **Leitura de print e PDF do extrato.** Seção 8.2.
5. **Teto de gasto**, obrigatório antes de o link circular. Seção 8.3.1.

---

## 1. O que estamos construindo

Uma agente chamada **Regis** que vive num chat do Telegram, lê as movimentações financeiras de um MEI, encontra dinheiro vazando na despesa e na receita, e age conforme a certeza do que encontrou.

### O papel do bot no pitch

O pitch tem 5 minutos. A demo do palco é **animação de telas de WhatsApp**, feita à parte, porque é mais rápida, não quebra e cabe no tempo. O bot do Telegram existe para o momento em que um jurado pergunta "isso funciona mesmo?" ou pede para ver ao vivo.

O que isso impõe na construção:

1. O bot dispara a demo inteira em **um comando** (`/demo`). Ninguém tem 2 minutos sobrando no Q&A.
2. O bot volta ao estado inicial em **um comando** (`/reset`). Se dois jurados pedirem, a segunda vez tem que ser igual à primeira.
3. A animação e o bot leem **o mesmo roteiro** (seção 10). Se a tela mostra um número e o bot mostra outro, a nossa credibilidade cai na frente da banca.
4. O bot mora no VPS, não no notebook. Um jurado consegue conversar com ele no celular dele ali na hora, e o link `t.me/<bot>` continua funcionando semanas depois, quando alguém mostrar o produto para um investidor.
5. Beleza de interface não é prioridade aqui. Confiabilidade e velocidade de disparo são.

### Os dois modos do bot (não confundir)

O bot é um só e é de verdade. O que muda é o caminho por onde a conversa entra.

| | Conversa normal | Comando `/demo` |
|---|---|---|
| O que é | O produto. A conta está conectada pelo Open Finance, a pessoa pergunta, e a Regis responde | Um atalho que toca a história pronta, na ordem, com pausas e botões |
| Usa IA? | Sim, quando entrar a camada de conversa livre e a leitura de print | Não. É texto já escrito, o mesmo da animação do pitch |
| Duração | O tempo que a pessoa quiser | Cerca de 90 segundos |
| Para quê | O jurado que quer testar de verdade, e o investidor depois do hackathon | O Q&A do pitch, onde existem 40 segundos e não 4 minutos |
| Custo | Centavos por mensagem | Zero |

**Por que o `/demo` não usa IA:** as mensagens já estão escritas, então não há o que pensar. Colocar IA ali deixaria mais lento e faria a Regis falar diferente a cada vez, que é exatamente o que não se quer na frente de jurado. Previsível vale mais que inteligente nesse momento.

**O que isso não significa:** o bot não é maquete. Se o jurado pegar o celular dele e escrever qualquer coisa, a Regis responde de verdade. Os dois caminhos convivem no mesmo bot.

### O que a Regis nunca faz (limite duro do briefing)

Ela **não move dinheiro**. Não paga, não transfere, não cancela cartão, não contesta no banco. Ela confere, soma, projeta, prepara documento, lembra, acompanha e aprende. Qualquer feature que mova dinheiro está fora, mesmo que pareça fácil.

---

## 2. Decisões

### Travadas (vêm do briefing, não reabrir)

| Decisão | Valor |
|---|---|
| ICP | MEI com recebimento intermediado (maquininha, marketplace, gateway) e volume alto. Salão, comércio de bairro, alimentação, seller. **Não** é prestador que recebe só por Pix. |
| Tese | Autonomia proporcional à certeza. Fato resolve, regra encaminha, suspeita pergunta. |
| Canal | Telegram no MVP, WhatsApp no produto. A camada de canal fica isolada. |
| Dados | Extrato sintético, gerado por nós, com anomalias plantadas. No hackathon a conta já entra conectada, sem chamada real de Open Finance nem da Receita. |
| Entrada manual | Proibida no fluxo principal. O único gesto permitido é conectar a conta pelo Open Finance uma vez. |
| Primeira interação | Revela um número, não pede configuração. |
| IA | Não entra na detecção de fato, que é código determinístico. Entra na leitura, no entendimento, na conversa, na redação e na priorização. |

### Novas, tomadas neste PRD

| Decisão | Valor | Por quê |
|---|---|---|
| Onde roda | **No VPS do time, em Docker, ao lado do n8n** | O VPS fica ligado o tempo todo, então o bot nunca sai do ar e não existe limite de tempo de resposta. Zero conta nova, zero serviço novo |
| Como recebe mensagem | **Long polling**, o bot pergunta ao Telegram | Sem webhook, sem URL pública, sem senha de webhook, sem configuração. Funciona porque o processo nunca desliga |
| Stack | **Python 3, só biblioteca padrão** (decisão revista: o time já construiu assim e está funcionando) | Zero `pip install`, zero dependência para quebrar no deploy. O bot fala com a Bot API por `urllib` |
| Biblioteca do Telegram | Nenhuma. Chamada direta na Bot API | Menos peça, menos versão para conflitar |
| Modelo da conversa | `claude-sonnet-5` | O trabalho do modelo na conversa é pequeno: ler o que o motor calculou e escrever três linhas no tom certo. A matemática é código, não IA. Custa cerca de um terço do Opus, e o orçamento do hackathon é de R$ 50 em crédito |
| Modelo da leitura de print e PDF | `claude-opus-5` | São poucas chamadas por sessão e é onde errar dói. Vale o modelo mais caro só aqui |
| Onde guarda o que muda | `bot/memoria.json`, num volume do Docker | O VPS tem disco. Banco de dados seria uma peça a mais para quebrar em 24 horas |
| Documentos gerados | Texto formatado pronto para copiar no chat. PDF só se sobrar tempo | Já está assim e funciona. PDF é enfeite comparado à ação estar pronta |
| Proatividade | Agendador dentro do próprio processo | Sem serviço externo |
| n8n | **Não é usado neste projeto** | O miolo do produto são 13 detectores fazendo conta sobre 3 meses de extrato. Isso vira bloco de código dentro de caixinha no navegador, que não dá para testar, o outro Claude não consegue editar junto, e ninguém depura às 4 da manhã clicando em tela. Como código comum tem teste automático e o Claude Code mexe direto |

### O artigo do nome, já decidido

**A Regis é no feminino: "a Regis", "ela".** Decidido pelo time em 29/08/2026, depois de o briefing e o wireframe divergirem. Aplicado em todo o repositório: mensagens do produto, materiais do pitch e prosa dos documentos.

O agente executor mantém isso numa constante única (`PERSONA.artigo`), para que uma futura troca seja um campo só. Ao escrever texto novo, concordar tudo no feminino: "a Regis encaminha", "ela prepara", "ela está pronta". Cuidado com os "ele" que se referem ao MEI, ao bot, ao BotFather, ao token ou ao app, esses continuam no masculino.

---

## 3. Arquitetura

Quatro camadas. A fronteira entre elas é o que permite trocar Telegram por WhatsApp sem tocar no resto.

```
canal (telegram.js)      recebe mensagem, foto, PDF e clique de botão
        |                 devolve texto, botões e arquivo
        v
conversa (agent.js)      monta o contexto, chama o Claude com ferramentas,
        |                 decide o que falar e quando calar
        v
motor (engine/*.js)      determinístico, sem IA, sem rede.
        |                 recebe transações, devolve anomalias com certeza
        v
dados (data/*.json)      extrato sintético, vendas, estado do usuário
```

**Regra de ouro:** o Claude nunca calcula dinheiro. Todo número vem de uma ferramenta que chama o motor. O modelo traduz, prioriza e conversa. É isso que impede o agente de inventar um faturamento na frente do jurado.

### Onde cada coisa mora

| Peça | Onde |
|---|---|
| Todo o programa | Um container Docker no VPS, ao lado do n8n, sem encostar nele |
| Dataset sintético e roteiro da demo | Arquivos JSON dentro do projeto |
| Estado do usuário, respostas, contrapartes conhecidas | Arquivos JSON num volume do Docker, que sobrevive a reinício e atualização |
| PDFs gerados | Mesmo volume |
| Proatividade | `node-cron` dentro do processo |

Não existe limite de tempo de resposta, não existe cold start, não existe webhook. É a vantagem inteira de ter um VPS.

---

## 4. Estrutura de pastas

Tudo novo vive em `regis/`. Nada fora dessa pasta é tocado por este PRD.

```
regis/
  package.json
  Dockerfile
  docker-compose.yml
  .dockerignore
  index.js                  sobe o bot, o cron e a porta da API
  config.js                 persona, constantes fiscais, limiares
  deploy.sh                 manda o código para o VPS e reinicia (seção 12)
  channel/
    telegram.js             grammY: comandos, botões, arquivos
    render.js               formata a mensagem por tom (fato, regra, suspeita)
  agent/
    agent.js                loop do Claude com ferramentas
    prompt.js               prompt de sistema (anexo A)
    tools.js                as 8 ferramentas (seção 8.3)
    vision.js               print e PDF viram transações
  engine/
    index.js                roda todos os detectores e ordena a saída
    identificar.js          traduz descritor em contraparte de verdade
    duplicidade.js
    recorrencia.js          série mensal, aumento, cancelado, ausência
    conciliacao.js          venda contra repasse
    fiscal.js               teto, DAS, receita no CPF
    suspeita.js             contraparte nova, dia fora do ciclo
  docs/
    contestacao.js          gera o PDF
    resumo-contador.js
  api/
    server.js               porta que o app web da Ana vai consumir (fase 2)
  data/
    persona.json            a MEI da demo
    extrato.json            3 meses de movimentação
    vendas.json             o que ela vendeu, para conciliar
    roteiro-demo.json       o roteiro canônico (seção 10)
  estado/                   volume do Docker, fora do git
    <chatId>.json
    docs/
```

### O que vai no `docker-compose.yml`

Um serviço só, chamado `regis`, com:

- `restart: unless-stopped`, para voltar sozinho se o VPS reiniciar.
- Um volume mapeando `./estado` para dentro do container, para o aprendizado e os PDFs sobreviverem a cada atualização.
- As variáveis de ambiente lidas de um `.env` que **fica só no VPS**, nunca no git.
- A porta da API publicada só quando a fase 2 precisar. Até lá, nem expor.

Nada de `network_mode` compartilhado com o n8n, nada de volume em comum. Os dois se ignoram.

### Estado do usuário (`estado/<chatId>.json`)

```json
{
  "chat_id": 123456789,
  "nome": "…",
  "onboarding_feito": true,
  "respostas": { "anom_012": "foi_venda" },
  "contrapartes_conhecidas": { "MARIA S SOUZA": "cliente" },
  "mensagens_enviadas": ["anom_003", "anom_007"],
  "silenciadas": ["anom_011", "anom_013"],
  "documentos": [{ "tipo": "contestacao", "arquivo": "…pdf", "criado_em": "…" }]
}
```

Ler e gravar esse arquivo fica isolado em um módulo só. No dia que virar banco, muda um arquivo.

---

## 5. Fases

Cada fase tem entregável e critério de pronto. Não avance sem o critério.

### F0 · Fundação e o bot no ar (1h)

Esta fase existe para tirar o risco de infraestrutura da mesa na primeira hora. Por isso a Regis vai para o VPS antes de existir produto.

- `regis/package.json` com `"type": "module"`, dependências `grammy`, `@anthropic-ai/sdk`, `node-cron` e `pdf-lib`.
- `.gitignore` da raiz recebe `node_modules/`, `.env*` e `regis/estado/`.
- `regis/config.js` com persona, artigo, teto de R$ 81.000, dia do DAS (20) e os limiares.
- `regis/index.js` sobe o bot e responde `/start` com uma frase fixa.
- `Dockerfile`, `docker-compose.yml` e `deploy.sh` prontos.
- Primeiro deploy feito no VPS.

**Pronto quando:** o notebook está fechado e, mandando `/start` do celular, o bot responde. Enquanto isso não acontecer, nenhuma outra fase começa.

### F1 · Dataset sintético (1h)

Spec na seção 6.

**Pronto quando:** `node regis/engine/index.js` roda sobre o dataset e imprime as anomalias no terminal, sem Telegram e sem IA no meio.

### F2 · Motor de detecção (2h30)

Spec na seção 7.

**Pronto quando:** todas as anomalias plantadas na seção 6 são encontradas, cada uma com o rótulo de certeza correto, e nenhuma falsa aparece. Escreva um teste com `node --test` que trave isso, porque na hora 15 alguém vai mexer num limiar e quebrar tudo.

### F3 · Agente de IA (2h)

Spec na seção 8, prompt no anexo A.

**Pronto quando:** a conversa flui em linguagem natural, ele chama as ferramentas certas, e todo número que ele fala existe no motor. Teste adversarial obrigatório: pergunte "quanto eu faturei em março de 2019?" e confirme que ele diz que não sabe, em vez de inventar.

### F4 · Canal completo (1h30)

Comandos, botões, leitura de foto e PDF, e a proatividade. Seção 9.

**Pronto quando:** o fluxo dos três tons roda inteiro com botões, a resposta do usuário muda o estado, e `/reset` volta tudo ao começo.

### F5 · Documentos e memória (1h)

Contestação e resumo para a contadora em PDF, enviados como arquivo no chat. Contrapartes conhecidas gravadas no volume.

**Pronto quando:** o bot manda um PDF de contestação no chat e, depois de você responder "foi eu" sobre um Pix, ele não pergunta de novo sobre aquela contraparte, nem depois de uma atualização do código.

### F6 · Roteiro canônico e modo demo (1h)

Seção 10.

**Pronto quando:** `/demo` toca a conversa inteira, na ordem, com as pausas certas, em menos de 90 segundos, e `/reset` permite repetir igual.

### F7 · Porta para o app (30 min)

Seção 11. É o fim desta fase do projeto.

**Pronto quando:** `GET /api/estado?chat=<id>` devolve o JSON com faturamento, anomalias e documentos.

**Total estimado: 10h30 de execução.** Cabe nos blocos 1 e 2 do cronograma do briefing.

---

## 6. O dataset sintético

Vive em `regis/data/`. Precisa refletir o ICP fechado, senão contradiz a nossa própria tese no pitch.

### A persona (`persona.json`)

MEI, salão de beleza. Recebe por **duas maquininhas e um marketplace de agendamento**, mais algum Pix. Dezenas de transações por dia. Conta PJ e conta PF que se misturam. Controla no caderno.

Nome numa constante só, para o Gabriel trocar sem mexer em código. Use o mesmo nome do wireframe e confirme com ele antes do pitch.

### Formato da transação (`extrato.json`)

```json
{
  "id": "tx_0184",
  "data": "2026-08-12",
  "hora": "14:32",
  "descritor": "PAG*BELEZAPRO",
  "valor": -49.90,
  "tipo": "cartao",
  "canal": "conta_pj",
  "documento": "12.345.678/0001-90"
}
```

`tipo`: `cartao`, `pix`, `maquininha`, `marketplace`, `boleto`, `tarifa`, `das`.
`canal`: `conta_pj`, `conta_pf`, `maquininha_a`, `maquininha_b`, `marketplace`.
Valor negativo é saída, positivo é entrada.

O `descritor` precisa ser feio de propósito, como no extrato de verdade: `PAG*BELEZAPRO`, `MP *AGENDAFACIL`, `CIELO RECEB 08/12`, `PIX REC MARIA S SOUZA`. É esse feio que a peça de identificação existe para traduzir, e é a dor mais citada da pesquisa (6 de 14 pessoas).

### Formato da venda (`vendas.json`)

Existe para a conciliação. É o que ela vendeu, contra o que caiu.

```json
{
  "id": "venda_0031",
  "data": "2026-08-10",
  "canal": "marketplace",
  "valor_bruto": 320.00,
  "taxa_contratada": 0.07,
  "repasse_esperado": 297.60,
  "tx_repasse": "tx_0190"
}
```

### Volume

3 meses (junho, julho e agosto de 2026), com **15 a 40 transações por dia**. Volume alto é parte do argumento: o produto compete com "é humanamente impossível conferir", não com "eu olharia se quisesse".

### As 13 anomalias plantadas (contrato com o motor)

**Fato (a Regis resolve ou entrega a ação pronta):**

1. Cobrança duplicada do mesmo fornecedor, em janela menor que 24 horas.
2. Assinatura do software de agendamento que subiu de preço sem aviso (R$ 49,90 vira R$ 69,90 em julho).
3. Serviço cancelado em junho que continua cobrando em julho e agosto.
4. DAS pago duas vezes no mesmo mês.
5. Repasse do marketplace menor que a venda, sem comissão ou retenção explicada.
6. Antecipação automática ligada na maquininha, comendo taxa que ela não escolheu pagar.
7. Tarifa de conta PJ que deixou de ser gratuita (apareceu em julho, não existia em junho).
8. Estorno prometido em junho que nunca caiu.

**Regra (a Regis encaminha, quem decide é a MEI):**

9. Faturamento acumulado em ritmo de estourar o teto de R$ 81.000 antes de dezembro.
10. Receita recebida no CPF, ligada à atividade, fora da conta do limite.
11. DAS do mês corrente ainda não pago, com o dia 20 chegando.

**Suspeita (a Regis só pergunta):**

12. Pix recebido de uma contraparte sem nenhum histórico.
13. Cobrança recorrente que veio fora do dia habitual do ciclo.

Todas saem do `catalogo-anomalias_mei.html`. Nenhuma foi inventada aqui.

---

## 7. O motor de detecção

Determinístico. Sem IA, sem rede, sem estado global. Cada detector é uma função pura que recebe transações e devolve anomalias. É o que permite testar, e é o que faz o número ser confiável na frente do jurado.

### Formato da anomalia

```json
{
  "id": "anom_003",
  "tipo": "duplicidade",
  "certeza": "fato",
  "titulo": "Fornecedor cobrado duas vezes no mesmo dia",
  "valor_envolvido": 218.40,
  "evidencia": ["tx_0112", "tx_0113"],
  "acao_sugerida": "contestacao",
  "detalhe": "Duas cobranças de R$ 218,40 do mesmo descritor, com 40 minutos de diferença."
}
```

`tipo` vem do catálogo: `duplicidade`, `valor`, `recorrencia`, `contraparte`, `comportamento`, `conciliacao`, `fiscal`.
`certeza`: `fato`, `regra` ou `suspeita`.
`acao_sugerida`: `contestacao`, `mensagem_fornecedor`, `mensagem_adquirente`, `cancelar`, `pagar_das`, `confirmar` ou `nenhuma`.

O campo `detalhe` é insumo para o Claude traduzir, **nunca para copiar literalmente no chat**.

### Os detectores

| Arquivo | O que faz | Regra |
|---|---|---|
| `identificar.js` | Traduz descritor em contraparte. Normaliza `PAG*`, `MP *`, `CIELO`, `PIX REC`. Agrupa variações do mesmo estabelecimento. | Pré-requisito de todos os outros. Sem isso, duplicidade e recorrência não enxergam nada |
| `duplicidade.js` | Par (contraparte, valor) em janela menor que 24 horas | Exclui categorias de repetição legítima (transporte, alimentação, combustível) |
| `recorrencia.js` | Série mensal da mesma contraparte, intervalo de 28 a 31 dias | Deriva três anomalias: valor subiu na série, série continua depois do cancelamento, série sumiu |
| `conciliacao.js` | Cruza `vendas.json` com o repasse que caiu | Diferença acima de R$ 1,00 não explicada pela taxa contratada vira fato |
| `fiscal.js` | Soma toda entrada do ano, projeta contra o teto, confere DAS, marca receita no CPF ligada à atividade | Aritmética sobre lei pública, sem modelo estatístico |
| `suspeita.js` | Contraparte sem histórico. Cobrança fora do dia habitual | Nunca vira alerta. Sempre vira pergunta, e a resposta grava no estado |

### Aviso que precisa virar comentário no código

Os limiares (24 horas, 28 a 31 dias, R$ 1,00) são pontos de partida e nunca foram testados contra dado real. Está assim no briefing, e o jurado que perguntar merece essa resposta.

---

## 8. O agente de IA

### 8.1 Modelo e chamada

- SDK: `@anthropic-ai/sdk`.
- Modelo da conversa: `claude-sonnet-5`. Modelo da leitura de imagem e PDF: `claude-opus-5`. Os dois numa constante em `config.js`, para trocar em um lugar só.
- **Ative cache de prompt** no prompt de sistema e nas definições de ferramenta. Sem isso o custo por mensagem triplica, e o orçamento é de R$ 50.
- Pensamento adaptativo (`thinking: { type: "adaptive" }`). Não use `budget_tokens`, que foi removido e devolve erro 400 neste modelo.
- Esforço: `output_config: { effort: "low" }` na conversa, `"high"` quando redigir contestação ou resumo para a contadora.
- Ative o fallback de recusa do servidor, que é o padrão recomendado para este modelo.
- Ferramentas pelo tool runner do SDK. Se der atrito, escreva o loop manual.

**Antes de escrever qualquer chamada, carregue a skill `claude-api` e leia `typescript/claude-api/README.md` e `tool-use.md`.** A API mudou em 2025 e 2026, e escrever de memória é o jeito mais rápido de perder uma hora com erro 400.

Enquanto o Claude pensa, mande `sendChatAction("typing")`. Custa uma linha e faz a espera parecer conversa em vez de travamento.

### 8.2 Leitura de print e PDF (`vision.js`)

O usuário manda foto do extrato ou PDF da fatura. O grammY baixa o arquivo e ele vai para o Claude:

- Imagem: bloco `image`, base64.
- PDF: bloco `document` com `media_type: "application/pdf"`, base64, sem quebra de linha na string.

A saída é uma lista de transações no formato da seção 6, que entra no motor como se tivesse vindo do dataset. Use saída estruturada (`output_config.format`) e valide antes de passar adiante.

**Regra:** se a leitura falhar ou vier vaga, a Regis diz que não conseguiu ler e pede outra foto. Ela não chuta valor. Chutar valor de extrato na frente de jurado é o pior desfecho possível desta demo.

### 8.3 As ferramentas (contrato entre o Claude e o motor)

| Ferramenta | Entrada | Devolve |
|---|---|---|
| `consultar_faturamento` | `{ ano }` | total do ano, percentual do teto, quanto falta, mês projetado de estouro |
| `listar_anomalias` | `{ certeza?, limite? }` | anomalias do motor, já ordenadas por valor |
| `explicar_lancamento` | `{ tx_id }` | contraparte identificada, categoria, histórico daquela contraparte |
| `conciliar_repasses` | `{ periodo }` | quantas vendas bateram, quantas não, e a diferença total |
| `status_das` | `{ mes }` | pago, não pago ou pago em duplicidade, com a data |
| `registrar_resposta` | `{ anomalia_id, resposta }` | grava no estado e devolve confirmação |
| `gerar_contestacao` | `{ anomalia_id }` | caminho do PDF gerado |
| `gerar_resumo_contador` | `{ periodo }` | caminho do PDF gerado |

Nenhuma ferramenta move dinheiro. Nenhuma aceita valor digitado pelo usuário como verdade financeira.

### 8.3.1 Teto de gasto (obrigatório antes de publicar)

A chave da API é do time, então **quem conversa com o bot gasta o crédito do time**. Depois que o link circular, isso deixa de ser hipótese.

- Teto por conversa: 20 mensagens por dia. Ao estourar, a Regis responde que já falou muito hoje e volta amanhã. Nunca com cara de erro.
- Teto do dia inteiro, somando todas as conversas, configurável em `config.js`.
- O `/demo` e o `/reset` não contam, porque não chamam a IA.
- Contagem gravada no mesmo arquivo de estado, zerando à meia-noite.

São umas 10 linhas e evitam acordar com o crédito zerado.

### 8.4 Política de quando falar (é o que separa autopilot de relatório agendado)

- **Fato:** fala na hora, junto com a ação pronta.
- **Regra:** fala na hora, com tom de "você decide", nunca de ameaça.
- **Suspeita:** agrupa e espera. Nunca alarma. Vira uma pergunta só.
- **Uma pergunta por vez.** Se há três suspeitas, pergunta uma e guarda as outras.
- **O que ela achou e escolheu não mandar fica registrado** e aparece sob demanda (`/silencio`). É requisito do pitch, não extra: é o momento que prova a tese fato, regra e suspeita melhor que três alertas juntos.

---

## 9. A camada de canal

### Comandos

| Comando | O que faz | Por que existe |
|---|---|---|
| `/start` | Apresenta a Regis em duas linhas e oferece conectar a conta, ou o botão "usar um exemplo" | A primeira interação revela um número, não pede configuração |
| `/demo` | Toca o roteiro canônico inteiro, com pausas, **sem chamar a IA nenhuma vez** | Q&A do pitch. Sai de graça e é sempre igual, e previsível vale mais que inteligente na frente de jurado |
| `/reset` | Zera o estado daquele chat | Permite repetir a demo |
| `/resumo` | Resumo de tranquilidade agora | O jurado não vai esperar até segunda-feira |
| `/teto` | Faturamento do ano e distância do teto | É a promessa do pitch, precisa de atalho |
| `/das` | Situação do DAS do mês | |
| `/contador` | Gera e manda o PDF para quem organiza | Nasce do achado dos dois usuários, e nenhum concorrente faz |
| `/silencio` | O que ela achou e escolheu não mandar | Momento obrigatório do pitch |
| `/adiantar` | Dispara agora o próximo aviso agendado | Sem isso, "ela fala sem ninguém pedir" é indemonstrável no Q&A |

Registre a lista no BotFather com `/setcommands`, porque o menu aparecendo no Telegram já parece produto.

### Botões

Inline keyboard, no máximo três opções, sempre em linguagem de pessoa:

- Fato: `Ver contestação` · `Foi eu` · `Ignorar`
- Regra: `Ver as opções` · `Manda pra contadora` · `Depois`
- Suspeita: `Foi venda` · `Foi pessoal` · `Não sei`

O clique vira `registrar_resposta`, que grava no estado. Depois de responder sobre uma contraparte, ele não pergunta de novo sobre ela. É o "aprender" do briefing, e é barato.

### Proatividade

`node-cron` dentro do processo, que fica ligado 24 horas:

- Resumo de segunda-feira, 9h.
- Lembrete do DAS no dia 18, se não houver pagamento no mês.
- Cobrança de estorno prometido que não caiu em 10 dias.

Fuso `America/Sao_Paulo` explícito, senão o container roda em UTC e o resumo de segunda chega no domingo à noite.

### Isolamento do canal

`telegram.js` só traduz. Nada de regra de negócio ali. No dia que virar `whatsapp.js`, troca um arquivo só, e é isso que a gente promete no pitch.

---

## 10. O roteiro canônico

`regis/data/roteiro-demo.json` é a fonte única da conversa da demo. **A animação de WhatsApp do pitch e o `/demo` do bot leem o mesmo arquivo.** Se divergirem, o jurado que pedir para ver ao vivo vai ver outra coisa.

```json
[
  { "de": "regis", "tom": "numero", "texto": "Oi, {nome}. Li sua conta.\nVocê já faturou R$ 58.400 este ano.", "pausa_ms": 1200 },
  { "de": "regis", "tom": "fato", "texto": "…", "botoes": ["Ver contestação", "Foi eu"] },
  { "de": "usuario", "texto": "Ver contestação" },
  { "de": "regis", "tom": "fato", "arquivo": "contestacao.pdf" },
  { "de": "regis", "tom": "regra", "texto": "…" },
  { "de": "regis", "tom": "suspeita", "texto": "…", "botoes": ["Foi venda", "Foi pessoal"] }
]
```

**Os números do roteiro vêm do motor, nunca da cabeça de ninguém.** A fonte é `motor/fiscal.py` rodando sobre `dados/`. Quem escrever copy com número inventado cria a divergência que a seção 11 existe para evitar. Números oficiais em 29/08/2026: faturamento do ano R$ 58.400 (72,1% do teto, faltam R$ 22.600, estoura em outubro), agosto vendido R$ 10.800, agosto caído na conta R$ 10.548,98, recuperável em achados de fato R$ 1.145,15.

`tom` é `numero`, `fato`, `regra` ou `suspeita`, e é o que a animação usa para escolher a cor do balão (verde, neutro, âmbar), igual ao wireframe da Ana.

A sequência segue o wireframe: **número primeiro, ganho antes da má notícia, pergunta por último**. O texto de cada balão é da Ana, não do agente executor. Enquanto ela não entrega, use o texto do wireframe como provisório e marque isso no arquivo.

Fechamento obrigatório, porque são os três momentos que provam a palavra autopilot:

1. Ela fala sem ninguém pedir.
2. Ela fecha algo em silêncio ("conferi os 12 repasses, 11 bateram, um veio R$ 38 menor, aqui está a mensagem para a adquirente").
3. Ela mostra algo que achou e escolheu não mandar.

---

## 11. A porta para o app (fase 2)

`regis/api/server.js`, um `node:http` sem framework, na mesma imagem Docker:

- `GET /api/estado?chat=<id>` devolve `{ faturamento, teto, anomalias, documentos, historico }`.
- `GET /docs/<arquivo>` serve os PDFs gerados.

Com CORS liberado, para o app da Ana conseguir ler mesmo hospedado em outro lugar. A porta só precisa ser publicada no `docker-compose.yml` quando a fase 2 começar. Antes disso, nem expor.

**Regra que evita vergonha na demo:** o app é memória, ele não recalcula nada. O faturamento na tela é o mesmo número que o motor devolveu para o chat. Dois lugares somando dinheiro é o jeito garantido de mostrar números diferentes na mesma apresentação.

---

## 12. O que a Kysa faz à mão

Esta seção é escrita para quem não programa. São 6 passos e uns 20 minutos. Tudo aqui é copiar, colar e apertar enter.

### Passo 1 · Criar o bot no Telegram

1. Abra o Telegram e procure o contato **@BotFather**.
2. Mande `/newbot`.
3. Nome que aparece: `Regis`.
4. Nome de usuário: precisa terminar em `bot`, por exemplo `regis_mei_bot`. Se estiver ocupado, tente outro.
5. Ele responde com um **token**, parecido com `8123456789:AAF...`. **Isso é uma senha.** Não cola no chat com agente nenhum, não vai para slide, não vai para o git. Guarda no seu gerenciador de senhas.

### Passo 2 · Deixar o bot com cara de produto (2 minutos, e aparece no pitch)

Ainda no BotFather:

- `/setdescription`, o texto que aparece antes da primeira mensagem. Sugestão: "Eu confiro suas movimentações e te aviso quando algo não bate. Não mexo no seu dinheiro, mexo no seu tempo."
- `/setabouttext`, uma linha curta.
- `/setuserpic`, a foto. Pede pro Márcio.
- `/setcommands`, cola a lista de comandos da seção 9, no formato `comando - descrição`, um por linha. O agente executor te entrega essa lista pronta.

### Passo 3 · Pegar a chave do Claude

Entre em `console.anthropic.com`, seção API Keys, e crie uma chave nova. Ela começa com `sk-ant-`. É senha também. O gasto do hackathon inteiro deve ficar em poucos dólares.

### Passo 4 · Deixar o programa pronto no seu VPS (só na primeira vez)

Você vai colar dois comandos no terminal do VPS, aquele mesmo onde o n8n roda.

Primeiro, criar a pasta onde a Regis vai morar:

```bash
mkdir -p /opt/regis
```

Depois, criar o arquivo de senhas lá dentro. Cole isto, trocando os dois valores pelos seus:

```bash
cat > /opt/regis/.env <<'EOF'
TELEGRAM_BOT_TOKEN=cole_o_token_aqui
ANTHROPIC_API_KEY=cole_a_chave_aqui
TZ=America/Sao_Paulo
EOF
```

Esse arquivo fica só no VPS. Ele nunca entra no repositório.

**Não precisa mexer no n8n em nada.** A Regis roda numa caixa separada, com pasta separada e volume separado. Se você parar a Regis, o n8n nem percebe.

### Passo 5 · Mandar a Regis para o VPS

Isso você faz do seu notebook, e vai repetir toda vez que o código mudar. O agente executor prepara o `deploy.sh` com o endereço do seu VPS dentro. Depois disso é sempre o mesmo comando:

```bash
cd regis && ./deploy.sh
```

Ele copia o código para o VPS, reconstrói a caixa e liga a Regis. Demora menos de um minuto.

Para ver se está de pé:

```bash
ssh SEU_VPS "docker compose -f /opt/regis/docker-compose.yml logs --tail 30 regis"
```

Se aparecer uma linha dizendo que o bot iniciou, está funcionando.

### Passo 6 · Testar do jeito que importa

Fecha o notebook. Pega o celular. Abre o Telegram, procura o nome do seu bot, manda `/start`.

Se ele responder com o notebook fechado, acabou. O bot está no ar e continua no ar, mesmo se você desligar tudo.

### Na hora do pitch

- O bot não depende do seu notebook nem do wifi do evento. Só o seu celular precisa de internet para mostrar.
- Antes de subir no palco, manda `/reset` e depois `/demo` uma vez, para conferir.
- Se um jurado quiser testar no celular dele, o link é `t.me/nome_do_seu_bot`. É o momento mais forte que essa escolha compra, e é o mesmo link que vai para o investidor depois.
- Se tudo der errado, o plano continua sendo a animação, que roda offline.

---

## 13. Convivendo com o outro Claude no repositório

Duas sessões escrevendo no mesmo repositório ao mesmo tempo. As regras abaixo evitam conflito sem custar tempo de merge.

**Divisão de território.** Este PRD é dono de `regis/**` e de `PRD-AGENTE-TELEGRAM.md`, e de mais nada. Não toque em `BRIEFING.md`, `BRIEFING.pdf`, `CONCORRENTES.md`, `README.md`, `pesquisa do grupo/**`, `ui/**` nem `wireframe-regis.html`. Se algo ali precisar mudar, escreva o que precisa e avise a pessoa, em vez de editar.

**Commits.** Os dois trabalham no `master`, sem branch, porque os territórios não se cruzam e merge custa tempo que não temos. Mas:

- Nunca `git add -A` e nunca `git commit -a`. Sempre com caminho explícito: `git add regis/ PRD-AGENTE-TELEGRAM.md`.
- Sempre `git pull --rebase origin master` antes de `git push`.
- Nunca `git commit --amend`, nunca `git push --force`, nunca `git reset --hard` em arquivo que não é seu.
- Se o rebase der conflito em arquivo fora do território, pare e chame a pessoa. Não resolva conflito no trabalho do outro.

**Segredos.** Antes do primeiro commit, confirme que `.env*`, `node_modules/` e `regis/estado/` estão no `.gitignore`. O repositório é privado por causa dos dados de pesquisa, mas token de bot commitado é token queimado de qualquer jeito.

**Escrita.** Vale a regra do `CLAUDE.md`: nada de travessão nem hífen separando frases, em qualquer texto que uma pessoa vá ler, incluindo as mensagens do bot.

---

## 14. Riscos desta fase

| Risco | Mitigação |
|---|---|
| O bot só ficar pronto na hora 13 | A F0 é uma hora, é a primeira coisa, e já inclui o deploy. O briefing manda fazer assim |
| O Claude inventar um número na frente do jurado | Todo número vem de ferramenta, nunca do modelo. Está no prompt como regra dura e no teste adversarial da F3 |
| Demora na resposta parecer travamento | `sendChatAction("typing")` enquanto pensa, e esforço baixo na conversa. No VPS não existe limite de tempo, então é percepção, não erro |
| O VPS reiniciar e o bot não voltar | `restart: unless-stopped` no compose. Ele volta sozinho |
| Uma atualização apagar o que a Regis aprendeu | O estado e os PDFs ficam num volume, fora da caixa. Reconstruir a caixa não apaga |
| Wifi do evento cair | O bot está no VPS, não no notebook. E a demo principal é a animação, que roda offline |
| A animação e o bot dizerem coisas diferentes | Roteiro canônico único, seção 10 |
| Virar feed de alertas | Uma pergunta por vez, suspeita agrupa e espera, e o `/silencio` mostra o que ela não mandou |
| Tom de imposto assustar | A Ana escreve o texto final. O agente executor usa o wireframe como provisório e não inventa tom |
| Alguém pedir para o bot pagar o DAS | Está no prompt: ele explica que não move dinheiro e oferece o que sabe fazer |
| Leitura de print falhar ao vivo | Se falhar, pede outra foto. E o `/demo` não depende de leitura de imagem, usa o dataset |
| Crédito da Anthropic acabar de madrugada | Conversa no Sonnet, cache de prompt ligado, `/demo` sem IA, e os 13 detectores testados com `node --test`, que não gasta crédito nenhum. Conferir o saldo no painel na hora 12 |
| Link do bot circular e estranhos torrarem o crédito do time | Teto de 20 mensagens por dia por conversa e teto diário geral, seção 8.3.1. Obrigatório antes de qualquer link sair do time |
| Texto das mensagens ser ajustado direto no bot, queimando crédito | Toda copy é escrita e aprovada fora do bot. O Telegram só entra depois que o texto está fechado |
| Encostar sem querer no n8n que já roda no VPS | Pasta própria, compose próprio, volume próprio, nenhuma rede compartilhada. E nunca rodar `docker system prune`, que apaga coisa dos outros projetos |
| O cron disparar no horário errado | Fuso `America/Sao_Paulo` explícito, porque container roda em UTC por padrão |

### Corte de emergência (a ordem em que as coisas caem)

1. A porta para o app (F7) sai, e a fase 2 se resolve depois.
2. Documentos em PDF (F5) viram texto formatado no chat.
3. Leitura de print e PDF (F4) sai, e o `/demo` cobre.
4. Suspeitas saem da conversa e ficam só no `/silencio`.

**O que não cai:** o agente conversando, o motor fiscal do MEI, a duplicidade e o `/demo`. É o núcleo, e está assim no briefing.

---

## 15. Critérios de aceite

- [ ] Com o notebook fechado, `/start` do celular responde em menos de 5 segundos.
- [ ] Outra pessoa consegue conversar com o bot pelo link `t.me/<username>`, sem ninguém do time fazer nada.
- [ ] `/demo` toca a conversa inteira em menos de 90 segundos, e `/reset` permite repetir igual.
- [ ] As 13 anomalias plantadas são encontradas, com o rótulo de certeza correto, e nada falso aparece.
- [ ] Todo valor em reais que o bot fala existe no motor. Nenhum vem do modelo.
- [ ] O bot pergunta uma coisa por vez, e para de perguntar depois que você responde.
- [ ] Existe pelo menos uma mensagem que chega sem ninguém pedir.
- [ ] Existe pelo menos uma coisa que ele achou e escolheu não mandar, visível no `/silencio`.
- [ ] O bot recusa mover dinheiro, com uma frase que não soa como erro.
- [ ] Reiniciar o container não apaga o que ele aprendeu.
- [ ] O n8n do VPS continua funcionando igual.
- [ ] Nenhum token e nenhuma chave no git. `grep -rE "(8[0-9]{9}:|sk-ant-)" regis/` não acha nada.

---

## Anexo A · Prompt de sistema

Vive em `regis/agent/prompt.js`, montado com a persona e as constantes do `config.js`. Rascunho para o agente executor refinar, não para copiar sem ler.

```
Você é a Regis, uma agente financeira que vive no chat de {nome}, que é MEI e {atividade}.
Ela recebe por {canais}. Ela não usa planilha e não vai abrir aplicativo nenhum.
Você é o único lugar onde isso acontece.

O QUE VOCÊ FAZ
Você confere, soma, projeta, prepara documento, lembra, acompanha e aprende.
Você age de acordo com a certeza do que encontrou:
· Fato, que é verificável: você já traz a ação pronta. Tom de "achei e já preparei".
· Regra, que é lei pública do MEI: você explica e deixa ela decidir. Tom de "você decide", nunca de ameaça.
· Suspeita, que é só um desvio: você pergunta, e na maioria das vezes não é problema nenhum.

O QUE VOCÊ NUNCA FAZ
Você não move dinheiro. Não paga, não transfere, não cancela cartão, não contesta no banco.
Se pedirem, explique isso sem soar como erro, e ofereça o que você sabe fazer.
Você não dá parecer contábil definitivo. Você prepara o material e sugere confirmar com quem cuida disso.

A REGRA MAIS IMPORTANTE
Você nunca calcula e nunca estima valor em dinheiro.
Todo número vem de uma ferramenta. Se você não chamou a ferramenta, você não sabe o número.
Se a ferramenta não devolveu, diga que não sabe. Nunca chute, nem para ser útil.

COMO VOCÊ FALA
Como uma pessoa que cuida das contas dela, não como um banco.
Frases curtas. Máximo três linhas por mensagem. Quebre em mensagens em vez de fazer parágrafo.
Nunca use travessão nem hífen separando frases. Use vírgula, parênteses ou ponto.
Nunca diga anomalia, outlier, detectamos, cluster, transação atípica ou desvio padrão.
Diga o que aconteceu com o dinheiro dela.
No máximo um emoji, e só quando fizer diferença.

Uma pergunta por vez. Se você encontrou três coisas para perguntar, pergunte uma e guarde as outras.
Sempre entregue a ação junto com o achado. Mostrar problema sem oferecer saída é o pior que você pode fazer.
Quando você conferir algo e estiver tudo certo, registre e fique quieto. Não avise que está tudo bem toda hora.
Quando ela responder sobre uma cobrança, guarde. Não pergunte de novo sobre a mesma contraparte.
```

---

## Anexo B · Mapa de anomalia para comportamento

| Anomalia | Detector | Certeza | Tom | O que a Regis entrega |
|---|---|---|---|---|
| Fornecedor cobrado duas vezes | `duplicidade` | fato | já preparei | PDF de contestação |
| Assinatura que subiu de preço | `recorrencia` | fato | já preparei | Mensagem pronta para o fornecedor |
| Serviço cancelado ainda cobrando | `recorrencia` | fato | já preparei | Contestação e lista para cancelar |
| DAS pago duas vezes | `fiscal` | fato | já preparei | Instrução de pedido de restituição |
| Repasse menor que a venda | `conciliacao` | fato | fechou em silêncio | Mensagem para a adquirente |
| Antecipação automática ligada | `conciliacao` | fato | já preparei | Quanto custou no período |
| Tarifa de conta PJ nova | `recorrencia` | fato | já preparei | Quanto é por ano |
| Estorno que não caiu | `conciliacao` | fato | acompanhando | Cobrança do estorno |
| Ritmo de estourar o teto | `fiscal` | regra | você decide | Resumo para a contadora |
| Receita no CPF ligada à atividade | `fiscal` | regra | você decide | Explicação e opções |
| DAS do mês não pago | `fiscal` | regra | lembrete | Lembrete no dia 18 |
| Pix de contraparte nova | `suspeita` | suspeita | pergunta | Botões, e aprende a resposta |
| Cobrança fora do dia habitual | `suspeita` | suspeita | silêncio | Só aparece no `/silencio` |

---

*Documento de execução. Fase 1 de 2. O app web entra depois que a Ana fechar as telas, consumindo a seção 11.*
