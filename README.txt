═══════════════════════════════════════════════════════════
  GIANNI (Custom) v2.0 — KOMPLETAN PAKET
  Zvanični bot: discord.gg/gian
═══════════════════════════════════════════════════════════

SADRŽAJ PAKETA:
  • bot.py                — glavni bot kod
  • requirements.txt      — Python paketi
  • oleun_data.json       — baza podataka (XP, novac, questovi, zoo...)
  • oleun_data.json.bak   — sigurnosna kopija baze
  • README.txt            — ovo uputstvo

═══════════════════════════════════════════════════════════
  POKRETANJE BOTA
═══════════════════════════════════════════════════════════

1) Instaliraj Python pakete:
     pip install -r requirements.txt

2) Postavi token kao environment variablu:
     Linux/Mac:   export DISCORD_TOKEN="tvoj_token_ovdje"
     Windows:     set DISCORD_TOKEN=tvoj_token_ovdje

3) Pokreni bota:
     python bot.py

═══════════════════════════════════════════════════════════
  NOVO U OVOJ VERZIJI
═══════════════════════════════════════════════════════════

  ✓ /pravila-voice  — embed sa pravilima za voice kanale
  ✓ /sync           — manualni reset slash komandi (vlasnik)
  ✓ Licencni guard  — opcionalan, gasi klonirane kopije
  ✓ Fix on_member_remove 404 "Unknown Guild" bug

═══════════════════════════════════════════════════════════
  LICENCNI GUARD (opcionalan)
═══════════════════════════════════════════════════════════

Po DEFAULTU je ISKLJUČEN da slučajno ne ugasi tvoj bot.

Da uključiš zaštitu protiv klonova, postavi env var:
     LICENSE_GUARD=1

Kad je uključen, bot:
  1. Provjeri da li je član zvaničnog GIANNI servera
  2. Ako nije — javi upozorenje, napusti sve servere, ugasi se

VAŽNO: Provjeri da je OFFICIAL_GUILD_ID u bot.py tačan ID
       tvog GIANNI servera prije nego uključiš guard!
       (linija 24, trenutno: 1494043955980140754)
