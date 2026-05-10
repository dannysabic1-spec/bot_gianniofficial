# ╔══════════════════════════════════════════════════════════════════╗
#            🎉  GIANNI (Custom) — Glavni Bot                     ║
# ║   Welcome sistem + Poo Game + Anti-Spam                        ║
# ══════════════════════════════════════════════════════════════════╝

import discord
import asyncio
import random
import time
import os
from collections import defaultdict, deque
from datetime import datetime, timezone
from discord.ext import commands

# ── Učitavanje konfiguracije iz Railway Environment Variables ──
# Ove varijable MORAŠ postaviti u Railway -> Variables tab
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", 0))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", 0))
AUTO_ROLE_ID = int(os.getenv("AUTO_ROLE_ID", 0))
POO_CHANNEL_ID = int(os.getenv("POO_CHANNEL_ID", 0))

# Anti-spam postavke
SPAM_MSG_LIMIT = 5
SPAM_WINDOW_SEC = 3
SPAM_TIMEOUT_SEC = 60

# ═══════════════════════════════════════════════════════════════
# INTENTS & BOT
# ═══════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# ══════════════════════════════════════════════════════════════
# ANTI-SPAM SISTEM
# ═══════════════════════════════════════════════════════════════
_spam_tracker: dict[int, deque] = defaultdict(deque)
_spam_warned: set[int] = set()

async def _handle_spam(message: discord.Message) -> bool:
    """Vrati True ako je poruka spam (i obriše je), False ako je OK."""
    member = message.author
    if not isinstance(member, discord.Member):
        return False
    
    # Admini i botovi su imuni
    if member.bot or member.guild_permissions.administrator:
        return False
    
    uid = member.id
    now = time.time()
    dq = _spam_tracker[uid]

    # Dodaj timestamp, makni stare
    dq.append(now)
    while dq and dq[0] < now - SPAM_WINDOW_SEC:
        dq.popleft()

    if len(dq) >= SPAM_MSG_LIMIT:
        # Obriši poruke spamera u ovom kanalu
        try:
            await message.channel.purge(limit=10, check=lambda m: m.author.id == uid, reason="Anti-spam")
        except Exception:
            pass

        # Timeout
        try:
            import datetime as _dt
            await member.timeout(_dt.timedelta(seconds=SPAM_TIMEOUT_SEC), reason="Anti-spam")
        except Exception:
            pass

        # Upozorenje u kanal
        if uid not in _spam_warned:
            _spam_warned.add(uid)
            try:
                warn_embed = discord.Embed(
                    title="🚫 Spam detektovan!",
                    description=f"{member.mention} — previše poruka u kratkom vremenu!\nTimeout: **{SPAM_TIMEOUT_SEC}s** ⏱️",
                    color=0xE74C3C,
                    timestamp=datetime.now(timezone.utc),
                )
                warn_embed.set_footer(text="GIANNI Anti-Spam sistem")
                await message.channel.send(embed=warn_embed, delete_after=8)
            except Exception:
                pass
            
            asyncio.create_task(_clear_spam_warn(uid, SPAM_TIMEOUT_SEC + 2))

        dq.clear()
        return True
    return False

async def _clear_spam_warn(uid: int, delay: float):
    await asyncio.sleep(delay)
    _spam_warned.discard(uid)
    _spam_tracker.pop(uid, None)

# ═══════════════════════════════════════════════════════════════
# WELCOME PORUKE & GIF-OVI
# ═══════════════════════════════════════════════════════════════
WELCOME_MSGS = [
    "Hej {mention}! Drago nam je što si stigao/la! Upoznaj se i uživaj! 🍻",
    "Evo ga/je {mention}! Server tek sad može početi! ",
    "Pazi ekipa, {mention} je stigao/la! Dobrodošao/la u porodicu! 🏠❤️",
    "{mention} se pojavio/la! Bio/la si tu negdje, a? Dobrodošao/la! 👀",
    "Naš/a novi/a prijatelj/ica {mention} je stigao/la! Uživaj! ",
    "{mention} je ušao/la u chat! Čaj ili kafa? ☕",
    "Legenda stiže! Dobrodošao/la {mention}, spreman/a na zabavu? ",
    "Oh, ko je ovo? {mention}! Baš si nam nedostajao/la! 😂❤️",
    "Ekipa, {mention} je odlučio/la da nam se pridruži. Mudra odluka! 😎✨",
    "{mention} je stigao/la! Sjedni, opusti se, ti si sada dio GIANNI familije! 👑",
    "Čekali smo te, {mention}! Dobrodošao/la! ",
    "{mention} je kucao/la na vrata — otvorili smo! Dobrodošao/la! 🚪",
]

WELCOME_GIFS = [
    "https://media.tenor.com/M0vSf9CGHoEAAAAC/celebration.gif",
    "https://media.tenor.com/SoQgOZMVWKoAAAAC/welcome-hi.gif",
    "https://media.tenor.com/bTFOnAa2HTEAAAAC/welcome-neon.gif",
    "https://media.tenor.com/Yd1G5y4OIIMAAAAC/fireworks-celebrate.gif",
    "https://media.tenor.com/YP5R3oMtd3MAAAAC/welcome-party.gif",
]

WELCOME_JOKES = [
    "😄 Zašto programeri vole prirodu? Jer nema bugova! 🐛",
    "😂 Šta kaže nula osmici? 'Lijepo ti stoji kaiš!' 😂",
    " Zašto je kompjuter uvijek hladan? Jer ima puno Windows! ",
    " Kako se zove Eskimo koji sjedi na stolici? Polarna sjednica! 🧊",
    "😂 Zašto ribe ne igraju tenis? Jer se boje mreže! 🎾",
    "🤣 Šta kaže jedan zid drugom? 'Vidimo se na uglu!' 🧱",
    "😄 Zašto matematičari nikad ne idu na plažu? Imaju previše problema s brojevima! 🏖️",
    "😂 Kako se zove snjegović koji leži na suncu? Lokva! ️💧",
    "🤣 Zašto banane nose sunčane naočale? Da se ne ogule od sunca! 🍌😎",
    "😄 Šta kaže more plaži? Ništa, samo maše! 👋",
    "😂 Kako se zove pas koji voli magiju? Labra-kadabra-dor! 🐕✨",
]

# ═══════════════════════════════════════════════════════════════
# EVENTI
# ═══════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"✅ {bot.user} je spreman! ({bot.user.id})")
    print(f" Serveri: {len(bot.guilds)}")
    
    try:
        await bot.load_extension("poo_game")
    except Exception as e:
        print(f"[poo-game] Greška pri učitavanju: {e}")
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Sinkronizirano {len(synced)} slash komandi")
    except Exception as e:
        print(f"[sync] {e}")
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🐾 Poo Game | /mypoo start"
        )
    )

@bot.event
async def on_member_join(member: discord.Member):
    """Čisti welcome embed — uvijek radi, nikad ne puca."""
    guild = member.guild
    
    if AUTO_ROLE_ID:
        role = guild.get_role(AUTO_ROLE_ID)
        if role:
            try:
                await member.add_roles(role, reason="Auto-uloga za nove članove")
            except Exception:
                pass
    
    if LOG_CHANNEL_ID:
        log_ch = guild.get_channel(LOG_CHANNEL_ID)
        if log_ch:
            try:
                log_e = discord.Embed(
                    title="📥 Novi Član",
                    color=0x2ECC71,
                    timestamp=datetime.now(timezone.utc)
                )
                log_e.set_author(name=str(member), icon_url=member.display_avatar.url)
                log_e.add_field(name="ID", value=f"`{member.id}`", inline=True)
                log_e.add_field(name="Nalog kreiran", value=member.created_at.strftime("%d.%m.%Y."), inline=True)
                log_e.add_field(name="Ukupno članova", value=f"`{guild.member_count}`", inline=True)
                log_e.set_footer(text="GIANNI • Log sistem")
                await log_ch.send(embed=log_e)
            except Exception:
                pass
    
    chan = guild.get_channel(WELCOME_CHANNEL_ID)
    if not chan:
        chan = discord.utils.find(
            lambda c: "welcome" in c.name.lower() or "dobrodosli" in c.name.lower(),
            guild.text_channels
        )
    if not chan:
        return
    
    now_ts = int(datetime.now(timezone.utc).timestamp())
    acct_days = (datetime.now(timezone.utc) - member.created_at).days
    msg = random.choice(WELCOME_MSGS).format(mention=member.mention)
    joke = random.choice(WELCOME_JOKES)
    
    poo_ch = guild.get_channel(POO_CHANNEL_ID)
    
    desc = (
        f"## 🎊 Dobrodošao/la, {member.display_name}!\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"{msg}\n\n"
        f"**Gdje početi?** 🗺️\n"
        f" Pročitaj pravila i uzmi uloge\n"
        f"💬 Pozdravi se u chatu\n"
        f"🐾 Pokreni svog Poo-a u {poo_ch.mention if poo_ch else '#poo-game'}!\n\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"👥 Si nam **#{guild.member_count}.** član  ·   discord.gg/gian"
    )
    
    embed = discord.Embed(
        description=desc,
        color=0xFFD700,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(
        name=" GIANNI Community — Dobrodošlica ",
        icon_url=guild.icon.url if guild.icon else None,
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="😄 Šala dobrodošlice", value=joke, inline=False)
    embed.add_field(name="⏰ Pridružio/la", value=f"<t:{now_ts}:R>", inline=True)
    embed.add_field(name=" Nalog star", value=f"**{acct_days}** dana", inline=True)
    embed.set_image(url=random.choice(WELCOME_GIFS))
    embed.set_footer(
        text="GIANNI (Custom)  ·  discord.gg/gian",
        icon_url=member.display_avatar.url,
    )
    
    try:
        await chan.send(content=member.mention, embed=embed)
    except discord.Forbidden:
        print(f"[welcome] Bot nema dozvolu za slanje u #{chan.name}")
    except Exception as e:
        print(f"[welcome] Greška: {e}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.guild:
        is_spam = await _handle_spam(message)
        if is_spam:
            return
    
    content = message.content.strip().lower()
    if content in (".poo", ".mypoo"):
        poo_ch = (message.guild.get_channel(POO_CHANNEL_ID) if message.guild else None)
        try:
            await message.delete()
        except Exception:
            pass
        embed = discord.Embed(
            title="🐾 Poo Game",
            description=(
                f"{message.author.mention} — Poo Game komande koristi u "
                f"{poo_ch.mention if poo_ch else f'<#{POO_CHANNEL_ID}>'}!\n\n"
                f"Tamo kucaj `/mypoo start` da pokreneš svog Poo-a!"
            ),
            color=0x8B4513,
        )
        embed.set_footer(text="🐾 GIANNI Poo Game")
        try:
            await message.channel.send(embed=embed, delete_after=12)
        except Exception:
            pass
        return
    
    await bot.process_commands(message)

# ═══════════════════════════════════════════════════════════════
# POKRETANJE
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not TOKEN:
        print("❌ GREŠKA: TOKEN nije postavljen! Provjeri Railway → Variables tab")
        exit(1)
    bot.run(TOKEN)
