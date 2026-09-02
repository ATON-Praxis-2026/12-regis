---
titulo: Roadmap de features
tipo: produto
status: proposta para o time
atualizado: 2026-08-30
autor: Time 12 · Hackathon Vanguarda
resumo: As features que constroem cada horizonte da visão, o filtro que toda feature precisa passar, o que fica de fora de propósito e as três decisões que o roadmap não pode tomar sozinho.
---

# ROADMAP · as features que constroem a visão

Deriva de `VISAO.md` e `ESTUDO-MERCADO.md`. Cada feature aqui existe para empurrar um horizonte específico. Feature que não empurra nenhum não entra, por melhor que pareça.

---

## O filtro de entrada

Antes de discutir prioridade, toda feature responde quatro perguntas. **Falhou uma, não entra.**

| # | A pergunta | Por que ela existe |
|---|---|---|
| 1 | **Encurta o tempo entre o dinheiro se mexer e a pessoa saber?** | É a métrica do norte. O produto não muda o valor da cobrança, muda o tempo. |
| 2 | **Nasce com nível de certeza declarado?** | Fato a Regis resolve, regra ela encaminha, suspeita ela pergunta. Feature sem nível vira feed de alertas. |
| 3 | **Respeita as quatro constantes?** | Não move dinheiro, fala primeiro, zero entrada manual no fluxo principal, nunca ajuda a esconder faturamento. |
| 4 | **Funciona sem a pessoa abrir nada?** | O usuário pode nunca abrir o app. Se a feature só existe em tela, ela não existe. |

---

## H0 · O que já está de pé

Não é promessa, é código no repositório. Serve de base e de honestidade: o roadmap começa daqui, não do zero.

| Peça | Onde | Nível que produz |
|---|---|---|
| Identificação de contraparte (descritor bruto vira quem é de verdade, com regras de gateway, imposto, tarifa e antecipação) | `motor/identificar.py` | habilita tudo |
| Duplicidade em janela curta | `motor/duplicidade.py` | fato |
| Recorrência, assinatura fantasma e cancelamento não honrado | `motor/recorrencia.py` | fato |
| Reajuste silencioso e desvio de valor | `motor/valor.py` | fato |
| Conciliação de venda contra repasse | `motor/conciliacao.py` | fato |
| Motor fiscal: acumulado, projeção de estouro, DAS por competência | `motor/fiscal.py` | regra |
| Suspeita com contraparte sem histórico | `motor/suspeita.py` | suspeita |
| Silenciamento do que já foi respondido | `motor/detectar.py` | aprendizado |
| Agente conversacional, memória e registro | `bot/conversa_ia.py`, `bot/registro.py` | canal |

**O que falta aqui e é dívida imediata:** os limiares (24 horas para duplicidade, 28 a 31 dias para recorrência) nunca foram testados contra dado real. Enquanto isso não acontecer, a precisão do motor é uma suposição bem informada.

---

## H1 · Os primeiros 90 dias: trocar o simulado pelo real

O horizonte responde "funciona com dado real e com o ICP de verdade?". Nenhuma feature nova de produto aqui é enfeite: são as que tiram o risco de morte.

### P0, sem isso nada mais importa

**1. Conexão Open Finance de verdade**
Consentimento, renovação antes de vencer, múltiplas contas por pessoa, tratamento de conta que caiu. *Nível: infraestrutura.* *Destrava: todo o resto.*
Cuidado registrado: hoje o custo conhecido vem de revendedor não oficial. A primeira tarefa é relação direta com a licenciada e uma segunda fonte mapeada.

**2. Importação dos 12 meses retroativos na conexão**
O Open Finance entrega histórico. Puxar tudo no momento do consentimento é o que permite a Regis **abrir afirmando um número na primeira mensagem**, em vez de pedir paciência por três meses. *Nível: fato e regra.* *Destrava: acumulado do ano real, recorrência com série de verdade, e a resposta à pergunta que ninguém resolve, o que é normal no dia 1.*
É a feature de maior retorno do horizonte inteiro e a mais fácil de esquecer.

**3. Canal WhatsApp**
Meta Cloud API no lugar do Telegram. A camada de canal já está isolada por decisão de arquitetura, então é troca e não reconstrução. *Nível: canal.* *Sustenta: 82% dos MEIs vendem por WhatsApp.*

**4. Orçamento de fala**
Limite duro de quantas mensagens a Regis manda por semana, uma pergunta por vez, fato e regra na hora, suspeita agrupada e adiada. *Nível: comportamento.* *Existe para: o produto morrer de fadiga é o risco número 1 de um autopilot.*

### P1, no mesmo horizonte

**5. Contraparte aprendida com persistência por pessoa**
Hoje o silenciamento existe dentro de uma execução. Vira memória durável: "foi eu" nunca é perguntado duas vezes. *Nível: aprendizado.*

**6. Painel de precisão interno**
Taxa de acerto e de falso positivo do motor contra extrato real, por detector. Não é feature de usuário, é o instrumento que diz se podemos aumentar autonomia. *Sem isso, mover coisas de suspeita para fato é chute.*

**7. Resumo de tranquilidade**
Mensagem periódica de "conferido, nada pendente, R$ X encontrados". *Nível: comportamento.* *Existe para: responder à ansiedade sem virar alerta.*

---

## H2 · Ano 1: reconciliar as quatro portas

O horizonte responde "dá para somar o faturamento inteiro, e não só o que passou pela conta?".

**8. Reconciliação de adquirente**
Ler o lado da venda pela API de lojista e cruzar com o repasse que caiu. Reconstrói o **bruto a partir do líquido**, que é o número que nem a planilha nem o app do banco têm. *Nível: fato.* *Ressalva honesta: é a tese que nunca foi a campo. Esta feature é o teste dela.*

**9. Reconciliação de marketplace**
Mesma lógica, com retenção e prazo de repasse. *Nível: fato.*

**10. Receita de atividade no Pix do CPF**
Desde a Resolução CGSN 183/2025 o que entra no CPF conta para o teto. A Regis precisa separar venda de dinheiro pessoal **sem pedir categorização**: infere pelo padrão (valor recorrente de cliente, contraparte que já comprou, horário comercial) e pergunta uma vez quando não tem certeza. *Nível: suspeita que vira regra.* *É a feature que atende os 97% de MEIs que usam Pix, e não só o ICP de maquininha.*

**11. Declaração de margem**
A Regis diz o tamanho do que ela não vê: "do que passa por conta e maquininha, você faturou R$ X. O que entrou em espécie eu não vejo." *Nível: comportamento.* *Existe para: um produto que informa a própria margem de erro é mais confiável que um que arredonda.*

**12. A segunda pessoa vira superfície**
Relatório mensal que vai sozinho para quem organiza (esposa, contadora), e acesso próprio para essa pessoa. *Nível: saída.* *Sustenta: metade da amostra não faz a parte fiscal, outra pessoa faz. Nenhum concorrente trata a conta como coisa de duas pessoas, e provavelmente é a segunda que abre.*

**13. Preparação da DASN**
Montar a declaração anual com o número reconciliado, pronta para conferência. **Preparar, nunca enviar.** *Nível: regra.*

**14. Auditoria do silêncio**
Registro do que a Regis achou e escolheu não mandar, com o motivo. Vira a linha "outros 6 achados ficaram de fora, são normais para o seu histórico". *Nível: comportamento.* *É a materialização da métrica de maturidade: quantos alertas ela deixou de precisar mandar.*

---

## H3 · Anos 2 e 3: a travessia

O horizonte responde "a Regis atravessa o teto junto com a pessoa, em vez de perdê-la ali?".

**15. Simulador de travessia**
"Se você fechar o ano em R$ X, isto muda no seu imposto." Comparativo entre continuar MEI, estourar até 20% e estourar acima. *Nível: regra.* *Nunca sugere segurar nota ou atrasar recebimento.*

**16. Dossiê de desenquadramento**
O ano inteiro reconciliado, transação a transação, no formato que a contadora precisa para fazer a migração. *Nível: regra.* *É a vantagem estrutural: a contabilidade recebe a pessoa sem histórico, a Regis chega com o ano completo.*

**17. Régua parametrizável**
O motor fiscal deixa de conhecer um teto e passa a conhecer **um conjunto de réguas**: MEI, nanoempreendedor (R$ 40,5 mil, a partir de 2027), ME e EPP no Simples. *Nível: regra.* *Sustenta: entre 2026 e 2029 as réguas se multiplicam, e é isso que protege o produto se o teto subir para R$ 150 mil.*

**18. Acompanhamento pós migração**
A pessoa vira ME e a Regis continua, com régua nova e obrigações novas (nota fiscal com campos de IBS e CBS a partir de 2027, decisão do regime híbrido). *Nível: regra.*

**19. Laudo de faturamento, com trava**
Documento de receita bruta reconciliada, emitido **a pedido da pessoa**, para quando ela precisar provar renda. *Nível: fato.* *Trava dura: a Regis nunca oferece crédito, nunca encaminha para banco, nunca recebe por indicação. No dia em que empurrar empréstimo, ela vira comercial de banco e o número perde credibilidade.*

---

## H4 · Destino: a camada de apuração

O horizonte responde "a Regis roda dentro de quem já tem a base?".

**20. API de apuração**
Entra movimentação, sai o número, os achados com nível de certeza e os documentos. Sem interface, sem marca. *Nível: infraestrutura.*

**21. Conversa embarcada**
O parceiro (banco, adquirente, contabilidade) põe a marca dele na conversa. *Ressalva do estudo de mercado: a posição de camada conversacional já tem ocupante financiado. Nós não disputamos o canal, disputamos o trabalho. Uma integração dentro do Jota ou da Magie é vitória, não derrota.*

**22. Multi régua e multi regime**
O mesmo motor servindo MEI, nanoempreendedor, ME e EPP, porque o parceiro tem a base inteira e não só um recorte.

---

## H4 em detalhe · a API de apuração

O H4 é o único horizonte em que o produto muda de forma: deixa de ser algo que uma pessoa usa e passa a ser algo que uma empresa embute. Por isso ele merece mais do que três linhas. O contrato completo, campo a campo, está em `pesquisa do grupo/api-de-apuracao.html`. Aqui fica o que decide, não o que implementa.

### O que a API vende

A tentação é vender detecção, e detecção é commodity: todo mundo usa IA, o ALL já classificou mais de um milhão de transações, e conectar e classificar virou infraestrutura de mercado.

> **A API não vende detecção. Ela vende apuração: entra movimentação, sai um número com consequência legal.**

A resposta tem seis blocos, e dois deles são os que valem dinheiro:

| Bloco | O que é | Por que importa |
|---|---|---|
| `numero` | acumulado, régua, distância, projeção e **cobertura** | a cobertura declara o que não foi observado, em vez de arredondar |
| `achados` | com nível de certeza, evidência e ação | é a parte que qualquer um copia |
| `silenciados` | o que foi achado e calado, com o motivo | a auditoria do silêncio, feature 14 |
| **`fala`** | o que dizer agora, o que guardar, o que nunca dizer | **achar é fácil, saber calar é o produto** |
| `documentos` | contestação, dossiê, DASN | preparados, nunca enviados |
| **`auditoria`** | versão do motor e **versão da régua** | apuração é cálculo legal, precisa ser reproduzível |

**Sobre o bloco `fala`:** um parceiro que integrar só os `achados` recria um feed de alertas e mata o próprio NPS em duas semanas. A política de comportamento embalada é o que impede isso, e é a diferença entre vender um detector e vender um autopilot.

**Sobre versionar a régua:** em 2029 alguém vai precisar recalcular 2026 com as regras de 2026, não com as de 2029. Isso exige guardar a versão da régua junto com o resultado. E é também o fosso comercial mais durável que temos: **manter régua fiscal atualizada é trabalho chato, contínuo e que ninguém quer ter dentro de casa.** Entre 2026 e 2029 ela muda várias vezes.

### Quem compra, e o que cada um compra

| Comprador | Escala conhecida | O que compra |
|---|---|---|
| Conta PJ e adquirente (Cora, Asaas, InfinitePay) | Cora com 1,7 milhão de clientes, Asaas com 270 mil | retenção e originação: eles veem um canal, a API devolve o cliente inteiro |
| Contabilidade digital (Contabilizei) | mais de 100 mil clientes, não atende MEI | funil: o lead da migração para ME, com o ano já reconciliado |
| Conversacionais (Jota, Magie) | 300 mil e 150 mil usuários | o que declaradamente não têm: nenhuma linha fiscal nos dois produtos |

### O problema estratégico que precisa estar decidido antes do primeiro contrato

A API vai gerar achados **sobre o próprio parceiro**. A taxa efetiva de 3,49% contra 2,89% contratados é uma das anomalias do nosso próprio dataset, e num contrato de distribuição o contratante seria a adquirente. Cedo ou tarde alguém pede para suprimir uma família de achado.

> **Achado sobre o parceiro nunca é suprimido.** Se isso for inaceitável para ele, ele não é parceiro.

Parece caro e é o contrário. Um produto que não move dinheiro, não vende crédito e não esconde nada do parceiro **é o único que pode ser embarcado por concorrentes entre si**. A neutralidade é o ativo comercial, não o custo dele. É a versão H4 da constante 1.

Consequência técnica: não existe parâmetro de supressão por família ou por contraparte. A única supressão possível é a da pessoa, pelo endpoint de respostas, e ela é registrada.

### A regra de degradação

A API prefere calar a inventar, exatamente como o produto:

- histórico insuficiente devolve `projecao: null` com motivo, nunca uma projeção fraca sem aviso;
- consentimento expirado devolve pendência, nunca um número velho apresentado como atual;
- régua desconhecida (lei nova ainda não modelada) devolve erro explícito, e **não estima**;
- nenhum acumulado sai sem o bloco de cobertura junto.

### O que precisa ser verdade antes

Não dá para começar pelo H4. Ele depende da **régua parametrizável** (feature 17), do **painel de precisão** (feature 06), porque vender apuração sem taxa de acerto medida é irresponsável, e de isolamento de dados e LGPD de verdade, já que a partir daqui o dado é de terceiro.

### O que eu faria primeiro, e não é a API

**A apuração como relatório, em lote, na mão, vendida para uma contabilidade só.** Descobre-se o contrato certo atendendo alguém antes de congelar o formato em JSON. O erro clássico é desenhar a API pelo que o time acha bonito, e não pelo que o primeiro cliente pede.

---

## Fora do roadmap, de propósito

Tão importante quanto a lista de cima. Cada uma destas é uma feature que alguém vai pedir, e a resposta é não, com motivo.

| Feature | Por que fica fora |
|---|---|
| **Categorização manual de gastos** | Perde para o caderno por construção. Quem depende de registro não acha o que a pessoa não sabe que existe. |
| **Orçamento e metas** | Orçar pressupõe que você vai abrir. Nosso usuário não abre. É o trabalho do ALL, não o nosso. |
| **Cancelar assinatura, contestar, pagar o DAS** | Move dinheiro ou age em nome da pessoa. Constante 1. A Regis prepara, a pessoa executa. |
| **Conta digital, cartão, rendimento** | Vira Jota e Magie, com menos dinheiro e menos tempo de estrada. E quem é conta quer o saldo dentro dela. |
| **Oferta de crédito** | Mata a credibilidade do número. Só laudo a pedido, feature 19. |
| **Otimização fiscal** (segurar nota, dividir entrada, atrasar recebimento) | Constante 4. A Regis mede o que entra, não o que foi declarado. |
| **Antifraude** | O banco pega primeiro e antifraude de emissor é maduro. Não competir. |
| **Feed de alertas** | Se a tela tiver mais de 5 itens sem hierarquia de certeza, o produto virou o que ele existe para não ser. |

---

## As três decisões que o roadmap não pode tomar sozinho

1. **O dinheiro em espécie.** Ele não tem trilha, e para comércio de bairro pode ser fatia grande do faturamento. Ou a Regis declara a margem e aceita ficar cega (feature 11), ou ela abre uma exceção à regra de zero entrada manual, com uma pergunta agregada por semana. A segunda opção é gesto recorrente, que é exatamente o que perde para o caderno. **Recomendo declarar a margem e não perguntar**, mas a decisão é do time.
2. **Até onde a inferência de receita no CPF pode ir sem perguntar.** Errar para mais assusta a pessoa com um teto que ela não estourou. Errar para menos é o erro perigoso, o que ela descobre em maio. Precisa de uma política explícita, não de um limiar escolhido no código.
3. **Quantas mensagens por semana é o teto.** A cadência é decisão de produto e de tom, não de engenharia, e ela define se a Regis vira presença ou vira spam.

---

## Como ler a ordem

O roadmap não se divide por anomalia, se concentra em poucas peças que destravam muitas. A ordem de dependência é esta:

```
identificação de contraparte
   └── duplicidade, recorrência, valor          (fato, já de pé)
   └── conciliação venda contra repasse         (fato, precisa de H2 features 8 e 9)
   └── motor fiscal                             (regra, já de pé)
          └── régua parametrizável              (H3, protege contra mudança de lei)
                 └── multi regime               (H4, é o que o parceiro compra)

histórico de 12 meses na conexão                (H1, feature 2)
   └── é o que faz tudo acima funcionar no dia 1
```

**A feature 2 é a que eu construiria primeiro depois do hackathon.** Ela é barata, ninguém se lembra dela, e é a diferença entre um produto que entrega um número na primeira mensagem e um que pede três meses de paciência.

---

*Documento vivo. Feature nova entra pelo filtro das quatro perguntas, nunca por parecer boa ideia.*
