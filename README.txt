═══════════════════════════════════════════════════════════
  GIANNI (Custom) v2.0 — KOMPLETAN PAKET
  Zvanični bot: discord.gg/gian
═══════════════════════════════════════════════════════════

SADRŽAJ PAKETA:
  • bot.py                — glavni bot kod (7512 linija, 98 komandi)
  • requirements.txt      — Python paketi koji su potrebni
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
  ✓ Licencni guard  — bot radi SAMO ako je član discord.gg/gian
                      (sve klonirane kopije se automatski gase)
  ✓ Fix on_member_remove 404 "Unknown Guild" bug

═══════════════════════════════════════════════════════════
  VAŽNO — LICENCA
═══════════════════════════════════════════════════════════

Ovaj bot je zaštićen. Ako neko klonira kod i pokrene svoju
kopiju na drugom serveru, bot:
  1. Detektuje da nije na zvaničnom GIANNI serveru
  2. Šalje upozorenje u tekst kanale
  3. Napušta sve servere i gasi se za 5 sekundi

Jedini originalni bot: https://discord.gg/gian
