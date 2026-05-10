# ╔══════════════════════════════════════════════════════════════════╗
# ║        🐾  GIANNI — PERSONAL POO GAME  (v3.0 ENHANCED)  🐾     ║
# ║  Svaki član ima SVOG Poo-a! Dugmad mijenjaju poo emoji live!   ║
# ║  Veliki emoji prikaz • Buttons • Kanal-lock • Anti-spam        ║
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
#   KONFIGURACIJA
# ═══════════════════════════════════════════════════════════════
# Naziv kanala u kojemu je dozvoljen poo game
# Može biti ime kanala (npr. "poo") ili ID kanala (int)
POO_CHANNEL_NAME = "poo"   # promijeni ako kanal ima drugačije ime
POO_CHANNEL_ID   = 0       # ako znaš ID kanala, upiši ga ovdje (prioritet nad imenom)

# Anti-spam: koliko sekundi između 2 poruke u poo kanalu
POO_SPAM_COOLDOWN = 3  # sekunde

# ═══════════════════════════════════════════════════════════════
#   CUSTOM POO EMOJI IDS
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
#   BOJE PO STANJU
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
    (0,    "Beba Poo",       "Tek se rodio! Treba puno ljubavi."),
    (100,  "Mali Poo",       "Raste brže nego što misliš!"),
    (300,  "Poo Junior",     "Već ima svoju ličnost."),
    (600,  "Poo Tinejdžer",  "Tvrdoglav, ali sladak."),
    (1000, "Poo Odrasli",    "Ozbiljan Poo koji zna što hoće."),
    (1500, "Poo Veteran",    "Iskusan — preživio je mnogo!"),
    (2200, "Poo Legenda",    "Malo ih je dostiglo ovu fazu..."),
    (3000, "Poo Besmrtni",   "Transcendirao je. Sveti Poo."),
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
        print(f"[poo-save] {e}")

poo_data: dict = load_poo_data()

# Anti-spam tracker: user_id -> last_message_timestamp
_spam_tracker: dict[int, float] = {}

def get_poo(user_id: int) -> dict | None:
    return poo_data.get(str(user_id))

def get_or_create_poo(user_id: int, name: str = "Poo") -> dict:
    uid = str(user_id)
    if uid not in poo_data:
        now_ts = int(datetime.now(timezone.utc).timestamp())
        poo_data[uid] = {
            "name":          name,
            "xp":            0,
            "hunger":        80,
            "happiness":     80,
            "cleanliness":   80,
            "energy":        80,
            "health":        100,
            "born_at":       now_ts,
            "last_feed":     0,
            "last_play":     0,
            "last_clean":    0,
            "last_sleep":    0,
            "last_work":     0,
            "last_daily":    0,
            "total_feeds":   0,
            "total_plays":   0,
            "total_works":   0,
            "sleeping":      False,
            "sleep_until":   0,
            "coins":         100,
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
    for s in POO_STAGES:
        if xp < s[0]:
            return s
    return None

def _bar(value: int, length: int = 8) -> str:
    filled = round((max(0, min(100, value)) / 100) * length)
    return "█" * filled + "░" * (length - filled)

def _pct_emoji(value: int) -> str:
    if value >= 80: return "💚"
    if value >= 50: return "💛"
    if value >= 25: return "🟠"
    return "❤️"

def _decay_stats(p: dict):
    base = 2.5
    p["hunger"]      = max(0, p.get("hunger",      100) - base * 0.5)
    p["happiness"]   = max(0, p.get("happiness",   100) - base * 0.4)
    p["cleanliness"] = max(0, p.get("cleanliness", 100) - base * 0.3)
    p["energy"]      = max(0, p.get("energy",      100) - base * 0.3)
    if p.get("hunger", 100) < 20 or p.get("cleanliness", 100) < 20:
        p["health"] = max(0, p.get("health", 100) - 1)
    else:
        p["health"] = min(100, p.get("health", 100) + 0.2)

def _get_state(p: dict) -> str:
    if p.get("sleeping", False) and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
        return "sleeping"
    h  = p.get("hunger",      100)
    hp = p.get("happiness",   100)
    cl = p.get("cleanliness", 100)
    en = p.get("energy",      100)
    hl = p.get("health",      100)
    if h  <= 10:  return "veryhungry"
    if h  <= 30:  return "hungry"
    if cl <= 20:  return "dirty"
    if hp <= 15:  return "heartbroken"
    if hp <= 30:  return "sad"
    if en <= 20:  return "tired"
    if hl <= 40:  return "sick"
    if hp >= 90 and h >= 80: return "happy"
    return "main"

def _emoji_for(state: str) -> str:
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

def _color_for(state: str) -> int:
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
    days = delta.days
    hours = delta.seconds // 3600
    if days == 0:   return f"{hours}h"
    if days < 7:    return f"{days}d {hours}h"
    return f"{days // 7}w {days % 7}d"

def _cd_left(last_ts: int, cd_sec: int) -> int:
    return max(0, cd_sec - (int(datetime.now(timezone.utc).timestamp()) - last_ts))

def _is_poo_channel(channel) -> bool:
    if POO_CHANNEL_ID and channel.id == POO_CHANNEL_ID:
        return True
    if POO_CHANNEL_NAME and POO_CHANNEL_NAME.lower() in channel.name.lower():
        return True
    return False

# ═══════════════════════════════════════════════════════════════
#   VELIKI EMOJI PRIKAZ (za embed)
#   Prikazuje emoji u 3x3 gridu da bude vizuelno VELIK
# ═══════════════════════════════════════════════════════════════
def _big_poo_display(emoji: str) -> str:
    e = emoji
    return (
        f"\u200b\n"
        f"⠀⠀⠀{e}⠀{e}⠀{e}\n"
        f"⠀⠀{e}⠀{e}⠀{e}⠀{e}\n"
        f"⠀⠀⠀{e}⠀{e}⠀{e}\n"
        f"\u200b"
    )

# ═══════════════════════════════════════════════════════════════
#   EMBED BUILDER — glavni embed
# ═══════════════════════════════════════════════════════════════
def build_poo_embed(p: dict, user: discord.User | discord.Member, title: str = None) -> discord.Embed:
    _decay_stats(p)
    save_poo_data(poo_data)

    state     = _get_state(p)
    emoji     = _emoji_for(state)
    color     = _color_for(state)
    xp        = p.get("xp", 0)
    coins     = p.get("coins", 0)
    poo_name  = p.get("name", "Poo")
    hunger    = int(p.get("hunger",      100))
    happy     = int(p.get("happiness",   100))
    clean     = int(p.get("cleanliness", 100))
    energy    = int(p.get("energy",      100))
    health    = int(p.get("health",      100))

    stg_xp, stg_name, stg_desc = _stage(xp)
    next_s = _next_stage(xp)

    embed = discord.Embed(
        title=title or f"💩  {poo_name}",
        color=color,
        timestamp=datetime.now(timezone.utc),
    )

    embed.set_author(
        name=f"{user.display_name} • Poo vlasnik 🐾",
        icon_url=user.display_avatar.url,
    )

    # ── VELIKI EMOJI U OPISU ──
    big_display = _big_poo_display(emoji)
    status_line = _state_label(state)
    embed.description = (
        f"{big_display}\n"
        f"**Stanje:** {status_line}\n"
        f"**Faza:** `{stg_name}`  •  **Starost:** `{_age_str(p.get('born_at', 0))}`\n"
        f"**XP:** `{xp:,}` 🌟  **Coins:** `{coins:,}` 💶"
    )

    # ── STATISTIKE (mobile-friendly: kratki barovi, sve u jednom fieldu) ──
    stats = (
        f"{_pct_emoji(hunger)} **Glad**       `{_bar(hunger)}` {hunger}%\n"
        f"{_pct_emoji(happy)}  **Sreća**      `{_bar(happy)}` {happy}%\n"
        f"{_pct_emoji(clean)}  **Čistoća**    `{_bar(clean)}` {clean}%\n"
        f"{_pct_emoji(energy)} **Energija**   `{_bar(energy)}` {energy}%\n"
        f"{_pct_emoji(health)} **Zdravlje**   `{_bar(health)}` {health}%"
    )
    embed.add_field(name="📊 Statistike", value=stats, inline=False)

    # ── XP PROGRESS ──
    if next_s:
        needed     = next_s[0] - xp
        total_need = next_s[0] - stg_xp
        cur_prog   = xp - stg_xp
        filled     = round((cur_prog / max(1, total_need)) * 10)
        prog_bar   = "▰" * max(0, min(10, filled)) + "▱" * (10 - max(0, min(10, filled)))
        xp_line    = f"`{prog_bar}` {xp:,}/{next_s[0]:,}  *(još {needed:,} XP do {next_s[1]})*"
    else:
        xp_line = f"🏆 **MAKSIMUM!** `{xp:,} XP` — Sveti Poo!"

    embed.add_field(name="⬆️ Napredak", value=xp_line, inline=False)

    # ── AKTIVNOSTI ──
    act = (
        f"🍽️ Nahranjen: **{p.get('total_feeds',0)}×**  "
        f"🎮 Igrao: **{p.get('total_plays',0)}×**  "
        f"💼 Radio: **{p.get('total_works',0)}×**"
    )
    embed.add_field(name="🏅 Aktivnosti", value=act, inline=False)

    embed.set_footer(text=f"🐾 Poo Game  •  {stg_desc}  •  Koristi dugmad ispod!")
    return embed


def build_action_embed(p: dict, user: discord.User | discord.Member, action_text: str, color: int = None) -> discord.Embed:
    _decay_stats(p)
    state   = _get_state(p)
    emoji   = _emoji_for(state)
    poo_name = p.get("name", "Poo")
    clr     = color or _color_for(state)

    embed = discord.Embed(
        description=action_text,
        color=clr,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(
        name=f"{user.display_name} • {poo_name}  {emoji}",
        icon_url=user.display_avatar.url,
    )
    h = int(p.get("hunger", 100))
    s = int(p.get("happiness", 100))
    c = int(p.get("cleanliness", 100))
    e = int(p.get("energy", 100))
    embed.add_field(
        name="📊 Brzo stanje",
        value=(
            f"🍗`{h}%` 😊`{s}%` 🧼`{c}%` ⚡`{e}%`\n"
            f"💶 Coins: **{p.get('coins',0):,}**"
        ),
        inline=False
    )
    embed.set_footer(text="🐾 Poo Game  •  /mypoo status za detalje")
    return embed


# ═══════════════════════════════════════════════════════════════
#   POO ACTION VIEW — dugmad koja mijenjaju poo emoji live
# ═══════════════════════════════════════════════════════════════
class PooActionView(discord.ui.View):
    def __init__(self, user_id: int, show_full: bool = True):
        super().__init__(timeout=300)
        self.user_id    = user_id
        self.show_full  = show_full

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ Ovo nije tvoj Poo! Koristi `.poo` da vidiš svog.", ephemeral=True
            )
            return False
        return True

    async def _refresh_embed(self, interaction: discord.Interaction):
        p = get_poo(interaction.user.id)
        if not p:
            await interaction.response.send_message("Nemaš Poo-a! Koristi `/mypoo start`", ephemeral=True)
            return
        embed = build_poo_embed(p, interaction.user)
        await interaction.response.edit_message(embed=embed, view=self)

    # ── 🍗 NAHRANI ──────────────────────────────────────────────
    @discord.ui.button(label="Nahrani", emoji="🍗", style=discord.ButtonStyle.success, row=0)
    async def btn_feed(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = get_poo(interaction.user.id)
        if not p:
            return await interaction.response.send_message("Nemaš Poo-a! `/mypoo start`", ephemeral=True)

        cd = _cd_left(p.get("last_feed", 0), 1200)
        if cd > 0:
            return await interaction.response.send_message(
                f"⏳ Sačekaj još **{cd//60}m {cd%60}s** da Poo svari! {POO_EMOJIS['main']}", ephemeral=True
            )

        idx = random.randint(0, len(POO_FOODS) - 1)
        food_name, h_gain, hp_gain, cl_loss, cost = POO_FOODS[idx]

        if p.get("coins", 0) < cost:
            return await interaction.response.send_message(
                f"❌ Nemaš dovoljno coina! ({food_name} = **{cost}💶**)\n"
                f"Imaš: **{p.get('coins',0)}💶** — zaradi više sa 💼 Posao ili 🎁 Dnevna!", ephemeral=True
            )

        old_stage = _stage(p.get("xp", 0))[1]
        p["coins"]       = p.get("coins", 0) - cost
        p["hunger"]      = min(100, p.get("hunger",      0) + h_gain)
        p["happiness"]   = min(100, p.get("happiness",   0) + hp_gain)
        p["cleanliness"] = max(0,   p.get("cleanliness", 100) - cl_loss)
        p["xp"]          = p.get("xp", 0) + 10
        p["last_feed"]   = int(datetime.now(timezone.utc).timestamp())
        p["total_feeds"] = p.get("total_feeds", 0) + 1
        save_poo_data(poo_data)

        level_up = _stage(p["xp"])[1] != old_stage
        state    = _get_state(p)
        emoji    = _emoji_for(state)

        desc = (
            f"{emoji} **{p.get('name','Poo')}** je pojeo {food_name}!\n\n"
            f"🍗 +**{h_gain}**  😊 +**{hp_gain}**  🌟 +**10** XP  💶 -**{cost}**"
        )
        if level_up:
            desc += f"\n\n🎉 **LEVEL UP!** → **{_stage(p['xp'])[1]}**! 🎊"

        embed = build_poo_embed(p, interaction.user, f"🍗 Poo je nahranjen!")
        await interaction.response.edit_message(embed=embed, view=self)

    # ── 🎮 IGRAJ SE ─────────────────────────────────────────────
    @discord.ui.button(label="Igraj se", emoji="🎮", style=discord.ButtonStyle.primary, row=0)
    async def btn_play(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = get_poo(interaction.user.id)
        if not p:
            return await interaction.response.send_message("Nemaš Poo-a! `/mypoo start`", ephemeral=True)

        if p.get("sleeping") and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
            return await interaction.response.send_message(
                f"{POO_EMOJIS['sleeping']} Poo spava! Budi se <t:{p['sleep_until']}:R>", ephemeral=True
            )

        cd = _cd_left(p.get("last_play", 0), 900)
        if cd > 0:
            return await interaction.response.send_message(
                f"⏳ Poo je umoran od igre! Sačekaj **{cd//60}m {cd%60}s**", ephemeral=True
            )

        games = [
            "🎯 Bacali strelice", "⚽ Fudbal u dvorištu",
            "🎮 Konzola do ponoći", "🃏 Kartaški dvoboj",
            "🎲 Bacanje kocke", "🏊 Plivanje u bazenu",
            "🚴 Vožnja bicikla", "🎳 Kuglanje",
        ]
        game   = random.choice(games)
        h_gain = random.randint(15, 30)
        e_loss = random.randint(5, 15)
        xp_g   = random.randint(8, 15)
        old_stage = _stage(p.get("xp", 0))[1]

        p["happiness"]   = min(100, p.get("happiness", 0) + h_gain)
        p["energy"]      = max(0,   p.get("energy", 100) - e_loss)
        p["xp"]          = p.get("xp", 0) + xp_g
        p["last_play"]   = int(datetime.now(timezone.utc).timestamp())
        p["total_plays"] = p.get("total_plays", 0) + 1
        save_poo_data(poo_data)

        level_up = _stage(p["xp"])[1] != old_stage
        emoji    = _emoji_for(_get_state(p))

        title = f"🎮 {game}!"
        if level_up:
            title += f" | 🎉 LEVEL UP → {_stage(p['xp'])[1]}!"

        embed = build_poo_embed(p, interaction.user, title)
        await interaction.response.edit_message(embed=embed, view=self)

    # ── 🧼 OPERI ────────────────────────────────────────────────
    @discord.ui.button(label="Operi", emoji="🧼", style=discord.ButtonStyle.secondary, row=0)
    async def btn_clean(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = get_poo(interaction.user.id)
        if not p:
            return await interaction.response.send_message("Nemaš Poo-a! `/mypoo start`", ephemeral=True)

        cd = _cd_left(p.get("last_clean", 0), 1800)
        if cd > 0:
            return await interaction.response.send_message(
                f"⏳ Poo je već čist! Sačekaj **{cd//60}m {cd%60}s**", ephemeral=True
            )

        gain = random.randint(30, 45)
        old_stage = _stage(p.get("xp", 0))[1]

        p["cleanliness"] = min(100, p.get("cleanliness", 0) + gain)
        p["happiness"]   = min(100, p.get("happiness",   0) + random.randint(5, 15))
        p["xp"]          = p.get("xp", 0) + 5
        p["last_clean"]  = int(datetime.now(timezone.utc).timestamp())
        save_poo_data(poo_data)

        embed = build_poo_embed(p, interaction.user, "🧼 Poo je opran!")
        await interaction.response.edit_message(embed=embed, view=self)

    # ── 😴 SPAVANJE ─────────────────────────────────────────────
    @discord.ui.button(label="Spavaj", emoji="😴", style=discord.ButtonStyle.secondary, row=1)
    async def btn_sleep(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = get_poo(interaction.user.id)
        if not p:
            return await interaction.response.send_message("Nemaš Poo-a! `/mypoo start`", ephemeral=True)

        if p.get("sleeping") and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
            return await interaction.response.send_message(
                f"{POO_EMOJIS['sleeping']} Već spava! Budi se <t:{p['sleep_until']}:R>", ephemeral=True
            )

        cd = _cd_left(p.get("last_sleep", 0), 7200)
        if cd > 0:
            h, m = cd // 3600, (cd % 3600) // 60
            return await interaction.response.send_message(
                f"⏳ Poo nije umoran! Sačekaj **{h}h {m}m**", ephemeral=True
            )

        now  = int(datetime.now(timezone.utc).timestamp())
        wake = now + 7200

        p["sleeping"]    = True
        p["sleep_until"] = wake
        p["last_sleep"]  = now
        p["xp"]          = p.get("xp", 0) + 5
        save_poo_data(poo_data)

        async def _wake():
            await asyncio.sleep(7200)
            if p.get("sleeping"):
                p["sleeping"]    = False
                p["sleep_until"] = 0
                p["energy"]      = min(100, p.get("energy",    0) + 50)
                p["happiness"]   = min(100, p.get("happiness", 0) + 20)
                p["health"]      = min(100, p.get("health",    0) + 10)
                save_poo_data(poo_data)
                try:
                    user_obj = await interaction.client.fetch_user(interaction.user.id)
                    e = discord.Embed(
                        title=f"☀️ {p.get('name','Poo')} se probudio!",
                        description=(
                            f"{POO_EMOJIS['satisfied']} Svježi i odmoran!\n\n"
                            f"⚡ +50  😊 +20  ❤️ +10\n\nVrati se! `/mypoo status`"
                        ),
                        color=POO_COLORS["happy"],
                    )
                    await user_obj.send(embed=e)
                except Exception:
                    pass
        asyncio.create_task(_wake())

        embed = build_poo_embed(p, interaction.user, f"😴 {p.get('name','Poo')} spava!")
        await interaction.response.edit_message(embed=embed, view=self)

    # ── 💼 POSAO ────────────────────────────────────────────────
    @discord.ui.button(label="Posao", emoji="💼", style=discord.ButtonStyle.primary, row=1)
    async def btn_work(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = get_poo(interaction.user.id)
        if not p:
            return await interaction.response.send_message("Nemaš Poo-a! `/mypoo start`", ephemeral=True)

        if p.get("sleeping") and int(datetime.now(timezone.utc).timestamp()) < p.get("sleep_until", 0):
            return await interaction.response.send_message(
                f"{POO_EMOJIS['sleeping']} Poo spava! Budi se <t:{p['sleep_until']}:R>", ephemeral=True
            )

        cd = _cd_left(p.get("last_work", 0), 2700)
        if cd > 0:
            return await interaction.response.send_message(
                f"⏳ Poo odmara između smjena! Sačekaj **{cd//60}m {cd%60}s**", ephemeral=True
            )

        if p.get("energy", 100) < 20:
            return await interaction.response.send_message(
                f"😪 Poo je previše umoran! Energija: **{int(p.get('energy',0))}%**\n"
                f"Pošalji ga spavati — dugme 😴", ephemeral=True
            )

        job, xp_mn, xp_mx = random.choice(POO_JOBS)
        xp_g   = random.randint(xp_mn, xp_mx)
        coin_g = random.randint(xp_mn // 2, xp_mx)
        e_loss = random.randint(10, 20)
        h_loss = random.randint(5, 15)
        old_stage = _stage(p.get("xp", 0))[1]

        p["xp"]          = p.get("xp", 0) + xp_g
        p["coins"]       = p.get("coins", 0) + coin_g
        p["energy"]      = max(0, p.get("energy", 100) - e_loss)
        p["hunger"]      = max(0, p.get("hunger", 100) - h_loss)
        p["last_work"]   = int(datetime.now(timezone.utc).timestamp())
        p["total_works"] = p.get("total_works", 0) + 1
        save_poo_data(poo_data)

        level_up = _stage(p["xp"])[1] != old_stage
        title    = f"💼 {job}"
        if level_up:
            title += f" | 🎉 LEVEL UP!"

        embed = build_poo_embed(p, interaction.user, title)
        await interaction.response.edit_message(embed=embed, view=self)

    # ── 🎁 DNEVNA NAGRADA ───────────────────────────────────────
    @discord.ui.button(label="Dnevna", emoji="🎁", style=discord.ButtonStyle.success, row=1)
    async def btn_daily(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = get_poo(interaction.user.id)
        if not p:
            return await interaction.response.send_message("Nemaš Poo-a! `/mypoo start`", ephemeral=True)

        now   = int(datetime.now(timezone.utc).timestamp())
        mn    = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        mn_ts = int(mn.timestamp())

        if p.get("last_daily", 0) >= mn_ts:
            nxt = int((mn + timedelta(days=1)).timestamp())
            return await interaction.response.send_message(
                f"⏳ Već si uzeo dnevnu nagradu! Sljedeća <t:{nxt}:R>", ephemeral=True
            )

        coins_r = random.randint(50, 150)
        xp_r    = random.randint(20, 50)
        h_bonus = random.randint(10, 25)
        old_stage = _stage(p.get("xp", 0))[1]

        p["coins"]      = p.get("coins",     0) + coins_r
        p["xp"]         = p.get("xp",        0) + xp_r
        p["hunger"]     = min(100, p.get("hunger",    0) + h_bonus)
        p["happiness"]  = min(100, p.get("happiness", 0) + 15)
        p["last_daily"] = now
        save_poo_data(poo_data)

        level_up = _stage(p["xp"])[1] != old_stage
        title    = "🎁 Dnevna nagrada!"
        if level_up:
            title += f" | 🎉 LEVEL UP → {_stage(p['xp'])[1]}!"

        embed = build_poo_embed(p, interaction.user, title)
        await interaction.response.edit_message(embed=embed, view=self)


# ═══════════════════════════════════════════════════════════════
#   COG — Personal Poo Game
# ═══════════════════════════════════════════════════════════════
class PersonalPooGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._decay_loop.start()
        self._dm_loop.start()

    def cog_unload(self):
        self._decay_loop.cancel()
        self._dm_loop.cancel()

    # ─── Decay svakih sat ───────────────────────────────────────
    @tasks.loop(minutes=60)
    async def _decay_loop(self):
        for p in poo_data.values():
            _decay_stats(p)
        save_poo_data(poo_data)

    @_decay_loop.before_loop
    async def _before_decay(self):
        await self.bot.wait_until_ready()

    # ─── DM notifikacije ────────────────────────────────────────
    @tasks.loop(minutes=30)
    async def _dm_loop(self):
        now     = int(datetime.now(timezone.utc).timestamp())
        cd      = 3 * 3600
        for uid, p in list(poo_data.items()):
            try:
                user     = await self.bot.fetch_user(int(uid))
                state    = _get_state(p)
                emoji    = _emoji_for(state)
                poo_name = p.get("name", "Poo")
                msgs = {
                    "hungry": (p.get("hunger",100)      < 30, "last_dm_hungry",
                        f"🍗 **{poo_name}** je gladan! Nahrani ga — dugme 🍗 Nahrani"),
                    "dirty":  (p.get("cleanliness",100) < 30, "last_dm_dirty",
                        f"🧼 **{poo_name}** smrdi! Operi ga — dugme 🧼 Operi"),
                    "bored":  (p.get("happiness",100)   < 30, "last_dm_bored",
                        f"😴 **{poo_name}** se dosađuje! Poigraj se — dugme 🎮 Igraj se"),
                    "tired":  (p.get("energy",100)      < 25, "last_dm_tired",
                        f"😪 **{poo_name}** je umoran! Pošalji spavati — dugme 😴 Spavaj"),
                }
                for key, (cond, ts_key, msg_text) in msgs.items():
                    if cond and now - p.get(ts_key, 0) >= cd:
                        e = discord.Embed(
                            title=f"🔔 Poo te treba!",
                            description=msg_text,
                            color=_color_for(state),
                            timestamp=datetime.now(timezone.utc),
                        )
                        e.set_footer(text="🐾 Poo Game — tvoj Poo te zove!")
                        try:
                            await user.send(embed=e)
                            p[ts_key] = now
                            save_poo_data(poo_data)
                        except Exception:
                            pass
                        break
            except Exception:
                continue

    @_dm_loop.before_loop
    async def _before_dm(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(60)

    # ─── Provjera kanala ────────────────────────────────────────
    async def _check_poo_channel(self, ctx_or_interaction) -> bool:
        if isinstance(ctx_or_interaction, discord.Interaction):
            channel = ctx_or_interaction.channel
            user    = ctx_or_interaction.user
        else:
            channel = ctx_or_interaction.channel
            user    = ctx_or_interaction.author

        if not _is_poo_channel(channel):
            target_name = f"#{POO_CHANNEL_NAME}" if POO_CHANNEL_NAME else "poo kanal"
            msg = (
                f"❌ {user.mention} — Poo komande su dozvoljene samo u **{target_name}**!\n"
                f"Idi tamo i nastavi igru! 🐾"
            )
            e = discord.Embed(description=msg, color=0xE74C3C)
            if isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(embed=e, ephemeral=True)
            else:
                await ctx_or_interaction.channel.send(embed=e, delete_after=8)
                try: await ctx_or_interaction.message.delete()
                except Exception: pass
            return False
        return True

    # ─── Anti-spam provjera ──────────────────────────────────────
    def _check_spam(self, user_id: int) -> float:
        now  = datetime.now(timezone.utc).timestamp()
        last = _spam_tracker.get(user_id, 0)
        if now - last < POO_SPAM_COOLDOWN:
            return POO_SPAM_COOLDOWN - (now - last)
        _spam_tracker[user_id] = now
        return 0

    # ─── .poo prefix komanda ─────────────────────────────────────
    @commands.command(name="poo", aliases=["mypoo"])
    async def prefix_poo(self, ctx: commands.Context, action: str = "status"):
        if not await self._check_poo_channel(ctx):
            return

        spam_wait = self._check_spam(ctx.author.id)
        if spam_wait > 0:
            msg = await ctx.send(
                embed=discord.Embed(
                    description=f"⏳ {ctx.author.mention} — polako! Sačekaj **{spam_wait:.1f}s**",
                    color=0xF39C12
                )
            )
            await asyncio.sleep(5)
            try: await msg.delete()
            except Exception: pass
            try: await ctx.message.delete()
            except Exception: pass
            return

        p = get_poo(ctx.author.id)
        if not p:
            e = discord.Embed(
                title="❌ Nemaš Poo-a!",
                description=f"Kreiraj ga sa `/mypoo start` ili `/mypoo start [ime]`\n\n{POO_EMOJIS['sad']}",
                color=0xE74C3C,
            )
            return await ctx.send(embed=e)

        action = action.lower().strip()

        if action in ("status", "stat", "s", "info", "show"):
            embed = build_poo_embed(p, ctx.author)
            view  = PooActionView(ctx.author.id)
            await ctx.send(embed=embed, view=view)

        elif action in ("feed", "jedi", "hrani", "f"):
            idx = random.randint(0, len(POO_FOODS) - 1)
            food_name, h_gain, hp_gain, cl_loss, cost = POO_FOODS[idx]
            cd = _cd_left(p.get("last_feed", 0), 1200)
            if cd > 0:
                e = discord.Embed(
                    description=f"⏳ Sačekaj još **{cd//60}m {cd%60}s** — Poo još svari!",
                    color=0xF39C12
                )
                return await ctx.send(embed=e, delete_after=8)
            if p.get("coins", 0) < cost:
                e = discord.Embed(
                    description=f"❌ Nemaš dovoljno coina! ({food_name} = {cost}💶)\nTrenutno: {p.get('coins',0)}💶",
                    color=0xE74C3C
                )
                return await ctx.send(embed=e, delete_after=8)
            p["coins"]       = p.get("coins", 0) - cost
            p["hunger"]      = min(100, p.get("hunger",      0) + h_gain)
            p["happiness"]   = min(100, p.get("happiness",   0) + hp_gain)
            p["cleanliness"] = max(0,   p.get("cleanliness", 100) - cl_loss)
            p["xp"]          = p.get("xp", 0) + 10
            p["last_feed"]   = int(datetime.now(timezone.utc).timestamp())
            p["total_feeds"] = p.get("total_feeds", 0) + 1
            save_poo_data(poo_data)
            embed = build_poo_embed(p, ctx.author, f"🍗 Poo je pojeo {food_name}!")
            await ctx.send(embed=embed, view=PooActionView(ctx.author.id))

        elif action in ("play", "igraj", "game", "p"):
            cd = _cd_left(p.get("last_play", 0), 900)
            if cd > 0:
                return await ctx.send(
                    embed=discord.Embed(description=f"⏳ Sačekaj **{cd//60}m {cd%60}s**", color=0xF39C12),
                    delete_after=8
                )
            games = ["🎯 Strelice","⚽ Fudbal","🎮 Konzola","🃏 Karte","🏊 Plivanje"]
            game   = random.choice(games)
            h_gain = random.randint(15, 30)
            e_loss = random.randint(5, 15)
            p["happiness"]   = min(100, p.get("happiness", 0) + h_gain)
            p["energy"]      = max(0,   p.get("energy", 100) - e_loss)
            p["xp"]          = p.get("xp", 0) + random.randint(8, 15)
            p["last_play"]   = int(datetime.now(timezone.utc).timestamp())
            p["total_plays"] = p.get("total_plays", 0) + 1
            save_poo_data(poo_data)
            embed = build_poo_embed(p, ctx.author, f"🎮 {game}!")
            await ctx.send(embed=embed, view=PooActionView(ctx.author.id))

        elif action in ("clean", "operi", "wash", "c"):
            cd = _cd_left(p.get("last_clean", 0), 1800)
            if cd > 0:
                return await ctx.send(
                    embed=discord.Embed(description=f"⏳ Sačekaj **{cd//60}m {cd%60}s**", color=0xF39C12),
                    delete_after=8
                )
            gain = random.randint(30, 45)
            p["cleanliness"] = min(100, p.get("cleanliness", 0) + gain)
            p["happiness"]   = min(100, p.get("happiness",   0) + random.randint(5,15))
            p["xp"]          = p.get("xp", 0) + 5
            p["last_clean"]  = int(datetime.now(timezone.utc).timestamp())
            save_poo_data(poo_data)
            embed = build_poo_embed(p, ctx.author, "🧼 Poo je opran!")
            await ctx.send(embed=embed, view=PooActionView(ctx.author.id))

        elif action in ("work", "posao", "w"):
            cd = _cd_left(p.get("last_work", 0), 2700)
            if cd > 0:
                return await ctx.send(
                    embed=discord.Embed(description=f"⏳ Sačekaj **{cd//60}m {cd%60}s**", color=0xF39C12),
                    delete_after=8
                )
            if p.get("energy", 100) < 20:
                return await ctx.send(
                    embed=discord.Embed(
                        description=f"😪 Poo je previše umoran! Energija: {int(p.get('energy',0))}%",
                        color=0xE74C3C
                    ),
                    delete_after=8
                )
            job, xp_mn, xp_mx = random.choice(POO_JOBS)
            xp_g   = random.randint(xp_mn, xp_mx)
            coin_g = random.randint(xp_mn // 2, xp_mx)
            p["xp"]          = p.get("xp", 0) + xp_g
            p["coins"]       = p.get("coins", 0) + coin_g
            p["energy"]      = max(0, p.get("energy", 100) - random.randint(10,20))
            p["hunger"]      = max(0, p.get("hunger", 100) - random.randint(5,15))
            p["last_work"]   = int(datetime.now(timezone.utc).timestamp())
            p["total_works"] = p.get("total_works", 0) + 1
            save_poo_data(poo_data)
            embed = build_poo_embed(p, ctx.author, f"💼 {job}")
            await ctx.send(embed=embed, view=PooActionView(ctx.author.id))

        elif action in ("sleep", "spavaj", "spa", "z"):
            cd = _cd_left(p.get("last_sleep", 0), 7200)
            if cd > 0:
                h, m = cd // 3600, (cd % 3600) // 60
                return await ctx.send(
                    embed=discord.Embed(description=f"⏳ Sačekaj **{h}h {m}m**", color=0xF39C12),
                    delete_after=8
                )
            now  = int(datetime.now(timezone.utc).timestamp())
            wake = now + 7200
            p["sleeping"]    = True
            p["sleep_until"] = wake
            p["last_sleep"]  = now
            p["xp"]          = p.get("xp", 0) + 5
            save_poo_data(poo_data)
            embed = build_poo_embed(p, ctx.author, f"😴 {p.get('name','Poo')} spava!")
            await ctx.send(embed=embed, view=PooActionView(ctx.author.id))

        elif action in ("daily", "dnevna", "d"):
            mn    = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            mn_ts = int(mn.timestamp())
            if p.get("last_daily", 0) >= mn_ts:
                nxt = int((mn + timedelta(days=1)).timestamp())
                return await ctx.send(
                    embed=discord.Embed(
                        description=f"⏳ Sljedeća dnevna nagrada <t:{nxt}:R>", color=0xF39C12
                    ),
                    delete_after=10
                )
            coins_r = random.randint(50, 150)
            xp_r    = random.randint(20, 50)
            p["coins"]      = p.get("coins",    0) + coins_r
            p["xp"]         = p.get("xp",       0) + xp_r
            p["hunger"]     = min(100, p.get("hunger",    0) + random.randint(10,25))
            p["happiness"]  = min(100, p.get("happiness", 0) + 15)
            p["last_daily"] = int(datetime.now(timezone.utc).timestamp())
            save_poo_data(poo_data)
            embed = build_poo_embed(p, ctx.author, f"🎁 Dnevna nagrada! +{coins_r}💶 +{xp_r}XP")
            await ctx.send(embed=embed, view=PooActionView(ctx.author.id))

        elif action in ("top", "leaderboard", "lb"):
            if not poo_data:
                return await ctx.send(
                    embed=discord.Embed(description="🏆 Ljestvica je prazna! Budi prvi — `/mypoo start`", color=0xF39C12),
                    delete_after=10
                )
            top   = sorted(poo_data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]
            medals = ["🥇","🥈","🥉"] + [f"`#{i}`" for i in range(4,11)]
            lines  = []
            for i, (uid, pp) in enumerate(top):
                xp_v  = pp.get("xp", 0)
                name  = pp.get("name", "Poo")
                stg   = _stage(xp_v)[1]
                emoji = _emoji_for(_get_state(pp))
                try:
                    mem  = ctx.guild.get_member(int(uid)) if ctx.guild else None
                    uname = mem.display_name if mem else f"#{uid[-4:]}"
                except Exception:
                    uname = f"#{uid[-4:]}"
                lines.append(f"{medals[i]} {emoji} **{name}** *({uname})* — `{stg}` **{xp_v:,} XP**")
            embed = discord.Embed(
                title="🏆 TOP 10 — Poo Ljestvica",
                description="\n".join(lines),
                color=POO_COLORS["holy"],
                timestamp=datetime.now(timezone.utc),
            )
            embed.set_footer(text="🐾 Poo Game  •  Više XP = viši rank!")
            await ctx.send(embed=embed)

        elif action in ("help", "pomoc", "?", "h"):
            embed = discord.Embed(
                title="🐾 Poo Game — Komande",
                description=(
                    f"**Prefix:** `.poo [akcija]`\n"
                    f"**Slash:** `/mypoo [akcija]`\n\n"
                    f"Sve komande rade i prefix i slash!\n"
                    f"Samo u **#{POO_CHANNEL_NAME}** kanalu! 🔒"
                ),
                color=POO_COLORS["default"],
                timestamp=datetime.now(timezone.utc),
            )
            cmds = [
                ("`.poo` ili `.poo status`", "Pogledaj svog Poo-a (sa dugmadima!)"),
                ("`.poo feed`",   "🍗 Nahrani Poo-a *(20min CD)*"),
                ("`.poo play`",   "🎮 Igraj se *(15min CD)*"),
                ("`.poo clean`",  "🧼 Operi Poo-a *(30min CD)*"),
                ("`.poo work`",   "💼 Pošalji na posao *(45min CD)*"),
                ("`.poo sleep`",  "😴 Spavanje *(2h CD, 2h sna)*"),
                ("`.poo daily`",  "🎁 Dnevna nagrada *(1x dnevno)*"),
                ("`.poo top`",    "🏆 Ljestvica Top 10"),
            ]
            for cmd, desc in cmds:
                embed.add_field(name=cmd, value=desc, inline=False)
            embed.set_footer(text="🐾 Dugmad na emberu ti štede tipkanje!")
            await ctx.send(embed=embed, delete_after=60)

        else:
            embed = build_poo_embed(p, ctx.author)
            view  = PooActionView(ctx.author.id)
            await ctx.send(embed=embed, view=view)

    # ─── Slash komande ──────────────────────────────────────────
    # (definisane ispod kao mypoo_group)


# ═══════════════════════════════════════════════════════════════
#   SLASH KOMANDE
# ═══════════════════════════════════════════════════════════════
mypoo_group = app_commands.Group(
    name="mypoo",
    description="🐾 Tvoj osobni Poo — briga, igra, rast!"
)

@mypoo_group.command(name="start", description="🥚 Kreiraj svog Poo-a!")
@app_commands.describe(ime="Ime za tvog Poo-a (opciono)")
async def slash_start(i: discord.Interaction, ime: str = None):
    uid = str(i.user.id)
    if uid in poo_data:
        p = poo_data[uid]
        embed = build_poo_embed(p, i.user, "🐾 Tvoj Poo već postoji!")
        return await i.response.send_message(embed=embed, view=PooActionView(i.user.id), ephemeral=True)

    name = (ime or f"{i.user.display_name}'s Poo")[:30]
    p    = get_or_create_poo(i.user.id, name)

    emoji = POO_EMOJIS["happy"]
    embed = discord.Embed(
        title=f"🥚 {name} je rođen!",
        description=(
            f"**{i.user.mention}**, tvoj Poo je upravo **rođen**! 🎉\n\n"
            f"{_big_poo_display(emoji)}\n"
            f"Brini se o njemu — **dugmad ispod** ti omogućavaju sve akcije!\n\n"
            f"🍗 Nahrani  •  🎮 Igraj  •  🧼 Operi\n"
            f"💼 Posao  •  😴 Spavaj  •  🎁 Dnevna\n\n"
            f"Ili koristi `.poo` u #{POO_CHANNEL_NAME} kanalu!"
        ),
        color=POO_COLORS["happy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=f"{i.user.display_name} • Novi Poo Vlasnik! 🐾", icon_url=i.user.display_avatar.url)
    embed.set_footer(text="🐾 Poo Game  •  Samo u #poo kanalu!")
    await i.response.send_message(embed=embed, view=PooActionView(i.user.id))

@mypoo_group.command(name="status", description="📊 Pogledaj svog Poo-a")
async def slash_status(i: discord.Interaction):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(
                title="❌ Nemaš Poo-a!",
                description=f"Kreiraj ga sa `/mypoo start` 🐾\n\n{POO_EMOJIS['sad']}",
                color=0xE74C3C,
            ),
            ephemeral=True,
        )
    embed = build_poo_embed(p, i.user)
    await i.response.send_message(embed=embed, view=PooActionView(i.user.id))

@mypoo_group.command(name="rename", description="✏️ Promijeni ime svog Poo-a")
@app_commands.describe(novo_ime="Novo ime (max 30 znakova)")
async def slash_rename(i: discord.Interaction, novo_ime: str):
    p = get_poo(i.user.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(description="❌ Nemaš Poo-a! `/mypoo start`", color=0xE74C3C),
            ephemeral=True,
        )
    if len(novo_ime) > 30:
        return await i.response.send_message(
            embed=discord.Embed(description="❌ Ime je predugačko! Max 30 znakova.", color=0xE74C3C),
            ephemeral=True,
        )
    old = p.get("name", "Poo")
    p["name"] = novo_ime
    save_poo_data(poo_data)
    embed = discord.Embed(
        title="✏️ Poo preimenovan!",
        description=f"**{old}** → **{novo_ime}**\n\n{POO_EMOJIS['happy']} *Drago mu je novo ime!*",
        color=POO_COLORS["happy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=i.user.display_name, icon_url=i.user.display_avatar.url)
    await i.response.send_message(embed=embed)

@mypoo_group.command(name="leaderboard", description="🏆 Top 10 Poo-ova")
async def slash_lb(i: discord.Interaction):
    if not poo_data:
        return await i.response.send_message(
            embed=discord.Embed(description="🏆 Ljestvica prazna! Budi prvi — `/mypoo start`", color=0xF39C12),
            ephemeral=True,
        )
    top    = sorted(poo_data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]
    medals = ["🥇","🥈","🥉"] + [f"`#{n}`" for n in range(4,11)]
    lines  = []
    for idx, (uid, pp) in enumerate(top):
        xp_v  = pp.get("xp", 0)
        name  = pp.get("name", "Poo")
        stg   = _stage(xp_v)[1]
        emoji = _emoji_for(_get_state(pp))
        try:
            mem   = i.guild.get_member(int(uid)) if i.guild else None
            uname = mem.display_name if mem else f"#{uid[-4:]}"
        except Exception:
            uname = f"#{uid[-4:]}"
        lines.append(f"{medals[idx]} {emoji} **{name}** *({uname})* — `{stg}` **{xp_v:,} XP**")

    embed = discord.Embed(
        title="🏆 TOP 10 — Poo Ljestvica",
        description="\n".join(lines),
        color=POO_COLORS["holy"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text="🐾 Poo Game  •  /mypoo work za više XP!")
    await i.response.send_message(embed=embed)

@mypoo_group.command(name="poo_info", description="👤 Pogledaj Poo-a drugog igrača")
@app_commands.describe(korisnik="Čijeg Poo-a pogledati?")
async def slash_info(i: discord.Interaction, korisnik: discord.Member):
    p = get_poo(korisnik.id)
    if not p:
        return await i.response.send_message(
            embed=discord.Embed(
                description=f"❌ **{korisnik.display_name}** nema Poo-a.",
                color=0xE74C3C,
            ),
            ephemeral=True,
        )
    embed = build_poo_embed(p, korisnik, f"🐾 {korisnik.display_name}'s Poo")
    await i.response.send_message(embed=embed)

@mypoo_group.command(name="help", description="❓ Uputstvo za Poo Game")
async def slash_help(i: discord.Interaction):
    embed = discord.Embed(
        title="🐾 Poo Game — Uputstvo",
        description=(
            f"Svaki član ima **svog osobnog Poo-a**!\n"
            f"Brini se o njemu dok ne postane **Sveti Poo**! 💩✨\n\n"
            f"**Kanali:** Samo u #{POO_CHANNEL_NAME} 🔒\n"
            f"**Prefix:** `.poo [akcija]`  •  **Slash:** `/mypoo [akcija]`"
        ),
        color=POO_COLORS["default"],
        timestamp=datetime.now(timezone.utc),
    )
    embed.add_field(
        name="🚀 Počni",
        value="`/mypoo start [ime]` — Kreiraj Poo-a\n`/mypoo status` ili `.poo` — Pogledaj ga",
        inline=False,
    )
    embed.add_field(
        name="🎮 Dugmad na emberu",
        value=(
            "🍗 **Nahrani** *(20min CD)*\n"
            "🎮 **Igraj se** *(15min CD)*\n"
            "🧼 **Operi** *(30min CD)*\n"
            "😴 **Spavaj** *(2h CD, 2h sna)*\n"
            "💼 **Posao** *(45min CD)*\n"
            "🎁 **Dnevna** *(1× dnevno)*"
        ),
        inline=True,
    )
    embed.add_field(
        name="📊 Statistike",
        value=(
            "🍗 **Glad** — smanjuje se s vremenom\n"
            "😊 **Sreća** — igrom raste, dosadivanjem pada\n"
            "🧼 **Čistoća** — jedenjem i vremenom pada\n"
            "⚡ **Energija** — troši se igrom i radom\n"
            "❤️ **Zdravlje** — pada ako gladan ili prljav"
        ),
        inline=True,
    )
    faze = "\n".join([f"`{s[0]:>5} XP` — **{s[1]}**" for s in POO_STAGES])
    embed.add_field(name="⬆️ Faze Rasta", value=faze, inline=False)
    embed.set_footer(text="🐾 Poo Game  •  Dugmad na emberu zamjenjuju sve komande!")
    await i.response.send_message(embed=embed, ephemeral=True)


# ═══════════════════════════════════════════════════════════════
#   SETUP FUNCTION
# ═══════════════════════════════════════════════════════════════
async def setup(bot: commands.Bot):
    cog = PersonalPooGame(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(mypoo_group)
    print("✅ PersonalPooGame učitan — .poo i /mypoo aktivni!")
