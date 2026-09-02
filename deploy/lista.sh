#!/usr/bin/env bash
# Mostra quem entrou na lista de espera do Regis.
#   ./deploy/lista.sh          lista na tela
#   ./deploy/lista.sh csv      exporta em CSV para abrir no Excel
set -euo pipefail
VPS_HOST="${VPS_HOST:-root@SEU_IP_DO_VPS}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
printf '#!/bin/sh\nprintf "%%s\\n" "$VPS_PASS"\n' > "$TMP/a.sh"; chmod 700 "$TMP/a.sh"
printf 'VPS_PASS=pass://SEU_COFRE/SSH VPS/password\n' > "$TMP/p.env"

BRUTO=$(pass-cli run --env-file "$TMP/p.env" -- \
  env SSH_ASKPASS="$TMP/a.sh" SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=accept-new "$VPS_HOST" \
  "docker exec regis-web cat /dados/lista-espera.json 2>/dev/null || echo '[]'")

if [ "${1:-}" = "csv" ]; then
  printf '%s' "$BRUTO" | python3 -c '
import json,sys,csv
lista=json.load(sys.stdin)
saida=csv.writer(sys.stdout)
saida.writerow(["email","nome","perfil","canais","quando"])
for p in lista: saida.writerow([p.get("email",""),p.get("nome",""),p.get("perfil",""),p.get("canais",""),p.get("quando","")])
'
else
  printf '%s' "$BRUTO" | python3 -c '
import json,sys
lista=json.load(sys.stdin)
if not lista:
    print("  Ninguém entrou na lista ainda."); raise SystemExit
print("  %d %s na lista de espera:\n" % (len(lista), "pessoa" if len(lista)==1 else "pessoas"))
for i,p in enumerate(lista,1):
    quando=p.get("quando","")[:16].replace("T"," ")
    extra=" · ".join(x for x in [p.get("perfil"),p.get("canais")] if x)
    print("  %2d. %-34s %s" % (i, p.get("email",""), p.get("nome","") or ""))
    print("      %s%s" % (quando, "  ·  "+extra if extra else ""))
'
fi
