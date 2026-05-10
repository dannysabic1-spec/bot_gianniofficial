# ╔══════════════════════════════════════════════════════════════════╗
# ║           GIANNI (Custom) — Konfiguracija                      ║
# ╚══════════════════════════════════════════════════════════════════╝
import os, sys

# Token se čita iz Railway Variables — nikad ga ne stavljaj direktno u kod!
TOKEN = os.environ.get("TOKEN", "")
if not TOKEN:
    sys.exit("GREŠKA: Postavi TOKEN u Railway → Variables tab!")

GUILD_ID             = 1496860022066385016
WELCOME_CHANNEL_ID   = 1494687347558715543
POO_CHANNEL_ID       = 1502902417778544640
LOG_CHANNEL_ID       = 0
AUTO_ROLE_ID         = 0
SPAM_MSG_LIMIT       = 6
SPAM_WINDOW_SEC      = 8
SPAM_TIMEOUT_SEC     = 60
