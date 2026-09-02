---
titulo: Visão de futuro da Regis
tipo: visao
status: proposta para o time
atualizado: 2026-08-30
autor: Time 12 · Hackathon Vanguarda
resumo: Para onde a Regis caminha depois das 24 horas. O ativo que ela constrói, a métrica do norte, cinco horizontes, o que nunca muda e onde a visão pode morrer.
---

# VISÃO · Para onde a Regis caminha

Documento de proposta, não de decisão fechada. Nasce do `BRIEFING.md` e não reabre nada que já está travado lá. Os números e as afirmações de mercado usados aqui estão verificados em fonte pública no `ESTUDO-MERCADO.md`, que também registra o que continua sem prova.

---

## A visão em uma linha

> **Que ninguém seja o último a saber do próprio dinheiro.**

Antes da Receita, antes do banco, antes da contadora, antes da fatura fechar. A pessoa que trabalha sozinha deveria ser a primeira a saber o que está acontecendo com o dinheiro dela, e hoje ela é a última.

---

## 1. O ativo que a Regis constrói (e que ninguém tem)

Vale separar o que é feature do que é ativo. Detecção de duplicata é feature, qualquer um faz. O ativo é outro:

> **A receita bruta reconciliada de quem trabalha sozinho.**

Ninguém tem esse número inteiro hoje.

| Quem | O que enxerga | O que falta |
|---|---|---|
| O banco | uma conta | as outras portas, e o bruto (a maquininha deposita líquido) |
| A adquirente | um canal | o resto do faturamento |
| O marketplace | as vendas dele | tudo o mais |
| A contadora | as notas emitidas | o que entrou sem nota |
| A Receita | fragmentos cruzados de Pix e cartão | contexto, e ela não devolve o número para a pessoa |
| **A própria pessoa** | **o saldo** | **o acumulado** |

O saldo é o que sobrou. O teto é sobre o que entrou. São números diferentes e é por isso que 13 de 15 respondentes acompanham de perto e 14 de 15 não sabem dizer a distância até o teto.

A Regis é o primeiro lugar onde esse número existe inteiro, com autorização da pessoa, do lado dela. Todo o resto da visão é consequência disso.

---

## 2. A métrica do norte: tempo até saber

A fórmula que saiu da pesquisa vale como bússola de produto:

```
custo do vazamento = valor da cobrança × meses até alguém perceber
```

A Regis não muda o valor. Ela muda o tempo. E a evolução do produto é a evolução desse tempo:

| Estágio | O que a Regis faz | Tempo até saber |
|---|---|---|
| Hoje, sem produto | a pessoa descobre na declaração de maio, ou quando a Receita avisa | 3 a 12 meses |
| **Contar o passado** | soma o que já entrou e devolve o acumulado do ano | dias |
| **Narrar o presente** | fala sozinha quando o dinheiro se mexe, sem ninguém abrir nada | imediato |
| **Avisar o futuro** | projeta o estouro do teto para outubro em pleno agosto | negativo |

A projeção do teto já é o terceiro estágio funcionando na demo. É a prova de que a direção não é hipótese.

**A pergunta que guia cada decisão de roadmap:** isso encurta o tempo entre o dinheiro se mexer e a pessoa saber? Se não encurta, não entra.

---

## 3. Como o autopilot amadurece: a fronteira da certeza

A tese é autonomia proporcional à certeza. Fato ela resolve, regra ela encaminha, suspeita ela pergunta. A visão é o que acontece com essa fronteira ao longo do tempo.

> **A Regis não fica mais autônoma porque ficou mais corajosa. Ela fica mais autônoma porque as coisas atravessam a fronteira da certeza.**

Uma contraparte perguntada uma vez vira contraparte conhecida. Uma resposta de "foi eu" vira histórico. Um padrão de repasse observado por três meses vira régua. O que era suspeita vira regra, o que era regra vira fato, e a Regis passa a resolver sozinha o que antes precisava perguntar.

A consequência é a métrica de qualidade menos óbvia e a mais importante do produto:

> **A medida de maturidade da Regis não é quantos alertas ela manda. É quantos ela deixou de precisar mandar.**

No dataset da demo isso já aparece: 6 falsos positivos que ela escolhe não mostrar. Em um ano de uso, essa lista precisa ser muito maior que a de alertas. Um autopilot que fala mais a cada mês está piorando.

---

## 4. Os cinco horizontes

| | Horizonte | A pergunta que ele responde |
|---|---|---|
| **H0** | Hoje, a demo | O número existe e dá para entregar sem configuração? |
| **H1** | 90 dias | Funciona com dado real e com o ICP de verdade? |
| **H2** | Ano 1 | Dá para reconciliar as quatro portas, não só a conta? |
| **H3** | Anos 2 e 3 | A Regis atravessa o teto junto com a pessoa? |
| **H4** | Destino | Todo mundo que trabalha sozinho vê sobre si o que o Estado já vê. |

### H0 · Hoje: uma conversa que revela um número

Angela, cabeleireira MEI, maquininha e marketplace, 367 transações em três meses. A Regis abre afirmando R$ 58.400 faturados e R$ 22.600 até o teto, entrega R$ 1.145,15 recuperáveis, avisa do estouro em 24/10 e fica calada sobre seis coisas normais. Dados simulados, Telegram, declarado no palco.

**O que este horizonte prova:** que o número pode ser entregue na primeira mensagem, sem onboarding, sem cadastro, sem a pessoa alimentar nada.

### H1 · Os primeiros 90 dias: trocar o simulado pelo real

Três trocas, em ordem:

1. **Dado real.** Open Finance em produção. O caminho já está mapeado e custeado (R$ 19,90 por conta via Banco MCP sobre a Pluggy, sandbox gratuito e sem aprovação). Primeira tarefa técnica: falar direto com a licenciada, porque hoje dependemos de um intermediário não oficial.
2. **Canal real.** WhatsApp no lugar do Telegram. A camada de canal já está isolada por decisão de arquitetura, então é troca, não reconstrução.
3. **ICP real.** 20 MEIs de salão, comércio de bairro e seller.

O terceiro item não é ambição, é **dívida da nossa própria pesquisa**. A hipótese central, a de que o valor que cai na conta não é o valor que foi vendido, é a única que o forms não conseguiu testar: 13 de 15 respondentes recebem por Pix, que cai inteiro e não tem repasse para conferir. Enquanto isso não for a campo, a tese do repasse é boa argumentação e não é evidência.

**O número que este horizonte precisa produzir:** a taxa de acerto do motor contra extrato real, não contra um gabarito que nós mesmos plantamos.

### H2 · Ano 1: reconciliar as quatro portas

Ler a conta bancária resolve uma porta de quatro. O faturamento bruto não mora lá.

| Porta | Onde o bruto está | O que falta construir |
|---|---|---|
| Maquininha | na adquirente, a conta recebe líquido | integração de lojista, para reconstruir a venda a partir do repasse |
| Marketplace | no painel do seller, com retenção e prazo | leitura do lado da venda |
| Pix | cai inteiro na conta, mas se divide entre a chave do CPF e a do CNPJ | deixou de ser o caso fácil: desde a Resolução CGSN 183/2025 a receita no CPF soma no limite |
| Espécie | em lugar nenhum | **ponto cego assumido** |

**Este horizonte ficou maior do que o briefing supunha.** 97% dos MEIs usam Pix e para 28% deles o Pix é mais de três quartos do faturamento (Sebrae, Hábitos Financeiros 2025). O perfil que o nosso forms encontrou por acaso, o MEI que recebe por Pix, passou a ser em janeiro de 2026 o de maior risco fiscal, porque o que entra no CPF agora conta para o teto e a e-Financeira reporta a movimentação todo mês. A reconciliação de repasse continua sendo diferencial, mas o alicerce é a soma multiporta contra a régua legal, que serve a quase todo MEI.

O dinheiro em espécie não tem trilha e não vai ter. A resposta da Regis não é fingir precisão, é declarar a margem: "do que passa por conta e maquininha, você faturou R$ X. O que entrou em espécie eu não vejo." **Um produto que informa o tamanho do que não sabe é mais confiável que um que arredonda.**

E entra aqui a consequência do achado dos dois usuários: metade dos MEIs da amostra não faz a parte fiscal, quem faz é a esposa, a contadora da família, alguém. **A segunda pessoa vira superfície do produto**, com o relatório mensal indo sozinho para quem organiza, sem o MEI precisar montar nada. Nenhum concorrente trata a conta como coisa de duas pessoas, e provavelmente é a segunda pessoa quem abre.

### H3 · Anos 2 e 3: a travessia

Todo produto para MEI trata o crescimento do cliente como churn. Ele cresce, vira ME, sai do app.

A Regis inverte isso, e essa é a parte mais valiosa da visão. O teto não é um muro, é uma porta que 570 mil pessoas atravessaram só em 2024, quase todas de surpresa e retroativamente. Quem tem o material que essa travessia exige? Só quem acompanhou o ano inteiro transação a transação.

> **O produto deixa de ser sobre não estourar o teto e passa a ser sobre estourar no controle. Crescer sem susto.**

Isso estica o ICP para cima sem trair a tese: o ME no Simples tem exatamente o mesmo problema de apuração, com uma régua diferente. E cria o momento de maior valor do produto justamente onde hoje existe o maior abandono.

Há validação comercial disso fora de casa: a Contabilizei tem mais de 100 mil clientes, **não atende MEI**, e organiza o funil justamente em torno da migração de MEI para ME. Alguém já construiu um negócio de escala em cima desse momento. A diferença é que a contabilidade recebe a pessoa na hora da travessia, sem histórico, e a Regis chega com o ano inteiro reconciliado.

**A adjacência tentadora, com trava.** Faturamento bruto reconciliado é precisamente o documento que falta para o MEI provar renda e conseguir crédito. É uma expansão óbvia e é perigosa: no dia em que a Regis empurrar empréstimo, ela vira comercial de banco e a pessoa para de acreditar no número. Se um dia acontecer, é laudo emitido a pedido da pessoa, nunca oferta.

### H4 · O destino: o espelho do algoritmo

O que mudou no Brasil não foi a regra, foi a capacidade do Estado de enxergar.

Desde 1º de janeiro de 2026 a e-Financeira reporta a movimentação mensal consolidada de PJ acima de R$ 6.000 (IN RFB 2.278/2025). O teto do MEI equivale a R$ 6.750 por mês. Na prática, **quase todo MEI que chega perto do limite já é reportado todos os meses.** Ele vê o próprio número uma vez por ano, em maio, quando já não dá para fazer nada.

> **O Estado começou a cruzar os dados do MEI. O MEI é o único que não cruza os próprios dados.**

A assimetria de informação entre o Estado e a pessoa nunca foi tão grande quanto agora, e ela só aumenta. A visão é fechá-la pelo lado de baixo, para 12,9 milhões de MEIs ativos, 78% de todas as empresas abertas em 2026, e depois para quem trabalha por conta sem sequer ter CNPJ.

Não é dar mais dado a quem já tem. É devolver à pessoa a visão que já existe sobre ela.

---

## 5. Como isso vira negócio

A conta direta não fecha hoje e é melhor dizer isso do que fingir. Dois a três contas por usuário custam R$ 40 a 60 por mês de infraestrutura, e o concorrente manual cobra R$ 29,90.

**E aqui o estudo de mercado trouxe a notícia desconfortável.** A Magie já tem mais de 150 mil clientes, processou mais de R$ 3 bilhões, responde por 1% das transações Pix via Open Finance e hoje vende o MagieOS como plataforma whitelabel de agentes financeiros no WhatsApp para bancos, fintechs e varejistas. A posição de camada conversacional embarcada já tem ocupante financiado.

A diferença é limpa, e é a nossa constante número 1:

> **A Magie move dinheiro, é o que ela faz. A Regis não move, e é por isso que ela pode fazer a única coisa que a Magie não faz, que é apuração.**

Então a Regis não disputa ser a camada conversacional. Ela é a **camada de apuração**, e pode rodar dentro da Magie, do Cora ou do Asaas. Concorrente de canal, nesse desenho, é distribuidor.

O caminho é **camada, não app avulso**. Banco, adquirente e contabilidade digital já têm o dado e já têm a base. Falta a eles uma competência que não é de dado, é de produto: falar primeiro, no tom certo, e ficar calado na hora certa. Isso é o que a Regis sabe fazer.

Entra a movimentação, sai a conversa. O parceiro põe a marca dele. Três formas de cobrar, para testar em H1 e H2: por conta conectada (com o custo de origem como piso), success fee sobre o valor recuperado, ou embutida na oferta do parceiro.

E é a resposta honesta para a pergunta "por que o banco não faz isso?": provavelmente vai fazer, e o caminho mais curto é ele fazer conosco.

---

## 6. O que nunca muda

Uma visão só é confiável se tiver constantes. São quatro, e nenhuma delas é negociável em nenhum horizonte:

1. **A Regis não move dinheiro.** É o que torna o acesso aceitável. No dia em que ela pagar, transferir ou contestar sozinha, ela vira uma instituição financeira e perde a única coisa que o produto tem de verdade, que é confiança.
2. **Ela fala primeiro.** Um autopilot que espera ser aberto é um relatório agendado. É a linha que separa a Regis de todo concorrente que não seja o banco.
3. **Zero entrada manual no fluxo principal.** A barra nunca foi o app X, é o caderno. Uma autorização única de leitura é aceitável, alimentar sistema não é.
4. **Ela nunca ajuda a esconder faturamento.** A Regis mede o dinheiro que entra, não o que foi declarado. Diante de um estouro ela mostra o número, explica o que muda e encaminha para a contadora. Segurar nota, atrasar recebimento ou dividir entrada está fora, pelo mesmo motivo que mover dinheiro está fora.

---

## 7. Onde a visão pode morrer

| Risco | O que fazemos a respeito |
|---|---|
| **A adquirente ou o banco faz primeiro** | É o cenário mais provável, e por isso distribuição é o plano e não a ameaça. Perdemos se insistirmos em ser aplicativo avulso brigando por download. |
| **O teto muda por lei** (PLP 67/2025, aprovado em comissão, quer R$ 150 mil com correção pelo IPCA) | Mesmo que passe, muda o número da régua e não o trabalho. E a régua está se multiplicando, não sumindo: a CGSN 183/2025 mandou somar o CPF, a e-Financeira começou a reportar mês a mês em 2026, o MEI passa a preencher campos de IBS e CBS em 2027, nasce o nanoempreendedor com limite de R$ 40,5 mil, e o Simples ganha um regime híbrido opcional. **De 2026 a 2029 o MEI ganha mais réguas e mais decisões.** |
| **A conexão de dado quebra** | Hoje dependemos de um revendedor não oficial. Tarefa de H1: relação direta com a licenciada, e uma segunda fonte mapeada. |
| **Virar mais um app que notifica** | A métrica de maturidade é quantos alertas ela deixou de mandar. Regra dura já valendo: tela com mais de 5 itens sem hierarquia de certeza está errada. |
| **O produto acerta e ninguém paga** | É o risco real de um público em nível 2 de consciência: quem não formulou o problema não procura solução. A resposta é distribuição, não aquisição. |
| **O canal deixar de ser diferencial** (já deixou) | Magie e Jota provam que agente financeiro no WhatsApp é infraestrutura, não ideia. Não competimos por canal nem por LLM, competimos pelo trabalho feito dentro dele. Se a resposta ao "por que não é só uma feature da Magie" não estiver pronta, perdemos a pergunta no palco. |
| **A tese do repasse não se confirmar em campo** | Então o produto é reconciliação de receita e teto, que continua de pé sozinho, e o ICP se alarga em vez de estreitar. Perdemos um diferencial, não o produto. |

---

## 8. O que a visão não é

Para não inventar produto durante o pitch:

- **Não é virar banco nem conta digital.** Cai na constante 1.
- **Não é contabilidade.** A Regis não emite nota e não substitui a contadora. A contadora é usuária, não concorrente.
- **Não é app de orçamento.** Orçar e vigiar são trabalhos diferentes. Orçamento pressupõe que alguém vai abrir.
- **Não é um feed de alertas com IA.** Esse produto já existe, chama-se notificação de banco, e morre de fadiga.

---

## 9. A visão em 30 segundos, para o palco

> Hoje a Regis conta o passado de uma pessoa. Em 90 dias ela lê conta real e fala no WhatsApp. Em um ano ela reconcilia as quatro portas por onde o dinheiro entra e manda o relatório para a contadora sozinha. Em três anos ela atravessa junto a saída do MEI, que é hoje o momento em que 570 mil pessoas por ano são pegas de surpresa.
>
> E o destino é este: desde janeiro de 2026 a Receita acompanha mês a mês a movimentação de quase todo MEI que se aproxima do teto. A pessoa acompanha uma vez por ano, em maio. A Regis existe para acabar com essa diferença.
>
> Ela não vai mexer no dinheiro de ninguém. Ela vai fazer com que ninguém seja o último a saber do próprio.

---

*Documento vivo. Os horizontes H1 e H2 viram plano de execução assim que o hackathon fechar.*
