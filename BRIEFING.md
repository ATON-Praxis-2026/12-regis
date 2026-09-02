---
titulo: Briefing da Regis
tipo: briefing
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: O que o time vai construir em 24 horas, com as decisões já fechadas, o escopo, o cronograma, o pitch e os riscos.
---

# BRIEFING · Regis (Financial Anomaly Autopilot)

Hackathon · Time 12 · Mesa 12 · Tema 20 (Financeiro)
Escolhido em 29/08/2026 às 11:38 · Entrega em 24 horas

---

## 1. O desafio (o que precisa ser entregue)

**Tema oficial:** Financial Anomaly Autopilot. "Deixe uma IA procurando dinheiro vazando 24 horas por dia."

**O desafio, nas palavras do brief:** construir um autopilot que monitore movimentações financeiras e encontre cobranças duplicadas, valores atípicos, despesas inesperadas e possíveis erros.

**Por que alguém quer isso:** elimina a conferência amostral de extratos e faturas e mantém vigilância contínua sobre cobrança duplicada, valor fora do padrão e despesa que ninguém aprovou.

**O que o jurado espera ver:** um autopilot funcionando. Não é um dashboard de finanças, não é um categorizador de gastos. É um agente que encontra o que está errado e faz alguma coisa a respeito.

---

## 2. O time

| Pessoa | Base | Sabe de | Quer aprender | Ferramentas | Papel no hackathon |
|---|---|---|---|---|---|
| **Kysa Robert** (Arcádia · Criação) | Projeto pontes entre mundos. Constrói gerador automático de apresentações e propostas. | construção · IA | comercial · narrativa | Claude, código, n8n/automação, APIs, agentes/RAG, design | **Tech lead.** Motor de detecção, agente de IA, integrações, automação. |
| **Ana Silveira** (Órbital · Gestão) | UX Designer, Rio. Constrói protótipo de app financeiro. | construção · narrativa | narrativa · IA | Claude, código, IA, mobile, design | **UX e interface.** Fluxos, telas, tom das mensagens, protótipo navegável. Já está construindo um app financeiro, ganho direto. |
| **Gabriel Hardt** (Arcádia · Criação) | Criatividade e estratégia, São Paulo. Organizando marca nova e seus sistemas. | narrativa · mercado | construção · organização | Claude, código, APIs, IA de imagem, design | **Narrativa e pitch.** Posicionamento, história da demo, roteiro da apresentação, marca. |
| **Márcio Faustini Modonezi** (Arcádia · Criação) | Fundador de estúdio criativo, Campinas. Transformando agência em empresa de branding. | construção | construção · mercado | Claude, código, IA de imagem, design | **Identidade visual e materiais.** Nome, marca, slides, assets visuais, apoio no front. |

**Leitura rápida do time:** três pessoas de Criação e uma de Gestão. Somos fortes em narrativa, design e IA aplicada. Somos fracos em engenharia pesada e em dados financeiros reais. Isso define a estratégia: **ganhar pela clareza do produto e pela demo, não pela sofisticação estatística.**

---

## 3. O que a pesquisa já nos disse

### 3.1 O ciclo do vazamento (enquadramento-problema)

Uma cobrança errada percorre seis etapas: **Acontece → Aparece → Percebe → Entende → Age → Resolve.** O tempo se perde em *Percebe* e *Age*.

O brief nos empurra para *Percebe*, que é onde todo concorrente já mora e onde detecção estatística virou commodity.

**Quatro enquadramentos possíveis, só dá para defender um:**

| | Problema | Produto | Risco |
|---|---|---|---|
| **A · "Ninguém olha"** | Cobertura | Vigilância contínua | Vira feed de alertas e morre de fadiga |
| **B · "Olho mas não sei se é problema"** | Julgamento | Contexto e evidência | Depende de dados que não teremos |
| **C · "Sei que está errado mas resolver é um inferno"** | Resolução | Agente que redige contestação e acompanha estorno | Depende de terceiros, difícil demonstrar |
| **D · "Não quero ser eu que deixou passar"** | Responsabilidade | Rastro auditável | Vende tranquilidade, valor difícil de medir |

**A pergunta que todo time esquece:** o que é "normal" no dia 1? Sem histórico, o sistema fica mudo ou grita para tudo. Resolver bem a primeira semana de uso já nos diferencia.

### 3.2 A tese central (catálogo de anomalias)

Toda anomalia tem dois eixos: **tipo** (duplicidade, valor, recorrência, contraparte, comportamento, processo, conciliação, fiscal) e **certeza**. A certeza é o eixo que decide o comportamento do produto:

| Certeza | O que é | O que o autopilot faz |
|---|---|---|
| **Fato** | Verificável. Duplicata exata, estorno que não caiu, teste grátis que virou pago. | **Resolve** sozinho ou entrega a ação pronta. |
| **Regra** | Fato que só existe se conhecermos a política de quem usa. | **Encaminha** para quem decide. |
| **Suspeita** | Desvio estatístico. Na maioria das vezes é legítimo. | **Pergunta**, contextualiza ou registra em silêncio. |

> **A tese:** o nível de autonomia do autopilot varia com o nível de certeza da anomalia. Fato ele resolve, regra ele encaminha, suspeita ele apenas pergunta. Nenhum concorrente comunica isso. Todos jogam tudo no mesmo feed de alertas.

**O que dá para demonstrar em 24h:** tudo marcado como *fato* (sem baseline, sem configuração). *Regra* exige política cadastrada. *Suspeita* exige histórico que não teremos.

### 3.3 O impasse PF versus PJ e como o MEI resolve (insights-mei)

- **PF:** poucas transações, uma pessoa só, a família dominante é *recorrência* (assinatura que não morre). O autopilot compete com "eu olharia se quisesse".
- **PJ:** centenas de transações, três pessoas diferentes detectam, decidem e resolvem. Família dominante é *processo* (regra interna quebrada). Quase tudo é *regra* e exige cadastrar política interna, inviável em 24h.
- **MEI:** PJ no papel, PF na prática. Uma pessoa decide, paga e resolve. Mas carrega uma camada fiscal com prazo e consequência, e **essa regra é pública e idêntica para todos**: teto de R$ 81.000/ano, DAS vence dia 20, DASN em maio. Ganhamos a camada de *regra* sem configurar nada.

**Números que sustentam** (status de verificação conferido no `DOSSIE.md`, seção 10):

| Número | Status | Como citar |
|---|---|---|
| Teto de R$ 81.000/ano, **congelado desde 2018** | ✅ verificado | Era "2019" nas versões anteriores deste briefing. **Corrigido.** Tolerância de 20% até R$ 97.200; acima disso, desenquadramento retroativo a janeiro, multa de 0,33% ao dia e juros Selic. |
| 570 mil MEIs desenquadrados em 2024 | ✅ Receita Federal | **30 vezes mais que em 2023**, atribuído ao cruzamento de Pix, cartão e transações. |
| ~60% dos MEIs misturam finanças pessoais e do negócio | ✅ Sebrae, 2023 | Dizer **"cerca de 60% dos MEIs, Sebrae, 2023"**. Não dizer "61% dos empreendedores": a fonte descreve populações diferentes e o dado é de 2022/2023. |
| Resolução CGSN nº 183/2025 (receita no CPF soma ao limite) | ✅ em vigor desde 01/01/2026 | A Receita publicou nota **desmentindo fake news** sobre ela e há questionamento constitucional. Dizer com precisão, sem dramatizar. Se o jurado for contador, ele conhece a polêmica. |
| 404 mil Termos de Exclusão em março/2026 | ⚠️ **não verificado** | Não usar no pitch até alguém confirmar na fonte. |
| 59% em caderno, 15% de cabeça | ⚠️ **não verificado** | Sustenta a frase "o concorrente real não é um app", que é afirmação forte. **Prioridade de verificação.** |
| Total de MEIs ativos | ⚠️ fontes divergem (11,5, 12,9 e 16,8 milhões) | Puxar do Portal do Empreendedor antes de usar. |

**A leitura melhor do número de 570 mil** (do `INSIGHTS.md`), mais forte que citar o número seco:

> **O Estado começou a cruzar os dados do MEI. O MEI é o único que não cruza os próprios dados.**

**Contra-narrativa a ter pronta:** a imprensa tratou os 570 mil como notícia boa, negócios crescendo (CartaCapital: "reforçando expansão da economia"). Se alguém devolver "isso não é bom?", a resposta é: crescer é ótimo, ser pego de surpresa retroativamente com multa diária e recálculo do ano inteiro não é. O produto não impede crescer, impede ser surpreendido.

**A frase de pitch que saiu daqui:** *"O vazamento do MEI não é só o que sai. É o que entra sem ele perceber."* Todo concorrente vigia despesa. Para o MEI, a anomalia mais cara está na receita: faturar demais, receber no CPF errado, receber menos do que vendeu.

### 3.4 O que 14 pessoas disseram (relatório de pesquisa)

Pesquisa por WhatsApp, 6 perguntas, 14 participantes (PF, rede de contatos do time).

- **12 de 14** tiveram ao menos um episódio de cobrança inesperada. **10 contestaram, 10 recuperaram o valor.**
- Tipos de episódio: fraude/clonagem (4), recorrente não reconhecida (3), erro ou taxa da instituição (2), cancelamento não honrado (2), duplicada (1).
- **Tempo até perceber:** imediato quando houve notificação externa; até 5 meses quando não houve. Quem descobriu rápido foi avisado por push ou pelo banco.
- **Contestar funciona.** A maioria descreveu como simples. O atrito está em provar, em ter que trocar cartão e em "descontar na próxima fatura em vez de devolver".
- **A dor espontânea mais citada (6 menções): não conseguir identificar o estabelecimento.** Estacionamento aparecendo com CNPJ de mercado, Pix crédito com nome de pessoa aleatória, "fico me perguntando meses à frente o que diabos é isso".
- **Frase de ouro (E13):** *"Eu olharia mais o extrato se tivesse alguma forma automática de categorizar as coisas e me mostrar só o que fosse relevante ou atípico."*
- **Frase de ouro (E12, sobre deixar passar):** *"Porque imaginei que tivesse feito mesmo."*

**O que isso muda na leitura:** a etapa *Resolve* é menos dolorosa do que a gente achava (10 de 10 recuperaram). O gargalo real está em *Percebe* (quem não tem push demora meses) e principalmente em *Entende* (não sei o que é essa cobrança, então assumo que fui eu). Isso fortalece o **enquadramento B** para PF.

### 3.5 O que os MEIs responderam no forms (respostas-forms, leitura preliminar)

Forms enviado no fim da tarde de 29/08. **15 respostas até 30/08, 14 de MEI e 1 de ME** (R12, fora do ICP, mantida na amostra e marcada). Rede de contatos do time, com viés claro: gente organizada, com contador na família ou conta PJ separada. Atualizar esta seção conforme chegarem mais (o arquivo `pesquisa do grupo/respostas-forms.md` é regerado pelo script).

A rodada de 9 respostas novas fez o que faltava: **puxou a amostra para cima do teto.** Antes ninguém passava de R$ 40 mil. Agora são 4 acima disso, e um deles já estourou o teto.

O que apareceu, e o que isso faz com as hipóteses:

| Hipótese do doc de insights | O que 15 respostas mostram | Leitura |
|---|---|---|
| O MEI não sabe quanto faturou no ano | 13 de 15 dizem "acompanho de perto". Ninguém marcou "não faço ideia". | **Contra a hipótese na superfície, confirmada no detalhe.** A confiança declarada é alta, mas a distância do teto continua sendo um número que ninguém tem (linha de baixo). Eles sabem o saldo, não sabem o acumulado. |
| O medo do teto aparece sozinho | Ninguém mencionou medo. 6 de 15 sabem que existe teto mas **não sabem quanto falta**, 7 sabem "mais ou menos", 1 perguntou "esse teto não tinha subido?" e 1 **já estourou**. | **Confirmada.** Não é medo, é névoa. Com n maior a contradição fica mais dura: 13 acompanham de perto e 14 não sabem dizer a distância exata. "Faltam R$ X" segue vago para todo mundo. |
| A mistura de contas é escolha, não descuido | 9 de 15 têm conta separada e mantêm assim. 6 misturam na prática: 1 chama de "bagunça", 1 **abandonou a conta PJ por causa das tarifas**, 1 diz que "a PJ tem arcado com as contas pessoais", 1 **varre a PJ para a PF assim que o dinheiro pinga**. | **Enfraquecida como dor principal, mas apareceu um caso pior.** Conta separada virou maioria. O problema deixou de ser a bagunça e passou a ser a varredura: quem esvazia a PJ toda hora torna o saldo inútil como medida de faturamento. Quem lê por saldo erra. Quem soma entrada por entrada acerta. |
| Ninguém confere repasse | Todos dizem que confere e que bate. Mas **13 de 15 recebem só por Pix, transferência ou Wise**. Só 2 têm canal intermediado: 1 com 15% em maquininha e 1 com 30% em link de pagamento. | **Continua sem teste.** Pix cai inteiro, não tem repasse para conferir. Duas respostas novas encostaram no tema e nenhuma delas tem volume. Esta é a hipótese que o forms não consegue validar. |
| A dor dominante é ansiedade, não economia | Quase todo mundo com tom prático. **Uma exceção nova e explícita:** "fico encucada se estou fazendo certo ou se repentinamente vou ser cobrada por ter preenchido algo errado". | **Meio confirmada.** A ansiedade existe e é sobre estar errada sem saber, não sobre perder dinheiro. É exatamente o que o resumo de tranquilidade responde. |

**O achado inesperado segue de pé: o imposto é terceirizado.** 5 de 15 não cuidam disso (esposa, esposa contadora, contadora da família, contador, área financeira). E quem não terceiriza acumula atraso em silêncio: 4 relatos de atraso, incluindo **10 parcelas de DAS atrasadas regularizadas num boleto só**, um **parcelamento de DAS atrasado por anos** e alguém que "perde a data e acaba pagando a fatura do mês atual junto com a do anterior, pagando multa". Quem terceiriza não sabe responder ("não lembro, quem resolveu foi minha esposa").

**O achado novo: alguém já estourou o teto, e o método de controle é escolher o que dá nota.** R15 fatura mais de R$ 81 mil e respondeu, na pergunta do teto, "já bateu mas controlo o que dou nota ou não, então até agora não fui desenquadrada". É a primeira resposta da amostra que vem de cima do teto, e ela diz duas coisas ao mesmo tempo. A dor é real e chega antes do desenquadramento. E o controle que existe hoje é feito na emissão da nota, não na conta.

**Isso pede uma decisão de produto, e ela é limite duro.** A Regis mede o dinheiro que entra, não o que foi declarado. Ela nunca sugere segurar nota, atrasar recebimento ou dividir entrada para caber no teto. Diante de um estouro, ela mostra o número, explica o que muda no imposto e encaminha para a contadora. Ajudar a esconder faturamento está fora, pelo mesmo motivo que mover dinheiro está fora.

**A ressalva que precisa ir para o pitch:** a hipótese central do ICP, o MEI com recebimento intermediado e volume alto, **continua sem validação neste forms**. 13 de 15 recebem por Pix, transferência ou Wise, canais que caem inteiros e não têm repasse para conferir. As 14 conversas com pessoas físicas sustentam a dor de reconciliação, o forms não. Se um jurado perguntar, a resposta honesta é essa, não um número inflado.

**O que isso muda no produto:** a Regis compete menos com o app do banco e mais com **a esposa contadora e a planilha**. Para quem tem contador, ela é o que prepara o material e avisa antes do prazo. Para quem não tem, ela é o lembrete do dia 20 que evita os 10 boletos atrasados.

**O que isso muda na pesquisa:** a amostra segue enviesada para o MEI organizado, mas duas das três lacunas se mexeram. Volume alto: **resolvida em parte**, já são 3 respostas acima de R$ 50 mil e 1 acima do teto. Canal intermediado: **aberta**, só 2 de 15, ambas com participação pequena. Controle no caderno: **aberta**, ninguém da amostra. Se der tempo antes do pitch, o pedido específico é por quem recebe em maquininha ou marketplace, que é onde a hipótese de repasse vive.

### 3.6 Quanto custa ler cada conta (custo-por-conta)

A pergunta certa não é "quanto custa o Open Finance", é **quanto custa cada conta que o agente precisa ler**. Sem esse número não dá para precificar nada.

| Plataforma | Custo reportado | Unidade | Observação |
|---|---|---|---|
| Pluggy | R$ 2.500/mês | Plano fechado | Limite de contas não divulgado |
| Belvo | R$ 6.000/mês | Até 25 links | Acima disso, negociação |
| Tecnospeed | R$ 1.500 + R$ 540/mês | Plano fechado | Limite não confirmado |
| Celcoin | Por transação | Sem setup | Valor não divulgado |
| **Banco MCP** | **R$ 19,90/mês** | **Por conta conectada** | Único com preço unitário confirmado. Revende a Pluggy no varejo. |

**Cadeia de dependência:** Banco Central → Pluggy (licenciada ITP) → Banco MCP (revende) → nosso produto. O dado é Open Finance de verdade, mas o risco é de continuidade: se o Banco MCP mudar preço ou sair do ar, o acesso quebra.

**Calculadora (5 contas por usuário, R$ 9,90 por conta acima da faixa base):**
- 10 usuários → 50 contas → R$ 499/mês
- 50 usuários → 250 contas → R$ 2.495/mês
- 200 usuários → 1.000 contas → R$ 9.980/mês

Benchmark fora do Brasil: Plaid cobra US$ 0,30 a 1,00 por conta (Auth) e US$ 0,05 a 0,15 por chamada (Balance). Não cobre bancos brasileiros, serve só de referência no pitch.

**O que isso destrava:** temos um caminho real de integração com custo unitário conhecido. O pitch pode dizer "cada conta custa R$ 19,90 para ler, um MEI tem 2 a 3 contas, o produto se paga com uma duplicata evitada por mês". E temos uma ressalva honesta para falar: o intermediário não é oficial, o sandbox da Pluggy é gratuito e o próximo passo é confirmar o limite do plano Pro direto com o comercial.

**Para o MEI especificamente:** um MEI costuma ter menos contas que a média (conta PJ, conta PF e a maquininha). Custo de infra por usuário fica na faixa de R$ 40 a 60/mês, o que pressiona o preço final. Isso reforça a hipótese do doc de insights: monetização direta é difícil, distribuição via banco, adquirente ou contador é o caminho mais provável.

---

### 3.7 Posicionamento: consciência, sofisticação e concorrentes (posicionamento)

Este é o documento que decide **o que a gente diz**, não para quem. Três camadas, e a ordem importa: comportamento define o ICP, os outros três dizem se ele é vendável.

**Onde o MEI está de consciência: nível 2.** Sabe que a bagunça atrapalha e que o teto existe, mas acha que a saída é "me organizar melhor" ou pagar um contador. Uma parte está no nível 1 (nem formulou como problema). Quase ninguém está no 3 ou 4.

As respostas do forms confirmam isso ao vivo: 6 de 15 sabem que o teto existe e **não sabem quanto falta**, outros 7 sabem só "mais ou menos", e o imposto está terceirizado na esposa ou na contadora da família em 5 dos 15 casos. É exatamente o nível 2, e é a definição do "contador do primo" listado como status quo.

**Sofisticação: dois mercados opostos com a mesma tecnologia.**

| | Vigiar despesa | Vigiar receita do MEI |
|---|---|---|
| Estágio | Avançado | Inicial |
| Quem já disse | Bancos, apps de finanças, gestores de assinatura | Praticamente ninguém |
| Promessa direta funciona? | Não, está gasta | Sim |
| O que seria preciso | Mecanismo novo ou identidade forte | Só ser o primeiro a dizer |

É a justificativa estratégica do segmento: em mercado pouco sofisticado não precisamos ser mais criativos que ninguém, precisamos chegar antes com a frase mais simples. **A promessa que está livre: "Você sabe quanto já faturou este ano?"**

**Concorrentes em três camadas, e a terceira é a que decide:**
- **Diretos:** apps de gestão para MEI, contabilidades digitais, funções nativas de conta PJ. Quase todos assumem que a pessoa alimenta o sistema, e ela não alimenta.
- **Adjacentes:** bancos, adquirentes, marketplaces. Já veem o dado e podem ligar isso quando quiserem. É o risco competitivo real e o canal de distribuição mais provável, então entra no pitch como parceiro, não só como ameaça.
- **Status quo:** o caderno, a planilha, o contador do primo, não fazer nada. **É quem detém o mercado.** Nenhum app perdeu esses usuários porque eles nunca foram de ninguém. O concorrente não é um produto, é um hábito.

> **A barra de comparação não é "melhor que o app X". É menos trabalho que o caderno.**

**As cinco decisões que este documento impõe:**
1. A primeira interação **revela um número**, sem onboarding, sem configuração, sem cadastro de categoria.
2. A promessa do pitch é sobre **receita**, não sobre IA. "Você sabe quanto já faturou este ano?", não "autopilot inteligente de anomalias".
3. O slide de concorrência mostra as três camadas e termina na frase do caderno.
4. **Zero entrada manual no fluxo principal.**
5. Distribuição entra no pitch, porque público inconsciente não busca solução.

#### A contradição que este documento cria (resolver antes de codar)

O posicionamento diz **zero entrada manual**. A Decisão 3 diz **extrato sintético importado** e a Decisão 5 diz que **o MEI manda print, PDF ou comprovante no chat**. Isso bate de frente, e vale separar duas coisas que não são a mesma:

- **Cadastro manual recorrente** (digitar venda por venda, categorizar, alimentar planilha): é isso que mata, é isso que perde para o caderno, e disso a Regis tem que ficar longe. Nenhuma tela nossa pode pedir isso.
- **Uma conexão única de conta** (a pessoa autoriza a leitura da conta pelo Open Finance, no próprio banco): não é alimentar sistema, é autorizar uma vez e pronto. É aceitável, desde que aconteça **uma vez** e a Regis faça todo o resto.

**Como resolver na prática:** a conexão é via Open Finance, a pessoa autoriza a leitura da conta uma vez no próprio banco e a partir daí a Regis trabalha sozinha e fala sozinha, zero gesto recorrente. No hackathon os dados são simulados, então a demo mostra a conta já conectada. No pitch, dizer isso com todas as letras: "você conecta a conta uma vez, e a Regis cuida do resto."

**E mais uma consequência boa:** no chat não existe "primeira tela", existe primeira mensagem. Encaminhar algo para um contato é hábito, e é justamente o oposto de alimentar um sistema. A escolha do canal já estava certa, este documento reforça.

---

### 3.8 O que o dossiê corrigiu (DOSSIE + INSIGHTS)

Análise das 14 entrevistas transcritas com Whisper local, com verificação de fonte. Cinco crenças do time caíram e três achados se firmaram. Isso muda o que construir, não só o que dizer.

#### O problema central, reescrito

> **O extrato é escrito na língua do sistema de pagamentos, não na língua da vida da pessoa. Por isso ela não reconhece o que é dela.**

Um estacionamento aparece com o CNPJ de um mercado. Um Pix crédito aparece com o nome de um desconhecido. E como ninguém sabe, **todo mundo chuta**: E12 chutou que era dele e pagou. E3 chutou que não era dela e cancelou um serviço que usava. E7 não quis chutar e gastou 3 horas no Google por R$ 30. E13 cansou de chutar e parou de olhar.

O reenquadramento que sai daí, e que é a melhor frase do projeto:

> **Não é um detector de anomalias. É um tradutor, e a detecção é o que sobra depois que tudo está traduzido.**

#### Cinco crenças que caíram

| Crença | Veredito | Consequência |
|---|---|---|
| "Contestar é difícil, o valor está em agir pelo usuário" | **Falso.** 10 contestaram, 10 recuperaram. A maioria achou simples. | O gargalo não é `Age → Resolve`. É `Percebe` e sobretudo **`Entende`**. |
| "As pessoas deixam passar por preguiça" | **Falso.** 9 de 14 negaram com veemência. | Não vaza por negligência, vaza por **incapacidade de reconhecer**. |
| "Reajuste sorrateiro é uma das maiores dores" | **Zero menções em 14.** | **Fica no código** (sai quase de graça depois da recorrência), **sai do pitch** como dor validada. |
| "Fraude é o gancho mais forte" | Comum (4 de 14), mas **o banco pega primeiro**. Bradesco avisou antes, cartão bloqueado automaticamente. | **Não competir em fraude.** Antifraude de emissor é maduro. |
| "Identificar o estabelecimento é detalhe técnico" | **É o produto.** Dor mais citada (6 de 14, espontânea). | Vira a peça número 1 da construção. |

#### O erro nos dois sentidos (o argumento mais forte da pesquisa)

O briefing usava só o E12 ("imaginei que tivesse feito mesmo"). Falta o par dele: **a E3 cancelou serviços que usava** por não lembrar o que eram. Juntos provam que o problema é **reconhecimento, não negligência**: os dois estavam prestando atenção e erraram assim mesmo, em direções opostas. Entra no pitch.

#### O produto não muda o valor, muda o tempo

```
custo do vazamento = valor da cobrança × meses até alguém perceber
```

| Como acompanha | Tempo até perceber |
|---|---|
| Recebe aviso externo (push, mensagem do banco) | imediato |
| Tem ritual mensal | ~1 mês |
| Não olha | 3 a 5 meses, ou nunca |

O produto move todo mundo para a primeira faixa, e o ganho é maior em quem está na última. Numa recorrência multiplica: os 5 meses do E4 são cinco cobranças. **Valida a métrica escolhida.**

#### A ordem de construção (a parte que importa para codar)

Duas peças destravam cinco das doze anomalias de PF. O esforço não se divide por anomalia, **concentra em duas peças**:

1. **Identificação do estabelecimento** · pré-requisito de quase tudo. É onde o LLM ganha de regex, e é o que justifica IA no projeto em vez de enfeite. Sinais: descritor sem correspondência no histórico, razão social diferente do nome de fachada, padrão de gateway (`PAG*`, `MP *`), Pix crédito com nome de pessoa física.
2. **Detecção de recorrência** · destrava assinatura fantasma, reajuste e cancelamento não honrado. Sinal: série mensal do mesmo estabelecimento, intervalo de 28 a 31 dias, valor constante.
3. **Duplicidade e feriado** · as duas regras determinísticas e baratas. Duplicidade: par (estabelecimento, valor) em janela menor que 24h, excluindo categorias com repetição legítima. Feriado: juro ou tarifa cruzado com calendário de feriados (o caso da E8, débito automático que rodou fora do dia por feriado municipal).
4. **Motor fiscal MEI** · aritmética sobre regra pública.
5. **O limiar de quando falar** · é o que separa autopilot de relatório agendado.

**Aviso:** os limiares (24h, 28 a 31 dias) são pontos de partida e nunca foram testados contra dado real.

---

### 3.9 O ICP redefinido (resultado-pesquisa-icp) · **é o documento que fecha a Decisão 1**

As 15 respostas de MEI refutaram a tese central, e é exatamente por isso que agora sabemos quem é o cliente. A amostra triplicou e a conclusão não mudou, ficou mais firme. Resultado registrado como saiu:

| Hipótese | Resultado |
|---|---|
| H1 · O MEI não sabe quanto faturou | **Refutada, com ressalva.** Todos deram o número de bate pronto, 13 de 15 "acompanho de perto". A ressalva: eles sabem o saldo, não sabem o acumulado do ano. |
| H2 · O medo do teto aparece sozinho | **Não apareceu.** Mas 14 de 15 não sabem a distância exata até o teto, e 1 já estourou e controla o estouro escolhendo o que dá nota. |
| H3 · Misturar contas é escolha | **Parcial.** 9 de 15 têm conta separada. Quem mistura tem motivo econômico (tarifa da conta PJ) ou assume a bagunça. Caso pior que a mistura: quem varre a PJ para a PF assim que o dinheiro pinga. |
| H4 · Ninguém confere repasse | **Sem teste.** Todos conferem ou consideram desnecessário, mas 13 de 15 recebem só por Pix, transferência ou Wise, que caem inteiros. Não existe repasse para conferir nesta amostra. |
| H5 · A dor dominante é ansiedade | **Parcial.** Tom tranquilo em quase todas, com uma exceção explícita: "fico encucada se estou fazendo certo ou se repentinamente vou ser cobrada por ter preenchido algo errado". A ansiedade é sobre estar errada sem saber, não sobre perder dinheiro. |

**Por que caíram, e o que isso destrava:** **13 de 15 recebem só por Pix, transferência ou Wise.** As duas exceções são pequenas, 15% em maquininha numa e 30% em link de pagamento na outra. Sem intermediário não existe repasse, não existe antecipação, não existe retenção, não existe chargeback. **Metade do catálogo de anomalias não tem onde acontecer.** E o volume é baixo o bastante para caber na memória, mesmo entre os 4 que já passam de R$ 50 mil por ano.

> **A variável mestra não é ser MEI. É como o dinheiro entra e em que volume.** Não é resultado ruim, é a régua que faltava.

#### O ICP (estreito de propósito)

> **MEI com recebimento intermediado (maquininha, marketplace ou gateway), com volume alto de transações, em que o valor que cai na conta pode não ser o valor que foi vendido.**
>
> Comércio de bairro, alimentação, **salão**, seller. **Não** prestador de serviço que recebe por Pix. E isso agora sabemos, não supomos.

| Faz sentido para | Não faz sentido para |
|---|---|
| Recebimento passa por intermediário | Pix direto, sem intermediário |
| Volume que não cabe na memória | Poucas vendas por mês |
| O valor recebido pode ser diferente do vendido | Valores cheios, contrato fixo |
| Vários canais que não conversam | Faturamento muito distante do teto |

**Isso pode virar tela e é um baita momento de demo:** um onboarding que pergunta o canal e responde com honestidade, *"pelo seu perfil, você provavelmente ainda não precisa disso"*. **Produto que sabe recusar usuário é raro**, e é uma demonstração de confiança que nenhum concorrente faz.

#### O achado que ninguém previu: são dois usuários

Metade da amostra **não faz a parte fiscal**, outra pessoa faz (esposa, esposa contadora, contadora da família). Dos demais: um gera boleto manualmente todo mês, um deixou dez parcelas atrasarem, uma disse "tive que aprender sozinha".

> O padrão não é anomalia que passa despercebida. É **ou você tem alguém, ou você vira o especialista sozinho.**

**Consequência de design:** se existem dois usuários (quem vende e quem organiza), o produto precisa de uma **saída compartilhável**: um resumo que o MEI manda para quem organiza, ou um acesso para essa pessoa. Nenhum concorrente trata a conta como coisa de duas pessoas. E provavelmente é o segundo que abre o app.

#### Quatro regras para não estragar o argumento

1. **Nunca dizer "a pesquisa mostra".** São seis conversas. A formulação certa é **"nas seis conversas que tivemos"**. Inflar o número derruba todo o resto.
2. **A demo tem que ser do ICP certo.** Se a tela mostrar um MEI de serviço com Pix, ela contradiz nossa própria tese. **A persona recebe por maquininha ou marketplace.**
3. **Dizer que os dados são simulados antes que perguntem.** Simulação declarada é método; escondida é problema.
4. **Manter as hipóteses refutadas no deck.** Hipótese que caiu e ficou registrada vale mais que hipótese omitida. É o que separa time que pesquisou de time que ilustrou.

---

### 3.10 Concorrentes (lacuna grave que o dossiê apontou)

O briefing não mencionava concorrentes em nenhuma seção. Isso é perigoso, porque existe **a pergunta mais provável do jurado**.

| Produto | De onde vem o dado | Fala sozinho? |
|---|---|---|
| **ALL** (myall.com.br) | Open Finance, 120+ instituições, +1M transações classificadas por IA, PF e PJ separados | Parcial, assistivo |
| **FinAI** | 100% registro manual, "não precisa conectar banco" | Não |
| **Mobills** | "integração automática" | Não |
| **Cora / InfinitePay / Asaas** | é a própria conta | Não |
| **Meu MEI Digital** (governo) | não lê dado bancário | Avisa prazo por calendário |
| **Bancos** | é o próprio banco | **Sim**, push na compra |

**Três fatos que importam:**
1. A linha divisória **não é a IA**, todos usam IA. É **de onde vem o dado**.
2. **Ninguém, além do banco, procura o usuário.** O ALL diz na própria home: "é isto que você abre todo dia".
3. **A parte difícil já foi construída.** Conectar e classificar virou infraestrutura, não diferencial.

**A pergunta mais perigosa do pitch:** *"por que isso não é só uma feature do ALL?"*

**A resposta, que precisa estar decorada:**
- O ALL classifica para **preencher um orçamento**, não para achar o que está errado.
- É declaradamente assistivo: "o que muda o seu dinheiro só acontece depois que você confirma".
- É um produto que **você abre**. O nosso usuário não abre.
- **Não tem nada de fiscal do MEI.**

> **Orçar e vigiar são trabalhos diferentes. Orçamento pressupõe que você vai olhar. Nosso usuário não olha, e para ele o produto tem que falar primeiro.**

E o FinAI é o nosso oposto exato: registro manual, então não pode achar vazamento invisível por construção. Rodando as 14 entrevistas contra ele, **só a E5 seria cliente**.

---

### 3.11 O teto invisível (pesquisa-mei-teto-invisivel) · **reposiciona o tema inteiro para o MEI**

Dossiê de mercado feito para calibrar o formulário de campo. Ele responde uma pergunta que nenhum documento anterior tinha respondido: **para o MEI, o que exatamente é uma anomalia financeira?**

> **Para o MEI, a anomalia não é uma cobrança duplicada. É o próprio faturamento**, um número que ele é obrigado por lei a controlar e é estruturalmente impedido de calcular.

#### A régua que define tudo

Todo o problema orbita um número congelado desde 2018.

| Faixa | O que acontece |
|---|---|
| Até **R$ 81.000** por ano (R$ 6.750 por mês) | Teto legal, tudo normal. |
| Até **R$ 97.200** (excesso de até 20%) | DAS complementar e migração para ME em janeiro do ano seguinte. |
| **Acima de 20%** | **Desenquadramento retroativo a janeiro do ano corrente.** O ano inteiro é recalculado como microempresa, com juros e multa sobre impostos que ele nunca soube que devia. |

A diferença entre as duas últimas faixas é brutal e quase ninguém sabe dela. Passar do teto não é multa, é perda do regime.

#### Por que somar é impossível, e não só chato

Esta é a parte que separa a Regis de um app de anotação. O MEI não deixa de somar por preguiça. São cinco elos, e **cada elo é uma oportunidade de produto**.

| # | O elo | Por que trava |
|---|---|---|
| 1 | **O dinheiro entra por quatro portas** | Pix na chave pessoal, Pix na conta PJ, maquininha, dinheiro vivo, boleto, plataforma. 56% das MPMEs usam maquininha e quase nenhuma usa só ela. **Não existe extrato único onde o faturamento apareça inteiro.** |
| 2 | **Tudo cai na conta do dinheiro de casa** | 61% misturam. No mesmo extrato: a venda, o Pix da irmã, o salário do cônjuge, o reembolso do amigo. Separar exige julgamento transação a transação, 400 vezes por mês. |
| 3 | **A maquininha deposita líquido, o teto conta bruto** | A venda de R$ 100 cai como R$ 96,50. Taxas consomem até 3% da receita. **Quem controla pelo extrato subestima o próprio faturamento, sempre na direção perigosa.** |
| 4 | **A ferramenta de controle é papel** | Planilha 30%, caderno 25%, app ou sistema 20%, contador 13%, nenhum controle 10%. Nada disso reconcilia repasse de adquirente. |
| 5 | **O resultado só aparece um ano depois** | Ele descobre na declaração anual, em maio do ano seguinte, ou quando a Receita avisa. **É um velocímetro que só liga depois da multa.** |

#### Por que agora: a fiscalização virou algoritmo

O que mudou não foi a regra, foi a capacidade do Estado de enxergar.

- **Os desenquadramentos por excesso saltaram 30 vezes de 2023 para 2024**, passando de 570 mil MEIs. A causa apontada não foi mudança de lei, foi o **cruzamento automático de Pix e cartão pela Receita**.
- **Desde 1º de janeiro de 2026 a e-Financeira reporta movimentação mensal consolidada de PJ acima de R$ 6.000** (IN RFB 2.278/2025). Repare na aritmética: o teto do MEI equivale a R$ 6.750 por mês. **Praticamente todo MEI que se aproxima do limite já está sendo reportado todo mês.**
- **A dívida do MEI cai no CPF do dono.** DAS atrasado negativa o titular e interrompe a contribuição previdenciária, o que pode bloquear auxílio-doença, salário-maternidade e aposentadoria.
- **O teto está congelado há 8 anos** e a reforma tributária começa a alíquota de teste em 2026, quando o MEI deixa de gerar crédito para clientes PJ. Só 11% das empresas se dizem preparadas.

**Números que sustentam (com a atribuição correta):**

| Número | O que é | Fonte |
|---|---|---|
| **12,9 mi** | MEIs ativos. A categoria é 78% de todas as empresas abertas em 2026. | Sebrae, out 2025 e 2026 |
| **570 mil** | Desenquadrados em 2024 por ultrapassar o teto, 30 vezes mais que em 2023. | **Análise da Contabilizei sobre dados da Receita**, não publicação oficial. Citar assim. |
| **404 mil** | MEIs que receberam Termo de Exclusão do Simples por dívida em março de 2026. | Receita Federal, mar 2026 |
| **61%** | Pagam contas da empresa com a conta pessoal. Era 60% em 2023, não melhorou. | Sebrae, Hábitos Financeiros 2025 |
| **68%** | Sem previsão de saldo de caixa nem para o mês seguinte. | Sebrae, levantamento **mais antigo**. Usar como ordem de grandeza, não como dado de 2026. |
| **R$ 0** | De reajuste no teto desde 2018. Três projetos parados (PLP 67/2025, PLP 186/2026). | Contabilizei |

#### Cinco leituras para o produto (em ordem de peso)

1. **A anomalia é a receita, não a despesa.** O tema fala em "despesa que ninguém aprovou". Traduzido para o MEI, isso é um mês que joga a média anual acima de R$ 6.750, e um DAS complementar retroativo com juros que ninguém viu chegando. **Isso resolve a tensão registrada em 3.7**, a de que "dinheiro vazando" pressupõe abundância: aqui o alerta vale exatamente quando o negócio vai bem, porque **crescer é o que aciona o risco**. *Consequência: o autopilot monitora entrada contra um limite legal, não saída contra um orçamento. Muda fonte de dado, tela e promessa.*
2. **Somos o espelho do algoritmo da Receita.** O Estado já tem o número. O empreendedor não. *Consequência: a promessa não é "organize suas finanças", é **"veja o que a Receita já vê sobre você"**. Urgência imediata, sem precisar convencer ninguém de que planejamento é importante.*
3. **O erro do líquido versus bruto é a anomalia mais bem escondida do Brasil.** Pequeno por transação, acumula o ano inteiro, aponta sempre na direção do perigo. É detectável cruzando o valor da venda com o repasse da adquirente, e **é exatamente o "possível erro" que o enunciado do desafio pede**. *Consequência: um detector que reconstrói o bruto a partir do líquido entrega um número que nem a planilha do usuário nem o app do banco têm.*
4. **O CPF é a alavanca emocional, não o CNPJ.** A dívida atravessa da empresa para a vida pessoal, e 61% já misturam as duas contas. *Consequência: falar em "seu nome" e "sua aposentadoria", nunca em "compliance fiscal do seu CNPJ".*
5. **Aqui o banco não é concorrente.** Nenhum banco enxerga o dinheiro vivo, a maquininha de outro adquirente ou a chave Pix pessoal, e nenhum tem incentivo para calcular obrigação tributária de cliente. **A conta PJ resolve pagamento. Ninguém resolve apuração.** *Consequência: o espaço competitivo é contra contador e planilha, não contra banco, e isso melhora muito a resposta da seção 3.10.*

#### O que este documento muda no resto do briefing

- **Reforça o ICP de 3.9 em vez de contradizê-lo.** A leitura 3 (líquido versus bruto) só existe quando há intermediário, que é justamente o recorte fechado na Decisão 1.
- **Corrige a leitura de concorrência de 3.10.** O banco sai da lista de ameaças reais para o recorte MEI.
- **Dá o slide de abertura do pitch**, se o campo confirmar: a soma de "não faço ideia" com "nunca somei" na pergunta 1, cruzada com "foi chute mesmo" na 1b. *"X de cada 10 MEIs que ouvimos não sabem quanto faturaram este ano, e a Receita sabe."*

#### Ressalva metodológica sobre o formulário (ler antes de tabular)

Na pergunta 1, as opções "Não faço ideia" e "Sei mais ou menos o mês, mas nunca somei" estão na mesma lista das faixas de valor. Isso mistura resposta com metadado: quem marca uma delas sai da distribuição, e o que sobra fica enviesado para quem tem mais controle. **Não apresentar "X% dos MEIs faturam entre R$ 40 e 60 mil" como se fosse a amostra inteira.** Reportar sobre a base de quem respondeu uma faixa, e dizer o tamanho dessa base.

**Perguntas que faltam no formulário**, em ordem de retorno: (alta) *"Você já passou do teto, ou já levou algum susto com imposto? Conta o que aconteceu."*; (alta) *"Da última vez que você precisou saber quanto tinha faturado, como você fez? Passo a passo."*, a única pergunta de comportamento observado num formulário todo declarativo; (média) *"Quem cuida disso: você, um contador, alguém da família?"*, que conversa direto com o achado dos dois usuários em 3.9; (média) na pergunta 4, perguntar explicitamente *"você anota o valor da venda ou o valor que caiu na conta?"*.

### 3.12 O wireframe e as decisões de copy (wireframe-regis.html)

Primeiro artefato de design da série (documento 07, na raiz do repositório). Traduz o job principal (jobs to be done, documento 06) em duas superfícies, a conversa no chat (núcleo) e o app de memória (apoio), e desenha um achado do começo ao fim: detecta, prepara, você envia, a Regis vigia, fecha o valor.

> **O último metro é humano.** A Regis detecta, redige e acompanha. Ela nunca envia a contestação, nunca cancela a assinatura, nunca estorna. Quem executa a ação é o usuário, e isso deixa o limite "não move dinheiro" visível na tela, não escondido na copy.

Cinco decisões de comportamento e copy ficaram travadas no processo:

| # | Decisão | Por quê |
|---|---|---|
| 1 | **A abertura afirma o número**, não pergunta. "Você já faturou R$ X este ano." | A Regis vê tudo, então entrega valor na primeira mensagem. A pergunta do pitch ("você sabe quanto já faturou?") vira o setup no palco, a afirmação é o payoff na tela. |
| 2 | **Ganho antes do alerta.** A duplicata resolvida vem antes do teto. | Abrir com algo que desarma a ansiedade antes de qualquer coisa que possa assustar. Bate com a força de ansiedade do JTBD. |
| 3 | **Tom do teto neutro e factual.** "Chega no teto", "o imposto muda", não "passa o teto" nem "muda seu regime". | Vago assusta mais que a verdade, o concreto acalma. Fecha na contadora como ajuda pra decidir. |
| 4 | **O padrão do dado define o tom.** Duas cobranças no mesmo dia é fato (resolve). Recorrência parecida é pergunta (engano ou duas assinaturas). | Autonomia proporcional à certeza aplicada antes de falar. Perguntar num caso óbvio soa como falta de confiança. |
| 5 | **A Regis vigia o dinheiro, não a sua ação.** Fecha sozinha quando vê o estorno cair, um toque gentil se nada aparece. | Ela observa o que pode (o dinheiro) e pergunta o que não pode (se você agiu). No produto via Open Finance, no MVP degrada pro botão "Já enviei". |

Consequência de tela, coerente com a leitura 1 de 3.11: a interface principal é uma reconciliação com um número no topo, não um feed de alertas. O alerta é exceção dentro dela.

---

## 4. Decisões que precisam ser tomadas AGORA

A pesquisa deixou quatro perguntas em aberto. Não dá para codar antes de responder.

### Decisão 1 · Quem é o usuário (**FECHADA** pelo resultado-pesquisa-icp)

**MEI com recebimento intermediado e volume alto.** Comércio de bairro, alimentação, salão, seller. Não é prestador de serviço com Pix, e isso foi aprendido em campo, não suposto. Detalhe completo na seção 3.9. A tabela abaixo fica como registro da decisão.


| Opção | A favor | Contra |
|---|---|---|
| **Pessoa física** | Temos 14 entrevistas. Dor real de identificação e recorrência. Fácil gerar dado sintético de fatura. Ana já constrói app financeiro. | Mercado saturado (bancos já fazem push). Anomalia é de baixo valor. Difícil provar ROI. |
| **MEI** | Resolve o impasso PF/PJ. Regra pública, sem configurar nada. Número inédito ("faltam R$ X para o teto"). Narrativa forte e pouco disputada. 570 mil desenquadrados é um argumento de mercado. | Zero entrevista com MEI ainda. Dado fiscal não tem API pública, vamos simular. Tom sensível (imposto e dívida). |
| **PJ / time financeiro** | Onde o brief mais aponta ("despesa que ninguém aprovou"). Volume alto, dinheiro grande. | Quase tudo é *regra* e exige cadastrar política. Três pessoas no fluxo. Impossível em 24h. |

**Recomendação:** **MEI como personagem central**, com o motor de detecção cobrindo também as anomalias comuns a PF (duplicata, recorrência, aumento de preço). Assim aproveitamos as entrevistas de PF e ganhamos a camada fiscal exclusiva do MEI. O demo conta a história de uma pessoa só que vende, recebe por Pix e maquininha, paga tudo no mesmo cartão e não sabe quanto já faturou no ano.

### Decisão 2 · Qual enquadramento

**Recomendação:** **B (julgamento) como coração, com um toque de C (resolução) para as anomalias de fato.**
O autopilot não só avisa. Ele explica o que é a cobrança, diz com que certeza acha que é problema, e, quando é fato, já entrega a ação pronta (texto de contestação, cancelamento, DAS para pagar). A separação fato / regra / suspeita É o produto. Isso responde direto à frase do E13 e ao "imaginei que tivesse feito mesmo" do E12.

Deixamos explicitamente de fora: enquadramento A puro (feed de alertas) e D (auditoria).

### Decisão 3 · Que dados vamos usar no protótipo

**Recomendação:** **extrato sintético em CSV/JSON, gerado por nós, com anomalias plantadas de propósito.** Sem Open Finance ao vivo, sem API da Receita. Ser honesto sobre isso no pitch: "hoje importa CSV ou colagem do extrato; a integração via Open Finance é o próximo passo, e já sabemos que custa R$ 19,90 por conta via Banco MCP sobre a Pluggy". O jurado perdoa dado simulado, não perdoa demo que não roda.

Se sobrar tempo (e só se sobrar): o sandbox da Pluggy é gratuito e sem aprovação. Uma conexão real no sandbox rende um slide de "isso já funciona de verdade". Não é prioridade.

**O dataset precisa refletir o ICP fechado, senão contradiz a nossa própria tese.** A persona **recebe por maquininha e marketplace**, com volume alto. Pix é minoria, não a regra.

O dataset precisa conter, no mínimo:
- 3 meses de movimentações de um MEI fictício com **muitas transações por dia** (maquininha crédito e débito, repasses de marketplace, algum Pix, cartão, DAS, assinaturas, tarifas).
- Anomalias de **fato** plantadas: cobrança duplicada em janela curta, boleto pago duas vezes, assinatura que subiu de preço, serviço cancelado ainda cobrando, DAS pago duas vezes, repasse de marketplace menor que a venda, antecipação automática ligada.
- Anomalia de **regra** fiscal: faturamento acumulado em ritmo de estourar o teto, receita no CPF ligada à atividade, DAS do mês não pago.
- Uma ou duas **suspeitas**: contraparte sem histórico, cobrança fora do dia habitual.

### Decisão 5 · Canal (DECIDIDA)

**O agente mora no chat. O app existe só como apoio.**

**MVP no Telegram, produto final no WhatsApp.** O Telegram tem API de bot gratuita, sem aprovação, criada em 2 minutos pelo BotFather, com botões, envio de foto e PDF. É onde testamos e demonstramos. O WhatsApp é o destino (é onde o ICP vive), e a troca é só de canal: o agente, o motor e as mensagens são os mesmos. No pitch, a demo roda no Telegram e a gente diz isso com clareza.

O ICP (MEI, que controla no caderno ou de cabeça) vive no WhatsApp: é onde vende, onde combina com cliente, onde manda o comprovante. Ele pode nunca abrir o app, e tudo bem. O produto precisa funcionar 100% na conversa.

O que isso muda:
- **Entrada de dados por Open Finance.** O MEI autoriza a leitura da conta uma vez, no próprio banco, e a Regis lê as movimentações sozinha. O agente confere e responde. Nada de mandar arquivo no fluxo principal.
- **Fato, regra e suspeita viram três tons de mensagem**, não três caixas de tela. Fato: "achei isso, já preparei a contestação, quer que eu envie?". Regra: "no ritmo atual você estoura o teto em outubro, te explico as opções?". Suspeita: "esse Pix de R$ 340 para a Maria foi você mesmo?".
- **A resposta do usuário ensina o sistema.** "Foi eu sim" registra a contraparte como conhecida. É assim que o "normal" se constrói na primeira semana, sem tela de configuração.
- **O resumo de tranquilidade vira mensagem periódica.** Toda segunda de manhã, ou todo dia 20 antes do DAS: "conferido, nada pendente, R$ X encontrados este mês".
- **O app é a memória.** Serve para ver o histórico, o acumulado do ano contra o teto, os documentos gerados. Nunca é obrigatório para nada. Se a demo tiver que escolher, o WhatsApp roda e o app vira slide.

### Decisão 4 · Métrica de sucesso

**Recomendação:** **dinheiro encontrado + tempo entre o vazamento e a ação.** Na demo, o resumo final mostra "R$ X recuperáveis encontrados em Y segundos, que ficariam Z meses sem ninguém ver". É o número que o jurado leva embora.

---

## 5. A solução proposta (versão para alinhar, não para fechar)

### O nome
**Regis.** Vem de registro (ela registra tudo) e de gargalo (ela acha onde o dinheiro trava). É o nome do contato no chat, então precisa soar como alguém com quem se conversa.

### A frase de posicionamento (a que abre o pitch)

> **Você sabe quanto já faturou este ano?**

Sem jargão, sem prometer IA. É a promessa que ninguém está usando, e o produto existe para responder isso e o que vem depois.

### Em uma frase
Regis é uma agente no chat (Telegram no MVP, WhatsApp no produto) que lê as movimentações financeiras de quem trabalha sozinho, encontra dinheiro vazando na despesa E na receita, e age de acordo com a certeza: resolve o que é fato, encaminha o que é regra, pergunta o que é suspeita.

### Arquitetura em duas camadas

| Camada | O que é | Obrigatório? |
|---|---|---|
| **Chat (principal)** · Telegram no MVP, WhatsApp no produto | Onde o agente vive. Recebe extrato, print, PDF, comprovante e notificação encaminhada. Avisa, pergunta, redige contestação, cobra o DAS, manda o resumo semanal. | **Sim.** Se só uma coisa funcionar, é essa. |
| **App web (apoio)** | Memória e visão geral: histórico de anomalias, acumulado do ano contra o teto, documentos gerados, contrapartes conhecidas. | Não. O usuário pode nunca abrir. |

### Os três motores de detecção

| Motor | Família | Como detecta | Nível |
|---|---|---|---|
| **Identificação (a peça 1)** | contraparte | Traduz o descritor do extrato em "quem é isso de verdade": nome de fachada, categoria, CNPJ. É pré-requisito dos outros dois e a dor mais citada na pesquisa (6 de 14). | Habilita tudo. É onde o LLM ganha de regex. |
| **Duplicidade e recorrência** | duplicidade · recorrência · valor | Mesma contraparte, mesmo valor, janela menor que 24h. Série mensal de 28 a 31 dias. Assinatura que continua após cancelamento. Cobrança que sumiu. Juro em vencimento que caiu em feriado. | Fato. Regra determinística, sem baseline. |
| **Fiscal MEI** | fiscal · conciliação | Soma tudo que entrou (Pix, maquininha, marketplace, e receita no CPF marcada como atividade). Projeta contra o teto de R$ 81 mil. Verifica DAS pago no mês. Cruza venda com repasse. | Regra pública. Aritmética, sem modelo estatístico. |
| **Entendimento** | contraparte · comportamento | Para cada lançamento não reconhecido, o agente de IA explica quem é o estabelecimento (nome fantasia, categoria, CNPJ) e pergunta antes de alarmar. | Suspeita. Usa LLM para enriquecer e conversar. |

### O que o usuário vê (no chat)

**A primeira mensagem revela um número, não pede configuração.** Antes de qualquer pergunta, a Regis devolve o dado que a pessoa não tinha: "Somei tudo que entrou: você já faturou R$ 58.400 este ano. Faltam R$ 22.600 para o teto do MEI." Só depois vêm os três tons.

Não é um feed de alertas. São três tons de mensagem, e o agente nunca manda mais de uma pergunta por vez:
1. **Fato, tom de "já preparei"**: "Achei a Netflix cobrada duas vezes dia 12 (R$ 55,90). Já escrevi a contestação, é só copiar e mandar para o cartão. Quer ver?" Botões: *Ver texto* / *Foi eu*.
2. **Regra, tom de "você decide"**: "Você já faturou R$ 58 mil este ano. No ritmo atual estoura o teto em outubro. Te mostro as opções?"
3. **Suspeita, tom de pergunta**: "Esse Pix de R$ 340 para Maria Souza, dia 3, foi você mesmo?" A resposta registra a contraparte e o agente não pergunta de novo.

Mais um **resumo de tranquilidade** periódico: "Semana conferida. R$ 210 encontrados, DAS de agosto pago, nada pendente." Responde ao enquadramento D sem virar produto de auditoria.

No app, a mesma informação aparece como histórico e como a barra do ano contra o teto. Nada que só exista lá.

### O que a Regis faz e o que ela nunca faz

**A Regis não move dinheiro.** Não paga, não transfere, não cancela cartão, não contesta direto no banco. Isso é decisão da pessoa e exige acesso que ela não tem nem deve ter. "Agir sozinha" significa fazer o trabalho de conferência, conta e papelada que hoje ninguém faz:

| A Regis faz sozinha | Exemplo |
|---|---|
| **Confere e concilia** | Cruza venda com repasse do marketplace. Bate o DAS pago com o mês. Verifica se a assinatura cancelada parou de cobrar. Quando bate, registra e cala. Quando não bate, avisa. |
| **Soma e projeta** | Faturamento acumulado do ano contra o teto, atualizado toda vez que entra receita. |
| **Prepara o documento** | Contestação escrita, e-mail para o fornecedor, mensagem para o marketplace cobrando o repasse, lista de assinaturas para cancelar. A pessoa só copia ou aperta enviar. |
| **Lembra sem ser pedido** | "DAS vence dia 20 e ainda não vi o pagamento." Resumo de segunda-feira. |
| **Acompanha** | Anota que a contestação foi enviada e cobra se o estorno não cair em 10 dias. |
| **Aprende com a resposta** | "Foi eu" registra a contraparte e ela para de perguntar sobre ela. |
| **Gera relatório** | Mensal, para o contador, para a própria pessoa, para pedido de crédito. |

**Frase para o pitch:** *a Regis não mexe no seu dinheiro. Ela mexe no seu tempo.*

A diferença para o alerta do banco não está em mover dinheiro. O banco diz "compra de R$ 55,90 na Netflix" e para. A Regis diz "a Netflix cobrou duas vezes este mês, aqui está a contestação, e vou conferir se o estorno cai em 10 dias". Vigiou, entendeu, preparou e vai acompanhar.

### Onde entra a IA (e onde não entra)
- **Não entra** na detecção de fato. Isso é código determinístico e é assim que ganhamos confiança.
- **Entra** na leitura do que chega pela conversa (print, PDF, comprovante, texto solto), no entendimento (explicar a cobrança), na conversa (perguntar e absorver a resposta), na redação da ação (contestação, mensagem para o fornecedor) e na priorização do que mandar e quando.

---

## 6. Escopo de 24 horas

### Entregáveis obrigatórios
1. **Agente no Telegram respondendo ao vivo.** Lê a conta conectada (dados simulados no hackathon), roda o motor, manda as mensagens nos três tons, aceita a resposta do usuário e redige uma contestação. Bot via BotFather, orquestrado por n8n ou código direto. A camada de canal fica isolada para virar WhatsApp depois (Meta Cloud API, Evolution API ou Z-API).
2. **Motor de detecção rodando** sobre o dataset sintético, com os três níveis de certeza funcionando.
3. **Agente de IA** lendo print/PDF, explicando ao menos uma cobrança não reconhecida e redigindo ao menos uma contestação.
4. **App web de apoio** (mobile first): histórico, barra do teto anual, documentos gerados. Pode ser protótipo navegável alimentado pelo mesmo motor.
5. **Pitch de 3 a 5 minutos** com demo ao vivo no celular, história de uma pessoa, e os números de mercado conferidos.
6. **Nome e identidade mínima** do produto (o nome é o nome do contato no chat, isso pesa).

### Fora do escopo (dizer isso no pitch, com orgulho)
- Integração real com Open Finance ou Receita Federal.
- Detecção estatística com baseline treinado.
- Fluxo de aprovação multi pessoa (PJ).
- Monetização definida.

### Corte de emergência (se faltar tempo)
Ordem do que cai primeiro: (1) app web vira slide com screenshot, (2) leitura de print/PDF vira CSV colado na conversa, (3) suspeitas saem da demo, (4) Telegram real vira simulador de chat na tela. **O agente conversando, o motor fiscal MEI e a duplicidade não caem.** São o núcleo.

---

## 7. Divisão de trabalho e cronograma

### Papéis

| Quem | Frente | Entrega concreta |
|---|---|---|
| **Kysa** | Motor + agente + canal | Dataset sintético, detectores, agente de IA, bot do Telegram (n8n), endpoint que o app consome. |
| **Ana** | Conversa + app | Roteiro e tom das mensagens (é a interface principal), fluxos de resposta e botões, e o app web de apoio. |
| **Gabriel** | Narrativa + pitch | Personagem da demo, roteiro do pitch, argumento de mercado, slides. Valida números. |
| **Márcio** | Marca + visual + apoio | Nome, identidade, assets, slides finais. Nas horas livres, pareia com Ana no front. |

### Cronograma sugerido (24h a partir do fechamento deste briefing)

| Bloco | Horas | O que acontece |
|---|---|---|
| **0 · Decidir** | 0 a 1h | Fechar as 4 decisões da seção 4. Definir nome provisório. Todos juntos. **Antes de tudo, disparar as mensagens para MEIs:** a Decisão 1 fecha na hora 1 e as entrevistas voltam na hora 3, ou seja, decidimos antes da validação chegar. Ou alguém dispara agora, ou assumimos conscientemente que as respostas são cor para o pitch e não validação. |
| **1 · Fundação** | 1h a 5h | Kysa: bot do Telegram criado e respondendo "oi" (primeira coisa, tira o risco de canal da mesa), depois dataset + detectores de fato. Ana: roteiro de conversa e wireframe do app. Gabriel: personagem e roteiro. Márcio: nome e direção visual. |
| **2 · Construir** | 5h a 13h | Kysa: motor fiscal + agente + leitura de print/PDF. Ana: mensagens finais e telas do app. Gabriel: pitch v1. Márcio: identidade e assets. **Checkpoint na hora 9.** |
| **3 · Integrar** | 13h a 18h | Motor ligado no Telegram e no app. Demo end to end rodando no celular. Gabriel ensaia com o produto real. |
| **4 · Polir** | 18h a 22h | Bugs, copy, animação, slides finais. Ensaio de pitch 2 vezes. Gravar vídeo de backup da demo. |
| **5 · Respiro** | 22h a 24h | Ensaio final, dormir um pouco, não mexer em código. |

**Regra do time:** a partir da hora 18 ninguém adiciona feature. Só conserta.

---

## 8. O pitch (esqueleto para o Gabriel)

1. **Abertura com a pergunta (30s):** "Você sabe quanto já faturou este ano?" Depois a pessoa, que **precisa ser do ICP**: "essa é a [nome], cabeleireira, MEI, aluga uma cadeira num salão e **recebe por duas maquininhas e um marketplace**, dezenas de transações por dia. Ela controla no caderno. Quanto ela faturou esse ano? Ela não sabe. E o que caiu na conta não é o que ela vendeu."
2. **O problema invisível (45s):** 570 mil desenquadrados em 2024, trinta vezes mais que no ano anterior, porque **o Estado começou a cruzar Pix, cartão e transações. O MEI é o único que não cruza os próprios dados.** Cerca de 60% misturam as contas. Todo app vigia o que sai; o vazamento dela está no que entra.
3. **A tese (30s):** fato, regra, suspeita. Autonomia proporcional à certeza. Ninguém faz isso.
3b. **Concorrência em três camadas (20s):** diretos (assumem que ela alimenta o sistema, e ela não alimenta), adjacentes (bancos e adquirentes, nosso canal e nosso risco), e o status quo. Fecha em: **o nosso concorrente não é um app, é o caderno. A barra não é ser melhor que o app X, é dar menos trabalho que o caderno.**
4. **Demo ao vivo no celular (2min):** ela conecta a conta pelo Open Finance (dizer na hora: "no produto final isso é WhatsApp, o agente é o mesmo"). A Regis responde: encontrou R$ X em duplicatas e assinaturas e já preparou a contestação (resolve), avisa que ela estoura o teto em outubro (encaminha), pergunta sobre um Pix estranho e ela responde "foi eu" (pergunta). Fecha no resumo de tranquilidade. O app aparece por 10 segundos como "a memória de tudo isso".

**Três momentos obrigatórios da demo**, porque são os que provam a palavra "autopilot" para o jurado:
- **Ela fala sem ninguém pedir.** O resumo de segunda-feira ou o lembrete do DAS chega sozinho (cron no n8n). Sem isso, parece ferramenta que se abre.
- **Ela fecha algo em silêncio.** "Conferi os 12 repasses da maquininha, 11 bateram, um veio R$ 38 menor, aqui está a mensagem para a adquirente." Mostra que ela trabalhou onde ninguém olhava.
- **Ela mostra algo que achou e escolheu não mandar.** Custa uma linha na tela e prova a tese fato/regra/suspeita melhor que os três alertas juntos. É literalmente o que separa autopilot de relatório agendado.
5. **Próximo passo e viabilidade (30s):** **cuidado com a conta aqui.** Não dizer "o produto se paga com uma duplicata evitada por mês" sem completar o raciocínio: 2 a 3 contas custam R$ 40 a 60/mês de infraestrutura e o FinAI cobra R$ 29,90/mês. Se o jurado fizer a conta, a pergunta seguinte é desconfortável. **Ou tira o número, ou já entra com a conclusão:** "por isso a monetização não é assinatura direta, é distribuição via banco, adquirente ou contabilidade, que já têm o dado e a base." Honestidade sobre o que é simulado e sobre o intermediário não ser oficial.
6. **Fechamento (15s):** a frase de pitch.

---

## 9. Riscos e como lidar

| Risco | Mitigação |
|---|---|
| Número de mercado errado na frente do jurado | Gabriel confere cada número nas fontes do doc de insights antes de fixar no slide. Teto, DAS e obrigações estão em discussão legislativa. |
| Demo quebra ao vivo | Vídeo gravado de backup na hora 20. E um simulador de chat na tela como plano C. |
| Jurado estranhar o Telegram | Dizer de frente: MVP no Telegram porque a API é imediata, o destino é WhatsApp e a troca é só de canal. Mostrar um mock de tela do WhatsApp com a mesma conversa. |
| Bot do Telegram cai ou webhook falha | Conectar na hora 1, não na hora 13. Vídeo de backup e simulador de chat como plano C. |
| Agente vira spam e o MEI silencia o contato | Uma pergunta por vez. Resumo no máximo semanal. Fato e regra mandam na hora, suspeita agrupa e espera. Ana define a cadência. |
| Tom de imposto gera medo em vez de alívio | Ana define o tom: o produto vende tranquilidade e controle, nunca ameaça. Testar as mensagens com alguém de fora. |
| Zero entrevista com MEI | Nas primeiras 3 horas, cada um manda as 5 hipóteses do doc de insights para 2 MEIs conhecidos por WhatsApp. Perguntas prontas: "quanto você já faturou esse ano?" (cronometrar), "por que usa a conta pessoal?", "já conferiu se o valor que caiu bate com a venda?". |
| Feed de alertas por acidente | Se uma tela tiver mais de 5 itens sem hierarquia de certeza, está errada. |
| A demo exigir digitação e perder para o caderno | Regra dura: no fluxo principal, o único gesto permitido é conectar a conta uma vez pelo Open Finance. Nada de cadastrar categoria, contraparte ou valor. Se a demo travar esperando alguém digitar, o posicionamento caiu junto. |
| Vender IA em vez de vender o número | O pitch abre com "você sabe quanto já faturou este ano?". A palavra autopilot aparece depois, explicando o mecanismo. Nunca antes. |
| Custos de Open Finance vêm de relatos no TabNews, não de tabela oficial | Citar como "relatos de desenvolvedores" e não como preço de tabela. Se der, abrir o sandbox da Pluggy e perguntar ao suporte. |
| **"Vocês entrevistaram o público errado"** | Resposta pronta: entrevistamos quem estava ao alcance em 24h, **e o resultado nos disse com clareza quem não é o cliente**. A tese sobre o público-alvo se apoia em dados secundários e está marcada como não validada em campo. Essa é a primeira coisa que faríamos na segunda-feira. É mais forte que fingir que quinze respostas de Pix validaram um produto para maquininha. |
| Inflar o número da pesquisa | Nunca "a pesquisa mostra". Sempre **"nas seis conversas que tivemos"**. |
| **"Por que isso não é só uma feature do ALL?"** | A pergunta mais provável do jurado. Resposta decorada na seção 3.9: orçar e vigiar são trabalhos diferentes, o ALL é assistivo e é um produto que você abre, e não tem nada de fiscal do MEI. |
| Parte da amostra vem da rede pessoal do time | Pesquisa de conveniência em 24h é isso, não é problema. Mas "14 pessoas" e "nossas famílias" têm pesos diferentes. **Ter a resposta pronta e não deixar o jurado descobrir sozinho.** |
| Um terço da amostra não é cliente | E9, E10, E7, E5 e E6 têm dor baixa ou nenhuma (E6 nem cartão tem). **A banca vai encontrar. Melhor sermos nós a dizer.** |
| Vender fraude e perder para o banco | Fraude não entra no pitch como diferencial. O banco pega primeiro e antifraude de emissor é maduro. |
| "E daí?": mostrar a anomalia sem oferecer a ação | É a morte do Guiabolso repetida. Toda anomalia na demo vem com a ação do lado. |
| Falar como banco | "Achei R$ 47 por mês saindo à toa", nunca "detectamos outlier no cluster 3". |
| LGPD e confiança | Dado financeiro é o mais sensível que existe. Ter resposta de 20 segundos sobre consentimento, escopo e não compartilhamento. |
| Dados identificados das entrevistas vazando | O relatório das 14 conversas tem nomes e bancos. Não sobe em repositório público, não vai em slide sem anonimizar. |

---

## 10. Referências internas

Pasta `pesquisa do grupo/`:
- `enquadramento-problema.html` · ciclo do vazamento, 4 enquadramentos, decisões em aberto.
- `catalogo-anomalias.html` · catálogo PF e PJ, eixos tipo e certeza.
- `catalogo-anomalias_mei.html` · mesmo catálogo com o bloco MEI e a família fiscal.
- `insights-mei.html` · números de mercado, resolução CGSN 183/2025, hipóteses e fontes.
- `relatorio-pesquisa-14-conversas.html` · 14 entrevistas PF, dados identificados, tratar com cuidado.
- `custo-por-conta.html` · custo por conta bancária via Open Finance (Pluggy, Belvo, Banco MCP), calculadora por usuário, benchmark Plaid.
- `DOSSIE.md` · todos os fatos com status de verificação (✅ verificado, ⚠️ não verificado, ❌ com erro), as 14 fichas completas, números agregados e ressalvas. **É a fonte de verdade para qualquer número que for para o slide.**
- `INSIGHTS.md` · conclusões, o que caiu, concorrentes, frases para o pitch e problemas práticos.
- `resultado-pesquisa-icp.html` · resultado das 5 hipóteses, o ICP redefinido por exclusão e as regras para não estragar o argumento.
- `pesquisa-mei-teto-invisivel.html` · dossiê do teto de R$ 81 mil: as três faixas de desenquadramento, a cadeia de cinco elos que impede a soma, a virada de fiscalização (e-Financeira desde jan/2026) e as cinco leituras para o produto. **É o documento que define o que é anomalia para o MEI.**
- `roteiro-campo-salao.md` · roteiro de 5 perguntas para conversa presencial com salão ou barbearia.
- `posicionamento.html` · níveis de consciência, estágios de sofisticação, concorrentes em três camadas e as 5 decisões de comunicação.
- `respostas-forms.md` · respostas do forms com MEIs, anonimizadas e resumidas. Regerar com `python3 "pesquisa do grupo/respostas-forms/gerar-markdown.py"` depois de salvar o CSV novo na pasta `respostas-forms/`. O CSV bruto não circula.

---

## 11. Estado da construção

Atualizado em 29/08/2026, 20h.

| Frente | Estado | Onde |
|---|---|---|
| **Dataset sintético** | ✅ pronto e validado | `dados/` |
| **Prévia de UI (5 telas anotadas)** | ✅ pronto | `ui/regis-telas.html` |
| **App navegável (responsivo, claro e escuro)** | ✅ pronto | `ui/regis-app.html` |
| **Conversa animada (hero, layout WhatsApp)** | ✅ pronto | `ui/regis-conversa.html` |
| **Motor de detecção** | 🔨 em construção | `motor/` |
| **Bot do Telegram** | 🔨 em construção | `bot/` |
| **Deck e pitch** | ⬜ não começou | |
| **Identidade visual** | ⬜ não começou | |

### O dataset (o que a demo vai usar)

Persona do ICP: **Angela Nogueira, cabeleireira MEI**. Ela **não é dona de salão**, aluga uma cadeira no Studio Bella e atende a própria clientela, então a conta que a Regis lê é só dela. **Maquininha e marketplace**, Pix como minoria (8%). 367 transações entre junho e agosto de 2026, 337 vendas, ticket médio de R$ 84.

**Faturamento acumulado de R$ 58.400** (72,1% do teto), faltam R$ 22.600, projeção de estouro em **24/10**. Esse é o número que abre a conversa e que o anel do app mostra.

Detalhe que importa para o pitch: o teto do MEI é sobre **receita bruta**, então os R$ 58.400 são o que foi vendido, não o que caiu na conta (R$ 26.996 líquidos no trimestre). A diferença entre esses dois números é literalmente o produto.

**12 anomalias plantadas**, com gabarito em `dados/anomalias-esperadas.json`:
- **8 de fato**, somando **R$ 1.145,15 recuperáveis**: boleto pago duas vezes, assinatura duplicada, assinatura cobrando após cancelamento, reajuste silencioso, repasse do marketplace R$ 38 curto, DAS pago duas vezes, antecipação automática (R$ 312 no trimestre), tarifa de conta PJ que deixou de ser isenta.
- **2 de regra**: teto em outubro, taxa efetiva de 3,49% contra 2,89% contratados.
- **2 de suspeita**: Pix de R$ 340 para contraparte sem histórico, Pix às 3h41 de domingo.

O gabarito traz também **6 falsos positivos esperados** (aluguel, química de R$ 380, pico de sábado, DAS mensal normal, taxa que bate com o contrato, Pix único para o supermercado). São eles que alimentam a linha "outros 6 achados ficaram de fora, são normais para o seu histórico", que é o momento em que o agente mostra que escolheu ficar calado.

---

*Documento vivo. Atualizar a seção 4 assim que as decisões forem fechadas.*
