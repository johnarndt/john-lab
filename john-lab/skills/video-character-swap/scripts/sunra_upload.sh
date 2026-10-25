#!/usr/bin/env bash
# Upload a local file to Sunra and print only its asset_url (pass that to create_video).
# usage: sunra_upload.sh FILE CONTENT_TYPE      e.g. sunra_upload.sh crop.mp4 video/mp4
set -euo pipefail
f="$1"; ct="$2"
r=$(sunra call get_upload_url "{\"content_type\":\"$ct\",\"filename\":\"$(basename "$f")\"}")
url=$(printf '%s' "$r" | python3 -I -c 'import json,sys;print(json.load(sys.stdin)["upload_url"])')
code=$(curl -s -o /dev/null -w '%{http_code}' -X PUT -H "Content-Type: $ct" --data-binary @"$f" "$url")
[ "$code" = 200 ] || { echo "upload failed: HTTP $code" >&2; exit 1; }
printf '%s' "$r" | python3 -I -c 'import json,sys;print(json.load(sys.stdin)["asset_url"])'
