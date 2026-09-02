#!/usr/bin/env bash
# Baixa o registro de conversas da Regis do VPS para bot/conversas.jsonl.
# Depois leia com: python3 bot/conversas.py
set -euo pipefail
VPS_HOST="${VPS_HOST:-root@SEU_IP_DO_VPS}"
DESTINO="$(cd "$(dirname "$0")/.." && pwd)/bot/conversas.jsonl"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
printf '#!/bin/sh\nprintf "%%s\\n" "$VPS_PASS"\n' > "$TMP/askpass.sh"; chmod 700 "$TMP/askpass.sh"
printf 'VPS_PASS=pass://SEU_COFRE/SSH VPS/password\n' > "$TMP/pass.env"
pass-cli run --env-file "$TMP/pass.env" -- \
  env SSH_ASKPASS="$TMP/askpass.sh" SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=accept-new "$VPS_HOST" \
  "docker exec regis-bot cat /dados/conversas.jsonl" > "$DESTINO"
echo "baixei $(wc -l < "$DESTINO") mensagens em $DESTINO"
echo "leia com: python3 bot/conversas.py"
