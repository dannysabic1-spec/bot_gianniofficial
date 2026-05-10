# ╔══════════════════════════════════════════════════════════════════╗
# ║     🎉 GIANNI — WELCOME COG (v3.0)                             ║
# ║  /setup-welcome → postavi kanal jednom, uvijek radi            ║
# ║  Nema hardkodiranih ID-eva — sve se čuva automatski            ║
# ╚══════════════════════════════════════════════════════════════════╝

import discord
import json
import os
import random
from datetime import datetime, timezone
from discord import app_commands
from discord.ext import commands

# ═══════════════════════════════════════════════════════════════
#   CONFIG STORAGE
#   Čuva podešavanja po serveru u welcome_config.json
# ═══════════════════════════════════════════════════════════════
WELCOME_CONFIG_FILE = "welcome_config.json"

def _load_cfg() -> dict:
    if os.path.exists(WELCOME_CONFIG_FILE):
        try:
            with open(WELCOME_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def _save_cfg(cfg: dict):
    try:
        with open(WELCOME_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[welcome-cfg] save error: {e}")

_welcome_cfg: dict = _load_cfg()

# ═══════════════════════════════════════════════════════════════
#   WELCOME PORUKE
# ═══════════════════════════════════════════════════════════════
WELCOME_MESSAGES = [
    "Hej {mention}! Drago nam je što si stigao/la! Ispoštuj pravila i uživaj! 🍻",
    "Evo ga/je {mention}! Server tek sad može početi! 🎉",
    "Pazi ekipa, {mention} je stigao/la! Dobrodošao/la u porodicu! 🏠❤️",
    "{mention} se pojavio/la! Dobrodošao/la! 👀",
    "Naš/a novi/a prijatelj/ica {mention} je stigao/la! Sretno i uživaj! 🌟",
    "{mention} ušao/la u chat! Čaj ili kafa? ☕",
    "Legenda stiže! Dobrodošao/la {mention}! 🎮",
    "Alarm! {mention} je upravo sletio/la na server! 🚨🎊",
    "Čekali smo te, {mention}! Dobrodošao/la! 🥰",
    "Server +1! {mention} se pridružio/la! 💪🎉",
    "{mention} kucao/la na vrata — otvorili smo! Dobrodošao/la! 🚪🎊",
    "Hej hej hej! {mention} je ovdje! Server dobio upgrade! ⬆️",
    "Oh, ko je ovo? {mention}! Baš si nam nedostajao/la, a ni ne znamo te još! 😂❤️",
    "{mention} je ušao/la u zgradu. Dobrodošao/la! 🏢🎉",
    "Sjedni, opusti se, {mention} — sada si dio GIANNI familije! 👑",
]

WELCOME_JOKES = [
    "😄 Zašto programeri vole prirodu? Jer nema bugova!",
    "😂 Šta kaže nula osmici? 'Lijepo ti stoji kaiš!'",
    "🤣 Zašto je kompjuter uvijek hladan? Jer ima puno Windows!",
    "😄 Zašto ribe ne igraju tenis? Jer se boje mreže! 🎾",
    "😂 Šta kaže jedan zid drugom? 'Vidimo se na uglu!'",
    "🤣 Zašto banane nose naočare? Da se ne ogule od sunca! 🍌",
    "😄 Šta kaže more plaži? Ništa, samo maše! 🌊",
    "😂 Kako se zove pas koji voli magiju? Labra-kadabra-dor! 🐕",
    "🤣 Zašto je škola kao zatvor? Niko ne želi ići! 🏫",
    "😄 Šta kaže tava tiganju? 'Daj mi prostora!'",
    "😂 Zašto slon ne može koristiti kompjuter? Jer se boji miša! 🐘",
    "🤣 Kako se zove snjegović na suncu? Lokva! ☀️💧",
    "😄 Šta kaže jedna vrata drugima? 'Ključ je da se ne zaključaš u sebi!'",
    "😂 Zašto krava nosi zvonce? Jer joj rogovi ne rade! 🐄",
    "🤣 Balkanski sat: 'Dođi u 7' znači dođi u 8:30! ⏰",
]

WELCOME_GIFS = [
    "https://media.tenor.com/M0vSf9CGHoEAAAAC/celebration.gif",
    "https://media.tenor.com/SoQgOZMVWKoAAAAC/welcome-hi.gif",
    "https://media.tenor.com/Yd1G5y4OIIMAAAAC/fireworks-celebrate.gif",
    "https://media.tenor.com/YP5R3oMtd3MAAAAC/welcome-party.gif",
]


class WelcomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── Pronađi welcome kanal ─────────────────────────────────
    def _get_channel(self, guild: discord.Guild) -> discord.TextChannel | None:
        gid = str(guild.id)

        # 1. Iz config-a (postavljeno sa /setup-welcome)
        if gid in _welcome_cfg:
            ch_id = _welcome_cfg[gid].get("channel_id")
            if ch_id:
                ch = guild.get_channel(ch_id)
                if ch and ch.permissions_for(guild.me).send_messages:
                    return ch

        # 2. Fallback: kanal sa "welcome" ili "dobrodoslica" u imenu
        for ch in guild.text_channels:
            name = ch.name.lower()
            if any(x in name for x in ("welcome", "dobrodoslic", "dobrodošlic", "pozdrav")):
                if ch.permissions_for(guild.me).send_messages:
                    return ch

        # 3. Fallback: system channel
        if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
            return guild.system_channel

        return None

    # ── on_member_join ────────────────────────────────────────
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        chan  = self._get_channel(guild)
        if not chan:
            return

        gid     = str(guild.id)
        cfg     = _welcome_cfg.get(gid, {})
        now_ts  = int(datetime.now(timezone.utc).timestamp())
        age_d   = (datetime.now(timezone.utc) - member.created_at).days
        mbr_no  = guild.member_count

        # Poruka — custom iz /setup-welcome ili random
        if cfg.get("custom_message"):
            personal = cfg["custom_message"].replace("{mention}", member.mention).replace("{name}", member.display_name).replace("{server}", guild.name)
        else:
            personal = random.choice(WELCOME_MESSAGES).format(mention=member.mention, name=member.display_name, server=guild.name)

        joke = random.choice(WELCOME_JOKES)

        # ── EMBED ──
        embed = discord.Embed(
            description=(
                f"## 🎊 Dobrodošao/la, {member.mention}!\n\n"
                f"{personal}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 **Pročitaj pravila** i upoznaj server!\n"
                f"💬 **Kreni chatati** i upoznaj ekipu!\n"
                f"📈 **Skupljaj XP** i napreduj!\n"
                f"🐾 **Pokreni svog Poo-a** — `/mypoo start`!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"**Si nam #{mbr_no}. član!** 🏅"
            ),
            color=cfg.get("color", 0xFFD700),
            timestamp=datetime.now(timezone.utc),
        )
        embed.set_author(
            name="✦ GIANNI Community — Nova Akvizicija! ✦",
            icon_url=guild.icon.url if guild.icon else None,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="😄 Šala dobrodošlice", value=joke, inline=False)
        embed.add_field(name="👥 Redni broj",  value=f"**#{mbr_no}**",   inline=True)
        embed.add_field(name="⏰ Stigao/la",   value=f"<t:{now_ts}:R>",  inline=True)
        embed.add_field(name="📅 Nalog star",  value=f"**{age_d} dana**", inline=True)

        # GIF slika (opciono)
        if cfg.get("show_gif", True):
            embed.set_image(url=random.choice(WELCOME_GIFS))

        embed.set_footer(
            text="GIANNI • discord.gg/gian",
            icon_url=member.display_avatar.url,
        )

        try:
            await chan.send(content=member.mention, embed=embed)
        except discord.Forbidden:
            print(f"[welcome] Nema dozvole u #{chan.name}")
        except Exception as e:
            print(f"[welcome] Greška: {e}")

        # ── DM ──
        if cfg.get("dm_enabled", True):
            try:
                dm = discord.Embed(
                    title=f"🎉 Dobrodošao/la na {guild.name}!",
                    description=(
                        f"Hej **{member.display_name}**! Drago nam je što si ovdje! 🥳\n\n"
                        f"📋 Pročitaj pravila i upoznaj server\n"
                        f"💬 Kreni chatati sa ekipom\n"
                        f"🎮 Sve komande → `/help`\n"
                        f"🐾 Napravi svog Poo-a → `/mypoo start`\n\n"
                        f"🔗 **discord.gg/gian**\n\n"
                        f"Dobrodošao/la u **GIANNI** porodicu! 🍻"
                    ),
                    color=cfg.get("color", 0xFFD700),
                    timestamp=datetime.now(timezone.utc),
                )
                if guild.icon:
                    dm.set_thumbnail(url=guild.icon.url)
                dm.set_footer(text="GIANNI • Welcome Bot")
                await member.send(embed=dm)
            except Exception:
                pass

    # ═══════════════════════════════════════════════════════════
    #   /setup-welcome — postavi welcome kanal
    # ═══════════════════════════════════════════════════════════
    @app_commands.command(name="setup-welcome", description="⚙️ Postavi welcome kanal i poruku [ADMIN]")
    @app_commands.describe(
        kanal="Kanal gdje bot šalje welcome poruke",
        poruka="Custom poruka (koristi {mention}, {name}, {server}) — ostavi prazno za random",
        gif="Prikaži GIF sliku u welcome emberu? (da/ne)",
        dm="Pošalji DM novom članu? (da/ne)",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def cmd_setup_welcome(
        self,
        interaction: discord.Interaction,
        kanal: discord.TextChannel,
        poruka: str = None,
        gif: bool = True,
        dm: bool = True,
    ):
        gid = str(interaction.guild_id)

        if not kanal.permissions_for(interaction.guild.me).send_messages:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"❌ Nemam dozvolu za slanje poruka u {kanal.mention}!\nDaj mi **Send Messages** u tom kanalu.",
                    color=0xE74C3C,
                ),
                ephemeral=True,
            )

        _welcome_cfg[gid] = {
            "channel_id":     kanal.id,
            "custom_message": poruka,
            "show_gif":       gif,
            "dm_enabled":     dm,
            "color":          0xFFD700,
        }
        _save_cfg(_welcome_cfg)

        # Potvrda
        embed = discord.Embed(
            title="✅ Welcome sistem podešen!",
            color=0x00E676,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="📢 Kanal",   value=kanal.mention,                                         inline=True)
        embed.add_field(name="🎞️ GIF",    value="✅ Da" if gif else "❌ Ne",                             inline=True)
        embed.add_field(name="📨 DM",      value="✅ Da" if dm else "❌ Ne",                             inline=True)
        embed.add_field(
            name="💬 Poruka",
            value=poruka or "*Random (20 različitih poruka)*",
            inline=False,
        )
        embed.add_field(
            name="📌 Varijable u custom poruci",
            value="`{mention}` — mention člana\n`{name}` — nick člana\n`{server}` — ime servera",
            inline=False,
        )
        embed.set_footer(text="GIANNI Welcome • Podešeno!")
        await interaction.response.send_message(embed=embed)

        # Test poruka u welcome kanalu
        test = discord.Embed(
            description=(
                f"🔧 **Test welcome poruke** — sistem je upravo podešen!\n\n"
                f"Kad se sljedeći član pridruži, dobit će welcome ovdje. 🎉"
            ),
            color=0x00E676,
        )
        test.set_footer(text="GIANNI • /setup-welcome test")
        try:
            await kanal.send(embed=test)
        except Exception:
            pass

    # ── Error handler za permissions ────────────────────────────
    @cmd_setup_welcome.error
    async def setup_welcome_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="❌ Trebaš **Administrator** dozvolu da koristiš `/setup-welcome`!",
                    color=0xE74C3C,
                ),
                ephemeral=True,
            )

    # ═══════════════════════════════════════════════════════════
    #   /welcome-info — provjeri trenutna podešavanja
    # ═══════════════════════════════════════════════════════════
    @app_commands.command(name="welcome-info", description="📋 Pogledaj trenutna welcome podešavanja")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def cmd_welcome_info(self, interaction: discord.Interaction):
        gid = str(interaction.guild_id)
        cfg = _welcome_cfg.get(gid)

        if not cfg:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=(
                        "⚠️ Welcome nije podešen!\n\n"
                        "Koristi `/setup-welcome #kanal` da ga aktiviraš."
                    ),
                    color=0xF39C12,
                ),
                ephemeral=True,
            )

        ch = interaction.guild.get_channel(cfg.get("channel_id", 0))
        embed = discord.Embed(
            title="📋 Welcome Podešavanja",
            color=0x00BCD4,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="📢 Kanal",  value=ch.mention if ch else "❌ Kanal ne postoji!",    inline=True)
        embed.add_field(name="🎞️ GIF",   value="✅ Da" if cfg.get("show_gif", True) else "❌ Ne", inline=True)
        embed.add_field(name="📨 DM",     value="✅ Da" if cfg.get("dm_enabled", True) else "❌ Ne", inline=True)
        embed.add_field(
            name="💬 Custom poruka",
            value=cfg.get("custom_message") or "*Random (20 različitih)*",
            inline=False,
        )
        embed.set_footer(text="Izmijeni sa /setup-welcome")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @cmd_welcome_info.error
    async def welcome_info_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed=discord.Embed(description="❌ Trebaš **Manage Server** dozvolu!", color=0xE74C3C),
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(WelcomeCog(bot))
    print("✅ WelcomeCog učitan — /setup-welcome i /welcome-info aktivni!")
