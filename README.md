# 🐾 GIANNI (Custom) Bot

## Šta radi ovaj bot?
- **Welcome sistem** — čist, kompaktan embed kad novi član uđe, uvijek radi
- **Poo Game** — svaki član ima svog osobnog Poo-a (embed sa nickom i svim stats)
- **Anti-Spam** — automatski briše spam i daje timeout

---

## ⚡ Brza instalacija

### 1. Instaliraj Python 3.10+
Preuzmi sa: https://www.python.org/downloads/

### 2. Instaliraj zavisnosti
```
pip install -r requirements.txt
```

### 3. Podesi `config.py`
Otvori `config.py` i promijeni:
- `TOKEN` — tvoj bot token
- `WELCOME_CHANNEL_ID` — ID kanala za welcome
- `POO_CHANNEL_ID` — ID kanala za Poo Game
- `LOG_CHANNEL_ID` — ID kanala za logove (0 = isključeno)
- `AUTO_ROLE_ID` — ID uloge za automatski dodjelu (0 = isključeno)

**Kako naći ID kanala:** Desni klik na kanal → "Kopiraj ID"
*(Moraš imati uključen Developer Mode: Settings → Advanced → Developer Mode)*

### 4. Pokreni bota
```
python bot.py
```

---

## 🎮 Poo Game Komande

Sve komande rade SAMO u kanalu koji je postavljen kao `POO_CHANNEL_ID`!

| Komanda | Opis | Cooldown |
|---------|------|----------|
| `/mypoo start [ime]` | Kreiraj svog Poo-a | — |
| `/mypoo status` | Pogledaj statistike | — |
| `/mypoo feed` | Nahrani Poo-a | 20 min |
| `/mypoo play` | Igraj se s Poo-om | 15 min |
| `/mypoo clean` | Operi Poo-a | 30 min |
| `/mypoo sleep` | Pošalji na spavanje | 2h |
| `/mypoo work` | Pošalji na posao | 45 min |
| `/mypoo daily` | Dnevna nagrada | 1× dnevno |
| `/mypoo rename [ime]` | Promijeni ime | — |
| `/mypoo leaderboard` | Top 10 Poo-ova | — |
| `/mypoo poo_info @user` | Pogledaj tuđeg Poo-a | — |
| `/mypoo help` | Uputstvo | — |

**Prefix komande:**  
`.poo` ili `.mypoo` — bot te redirectuje u pravi kanal

---

## 🚫 Anti-Spam
Bot automatski:
- Prati broj poruka po korisniku u kratkom vremenskom okviru
- Briše spam poruke
- Daje timeout spameru (60 sekundi)
- Admini su imuni

Podesi granice u `config.py`:
- `SPAM_MSG_LIMIT` — max poruka (default: 6)
- `SPAM_WINDOW_SEC` — vremenski prozor u sekundama (default: 8)
- `SPAM_TIMEOUT_SEC` — trajanje timeoutа (default: 60)

---

## 📁 Fajlovi
- `bot.py` — Glavni bot fajl
- `poo_game.py` — Poo Game sistem
- `config.py` — Konfiguracija (TOKEN, ID-ovi)
- `poo_personal_data.json` — Automatski kreira se, čuva podatke igrača

---

## ⚠️ Napomene
- **Regeneriraj token** u Discord Developer Portal → Bot → Reset Token
- Nikad ne dijeli `config.py` niti token s nikime
- Bot mora imati dozvole: `Send Messages`, `Embed Links`, `Manage Messages`, `Moderate Members`
- Za welcome — bot mora biti u kanalu s dozvolom `View Channel` + `Send Messages`
