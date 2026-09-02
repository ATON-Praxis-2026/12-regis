#!/usr/bin/env python3
"""Gera respostas-forms.md a partir do CSV exportado do Google Forms.

Uso:
  1. No Forms > Respostas > baixar CSV (ou o .zip).
  2. Salve o CSV nesta pasta (substitui o antigo). Se vier .zip, descompacte aqui.
  3. python3 gerar-markdown.py

Respondentes ficam anonimos (R1, R2...). O CSV nao deve ir para repositorio publico.
"""
import csv, glob, os, re, sys
from datetime import date
from collections import Counter, OrderedDict

AQUI = os.path.dirname(os.path.abspath(__file__))
csvs = sorted(glob.glob(os.path.join(AQUI, "*.csv")), key=os.path.getmtime)
if not csvs:
    sys.exit("Nenhum CSV encontrado nesta pasta.")
CSV = csvs[-1]
SAIDA = os.path.join(AQUI, "..", "respostas-forms.md")

rows = list(csv.reader(open(CSV, encoding="utf-8-sig")))
hdr, data = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]

# nomes curtos das colunas
NOMES = OrderedDict([
    (1, "Tipo de CNPJ"),
    (2, "Chute de faturamento no ano"),
    (3, "Confiança no chute"),
    (4, "Sabe quanto falta para o teto?"),
    (5, "Por onde o dinheiro entra"),
    (6, "Mistura conta pessoal e do negócio?"),
    (7, "Confere se o que caiu bate com a venda?"),
    (8, "Última vez que resolveu imposto / DAS / declaração"),
])
FECHADAS = [1, 2, 3, 4]
ABERTAS = [5, 6, 7, 8]

def limpa(s):
    return re.sub(r"\s+", " ", (s or "").strip())

def tabela_contagem(idx):
    c = Counter(limpa(r[idx]) or "(em branco)" for r in data)
    linhas = ["| Resposta | n |", "|---|---|"]
    for k, v in c.most_common():
        linhas.append(f"| {k} | {v} |")
    return "\n".join(linhas)

out = []
out.append("---")
out.append("titulo: Respostas do forms com MEIs")
out.append("tipo: pesquisa")
out.append("status: vigente")
out.append(f"atualizado: {date.today().isoformat()}")
out.append("autor: Time 12 · Hackathon Vanguarda")
out.append("resumo: O que os MEIs responderam sobre faturamento, canais de recebimento, mistura de contas e imposto.")
out.append("---")
out.append("")
out.append("# Respostas do forms · Pesquisa MEI (Regis)\n")
out.append(f"Gerado automaticamente por `respostas-forms/gerar-markdown.py` a partir de `{os.path.basename(CSV)}`.")
out.append(f"**{len(data)} respostas.** Última resposta em {limpa(data[-1][0]) if data else 'n/a'}.")
out.append("Respondentes anonimizados (R1, R2...). Para reler o dado bruto, abra o CSV na pasta `respostas-forms/`, que não deve circular.\n")
out.append("---\n")
out.append("## Resumo das perguntas fechadas\n")
for i in FECHADAS:
    out.append(f"### {NOMES[i]}\n")
    out.append(tabela_contagem(i) + "\n")

out.append("---\n")
out.append("## Respostas abertas, por pergunta\n")
for i in ABERTAS:
    out.append(f"### {NOMES[i]}\n")
    for n, r in enumerate(data, 1):
        t = limpa(r[i])
        if t:
            out.append(f"- **R{n}** ({limpa(r[2])}): {t}")
    out.append("")

out.append("---\n")
out.append("## Ficha por respondente\n")
for n, r in enumerate(data, 1):
    out.append(f"### R{n} · {limpa(r[1])} · {limpa(r[0])}\n")
    for i in NOMES:
        t = limpa(r[i])
        if t:
            out.append(f"- **{NOMES[i]}:** {t}")
    out.append("")

open(SAIDA, "w", encoding="utf-8").write("\n".join(out))
print(f"ok: {len(data)} respostas -> {os.path.relpath(SAIDA)}")
