# ╔══════════════════════════════════════════════════════════════════╗
# ║           🐾  GIANNI — PERSONAL POO GAME  🐾                   ║
# ║   Svaki član ima SVOG Poo-a! Brine se, hrani, igra, radi...    ║
# ║   Lijepi emberi, DM notifikacije, custom emoji stanja          ║
# ╚══════════════════════════════════════════════════════════════════╝

import discord
import asyncio
import json
import os
import random
from datetime import datetime, timezone, timedelta
from discord import app_commands
from discord.ext import commands, tasks

# ═══════════════════════════════════════════════════════════════
#   CUSTOM POO EMOJI IDS (iz bota — GIANNI Custom)
#   Format: <:name:id>
# ═══════════════════════════════════════════════════════════════
POO_EMOJIS = {
    "main":        "<:poopoo:1502906803317379102>",   # normalan / sretan poo (ljubav)  → pooplove
    "happy":       "<:pooplove:1502906803317379102>",
    "hungry":      "<:pleadpoop:1502906780177530951>",
    "veryhungry":  "<:cryingpoop:1502906783172399224>",
    "sad":         "<:poopsad:1502906805334966374>",
    "angry":       "<:angrypoop:1502906809269096468>",
    "cowboy":      "<:angrycowboypoop:1502906807234859028>",
    "heartbroken": "<:heartbrokenpoop:1502906810971979807>",
    "holy":        "<:holyshit:1502906801178280076>",
    "satisfied":   "<:satisfied:1502906795380814456>",
    "sleeping":    "<:satisfied:1502906795380814456>",
    "hardcry":     "<:hardcry:1502906795189076039>",
    "tired":       "<:hardcry:1502906795189076039>",
    "working":     "<:poopsussysweat:1502906790650712215>",
    "sweat":       "<:poopsussysweat:1502906790650712215>",
    "disgusted":   "<:poopdisgusted:1502906775609934005>",
    "dirty":       "<:poopdisgusted:1502906775609934005>",
}

# ═══════════════════════════════════════════════════════════════
#   BOJ — boja embera po stanju poo-a
# ═══════════════════════════════════════════════════════════════
POO_COLORS = {
    "happy":       0x8B4513,   # topla smeđa
    "hungry":      0xE74C3C,   # crvena — alarm
    "sad":         0x546E7A,   # plavo-siva — tuga
    "dirty":       0x795548,   # tamna smeđa
    "sleeping":    0x5C6BC0,   # indigo — mirno
    "working":     0xF39C12,   # zlatna — aktivan
    "sick":        0x66BB6A,   # zelena — bolesno
    "angry":       0xC62828,   # tamno crvena
    "holy":        0xFFD700,   # zlatna — legendaran
    "default":     0x8D6E63,   # standardna smeđa
}

# ═══════════════════════════════════════════════════════════════
#   FAZE RASTA POO-A
# ═══════════════════════════════════════════════════════════════
POO_STAGES = [
    (0,     "💩",  "Beba Poo",       "Tek se rodio! Treba puno ljubavi."),
    (100,   "💩",  "Mali Poo",       "Raste brže nego što misliš!"),
    (300,   "💩",  "Poo Junior",     "Već ima svoju ličnost."),
    (600,   "💩",  "Poo Tinejdžer",  "Tvrdoglav, ali sladak."),
    (1000,  "💩",  "Poo Odrasli",    "Ozbiljan Poo koji zna što hoće."),
    (1500,  "💩",  "Poo Veteran",    "Iskusan — preživio je mnogo!"),
    (2200,  "💩",  "Poo Legenda",    "Malo ih je dostiglo ovu fazu..."),
    (3000,  "💩",  "Poo Besmrtni",   "Transcendirao je. Sveti Poo."),
]

# ═══════════════════════════════════════════════════════════════
#   RADNI POSLOVI — za /mypoo work
# ═══════════════════════════════════════════════════════════════
POO_JOBS = [
    ("🧹 Pomeo ulicu",          15, 20),
    ("🍕 Dostavljao pizzu",     20, 30),
    ("🔧 Popravljao slavinu",   18, 25),
    ("🛒 Nosio namirnice baki", 12, 18),
    ("📦 Slagao kutije",        15, 22),
    ("🚗 Prao automobile",      20, 28),
    ("🌿 Rezao travu",          14, 20),
    ("📫 Nosio poštu",          16, 24),
    ("🎪 Čuvao parking",        10, 16),
    ("🏗️ Radio na građevini",   25, 35),
    ("🥐 Pomagao u pekari",     18, 26),
    ("🐑 Čuvao ovce",           12, 20),
    ("🍺 Konobarisao",          22, 32),
    ("📚 Učio kao demonstrator",20, 28),
    ("🎭 Glumio ulični muzičar", 15, 25),
    ("🌶️ Brao paprike",         13, 19),
    ("💪 Radio kao zaštitar",   24, 34),
    ("🚕 Vozio taksi noću",     28, 38),
    ("🧓 Čuvao baku",           10, 14),
    ("🥙 Prodavao ćevape",      20, 30),
]

# ═══════════════════════════════════════════════════════════════
#   HRANA — /mypoo feed izbori
# ═══════════════════════════════════════════════════════════════
POO_FOODS = [
    ("🍗 Piletina",   30, 10, 5,  35),
    ("🥩 Biftek",     40, 15, 8,  60),
    ("🥗 Salata",     20,  5, 3,  15),
    ("🍕 Pizza",      35, 20, 5,  40),
    ("🍜 Ramen",      25, 10, 5,  25),
    ("🥐 Kroasan",    15,  5, 2,  10),
    ("🍰 Tortica",    20, 25, 3,  30),
    ("🥙 Ćevapi",     35, 15, 5,  45),
    ("🍩 Krofna",     25, 20, 5,  20),
    ("🥛 Mlijeko",    15,  5, 10, 10),
]

# ═══════════════════════════════════════════════════════════════
#   IGRE — /mypoo play
# ═══════════════════════════════════════════════════════════════
POO_GAMES = [
    "🎯 Bacali ste strelice zajedno",
    "⚽ Igrali ste fudbal u dvorištu",
    "🎮 Upali ste konzolu i igrali do ponoći",
    "🃏 Odigrali kartaški dvoboj",
    "🎲 Bacali kocku i smijali se",
    "🎸 Svirali gitaru i pjevali",
    "🧩 Složili zagonetku zajedno",
    "🎳 Otišli na kuglanje",
    "🏊 Plivali u bazenu",
    "🛸 Zamišljali avanture svemira",
    "🎠 Vozili vrtuljak na sajmu",
    "🎯 Gađali metu na strelištu",
    "🎡 Bili na vašaru i jeli šećernu vunu",
    "🚴 Vozili bicikl kroz park",
    "🎪 Gledali cirkus zajedno",
]

# ═══════════════════════════════════════════════════════════════
#   DM NOTIFIKACIJE — poruke koje GIANNI šalje u DM
# ═══════════════════════════════════════════════════════════════
DM_MESSAGES = {
    "hungry": [
        "🍗 **{poo_name}** je gladan! Nahrani ga brzo — koristi `/mypoo feed`! {emoji}",
        "😭 Poo vrišti od gladi! **{poo_name}** čeka svoju porciju! `/mypoo feed`",
        "🚨 Upozorenje! **{poo_name}** nije jeo već dugo. Nahrani ga! `/mypoo feed`",
        "🥺 **{poo_name}**: *'Umirit ću se od gladi...'* Nahrani me! `/mypoo feed`",
    ],
    "dirty": [
        "🧼 **{poo_name}** smrdi ko sto poo-a! Operaj ga — `/mypoo clean`! {emoji}",
        "😤 **{poo_name}** je jako prljav. Zguraj ga pod tuš! `/mypoo clean`",
        "💀 Komšije se žale! **{poo_name}** treba hitno kupanje. `/mypoo clean`",
    ],
    "bored": [
        "😴 **{poo_name}** je dosađuje sam... Poigraj se s njim! `/mypoo play` {emoji}",
        "🎮 **{poo_name}** pita te: *'Hoćemo li igrati nešto?'* `/mypoo play`",
        "🥺 **{poo_name}** te čeka da se vratiš! `/mypoo play`",
    ],
    "tired": [
        "😪 **{poo_name}** je umoran — pošalji ga na spavanje! `/mypoo sleep` {emoji}",
        "💤 **{poo_name}** jedva drži oči otvorene. `/mypoo sleep`",
    ],
    "sick": [
        "🤒 **{poo_name}** nije dobro! Nahrani ga i poigraj se da se oporavi! `/mypoo feed`",
        "🏥 Pažnja! **{poo_name}** mu trebaju briga i pažnja! `/mypoo feed` `/mypoo play`",
    ],
    "levelup": [
        "🎉 **{poo_name}** je narastao! Dostigao je fazu **{stage}**! Čestitamo! 🐾",
        "⬆️ Napredak! **{poo_name}** je sada **{stage}**! Nastavi tako! 💩",
    ],
}

# ═══════════════════════════════════════════════════════════════
#   DATA STORAGE
# ═══════════════════════════════════════════════════════════════
POO_DATA_FILE = "poo_personal_data.json"

def load_poo_data() -> dict:
    if os.path.exists(POO_DATA_FILE):
        try:
            with open(POO_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_poo_data(data: dict):
    with open(POO_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

poo_data: dict = load_poo_data()

def get_poo(user_id: int) -> dict | None:
    return poo_data.get(str(user_id))

def get_or_create_poo(user_id: int, name: str = "Poo") -> dict:
    uid = str(user_id)
    if uid not in poo_data:
        poo_data[uid] = {
            "name":        name,
            "xp":          0,
            "level":       0,
            "hunger":      80,
            "happiness":   80,
            "cleanliness": 80,
            "energy":      80,
            "health":      100,
            "born_at":     int(datetime.now(timezone.utc).timestamp()),
            "last_feed":   0,
            "last_play":   0,
            "last_clean":  0,
            "last_sleep":  0,
            "last_work":   0,
            "last_daily":  0,
            "total_feeds": 0,
            "total_plays": 0,
            "total_works": 0,
            "sleeping":    False,
            "sleep_until": 0,
            "coins":       100,
            "last_dm_hungry":  0,
            "last_dm_dirty":   0,
            "last_dm_bored":   0,
            "last_dm_tired":   0,
        }
        save_poo_data(poo_data)
    return poo_data[uid]

# ═══════════════════════════════════════════════════════════════
#   HELPERS
# ═══════════════════════════════════════════════════════════════
def _stage(xp: int) -> tuple:
    stage = POO_STAGES[0]
    for s in POO_STAGES:
        if xp >= s[0]:
            stage = s
        else:
            break
    return stage

def _next_stage(xp: int) -> tuple | None:
    for i, s in enumerate(POO_STAGES):
        if xp < s[0]:
            return s
    return None

def _bar(value: int, max_val: int = 100, length: int = 10) -> str:
    filled = round((value / max_val) * length)
    filled = max(0, min(length, filled))
    bar = "█" * filled + "░" * (length - filled)
    pct = int((value / max_val) * 100)
    return f"`{bar}` **{pct}%**"

def _stat_emoji(value: int) -> str:
    if value >= 80: return "💚"
    if value >= 50: return "💛"
    if value >= 25: return "🟠"
    return "❤️"

def _decay_stats(p: dict):
    """Smanji statistike s vremenom (poziva se pri svakom pregledu)."""
    now = int(datetime.now(timezone.utc).timestamp())
    hours_since = (now - p.get("born_at", now)) / 3600.0

    # Decay po satu — agresivniji kada je Poo stariji
    base_decay = 2.5
    p["hunger"]      = max(0, p.get("hunger",      100) - base_decay * 0.5)
    p["happiness"]   = max(0, p.get("happiness",   100) - base_decay * 0.4)
    p["cleanliness"] = max(0, p.get("cleanliness", 100) - base_decay * 0.3)
    p["energy"]      = max(0, p.get("energy",      100) - base_decay * 0.3)

    # Zdravlje pada samo ako je gladan ili prljav
    if p.get("hunger", 100) < 20 or p.get("cleanliness", 100) < 20:
        p["health"] = max(0, p.get("health", 100) - 1)
    else:
        p["health"] = min(100, p.get("health", 100) + 0.2)

def _get_poo_state(p: dict) -> str:
    """Odredi trenutno stanje Poo-a na osnovu statistika."""
    if p.get("sleeping", False):
        return "sleeping"
    hunger = p.get("hunger", 100)
    happy  = p.get("happiness", 100)
    clean  = p.get("cleanliness", 100)
    energy = p.get("energy", 100)
    health = p.get("health", 100)

    if hunger <= 10:   return "veryhungry"
    if hunger <= 30:   return "hungry"
    if clean  <= 20:   return "dirty"
    if happy  <= 15:   return "heartbroken"
    if happy  <= 30:   return "sad"
    if energy <= 20:   return "tired"
    if health <= 40:   return "sick"  # sick nema custom emoji, koristimo disgusted
    if happy  >= 90 and hunger >= 80: return "happy"
    if energy <= 40:   return "working"
    return "main"

def _get_emoji_for_state(state: str) -> str:
    mapping = {
        "sleeping":    POO_EMOJIS["sleeping"],
        "veryhungry":  POO_EMOJIS["veryhungry"],
        "hungry":      POO_EMOJIS["hungry"],
        "dirty":       POO_EMOJIS["disgusted"],
        "heartbroken": POO_EMOJIS["heartbroken"],
        "sad":         POO_EMOJIS["sad"],
        "tired":       POO_EMOJIS["tired"],
        "sick":        POO_EMOJIS["disgusted"],
        "happy":       POO_EMOJIS["happy"],
        "working":     POO_EMOJIS["working"],
        "main":        POO_EMOJIS["main"],
        "angry":       POO_EMOJIS["angry"],
    }
    return mapping.get(state, POO_EMOJIS["main"])

def _get_color_for_state(state: str) -> int:
    mapping = {
        "sleeping":    POO_COLORS["sleeping"],
        "veryhungry":  POO_COLORS["hungry"],
        "hungry":      POO_COLORS["hungry"],
        "dirty":       POO_COLORS["dirty"],
        "heartbroken": POO_COLORS["sad"],
        "sad":         POO_COLORS["sad"],
        "tired":       POO_COLORS["default"],
        "sick":        POO_COLORS["sick"],
        "happy":       POO_COLORS["happy"],
        "working":     POO_COLORS["working"],
        "main":        POO_COLORS["default"],
    }
    return mapping.get(state, POO_COLORS["default"])

def _state_label(state: str) -> str:
    labels = {
        "sleeping":    "😴 Spava",
        "veryhungry":  "😭 Umire od gladi!",
        "hungry":      "🥺 Gladan",
        "dirty":       "🤢 Jako prljav",
        "heartbroken": "💔 Slomljenog srca",
        "sad":         "😢 Tužan",
        "tired":       "😪 Umoran",
        "sick":        "🤒 Bolestan",
        "happy":       "😍 Presretan",
        "working":     "💪 Aktivan",
        "main":        "😊 Dobro raspoložen",
        "angry":       "😡 Ljut",
    }
    return labels.get(state, "💩 Normalan")

def _age_str(born_ts: int) -> str:
    now = datetime.now(timezone.utc)
    born = datetime.fromtimestamp(born_ts, tz=timezone.utc)
    delta = now - born
    days = delta.days
    hours = delta.seconds // 3600
    if days == 0:
        return f"{hours}h"
    if days < 7:
        return f"{days}d {hours}h"
    weeks = days // 7
    return f"{weeks} nedjelja {days % 7}d"

def _cooldown_left(last_ts: int, cooldown_sec: int) -> int:
    """Vrati koliko sekundi je ostalo do sljedećeg korišćenja. 0 = može."""
    now = int(datetime.now(timezone.utc).timestamp())
    elapsed = now - last_ts
    remaining = cooldown_sec - elapsed
    return max(0, remaining)

# ═══════════════════════════════════════════════════════════════
#   EMBED BUILDER — srce sustava
# ═══════════════════════════════════════════════════════════════
def build_poo_embed(p: dict, user: discord.User | discord.Member, title_override: str = None) -> discord.Embed:
    _decay_stats(p)
    save_poo_data(poo_data)

    state = _get_poo_state(p)
    emoji = _get_emoji_for_state(state)
    color = _get_color_for_state(state)
    stage_xp, stage_art, stage_name, stage_desc = _stage(p.get("xp", 0))
    next_s = _next_stage(p.get("xp", 0))

    poo_name = p.get("name", "Poo")
    hunger   = int(p.get("hunger",      100))
    happy    = int(p.get("happiness",   100))
    clean    = int(p.get("cleanliness", 100))
    energy   = int(p.get("energy",      100))
    health   = int(p.get("health",      100))
    xp       = p.get("xp", 0)
    coins    = p.get("coins", 0)

    # ── Vizualni prikaz Poo-a u emberu ──
    poo_display = (
        f"\n"
        f"{'　' * 4}{emoji}\n"
        f"{'　' * 4}{emoji}\n"
        f"{'　' * 3}{emoji}{emoji}{emoji}\n"
    )

    # ── Title ──
    title = title_override or f"🐾  {poo_name}  •  {stage_name}"

    # ── Opis / stanje ──
    state_txt  = _state_label(state)
    age_txt    = _age_str(p.get("born_at", int(datetime.now(timezone.utc).timestamp())))
    born_ts    = p.get("born_at", int(datetime.now(timezone.utc).timestamp()))
    works_done = p.get("total_works", 0)
    feeds_done = p.get("total_feeds", 0)
    plays_done = p.get("total_plays", 0)

    desc = (
        f"**Vlasnik:** {user.mention}\n"
        f"**Stanje:** {state_txt}\n"
        f"**Starost:** `{age_txt}` • **Faza:** `{stage_name}`\n"
        f"**XP:** `{xp:,}` 🌟 • **Coins:** `{coins:,}` 💶\n"
        f"\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"\n"
        f"```\n"
        f"        ╔══════════╗\n"
        f"        ║   POO    ║\n"
        f"        ╚══════════╝\n"
        f"```"
    )

    embed = discord.Embed(
        title=title,
        description=desc,
        color=color,
        timestamp=datetime.now(timezone.utc),
    )

    # ── Slika: koristimo thumbnail sa Poo emoji prikazom ──
    # Koristimo autora da prikažemo avatar vlasnika
    embed.set_author(
        name=f"{user.display_name} • Poo vlasnik",
        icon_url=user.display_avatar.url,
    )

    # ── Stats polje ──
    stats_lines = (
        f"🍗 **Glad**       {_stat_emoji(hunger)} {_bar(hunger)}\n"
        f"😊 **Sreća**      {_stat_emoji(happy)}  {_bar(happy)}\n"
        f"🧼 **Čistoća**    {_stat_emoji(clean)}  {_bar(clean)}\n"
        f"⚡ **Energija**   {_stat_emoji(energy)} {_bar(energy)}\n"
        f"❤️ **Zdravlje**   {_stat_emoji(health)} {_bar(health)}"
    )
    embed.add_field(name="📊  Statistike", value=stats_lines, inline=False)

    # ── Aktivnosti ──
    act_lines = (
        f"🍽️ Nahranjen: **{feeds_done}×**  •  "
        f"🎮 Igrao: **{plays_done}×**  •  "
        f"💼 Radio: **{works_done}×**"
    )
    embed.add_field(name="🏅  Aktivnosti", value=act_lines, inline=False)

    # ── XP Progress ──
    if next_s:
        needed = next_s[0] - xp
        xp_bar_len = 12
        prev_xp = stage_xp
        total_needed = next_s[0] - prev_xp
        current_prog = xp - prev_xp
        filled = round((current_prog / max(1, total_needed)) * xp_bar_len)
        filled = max(0, min(xp_bar_len, filled))
        prog_bar = "▰" * filled + "▱" * (xp_bar_len - filled)
        xp_field = f"`{prog_bar}` **{xp:,}** / **{next_s[0]:,}** XP\n*Još `{needed:,}` XP do {next_s[2]}*"
    else:
        xp_field = f"🏆 **MAKSIMALNA FAZA DOSTIGNUTA!**\n`{xp:,}` XP — Sveti Poo!"

    embed.add_field(name="⬆️  Napredak", value=xp_field, inline=False)

    # ── Footer ──
    embed.set_footer(text=f"🐾 GIANNI Poo Game  •  {stage_desc}  •  /mypoo help")

    return embed


def build_mini_embed(p: dict, user: discord.User | discord.Member, action_text: str, color: int = None) -> discord.Embed:
    """Mali embed za DM notifikacije i akcije."""
    _decay_stats(p)
    state = _get_poo_state(p)
    emoji = _get_emoji_for_state(state)
    poo_name = p.get("name", "Poo")
    embed_color = color or _get_color_for_state(state)

    hunger  = int(p.get("hunger",      100))
    happy   = int(p.get("happiness",   100))
    clean   = int(p.get("cleanliness", 100))
    energy  = int(p.get("energy",      100))

    embed = discord.Embed(
        title=f"{emoji}  {poo_name}",
        description=action_text,
        color=embed_color,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(
        name=f"{user.display_name}",
        icon_url=user.display_avatar.url,
    )
    quick_stats = (
        f"🍗 {hunger}%  😊 {happy}%  🧼 {clean}%  ⚡ {energy}%"
    )
    embed.add_field(name="📊 Stanje", value=quick_stats, inline=False)
    embed.set_footer(text="🐾 GIANNI Poo Game  •  /mypoo status za detalje")
    return embed


# ═══════════════════════════════════════════════════════════════
#   COG — Personal Poo Game
# ═══════════════════════════════════════════════════════════════
class PersonalPooGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.dm_notifier.start()
        self.stat_decay_loop.start()

    def cog_unload(self):
        self.dm_notifier.cancel()
        self.stat_decay_loop.cancel()

    # ─── Background: decay svaki sat ───────────────────────────────
    @tasks.loop(minutes=60)
    async def stat_decay_loop(self):
        """Smanjuje statistike Poo-a svakih sat vremena."""
        for uid, p in poo_data.items():
            _decay_stats(p)
        save_poo_data(poo_data)

    @stat_decay_loop.before_loop
    async def before_decay(self):
        await self.bot.wait_until_ready()

    # ─── Background: DM notifikacije ───────────────────────────────
    @tasks.loop(minutes=30)
    async def dm_notifier(self):
        """Šalje DM notifikacije vlasnicima čiji Poo treba pažnju."""
        now = int(datetime.now(timezone.utc).timestamp())
        dm_cooldown = 3 * 3600  # 3 sata između DM-ova iste vrste

        for uid, p in list(poo_data.items()):
            try:
                user = await self.bot.fetch_user(int(uid))
                poo_name = p.get("name", "Poo")
                state = _get_poo_state(p)
                emoji = _get_emoji_for_state(state)

                async def send_dm(dm_type: str, dm_last_key: str, msg_list: list, **fmt_kw):
                    last = p.get(dm_last_key, 0)
                    if now - last < dm_cooldown:
                        return
                    msg = random.choice(msg_list).format(
                        poo_name=poo_name, emoji=emoji, **fmt_kw
                    )
                    embed = discord.Embed(
                        title=f"🔔  Poo Notifikacija — {poo_name}",
                        description=msg,
                        color=_get_color_for_state(state),
                        timestamp=datetime.now(timezone.utc),
                    )
                    embed.add_field(
                        name="📊 Brzo stanje",
                        value=(
                            f"🍗 Glad: `{int(p.get('hunger',100))}%`  "
                            f"😊 Sreća: `{int(p.get('happiness',100))}%`\n"
                            f"🧼 Čistoća: `{int(p.get('cleanliness',100))}%`  "
                            f"⚡ Energija: `{int(p.get('energy',100))}%`"
                        ),
                        inline=False,
                    )
                    embed.set_footer(text="🐾 GIANNI Poo Game — tvoj Poo te treba!")
                    try:
                        await user.send(embed=embed)
                        p[dm_last_key] = now
                        save_poo_data(poo_data)
                    except (discord.Forbidden, discord.HTTPException):
                        pass  # DM zaključan — preskočimo

                hunger = p.get("hunger", 100)
                clean  = p.get("cleanliness", 100)
                happy  = p.get("happiness", 100)
                energy = p.get("energy", 100)

                if hunger < 30:
                    await send_dm("hungry", "last_dm_hungry", DM_MESSAGES["hungry"])
                elif clean < 30:
                    await send_dm("dirty", "last_dm_dirty", DM_MESSAGES["dirty"])
                elif happy < 30:
                    await send_dm("bored", "last_dm_bored", DM_MESSAGES["bored"])
                elif energy < 25:
                    await send_dm("tired", "last_dm_tired", DM_MESSAGES["tired"])

            except Exception:
                continue

    @dm_notifier.before_loop
    async def before_notifier(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(60)  # Sačekaj minutu od starta


# ═══════════════════════════════════════════════════════════════
#   SLASH KOMANDE — /mypoo ...
# ═══════════════════════════════════════════════════════════════
mypoo_group = app_commands.Group(
    name="mypoo",
    description="🐾 Tvoj osobni Poo — hrani ga, igraj se, brini o njemu!"
)


@mypoo_group.command(name="start", description="🐾 Pokreni svog osobnog Poo-a!")
@app_commands.describe(ime="Kako ćeš nazvati svog Poo-a? (opciono)")
async def mypoo_start(i: discord.Interaction, ime: str = None):
    uid = str(i.user.id)
    if uid in poo_data:
        p = poo_data[uid]
        embed = build_poo_embed(p, i.user, f"🐾 Tvoj Poo već postoji!")
        return await i.response.send_message(
            content="❗ Već imaš svog Poo-a! Evo ga:",
            embed=embed,
            ephemeral=True
        )

    poo_name = (ime or f"{i.user.display_name}'s Poo")[:30]
    p = get_or_create_poo(i.user.id, poo_name)

    # ── Dobrodošli embed ──
    state_emoji = POO_EMOJIS["happy"]
    embed = discord.Embed(
        title=f"🥚  Dobrodošao, {poo_name}!",
        description=(
            f"**{i.user.mention}**, tvoj Poo je upravo **rođen**! 🎉\n\n"
            f"{state_emoji}  ← Ovo je tvoj novi Poo prijatelj!\n\n"
            f"Brini se o njemu — nahrani ga, igraj se s njim,\n"
            f"drži ga čistim i zdravim dok ne postane **Sveti Poo**! 💩✨\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🍗 **Hrani ga**: `/mypoo feed`\n"
            f"🎮 **Igraj se**: `/mypoo play`\n"
            f"🧼 **Operaj ga**: `/mypoo clean`\n"
            f"💼 **Pošalji na posao**: `/mypoo work`\n"
            f"😴 **Spavanje**: `/mypoo sleep`\n"
            f"📊 **Status**: `/mypoo status`\n"
            f"🎁 **Dnevna nagrada**: `/mypoo daily`\n"
        ),
        color=POO_COLORS["happy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(
        name=f"{i.user.display_name} • Novi Poo Vlasnik! 🐾",
        icon_url=i.user.display_avatar.url,
    )
    embed.add_field(
        name="💡 Savjet",
        value=(
            f"Gianni bot će ti slati **DM notifikacije** kada Poo treba pažnju!\n"
            f"Otvori DM-ove od botova ako ih imaš zaključane 📬"
        ),
        inline=False,
    )
    embed.set_footer(text="🐾 GIANNI Poo Game  •  Počni svoju Poo avanturu!")

    await i.response.send_message(embed=embed)


@mypoo_group.command(name="status", description="📊 Pogledaj status svog Poo-a")
async def mypoo_status(i: discord.Interaction):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(
                title="❌  Nemaš Poo-a!",
                description="Pokreni svog Poo-a sa `/mypoo start` 🐾",
                color=0xE74C3C
            ),
            ephemeral=True
        )
    embed = build_poo_embed(p, i.user)
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="feed", description="🍗 Nahrani svog Poo-a")
@app_commands.describe(hrana="Izaberi šta ćeš dati Poo-u za jelo")
@app_commands.choices(hrana=[
    app_commands.Choice(name="🍗 Piletina (35💶)",  value="0"),
    app_commands.Choice(name="🥩 Biftek (60💶)",    value="1"),
    app_commands.Choice(name="🥗 Salata (15💶)",    value="2"),
    app_commands.Choice(name="🍕 Pizza (40💶)",      value="3"),
    app_commands.Choice(name="🍜 Ramen (25💶)",      value="4"),
    app_commands.Choice(name="🥐 Kroasan (10💶)",    value="5"),
    app_commands.Choice(name="🍰 Tortica (30💶)",    value="6"),
    app_commands.Choice(name="🥙 Ćevapi (45💶)",     value="7"),
    app_commands.Choice(name="🍩 Krofna (20💶)",     value="8"),
    app_commands.Choice(name="🥛 Mlijeko (10💶)",    value="9"),
])
async def mypoo_feed(i: discord.Interaction, hrana: str = "0"):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!", description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True
        )

    # Cooldown: 20 minuta
    cd_left = _cooldown_left(p.get("last_feed", 0), 1200)
    if cd_left > 0:
        mins = cd_left // 60
        secs = cd_left % 60
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo nije gladan!",
                description=f"Možeš ponovo hraniti za **{mins}m {secs}s**\n*Poo treba da svari prethodnog obroka!*",
                color=0xF39C12
            ),
            ephemeral=True
        )

    food_idx = int(hrana)
    food_name, hunger_gain, happy_gain, clean_gain, cost = POO_FOODS[food_idx]

    if p.get("coins", 0) < cost:
        return await i.response.send_message(
            embed=discord.Embed(
                title="❌ Nemaš dovoljno coina!",
                description=f"{food_name} košta **{cost} 💶**\nImaš: **{p.get('coins',0)} 💶**\nZaradi više sa `/mypoo work` ili `/mypoo daily`!",
                color=0xE74C3C
            ),
            ephemeral=True
        )

    old_xp = p.get("xp", 0)
    old_stage = _stage(old_xp)[2]

    p["coins"]       = p.get("coins", 0) - cost
    p["hunger"]      = min(100, p.get("hunger",      0) + hunger_gain)
    p["happiness"]   = min(100, p.get("happiness",   0) + happy_gain)
    p["cleanliness"] = max(0,   p.get("cleanliness", 100) - clean_gain)  # jelo malo prlja
    p["xp"]          = p.get("xp", 0) + 10
    p["last_feed"]   = int(datetime.now(timezone.utc).timestamp())
    p["total_feeds"] = p.get("total_feeds", 0) + 1
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[2]
    level_up  = (new_stage != old_stage)

    state   = _get_poo_state(p)
    emoji   = _get_emoji_for_state(state)
    color   = POO_COLORS["happy"] if not level_up else POO_COLORS["holy"]

    desc = (
        f"{emoji} **{p.get('name','Poo')}** je pojeo/la {food_name}! 😋\n\n"
        f"+ **{hunger_gain}** 🍗 Glad  "
        f"+ **{happy_gain}** 😊 Sreća  "
        f"+ **10** 🌟 XP\n"
        f"- **{cost}** 💶 Coina"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"

    embed = build_mini_embed(p, i.user, desc, color=color)
    embed.title = f"🍗  Poo je nahranjen!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="play", description="🎮 Poigraj se sa svojim Poo-om")
async def mypoo_play(i: discord.Interaction):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!", description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True
        )

    if p.get("sleeping", False) and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
        return await i.response.send_message(
            embed=discord.Embed(
                title="😴 Poo spava!",
                description=f"**{p.get('name','Poo')}** je na odmoru. Neka spava! {POO_EMOJIS['sleeping']}\nProbudi se <t:{p['sleep_until']}:R>",
                color=POO_COLORS["sleeping"]
            ),
            ephemeral=True
        )

    # Cooldown: 15 minuta
    cd_left = _cooldown_left(p.get("last_play", 0), 900)
    if cd_left > 0:
        mins = cd_left // 60
        secs = cd_left % 60
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo je umoran od igre!",
                description=f"Možeš ponovo za **{mins}m {secs}s**\n*Poo treba malo odmora između igara!*",
                color=0xF39C12
            ),
            ephemeral=True
        )

    game = random.choice(POO_GAMES)
    old_xp = p.get("xp", 0)
    old_stage = _stage(old_xp)[2]

    happy_gain  = random.randint(15, 30)
    energy_loss = random.randint(5, 15)
    xp_gain     = random.randint(8, 15)

    p["happiness"] = min(100, p.get("happiness", 0) + happy_gain)
    p["energy"]    = max(0,   p.get("energy",    100) - energy_loss)
    p["xp"]        = p.get("xp", 0) + xp_gain
    p["last_play"] = int(datetime.now(timezone.utc).timestamp())
    p["total_plays"] = p.get("total_plays", 0) + 1
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[2]
    level_up  = (new_stage != old_stage)

    emoji = POO_EMOJIS["happy"]
    desc  = (
        f"{emoji} {game}!\n\n"
        f"+ **{happy_gain}** 😊 Sreća  "
        f"+ **{xp_gain}** 🌟 XP\n"
        f"- **{energy_loss}** ⚡ Energija"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"

    embed = build_mini_embed(p, i.user, desc, color=POO_COLORS["happy"])
    embed.title = "🎮  Poo se igrao!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="clean", description="🧼 Očisti svog Poo-a")
async def mypoo_clean(i: discord.Interaction):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!", description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True
        )

    # Cooldown: 30 minuta
    cd_left = _cooldown_left(p.get("last_clean", 0), 1800)
    if cd_left > 0:
        mins = cd_left // 60
        secs = cd_left % 60
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo je već čist!",
                description=f"Možeš opet prati za **{mins}m {secs}s**",
                color=0xF39C12
            ),
            ephemeral=True
        )

    clean_gain = random.randint(30, 45)
    happy_gain = random.randint(5, 15)
    xp_gain    = 5

    old_clean = int(p.get("cleanliness", 100))
    p["cleanliness"] = min(100, p.get("cleanliness", 0) + clean_gain)
    p["happiness"]   = min(100, p.get("happiness",   0) + happy_gain)
    p["xp"]          = p.get("xp", 0) + xp_gain
    p["last_clean"]  = int(datetime.now(timezone.utc).timestamp())
    save_poo_data(poo_data)

    emoji = POO_EMOJIS["satisfied"]
    reactions = [
        f"Tuš pun pjene! {emoji} **{p.get('name','Poo')}** je sada svjež kao cvijet! 🌸",
        f"Sapun, voda, četka! {emoji} **{p.get('name','Poo')}** blista! ✨",
        f"Kupanje gotovo! {emoji} **{p.get('name','Poo')}** miriše predivno! 🌺",
        f"Malo šampona i voilà! {emoji} **{p.get('name','Poo')}** je čist ko suza! 💧",
    ]
    desc = (
        f"{random.choice(reactions)}\n\n"
        f"Čistoća: **{old_clean}%** → **{int(p['cleanliness'])}%**\n"
        f"+ **{clean_gain}** 🧼 Čistoća  "
        f"+ **{happy_gain}** 😊 Sreća  "
        f"+ **{xp_gain}** 🌟 XP"
    )
    embed = build_mini_embed(p, i.user, desc, color=0x00BCD4)
    embed.title = "🧼  Poo je opran!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="sleep", description="😴 Pošalji Poo-a na spavanje (obnavlja energiju)")
async def mypoo_sleep(i: discord.Interaction):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!", description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True
        )

    if p.get("sleeping", False) and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
        wake_ts = p.get("sleep_until", 0)
        return await i.response.send_message(
            embed=discord.Embed(
                title="😴 Već spava!",
                description=f"**{p.get('name','Poo')}** već spava {POO_EMOJIS['sleeping']}\nBudi se <t:{wake_ts}:R>",
                color=POO_COLORS["sleeping"]
            ),
            ephemeral=True
        )

    # Cooldown: 2 sata
    cd_left = _cooldown_left(p.get("last_sleep", 0), 7200)
    if cd_left > 0:
        hours = cd_left // 3600
        mins  = (cd_left % 3600) // 60
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo nije umoran!",
                description=f"Možeš ponovo poslati na spavanje za **{hours}h {mins}m**",
                color=0xF39C12
            ),
            ephemeral=True
        )

    now = int(datetime.now(timezone.utc).timestamp())
    sleep_duration = 2 * 3600  # 2 sata sna
    wake_time = now + sleep_duration

    p["sleeping"]    = True
    p["sleep_until"] = wake_time
    p["last_sleep"]  = now
    p["xp"]          = p.get("xp", 0) + 5
    save_poo_data(poo_data)

    emoji = POO_EMOJIS["sleeping"]
    desc = (
        f"{emoji} **{p.get('name','Poo')}** je legao spavati...\n\n"
        f"💤 *Slatki snovi, mali Poo!*\n\n"
        f"Budi se <t:{wake_time}:R>\n"
        f"Energija i sreća će se obnoviti dok spava! ⚡😊"
    )
    embed = discord.Embed(
        title="😴  Poo spava",
        description=desc,
        color=POO_COLORS["sleeping"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=f"{i.user.display_name}", icon_url=i.user.display_avatar.url)
    embed.set_footer(text="🐾 GIANNI Poo Game  •  Ne budi ga!")

    # Probuditi Poo-a automatski
    async def wake_poo():
        await asyncio.sleep(sleep_duration)
        if p.get("sleeping", False):
            p["sleeping"]    = False
            p["sleep_until"] = 0
            p["energy"]      = min(100, p.get("energy",     0) + 50)
            p["happiness"]   = min(100, p.get("happiness",  0) + 20)
            p["health"]      = min(100, p.get("health",     0) + 10)
            save_poo_data(poo_data)
            # DM notifikacija — probudio se
            try:
                user = await i.client.fetch_user(i.user.id)
                wake_embed = discord.Embed(
                    title=f"☀️  {p.get('name','Poo')} se probudio!",
                    description=(
                        f"{POO_EMOJIS['satisfied']} **{p.get('name','Poo')}** se upravo probudio!\n\n"
                        f"+ **50** ⚡ Energija\n"
                        f"+ **20** 😊 Sreća\n"
                        f"+ **10** ❤️ Zdravlje\n\n"
                        f"Vrati se i nahrani ga! `/mypoo feed`"
                    ),
                    color=POO_COLORS["happy"],
                    timestamp=datetime.now(timezone.utc),
                )
                wake_embed.set_footer(text="🐾 GIANNI Poo Game")
                await user.send(embed=wake_embed)
            except Exception:
                pass

    asyncio.create_task(wake_poo())

    await i.response.send_message(embed=embed)


@mypoo_group.command(name="work", description="💼 Pošalji Poo-a na posao (zarađuj coine i XP)")
async def mypoo_work(i: discord.Interaction):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!", description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True
        )

    if p.get("sleeping", False) and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
        return await i.response.send_message(
            embed=discord.Embed(
                title="😴 Poo spava!",
                description=f"Ne možeš slati na posao Poo-a koji spava! {POO_EMOJIS['sleeping']}",
                color=POO_COLORS["sleeping"]
            ),
            ephemeral=True
        )

    # Cooldown: 45 minuta
    cd_left = _cooldown_left(p.get("last_work", 0), 2700)
    if cd_left > 0:
        mins = cd_left // 60
        secs = cd_left % 60
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo je još na odmoru!",
                description=f"Možeš poslati na posao za **{mins}m {secs}s**\n*Treba mu odmor između smjena!*",
                color=0xF39C12
            ),
            ephemeral=True
        )

    if p.get("energy", 100) < 20:
        return await i.response.send_message(
            embed=discord.Embed(
                title="😪 Poo je previše umoran!",
                description=f"Energija je samo **{int(p.get('energy',0))}%**!\nPošalji ga da spava prvo — `/mypoo sleep`",
                color=POO_COLORS["sad"]
            ),
            ephemeral=True
        )

    job_name, xp_min, xp_max = random.choice(POO_JOBS)
    xp_gain    = random.randint(xp_min, xp_max)
    coins_gain = random.randint(xp_min // 2, xp_max)
    energy_loss = random.randint(10, 20)
    hunger_loss = random.randint(5, 15)

    old_xp    = p.get("xp", 0)
    old_stage = _stage(old_xp)[2]

    p["xp"]          = p.get("xp", 0) + xp_gain
    p["coins"]       = p.get("coins", 0) + coins_gain
    p["energy"]      = max(0, p.get("energy",    100) - energy_loss)
    p["hunger"]      = max(0, p.get("hunger",    100) - hunger_loss)
    p["last_work"]   = int(datetime.now(timezone.utc).timestamp())
    p["total_works"] = p.get("total_works", 0) + 1
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[2]
    level_up  = (new_stage != old_stage)

    emoji = POO_EMOJIS["working"]
    desc  = (
        f"{emoji} **{p.get('name','Poo')}** {job_name}\n\n"
        f"+ **{xp_gain}** 🌟 XP  "
        f"+ **{coins_gain}** 💶 Coina\n"
        f"- **{energy_loss}** ⚡ Energija  "
        f"- **{hunger_loss}** 🍗 Glad"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"

    embed = build_mini_embed(p, i.user, desc, color=POO_COLORS["working"])
    embed.title = "💼  Poo je radio!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="daily", description="🎁 Preuzmi dnevnu nagradu za svog Poo-a")
async def mypoo_daily(i: discord.Interaction):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!", description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True
        )

    now  = int(datetime.now(timezone.utc).timestamp())
    last = p.get("last_daily", 0)
    midnight_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    midnight_ts    = int(midnight_today.timestamp())

    if last >= midnight_ts:
        next_midnight = midnight_today + timedelta(days=1)
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Već si preuzeo dnevnu nagradu!",
                description=f"Sljedeća nagrada dostupna <t:{int(next_midnight.timestamp())}:R>",
                color=0xF39C12
            ),
            ephemeral=True
        )

    coins_reward = random.randint(50, 150)
    xp_reward    = random.randint(20, 50)
    hunger_bonus = random.randint(10, 25)

    old_xp    = p.get("xp", 0)
    old_stage = _stage(old_xp)[2]

    p["coins"]      = p.get("coins",     0) + coins_reward
    p["xp"]         = p.get("xp",        0) + xp_reward
    p["hunger"]     = min(100, p.get("hunger",     0) + hunger_bonus)
    p["happiness"]  = min(100, p.get("happiness",  0) + 15)
    p["last_daily"] = now
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[2]
    level_up  = (new_stage != old_stage)

    emoji = POO_EMOJIS["happy"]
    desc  = (
        f"{emoji} **{p.get('name','Poo')}** je presretan!\n\n"
        f"🎁 **Dnevna nagrada:**\n"
        f"+ **{coins_reward}** 💶 Coina\n"
        f"+ **{xp_reward}** 🌟 XP\n"
        f"+ **{hunger_bonus}** 🍗 Glad\n"
        f"+ **15** 😊 Sreća\n\n"
        f"*Vrati se sutra po sljedeću nagradu!*"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"

    embed = build_mini_embed(p, i.user, desc, color=POO_COLORS["holy"])
    embed.title = "🎁  Dnevna Nagrada!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="rename", description="✏️ Promijeni ime svog Poo-a")
@app_commands.describe(novo_ime="Novo ime za tvog Poo-a (max 30 znakova)")
async def mypoo_rename(i: discord.Interaction, novo_ime: str):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!", description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True
        )
    if len(novo_ime) > 30:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Ime je predugačko!", description="Maksimum 30 znakova!", color=0xE74C3C),
            ephemeral=True
        )
    old_name   = p.get("name", "Poo")
    p["name"]  = novo_ime
    save_poo_data(poo_data)

    embed = discord.Embed(
        title="✏️  Poo preimenovan!",
        description=f"**{old_name}** → **{novo_ime}**\n\n{POO_EMOJIS['happy']} *Drago mu je novo ime!*",
        color=POO_COLORS["happy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=f"{i.user.display_name}", icon_url=i.user.display_avatar.url)
    embed.set_footer(text="🐾 GIANNI Poo Game")
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="leaderboard", description="🏆 Top 10 Poo-ova po XP-u")
async def mypoo_leaderboard(i: discord.Interaction):
    if not poo_data:
        return await i.response.send_message(
            embed=discord.Embed(
                title="🏆  Ljestvica prazna",
                description="Niko još nema Poo-a! Budi prvi — `/mypoo start`",
                color=0xF39C12
            ),
            ephemeral=True
        )

    sorted_poos = sorted(poo_data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]
    medals = ["🥇", "🥈", "🥉"] + [f"`#{n}`" for n in range(4, 11)]

    lines = []
    for idx, (uid, p) in enumerate(sorted_poos):
        xp        = p.get("xp", 0)
        poo_name  = p.get("name", "Poo")
        stage_n   = _stage(xp)[2]
        state     = _get_poo_state(p)
        emoji     = _get_emoji_for_state(state)
        try:
            member = i.guild.get_member(int(uid)) if i.guild else None
            username = member.display_name if member else f"Korisnik#{uid[-4:]}"
        except Exception:
            username = f"Korisnik#{uid[-4:]}"

        lines.append(
            f"{medals[idx]} **{poo_name}** *(vlasnik: {username})*\n"
            f"   {emoji} `{stage_n}` — **{xp:,} XP**"
        )

    embed = discord.Embed(
        title="🏆  TOP 10  —  Poo Ljestvica",
        description="\n\n".join(lines),
        color=POO_COLORS["holy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text="🐾 GIANNI Poo Game  •  /mypoo work za više XP!")
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="poo_info", description="👤 Pogledaj Poo-a nekog drugog igrača")
@app_commands.describe(korisnik="Čijeg Poo-a želiš vidjeti?")
async def mypoo_info(i: discord.Interaction, korisnik: discord.Member):
    p = get_poo(korisnik.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(
                title="❌ Nema Poo-a!",
                description=f"**{korisnik.display_name}** još nema svog Poo-a.",
                color=0xE74C3C
            ),
            ephemeral=True
        )
    embed = build_poo_embed(p, korisnik, f"🐾  {korisnik.display_name}'s Poo")
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="help", description="❓ Uputstvo za Poo Game")
async def mypoo_help(i: discord.Interaction):
    embed = discord.Embed(
        title="🐾  MYPOO — Uputstvo",
        description=(
            f"Svaki član ima **svog osobnog Poo-a**!\n"
            f"Brini se o njemu i gledaj kako raste! 💩\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=POO_COLORS["default"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.add_field(
        name="🚀 Početak",
        value=(
            "`/mypoo start [ime]` — Kreiraj svog Poo-a\n"
            "`/mypoo status` — Pogledaj statistike\n"
            "`/mypoo poo_info @korisnik` — Pogledaj tuđeg Poo-a"
        ),
        inline=False,
    )
    embed.add_field(
        name="🍗 Briga",
        value=(
            "`/mypoo feed [hrana]` — Nahrani Poo-a *(20 min CD)*\n"
            "`/mypoo clean` — Opere Poo-a *(30 min CD)*\n"
            "`/mypoo sleep` — Pošalji na spavanje *(2h CD, 2h sna)*\n"
            "`/mypoo play` — Igraj se *(15 min CD)*"
        ),
        inline=False,
    )
    embed.add_field(
        name="💰 Zarađivanje",
        value=(
            "`/mypoo work` — Pošalji na posao *(45 min CD)*\n"
            "`/mypoo daily` — Dnevna nagrada *(1× dnevno)*"
        ),
        inline=False,
    )
    embed.add_field(
        name="🏆 Ostalo",
        value=(
            "`/mypoo rename [ime]` — Promijeni ime\n"
            "`/mypoo leaderboard` — Top 10 Poo-ova"
        ),
        inline=False,
    )
    embed.add_field(
        name="📊 Statistike",
        value=(
            f"🍗 **Glad** — smanjuje se s vremenom\n"
            f"😊 **Sreća** — raste igrom, pada dosadivanjem\n"
            f"🧼 **Čistoća** — pada jedenjem i vremenom\n"
            f"⚡ **Energija** — troši se igrom i radom\n"
            f"❤️ **Zdravlje** — pada ako je gladan ili prljav"
        ),
        inline=False,
    )
    embed.add_field(
        name="🔔 DM Notifikacije",
        value="GIANNI bot ti šalje poruke u DM kada Poo treba pažnju!\nOtvori DM-ove od botova. 📬",
        inline=False,
    )

    faze_txt = "\n".join([f"`{s[0]:>5} XP` — **{s[2]}** {s[3]}" for s in POO_STAGES])
    embed.add_field(
        name="⬆️ Faze Rasta",
        value=faze_txt,
        inline=False,
    )
    embed.set_footer(text="🐾 GIANNI Poo Game  •  Poo te čeka!")
    await i.response.send_message(embed=embed, ephemeral=True)


# ═══════════════════════════════════════════════════════════════
#   SETUP FUNCTION — dodati u main bot
# ═══════════════════════════════════════════════════════════════
async def setup(bot: commands.Bot):
    """Registruje Personal Poo Game cog i slash komande."""
    cog = PersonalPooGame(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(mypoo_group)
    print("✅ PersonalPooGame Cog učitan!")
