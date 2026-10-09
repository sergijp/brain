#!/bin/zsh
# Сповіщення в Telegram @nadolo_trading_analitycs_bot
# Використання:
#   tg-notify.sh "текст"                 — тільки текст
#   tg-notify.sh "текст" /шлях/до.png    — скрін із підписом
# Токен береться з ~/AI/telegram-bot/.env, у скрипті не зберігається.
set -e
ENV_FILE="$HOME/AI/telegram-bot/.env"
[ -f "$ENV_FILE" ] || { echo "no .env"; exit 1; }
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' "$ENV_FILE" | cut -d= -f2-)
CHAT=$(grep '^ALLOWED_USER_ID=' "$ENV_FILE" | cut -d= -f2-)
[ -n "$TOKEN" ] && [ -n "$CHAT" ] || { echo "no token/chat"; exit 1; }

TEXT="$1"
IMG="$2"
OK='import sys,json;d=json.load(sys.stdin);print("sent" if d.get("ok") else "FAIL: "+str(d.get("description")))'

if [ -n "$IMG" ] && [ -f "$IMG" ]; then
  curl -s --max-time 40 -X POST "https://api.telegram.org/bot${TOKEN}/sendPhoto" \
    -F "chat_id=${CHAT}" \
    -F "parse_mode=HTML" \
    -F "caption=${TEXT}" \
    -F "photo=@${IMG}" | python3 -I -c "$OK"
else
  curl -s --max-time 15 -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${CHAT}" \
    --data-urlencode "text=${TEXT}" \
    --data-urlencode "parse_mode=HTML" | python3 -I -c "$OK"
fi
