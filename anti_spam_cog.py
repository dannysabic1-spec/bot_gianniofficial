# ╔══════════════════════════════════════════════════════════════════╗
# ║     🛡️ GIANNI — ANTI-SPAM COG                                  ║
# ║  Blokira spam u svim kanalima (emoji, ponavljanje, flood)      ║
# ╚══════════════════════════════════════════════════════════════════╝

import discord
import asyncio
from collections import defaultdict, deque
from datetime import datetime, timezone
from discord.ext import commands

# ═══════════════════════════════════════════════════════════════
#   KONFIGURACIJA
# ═══════════════════════════════════════════════════════════════
SPAM_MAX_MSGS    = 5      # max poruka u...
SPAM_INTERVAL    = 5.0    # ...sekundi po korisniku
SPAM_SAME_MSG    = 3      # koliko puta ista poruka = spam
SPAM_MAX_EMOJIS  = 10     # max emojia u jednoj poruci
SPAM_WARN_DELETE = 8      # sekundi do brisanja upozorenja
SPAM_MUTE_SECS   = 60     # sekundi mute pri prekršaju (0 = bez mute)

# Kanali koji su izuzeti od anti-spama (po ID-u ili imenu)
SPAM_EXEMPT_CHANNEL_IDS   = []        # npr. [123456789, 987654321]
SPAM_EXEMPT_CHANNEL_NAMES = ["spam", "meme", "off-topic"]  # kanali gdje je spam ok

# ═══════════════════════════════════════════════════════════════
#   TRACKER
# ═══════════════════════════════════════════════════════════════
_msg_history:  dict[int, deque]  = defaultdict(lambda: deque())
_same_history: dict[int, list]   = defaultdict(list)
_warned:       set[int]          = set()


class AntiSpamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _is_exempt(self, channel) -> bool:
        if channel.id in SPAM_EXEMPT_CHANNEL_IDS:
            return True
        for name_part in SPAM_EXEMPT_CHANNEL_NAMES:
            if name_part.lower() in channel.name.lower():
                return True
        return False

    def _count_emojis(self, text: str) -> int:
        import re
        custom  = len(re.findall(r"<a?:\w+:\d+>", text))
        unicode = len([c for c in text if ord(c) > 0x1F300])
        return custom + unicode

    async def _warn_and_delete(self, message: discord.Message, reason: str):
        try:
            await message.delete()
        except Exception:
            pass

        uid = message.author.id
        if uid in _warned:
            return
        _warned.add(uid)

        try:
            embed = discord.Embed(
                description=(
                    f"🛡️ {message.author.mention} — **{reason}**\n"
                    f"Molimo te da poštuješ pravila servera!"
                ),
                color=0xE74C3C,
                timestamp=datetime.now(timezone.utc),
            )
            embed.set_footer(text="Upozorenje se briše za 8s")
            warn_msg = await message.channel.send(embed=embed)

            await asyncio.sleep(SPAM_WARN_DELETE)
            try:
                await warn_msg.delete()
            except Exception:
                pass
        except Exception:
            pass
        finally:
            await asyncio.sleep(5)
            _warned.discard(uid)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        if self._is_exempt(message.channel):
            return

        try:
            if message.author.guild_permissions.administrator:
                return
        except Exception:
            return

        uid     = message.author.id
        content = message.content
        now     = datetime.now(timezone.utc).timestamp()

        # ── 1. FLOOD (previše poruka brzo) ──────────────────────
        history = _msg_history[uid]
        history.append(now)
        while history and now - history[0] > SPAM_INTERVAL:
            history.popleft()

        if len(history) > SPAM_MAX_MSGS:
            await self._warn_and_delete(message, "Previše poruka! Polako malo, ne spamaj!")
            return

        # ── 2. ISTE PORUKE (copy-paste spam) ────────────────────
        same = _same_history[uid]
        same.append(content.strip().lower()[:100])
        if len(same) > SPAM_SAME_MSG * 2:
            same.pop(0)

        last_n = same[-SPAM_SAME_MSG:]
        if len(last_n) == SPAM_SAME_MSG and len(set(last_n)) == 1:
            _same_history[uid] = []
            await self._warn_and_delete(message, "Ne šalji istu poruku više puta!")
            return

        # ── 3. PREVIŠE EMOJIA ───────────────────────────────────
        if self._count_emojis(content) > SPAM_MAX_EMOJIS:
            await self._warn_and_delete(message, f"Previše emojia! Max {SPAM_MAX_EMOJIS} po poruci.")
            return

        # ── 4. CAPS LOCK SPAM (>80% velikih slova, duža poruka) ─
        letters = [c for c in content if c.isalpha()]
        if len(letters) > 20:
            caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
            if caps_ratio > 0.8:
                await self._warn_and_delete(message, "Ne vičи (CAPS LOCK)! Sniži ton malo.")
                return


async def setup(bot: commands.Bot):
    await bot.add_cog(AntiSpamCog(bot))
    print("✅ AntiSpamCog učitan!")
