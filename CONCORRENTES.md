---
titulo: Concorrentes · de onde vem o dado
tipo: pesquisa
status: vigente
atualizado: 2026-08-30
autor: Time 12 · Hackathon Vanguarda
resumo: Quem já disputa a frase app de finanças com IA, de onde cada produto tira o dado, quais falam sozinhos e quais já movem dinheiro pelo WhatsApp.
---

# CONCORRENTES — de onde vem o dado

> Onze produtos que disputam a mesma frase, "app de finanças com IA", separados pelas duas
> perguntas que realmente os distinguem: **quem alimenta o sistema, ele fala sozinho, e ele mexe no dinheiro?**
>
> Levantado em 29/08/2026. **Jota e Magie acrescentados em 30/08/2026**, e eles mudam o quadro. Versão publicada: https://claude.ai/code/artifact/21f66939-eda8-452c-b377-3c76c82fdf84
> Ver também `DOSSIE.md` (dados) e `INSIGHTS.md` (conclusões).

---

## Quadro comparativo

### Origem do dado e postura

| Produto | De onde vem o dado | Fala sozinho? | Trabalho principal |
|---|---|---|---|
| **FinAI** | o usuário digita, fala ou fotografa | **Não** — só existe o que você contou | substituir a planilha |
| **ALL** (myall.com.br) | **Open Finance**, 120+ instituições | Parcial — mostra na tela; a assistente propõe e espera confirmação | orçamento pelo método Cerbasi |
| **Mobills** | "integração automática" *(mecanismo não confirmado)* | Não | controle de gastos e orçamento |
| **Organizze** | *não verificado* | Não | controle de gastos |
| **Cora / InfinitePay / Asaas** | é a própria conta — só vê o que passa nela | Não | conta, cobrança e nota fiscal |
| **Meu MEI Digital** (governo) | **não lê dado bancário** | Avisa prazo, por calendário | serviços e obrigações do MEI |
| **Bancos** (Nubank, Inter, C6, PicPay) | é o próprio banco — só o que é dele | **Sim** — push no momento da compra | extrato do próprio banco |
| **Jota** (jota.ai) | **Open Finance** + é a própria conta | **Sim, e por decisão de produto**, o Jota 2.0 é a virada de reativo para antecipatório | conta digital e fluxo de caixa por conversa |
| **Magie** (magie.com.br) | **Open Finance** + é a própria conta | Sim, banking conversacional | banco no WhatsApp, e infraestrutura whitelabel para terceiros |
| **Nossa ideia** | extrato e fatura reais, via Open Finance | **Sim — é a premissa** | achar e explicar o que não fecha |

### Alcance, público e preço

| Produto | Identifica cobrança desconhecida? | PF / PJ | Canal | Preço |
|---|---|---|---|---|
| **FinAI** | Não — é o usuário quem nomeia | ambos, do que foi digitado | app + WhatsApp | R$ 19,90 a R$ 29,90/mês |
| **ALL** | Classifica, mas para preencher orçamento | PF e PJ na mesma conta, separados | app + web | não publicado no site |
| **Mobills** | não anunciado | PF | app | freemium |
| **Organizze** | não anunciado | PF | app | pago |
| **Cora / InfinitePay / Asaas** | Não | PJ apenas | app | conta gratuita |
| **Meu MEI Digital** | Não | PJ (MEI) | app, login gov.br | gratuito |
| **Bancos** | Antifraude sim; identificação de estabelecimento não | ambos | app + push | gratuito |
| **Jota** | Categoriza sozinho; **nada de fiscal** | PF, PJ e **MEI** | **WhatsApp** + app | gratuito |
| **Magie** | Não anunciado; **nada de fiscal** | PF, expandindo para empresas | **WhatsApp** | gratuito |
| **Nossa ideia** | **É a razão de existir** | MEI multiporta | Telegram no MVP, WhatsApp no produto | a decidir |

---

## Leitura do quadro

### 1. A linha divisória não é a IA — todos usam IA

É **de onde vem o dado**. De um lado, quem depende do usuário registrar (FinAI). Do outro, quem lê a conta (ALL, PFMs, bancos).

**Quem depende do registro não consegue, por construção, encontrar aquilo que o usuário não sabe que existe.**

### 2. Ninguém, além do banco, procura o usuário

Todos os produtos independentes esperam que o usuário abra. O ALL diz isso literalmente na home: *"é isto que você abre todo dia"*.

A única coisa genuinamente proativa no quadro é o **push do próprio banco** — e ele só enxerga o próprio banco, e basicamente só dispara para suspeita de fraude.

**É esse o espaço.**

### 2b. Correção de 30/08: já tem quem procure o usuário, e tem dinheiro

O item 2 acima envelheceu em um dia. **O Jota 2.0, lançado em junho de 2026, é exatamente a passagem de um assistente que responde quando perguntado para um agente que se antecipa**, e veio acompanhado de uma Série A de R$ 150 milhões. Falar primeiro deixou de ser terreno vago.

O que sobra de espaço não é o canal nem a postura. É **o trabalho**. Nenhum dos dois faz apuração.

### 3. A parte difícil já foi construída por alguém

O ALL tem **120+ instituições integradas e mais de 1 milhão de transações classificadas**. O fosso técnico que parecia ser a vantagem — conectar e classificar — já é infraestrutura existente no mercado.

A diferenciação sobrou para o **trabalho**: orçar versus vigiar, e agora também **pagar versus apurar**.

### 4. A nova linha divisória: quem mexe no dinheiro

Jota e Magie movem dinheiro, é o que eles são. Isso lhes dá receita e lhes tira uma coisa: eles querem o dinheiro dentro deles. Um produto que é conta tem interesse no saldo que segura.

> **Os dois movem dinheiro. A Regis não move, e é por isso que ela pode fazer a única coisa que nenhum dos dois faz, que é apuração. E pode ler as contas dos concorrentes sem conflito.**

---

## Os dois que importam

### FinAI — oposto por construção

`finai-oficial.com`

- **Dado:** 100% manual. Do FAQ deles, textualmente:
  > *"Preciso conectar minha conta bancária? **Não.** A FinAI funciona a partir do que você registra — sem precisar conectar banco, cartão ou qualquer conta."*
- Registro por texto, áudio ou foto, pelo app ou WhatsApp. IA classifica o que foi digitado.
- Conta conjunta para casal, caixinhas com metas, cartão cadastrado manualmente.
- **Quem é:** produto solo — *"bancário de dia, indie hacker de noite"*, Santa Catarina. Cerca de 200 usuários.
- **Onde ganha:** pega **dinheiro em espécie**, que nenhum produto conectado enxerga. E entra no ar sem integração, consentimento ou revisão de segurança.
- **Onde perde:** exige o hábito diário que o público-alvo não tem.

**Teste contra as nossas 14 entrevistas:** E13 e E4 não vão registrar transação por transação. E3 não sabe classificar o que não identifica. E7 não tem a transação — ela veio da fatura, não do registro dele. **Só a E5 é cliente do FinAI** — ele substitui a planilha dela com vantagem.

> FinAI atende quem já tem disciplina e quer ferramenta melhor.
> Nós atendemos quem não tem disciplina nenhuma.

**Contradição interna deles:** a home cita que *"97,5% das pessoas abandonam o controle financeiro no primeiro mês — não por preguiça, mas porque as ferramentas são complicadas demais"* — e entregam um produto que depende de registro manual diário. *(Esse 97,5% é número de marketing sem fonte. Não usar no nosso pitch.)*

### ALL — o mais próximo, por larga margem

`myall.com.br`

- **Dado:** Open Finance, somente leitura, 120+ instituições. IA classifica cada lançamento.
- **PF e PJ** convivem na mesma conta, com orçamento, categorias e relatórios **independentes**.
- **Distribuição:** parceria oficial com o curso **Inteligência Financeira, de Gustavo Cerbasi**. Canal de aquisição pronto.
- **Números deles:** 4,9 nas lojas, +5 mil pessoas, +1 milhão de transações classificadas.
- **Onde difere:** o trabalho dele é **encaixar gastos num orçamento por blocos**. Classifica para preencher o método, não para achar o que está errado. **Nada sobre duplicidade, cobrança fantasma ou lançamento não reconhecido.**

A frase que marca a fronteira:

> *"O que ela faz sozinha é a parte chata: ler extrato, classificar, somar. O que muda o seu dinheiro só acontece depois que você confirma."*

O ALL é deliberadamente **assistivo**: propõe e aguarda. Uma proposta que se define como **autônoma** ocupa o espaço imediatamente ao lado — e precisa explicar, com clareza, por que autonomia é melhor e não apenas mais arriscada.

**É a pergunta mais perigosa do pitch:** *"por que isso não é só uma feature do ALL?"*

Resposta sugerida: orçar e vigiar são trabalhos diferentes. Orçamento pressupõe que você **vai olhar**. Nosso usuário não olha — e para ele o produto tem que falar primeiro.

---

---

## Os dois que apareceram em 30/08, e são os mais perigosos

### Jota, a maior ameaça do quadro

`jota.ai`

- **O que é:** conta digital que vive dentro do WhatsApp, mais app próprio. A tese declarada é que a principal interface financeira será uma conversa.
- **Dado:** conecta bancos externos por **Open Finance** ("conectar seus bancos, Nubank, MercadoPago, Itaú e outros, pelo Open Finance e gerenciar tudo comigo pela conversa"), e ainda é a própria conta.
- **Move dinheiro:** sim, é o núcleo. Pix, boleto, cobrança de cliente, **venda no cartão em até 12x sem maquininha**, rendimento de 100% do CDI no saldo.
- **Fala sozinho:** sim, e é o posicionamento. O site descreve "antes de sair, o Jota te manda as pendências do dia".
- **Público:** PF, PJ e **MEI**. O alvo declarado é o empreendedor que toca tudo sozinho, quem não tem intimidade com planilha.
- **Escala:** cerca de **300 mil usuários** e **R$ 3,5 bilhões** de volume anualizado.
- **Dinheiro:** seed de US$ 8,9 milhões no início de 2024 (MAYA Capital, HOF Capital) e **Série A de R$ 150 milhões em junho de 2026**, liderada pela Haun Ventures, com HOF, Alter Global e Greyhound.
- **Quem toca:** Davi Holanda, fundador da Bankly, passagem pelo PagBank.
- **Preço:** gratuito.

**O Jota 2.0** é a parte que dói: a virada anunciada é de assistente reativo para **agente que se antecipa**, categorizando gastos sozinho, organizando contas e produzindo insight sem ser perguntado. Nos testes eles relatam engajamento 5 vezes maior.

**O que ele não faz, e é a nossa brecha inteira:** nada de fiscal. Em todo o site, nenhuma menção a DAS, imposto, faturamento acumulado, teto do MEI ou nota fiscal. Ele organiza o fluxo de caixa do dia. Ele não sabe dizer quanto a pessoa faturou no ano nem quanto falta para o teto.

> Jota resolve o dia. A Regis resolve o ano.

### Magie, a camada vendida como infraestrutura

`magie.com.br`

- **O que é:** banking conversacional no WhatsApp e, principalmente, **MagieOS**, plataforma **whitelabel** de agentes financeiros vendida para bancos, fintechs e varejistas.
- **Dado:** Open Finance. **Move dinheiro:** sim, Pix e contas, com crédito e câmbio em desenvolvimento.
- **Escala:** mais de **150 mil clientes**, mais de **R$ 3 bilhões processados**, e **1% das transações Pix via Open Finance**.
- **Dinheiro:** seed de US$ 4 milhões da Lux Capital em 2024, o primeiro investimento do fundo no Brasil. Lançou jornada de consignado com IA e negocia com bancos da América Latina e da Europa.
- **Fiscal:** nada.

**Por que importa mais do que o tamanho sugere:** a Magie ocupa exatamente a posição que a nossa visão chamava de horizonte 4, a camada conversacional embarcada em quem já tem a base. *Consequência: a Regis não disputa ser a camada conversacional. Ela é a camada de **apuração**, e pode rodar dentro da Magie, do Jota, do Cora ou do Asaas.*

### A resposta decorada, para o palco

Se um jurado disser "isso não é o Jota?":

> O Jota é uma conta que fala. Ele resolve o dia da pessoa: cobra cliente, paga boleto, categoriza gasto. Ele não soma o ano nem conhece a régua legal, e nenhuma linha do site dele fala de imposto. Nós não somos conta, não movemos dinheiro, e é por isso que podemos ler todas as contas, inclusive a dele, e responder a única pergunta que ninguém responde: quanto você já faturou este ano, e quanto falta para o teto.

---

## Não é concorrente: Meu MEI Digital

Lançado pelo Ministério do Empreendedorismo (MEMP) com Sebrae, Receita Federal e Serpro. Gratuito, Android e iOS, login gov.br.

Centraliza **serviços e obrigações**: DTE-SN, Carteira do MEI, orientação de pagamento do DAS, formalização e alteração de cadastro, linhas de crédito, conteúdo educativo, alertas de prazo e orientação antifraude. Tem a assistente de IA **"Meire"** para responder dúvidas.

**Não lê dado bancário nenhum.** Os alertas são de prazo, por calendário, não por análise de transação. É o portal de obrigações do MEI, não um monitor financeiro.

---

## Confiabilidade de cada linha

| Nível | Produtos | Como foi verificado |
|---|---|---|
| ✅ **Verificado** | FinAI, ALL, Meu MEI Digital | Site lido página por página, incluindo FAQ. Citações textuais. Meu MEI Digital confirmado em gov.br e imprensa. |
| ✅ **Verificado** | Jota, Magie | Sites institucionais lidos em 30/08/2026, cruzados com Startupi, TI Inside, Mobile Time e TechCrunch. Rodadas e números de escala vêm de anúncio das empresas, sem auditoria independente. |
| ⚠️ **Parcial** | Mobills, Cora, InfinitePay, Asaas | Mobills: o site fala em "integração automática" sem detalhar se é Open Finance. Os demais: lidos por resumo de busca dos próprios sites, sem navegação a fundo. |
| ❌ **Não verificado** | Organizze, bancos | Organizze entrou por constar do mapa inicial, não foi checado. Bancos entraram por conhecimento geral da categoria. **Não usar no pitch sem conferir.** |

**Preços e números de usuários** vêm das próprias empresas e são material de marketing. O "+200 pessoas" do FinAI e o "+5 mil" do ALL não têm auditoria independente.

**O mercado se move.** Este quadro é de 29/08/2026. Qualquer um deles pode anunciar detecção de anomalia na semana que vem.

---

## Fontes

- https://finai-oficial.com/
- https://www.myall.com.br/
- https://www.gov.br/empresas-e-negocios/pt-br/empreendedor/meu-mei-digital
- https://www.mobills.com.br/
- https://jota.ai/
- https://startupi.com.br/jota-levanta-r150-milhoes/ · Série A de R$ 150 milhões, Jota 2.0, 300 mil usuários
- https://www.mobiletime.com.br/noticias/24/02/2025/jota-whatsapp/ · lançamento e fundadores
- https://magie.com.br/sobre · MagieOS, whitelabel, números de escala
- https://techcrunch.com/2024/08/22/lux-capital-made-its-first-investment-in-brazil-a-4m-seed-for-ai-fintech-magie · seed da Lux Capital
