# -*- coding: utf-8 -*-
"""
Stub do motor de detecção.

Existe por um motivo só: o bot não pode quebrar enquanto `motor/detectar.py`
está sendo escrito por outra pessoa. Se o import do motor real falhar,
`regis_bot.py` cai aqui e continua rodando com os mesmos dados da demo.

O formato de saída é idêntico ao contrato acordado:

    {"resumo": {...}, "achados": [...], "silenciados": [...]}

Os números vêm do gabarito em `dados/anomalias-esperadas.json` e do
`dados/README.md`, então a demo com stub mostra exatamente os mesmos valores
que a demo com o motor real.

Dados sintéticos. Nenhuma pessoa ou empresa aqui é real.
"""

RESUMO = {
    "faturamento_acumulado": 58400.00,
    "teto": 81000.00,
    "percentual_do_teto": 72.1,
    "falta_para_o_teto": 22600.00,
    "projecao_estouro": "outubro de 2026",
    "total_recuperavel": 1145.15,
    "qtd_transacoes_conferidas": 367,
}

ACHADOS = [
    {
        "id": "AN-01",
        "certeza": "fato",
        "tipo": "duplicidade",
        "contraparte": "Beleza Distribuidora",
        "titulo": "O boleto da Beleza Distribuidora foi pago duas vezes",
        "explicacao": (
            "R$ 487,60 saiu às 09:12 e o mesmo valor saiu de novo às 16:48 do dia 14/07. "
            "Mesmo fornecedor, mesmo valor, mesmo dia."
        ),
        "valor": 487.60,
        "transacoes": ["TX-0165", "TX-0167"],
        "acao": {
            "tipo": "email",
            "titulo": "Ver o texto",
            "texto": (
                "Prezados da Beleza Distribuidora,\n\n"
                "O boleto de R$ 487,60 com vencimento em 14/07/2026 foi pago duas vezes no mesmo dia, "
                "às 09:12 e às 16:48. Seguem os dois comprovantes.\n\n"
                "Peço a devolução de R$ 487,60 na minha conta, ou o abatimento desse "
                "valor no próximo pedido, o que for mais rápido para vocês.\n\n"
                "Fico no aguardo.\n"
                "Angela Nogueira, cabeleireira MEI"
            ),
        },
    },
    {
        "id": "AN-02",
        "certeza": "fato",
        "tipo": "duplicidade",
        "contraparte": "Netflix",
        "titulo": "A Netflix cobrou duas vezes no dia 12",
        "explicacao": (
            "R$ 55,90 às 09:14 e R$ 55,90 de novo às 21:47, tudo no dia 12/08. "
            "É a mesma mensalidade cobrada duas vezes."
        ),
        "valor": 55.90,
        "transacoes": ["TX-0274", "TX-0277"],
        "acao": {
            "tipo": "contestacao",
            "titulo": "Ver o texto",
            "texto": (
                "Contestação de cobrança duplicada\n\n"
                "Titular: Angela Nogueira, cabeleireira MEI.\n"
                "Cobrança: Netflix, R$ 55,90, em 12/08/2026 às 09:14 e às 21:47.\n\n"
                "A mensalidade de agosto foi lançada duas vezes no mesmo dia. Solicito o estorno de uma "
                "das cobranças, no valor de R$ 55,90.\n\n"
                "Anexo o extrato com os dois lançamentos."
            ),
        },
    },
    {
        "id": "AN-03",
        "certeza": "fato",
        "tipo": "recorrencia",
        "contraparte": "Agenda Salão App",
        "titulo": "O app de agenda continua cobrando depois do cancelamento",
        "explicacao": (
            "Você cancelou em 12/06, protocolo AGS-2026-88421. "
            "Mesmo assim ele cobrou R$ 39,90 em 22/06, 22/07 e 22/08."
        ),
        "valor": 119.70,
        "transacoes": ["TX-0084", "TX-0196", "TX-0323"],
        "acao": {
            "tipo": "email",
            "titulo": "Ver o texto",
            "texto": (
                "Assunto: cobrança após cancelamento, protocolo AGS-2026-88421\n\n"
                "Cancelei o Agenda Salão App em 12/06/2026, protocolo AGS-2026-88421. Mesmo assim recebi "
                "três cobranças de R$ 39,90, em 22/06, 22/07 e 22/08, somando R$ 119,70.\n\n"
                "Peço o cancelamento definitivo e a devolução dos R$ 119,70.\n\n"
                "Angela Nogueira, cabeleireira MEI"
            ),
        },
    },
    {
        "id": "AN-04",
        "certeza": "fato",
        "tipo": "valor",
        "contraparte": "SomPro Música Ambiente",
        "titulo": "O som ambiente subiu de preço sem avisar",
        "explicacao": (
            "Eram R$ 32,90 por mês até julho. Em 08/08 veio R$ 47,90, uma alta de 45,6 por cento."
        ),
        "valor": 15.00,
        "periodicidade": "por mês",
        "transacoes": ["TX-0261"],
        "acao": {
            "tipo": "mensagem",
            "titulo": "Ver o texto",
            "texto": (
                "Olá,\n\n"
                "A assinatura do som ambiente passou de R$ 32,90 para R$ 47,90 na cobrança de 08/08/2026, "
                "sem aviso prévio.\n\n"
                "Podem me confirmar o motivo do reajuste e a data em que ele foi comunicado? Se o valor "
                "novo for mantido, peço o cancelamento a partir do próximo ciclo.\n\n"
                "Angela Nogueira, cabeleireira MEI"
            ),
        },
    },
    {
        "id": "AN-05",
        "certeza": "fato",
        "tipo": "conciliacao",
        "contraparte": "BelezaNet",
        "titulo": "O repasse da BelezaNet veio R$ 38,00 menor",
        "explicacao": (
            "Conferi os repasses do marketplace. Na sexta 28/08 foram 11 atendimentos, R$ 1.042,00 "
            "vendidos. Com a comissão de 12 por cento deveriam cair R$ 916,96, e caíram R$ 878,96."
        ),
        "valor": 38.00,
        "transacoes": ["TX-0344"],
        "acao": {
            "tipo": "mensagem",
            "titulo": "Ver o texto",
            "texto": (
                "Olá, time da BelezaNet.\n\n"
                "O repasse do dia 28/08/2026 cobriu 11 atendimentos, com valor de venda de R$ 1.042,00. "
                "Com a comissão de 12 por cento prevista em contrato, o repasse deveria ser de R$ 916,96, "
                "mas foi creditado R$ 878,96.\n\n"
                "Falta R$ 38,00. Podem verificar e me enviar o detalhamento desse repasse?\n\n"
                "Angela Nogueira, cabeleireira MEI"
            ),
        },
    },
    {
        "id": "AN-06",
        "certeza": "fato",
        "tipo": "duplicidade",
        "contraparte": "DAS MEI",
        "titulo": "O DAS de junho foi pago duas vezes",
        "explicacao": (
            "R$ 87,05 da competência 06/2026 saiu em 17/07 e saiu de novo em 20/07. "
            "São três dias de diferença, por isso passou batido."
        ),
        "valor": 87.05,
        "transacoes": ["TX-0175", "TX-0193"],
        "acao": {
            "tipo": "instrucao",
            "titulo": "Ver o passo a passo",
            "texto": (
                "Pedido de restituição de DAS pago em duplicidade\n\n"
                "1. Entre no portal do Simples Nacional, área do MEI, com o código de acesso ou gov.br.\n"
                "2. Abra Restituição e informe a competência 06/2026.\n"
                "3. Informe os dois pagamentos de R$ 87,05, de 17/07/2026 e de 20/07/2026.\n"
                "4. Peça a restituição de um deles e informe a sua conta.\n\n"
                "Quem faz o pedido é você, com o seu acesso. Eu deixei o texto e os dados prontos."
            ),
        },
    },
    {
        "id": "AN-07",
        "certeza": "fato",
        "tipo": "valor",
        "contraparte": "Cielo",
        "titulo": "A antecipação automática está ligada",
        "explicacao": (
            "Ela está ligada desde 02/03 e morde 2,99 por cento de tudo que você vende no crédito."
        ),
        "valor": 312.00,
        "periodicidade": "no trimestre",
        "transacoes": ["TX-0004", "TX-0367"],
        "acao": {
            "tipo": "instrucao",
            "titulo": "Ver o passo a passo",
            "texto": (
                "Como desligar a antecipação automática\n\n"
                "1. Abra o app da maquininha e entre com o seu login.\n"
                "2. Vá em Recebimentos, depois Antecipação.\n"
                "3. Desligue a chave de antecipação automática.\n"
                "4. Confirme e guarde o protocolo.\n\n"
                "Se desligar, o dinheiro do crédito passa a cair em 30 dias em vez de cair no dia. "
                "Vale conferir se o seu caixa aguenta essa espera antes de mexer. A decisão é sua, "
                "eu só somei o que ela custa."
            ),
        },
    },
    {
        "id": "AN-08",
        "certeza": "fato",
        "tipo": "valor",
        "contraparte": "Banco, conta PJ",
        "titulo": "A conta PJ deixou de ser gratuita",
        "explicacao": (
            "A isenção valia até 31/07 e em 05/08 apareceu a primeira tarifa de manutenção."
        ),
        "valor": 29.90,
        "periodicidade": "por mês",
        "transacoes": ["TX-0244"],
        "acao": {
            "tipo": "mensagem",
            "titulo": "Ver o texto",
            "texto": (
                "Mensagem para o gerente da conta\n\n"
                "Olá, sou Angela Nogueira, cabeleireira MEI.\n"
                "Minha conta PJ era isenta de tarifa de manutenção até 31/07/2026 e em 05/08 veio a "
                "primeira cobrança de R$ 29,90.\n\n"
                "Gostaria de saber se consigo renovar a isenção, ou migrar para uma conta MEI sem tarifa. "
                "No ano essa tarifa dá R$ 358,80, o que pesa no meu tamanho de negócio.\n\n"
                "Obrigada."
            ),
        },
    },
    {
        "id": "AN-09",
        "certeza": "regra",
        "tipo": "fiscal",
        "contraparte": None,
        "titulo": "No ritmo atual você encosta no teto em outubro",
        "explicacao": (
            "Junho, julho e agosto vêm crescendo cerca de R$ 1.300,00 por mês. "
            "Mantendo esse ritmo, os R$ 81.000,00 chegam em outubro de 2026."
        ),
        "valor": 0.0,
        "transacoes": [],
        "acao": {
            "tipo": "opcoes",
            "titulo": "Ver as opções",
            "texto": (
                "Você tem três caminhos, e nenhum deles é urgente hoje.\n\n"
                "1. Segurar o faturamento até janeiro. Funciona se der para adiar serviço grande, "
                "mas significa recusar trabalho.\n"
                "2. Migrar para ME no Simples Nacional. O limite sobe muito, a contabilidade passa a ter "
                "custo mensal, e você ganha espaço para crescer sem susto.\n"
                "3. Não fazer nada e se preparar. Até 20 por cento acima do teto você paga a diferença no "
                "ano seguinte e continua MEI. Acima disso, o desenquadramento é automático.\n\n"
                "Quem fecha essa escolha com você é a sua contadora. Eu preparo o resumo do ano para ela."
            ),
        },
    },
    {
        "id": "AN-10",
        "certeza": "regra",
        "tipo": "valor",
        "contraparte": "Cielo",
        "titulo": "A maquininha passou a descontar 3,49 por cento no crédito",
        "explicacao": (
            "O seu contrato diz 2,89 por cento. De 17/08 para cá as vendas no crédito vieram com 3,49. "
            "Até agora a diferença deu R$ 11,03, e ela cresce todo dia."
        ),
        "valor": 11.03,
        "transacoes": ["TX-0308", "TX-0363"],
        "acao": {
            "tipo": "mensagem",
            "titulo": "Ver o texto",
            "texto": (
                "Mensagem para a adquirente\n\n"
                "Sou Angela Nogueira, cabeleireira MEI. Minha taxa contratada de crédito é "
                "2,89 por cento.\n\n"
                "Desde 17/08/2026 as vendas no crédito estão vindo com desconto de 3,49 por cento. "
                "Até 29/08 a diferença soma R$ 11,03.\n\n"
                "Podem confirmar qual taxa está valendo na minha conta e desde quando? Se houve reajuste, "
                "peço a cópia do aviso.\n\n"
                "Obrigada."
            ),
        },
    },
    {
        "id": "AN-11",
        "certeza": "suspeita",
        "tipo": "contraparte",
        "contraparte": "Maria Souza",
        "titulo": "Um Pix de R$ 340,00 para Maria Souza",
        "explicacao": "Foi no dia 03/08 e é a primeira vez que esse nome aparece na sua conta.",
        "valor": 340.00,
        "transacoes": ["TX-0241"],
        "acao": None,
    },
    {
        "id": "AN-12",
        "certeza": "suspeita",
        "tipo": "comportamento",
        "contraparte": "Jéssica Alves",
        "titulo": "Um Pix de R$ 268,00 às 03:41 de domingo",
        "explicacao": (
            "Foi em 19/07, para a Jéssica, que você já paga todo mês. O valor bate com o de sempre, "
            "só o horário que fugiu do seu padrão."
        ),
        "valor": 268.00,
        "transacoes": ["TX-0192"],
        "acao": None,
    },
]

SILENCIADOS = [
    {"id": "SIL-01", "titulo": "Aluguel de R$ 1.850,00",
     "motivo": "é o mesmo valor todo mês, no mesmo dia"},
    {"id": "SIL-02", "titulo": "Vendas de R$ 380,00",
     "motivo": "são as químicas, o seu ticket alto de sempre"},
    {"id": "SIL-03", "titulo": "Pico de movimento na sexta e no sábado",
     "motivo": "é assim toda semana na sua agenda"},
    {"id": "SIL-04", "titulo": "DAS de julho e de agosto",
     "motivo": "um pagamento por competência, tudo certo"},
    {"id": "SIL-05", "titulo": "Taxa de 1,49 por cento no débito",
     "motivo": "bate com o contrato, conferi e não precisa te incomodar"},
    {"id": "SIL-06", "titulo": "Pix único para o supermercado",
     "motivo": "foi você, no horário de sempre, valor de compra normal"},
]


def detectar(pasta="dados"):
    """Devolve o mesmo formato do motor real. O argumento é ignorado de propósito."""
    import copy

    return {
        "resumo": copy.deepcopy(RESUMO),
        "achados": copy.deepcopy(ACHADOS),
        "silenciados": copy.deepcopy(SILENCIADOS),
        "fonte": "stub",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(detectar(), ensure_ascii=False, indent=2))
