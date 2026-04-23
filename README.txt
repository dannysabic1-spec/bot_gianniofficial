═══════════════════════════════════════════════════════════
  GIANNI (Custom) v2.0 — KOMPLETAN PAKET
  Zvanični bot: discord.gg/gian
═══════════════════════════════════════════════════════════

SADRŽAJ:
  • bot.py                — glavni kod
  • requirements.txt      — Python paketi
  • oleun_data.json       — baza (XP, novac, questovi, zoo)
  • oleun_data.json.bak   — backup baze
  • README.txt            — ovo uputstvo

═══════════════════════════════════════════════════════════
  POKRETANJE
═══════════════════════════════════════════════════════════

1) pip install -r requirements.txt
2) Postavi env: DISCORD_TOKEN=tvoj_token
3) python bot.py

═══════════════════════════════════════════════════════════
  ŠTA JE POPRAVLJENO U OVOJ VERZIJI
═══════════════════════════════════════════════════════════

  ✓ /pravila-voice           — embed sa voice pravilima
  ✓ /sync                    — manualni reset slash komandi
  ✓ Voice JTC fix            — bolje detektovanje grešaka
                                + DM korisniku ako padne
  ✓ Staff prijave PRIVATNE   — vidi samo vlasnik bota
  ✓ Giveaway recovery        — nastavlja se nakon restarta
  ✓ Orphaned VC cleanup      — auto-briše prazne na startup
  ✓ on_member_remove fix     — 404 Unknown Guild guard
  ✓ Licencni guard (opt-in)  — LICENSE_GUARD=1 da uključiš

═══════════════════════════════════════════════════════════
  ŠTA SE NASTAVLJA NAKON RESTARTA
═══════════════════════════════════════════════════════════

  ✓ XP / leveli / novac / bank / streak
  ✓ Quest progress (dnevni/sedmični)
  ✓ Zoo, inventar, achievements, badges
  ✓ Reputation, marriage, ban/warn historija
  ✓ Selfroles, ticket, giveaway, staff-vote dugmad
  ✓ Aktivni giveaway-ji + entrants (NOVO!)
  ✓ Privatni VC-ovi (vlasništvo)

VAŽNO: Pri re-uploadu na hosting NE prepiši
       oleun_data.json — pregazićeš sve podatke!
       Najbolje: uploadi samo bot.py, ostavi
       oleun_data.json na hostingu netaknut.

═══════════════════════════════════════════════════════════
  LICENCNI GUARD (opcionalan)
═══════════════════════════════════════════════════════════

DEFAULT: ISKLJUČEN. Da uključiš → env var LICENSE_GUARD=1.
Bot će tada raditi SAMO ako je član discord.gg/gian.
Provjeri OFFICIAL_GUILD_ID u bot.py (linija 24).
