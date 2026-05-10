# ╔══════════════════════════════════════════════════════════════════╗
# ║         🤖 GIANNI (Custom) — GLAVNI BOT                        ║
# ╠══════════════════════════════════════════════════════════════════╣
# ║                                                                  ║
# ║   TOKEN SE NE UPISUJE OVDJE — dodaj ga u worker kao:           ║
# ║   Environment Variable:  DISCORD_TOKEN = tvoj_token            ║
# ║                                                                  ║
# ║   (Bot automatski čita DISCORD_TOKEN iz okruženja)              ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

import discord
import asyncio
import os
from discord.ext import commands
from discord import app_commands

BOT_NAME = "GIANNI (Custom)"
VERSION  = "v2.3"

# Čita token iz environment varijable — postavi u workeru kao DISCORD_TOKEN
TOKEN = os.environ.get("DISCORD_TOKEN", "")

# ═══════════════════════════════════════════════════════════════
#   INTENTS
# ═══════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members         = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# ═══════════════════════════════════════════════════════════════
#   KOMPLETAN HELP EMBED
# ═══════════════════════════════════════════════════════════════
def _build_help_embed() -> discord.Embed:
    embed = discord.Embed(
        title=f"📖  {BOT_NAME} — Sve Komande",
        description=(
            "**Svaka komanda radi i sa `.` prefixom i sa `/` slash!**\n"
            "Primjer: `.help` = `/help` • `.poo` = `/mypoo status`\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=0x00BCD4,
        timestamp=discord.utils.utcnow(),
    )
    embed.add_field(
        name="🐾 Poo Game  *(samo u #poo kanalu)*",
        value=(
            "`.poo` — Otvori svog Poo-a sa dugmadima\n"
            "`.poo feed` — 🍗 Nahrani *(20 min CD)*\n"
            "`.poo play` — 🎮 Igraj se *(15 min CD)*\n"
            "`.poo clean` — 🧼 Operi *(30 min CD)*\n"
            "`.poo work` — 💼 Posao *(45 min CD)*\n"
            "`.poo sleep` — 😴 Spavaj *(2h CD)*\n"
            "`.poo daily` — 🎁 Dnevna nagrada *(1× dnevno)*\n"
            "`.poo top` — 🏆 Top 10 ljestvica\n"
            "`.poo help` — ❓ Detaljna uputstva\n"
            "\n*Slash:* `/mypoo start [ime]` • `/mypoo status` • `/mypoo rename` • `/mypoo leaderboard`"
        ),
        inline=False,
    )
    embed.add_field(
        name="⚙️ Admin Setup  *(samo admini)*",
        value=(
            "`.setup-welcome #kanal` — Postavi welcome kanal\n"
            "`.welcome-info` — Provjeri welcome podešavanja\n"
            "\n*Slash:* `/setup-welcome #kanal [poruka] [gif] [dm]` • `/welcome-info`"
        ),
        inline=False,
    )
    embed.add_field(
        name="📋 Ostalo",
        value=(
            "`.help` — 📖 Ova lista komandi\n"
            "`.pravila` — 📜 Pravila servera i bota\n"
            "`.ping` — 🏓 Provjeri da li bot radi"
        ),
        inline=False,
    )
    embed.add_field(
        name="💡 Savjeti",
        value=(
            "• Sva dugmad na Poo emberu mijenjaju emoji **live**!\n"
            "• Anti-spam aktivan u svim kanalima\n"
            "• Welcome se podešava jednom sa `/setup-welcome`"
        ),
        inline=False,
    )
    embed.set_footer(text=f"{BOT_NAME} {VERSION}  •  discord.gg/gian")
    return embed


# ═══════════════════════════════════════════════════════════════
#   PRAVILA EMBED
# ═══════════════════════════════════════════════════════════════
def _build_pravila_embed() -> discord.Embed:
    embed = discord.Embed(
        title="📜  GIANNI — Pravila Servera & Bota",
        description=(
            "Dobrodošao/la na **GIANNI** server!\n"
            "Poštuj pravila i uživaj u zajednici. 🍻\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=0xFFD700,
        timestamp=discord.utils.utcnow(),
    )
    embed.add_field(
        name="🇧🇦 Pravila Servera",
        value=(
            "**1.** Poštuj sve članove — nema vrijeđanja ni diskriminacije\n"
            "**2.** Nema reklama ni invite linkova bez dozvole admina\n"
            "**3.** Nema spam poruka ni flood-a\n"
            "**4.** Sadržaj mora biti primjeren kanalu\n"
            "**5.** Slušaj upute admina i moderatora\n"
            "**6.** Nema dijeljenja osobnih podataka tuđih osoba\n"
            "**7.** Govori kulturno — nema provociranja\n"
            "**8.** Poo game komande **samo u #poo kanalu**"
        ),
        inline=False,
    )
    embed.add_field(
        name="🤖 Komande Bota  *(. ili / — oboje radi)*",
        value=(
            "**Poo Game** *(samo #poo):*\n"
            "`.poo` `.poo feed` `.poo play` `.poo clean`\n"
            "`.poo work` `.poo sleep` `.poo daily` `.poo top`\n"
            "*/mypoo start* • */mypoo status* • */mypoo rename* • */mypoo leaderboard*\n\n"
            "**Opće:**\n"
            "`.help` • `.pravila` • `.ping`\n\n"
            "**Admin:**\n"
            "`.setup-welcome #kanal` • `.welcome-info`"
        ),
        inline=False,
    )
    embed.add_field(
        name="🛡️ Anti-Spam",
        value=(
            "🔴 Max **5 poruka / 5 sekundi**\n"
            "🔴 Max **3 iste poruke** zaredom\n"
            "🔴 Max **10 emojia** po poruci\n"
            "⚪ Admini su izuzeti"
        ),
        inline=False,
    )
    embed.set_footer(text=f"{BOT_NAME} {VERSION}  •  discord.gg/gian")
    return embed


# ═══════════════════════════════════════════════════════════════
#   PREFIX KOMANDE
# ═══════════════════════════════════════════════════════════════
@bot.command(name="help", aliases=["h", "komande"])
async def cmd_help(ctx):
    await ctx.send(embed=_build_help_embed())

@bot.command(name="pravila", aliases=["rules", "pr"])
async def cmd_pravila(ctx):
    await ctx.send(embed=_build_pravila_embed())

@bot.command(name="ping", aliases=["p"])
async def cmd_ping(ctx):
    lat = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot radi! ✅\n\n**Latencija:** `{lat} ms`",
        color=0x00E676 if lat < 150 else 0xF39C12,
        timestamp=discord.utils.utcnow(),
    )
    embed.set_footer(text=f"{BOT_NAME} {VERSION}")
    await ctx.send(embed=embed)

@bot.command(name="setup-welcome", aliases=["setupwelcome", "sw"])
@commands.has_permissions(administrator=True)
async def cmd_prefix_setup_welcome(ctx, kanal: discord.TextChannel = None):
    if not kanal:
        return await ctx.send(
            embed=discord.Embed(
                description="❌ Koristi: `.setup-welcome #kanal`\nIli slash: `/setup-welcome #kanal`",
                color=0xE74C3C,
            ), delete_after=10,
        )
    import json
    cfg_file = "welcome_config.json"
    cfg = {}
    try:
        if os.path.exists(cfg_file):
            with open(cfg_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
    except Exception:
        pass
    cfg[str(ctx.guild.id)] = {"channel_id": kanal.id, "show_gif": True, "dm_enabled": True}
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    await ctx.send(embed=discord.Embed(
        title="✅ Welcome kanal podešen!",
        description=f"📢 Welcome poruke idu u {kanal.mention}",
        color=0x00E676, timestamp=discord.utils.utcnow(),
    ))

@cmd_prefix_setup_welcome.error
async def _sw_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(description="❌ Trebaš **Administrator** dozvolu!", color=0xE74C3C), delete_after=6)

@bot.command(name="welcome-info", aliases=["welcomeinfo", "wi"])
@commands.has_permissions(manage_guild=True)
async def cmd_prefix_welcome_info(ctx):
    import json
    cfg_file = "welcome_config.json"
    cfg = {}
    try:
        if os.path.exists(cfg_file):
            with open(cfg_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
    except Exception:
        pass
    gid = str(ctx.guild.id)
    if gid not in cfg:
        return await ctx.send(embed=discord.Embed(
            description="⚠️ Welcome nije podešen!\nKoristi `.setup-welcome #kanal`", color=0xF39C12,
        ), delete_after=10)
    ch = ctx.guild.get_channel(cfg[gid].get("channel_id", 0))
    embed = discord.Embed(title="📋 Welcome Podešavanja", color=0x00BCD4, timestamp=discord.utils.utcnow())
    embed.add_field(name="📢 Kanal", value=ch.mention if ch else "❌ Kanal ne postoji!", inline=True)
    embed.add_field(name="🎞️ GIF",  value="✅ Da" if cfg[gid].get("show_gif", True) else "❌ Ne", inline=True)
    embed.add_field(name="📨 DM",    value="✅ Da" if cfg[gid].get("dm_enabled", True) else "❌ Ne", inline=True)
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════════════
#   SLASH KOMANDE
# ═══════════════════════════════════════════════════════════════
@bot.tree.command(name="help", description="📖 Lista svih komandi bota")
async def slash_help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=_build_help_embed(), ephemeral=True)

@bot.tree.command(name="pravila", description="📜 Pravila servera i bota sa listom komandi")
async def slash_pravila(interaction: discord.Interaction):
    await interaction.response.send_message(embed=_build_pravila_embed())

@bot.tree.command(name="ping", description="🏓 Provjeri da li bot radi")
async def slash_ping(interaction: discord.Interaction):
    lat = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot radi! ✅\n\n**Latencija:** `{lat} ms`",
        color=0x00E676 if lat < 150 else 0xF39C12,
        timestamp=discord.utils.utcnow(),
    )
    embed.set_footer(text=f"{BOT_NAME} {VERSION}")
    await interaction.response.send_message(embed=embed)


# ═══════════════════════════════════════════════════════════════
#   ON READY
# ═══════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"\n{'═'*60}")
    print(f"  ✅  {BOT_NAME} {VERSION} — ONLINE")
    print(f"  👤  {bot.user} (ID: {bot.user.id})")
    print(f"  🏠  Serveri: {len(bot.guilds)}")
    print(f"{'═'*60}")
    try:
        synced = await bot.tree.sync()
        print(f"  ✔  Sync: {len(synced)} komandi")
    except Exception as e:
        print(f"  ✘  Sync greška: {e}")
    for guild in bot.guilds:
        try:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f"  ✔  {guild.name}")
        except Exception as e:
            print(f"  ✘  {guild.name}: {e}")
    print(f"{'═'*60}\n")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    await bot.process_commands(message)


# ═══════════════════════════════════════════════════════════════
#   UČITAVANJE COGOVA
# ═══════════════════════════════════════════════════════════════
async def load_cogs():
    for module, name in [("poo_game","🐾 Poo Game"),("welcome_cog","🎉 Welcome"),("anti_spam_cog","🛡️ Anti-Spam")]:
        try:
            await bot.load_extension(module)
            print(f"  ✔  {name}")
        except Exception as e:
            print(f"  ✘  {name} GREŠKA: {e}")


# ═══════════════════════════════════════════════════════════════
#   POKRETANJE
# ═══════════════════════════════════════════════════════════════
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
