# 🐾 GIANNI — Personal Poo Game
## Kako dodati `poo_game.py` u svog bota

---

### 📁 Fajlovi
- `poo_game.py` — Glavni modul sa svim komandama i sistemom
- `poo_personal_data.json` — Kreira se automatski (čuva podatke igrača)

---

### ⚡ Instalacija (2 načina)

#### Opcija A — Kao zasebni Cog (preporučeno)
Dodaj u `bot.py` (na kraj, prije `bot.run(TOKEN)`):

```python
import asyncio

async def load_extensions():
    await bot.load_extension("poo_game")  # učitaj cog

# U on_ready eventu ili odmah ispod bot definicije:
asyncio.run(load_extensions())
```

Ili ako bot ima `setup_hook`:
```python
async def setup_hook(self):
    await self.load_extension("poo_game")
```

#### Opcija B — Direktno u main bot fajl
Dodaj na kraj fajla (ispred `bot.run(TOKEN)`):

```python
# ── PERSONAL POO GAME ──────────────────────────────────────
from poo_game import setup as poo_setup, mypoo_group

async def _load_poo():
    await poo_setup(bot)
    
# U on_ready ili setup_hook:
asyncio.create_task(_load_poo())
```

Ili još jednostavnije — dodaj direktno u `on_ready`:
```python
@bot.event
async def on_ready():
    # ... postojeći kod ...
    
    # Dodaj Poo Game
    from poo_game import PersonalPooGame, mypoo_group
    if not bot.get_cog("PersonalPooGame"):
        await bot.add_cog(PersonalPooGame(bot))
        bot.tree.add_command(mypoo_group)
        await bot.tree.sync()
        print("✅ Poo Game aktiviran!")
```

---

### 🎮 Komande
| Komanda | Opis | Cooldown |
|---------|------|----------|
| `/mypoo start [ime]` | Kreiraj svog Poo-a | — |
| `/mypoo status` | Pogledaj statistike | — |
| `/mypoo feed [hrana]` | Nahrani Poo-a | 20 min |
| `/mypoo play` | Igraj se s Poo-om | 15 min |
| `/mypoo clean` | Operi Poo-a | 30 min |
| `/mypoo sleep` | Pošalji na spavanje | 2h CD, 2h sna |
| `/mypoo work` | Pošalji na posao | 45 min |
| `/mypoo daily` | Dnevna nagrada | 1× dnevno |
| `/mypoo rename [ime]` | Promijeni ime | — |
| `/mypoo leaderboard` | Top 10 Poo-ova | — |
| `/mypoo poo_info @user` | Pogledaj tuđeg Poo-a | — |
| `/mypoo help` | Uputstvo | — |

---

### 🔧 Konfiguracija Custom Emoji ID-jeva
Ako tvoji emoji ID-jevi nisu isti, promijeni ih u `POO_EMOJIS` rječniku:

```python
POO_EMOJIS = {
    "main":        "<:pooplove:TVOJ_ID>",
    "hungry":      "<:pleadpoop:TVOJ_ID>",
    "veryhungry":  "<:cryingpoop:TVOJ_ID>",
    "sad":         "<:poopsad:TVOJ_ID>",
    "angry":       "<:angrypoop:TVOJ_ID>",
    "cowboy":      "<:angrycowboypoop:TVOJ_ID>",
    "heartbroken": "<:heartbrokenpoop:TVOJ_ID>",
    "holy":        "<:holyshit:TVOJ_ID>",
    "satisfied":   "<:satisfied:TVOJ_ID>",
    "sleeping":    "<:satisfied:TVOJ_ID>",
    "hardcry":     "<:hardcry:TVOJ_ID>",
    "tired":       "<:hardcry:TVOJ_ID>",
    "working":     "<:poopsussysweat:TVOJ_ID>",
    "sweat":       "<:poopsussysweat:TVOJ_ID>",
    "disgusted":   "<:poopdisgusted:TVOJ_ID>",
    "dirty":       "<:poopdisgusted:TVOJ_ID>",
}
```

ID-jevi koje vidiš na screenshotu:
```
heartbrokenpoop  → 1502906810971979807
angrypoop        → 1502906809269096468
angrycowboypoop  → 1502906807234859028
poopsad          → 1502906805334966374
pooplove         → 1502906803317379102
holyshit         → 1502906801178280076
satisfied        → 1502906795380814456
hardcry          → 1502906795189076039
poopsussysweat   → 1502906790650712215
cryingpoop       → 1502906783172399224
pleadpoop        → 1502906780177530951
poopdisgusted    → 1502906775609934005
```

---

### 🔔 DM Notifikacije
Bot automatski šalje DM notifikacije kada:
- 🍗 Poo je gladan (glad < 30%)
- 🧼 Poo je prljav (čistoća < 30%)
- 😔 Poo je dosađuje (sreća < 30%)
- 😪 Poo je umoran (energija < 25%)
- ☀️ Poo se probudio nakon spavanja

Cooldown između DM-ova iste vrste: **3 sata**

---

### 💾 Podaci
Podaci se čuvaju u `poo_personal_data.json` u istom folderu kao bot.
Svaki igrač ima zaseban zapis po user ID-u.
