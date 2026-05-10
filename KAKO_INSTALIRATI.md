# 🐾 GIANNI Bot — Instalacija i Podešavanje

## 📁 Fajlovi u paketu

| Fajl | Opis |
|------|------|
| `bot.py` | Glavni fajl — pokreće sve |
| `poo_game.py` | Poo Game sistem (sve komande) |
| `welcome_cog.py` | Welcome sistem (1 kanal, uvijek radi) |
| `anti_spam_cog.py` | Anti-spam zaštita |
| `requirements.txt` | Potrebne biblioteke |
| `poo_personal_data.json` | Auto-kreira se (čuva poo podatke) |

---

## ⚡ Instalacija (3 koraka)

### Korak 1 — Instaliraj biblioteke
```bash
pip install -r requirements.txt
```

### Korak 2 — Podesi token
**Opcija A — Env varijabla (preporučeno):**
```bash
# Linux/Mac:
export DISCORD_TOKEN=tvoj_discord_token_ovdje

# Windows CMD:
set DISCORD_TOKEN=tvoj_discord_token_ovdje

# Windows PowerShell:
$env:DISCORD_TOKEN="tvoj_discord_token_ovdje"
```

**Opcija B — .env fajl:**
Napravi `.env` fajl u istom folderu:
```
DISCORD_TOKEN=tvoj_discord_token_ovdje
```

### Korak 3 — Pokreni bota
```bash
python bot.py
```

---

## 🔧 Konfiguracija

### Poo Game kanal (OBAVEZNO!)
Otvori `poo_game.py` i pronađi na vrhu:

```python
POO_CHANNEL_NAME = "poo"   # ime kanala gdje je dozvoljen poo
POO_CHANNEL_ID   = 0       # ili upiši ID kanala (prioritet)
```

Primjer sa ID-em:
```python
POO_CHANNEL_ID = 1234567890123456789  # ID tvog poo kanala
```

Kako naći ID kanala: Desni klik na kanal → "Copy Channel ID" (mora biti uključen Developer Mode)

### Welcome kanal
Otvori `welcome_cog.py`:
```python
WELCOME_CHANNEL_ID = 1234567890123456789  # ID welcome kanala
```

Ako ostane 0, bot će automatski tražiti kanal sa "welcome" u imenu.

---

## 🐾 Poo Game — Komande

### Prefix komande (u #poo kanalu)
```
.poo              → Pogledaj svog Poo-a (sa dugmadima!)
.poo feed         → 🍗 Nahrani (20min cooldown)
.poo play         → 🎮 Igraj se (15min cooldown)
.poo clean        → 🧼 Operi (30min cooldown)
.poo work         → 💼 Posao (45min cooldown)
.poo sleep        → 😴 Spavaj (2h cooldown, 2h sna)
.poo daily        → 🎁 Dnevna nagrada (1x dnevno)
.poo top          → 🏆 Ljestvica Top 10
.poo help         → ❓ Uputstvo
```

### Slash komande (svuda)
```
/mypoo start [ime]     → Kreiraj Poo-a
/mypoo status          → Pogledaj Poo-a
/mypoo rename [ime]    → Promijeni ime
/mypoo leaderboard     → Top 10
/mypoo poo_info @user  → Tuđi Poo
/mypoo help            → Uputstvo
```

---

## 🎮 Kako funkcionišu dugmad

Kada otvoriš `.poo` ili `/mypoo status`, embed ima **6 dugmadi**:

| Dugme | Akcija | Cooldown |
|-------|--------|----------|
| 🍗 Nahrani | Hrani Poo-a | 20 min |
| 🎮 Igraj se | Igra se | 15 min |
| 🧼 Operi | Čisti Poo-a | 30 min |
| 😴 Spavaj | Spavanje | 2h CD, 2h sna |
| 💼 Posao | Zarađuje | 45 min |
| 🎁 Dnevna | Dnevna nagrada | 1x dnevno |

**Kada klikneš dugme:**
- Embed se odmah ažurira sa novim stanjem i emoji-em!
- Poo emoji se mijenja zavisno od stanja (gladan, sretan, umoran...)
- Samo vlasnik Poo-a može koristiti dugmad!

---

## 💩 Custom Emoji IDs

Sve koristi emoji ID-eve iz GIANNI Custom bota:

```
pooplove         → 1502906803317379102
pleadpoop        → 1502906780177530951
cryingpoop       → 1502906783172399224
poopsad          → 1502906805334966374
angrypoop        → 1502906809269096468
angrycowboypoop  → 1502906807234859028
heartbrokenpoop  → 1502906810971979807
holyshit         → 1502906801178280076
satisfied        → 1502906795380814456
hardcry          → 1502906795189076039
poopsussysweat   → 1502906790650712215
poopdisgusted    → 1502906775609934005
```

Ako emoji ne rade, bot mora biti na serveru gdje su ti emoji definirani!

---

## 📱 Mobile-Friendly Dizajn

Bot je optimiziran za **Samsung Galaxy S25** i sve mobitele:
- Kratki bari statistika (8 znakova umjesto 10)
- Veliki emoji prikaz u 3×3 gridu
- Kompaktni tekst — čitljiv na malom ekranu
- Dugmad su optimizirana za touch (ne treba tipkati komande)

---

## 🛡️ Anti-Spam Pravila

| Pravilo | Limit |
|---------|-------|
| Flood | Max 5 poruka / 5 sekundi |
| Iste poruke | Max 3 iste poruke zaredom |
| Emojii | Max 10 emojia po poruci |
| CAPS LOCK | Max 80% velikih slova |

Kanali izuzeti od anti-spama: `spam`, `meme`, `off-topic`
Admini su uvijek izuzeti.

---

## 🔔 DM Notifikacije

Bot automatski šalje DM kada Poo treba pažnju:
- 🍗 Gladan (< 30%)
- 🧼 Prljav (< 30%)
- 😔 Dosađuje se (< 30%)
- 😪 Umoran (< 25%)

**Cooldown između DM-ova:** 3 sata

---

## ❓ Česte greške

### "Emoji ne prikazuju se"
Bot mora biti na istom serveru gdje su custom emojiji definirani, ILI mora imati pristup emoji-ima kao eksterni emojiji (Nitro/Boostovan server).

### "Komande ne rade"
Sačekaj 1-2 minuta da se slash komande sync-aju. Restart bota ako traje duže.

### "Welcome ne šalje"
Provjeri `WELCOME_CHANNEL_ID` u `welcome_cog.py` i da bot ima dozvolu `Send Messages` u tom kanalu.

### "Poo komande ne rade van #poo"
To je namjerno! Poo komande su zaključane samo za poo kanal. Promijeni `POO_CHANNEL_NAME` ili `POO_CHANNEL_ID` u `poo_game.py` ako trebaš drugi kanal.

---

## 💾 Backup podataka

Poo podaci se čuvaju u `poo_personal_data.json`.
**Nikada ne briši ovaj fajl!**

Preporučeni backup: kopiraj fajl jednom dnevno na sigurno mjesto.

---

*Bot razvio: GIANNI Community • discord.gg/gian*
