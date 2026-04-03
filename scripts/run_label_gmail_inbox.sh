#!/bin/bash
set -euo pipefail
export PATH="/root/.local/bin:$PATH"
export GOG_ACCOUNT="philip.stacy@gmail.com"
export GOG_KEYRING_PASSWORD='openclaw-gog'
exec python3 /root/.openclaw/workspace/scripts/label_gmail_inbox.py
