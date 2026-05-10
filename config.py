# ╔══════════════════════════════════════════════════════════════════╗
# ║           GIANNI (Custom) — Konfiguracija                      ║
# ╚══════════════════════════════════════════════════════════════════╝
import os

# ── Bot Token ──────────────────────────────────────────────────────
# Na Railway/Render: postavi env var TOKEN u dashboard-u
# Lokalno: možeš direktno zalijepiti token ovdje umjesto os.environ.get(...)
TOKEN = os.environ.get("TOKEN", "ZALIJEPI-TOKEN-OVDJE-ILI-POSTAVI-ENV-VAR")

# ── Guild (Server) ID ───────────────────────────────────────────────
GUILD_ID = 1496860022066385016

# ── Kanal gdje Welcome ide ──────────────────────────────────────────
# Stavi ID svog welcome kanala ovdje (broj, ne mention)
WELCOME_CHANNEL_ID = 1494687347558715543  # Promijeni na pravi ID

# ── Kanal gdje je Poo Game dozvoljen ───────────────────────────────
# Samo u ovom kanalu korisnici mogu koristiti /mypoo i .poo komande
# Stavi ID kanala (npr. poo-game kanal)
POO_CHANNEL_ID = 1502902417778544640  # Promijeni na pravi ID

# ── Log Kanal (opcionalno — za administrativne logove) ─────────────
LOG_CHANNEL_ID = 0  # Postavi na 0 da isključiš logovanje

# ── Auto-Uloga za nove članove (opcionalno) ─────────────────────────
AUTO_ROLE_ID = 0  # Postavi na 0 da isključiš auto-ulogu

# ── Anti-Spam konfiguracija ─────────────────────────────────────────
SPAM_MSG_LIMIT   = 6    # Maksimalno poruka...
SPAM_WINDOW_SEC  = 8    # ...u ovom broju sekundi
SPAM_TIMEOUT_SEC = 60   # Timeout trajanje u sekundama (1 minuta)
