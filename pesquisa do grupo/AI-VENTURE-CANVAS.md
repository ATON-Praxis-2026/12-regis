---
titulo: AI Venture Canvas
tipo: template
status: preenchido
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: Canvas respondido com base no BRIEFING.md e na pesquisa da pasta, para a Regis (Financial Anomaly Autopilot).
---

# AI VENTURE CANVAS

> Do problema real ao autopilot: um sistema que recebe um input, executa o trabalho e entrega um output verificável.

**Equipe:** 12
**Tema:** 20, Financial Anomaly Autopilot (produto: Regis)
**Data:** 29/08/2026

---

## 1. PROBLEMA REAL

- Qual trabalho ou processo está sendo resolvido?
- Quem sofre com esse problema?
- Com que frequência ele acontece?
- Por que é caro, lento, repetitivo ou problemático hoje?

<!-- resposta -->

O trabalho é somar quanto o negócio faturou no ano e comparar com o teto legal do MEI (R$ 81.000, congelado desde 2018), além de achar cobrança duplicada, assinatura fantasma e repasse de maquininha ou marketplace menor do que a venda.

Quem sofre é o MEI com recebimento intermediado (maquininha, marketplace ou gateway) e volume alto de transações: comércio de bairro, alimentação, salão, seller. Não o prestador de serviço que recebe só por Pix, esse perfil não tem onde a maior parte das anomalias acontecer.

Acontece todos os dias. Dezenas de transações entram por canais diferentes (Pix pessoal, Pix da conta PJ, maquininha, marketplace, dinheiro em espécie) e nunca aparecem juntas num único extrato.

É caro e lento porque o Estado já cruza esses dados e o empreendedor não. Os desenquadramentos por excesso de faturamento saltaram 30 vezes de 2023 para 2024, passando de 570 mil MEIs, por causa do cruzamento automático de Pix e cartão pela Receita. Somar é estruturalmente difícil, não é preguiça: o dinheiro entra por quatro portas, se mistura com a conta pessoal (61% dos MEIs), a maquininha deposita líquido enquanto o teto conta bruto, o controle é caderno ou planilha na maioria dos casos, e o resultado só aparece um ano depois, na declaração de maio.

---

## 2. COMO É RESOLVIDO HOJE

- Quem executa esse trabalho atualmente?
- Funcionário interno, BPO, consultoria, escritório, agência ou prestador?
- Como é o processo atual?
- Quais são seus principais custos e fricções?

<!-- resposta -->

Hoje é a própria pessoa, de cabeça, em planilha ou em caderno (30% planilha, 25% caderno, 20% app ou sistema, 13% contador, 10% nenhum controle). A parte fiscal costuma ser terceirizada: nas conversas com MEIs, metade da amostra não faz essa parte sozinha, é a esposa, uma contadora da família, ou a própria pessoa que "teve que aprender sozinha" sob pressão.

O processo é manual e reativo. Confere o extrato quando lembra, não quando deveria. Descobre o faturamento real só na declaração anual, em maio do ano seguinte, ou quando a Receita avisa. Quem tem contador manda print ou PDF pelo WhatsApp, sem sistema entre os dois.

Os custos e fricções: reconciliar transação a transação é julgamento manual repetido centenas de vezes por mês, nenhuma ferramenta cruza venda com repasse de adquirente, e o aviso chega tarde demais (um caso real da pesquisa teve dez guias de DAS atrasadas ao mesmo tempo). O concorrente real não é outro aplicativo, é o hábito do caderno e da memória.

---

## 3. GRAU DE AUTONOMIA

- O que antes era feito por uma pessoa e agora o sistema executa sozinho?
- Onde ainda existe intervenção humana?
- Quais decisões o agente toma sozinho e quais precisam de aprovação?

<!-- resposta -->

Antes era a pessoa quem somava tudo que entrou, conferia se o repasse batia com a venda, lembrava do vencimento do DAS, identificava se uma cobrança repetida era erro, e escrevia (ou deixava de escrever) a contestação. Agora o sistema faz isso sozinho: soma e projeta o faturamento contra o teto, concilia venda com repasse, verifica se o DAS do mês foi pago, identifica quem é o estabelecimento por trás de um descritor obscuro, detecta duplicidade (mesma contraparte e valor em janela menor que 24h) e recorrência (série mensal de 28 a 31 dias), e redige a ação pronta.

A intervenção humana continua onde envolve mover dinheiro ou confirmar intenção: enviar a contestação, cancelar a assinatura, pagar o DAS, e confirmar se um Pix sem histórico foi a própria pessoa. A Regis nunca move dinheiro, esse é o limite duro do produto.

A autonomia varia com a certeza da anomalia. Fato (duplicata exata, estorno que não caiu) ela resolve sozinha e entrega a ação pronta, só falta copiar e enviar. Regra (o teto se aproximando, um DAS não pago) ela encaminha e explica as opções, mas quem decide é a pessoa. Suspeita (desvio estatístico, contraparte sem histórico) ela só pergunta, e a resposta ensina o sistema para a próxima vez.

---

## 4. AUTOPILOT / SOLUÇÃO

- Qual é o INPUT recebido pelo sistema?
- Que trabalho o sistema executa?
- Qual OUTPUT concreto ele entrega?
- O objetivo é EXECUTAR o serviço, e não apenas acompanhar o usuário.

<!-- resposta -->

INPUT: a movimentação da conta, lida por conexão de Open Finance, somente leitura, autorizada pela pessoa no próprio banco. Um print, um PDF de fatura, um comprovante ou a notificação do banco ainda podem entrar pelo chat (Telegram no MVP, WhatsApp no produto final), mas são gesto pontual, não a forma de alimentar o sistema.

Trabalho executado: um motor de identificação traduz o descritor cru do extrato em quem é o estabelecimento de verdade (nome de fachada, categoria, CNPJ), um motor de duplicidade e recorrência aplica regras determinísticas sobre janela de tempo e valor, um motor fiscal MEI soma tudo que entrou e projeta contra o teto de R$ 81.000, verifica o DAS do mês e cruza venda com repasse, e um agente de IA lê o que chega pela conversa, explica cobranças não reconhecidas, redige a contestação ou a mensagem para o fornecedor, e decide o que mandar e quando.

OUTPUT concreto: mensagens nos três tons de certeza (fato já resolvido com ação pronta para copiar e enviar, regra explicada com as opções, suspeita perguntada em uma frase), o número de faturamento acumulado contra o teto, um resumo periódico de tranquilidade, e um relatório para o contador.

O sistema não se limita a mostrar um dashboard que a pessoa precisa abrir e interpretar. Ele executa a conferência, a soma e a redação da ação, e é ele quem inicia a conversa.

---

## 5. MVP / PROVA

- Qual é o menor fluxo ponta a ponta que precisa funcionar até o piloto?
- O que será demonstrado ao vivo?
- Que evidência prova que o serviço realmente executa o trabalho?

<!-- resposta -->

O menor fluxo ponta a ponta: o MEI conecta a conta pelo Open Finance, o motor roda sobre o dataset sintético, a Regis responde nos três tons, aceita a resposta do usuário ("foi eu sim") e redige uma contestação pronta para enviar.

O que será demonstrado ao vivo: a persona Angela Nogueira, cabeleireira MEI que aluga uma cadeira num salão (maquininha e marketplace, Pix como minoria), com a conta já conectada pelo Open Finance. Como no hackathon os dados são simulados, a demo parte da conta conectada, não de uma conexão ao vivo. A Regis abre com o número (faturou R$ 58.400, faltam R$ 22.600 para o teto, projeção de estouro em 24/10), depois um ganho (duplicata resolvida), depois uma regra (o teto se aproximando), depois uma suspeita (um Pix estranho que ela confirma que foi ela), e fecha no resumo de tranquilidade. Dois momentos provam a palavra autopilot: ela fala sem ninguém pedir (lembrete do DAS por cron) e ela fecha algo em silêncio (repasse do marketplace conferido, sem alarme).

A evidência: R$ 1.145,15 recuperáveis em 8 anomalias de fato plantadas no dataset de 367 transações em 3 meses, mais 2 de regra (teto, taxa efetiva acima do contratado) e 2 de suspeita, com gabarito verificável em `dados/anomalias-esperadas.json`. O gabarito também traz 6 falsos positivos que a Regis escolhe não mostrar, prova de que ela distingue sinal de ruído em vez de alertar sobre tudo.

---

## 6. VALOR ECONÔMICO

- Por que alguém pagaria por isso?
- Economia de dinheiro? Economia de tempo?
- Reduz risco? Aumenta receita?
- Qual é a evidência ou hipótese de valor mais importante?

<!-- resposta -->

Alguém pagaria para não ser pego de surpresa por um desenquadramento retroativo (o ano inteiro recalculado como microempresa, com multa de 0,33% ao dia e juros Selic sobre impostos que ninguém sabia que devia), e para recuperar dinheiro parado em cobrança duplicada, assinatura fantasma e repasse menor do que a venda.

Economia de dinheiro e de tempo, as duas coisas. No dataset da demo, R$ 1.145,15 recuperáveis em um trimestre. E o tempo até perceber cai de meses (3 a 5 sem ritual de conferência, às vezes nunca) para imediato, porque quem tem aviso externo (push, mensagem do banco) percebe na hora, e a Regis vira esse aviso externo para tudo, não só para fraude.

Reduz risco de forma clara: risco fiscal (a dívida do MEI cai no CPF, pode travar auxílio doença, salário maternidade e aposentadoria) e risco de perder o regime do Simples.

A hipótese de valor mais importante: custo do vazamento é igual ao valor da cobrança multiplicado pelos meses até alguém perceber. A Regis não muda o valor da cobrança, muda o tempo até a pessoa saber, e é aí que mora o ganho.

---

## 7. MERCADO / OPORTUNIDADE

- Existe dinheiro sendo gasto hoje para resolver esse problema?
- Quais empresas ou serviços já atuam nessa categoria?
- Qual evidência rápida mostra que existe uma oportunidade relevante?
- Não é necessário TAM, SAM e SOM detalhado durante o hackathon.

<!-- resposta -->

Sim, existe dinheiro sendo gasto hoje. Contabilidades digitais, apps de gestão para MEI e a própria infraestrutura de leitura via Open Finance já têm preço de mercado (o Banco MCP cobra R$ 19,90 por conta conectada, revendendo a Pluggy no varejo). O FinAI cobra R$ 29,90 por mês por registro manual.

Empresas já atuando: ALL (Open Finance com mais de 120 instituições e um milhão de transações classificadas por IA, mas é assistivo, "é você quem abre"), FinAI (100% manual, não conecta banco), Mobills, Cora, InfinitePay e Asaas (a própria conta PJ resolve pagamento, não apuração), Meu MEI Digital do governo (avisa prazo por calendário, não lê dado bancário), e os bancos, únicos que hoje procuram o usuário por conta própria, via push de compra.

Evidência rápida de oportunidade: 12,9 milhões de MEIs ativos, 78% de todas as empresas abertas em 2026. 570 mil desenquadramentos em 2024, 30 vezes mais que em 2023, atribuídos ao cruzamento automático de Pix e cartão pela Receita. 61% dos MEIs misturam conta pessoal e da empresa. E a linha divisória entre os concorrentes não é a inteligência artificial, todos já usam IA, é de onde vem o dado e se o produto fala sozinho ou espera ser aberto.

---

## 8. MODELO DE NEGÓCIO

- Quem paga, e paga pelo quê exatamente?
- Como podemos cobrar?
- Exemplos: assinatura, por execução, por volume, success fee, percentual do valor econômico gerado.

<!-- resposta -->

Não fechado no hackathon (fora do escopo explícito das 24h). A hipótese de trabalho: monetização direta ao MEI é difícil, porque o custo de infraestrutura por usuário já fica na faixa de R$ 40 a 60 por mês (2 a 3 contas a R$ 19,90 cada) e o mercado está num estágio de sofisticação baixo para vigilância de receita, ainda não formulou o problema como algo que se paga para resolver.

O caminho mais provável é distribuição via banco, adquirente ou contabilidade digital, que já têm o dado e a base de usuários, e para quem a Regis vira uma feature agregada, não um produto avulso.

Formas de cobrança possíveis para explorar depois do hackathon: por volume de contas conectadas (usando o custo de origem, R$ 19,90 por conta, como piso de referência), success fee sobre o valor recuperado (duplicatas e assinaturas fantasmas encontradas), ou embutida na oferta do parceiro de distribuição.

---

## 9. CLIENTE / COMPRADOR

- Quem usa a solução?
- Quem efetivamente paga por esse serviço?
- Que tipo de empresa ou profissional tem esse problema?

<!-- resposta -->

Quem usa: o MEI com recebimento intermediado (maquininha, marketplace ou gateway) e volume de transações alto o bastante para não caber na memória. Comércio de bairro, alimentação, salão, seller. Não o prestador de serviço que recebe só por Pix direto, esse perfil foi testado e refutado nas conversas de campo, porque sem intermediário metade do catálogo de anomalias não tem onde acontecer.

Quem paga, ainda não definido (ver bloco 8). Hipótese: não é o próprio MEI diretamente, é o parceiro de distribuição (banco, adquirente, contabilidade) que já tem a base.

Tipo de empresa ou profissional: negócios com múltiplos canais de recebimento e dezenas de transações por dia, tipicamente comércio físico com maquininha e presença em marketplace. E, achado importante da pesquisa, muitas vezes existem duas pessoas no fluxo, quem vende e quem organiza a parte fiscal (esposa, contadora da família), o que exige uma saída compartilhável, não só um usuário único.

---

## REGRA CENTRAL DO CANVAS

> Não construir apenas um copiloto ou chatbot que ajuda alguém a executar um serviço. A tese é um AUTOPILOT: um sistema que recebe um input, executa o trabalho e entrega um output verificável.

---

### Notas da transcrição

Alguns trechos do impresso ficaram parcialmente ilegíveis na foto e foram reconstruídos pelo contexto:

- Bloco 8, primeira pergunta: lida como "Quem paga, e paga pelo quê exatamente?"
- Bloco 8, terceira linha: a lista de exemplos de cobrança está no impresso, a redação exata de "percentual do valor econômico gerado" pode divergir.
- Os campos do cabeçalho (equipe, tema, data) estão em branco no impresso, com "Equipe 12" escrito à mão.

Conferir contra o canvas físico antes de usar como referência definitiva.
