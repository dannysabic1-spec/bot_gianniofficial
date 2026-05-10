# ╔══════════════════════════════════════════════════════════════════╗
# ║           🐾  GIANNI — PERSONAL POO GAME  🐾                   ║
# ║   Svaki član ima SVOG Poo-a! Brine se, hrani, igra, radi...    ║
# ║   Custom emoji, DM notifikacije, kanal restrikcija             ║
# ╚══════════════════════════════════════════════════════════════════╝

import discord
import asyncio
import json
import os
import random
from datetime import datetime, timezone, timedelta
from discord import app_commands
from discord.ext import commands, tasks

from config import POO_CHANNEL_ID

# ═══════════════════════════════════════════════════════════════
#   CUSTOM POO EMOJI IDS — GIANNI (Custom)
# ═══════════════════════════════════════════════════════════════
POO_EMOJIS = {
    "main":        "<:pooplove:1502906803317379102>",
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
#   BOJE EMBERA po stanju
# ═══════════════════════════════════════════════════════════════
POO_COLORS = {
    "happy":    0x8B4513,
    "hungry":   0xE74C3C,
    "sad":      0x546E7A,
    "dirty":    0x795548,
    "sleeping": 0x5C6BC0,
    "working":  0xF39C12,
    "sick":     0x66BB6A,
    "angry":    0xC62828,
    "holy":     0xFFD700,
    "default":  0x8D6E63,
}

# ═══════════════════════════════════════════════════════════════
#   FAZE RASTA
# ═══════════════════════════════════════════════════════════════
POO_STAGES = [
    (0,    "Beba Poo",      "Tek se rodio! Treba puno ljubavi."),
    (100,  "Mali Poo",      "Raste brže nego što misliš!"),
    (300,  "Poo Junior",    "Već ima svoju ličnost."),
    (600,  "Poo Tinejdžer", "Tvrdoglav, ali sladak."),
    (1000, "Poo Odrasli",   "Ozbiljan Poo koji zna što hoće."),
    (1500, "Poo Veteran",   "Iskusan — preživio je mnogo!"),
    (2200, "Poo Legenda",   "Malo ih je dostiglo ovu fazu..."),
    (3000, "Poo Besmrtni",  "Transcendirao je. Sveti Poo."),
]

# ═══════════════════════════════════════════════════════════════
#   RADNI POSLOVI
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
    ("💪 Radio kao zaštitar",   24, 34),
    ("🚕 Vozio taksi noću",     28, 38),
    ("🧓 Čuvao baku",           10, 14),
    ("🥙 Prodavao ćevape",      20, 30),
]

# ═══════════════════════════════════════════════════════════════
#   HRANA
# ═══════════════════════════════════════════════════════════════
POO_FOODS = [
    ("🍗 Piletina",  30, 10, 5,  35),
    ("🥩 Biftek",    40, 15, 8,  60),
    ("🥗 Salata",    20,  5, 3,  15),
    ("🍕 Pizza",     35, 20, 5,  40),
    ("🍜 Ramen",     25, 10, 5,  25),
    ("🥐 Kroasan",   15,  5, 2,  10),
    ("🍰 Tortica",   20, 25, 3,  30),
    ("🥙 Ćevapi",    35, 15, 5,  45),
    ("🍩 Krofna",    25, 20, 5,  20),
    ("🥛 Mlijeko",   15,  5, 10, 10),
]

# ═══════════════════════════════════════════════════════════════
#   IGRE
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
    "🎡 Bili na vašaru i jeli šećernu vunu",
    "🚴 Vozili bicikl kroz park",
    "🎪 Gledali cirkus zajedno",
]

# ═══════════════════════════════════════════════════════════════
#   DM PORUKE
# ═══════════════════════════════════════════════════════════════
DM_MESSAGES = {
    "hungry": [
        "🍗 **{poo_name}** je gladan! Nahrani ga brzo — `/mypoo feed`! {emoji}",
        "😭 Poo vrišti od gladi! **{poo_name}** čeka svoju porciju! `/mypoo feed`",
        "🚨 **{poo_name}** nije jeo već dugo. Nahrani ga! `/mypoo feed`",
    ],
    "dirty": [
        "🧼 **{poo_name}** smrdi! Operaj ga — `/mypoo clean`! {emoji}",
        "😤 **{poo_name}** je jako prljav. Zguraj ga pod tuš! `/mypoo clean`",
    ],
    "bored": [
        "😴 **{poo_name}** se dosađuje... Poigraj se s njim! `/mypoo play` {emoji}",
        "🎮 **{poo_name}** pita te: *'Hoćemo li igrati nešto?'* `/mypoo play`",
    ],
    "tired": [
        "😪 **{poo_name}** je umoran — pošalji ga na spavanje! `/mypoo sleep` {emoji}",
        "💤 **{poo_name}** jedva drži oči otvorene. `/mypoo sleep`",
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
    try:
        tmp = POO_DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, POO_DATA_FILE)
    except Exception as e:
        print(f"[poo-save] ERROR: {e}")


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
            "last_dm_hungry": 0,
            "last_dm_dirty":  0,
            "last_dm_bored":  0,
            "last_dm_tired":  0,
        }
        save_poo_data(poo_data)
    return poo_data[uid]


# ═══════════════════════════════════════════════════════════════
#   HELPER FUNKCIJE
# ═══════════════════════════════════════════════════════════════
def _stage(xp: int) -> tuple:
    result = POO_STAGES[0]
    for s in POO_STAGES:
        if xp >= s[0]:
            result = s
        else:
            break
    return result


def _next_stage(xp: int):
    for s in POO_STAGES:
        if xp < s[0]:
            return s
    return None


def _bar(value: int, length: int = 8) -> str:
    filled = max(0, min(length, round((value / 100) * length)))
    return "█" * filled + "░" * (length - filled)


def _stat_emoji(value: int) -> str:
    if value >= 80: return "💚"
    if value >= 50: return "💛"
    if value >= 25: return "🟠"
    return "❤️"


def _pct(value: int) -> str:
    return f"{int(value)}%"


def _decay_stats(p: dict):
    base_decay = 2.5
    p["hunger"]      = max(0, p.get("hunger",      100) - base_decay * 0.5)
    p["happiness"]   = max(0, p.get("happiness",   100) - base_decay * 0.4)
    p["cleanliness"] = max(0, p.get("cleanliness", 100) - base_decay * 0.3)
    p["energy"]      = max(0, p.get("energy",      100) - base_decay * 0.3)
    if p.get("hunger", 100) < 20 or p.get("cleanliness", 100) < 20:
        p["health"] = max(0, p.get("health", 100) - 1)
    else:
        p["health"] = min(100, p.get("health", 100) + 0.2)


def _get_poo_state(p: dict) -> str:
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
    if health <= 40:   return "sick"
    if happy  >= 90 and hunger >= 80: return "happy"
    return "main"


def _emoji(state: str) -> str:
    m = {
        "sleeping":    POO_EMOJIS["sleeping"],
        "veryhungry":  POO_EMOJIS["veryhungry"],
        "hungry":      POO_EMOJIS["hungry"],
        "dirty":       POO_EMOJIS["disgusted"],
        "heartbroken": POO_EMOJIS["heartbroken"],
        "sad":         POO_EMOJIS["sad"],
        "tired":       POO_EMOJIS["tired"],
        "sick":        POO_EMOJIS["disgusted"],
        "happy":       POO_EMOJIS["happy"],
        "main":        POO_EMOJIS["main"],
    }
    return m.get(state, POO_EMOJIS["main"])


def _color(state: str) -> int:
    m = {
        "sleeping":    POO_COLORS["sleeping"],
        "veryhungry":  POO_COLORS["hungry"],
        "hungry":      POO_COLORS["hungry"],
        "dirty":       POO_COLORS["dirty"],
        "heartbroken": POO_COLORS["sad"],
        "sad":         POO_COLORS["sad"],
        "tired":       POO_COLORS["default"],
        "sick":        POO_COLORS["sick"],
        "happy":       POO_COLORS["happy"],
        "main":        POO_COLORS["default"],
    }
    return m.get(state, POO_COLORS["default"])


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
        "main":        "😊 Dobro raspoložen",
    }
    return labels.get(state, "💩 Normalan")


def _age_str(born_ts: int) -> str:
    delta = datetime.now(timezone.utc) - datetime.fromtimestamp(born_ts, tz=timezone.utc)
    days  = delta.days
    hours = delta.seconds // 3600
    if days == 0:   return f"{hours}h"
    if days < 7:    return f"{days}d {hours}h"
    return f"{days // 7}ned {days % 7}d"


def _cd_left(last_ts: int, cooldown_sec: int) -> int:
    remaining = cooldown_sec - (int(datetime.now(timezone.utc).timestamp()) - last_ts)
    return max(0, remaining)


# ═══════════════════════════════════════════════════════════════
#   EMBED BUILDER — glavni embed sa svim statistikama
# ═══════════════════════════════════════════════════════════════
def build_poo_embed(p: dict, user: discord.User | discord.Member,
                    title_override: str = None) -> discord.Embed:
    _decay_stats(p)
    save_poo_data(poo_data)

    state     = _get_poo_state(p)
    em        = _emoji(state)
    col       = _color(state)
    stage_xp, stage_name, stage_desc = _stage(p.get("xp", 0))
    next_s    = _next_stage(p.get("xp", 0))
    poo_name  = p.get("name", "Poo")

    hunger  = int(p.get("hunger",      100))
    happy   = int(p.get("happiness",   100))
    clean   = int(p.get("cleanliness", 100))
    energy  = int(p.get("energy",      100))
    health  = int(p.get("health",      100))
    xp      = p.get("xp", 0)
    coins   = p.get("coins", 0)

    title = title_override or f"🐾 {poo_name}  ·  {stage_name}"

    # XP progress
    if next_s:
        needed      = next_s[0] - xp
        total_need  = next_s[0] - stage_xp
        cur_prog    = xp - stage_xp
        filled      = max(0, min(10, round((cur_prog / max(1, total_need)) * 10)))
        prog_bar    = "▰" * filled + "▱" * (10 - filled)
        xp_line     = f"`{prog_bar}` {xp:,} / {next_s[0]:,} XP  ·  još {needed:,} do **{next_s[1]}**"
    else:
        xp_line = f"🏆 **MAKSIMUM!** `{xp:,}` XP — Sveti Poo!"

    desc = (
        f"**Vlasnik:** {user.mention}\n"
        f"**Stanje:** {_state_label(state)}  {em}\n"
        f"**Starost:** `{_age_str(p.get('born_at', int(datetime.now(timezone.utc).timestamp())))}`"
        f"  ·  **XP:** `{xp:,}` 🌟  ·  **Coini:** `{coins:,}` 💶\n"
        f"\n{xp_line}"
    )

    embed = discord.Embed(title=title, description=desc, color=col,
                          timestamp=datetime.now(timezone.utc))
    embed.set_author(name=f"{user.display_name}  ·  Poo vlasnik 🐾",
                     icon_url=user.display_avatar.url)
    embed.set_thumbnail(url=user.display_avatar.url)

    # Statistike — kompaktno za mobile
    stats = (
        f"{_stat_emoji(hunger)} 🍗 Glad       `{_bar(hunger)}` {_pct(hunger)}\n"
        f"{_stat_emoji(happy)}  😊 Sreća      `{_bar(happy)}`  {_pct(happy)}\n"
        f"{_stat_emoji(clean)}  🧼 Čistoća    `{_bar(clean)}`  {_pct(clean)}\n"
        f"{_stat_emoji(energy)} ⚡ Energija   `{_bar(energy)}` {_pct(energy)}\n"
        f"{_stat_emoji(health)} ❤️  Zdravlje   `{_bar(health)}` {_pct(health)}"
    )
    embed.add_field(name="📊 Statistike", value=stats, inline=False)

    # Aktivnosti
    embed.add_field(
        name="🏅 Aktivnosti",
        value=(
            f"🍽️ Nahranjen: **{p.get('total_feeds', 0)}×**\n"
            f"🎮 Igrao se: **{p.get('total_plays', 0)}×**\n"
            f"💼 Radio: **{p.get('total_works', 0)}×**"
        ),
        inline=True
    )

    # Faza
    embed.add_field(
        name="⬆️ Faza",
        value=f"**{stage_name}**\n*{stage_desc}*",
        inline=True
    )

    embed.set_footer(text=f"🐾 GIANNI Poo Game  ·  /mypoo help za sve komande")
    return embed


def build_mini_embed(p: dict, user: discord.User | discord.Member,
                     action_text: str, color: int = None) -> discord.Embed:
    _decay_stats(p)
    state       = _get_poo_state(p)
    em          = _emoji(state)
    poo_name    = p.get("name", "Poo")
    embed_color = color or _color(state)

    hunger = int(p.get("hunger",      100))
    happy  = int(p.get("happiness",   100))
    clean  = int(p.get("cleanliness", 100))
    energy = int(p.get("energy",      100))

    embed = discord.Embed(
        title=f"{em}  {poo_name}",
        description=action_text,
        color=embed_color,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
    embed.add_field(
        name="📊 Stanje",
        value=f"🍗 `{hunger}%`  😊 `{happy}%`  🧼 `{clean}%`  ⚡ `{energy}%`",
        inline=False
    )
    embed.set_footer(text="🐾 GIANNI Poo Game  ·  /mypoo status za detalje")
    return embed


# ═══════════════════════════════════════════════════════════════
#   HELPER — provjeri da li je kanal dozvoljen
# ═══════════════════════════════════════════════════════════════
async def _check_poo_channel(interaction: discord.Interaction) -> bool:
    """Vrati True ako je interakcija u poo kanalu, inače pošalji grešku i vrati False."""
    if POO_CHANNEL_ID and interaction.channel_id != POO_CHANNEL_ID:
        ch = interaction.guild.get_channel(POO_CHANNEL_ID) if interaction.guild else None
        msg = (
            f"❌ **Poo Game nije dozvoljen ovdje!**\n"
            f"Koristi komande u {ch.mention if ch else f'<#{POO_CHANNEL_ID}>'}!"
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🚫 Pogrešan kanal",
                description=msg,
                color=0xE74C3C
            ),
            ephemeral=True
        )
        return False
    return True


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

    @tasks.loop(minutes=60)
    async def stat_decay_loop(self):
        for p in poo_data.values():
            _decay_stats(p)
        save_poo_data(poo_data)

    @stat_decay_loop.before_loop
    async def before_decay(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=30)
    async def dm_notifier(self):
        now = int(datetime.now(timezone.utc).timestamp())
        dm_cooldown = 3 * 3600

        for uid, p in list(poo_data.items()):
            try:
                user     = await self.bot.fetch_user(int(uid))
                poo_name = p.get("name", "Poo")
                state    = _get_poo_state(p)
                em       = _emoji(state)

                async def _send_dm(dm_last_key: str, msg_list: list, **kw):
                    if now - p.get(dm_last_key, 0) < dm_cooldown:
                        return
                    msg = random.choice(msg_list).format(poo_name=poo_name, emoji=em, **kw)
                    embed = discord.Embed(
                        title=f"🔔 Poo Notifikacija — {poo_name}",
                        description=msg,
                        color=_color(state),
                        timestamp=datetime.now(timezone.utc),
                    )
                    embed.add_field(
                        name="📊 Stanje",
                        value=(
                            f"🍗 `{int(p.get('hunger',100))}%`  "
                            f"😊 `{int(p.get('happiness',100))}%`\n"
                            f"🧼 `{int(p.get('cleanliness',100))}%`  "
                            f"⚡ `{int(p.get('energy',100))}%`"
                        ),
                        inline=False,
                    )
                    embed.set_footer(text="🐾 GIANNI Poo Game — tvoj Poo te treba!")
                    try:
                        await user.send(embed=embed)
                        p[dm_last_key] = now
                        save_poo_data(poo_data)
                    except (discord.Forbidden, discord.HTTPException):
                        pass

                if p.get("hunger", 100) < 30:
                    await _send_dm("last_dm_hungry", DM_MESSAGES["hungry"])
                elif p.get("cleanliness", 100) < 30:
                    await _send_dm("last_dm_dirty", DM_MESSAGES["dirty"])
                elif p.get("happiness", 100) < 30:
                    await _send_dm("last_dm_bored", DM_MESSAGES["bored"])
                elif p.get("energy", 100) < 25:
                    await _send_dm("last_dm_tired", DM_MESSAGES["tired"])

            except Exception:
                continue

    @dm_notifier.before_loop
    async def before_notifier(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(60)


# ═══════════════════════════════════════════════════════════════
#   SLASH GRUPE — /mypoo ...
# ═══════════════════════════════════════════════════════════════
mypoo_group = app_commands.Group(
    name="mypoo",
    description="🐾 Tvoj osobni Poo — hrani ga, igraj se, brini o njemu!"
)


@mypoo_group.command(name="start", description="🐾 Pokreni svog osobnog Poo-a!")
@app_commands.describe(ime="Kako ćeš nazvati svog Poo-a? (opciono)")
async def mypoo_start(i: discord.Interaction, ime: str = None):
    if not await _check_poo_channel(i):
        return
    uid = str(i.user.id)
    if uid in poo_data:
        embed = build_poo_embed(poo_data[uid], i.user, "🐾 Tvoj Poo već postoji!")
        return await i.response.send_message(embed=embed, ephemeral=True)

    poo_name = (ime or f"{i.user.display_name}'s Poo")[:30]
    p        = get_or_create_poo(i.user.id, poo_name)
    em       = POO_EMOJIS["happy"]

    embed = discord.Embed(
        title=f"🥚 Dobrodošao, {poo_name}!",
        description=(
            f"**{i.user.mention}**, tvoj Poo je upravo **rođen**! 🎉\n\n"
            f"{em} {em} {em}\n\n"
            f"Brini se o njemu — nahrani ga, igraj se s njim,\n"
            f"drži ga čistim i zdravim dok ne postane **Sveti Poo**! ✨\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🍗 `/mypoo feed` — Nahrani\n"
            f"🎮 `/mypoo play` — Igraj se\n"
            f"🧼 `/mypoo clean` — Operi\n"
            f"💼 `/mypoo work` — Pošalji na posao\n"
            f"😴 `/mypoo sleep` — Spavanje\n"
            f"📊 `/mypoo status` — Status\n"
            f"🎁 `/mypoo daily` — Dnevna nagrada\n"
            f"🏆 `/mypoo leaderboard` — Ljestvica"
        ),
        color=POO_COLORS["happy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=f"{i.user.display_name} • Novi Poo Vlasnik! 🐾",
                     icon_url=i.user.display_avatar.url)
    embed.set_thumbnail(url=i.user.display_avatar.url)
    embed.set_footer(text="🐾 GIANNI Poo Game  ·  Počni svoju Poo avanturu!")
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="status", description="📊 Pogledaj status svog Poo-a")
async def mypoo_status(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni svog Poo-a sa `/mypoo start` 🐾",
                                color=0xE74C3C),
            ephemeral=True
        )
    await i.response.send_message(embed=build_poo_embed(p, i.user))


@mypoo_group.command(name="feed", description="🍗 Nahrani svog Poo-a")
@app_commands.describe(hrana="Izaberi šta ćeš dati Poo-u")
@app_commands.choices(hrana=[
    app_commands.Choice(name="🍗 Piletina (35💶)",  value="0"),
    app_commands.Choice(name="🥩 Biftek (60💶)",    value="1"),
    app_commands.Choice(name="🥗 Salata (15💶)",    value="2"),
    app_commands.Choice(name="🍕 Pizza (40💶)",     value="3"),
    app_commands.Choice(name="🍜 Ramen (25💶)",     value="4"),
    app_commands.Choice(name="🥐 Kroasan (10💶)",   value="5"),
    app_commands.Choice(name="🍰 Tortica (30💶)",   value="6"),
    app_commands.Choice(name="🥙 Ćevapi (45💶)",    value="7"),
    app_commands.Choice(name="🍩 Krofna (20💶)",    value="8"),
    app_commands.Choice(name="🥛 Mlijeko (10💶)",   value="9"),
])
async def mypoo_feed(i: discord.Interaction, hrana: str = "0"):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True)

    cd = _cd_left(p.get("last_feed", 0), 1200)
    if cd > 0:
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo nije gladan!",
                description=f"Nahrani ponovo za **{cd // 60}m {cd % 60}s**",
                color=0xF39C12),
            ephemeral=True)

    food_idx   = int(hrana)
    food_name, hunger_gain, happy_gain, clean_loss, cost = POO_FOODS[food_idx]
    if p.get("coins", 0) < cost:
        return await i.response.send_message(
            embed=discord.Embed(
                title="❌ Nema dovoljno coina!",
                description=f"{food_name} košta **{cost} 💶**\nImaš: **{p.get('coins',0)} 💶**",
                color=0xE74C3C),
            ephemeral=True)

    old_stage = _stage(p.get("xp", 0))[1]
    p["coins"]       = p.get("coins", 0) - cost
    p["hunger"]      = min(100, p.get("hunger",      0) + hunger_gain)
    p["happiness"]   = min(100, p.get("happiness",   0) + happy_gain)
    p["cleanliness"] = max(0,   p.get("cleanliness", 100) - clean_loss)
    p["xp"]          = p.get("xp", 0) + 10
    p["last_feed"]   = int(datetime.now(timezone.utc).timestamp())
    p["total_feeds"] = p.get("total_feeds", 0) + 1
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[1]
    level_up  = (new_stage != old_stage)
    desc = (
        f"{POO_EMOJIS['happy']} **{p.get('name','Poo')}** je pojeo/la {food_name}! 😋\n\n"
        f"+ **{hunger_gain}** 🍗  + **{happy_gain}** 😊  + **10** 🌟 XP\n"
        f"- **{cost}** 💶 Coina"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"
    embed = build_mini_embed(p, i.user, desc,
                             color=POO_COLORS["holy"] if level_up else POO_COLORS["happy"])
    embed.title = "🍗 Poo je nahranjen!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="play", description="🎮 Poigraj se sa svojim Poo-om")
async def mypoo_play(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True)

    if p.get("sleeping", False) and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
        return await i.response.send_message(
            embed=discord.Embed(
                title="😴 Poo spava!",
                description=f"Budi se <t:{p['sleep_until']}:R>",
                color=POO_COLORS["sleeping"]),
            ephemeral=True)

    cd = _cd_left(p.get("last_play", 0), 900)
    if cd > 0:
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo treba odmor!",
                description=f"Igranje ponovo za **{cd // 60}m {cd % 60}s**",
                color=0xF39C12),
            ephemeral=True)

    game       = random.choice(POO_GAMES)
    old_stage  = _stage(p.get("xp", 0))[1]
    happy_gain = random.randint(15, 30)
    en_loss    = random.randint(5, 15)
    xp_gain    = random.randint(8, 15)

    p["happiness"] = min(100, p.get("happiness", 0) + happy_gain)
    p["energy"]    = max(0,   p.get("energy",    100) - en_loss)
    p["xp"]        = p.get("xp", 0) + xp_gain
    p["last_play"] = int(datetime.now(timezone.utc).timestamp())
    p["total_plays"] = p.get("total_plays", 0) + 1
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[1]
    level_up  = (new_stage != old_stage)
    desc = (
        f"{POO_EMOJIS['happy']} {game}!\n\n"
        f"+ **{happy_gain}** 😊  + **{xp_gain}** 🌟 XP\n"
        f"- **{en_loss}** ⚡ Energija"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"
    embed = build_mini_embed(p, i.user, desc, color=POO_COLORS["happy"])
    embed.title = "🎮 Poo se igrao!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="clean", description="🧼 Očisti svog Poo-a")
async def mypoo_clean(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True)

    cd = _cd_left(p.get("last_clean", 0), 1800)
    if cd > 0:
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo je već čist!",
                description=f"Peri ponovo za **{cd // 60}m {cd % 60}s**",
                color=0xF39C12),
            ephemeral=True)

    clean_gain = random.randint(30, 45)
    happy_gain = random.randint(5, 15)
    p["cleanliness"] = min(100, p.get("cleanliness", 0) + clean_gain)
    p["happiness"]   = min(100, p.get("happiness",   0) + happy_gain)
    p["xp"]          = p.get("xp", 0) + 5
    p["last_clean"]  = int(datetime.now(timezone.utc).timestamp())
    save_poo_data(poo_data)

    em = POO_EMOJIS["satisfied"]
    desc = (
        f"{em} **{p.get('name','Poo')}** je svjež kao cvijet! 🌸\n\n"
        f"+ **{clean_gain}** 🧼 Čistoća\n"
        f"+ **{happy_gain}** 😊 Sreća\n"
        f"+ **5** 🌟 XP"
    )
    embed = build_mini_embed(p, i.user, desc, color=0x00BCD4)
    embed.title = "🧼 Poo je opran!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="sleep", description="😴 Pošalji Poo-a na spavanje")
async def mypoo_sleep(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True)

    now = int(datetime.now(timezone.utc).timestamp())
    if p.get("sleeping", False) and now < p.get("sleep_until", 0):
        return await i.response.send_message(
            embed=discord.Embed(
                title="😴 Već spava!",
                description=f"**{p.get('name','Poo')}** se budi <t:{p['sleep_until']}:R>",
                color=POO_COLORS["sleeping"]),
            ephemeral=True)

    cd = _cd_left(p.get("last_sleep", 0), 7200)
    if cd > 0:
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo nije umoran!",
                description=f"Spavanje ponovo za **{cd // 3600}h {(cd % 3600) // 60}m**",
                color=0xF39C12),
            ephemeral=True)

    sleep_dur  = 2 * 3600
    wake_time  = now + sleep_dur
    p["sleeping"]    = True
    p["sleep_until"] = wake_time
    p["last_sleep"]  = now
    p["xp"]          = p.get("xp", 0) + 5
    save_poo_data(poo_data)

    em  = POO_EMOJIS["sleeping"]
    embed = discord.Embed(
        title="😴 Poo spava",
        description=(
            f"{em} **{p.get('name','Poo')}** je legao spavati...\n\n"
            f"💤 Budi se <t:{wake_time}:R>\n"
            f"Energija i sreća će se obnoviti!"
        ),
        color=POO_COLORS["sleeping"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=f"{i.user.display_name}", icon_url=i.user.display_avatar.url)
    embed.set_footer(text="🐾 GIANNI Poo Game  ·  Ne budi ga!")

    async def _wake():
        await asyncio.sleep(sleep_dur)
        if p.get("sleeping", False):
            p["sleeping"]    = False
            p["sleep_until"] = 0
            p["energy"]      = min(100, p.get("energy",    0) + 50)
            p["happiness"]   = min(100, p.get("happiness", 0) + 20)
            p["health"]      = min(100, p.get("health",    0) + 10)
            save_poo_data(poo_data)
            try:
                user = await i.client.fetch_user(i.user.id)
                w_em = discord.Embed(
                    title=f"☀️ {p.get('name','Poo')} se probudio!",
                    description=(
                        f"{POO_EMOJIS['satisfied']} Poo se upravo probudio!\n\n"
                        f"+ **50** ⚡ Energija\n"
                        f"+ **20** 😊 Sreća\n"
                        f"+ **10** ❤️ Zdravlje\n\n"
                        f"Nahrani ga! `/mypoo feed`"
                    ),
                    color=POO_COLORS["happy"],
                    timestamp=datetime.now(timezone.utc),
                )
                w_em.set_footer(text="🐾 GIANNI Poo Game")
                await user.send(embed=w_em)
            except Exception:
                pass

    asyncio.create_task(_wake())
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="work", description="💼 Pošalji Poo-a na posao")
async def mypoo_work(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True)

    if p.get("sleeping", False) and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
        return await i.response.send_message(
            embed=discord.Embed(
                title="😴 Poo spava!",
                description=f"Ne možeš slati Poo-a koji spava na posao!",
                color=POO_COLORS["sleeping"]),
            ephemeral=True)

    cd = _cd_left(p.get("last_work", 0), 2700)
    if cd > 0:
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Poo odmara!",
                description=f"Posao ponovo za **{cd // 60}m {cd % 60}s**",
                color=0xF39C12),
            ephemeral=True)

    if p.get("energy", 100) < 20:
        return await i.response.send_message(
            embed=discord.Embed(
                title="😪 Previše umoran!",
                description=f"Energija: **{int(p.get('energy',0))}%**\nPošalji ga da spava! `/mypoo sleep`",
                color=POO_COLORS["sad"]),
            ephemeral=True)

    job_name, xp_min, xp_max = random.choice(POO_JOBS)
    xp_gain     = random.randint(xp_min, xp_max)
    coins_gain  = random.randint(xp_min // 2, xp_max)
    energy_loss = random.randint(10, 20)
    hunger_loss = random.randint(5, 15)
    old_stage   = _stage(p.get("xp", 0))[1]

    p["xp"]          = p.get("xp", 0) + xp_gain
    p["coins"]       = p.get("coins", 0) + coins_gain
    p["energy"]      = max(0, p.get("energy",  100) - energy_loss)
    p["hunger"]      = max(0, p.get("hunger",  100) - hunger_loss)
    p["last_work"]   = int(datetime.now(timezone.utc).timestamp())
    p["total_works"] = p.get("total_works", 0) + 1
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[1]
    level_up  = (new_stage != old_stage)
    em        = POO_EMOJIS["working"]
    desc = (
        f"{em} **{p.get('name','Poo')}** {job_name}\n\n"
        f"+ **{xp_gain}** 🌟 XP  + **{coins_gain}** 💶 Coina\n"
        f"- **{energy_loss}** ⚡ Energija  - **{hunger_loss}** 🍗 Glad"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"
    embed = build_mini_embed(p, i.user, desc, color=POO_COLORS["working"])
    embed.title = "💼 Poo je radio!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="daily", description="🎁 Preuzmi dnevnu nagradu")
async def mypoo_daily(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True)

    now           = int(datetime.now(timezone.utc).timestamp())
    midnight_ts   = int(datetime.now(timezone.utc).replace(
                        hour=0, minute=0, second=0, microsecond=0).timestamp())
    if p.get("last_daily", 0) >= midnight_ts:
        next_mid = midnight_ts + 86400
        return await i.response.send_message(
            embed=discord.Embed(
                title="⏳ Već si uzeo dnevnu nagradu!",
                description=f"Sljedeća nagrada <t:{next_mid}:R>",
                color=0xF39C12),
            ephemeral=True)

    coins_r   = random.randint(50, 150)
    xp_r      = random.randint(20, 50)
    hunger_b  = random.randint(10, 25)
    old_stage = _stage(p.get("xp", 0))[1]

    p["coins"]      = p.get("coins",    0) + coins_r
    p["xp"]         = p.get("xp",       0) + xp_r
    p["hunger"]     = min(100, p.get("hunger",    0) + hunger_b)
    p["happiness"]  = min(100, p.get("happiness", 0) + 15)
    p["last_daily"] = now
    save_poo_data(poo_data)

    new_stage = _stage(p["xp"])[1]
    level_up  = (new_stage != old_stage)
    em        = POO_EMOJIS["happy"]
    desc = (
        f"{em} **{p.get('name','Poo')}** je presretan!\n\n"
        f"🎁 **Dnevna nagrada:**\n"
        f"+ **{coins_r}** 💶 Coina\n"
        f"+ **{xp_r}** 🌟 XP\n"
        f"+ **{hunger_b}** 🍗 Glad\n"
        f"+ **15** 😊 Sreća\n\n"
        f"*Vrati se sutra!* 😊"
    )
    if level_up:
        desc += f"\n\n🎉 **LEVEL UP!** Poo je sada **{new_stage}**! 🎊"
    embed = build_mini_embed(p, i.user, desc, color=POO_COLORS["holy"])
    embed.title = "🎁 Dnevna Nagrada!"
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="rename", description="✏️ Promijeni ime svog Poo-a")
@app_commands.describe(novo_ime="Novo ime za Poo-a (max 30 znakova)")
async def mypoo_rename(i: discord.Interaction, novo_ime: str):
    if not await _check_poo_channel(i):
        return
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Nemaš Poo-a!",
                                description="Pokreni sa `/mypoo start` 🐾", color=0xE74C3C),
            ephemeral=True)
    if len(novo_ime) > 30:
        return await i.response.send_message(
            embed=discord.Embed(title="❌ Predugačko!", description="Max 30 znakova!", color=0xE74C3C),
            ephemeral=True)
    old_name  = p.get("name", "Poo")
    p["name"] = novo_ime
    save_poo_data(poo_data)
    embed = discord.Embed(
        title="✏️ Poo preimenovan!",
        description=f"**{old_name}** → **{novo_ime}** {POO_EMOJIS['happy']}",
        color=POO_COLORS["happy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=f"{i.user.display_name}", icon_url=i.user.display_avatar.url)
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="leaderboard", description="🏆 Top 10 Poo-ova po XP-u")
async def mypoo_leaderboard(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    if not poo_data:
        return await i.response.send_message(
            embed=discord.Embed(
                title="🏆 Ljestvica prazna",
                description="Niko još nema Poo-a! Budi prvi — `/mypoo start`",
                color=0xF39C12),
            ephemeral=True)

    sorted_poos = sorted(poo_data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]
    medals = ["🥇", "🥈", "🥉"] + [f"`#{n}`" for n in range(4, 11)]

    lines = []
    for idx, (uid, p) in enumerate(sorted_poos):
        xp       = p.get("xp", 0)
        poo_name = p.get("name", "Poo")
        stage_n  = _stage(xp)[1]
        em       = _emoji(_get_poo_state(p))
        try:
            member   = i.guild.get_member(int(uid)) if i.guild else None
            username = member.display_name if member else f"Korisnik#{uid[-4:]}"
        except Exception:
            username = f"Korisnik#{uid[-4:]}"
        lines.append(f"{medals[idx]} {em} **{poo_name}** — *{username}*  ·  `{stage_n}`  ·  **{xp:,} XP**")

    embed = discord.Embed(
        title="🏆 TOP 10 — Poo Ljestvica",
        description="\n".join(lines),
        color=POO_COLORS["holy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text="🐾 GIANNI Poo Game  ·  /mypoo work za više XP!")
    await i.response.send_message(embed=embed)


@mypoo_group.command(name="poo_info", description="👤 Pogledaj Poo-a nekog drugog igrača")
@app_commands.describe(korisnik="Čijeg Poo-a želiš vidjeti?")
async def mypoo_info(i: discord.Interaction, korisnik: discord.Member):
    if not await _check_poo_channel(i):
        return
    p = get_poo(korisnik.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(
                title="❌ Nema Poo-a!",
                description=f"**{korisnik.display_name}** još nema svog Poo-a.",
                color=0xE74C3C),
            ephemeral=True)
    await i.response.send_message(embed=build_poo_embed(p, korisnik, f"🐾 {korisnik.display_name}'s Poo"))


@mypoo_group.command(name="help", description="❓ Uputstvo za Poo Game")
async def mypoo_help(i: discord.Interaction):
    if not await _check_poo_channel(i):
        return
    embed = discord.Embed(
        title="🐾 MYPOO — Uputstvo",
        description=(
            "Svaki član ima **svog osobnog Poo-a**!\n"
            "Brini se o njemu i gledaj kako raste! 💩\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=POO_COLORS["default"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.add_field(
        name="🚀 Početak",
        value=(
            "`/mypoo start [ime]` — Kreiraj svog Poo-a\n"
            "`/mypoo status` — Pogledaj statistike\n"
            "`/mypoo poo_info @user` — Pogledaj tuđeg Poo-a\n"
            "`/mypoo leaderboard` — Top 10"
        ),
        inline=False,
    )
    embed.add_field(
        name="🍗 Briga",
        value=(
            "`/mypoo feed [hrana]` — Nahrani *(20min CD)*\n"
            "`/mypoo clean` — Opere *(30min CD)*\n"
            "`/mypoo sleep` — Spavanje *(2h CD, 2h sna)*\n"
            "`/mypoo play` — Igraj se *(15min CD)*"
        ),
        inline=False,
    )
    embed.add_field(
        name="💰 Zarađivanje",
        value=(
            "`/mypoo work` — Posao *(45min CD)*\n"
            "`/mypoo daily` — Dnevna nagrada *(1× dnevno)*\n"
            "`/mypoo rename [ime]` — Promijeni ime"
        ),
        inline=False,
    )
    embed.add_field(
        name="📊 Statistike padaju s vremenom",
        value=(
            "🍗 **Glad** — prati ga, nahrani na vrijeme!\n"
            "😊 **Sreća** — raste igrom i hranjenjem\n"
            "🧼 **Čistoća** — pada s vremenom i jedenjem\n"
            "⚡ **Energija** — troši se igrom i radom\n"
            "❤️ **Zdravlje** — pada ako je gladan/prljav"
        ),
        inline=False,
    )
    embed.add_field(
        name="⬆️ Faze Rasta",
        value="\n".join([f"`{s[0]:>5} XP` — **{s[1]}**" for s in POO_STAGES]),
        inline=False,
    )
    embed.set_footer(text="🐾 GIANNI Poo Game  ·  Poo te čeka!")
    await i.response.send_message(embed=embed, ephemeral=True)


# ═══════════════════════════════════════════════════════════════
#   SETUP
# ═══════════════════════════════════════════════════════════════
async def setup(bot: commands.Bot):
    cog = PersonalPooGame(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(mypoo_group)
    print("✅ PersonalPooGame Cog učitan!")
