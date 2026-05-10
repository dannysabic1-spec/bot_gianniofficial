# ╔══════════════════════════════════════════════════════════════════╗
# ║           GIANNI (Custom) — Konfiguracija                      ║
# ╚══════════════════════════════════════════════════════════════════╝
import os, sys

# ── Bot Token ──────────────────────────────────────────────────────
# Railway: postavi environment variable TOKEN u Variables tabu
# Lokalno:  TOKEN=tvoj_token python bot.py
TOKEN = os.environ.get("TOKEN", "")
if not TOKEN or TOKEN.startswith("ZALIJEPI"):
    print("=" * 60)
    print("GREŠKA: Bot token nije postavljen!")
    print("Na Railway idi na: Variables → Add Variable")
    print("  Name:  TOKEN")
    print("  Value: (zalijepi novi token)")
    print("=" * 60)
    sys.exit(1)

# ── Guild (Server) ID ───────────────────────────────────────────────
GUILD_ID = 1496860022066385016

# ── Kanal gdje Welcome ide ──────────────────────────────────────────
WELCOME_CHANNEL_ID = 1494687347558715543

# ── Kanal gdje je Poo Game dozvoljen ───────────────────────────────
POO_CHANNEL_ID = 1502902417778544640

# ── Log Kanal (0 = isključeno) ──────────────────────────────────────
LOG_CHANNEL_ID = 0

# ── Auto-Uloga za nove članove (0 = isključeno) ─────────────────────
AUTO_ROLE_ID = 0

# ── Anti-Spam konfiguracija ─────────────────────────────────────────
SPAM_MSG_LIMIT   = 6    # Maksimalno poruka...
SPAM_WINDOW_SEC  = 8    # ...u ovom broju sekundi
SPAM_TIMEOUT_SEC = 60   # Timeout trajanje u sekundama
