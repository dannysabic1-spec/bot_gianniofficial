import discord, random, asyncio, json, os, time, aiohttp, re
from collections import defaultdict, deque, Counter
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timezone, timedelta

# ═══════════════════════════════════════════
#           KONFIGURACIJA
# ═══════════════════════════════════════════
BOT_NAME = "GIANNI (Custom Game Vanity)"
VERSION  = "v2.0"
TOKEN    = os.environ.get("DISCORD_TOKEN")

COLORS = {
    "default": 0x00BCD4, "success": 0x00E5FF, "error":   0xE74C3C,
    "warning": 0xF39C12, "info":    0x00BCD4, "gold":    0xF1C40F,
    "balkan":  0x00BCD4, "purple":  0x00BCD4, "fun":     0x00BCD4,
    "dark":    0x2C2F33, "teal":    0x00BCD4, "love":    0xFF4D6D,
    "pink":    0x00BCD4,
    "aqua":    0x00BCD4,
}

JOBS = [
    "Radio si kao konobar 🍺", "Čuvao si baku 🧓", "Prodavao ćevape 🥙",
    "Vozio si taksi 🚕", "Radio si na građevini 🏗️", "Popravljao auta 🔧",
    "Čuvao parking 🚗", "Nosio poštu 📬", "Prodavao lubenicu 🍉",
    "Brao paprike u polju 🌶️", "Radio u pekari 🥖", "Čuvao ovce 🐑",
    "Prodavao karte na stanici 🚌", "Radio kao zaštitar 💪", "Prao automobile 🚿",
]

EIGHTBALL_REPLIES = [
    "🟢 Definitivno da!", "🟢 Sve znakovi govore — DA.",
    "🟢 Bez ikakve sumnje, majstore!", "🟢 Računaj na to, brate.",
    "🟡 Pitaj ponovo malo kasnije.", "🟡 Nisam baš siguran, brate.",
    "🟡 Teško reći u ovom trenutku.", "🟡 Magla mi zaklanja odgovor.",
    "🔴 Ne računaj na to.", "🔴 Odgovor je jasno — NE.",
    "🔴 Izgledi su jako loši.", "🔴 Zaboravi na to, majstore.",
]

# ═══════════════════════════════════════════
#    MEMOVI (veliki bazen sa rotacijom)
# ═══════════════════════════════════════════
MEMES = [
    "Kad kažeš 'samo još 5 minuta' a prođe 3 sata. 😴📱",
    "Baka: 'Jesi li jeo?' Ti: 'Jesam.' Baka: 'A jesi li gladan?' 🍽️👵",
    "Kad upališ klimu na 16°C a napolju je 40°C. ❄️🥵",
    "Turbofolk u 3 ujutru, sutra na posao u 7. 🎶😵",
    "Kad kažeš 'idemo na kafu' a završiš na roštilju do zore. 🥩🍻",
    "Svaki Balkanac ima ujaka koji sve zna popraviti. 🔧😂",
    "'Sačekaj 5 minuta' — Balkan vreme: 45 minuta minimum. ⏰🤌",
    "Kad pitaš baku za recept: 'Malo ovog, malo onog, dok ne bude dobro.' 📏👵",
    "Kad kaže 'idem odmah' a gleda TV već sat vremena. 📺🛋️",
    "Ništa me ne boli više nego kad mi telefon padne na lice u krevetu. 📱😩",
    "Balkan dijetа: ne jedeš između obroka. Obroci su svaki sat. 🍴⏱️",
    "Komšija u 11 noću: buši zidove. Normalnost. 🔨🏠",
    "Kad mama kaže 'pričekaj dok dođemo kući' — Bog te čuvaj. 😰🏡",
    "'Idemo samo na malo' — 6 sati kasnije. 😂⌛",
    "Kad vidiš stranca u selu svi izlaze da gledaju. 👀🏡",
    "Balkan autopilot: čim sjedneš — telefon u ruci. 📱🧠",
    "Svaka baka misli da je njeno dijete premršavo. Vaga se ne slaže. ⚖️👵",
    "Na Balkanu se ne kaže 'hvala' u kafani. Prstom se kuca po stolu. 🫵☕",
    "Kad kažeš da si sit a vidiš čevape. 🥙😤",
    "Balkanska logika: ne možeš biti bolestan ljeti, samo zimi. ☀️🤧",
    "Baka čuva svaku vrećicu od kupovine već 30 godina. 🛍️♻️",
    "Kad ti kaže 'nisam ljuta' — bježi. 😬💨",
    "Balkanska dijalektika: svaka rasprava završi pričom o ratu. ⚔️🗣️",
    "Pranje auta = kiša za 2 sata garantovana. 🚗🌧️",
    "Kada slušaš muziku na slušalicama a mama govori s tobom. 🎧😤",
    "Spavanje na plaži sa šeširom na licu. Balkanski ljetni odmor. 🏖️👒",
    "Na Balkanu svadbena muzika mora biti glasnija od aviona. ✈️🎵",
    "'Ajde brzo' — 20 minuta čekanja. 🏃⏳",
    "Kad dobiješ viber poruku od mame u 2 noću: 'Jesi li stigao?' 📲😅",
    "Piknik bez kajmaka — nije piknik. 🧀🌿",
    "Svaki kvar na autu Balkanac može dijagnosticirati zvukom. 🚗👂",
    "Kad ti komšija javi vijest koja nije tvoja stvar. 📰🙄",
    "Ljeto = hvatanje klime ispod jorgana. 🛏️❄️",
    "Balkan parking: dvije linije? Staju četiri auta. 🚙😂",
    "Fritula je rješenje za sve životne probleme. 🍩🫶",
    "Kad dođe familija iznenada a kuća nije čista. 😱🧹",
    "Svako putovanje počinje sa 'imaš li pare za autoput?'. 🛣️💶",
    "Baka na kafi: zna sve o svima u gradu. 👵☕📰",
    "Balkanska statistika: 9 od 10 problema se rješava uz kafu. ☕📊",
    "'Otišao sam samo po hleb' — vratio se sa pola marketa. 🛒😅",
    "Kad igraš fudbal na ulici i lopta ode kod ljutog komšije. ⚽😰",
    "Svaki razgovor na Balkanu počne sa: 'Brate, slušaj ovo...' 🗣️👂",
    "Dnevna soba samo za goste. Gosti nikad ne dolaze. 🛋️🔒",
    "Šalter na pošti: radi jedan, čekaju trideset. 🏢😑",
    "Kad se probudi baka u 5 ujutru i odmah počne pjevati. 🌅🎵👵",
    "Balkanski sat: 'Dođi u 7' znači dođi u 8:30. 🕖😄",
    "Svaka kuća ima baku koja čuva bombone od 1998. 🍬👵",
    "Na Balkanu, ako ne jedeš treću porciju, nisi počašćen. 🍽️😅",
    "Kad završiš posao i nema struje za punjač. 🔌😩",
    "Balkanac na moru: čeka red u restoranu, naruči duplo, pojede četvoro. 🍴🌊",
    "Usred filma: 'Koliko još traje?' — Baš na napetom dijelu. 🎬😤",
    "Kad kaže 'jesi li gladan?' a hrana je već na stolu. 🍲🏃",
    "Svaka balkanska mama je doktor, kuhar i psiholog u jednom. 👩‍⚕️👩‍🍳🧠",
    "Kad ideš kod zubara a zub prestane boljeti čim sjedneš u čekaonicu. 🦷😤",
    "Balkan net: radi samo kad ne trebaš. 📶🙃",
    "Djeca na Balkanu idu van da se igraju — mama zna sve što su radila. 🏃👁️",
    "Kad vidiš kišu a majka te pita jesi li ponio kapu. 🌧️🧢",
    "Jedina stvar brža od vijesti na Balkanu — trač. 👄⚡",
    "Svaki rodjak želi znati kada se ženiš. Svake godine. 💍😭",
    "Na ljetovanju: sunce, more i debata gdje ćemo ručati 2 sata. 🌞🍽️",
    "Balkanac u inostranstvu: pronađe Balkanca u roku 10 minuta. 🌍🤝",
    "Kad čistiš sobu a mama kaže 'baciš li to, ubijam te'. 🗑️😅",
    "Fijaker sa konjima sporiji od balkanskog interneta. 🐴📶",
    "Svaka baka krije novac u džepu kecelje. 💸👵",
    "Domaći sok od šljive — lijek za sve. 🍑💊",
    "Balkan dijalog: 'Jesi jeo?' 'Jesam.' 'Jedi još.' 🍽️🔄",
    "Kad nema struje — svi izađu napolje i postanu filozofi. 🕯️🧠",
    "Majka ne razumije 'meni ništa ne treba za rodjendan'. 🎁👩‍👦",
    "Na Balkanu kafu piješ u svakoj kući čak i ako si 'samo svrnuo'. ☕🏠",
    "Djeca na Balkanu nemaju 'slobodnog vremena' — ima posla uvijek. 🧹⏰",
    "Balkan parking 2: dvostruki parking je tradicija, ne greška. 🚗🚗",
    "Svako selo ima svog vračara i svi tvrde da ne vjeruju. 🔮😏",
    "Kad mama pita 'gdje si bio?' a ti bio u WC-u. 🚽😤",
    "Balkan zimovanje: pečenje kestena i debata o politici. 🌰🗳️",
    "Sendvič koji je spakovao ko znaš uvijek je bolji. 🥪❤️",
    "Svaki kafić ima isti TV kanal i uvijek su vijesti. 📺☕",
    "Balkanski wifi lozinka: nešto poput 'qwerty1234'. 📶😂",
    "Kad igraš tablić i gledaš protivnikove karte u odrazu prozora. 🃏👁️",
    "Balkan letovanje: čekaš godinu dana, provedeš 7 dana, žališ se pola godine. 🌊😤",
    "Svaka balkanska mama reciklira plastične flaše u vazi. 🌺♻️",
    "Kad rjeknete 'ajde' a niko se ne miče. 🚶🗿",
    "Balkan shopping: ideš po jedno, vratiš se sa svime osim tog jednog. 🛍️😅",
]

MEME_STATE: dict = {}  # guild_id -> shuffled list of remaining indices

def get_next_meme(guild_id: int) -> str:
    key = str(guild_id)
    if key not in MEME_STATE or not MEME_STATE[key]:
        idxs = list(range(len(MEMES)))
        random.shuffle(idxs)
        MEME_STATE[key] = idxs
    return MEMES[MEME_STATE[key].pop()]

# ═══════════════════════════════════════════
#    VJEŠALA — rječnik
# ═══════════════════════════════════════════
VJASALA_RJECNIK = [
    "RAKIJA","CEVAPI","BALKON","KAFANA","MARKET","TRAKTOR","KOMSIJA","BONTON",
    "FUDBAL","PAPRIKA","BUREK","KAJMAK","SARMA","KIFLA","PEKARA","BAKLAVA",
    "KOMPJUTER","INTERNET","MOBITEL","PUNJAC","SLUSALICE","TASTATURA","MIŠKA",
    "PLANINA","JEZERO","RIJEKA","SUMSKA","LIVADA","VRELO","KLISURA","BRDOVIT",
    "LIJENOST","MUDROST","HRABROST","ZIVAHNA","BRZINA","TOPLINA","VESELJE",
    "BAKA","DJED","STRIC","UJNA","BRAT","SESTRA","MAJKA","OTAC","DIJETE",
    "KREVET","STOLICA","ORMAR","ZAVJESA","TEPIH","OGLEDALO","PROZOR","VRATA",
    "KOKOSOVO","JAGODA","MALINA","BOROVNICA","SMOKVA","SLJIVA","TRESNJA",
    "AUTOMOBIL","MOTOCIKL","BICIKL","AVION","BROD","VAGON","TRAMVAJ","METRO",
    "GITARA","VIOLINA","BUBNJEVI","FLAUTA","KLAVIR","HARMONIKA","SAKSOFON",
    "POLICAJAC","VATROGASAC","LJEKAR","UCITELJ","NOVINAR","ARHITEKT","INZENJER",
    "SUNCOKREO","RUZA","LAVANDA","KAKTUS","TULIPAN","JORGOVANA","MASLACAK",
    "OBLAK","MUNJA","GROM","SNIJEG","ROSA","MAGLA","VJETAR","OLUJA","DUGA",
    "LEPTIR","PCELICA","BUBAMARA","VJEVERICA","JELEN","LISICA","MEDVJED","VUK",
    "TORTA","KOLAC","KROFNA","PALACINKA","WAFFLE","BROWNIE","TIRAMISU","MACARON",
    "KUHINJA","KUPATILO","HODNIK","PODRUM","TAVAN","GARAZ","BALKON","TERASA",
    "SLOBODA","JEDNAKOST","LJUBAV","NADA","VJERA","SREĆA","ISTINA","PRAVDA",
    "GIMNASTIKA","PLIVANJE","ATLETIKA","KOSARKA","ODBOJKA","TENIS","SAHI","BOKS",
    "JANUAR","FEBRUAR","OKTOBAR","NOVEMBAR","DECEMBAR","SUBOTA","NEDJELJA",
    "DUGACAK","KRATAK","VISOK","NIZAK","DEBEO","MRSAV","BRZO","POLAKO","GLASNO",
]

VJASALA_FAZE = [
    "```\n  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========```",
]

# ═══════════════════════════════════════════
#    INTENTS & BOT
# ═══════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True  # potrebno za /vanity (čitanje custom statusa)
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# ═══════════════════════════════════════════
#    PREFIX BRIDGE — .kpm radi kao /kpm
# ═══════════════════════════════════════════
class _FakeResponse:
    def __init__(self, fake): self.fake = fake; self._sent = False
    async def send_message(self, content=None, *, embed=None, embeds=None, view=None, ephemeral=False, **kw):
        kwargs = {}
        if content is not None: kwargs["content"] = content
        if embed is not None: kwargs["embed"] = embed
        if embeds is not None: kwargs["embeds"] = embeds
        if view is not None: kwargs["view"] = view
        cmd_name = (self.fake.message.content[1:].split(maxsplit=1)[0].lower() if self.fake.message.content.startswith(".") else "")
        if ephemeral and cmd_name == "help":
            try:
                msg = await self.fake.user.send(**kwargs)
                try: await self.fake.message.add_reaction("📬")
                except: pass
                self.fake._original = msg; self._sent = True
                return msg
            except: pass
        if ephemeral:
            kwargs["delete_after"] = 10
        msg = await self.fake.channel.send(**kwargs)
        self.fake._original = msg; self._sent = True
        return msg
    async def defer(self, ephemeral=False, thinking=False): self._sent = True
    async def edit_message(self, **kw):
        try: await self.fake._original.edit(**{k:v for k,v in kw.items() if v is not None})
        except: pass
    def is_done(self): return self._sent

class _FakeFollowup:
    def __init__(self, fake): self.fake = fake
    async def send(self, content=None, *, embed=None, embeds=None, view=None, ephemeral=False, **kw):
        kwargs = {}
        if content is not None: kwargs["content"] = content
        if embed is not None: kwargs["embed"] = embed
        if embeds is not None: kwargs["embeds"] = embeds
        if view is not None: kwargs["view"] = view
        cmd_name = (self.fake.message.content[1:].split(maxsplit=1)[0].lower() if self.fake.message.content.startswith(".") else "")
        if ephemeral and cmd_name == "help":
            try: return await self.fake.user.send(**kwargs)
            except: pass
        if ephemeral:
            kwargs["delete_after"] = 10
        return await self.fake.channel.send(**kwargs)

class FakeInteraction:
    def __init__(self, message):
        self.user = message.author
        self.channel = message.channel
        self.guild = message.guild
        self.message = message
        self.client = bot
        self.command = None
        self._original = None
        self._response = _FakeResponse(self)
        self._followup = _FakeFollowup(self)
    @property
    def response(self): return self._response
    @property
    def followup(self): return self._followup
    @property
    def channel_id(self): return self.channel.id
    @property
    def guild_id(self): return self.guild.id if self.guild else None
    async def original_response(self): return self._original

def _parse_member(text, guild):
    text = text.strip()
    if not text: return None
    m = re.match(r"<@!?(\d+)>", text)
    if m:
        return guild.get_member(int(m.group(1)))
    if text.isdigit():
        return guild.get_member(int(text))
    text_low = text.lower()
    for mem in guild.members:
        if mem.name.lower() == text_low or mem.display_name.lower() == text_low:
            return mem
    for mem in guild.members:
        if text_low in mem.name.lower() or text_low in mem.display_name.lower():
            return mem
    return None

def _parse_role(text, guild):
    text = text.strip()
    m = re.match(r"<@&(\d+)>", text)
    if m: return guild.get_role(int(m.group(1)))
    if text.isdigit(): return guild.get_role(int(text))
    for r in guild.roles:
        if r.name.lower() == text.lower(): return r
    return None

def _parse_channel(text, guild):
    text = text.strip()
    m = re.match(r"<#(\d+)>", text)
    if m: return guild.get_channel(int(m.group(1)))
    if text.isdigit(): return guild.get_channel(int(text))
    for c in guild.channels:
        if c.name.lower() == text.lower(): return c
    return None

# ═══════════════════════════════════════════
#    KANAL PRAVILA — gdje koja igra/komanda smije
# ═══════════════════════════════════════════
# Format: "ime_komande": "dio_imena_kanala_gdje_smije"
CHANNEL_RULES = {
    # Igre
    "kaladont": "kaladont", "kaladont-stop": "kaladont",
    "vjasala": "vješalo",  # ili "vjesalo"
    "kpm": "kamen-papir",
    "kviz": "kviz",
    "geografija": "geografija",
    "toplo-hladno": "geografija",
    "amogus": "among-us", "amogus-stop": "among-us",
    # Casino
    "blackjack": "casino", "slots": "casino", "rulet": "casino",
    "flip": "casino", "kocka": "casino", "kradi": "casino",
    "bingo": "casino",
    # Ekonomija
    "baki": "economics", "posao": "economics", "daily": "economics",
    "daj": "economics", "shop": "economics", "kupi": "economics",
    "bank": "economics", "lottery": "economics", "heist": "economics",
    "quests": "economics", "rank": "economics", "leaderboard": "economics",
    # Brojanje
    # (auto, brojanje ima svoj kanal kroz cnt_cfg)
    # Ljubavne
    "zagrljaj": "zagrljaji", "poljubac": "zagrljaji", "mazi": "zagrljaji",
    "srce": "zagrljaji", "high5": "zagrljaji", "tapsi": "zagrljaji",
    "cudan": "zagrljaji", "pocetkaj": "zagrljaji", "curse": "zagrljaji",
    # Fun
    "meme": "zabava", "8ball": "zabava",
}
# Ove komande RADE SVUDA (ne ograničavamo)
CMDS_ANYWHERE = {
    "ping", "help", "serverinfo", "userinfo", "avatar", "invite", "spotify",
    "qr", "remind", "birthday", "afk", "serverstats", "topchatters",
    "say", "poll", "suggest", "confess", "report", "pravila", "warn", "warnings",
    "clearwarnings", "ban", "kick", "timeout", "clear",
    # setup
    "setup", "setup-roles", "setup-welcome", "setup-leave", "setup-autorole",
    "setup-log", "setup-starboard", "setup-levelrole", "setup-birthday",
    "setup-panels", "ticket-setup", "brojanje-postavi", "brojanje-info",
    "brojanje-reset", "setname", "setavatar", "setchannel", "sort-roles",
    "server-config", "vanity",
}

# Kanali u kojima SVE komande rade (slobodne zone)
FREE_CHANNELS = ["comanda", "komanda", "komande", "giveaways", "events", "bot-spam", "bot-commands"]

def check_channel_rule(channel, cmd_name: str):
    """Vrati None ako smije, ili ime potrebnog kanala ako ne smije."""
    ch_name = (channel.name or "").lower()
    # Slobodne zone — sve smije
    if any(fc in ch_name for fc in FREE_CHANNELS): return None
    if cmd_name in CMDS_ANYWHERE: return None
    needed = CHANNEL_RULES.get(cmd_name)
    if not needed: return None  # nije ograničena
    if needed.lower() in ch_name: return None  # OK
    return needed

def _extract_string_options(options: list) -> list[str]:
    """Rekurzivno izvuci sve string vrijednosti iz slash komande opcija."""
    result = []
    for opt in options or []:
        if not isinstance(opt, dict): continue
        if opt.get("type") == 3:  # type 3 = STRING u Discord API
            result.append(str(opt.get("value", "")))
        result.extend(_extract_string_options(opt.get("options", [])))
    return result

async def _global_channel_check(interaction: discord.Interaction) -> bool:
    if not interaction.guild or not interaction.command: return True
    # admini i vlasnik smiju svuda
    try:
        if interaction.user.guild_permissions.administrator: return True
    except: return True

    # ── Anti-Invite u slash komandama ─────────────────────
    # Provjeri sve string parametre koje korisnik upiše u komandu
    try:
        opts = _extract_string_options((interaction.data or {}).get("options", []))
        for val in opts:
            if INVITE_REGEX.search(val):
                await interaction.response.send_message(
                    embed=em("🚫 Reklama zabranjena",
                             f"{interaction.user.mention} — invite linkovi nisu dozvoljeni ni u komandama!",
                             color=COLORS["error"]),
                    ephemeral=True
                )
                return False
    except: pass

    needed = check_channel_rule(interaction.channel, interaction.command.name)
    if needed is None: return True
    target = discord.utils.find(lambda c: needed.lower() in c.name.lower(), interaction.guild.text_channels)
    msg = f"❌ **Ova komanda nije za ovaj kanal!**\n➡️ Koristi je u {target.mention if target else f'#{needed}'}"
    try:
        await interaction.response.send_message(embed=em("🚫 Pogrešan kanal", msg, color=COLORS["warning"]), ephemeral=True)
    except: pass
    return False

bot.tree.interaction_check = _global_channel_check

async def try_prefix_command(message):
    """Returns True if a .command was found and executed."""
    content = message.content.strip()
    if not content.startswith("."): return False
    if len(content) < 2 or content[1] in (" ", ".", "/"): return False
    parts = content[1:].split(maxsplit=1)
    cmd_name = parts[0].lower()
    args_text = parts[1] if len(parts) > 1 else ""
    PREFIX_ALIASES = {"i": "invite", "inv": "invite", "h": "help", "p": "ping", "lb": "leaderboard", "np": "spotify", "sp": "spotify", "stats": "serverstats", "ss": "serverstats", "tc": "topchatters", "top": "topchatters", "b": "bank", "lot": "lottery", "r": "remind", "qrcode": "qr"}
    cmd_name = PREFIX_ALIASES.get(cmd_name, cmd_name)
    cmd = bot.tree.get_command(cmd_name)
    if cmd is None: return False
    # Kanal pravila
    if not message.author.guild_permissions.administrator:
        needed = check_channel_rule(message.channel, cmd_name)
        if needed:
            target = discord.utils.find(lambda c: needed.lower() in c.name.lower(), message.guild.text_channels)
            await message.channel.send(
                embed=em("🚫 Pogrešan kanal", f"❌ {message.author.mention} — **ova komanda nije za ovaj kanal!**\n➡️ Idi u {target.mention if target else f'#{needed}'}", color=COLORS["warning"]),
                delete_after=10
            )
            try: await message.delete()
            except: pass
            return True
    fake = FakeInteraction(message)
    kwargs = {}
    try:
        params = list(cmd.parameters) if hasattr(cmd, "parameters") else []
        remaining = args_text
        for idx, p in enumerate(params):
            ptype = getattr(p.type, "name", str(p.type)).lower()
            is_last = (idx == len(params) - 1)
            if not remaining and not p.required:
                continue
            if not remaining and p.required:
                await message.channel.send(embed=em("❌", f"Fali argument: `{p.name}`. Probaj sa `/` umjesto `.` za pomoć.", color=COLORS["error"]), delete_after=8)
                return True
            if "user" in ptype or "member" in ptype:
                token, _, rest = remaining.partition(" ")
                mem = _parse_member(token, message.guild)
                if mem is None:
                    await message.channel.send(embed=em("❌", f"Korisnik nije pronađen: `{token}`", color=COLORS["error"]), delete_after=6)
                    return True
                kwargs[p.name] = mem
                remaining = rest.strip()
            elif "role" in ptype:
                token, _, rest = remaining.partition(" ")
                r = _parse_role(token, message.guild)
                if r is None:
                    await message.channel.send(embed=em("❌", f"Uloga nije pronađena: `{token}`", color=COLORS["error"]), delete_after=6)
                    return True
                kwargs[p.name] = r
                remaining = rest.strip()
            elif "channel" in ptype:
                token, _, rest = remaining.partition(" ")
                ch = _parse_channel(token, message.guild)
                if ch is None:
                    await message.channel.send(embed=em("❌", f"Kanal nije pronađen: `{token}`", color=COLORS["error"]), delete_after=6)
                    return True
                kwargs[p.name] = ch
                remaining = rest.strip()
            elif "integer" in ptype or "int" in ptype:
                token, _, rest = remaining.partition(" ")
                try: kwargs[p.name] = int(token)
                except ValueError:
                    await message.channel.send(embed=em("❌", f"`{p.name}` mora biti broj. Dao si: `{token}`", color=COLORS["error"]), delete_after=6)
                    return True
                remaining = rest.strip()
            elif "number" in ptype or "float" in ptype:
                token, _, rest = remaining.partition(" ")
                try: kwargs[p.name] = float(token)
                except ValueError:
                    await message.channel.send(embed=em("❌", f"`{p.name}` mora biti broj.", color=COLORS["error"]), delete_after=6)
                    return True
                remaining = rest.strip()
            elif "boolean" in ptype or "bool" in ptype:
                token, _, rest = remaining.partition(" ")
                kwargs[p.name] = token.lower() in ("da","yes","true","1","on")
                remaining = rest.strip()
            else:  # string
                if is_last:
                    kwargs[p.name] = remaining
                    remaining = ""
                else:
                    token, _, rest = remaining.partition(" ")
                    kwargs[p.name] = token
                    remaining = rest.strip()
        await cmd.callback(fake, **kwargs)
    except app_commands.CommandOnCooldown as e:
        await message.channel.send(embed=em("⏱️ Cooldown", f"Probaj ponovo za `{int(e.retry_after)}s`", color=COLORS["warning"]), delete_after=6)
    except Exception as e:
        await message.channel.send(embed=em("❌ Greška", f"`{type(e).__name__}`: {str(e)[:200]}\n\n💡 Probaj sa `/{cmd_name}` umjesto `.{cmd_name}`", color=COLORS["error"]), delete_after=10)
        print(f"[prefix bridge] {cmd_name}: {e}")
    return True

# ═══════════════════════════════════════════
#    PODACI
# ═══════════════════════════════════════════
import os as _os
_DATA_DIR = "/app/data" if _os.path.isdir("/app/data") else "."
try: _os.makedirs(_DATA_DIR, exist_ok=True)
except: _DATA_DIR = "."
DATA_FILE = _os.path.join(_DATA_DIR, "oleun_data.json")
if not _os.path.exists(DATA_FILE) and _os.path.exists("oleun_data.json"):
    try:
        import shutil as _sh
        _sh.copy("oleun_data.json", DATA_FILE)
        print(f"[migracija] Kopiran oleun_data.json → {DATA_FILE}")
    except Exception as _e: print(f"[migracija] {_e}")
print(f"[storage] DATA_FILE = {DATA_FILE}")
data = {"economy": {}, "xp": {}, "warnings": {}, "zoo": {}, "quests": {}, "selfroles": {},
        "guild_config": {}, "afk": {}, "birthdays": {}, "starboard_done": {}, "counting": {},
        "msg_count": {}, "invites": {}, "invite_uses": {},
        "money": {}, "bank": {}, "lottery": {"pot": 0, "tickets": {}, "last_draw": 0},
        "heist_cooldown": {}, "reminders": [], "confess_count": 0,
        "cmd_uses": {}, "private_voices": {}, "pvc_info_posted": False,
        "msg_count_week": {}, "aotw_last": None}

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            data["economy"]        = loaded.get("economy", {})
            data["xp"]             = loaded.get("xp", {})
            data["warnings"]       = loaded.get("warnings", {})
            data["zoo"]            = loaded.get("zoo", {})
            data["quests"]         = loaded.get("quests", {})
            data["selfroles"]      = loaded.get("selfroles", {})
            data["guild_config"]   = loaded.get("guild_config", {})
            data["afk"]            = loaded.get("afk", {})
            data["birthdays"]      = loaded.get("birthdays", {})
            data["starboard_done"] = loaded.get("starboard_done", {})
            data["msg_count"]      = loaded.get("msg_count", {})
            data["invites"]        = loaded.get("invites", {})
            data["invite_uses"]    = loaded.get("invite_uses", {})
            data["money"]          = loaded.get("money", {})
            data["bank"]           = loaded.get("bank", {})
            data["lottery"]        = loaded.get("lottery", {"pot": 0, "tickets": {}, "last_draw": 0})
            data["heist_cooldown"] = loaded.get("heist_cooldown", {})
            data["reminders"]      = loaded.get("reminders", [])
            data["confess_count"]  = loaded.get("confess_count", 0)
            data["cmd_uses"]       = loaded.get("cmd_uses", {})
            data["private_voices"] = loaded.get("private_voices", {})
            data["pvc_info_posted"]= loaded.get("pvc_info_posted", False)
            data["msg_count_week"] = loaded.get("msg_count_week", {})
            data["aotw_last"]      = loaded.get("aotw_last", None)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_guild_config(guild_id) -> dict:
    key = str(guild_id)
    if key not in data["guild_config"]:
        data["guild_config"][key] = {}
    return data["guild_config"][key]

load_data()

def get_economy(uid):
    key = str(uid)
    if key not in data["economy"]:
        data["economy"][key] = {"balance": 500, "last_work": 0, "last_daily": 0}
    d = data["economy"][key]
    d.setdefault("last_daily", 0)
    return d

def get_xp(uid):
    key = str(uid)
    if key not in data["xp"]:
        data["xp"][key] = {"xp": 0, "level": 1}
    return data["xp"][key]

def add_xp(uid, amount):
    d = get_xp(uid)
    d["xp"] += amount
    needed = d["level"] * 75
    if d["xp"] >= needed:
        d["xp"] -= needed
        d["level"] += 1
        return True
    return False

def get_zoo(uid):
    key = str(uid)
    if key not in data["zoo"]:
        data["zoo"][key] = {}
    return data["zoo"][key]

def get_warnings(guild_id, uid):
    gk, uk = str(guild_id), str(uid)
    data["warnings"].setdefault(gk, {})
    data["warnings"][gk].setdefault(uk, [])
    return data["warnings"][gk][uk]

# ═══════════════════════════════════════════
#    EMBED HELPER
# ═══════════════════════════════════════════
def em(title, desc="", color=COLORS["balkan"], fields=None, footer=None, thumb=None, image=None):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now(timezone.utc))
    if fields:
        for n, v, inline in fields:
            e.add_field(name=n, value=v or "\u200b", inline=inline)
    e.set_footer(text=footer or f"{BOT_NAME} {VERSION}")
    if thumb:  e.set_thumbnail(url=thumb)
    if image:  e.set_image(url=image)
    return e

# Premium embed za važne ekrane (profil, daily, level-up, pobjede, shop)
def em_pro(title, desc="", color=COLORS["gold"], fields=None, footer=None, thumb=None, image=None, author=None, accent=True):
    sep = "˚｡⋆୨୧˚ ───────────── ˚୨୧⋆｡˚"
    if accent and desc:
        desc = f"{sep}\n{desc}\n{sep}"
    elif accent:
        desc = sep
    e = discord.Embed(title=f"✦ {title} ✦", description=desc, color=color, timestamp=datetime.now(timezone.utc))
    if fields:
        for n, v, inline in fields:
            e.add_field(name=f"⟢ {n}", value=v or "\u200b", inline=inline)
    if author:
        e.set_author(name=author.display_name, icon_url=author.display_avatar.url)
    e.set_footer(text=footer or f"⚡ {BOT_NAME} {VERSION}")
    if thumb:  e.set_thumbnail(url=thumb)
    if image:  e.set_image(url=image)
    return e

# ═══════════════════════════════════════════
#    GIF HELPER (nekos.best)
# ═══════════════════════════════════════════
async def get_gif(action: str) -> str | None:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://nekos.best/api/v2/{action}", timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status == 200:
                    j = await r.json()
                    return j["results"][0]["url"]
    except:
        pass
    return None

# ═══════════════════════════════════════════
#    EVENTI
# ═══════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"\n{'═'*45}\n  {BOT_NAME} {VERSION} — ONLINE\n{'═'*45}")
    # ── Persistent views (preživljavaju restart) ──
    try:
        bot.add_view(GiveawayView())
        bot.add_view(TicketOpenView())
        bot.add_view(TicketCloseView())
        bot.add_view(PrivateVCPanel())
        print("  ✔ Persistent views aktivni (giveaway / ticket / privatni VC)")
    except Exception as e:
        print(f"  ✘ Persistent views: {e}")
    # ── Smart sync: samo ako je broj komandi promijenjen ──
    cur_cmds = len(bot.tree.get_commands())
    last_cmds = data.get("_last_synced_count", -1)
    if cur_cmds != last_cmds:
        try:
            synced = await bot.tree.sync()
            data["_last_synced_count"] = len(synced)
            save_data()
            print(f"  ✔ Globalni sync: {len(synced)} komandi (promijenjeno)")
        except Exception as e:
            print(f"  ✘ Globalni sync error: {e}")
        for guild in bot.guilds:
            try:
                bot.tree.copy_global_to(guild=guild)
                await bot.tree.sync(guild=guild)
                print(f"  ✔ {guild.name} ({guild.member_count} članova)")
            except Exception as e:
                print(f"  ✘ {guild.name}: {e}")
    else:
        print(f"  ⚡ Sync preskočen — komande nepromijenjene ({cur_cmds})")
    print(f"{'═'*45}\n")
    # Cache invites
    for guild in bot.guilds:
        try:
            invs = await guild.invites()
            data["invite_uses"][str(guild.id)] = {inv.code: inv.uses for inv in invs}
        except Exception as _e: print(f"[invite cache] {guild.name}: {_e}")
    save_data()
    if not change_status.is_running(): change_status.start()
    if not birthday_check.is_running(): birthday_check.start()
    if not auto_backup.is_running(): auto_backup.start()
    if not vanity_loop.is_running(): vanity_loop.start()
    if not auto_game_loop.is_running(): auto_game_loop.start()
    if not active_member_week.is_running(): active_member_week.start()
    try: await post_pvc_info()
    except Exception as _e: print(f"[pvc-info init] {_e}")
    print(f"  🛡️ Sigurnost: Anti-Nuke ✓ • Anti-Invite ✓ • Auto-Backup ✓ • Owner whitelist: {len(OWNER_IDS)}")
    for key, panel in data.get("selfroles", {}).items():
        if not panel.get("message_id"):
            continue
        try:
            view = _build_selfrole_view(key)
            bot.add_view(view, message_id=panel["message_id"])
        except Exception as e:
            print(f"  ✘ selfroles restore [{key}]: {e}")

@bot.event
async def on_guild_join(guild):
    print(f"  ➕ Pridružen server: {guild.name} ({guild.member_count} članova)")
    try:
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f"  ✔ Komande sync-ane za {guild.name}")
    except Exception as e:
        print(f"  ✘ Sync error za {guild.name}: {e}")
    chan = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
    if chan:
        try:
            e = discord.Embed(
                title=f"👋 Zdravo, {guild.name}!",
                description=(
                    f"Ja sam **{BOT_NAME}** — Balkan Discord bot!\n\n"
                    f"📖 Ukucaj `/help` da vidiš sve komande.\n"
                    f"🎮 Igraj igre, skupljaj životinje, zarađuj pare!\n\n"
                    f"*Verzija: {VERSION}*"
                ),
                color=COLORS["balkan"],
                timestamp=datetime.now(timezone.utc)
            )
            e.set_thumbnail(url=bot.user.display_avatar.url)
            e.set_footer(text=f"{BOT_NAME} {VERSION}")
            await chan.send(embed=e)
        except Exception:
            pass

@bot.event
async def on_member_join(member):
    cfg = get_guild_config(member.guild.id)

    # ── Anti-Raid (PAMETNI: ne lockuje, samo kickuje sumnjive) ──
    try:
        if await antiraid_check(member):
            return  # Kickovan, ne radi welcome
    except Exception as _e: print(f"[anti-raid] {_e}")

    # ── Invite Tracking ────────────────────────────────
    try:
        gkey = str(member.guild.id)
        old = data["invite_uses"].get(gkey, {})
        new_invites = await member.guild.invites()
        new_uses = {inv.code: inv.uses for inv in new_invites}
        used_code = None
        for code, uses in new_uses.items():
            if uses > old.get(code, 0):
                used_code = code
                break
        if used_code:
            inviter = next((inv.inviter for inv in new_invites if inv.code == used_code), None)
            if inviter and not inviter.bot:
                ikey = f"{member.guild.id}:{inviter.id}"
                rec = data["invites"].setdefault(ikey, {"count": 0, "code": used_code})
                rec["count"] += 1
                rec["code"] = used_code
        data["invite_uses"][gkey] = new_uses
        save_data()
    except Exception as _e: print(f"[invite-track join] {_e}")

    # ── Sumnjivi nalozi (mlađi od 7 dana) — upozorenje u log ──
    try:
        if is_suspicious_account(member):
            age_days = (datetime.now(timezone.utc) - member.created_at).days
            await audit_log(member.guild, "⚠️ Sumnjiv nalog se pridružio",
                f"{member.mention} (`{member}`) — nalog je star samo **{age_days} dan/a**.\n"
                f"Mogući fake/spam nalog. Provjeriti aktivnost.",
                color=COLORS.get("warning", 0xFFA500))
    except Exception as _e: print(f"[suspicious] {_e}")

    # ── Server Milestones (50, 100, 200, 500, 1000…) ──
    try:
        cnt = sum(1 for m in member.guild.members if not m.bot)
        milestones = [25, 50, 100, 150, 200, 300, 500, 750, 1000, 1500, 2000, 5000]
        if cnt in milestones:
            ms_ch = member.guild.get_channel(cfg.get("welcome_channel") or 1494687347558715543) or member.guild.system_channel
            if ms_ch:
                ms_e = discord.Embed(
                    title=f"🎊 MILESTONE — {cnt} ČLANOVA! 🎊",
                    description=(
                        f"━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🏆 Upravo smo dostigli **{cnt}** članova!\n"
                        f"💜 Hvala svima koji su dio **× GIANNI** porodice!\n"
                        f"🚀 Nastavljamo dalje — sljedeća stanica još veća!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━"
                    ),
                    color=0xFFD700, timestamp=datetime.now(timezone.utc)
                )
                ms_e.set_image(url="https://media.tenor.com/M0vSf9CGHoEAAAAC/celebration.gif")
                ms_e.set_footer(text=f"{BOT_NAME} • Server raste! 📈")
                await ms_ch.send(content="@everyone", embed=ms_e,
                    allowed_mentions=discord.AllowedMentions(everyone=True))
    except Exception as _e: print(f"[milestone] {_e}")

    # ── Auto-Role ──────────────────────────────────────
    if auto_role_id := cfg.get("auto_role"):
        role = member.guild.get_role(auto_role_id)
        if role:
            try: await member.add_roles(role)
            except: pass

    # ── Log ────────────────────────────────────────────
    if log_ch := member.guild.get_channel(cfg.get("log_channel", 0)):
        le = discord.Embed(title="📥 Novi Član", color=COLORS["success"], timestamp=datetime.now(timezone.utc))
        le.set_author(name=str(member), icon_url=member.display_avatar.url)
        le.add_field(name="ID", value=f"`{member.id}`", inline=True)
        le.add_field(name="Nalog kreiran", value=member.created_at.strftime("%d.%m.%Y."), inline=True)
        le.add_field(name="Ukupno članova", value=f"`{member.guild.member_count}`", inline=True)
        await log_ch.send(embed=le)

    # ── DM Dobrodošlice ──────────────────────────────
    try:
        dm_e = discord.Embed(
            title=f"🎉 Dobrodošao/la na {member.guild.name}!",
            description=(
                f"Hej **{member.display_name}**! Drago nam je što si tu! 🥳\n\n"
                f"📋 Pročitaj **#pravila** i upiši se u **#informacije**\n"
                f"🎮 Pridruži se **#glavni-chat** i upoznaj ekipu\n"
                f"❓ Trebaš pomoć? Otvori **ticket** ili pitaj bilo kog moderatora\n\n"
                f"💡 *Pišeš `.help` za sve dostupne komande bota!*\n"
                f"🇷🇸 Uživaj na **{member.guild.name}** — najboljem Balkan serveru! 🍻"
            ),
            color=COLORS["error"], timestamp=datetime.now(timezone.utc)
        )
        if member.guild.icon: dm_e.set_thumbnail(url=member.guild.icon.url)
        dm_e.set_footer(text=f"{BOT_NAME} • Welcome Bot")
        await member.send(embed=dm_e)
    except: pass  # Korisnik ima zatvorene DM

    # ── Welcome ────────────────────────────────────────
    ch_id = cfg.get("welcome_channel")
    chan = member.guild.get_channel(ch_id) if ch_id else discord.utils.get(member.guild.text_channels, name="welcome")
    if not chan: return

    WELCOME_PORUKE = [
        f"Hej {member.mention}! Drago nam je što si stigao/la! Upoznaj se, ispoštuj pravila i uživaj! 🍻",
        f"Evo ga/je {member.mention}! Server tek sad može početi! 🎉",
        f"Pazi ekipa, {member.mention} je stigao/la! Dobrodošao/la u porodicu! 🏠❤️",
        f"{member.mention} se pojavio/la! Bio/la si tu negdje, a? Dobrodošao/la! 👀",
        f"Naš/a novi/a prijatelj/ica {member.mention} je stigao/la! Sretno i uživaj! 🌟",
        f"{member.mention} je ušao/la u chat! Čaj ili kafa? ☕",
        f"Legenda stiže! Dobrodošao/la {member.mention}, nadam se da si spreman/a na zabavu! 🎮",
        f"Pssst... {member.mention} je upravo stigao/la. Recite tiho — iznenadite ih! 🤫🎊",
        f"Alarm! Alarm! {member.mention} je upravo sletio/la na server! Dobrodošao/la! 🚨🎊",
        f"Oh, ko je ovo? {member.mention}! Baš si nam nedostajao/la, a ni ne znamo te još! 😂❤️",
        f"Ekipa, pažnja! {member.mention} je odlučio/la da nam se pridruži. Mudra odluka! 😎✨",
        f"Novi/a član/ica detected! {member.mention} je ušao/la u zgradu. Dobrodošao/la! 🏢🎉",
        f"{member.mention} je stigao/la! Sjedni, opusti se, ti si sada dio GIANNI familije! 👑",
        f"Čekali smo te, {member.mention}! Dobrodošao/la, nadam se da ćeš ostati zauvijek! 🥰",
        f"Server +1! {member.mention} se pridružio/la! Dobrodošao/la među naše! 💪🎉",
        f"Jel to {member.mention}?! Ma daj, dobrodošao/la! Počasti nas prisustvom! 🍾✨",
        f"{member.mention} je kucao/la na vrata — otvorili smo! Dobrodošao/la u GIANNI! 🚪🎊",
        f"Evo novog/e! {member.mention} — nadam se da voliš zabavu jer smo ovdje puni toga! 🎮🔥",
        f"Hej hej hej! {member.mention} je ovdje! Server upravo dobio upgrade! ⬆️😄",
        f"Dobrodošao/la {member.mention}! Zapni se, bit će zabavno! 🎢❤️",
    ]

    WELCOME_SALE = [
        "😄 Zašto programeri vole prirodu? Jer nema bugova! 🐛",
        "😂 Šta kaže nula osmici? 'Lijepo ti stoji kaiš!' 😂",
        "🤣 Zašto je kompjuter uvijek hladan? Jer ima puno Windows! 🪟",
        "😄 Kako se zove Eskimo koji sjedi na stolici? Polarna sjednica! 🧊",
        "😂 Zašto ribe ne igraju tenis? Jer se boje mreže! 🎾🐟",
        "🤣 Šta kaže jedan zid drugom? 'Vidimo se na uglu!' 🧱",
        "😄 Zašto matematičari nikad ne idu na plažu? Jer imaju previše problema s brojevima! 🏖️",
        "😂 Kako se zove snjegović koji leži na suncu? Lokva! ☀️💧",
        "🤣 Zašto banane nose sunčane naočale? Jer se ne žele oguliti od sunca! 🍌😎",
        "😄 Šta kaže jedan lift drugom? 'Mene diže ovo što tebe spušta!' 🛗",
        "😂 Kako se zove majmun bez banane? Majmun! Banana nije sastavni dio naziva! 🐒",
        "🤣 Zašto je škola poput zatvora? Uniforme, mreže na prozorima i niko ne želi ići! 🏫",
        "😄 Šta kaže tava tiganju? 'Hej, daj mi prostora, sav si se raspalio!' 🍳",
        "😂 Zašto slon ne može koristiti kompjuter? Jer se boji miša! 🐘🖱️",
        "🤣 Koliko treba da se promijeni sijalica? Niti jedna — ona se mijenja sama kad je sprema! 💡",
        "😄 Šta kaže more plaži? Ništa, samo maše! 🌊👋",
        "😂 Zašto krava nosi zvonce? Jer joj rogovi ne rade! 🐄🔔",
        "🤣 Kako se zove pas koji voli magiju? Labra-kadabra-dor! 🐕✨",
        "😄 Zašto je knjiga uvijek tužna? Jer ima previše stranica iza sebe! 📚😢",
        "😂 Šta kaže jedna vrata drugima? 'Ključ je da se ne zaključaš u sebi!' 🚪🔑",
    ]

    sala = random.choice(WELCOME_SALE)
    custom_msg = cfg.get("welcome_message",
        random.choice(WELCOME_PORUKE))

    # Direktni ID-evi GIANNI kanala
    GIANNI_CHANNELS = {
        "informacije": 1494359372531372094,
        "pravila":     1494043956965544092,
        "selfroles":   1494058515319230614,
        "chat":        1494687347558715543,
        "public":      1494043958131556448,
    }
    def ch_link(key):
        c = member.guild.get_channel(GIANNI_CHANNELS[key])
        return c.mention if c else "#—"

    desc = (
        f"   🏠  **GIANNI COMMUNITY**\n\n"
        f"{custom_msg.replace('{user}', member.mention).replace('{server}', member.guild.name)}\n\n"
        f"ℹ️  **INFORMACIJE**   →  {ch_link('informacije')}\n"
        f"📋  **PRAVILA**       →  {ch_link('pravila')}\n"
        f"🔰  **SELF-ROLES**    →  {ch_link('selfroles')}\n"
        f"💬  **GLAVNI CHAT**   →  {ch_link('chat')}\n"
        f"🗨️  **PUBLIC**        →  {ch_link('public')}"
    )

    e = discord.Embed(
        title=f"🎉 Dobrodošao/la, {member.display_name}!",
        description=desc,
        color=COLORS["success"], timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="😄 Šala dobrodošlice", value=sala, inline=False)
    e.add_field(name="👥 Član broj", value=f"`#{member.guild.member_count}`", inline=True)
    e.add_field(name="⏰ Pridružio/la se", value=f"<t:{int(datetime.now(timezone.utc).timestamp())}:R>", inline=True)
    e.set_thumbnail(url=member.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Dobrodošlica")
    await chan.send(content=member.mention, embed=e)

@bot.event
async def on_member_remove(member):
    cfg = get_guild_config(member.guild.id)

    # ── Log ────────────────────────────────────────────
    if log_ch := member.guild.get_channel(cfg.get("log_channel", 0)):
        le = discord.Embed(title="📤 Član Otišao", color=COLORS["warning"], timestamp=datetime.now(timezone.utc))
        le.set_author(name=str(member), icon_url=member.display_avatar.url)
        le.add_field(name="ID", value=f"`{member.id}`", inline=True)
        le.add_field(name="Pridružio se", value=member.joined_at.strftime("%d.%m.%Y.") if member.joined_at else "?", inline=True)
        await log_ch.send(embed=le)

    # ── Leave message ──────────────────────────────────
    ch_id = cfg.get("leave_channel") or cfg.get("welcome_channel")
    chan = member.guild.get_channel(ch_id) if ch_id else discord.utils.get(member.guild.text_channels, name="welcome")
    if not chan: return
    e = discord.Embed(
        title=f"👋 {member.display_name} je napustio/la server",
        description=f"Žao nam je što ode **{member.display_name}**. Srećno! 🙏",
        color=COLORS["error"], timestamp=datetime.now(timezone.utc)
    )
    e.set_thumbnail(url=member.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Oproštaj")
    await chan.send(embed=e)

@bot.event
async def on_member_update(before, after):
    if before.premium_since is None and after.premium_since is not None:
        guild  = after.guild
        boosts = guild.premium_subscription_count or 0
        tier   = guild.premium_tier

        BOOST_REWARD = 2500
        get_economy(after.id)["balance"] += BOOST_REWARD
        save_data()

        tier_names = {0: "Nema tiera", 1: "Tier 1 🥈", 2: "Tier 2 🥇", 3: "Tier 3 💎"}

        chan = (
            guild.get_channel(1494043956965544094) or
            discord.utils.get(guild.text_channels, name="boosts") or
            discord.utils.get(guild.text_channels, name="general") or
            discord.utils.get(guild.text_channels, name="opšte") or
            discord.utils.get(guild.text_channels, name="chat") or
            next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
        )
        if not chan:
            return

        zahvale = [
            f"Ti si naša zvezda, {after.mention}! ✨",
            f"Legenda servera — {after.mention}! 🏆",
            f"Bog među nama — {after.mention}! 🙏",
            f"Bez tebe ne bismo bili ništa, {after.mention}! 💜",
            f"Kralj/Kraljica servera — {after.mention}! 👑",
            f"MVP bez premca — {after.mention}! 🎖️",
            f"Hvala ti beskrajno, {after.mention}! Srce si ove zajednice! ❤️",
        ]
        bsep = "══════════════════════════════"
        e = discord.Embed(
            title="🚀 ꜱᴇʀᴠᴇʀ ʙᴏᴏꜱᴛ! 💜",
            description=(
                f"```ansi\n\u001b[1;35m{bsep}\u001b[0m\n```"
                f"## 💜  {after.mention} je boostovao/la **{guild.name}**!\n\n"
                f"✨ {random.choice(zahvale)}\n\n"
                f"Hvala ti iz dna duše što podržavaš nas! "
                f"Tvoj boost čini ovaj server boljim mjestom za sve! 🌍💙\n"
                f"```ansi\n\u001b[1;35m{bsep}\u001b[0m\n```"
            ),
            color=0xF47FFF,
            timestamp=datetime.now(timezone.utc)
        )
        e.add_field(name="🚀 Ukupno Boosta",  value=f"```yaml\n{boosts} boost{'a' if boosts != 1 else ''}\n```", inline=True)
        e.add_field(name="🏅 Server Tier",    value=f"```yaml\n{tier_names.get(tier, '?')}\n```",                inline=True)
        e.add_field(name="💶 Nagrada",         value=f"```diff\n+ {BOOST_REWARD:,} coina dodato!\n```",           inline=False)
        e.add_field(name="🎁 Discord hvali:",  value="*Zahvaljujemo platformi Discord što nam omogućava ovu fantastičnu zajednicu!* 🙏", inline=False)
        e.set_thumbnail(url=after.display_avatar.url)
        e.set_image(url="https://i.imgur.com/wSTFkRM.gif")
        e.set_footer(text=f"💜 {BOT_NAME} {VERSION} • Hvala na podršci!")
        await chan.send(content=after.mention, embed=e)

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.guild: return

    # ── Prefix bridge (.kpm radi kao /kpm) ──
    if message.content.startswith("."):
        if await try_prefix_command(message):
            return

    # ── WLCM auto-reakcije (svako ko napiše "wlcm" dobije 🇼🇱🇨🇲) ──
    if message.content.lower().strip() in ("wlcm", "wlcm all"):
        for emj in ["🇼", "🇱", "🇨", "🇲"]:
            try: await message.add_reaction(emj)
            except: pass
        return

    # ── Brojanje handler (PRIJE auto-mod-a, da se uvijek reaguje) ──
    cnt_cfg = data.get("counting", {}).get(str(message.guild.id))
    if cnt_cfg and message.channel.id == cnt_cfg.get("channel_id"):
        content = message.content.strip()
        try:
            num = int(content)
        except ValueError:
            try: await message.delete()
            except: pass
            return
        expected = cnt_cfg.get("current", 0) + 1
        last_user = cnt_cfg.get("last_user")
        if last_user == message.author.id:
            try: await message.add_reaction("⛔")
            except Exception as e: print(f"[brojanje] reaction fail: {e}")
            warn_e = discord.Embed(
                title="⛔ OPOMENA — Ne možeš brojati iza sebe!",
                description=(
                    f"{message.author.mention}, **mora neko drugi nastaviti** prije nego što ti opet brojiš.\n\n"
                    f"➡️ Sljedeći broj je i dalje: **{expected}**"
                ),
                color=COLORS["warning"]
            )
            warn_e.set_footer(text=f"Pravilo: izmjenjivanje korisnika obavezno")
            await message.channel.send(content=message.author.mention, embed=warn_e, delete_after=8)
            try: await message.delete()
            except: pass
            return
        if num != expected:
            try: await message.add_reaction("❌")
            except Exception as e: print(f"[brojanje] reaction fail: {e}")
            try: await message.delete()
            except: pass
            # broji greške po korisniku (NE resetujemo brojanje!)
            mistakes = cnt_cfg.setdefault("mistakes", {})
            uid_str = str(message.author.id)
            mistakes[uid_str] = mistakes.get(uid_str, 0) + 1
            user_total = mistakes[uid_str]
            save_data()
            err_e = discord.Embed(
                title="💥 OPOMENA — Pogrešan broj!",
                description=(
                    f"{message.author.mention}, **pogriješio/la** si!\n\n"
                    f"❌ Tvoj odgovor: **{num}**\n"
                    f"✅ Trebalo je: **{expected}**\n\n"
                    f"⚠️ Tvojih grešaka ukupno: **{user_total}**\n"
                    f"➡️ Brojanje **se nastavlja** — sljedeći broj je i dalje: **{expected}**"
                ),
                color=COLORS["error"], timestamp=datetime.now(timezone.utc)
            )
            err_e.set_footer(text=f"Pazi sljedeći put, {message.author.display_name}!")
            await message.channel.send(content=message.author.mention, embed=err_e, delete_after=10)
            return
        # tačan broj
        cnt_cfg["current"] = num
        cnt_cfg["last_user"] = message.author.id
        if num > cnt_cfg.get("high_score", 0):
            cnt_cfg["high_score"] = num
        save_data()
        try:
            await message.add_reaction("✅")
        except Exception as e:
            print(f"[brojanje] reaction fail: {e}")
        # uokvireni label ispod broja
        try:
            label = discord.Embed(
                description=f"✅  **#{num}**  ·  sljedeći: **{num+1}**",
                color=COLORS["success"]
            )
            label.set_footer(text=f"Brojao/la: {message.author.display_name}")
            await message.reply(embed=label, mention_author=False, silent=True)
        except Exception as e:
            print(f"[brojanje] reply fail: {e}")
        if num % 50 == 0:
            eco = get_economy(message.author.id)
            eco["balance"] += 100
            add_xp(message.author.id, 50); save_data()
            await message.channel.send(
                embed=em(f"🎯 Milestone {num}!",
                         f"{message.author.mention} dostigao broj **{num}**!\n`+100 💶` `+50 XP`",
                         color=COLORS["gold"]),
                delete_after=10
            )
        return

    # ── Auto-Mod ──────────────────────────────────────
    if await check_nsfw(message):
        return
    if await check_automod(message):
        return

    # ── AFK: clear if author was AFK ──────────────────
    uid_str = str(message.author.id)
    if uid_str in data["afk"]:
        afk_info = data["afk"].pop(uid_str)
        save_data()
        since = datetime.fromtimestamp(afk_info["since"], tz=timezone.utc)
        elapsed = datetime.now(timezone.utc) - since
        mins = int(elapsed.total_seconds() // 60)
        await message.channel.send(
            embed=em("👋 Dobro došao/la nazad!", f"Skinut AFK status. Bio/la si odsutan/na **{mins} min**.", color=COLORS["info"]),
            delete_after=8
        )

    # ── AFK: notify if mentioning AFK user ────────────
    for mentioned in message.mentions:
        m_str = str(mentioned.id)
        if m_str in data["afk"]:
            afk_r = data["afk"][m_str]
            await message.channel.send(
                embed=em(f"😴 {mentioned.display_name} je AFK",
                         f"Razlog: *{afk_r.get('reason', 'nema razloga')}*",
                         color=COLORS["warning"]),
                delete_after=10
            )

    # ── Quest: msgs20 ─────────────────────────────────
    if not message.content.startswith("/") and not message.content.startswith("!"):
        completed = quest_progress(message.author.id, "msgs20")
        if completed:
            await message.channel.send(
                embed=em(f"✅ Quest završen! {completed['name']}", f"+**{completed['reward']} 💶**!", color=COLORS["gold"]),
                delete_after=8
            )

    # ── Kaladont handler ──────────────────────────────
    if message.channel.id in kaladont_games and not message.content.startswith("/"):
        game = kaladont_games[message.channel.id]
        word = message.content.upper().strip()
        letters = game["letters"]
        req = game["word"][-letters:]

        async def reject(reason: str):
            await message.channel.send(
                embed=em("❌ " + reason, f"Potrebno: počinje sa **`{req}`**", color=COLORS["error"]),
                delete_after=5
            )

        if not word.isalpha():
            pass  # ignore non-word messages silently
        elif len(word) < 3:
            await reject("Prekratka! Min 3 slova.")
        elif word[:letters] != req:
            await reject(f"Mora početi sa **`{req}`**! Tvoja: `{word}`")
        elif word in game["used"]:
            await reject(f"`{word}` je već bila!")
        else:
            game["word"] = word
            game["used"].add(word)
            game["chain"].append((word, message.author.display_name))
            count   = len(game["chain"])
            new_req = word[-letters:]
            try: await message.add_reaction("✅")
            except: pass
            # ── POBJEDA: ako je riječ "KALADONT" ──
            if word == "KALADONT":
                try: await message.add_reaction("👑")
                except: pass
                eco = get_economy(message.author.id)
                nagrada = 1500
                eco["balance"] = eco.get("balance", 0) + nagrada
                add_xp(message.author.id, 200)
                save_data()
                win_e = discord.Embed(
                    title="👑 KALADONT! POBJEDA! 👑",
                    description=(
                        f"━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🏆 **{message.author.mention}** je rekao/la magičnu riječ: **KALADONT**!\n\n"
                        f"📊 Riječi u nizu: **`{count}`**\n"
                        f"💰 Nagrada: **+{nagrada} 💶**\n"
                        f"⭐ XP: **+200**\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎉 Igra je završena!"
                    ),
                    color=COLORS.get("gold", 0xFFD700),
                    timestamp=datetime.now(timezone.utc)
                )
                win_e.set_footer(text=f"{BOT_NAME} {VERSION} • KALADONT pobjeda")
                await message.channel.send(content=message.author.mention, embed=win_e)
                del kaladont_games[message.channel.id]
                return
            await message.channel.send(embed=kaladont_word_card(word, message.author.display_name, new_req, count))
            if game["msg"]:
                try: await game["msg"].edit(embed=kaladont_active_embed(game))
                except: pass
        return  # don't process XP for kaladont channel messages

    # ── Msg Counter ───────────────────────────────────
    mkey = f"{message.guild.id}:{message.author.id}"
    data["msg_count"][mkey] = data["msg_count"].get(mkey, 0) + 1
    data.setdefault("msg_count_week", {})
    data["msg_count_week"][mkey] = data["msg_count_week"].get(mkey, 0) + 1

    # ── XP ────────────────────────────────────────────
    if random.random() < 0.55:
        if add_xp(message.author.id, random.randint(15, 40)):
            save_data()
            lvl = get_xp(message.author.id)["level"]
            cfg = get_guild_config(message.guild.id)
            lr = cfg.get("level_roles", {})
            new_role = None
            if str(lvl) in lr:
                lvl_role = message.guild.get_role(lr[str(lvl)])
                if lvl_role:
                    try:
                        await message.author.add_roles(lvl_role)
                        new_role = lvl_role
                    except: pass
            # Šalji u dedicated level-up kanal ako je postavljen, inače fallback
            lvl_ch_id = cfg.get("levelup_channel") or 1494043957242495107
            lvl_ch = message.guild.get_channel(lvl_ch_id) or message.channel
            sep = "━━━━━━━━━━━━━━━━━━━━━━"
            desc = (
                f"{sep}\n"
                f"🎉 Čestitamo {message.author.mention}!\n"
                f"Dostigao/la si **`★ LEVEL {lvl} ★`**\n"
                f"{sep}\n"
                f"💬 Nastavi pisati i osvajati još više XP-a!\n"
            )
            if new_role:
                desc += f"🏷️ **Otključana uloga:** {new_role.mention}\n"
            desc += f"\n📊 Provjeri statistiku sa `/rank`"
            lv_em = discord.Embed(
                title="🌟 ʟᴇᴠᴇʟ ᴜᴘ! 🌟",
                description=desc,
                color=0xFFD700,
                timestamp=datetime.now(timezone.utc)
            )
            lv_em.set_thumbnail(url=message.author.display_avatar.url)
            lv_em.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
            lv_em.set_footer(text=f"⚡ {BOT_NAME} • XP Sistem")
            try:
                if lvl_ch.id == message.channel.id:
                    await lvl_ch.send(content=message.author.mention, embed=lv_em, delete_after=15)
                else:
                    await lvl_ch.send(content=message.author.mention, embed=lv_em)
            except Exception as _e:
                print(f"[level-up] {_e}")
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@bot.event
async def on_message_edit(before, after):
    if before.author.bot or before.content == after.content: return
    if not before.guild: return
    cfg = get_guild_config(before.guild.id)
    log_ch = before.guild.get_channel(cfg.get("log_channel", 0))
    if not log_ch: return
    e = discord.Embed(title="✏️ Poruka Editovana", color=COLORS["warning"], timestamp=datetime.now(timezone.utc))
    e.set_author(name=str(before.author), icon_url=before.author.display_avatar.url)
    e.add_field(name="Kanal",   value=before.channel.mention,           inline=True)
    e.add_field(name="📍 Link", value=f"[Idi na poruku]({after.jump_url})", inline=True)
    e.add_field(name="Prije",   value=(before.content[:1000] or "*prazno*"), inline=False)
    e.add_field(name="Poslije", value=(after.content[:1000]  or "*prazno*"), inline=False)
    await log_ch.send(embed=e)

@bot.event
async def on_message_delete(message):
    if message.author.bot or not message.guild: return
    cfg = get_guild_config(message.guild.id)
    log_ch = message.guild.get_channel(cfg.get("log_channel", 0))
    if not log_ch: return
    e = discord.Embed(title="🗑️ Poruka Obrisana", color=COLORS["error"], timestamp=datetime.now(timezone.utc))
    e.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    e.add_field(name="Kanal",    value=message.channel.mention,                         inline=True)
    e.add_field(name="Sadržaj",  value=(message.content[:1000] or "*prilog/prazno*"),   inline=False)
    await log_ch.send(embed=e)

@bot.event
async def on_member_ban(guild, user):
    cfg = get_guild_config(guild.id)
    log_ch = guild.get_channel(cfg.get("log_channel", 0))
    if not log_ch: return
    e = discord.Embed(title="🔨 Član Banovan", color=COLORS["error"], timestamp=datetime.now(timezone.utc))
    e.set_author(name=str(user), icon_url=user.display_avatar.url)
    e.add_field(name="ID", value=f"`{user.id}`", inline=True)
    await log_ch.send(embed=e)

@bot.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) != "⭐" or not payload.guild_id: return
    cfg = get_guild_config(payload.guild_id)
    sb_ch_id = cfg.get("starboard_channel")
    if not sb_ch_id: return
    if payload.channel_id == sb_ch_id: return
    threshold = cfg.get("starboard_threshold", 3)
    guild   = bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    try:
        message = await channel.fetch_message(payload.message_id)
    except: return
    star_r = discord.utils.get(message.reactions, emoji="⭐")
    count  = star_r.count if star_r else 0
    if count < threshold: return
    sb_channel = guild.get_channel(sb_ch_id)
    if not sb_channel: return
    gkey   = str(payload.guild_id)
    mkey   = str(payload.message_id)
    done   = data["starboard_done"].setdefault(gkey, {})
    if mkey in done:
        try:
            sb_msg = await sb_channel.fetch_message(done[mkey])
            ne = sb_msg.embeds[0]
            ne.set_footer(text=f"⭐ {count} | #{channel.name}")
            await sb_msg.edit(embed=ne)
        except: pass
        return
    e = discord.Embed(description=message.content or "", color=COLORS["gold"], timestamp=message.created_at)
    e.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    e.add_field(name="📍 Original", value=f"[Idi na poruku]({message.jump_url})", inline=False)
    if message.attachments: e.set_image(url=message.attachments[0].url)
    e.set_footer(text=f"⭐ {count} | #{channel.name}")
    sb_msg = await sb_channel.send(f"⭐ **{count}** | {channel.mention}", embed=e)
    done[mkey] = sb_msg.id
    save_data()

@tasks.loop(hours=1)
async def birthday_check():
    today = datetime.now(timezone.utc).strftime("%d-%m")
    for uid, bday in list(data.get("birthdays", {}).items()):
        if bday != today: continue
        for guild in bot.guilds:
            member = guild.get_member(int(uid))
            if not member: continue
            cfg   = get_guild_config(guild.id)
            ch_id = cfg.get("birthday_channel")
            if not ch_id: continue
            chan = guild.get_channel(ch_id)
            if not chan: continue
            e = discord.Embed(
                title="🎂 Sretan Rođendan!",
                description=f"Danas je rođendan od {member.mention}! 🎉\nSvi mu/joj čestitajte! 🥳",
                color=COLORS["fun"], timestamp=datetime.now(timezone.utc)
            )
            e.set_thumbnail(url=member.display_avatar.url)
            e.set_footer(text=f"{BOT_NAME} • Rođendani")
            try: await chan.send(content=member.mention, embed=e)
            except: pass

@bot.command(name="sync")
@commands.has_permissions(administrator=True)
async def sync_cmd(ctx):
    try:
        bot.tree.copy_global_to(guild=ctx.guild)
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(embed=em("✅ Sinhronizovano!", f"`{len(synced)}` komandi registrovano.", color=COLORS["success"]))
    except Exception as e:
        await ctx.send(embed=em("❌ Greška", str(e), color=COLORS["error"]))

# ═══════════════════════════════════════════
#    🛡️ SIGURNOST: Anti-Nuke / Audit / Backup / Whitelist
# ═══════════════════════════════════════════
OWNER_IDS: set = {984906640509788180}  # Discord ID-evi koji su 100% sigurni (anti-nuke whitelist)
NUKE_WINDOW = 30        # sekundi
NUKE_BAN_LIMIT = 3      # max banova/kickova/brisanja u prozoru
nuke_tracker: dict = defaultdict(lambda: defaultdict(deque))

# ── PAMETNI Anti-Raid (NE LOCKUJE server, samo kickuje sumnjive) ───
RAID_WINDOW = 30            # sekundi (5+ joinova u 30s = raid lockdown 5 min)
RAID_JOIN_LIMIT = 5         # 5+ NOVIH naloga u 30s = raid
SUSPICIOUS_AGE_DAYS = 7     # nalozi mlađi od ovoliko dana = sumnjivi
join_tracker: dict = defaultdict(deque)   # guild_id -> deque[(timestamp, member_id, account_age_days)]
raid_mode: dict = {}        # guild_id -> until_timestamp (period gdje se sumnjivi auto-kickaju)

def is_suspicious_account(member) -> bool:
    """Nalog je sumnjiv ako je: < 7 dana star, default avatar, prazan profil"""
    age_days = (datetime.now(timezone.utc) - member.created_at).days
    if age_days < SUSPICIOUS_AGE_DAYS:
        return True
    return False

async def antiraid_check(member):
    """Prati joinove. Ako je raid, ulazi u raid mod gdje se sumnjivi nalozi automatski kickaju."""
    now = time.time()
    gid = member.guild.id
    age_days = (datetime.now(timezone.utc) - member.created_at).days
    dq = join_tracker[gid]
    dq.append((now, member.id, age_days))
    while dq and dq[0][0] < now - RAID_WINDOW:
        dq.popleft()
    # Brojanje SAMO novih naloga (sumnjivih) u prozoru
    suspicious_recent = sum(1 for _, _, ad in dq if ad < SUSPICIOUS_AGE_DAYS)
    if suspicious_recent >= RAID_JOIN_LIMIT:
        # ULAZAK U RAID MOD na 5 minuta
        raid_mode[gid] = now + 300
        await audit_log(member.guild, "🚨 RAID DETEKTOVAN!",
            f"**{suspicious_recent}** sumnjivih naloga (mlađih od {SUSPICIOUS_AGE_DAYS} dana) u zadnjih {RAID_WINDOW}s!\n"
            f"⚙️ **Raid mode AKTIVAN 5min** — sumnjivi nalozi će biti automatski kickovani.\n"
            f"✅ Stari/legitimni nalozi prolaze normalno.")
    # Ako smo u raid modu i nalog je sumnjiv → kickuj
    if gid in raid_mode and now < raid_mode[gid] and is_suspicious_account(member):
        try:
            await member.send(embed=em("🛡️ Raid Zaštita", f"Server **{member.guild.name}** je trenutno pod raid zaštitom. Tvoj nalog je premlad ({age_days}d). Pokušaj ponovo kasnije.", color=COLORS["warning"]))
        except: pass
        try:
            await member.kick(reason="🛡️ Anti-Raid: sumnjiv nalog tokom raida")
            await audit_log(member.guild, "🛡️ Anti-Raid Kick", f"Kickovan: `{member}` (`{member.id}`) — nalog star {age_days}d")
            return True
        except: pass
    return False

async def audit_log(guild, title, desc):
    """Šalje sigurnosni log u log_channel + DM-uje OWNER_IDS."""
    try:
        cfg = get_guild_config(guild.id)
        if log_ch := guild.get_channel(cfg.get("log_channel", 0)):
            await log_ch.send(embed=em(title, desc, color=COLORS["error"]))
    except: pass
    for oid in OWNER_IDS:
        try:
            owner = await bot.fetch_user(oid)
            await owner.send(embed=em(f"🔔 [{guild.name}] {title}", desc, color=COLORS["warning"]))
        except: pass

async def antinuke_check(guild, mod, action: str):
    """Vrati True ako moderator prelazi limit. Skida mu admin uloge i obavještava."""
    if mod.id in OWNER_IDS or mod.bot:
        return False
    now = time.time()
    dq = nuke_tracker[guild.id][mod.id]
    dq.append(now)
    while dq and dq[0] < now - NUKE_WINDOW:
        dq.popleft()
    if len(dq) >= NUKE_BAN_LIMIT:
        dq.clear()
        # Skini sve admin uloge
        try:
            removed = []
            for r in list(mod.roles):
                if r.permissions.administrator or r.permissions.ban_members or r.permissions.kick_members or r.permissions.manage_roles:
                    try:
                        await mod.remove_roles(r, reason="🛡️ Anti-Nuke: prelazak limita")
                        removed.append(r.name)
                    except: pass
            await audit_log(guild, "🚨 ANTI-NUKE AKTIVAN!",
                f"**Moderator:** {mod.mention} (`{mod}`)\n**Akcija:** {action}\n**Limit:** {NUKE_BAN_LIMIT} u {NUKE_WINDOW}s\n**Skinute uloge:** {', '.join(removed) if removed else 'nijedna'}")
        except Exception as _e: print(f"[anti-nuke] {_e}")
        return True
    return False

@bot.event
async def on_member_ban(guild, user):
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == user.id:
                await antinuke_check(guild, entry.user, f"BAN korisnika `{user}`")
                await audit_log(guild, "🔨 BAN", f"**Moderator:** {entry.user.mention}\n**Korisnik:** `{user}` (`{user.id}`)\n**Razlog:** {entry.reason or '—'}")
                break
    except Exception as _e: print(f"[on_member_ban] {_e}")

@bot.event
async def on_member_remove(member):
    try:
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id and (time.time() - entry.created_at.timestamp()) < 5:
                await antinuke_check(member.guild, entry.user, f"KICK korisnika `{member}`")
                await audit_log(member.guild, "👢 KICK", f"**Moderator:** {entry.user.mention}\n**Korisnik:** `{member}` (`{member.id}`)")
                break
    except Exception as _e: print(f"[on_member_remove] {_e}")

@bot.event
async def on_guild_channel_delete(channel):
    try:
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if entry.target.id == channel.id:
                await antinuke_check(channel.guild, entry.user, f"BRISANJE kanala #{channel.name}")
                await audit_log(channel.guild, "🗑️ KANAL OBRISAN", f"**Moderator:** {entry.user.mention}\n**Kanal:** `#{channel.name}`")
                break
    except Exception as _e: print(f"[on_channel_delete] {_e}")

@bot.event
async def on_guild_role_delete(role):
    try:
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            if entry.target.id == role.id:
                await antinuke_check(role.guild, entry.user, f"BRISANJE uloge {role.name}")
                await audit_log(role.guild, "🏷️ ULOGA OBRISANA", f"**Moderator:** {entry.user.mention}\n**Uloga:** `{role.name}`")
                break
    except Exception as _e: print(f"[on_role_delete] {_e}")

# ── Auto-backup svakih 6 sati ────────────────────────
@tasks.loop(hours=6)
async def auto_backup():
    try:
        import shutil as _sh
        backup_dir = _os.path.join(_DATA_DIR, "backups")
        _os.makedirs(backup_dir, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        dst = _os.path.join(backup_dir, f"oleun_data_{ts}.json")
        _sh.copy(DATA_FILE, dst)
        # Drži maksimum 20 backupa
        backups = sorted(_os.listdir(backup_dir))
        for old in backups[:-20]:
            try: _os.remove(_os.path.join(backup_dir, old))
            except: pass
        print(f"[backup] {dst}")
    except Exception as _e: print(f"[backup] {_e}")

@tasks.loop(seconds=30)
async def change_status():
    statuses = [
        discord.Activity(type=discord.ActivityType.playing,   name=f"/help | {BOT_NAME}"),
        discord.Activity(type=discord.ActivityType.watching,  name="Balkanske drame 🎭"),
        discord.Activity(type=discord.ActivityType.competing, name="kocki i rakiji 🍻"),
        discord.Activity(type=discord.ActivityType.playing,   name="Balkan igre 🎮"),
        discord.Activity(type=discord.ActivityType.watching,  name="tvojim /hunt resultatima 🏹"),
        discord.Activity(type=discord.ActivityType.playing,   name="sa životinjama u zoo-u 🦁"),
        discord.Activity(type=discord.ActivityType.competing, name="battle turniru ⚔️"),
        discord.CustomActivity(name="💰 Ekonomija • 🎮 Igre • 🐾 OWO"),
        discord.CustomActivity(name=f"🟣 {BOT_NAME}"),
        discord.Activity(type=discord.ActivityType.listening, name="/help za sve komande"),
    ]
    await bot.change_presence(activity=random.choice(statuses))

# ═══════════════════════════════════════════
#    INFO & UTILS
# ═══════════════════════════════════════════
@bot.tree.command(name="ping", description="🏓 Provjeri brzinu bota")
async def ping(i: discord.Interaction):
    ms = round(bot.latency * 1000)
    status, color = ("🟢 Odlično", COLORS["success"]) if ms < 80 else ("🟡 Dobro", COLORS["warning"]) if ms < 180 else ("🔴 Sporo", COLORS["error"])
    await i.response.send_message(embed=em("🏓 Pong!", color=color, fields=[
        ("📡 Latency", f"`{ms}ms`", True), ("📊 Status", status, True), ("🤖 Bot", f"`{bot.user}`", True)
    ]))

@bot.tree.command(name="serverinfo", description="📊 Informacije o serveru")
async def serverinfo(i: discord.Interaction):
    g = i.guild
    bots, humans = sum(1 for m in g.members if m.bot), g.member_count - sum(1 for m in g.members if m.bot)
    await i.response.send_message(embed=em(f"🏰 {g.name}", color=COLORS["purple"], thumb=g.icon.url if g.icon else None, fields=[
        ("👑 Vlasnik",   g.owner.mention,                                        True),
        ("👥 Članovi",   f"`{humans}` ljudi • `{bots}` botova",                 True),
        ("📅 Kreiran",   g.created_at.strftime("%d.%m.%Y."),                    True),
        ("💬 Kanali",    f"`{len(g.text_channels)}` tekst • `{len(g.voice_channels)}` voice", True),
        ("🏷️ Uloge",    f"`{len(g.roles)-1}`",                                  True),
        ("🚀 Boostovi",  f"`{g.premium_subscription_count or 0}`",              True),
    ]))

@bot.tree.command(name="userinfo", description="👤 Informacije o korisniku")
async def userinfo(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    eco, xpd = get_economy(u.id), get_xp(u.id)
    warns = len(get_warnings(i.guild.id, u.id))
    await i.response.send_message(embed=em(f"👤 {u.display_name}", color=u.accent_color or COLORS["default"], thumb=u.display_avatar.url, fields=[
        ("🆔 ID",          f"`{u.id}`",                                            True),
        ("📅 Pridružio",   u.joined_at.strftime("%d.%m.%Y.") if u.joined_at else "N/A", True),
        ("🏷️ Top uloga",  u.top_role.mention,                                    True),
        ("💰 Balans",      f"`{eco['balance']:,} 💶`",                            True),
        ("📈 Level",       f"`{xpd['level']}`",                                   True),
        ("⚠️ Upozorenja",  f"`{warns}`",                                           True),
    ]))

@bot.tree.command(name="spotify", description="🎵 Pogledaj šta korisnik trenutno sluša na Spotifyu")
async def spotify_cmd(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    spotify = next((a for a in u.activities if isinstance(a, discord.Spotify)), None)
    if not spotify:
        return await i.response.send_message(
            embed=em("🎵 Spotify", f"{u.mention} trenutno **ne sluša ništa** na Spotifyu.\n\n💡 *Mora imati Spotify povezan sa Discord nalogom i pustiti pjesmu.*", color=COLORS["warning"]),
            ephemeral=False
        )
    duration = spotify.duration
    elapsed = datetime.now(timezone.utc) - spotify.start
    progress = min(elapsed.total_seconds() / duration.total_seconds(), 1.0)
    bar_len = 20
    filled = int(progress * bar_len)
    bar = "▰" * filled + "▱" * (bar_len - filled)
    def fmt_t(td):
        s = int(td.total_seconds()); return f"{s//60}:{s%60:02d}"
    e = discord.Embed(
        title=f"🎵 {spotify.title}",
        url=f"https://open.spotify.com/track/{spotify.track_id}",
        description=f"**Izvođač:** {spotify.artist}\n**Album:** {spotify.album}\n\n`{fmt_t(elapsed)}` {bar} `{fmt_t(duration)}`",
        color=0x1DB954,  # Spotify zelena
        timestamp=datetime.now(timezone.utc)
    )
    e.set_author(name=f"{u.display_name} sluša", icon_url=u.display_avatar.url)
    if spotify.album_cover_url: e.set_thumbnail(url=spotify.album_cover_url)
    e.set_footer(text=f"Spotify • {BOT_NAME}")
    await i.response.send_message(embed=e)

@bot.tree.command(name="invite", description="📊 Statistika — poruke + invite-ovi")
async def invite_cmd(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    mkey = f"{i.guild.id}:{u.id}"
    msg_n = data["msg_count"].get(mkey, 0)
    ikey = f"{i.guild.id}:{u.id}"
    inv_rec = data["invites"].get(ikey, {})
    inv_count = inv_rec.get("count", 0)
    invite_url = None
    invite_uses = 0
    try:
        invs = await i.guild.invites()
        user_invs = [inv for inv in invs if inv.inviter and inv.inviter.id == u.id]
        if user_invs:
            best = max(user_invs, key=lambda x: x.uses)
            invite_url = f"https://discord.gg/{best.code}"
            invite_uses = best.uses
            if not inv_rec:
                inv_count = best.uses
    except Exception as _e: print(f"[pump] {_e}")
    e = em(f"📊 Statistika — {u.display_name}",
        color=u.accent_color or COLORS["balkan"], thumb=u.display_avatar.url, fields=[
        ("✍️ Poruke poslato", f"`{msg_n:,}`", True),
        ("👥 Doveo članova",   f"`{inv_count}`", True),
        ("📅 Pridružio",       u.joined_at.strftime("%d.%m.%Y.") if u.joined_at else "N/A", True),
        ("🔗 Tvoj invite",     f"`{invite_uses}` korišćenja" if invite_url else "*nemaš svoj invite link*", False),
    ])
    e.set_footer(text=f"Korisnik: {u} • ID: {u.id}")
    view = None
    if invite_url:
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Otvori invite", emoji="🔗", url=invite_url, style=discord.ButtonStyle.link))
    await i.response.send_message(embed=e, view=view) if view else await i.response.send_message(embed=e)

@bot.tree.command(name="avatar", description="🖼️ Prikaži avatar korisnika")
async def avatar(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    await i.response.send_message(embed=em(f"🖼️ {u.display_name}",
        f"[PNG]({u.display_avatar.with_format('png').url}) • [JPG]({u.display_avatar.with_format('jpg').url}) • [WEBP]({u.display_avatar.with_format('webp').url})",
        color=COLORS["info"], image=u.display_avatar.url))

@bot.tree.command(name="say", description="🗣️ Bot šalje poruku")
@app_commands.checks.has_permissions(manage_messages=True)
async def say(i: discord.Interaction, tekst: str, kanal: discord.TextChannel = None):
    target = kanal or i.channel
    await target.send(tekst, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
    await i.response.send_message(embed=em("✅ Poslato!", f"Kanal: {target.mention}", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="brojanje-postavi", description="🔢 Postavi kanal za brojanje [ADMIN]")
@app_commands.describe(kanal="Kanal u kojem će se brojati", pocetak="Od kog broja krenuti (default 0 → sljedeći je 1)")
@app_commands.checks.has_permissions(administrator=True)
async def brojanje_postavi(i: discord.Interaction, kanal: discord.TextChannel, pocetak: int = 0):
    data["counting"][str(i.guild.id)] = {
        "channel_id": kanal.id,
        "current": max(0, pocetak),
        "last_user": None,
        "high_score": data.get("counting", {}).get(str(i.guild.id), {}).get("high_score", 0)
    }
    save_data()
    nxt = max(0, pocetak) + 1
    e = em("✅ Kanal za brojanje postavljen!",
           f"Kanal: {kanal.mention}\n"
           f"Trenutno: **{max(0, pocetak)}**\n"
           f"Sljedeći broj: **{nxt}**\n\n"
           f"📜 **Pravila:**\n"
           f"• Pišite brojeve redom (1, 2, 3, …)\n"
           f"• Ne smiješ brojati dvaput zaredom\n"
           f"• Ko pogriješi → reset na 0\n"
           f"• Svaki **50.** broj = `+100 💶` `+50 XP` 🎯",
           color=COLORS["success"])
    await i.response.send_message(embed=e)

@bot.tree.command(name="brojanje-info", description="🔢 Pokaži stanje brojanja")
async def brojanje_info(i: discord.Interaction):
    cfg = data.get("counting", {}).get(str(i.guild.id))
    if not cfg:
        return await i.response.send_message(
            embed=em("❌", "Brojanje nije postavljeno! Admin može sa `/brojanje-postavi`.", color=COLORS["error"]),
            ephemeral=True
        )
    ch = i.guild.get_channel(cfg["channel_id"])
    nxt = cfg.get("current", 0) + 1
    last = cfg.get("last_user")
    last_txt = f"<@{last}>" if last else "—"
    e = discord.Embed(
        title="🔢 Brojanje — stanje",
        description=(
            f"📍 **Kanal:** {ch.mention if ch else '*(obrisan)*'}\n"
            f"🔢 **Trenutno:** `{cfg.get('current', 0)}`\n"
            f"➡️ **Sljedeći broj:** `{nxt}`\n"
            f"👤 **Zadnji brojao:** {last_txt}\n"
            f"🏆 **Rekord:** `{cfg.get('high_score', 0)}`"
        ),
        color=COLORS["info"], timestamp=datetime.now(timezone.utc)
    )
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

@bot.tree.command(name="brojanje-reset", description="🔢 Resetuj brojanje na 0 [ADMIN]")
@app_commands.checks.has_permissions(administrator=True)
async def brojanje_reset(i: discord.Interaction):
    cfg = data.get("counting", {}).get(str(i.guild.id))
    if not cfg:
        return await i.response.send_message(
            embed=em("❌", "Brojanje nije postavljeno!", color=COLORS["error"]),
            ephemeral=True
        )
    cfg["current"] = 0
    cfg["last_user"] = None
    save_data()
    await i.response.send_message(embed=em("✅ Resetovano!", "Brojanje krene od **1**.", color=COLORS["success"]))

@bot.tree.command(name="setname", description="✏️ Promeni ime bota")
@app_commands.checks.has_permissions(administrator=True)
async def setname(i: discord.Interaction, ime: str):
    try:
        await bot.user.edit(username=ime)
        e = em("✅ Ime promenjeno!", f"Novo ime: **{ime}**", color=COLORS["success"])
    except discord.HTTPException as ex:
        e = em("❌ Greška", f"{ex}\n*Max 2 promene na 10 min*", color=COLORS["error"])
    await i.response.send_message(embed=e, ephemeral=True)

@bot.tree.command(name="setavatar", description="🖼️ Promeni sliku bota")
@app_commands.checks.has_permissions(administrator=True)
async def setavatar(i: discord.Interaction, url: str):
    await i.response.defer(ephemeral=True)
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                if resp.status != 200:
                    return await i.followup.send(embed=em("❌ Greška", "Ne mogu preuzeti sliku.", color=COLORS["error"]), ephemeral=True)
                img = await resp.read()
        await bot.user.edit(avatar=img)
        e = em("✅ Avatar promenjen!", "Nova slika je postavljena!", color=COLORS["success"], thumb=url)
    except Exception as ex:
        e = em("❌ Greška", str(ex), color=COLORS["error"])
    await i.followup.send(embed=e, ephemeral=True)

# ═══════════════════════════════════════════
#    MODERACIJA
# ═══════════════════════════════════════════
@bot.tree.command(name="ban", description="🔨 Banuj korisnika")
@app_commands.default_permissions(ban_members=True)
@app_commands.checks.has_permissions(ban_members=True)
async def ban(i: discord.Interaction, korisnik: discord.Member, razlog: str = "Bez razloga"):
    if korisnik.top_role >= i.user.top_role:
        return await i.response.send_message(embed=em("❌ Greška", "Ne možeš banovati nekoga sa višom ulogom!", color=COLORS["error"]), ephemeral=True)
    await korisnik.ban(reason=razlog)
    await i.response.send_message(embed=em("🔨 Banovan", color=COLORS["error"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", f"{korisnik} (`{korisnik.id}`)", False),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, False),
    ]))

@bot.tree.command(name="kick", description="👢 Izbaci korisnika")
@app_commands.default_permissions(kick_members=True)
@app_commands.checks.has_permissions(kick_members=True)
async def kick(i: discord.Interaction, korisnik: discord.Member, razlog: str = "Bez razloga"):
    if korisnik.top_role >= i.user.top_role:
        return await i.response.send_message(embed=em("❌ Greška", "Ne možeš izbaciti nekoga sa višom ulogom!", color=COLORS["error"]), ephemeral=True)
    await korisnik.kick(reason=razlog)
    await i.response.send_message(embed=em("👢 Izbačen", color=COLORS["warning"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", f"{korisnik} (`{korisnik.id}`)", False),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, False),
    ]))

@bot.tree.command(name="timeout", description="⏱️ Ućutkaj korisnika")
@app_commands.default_permissions(moderate_members=True)
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout_cmd(i: discord.Interaction, korisnik: discord.Member, minuta: int = 10, razlog: str = "Bez razloga"):
    if not 1 <= minuta <= 1440:
        return await i.response.send_message(embed=em("❌ Greška", "Između 1 i 1440 minuta!", color=COLORS["error"]), ephemeral=True)
    await korisnik.timeout(discord.utils.utcnow() + timedelta(minutes=minuta), reason=razlog)
    await i.response.send_message(embed=em("⏱️ Ućutkan", color=COLORS["warning"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", korisnik.mention, True), ("⏳ Trajanje", f"`{minuta}` min", True),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, True),
    ]))

@bot.tree.command(name="warn", description="⚠️ Upozori korisnika")
@app_commands.default_permissions(manage_messages=True)
@app_commands.checks.has_permissions(manage_messages=True)
async def warn(i: discord.Interaction, korisnik: discord.Member, razlog: str = "Kršenje pravila"):
    warns = get_warnings(i.guild.id, korisnik.id)
    warns.append({"razlog": razlog, "moderator": str(i.user), "vreme": datetime.now(timezone.utc).strftime("%d.%m.%Y. %H:%M")})
    save_data()
    await i.response.send_message(embed=em("⚠️ Upozorenje", color=COLORS["warning"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", korisnik.mention, True), ("📊 Ukupno", f"`{len(warns)}`", True),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, True),
    ]))

@bot.tree.command(name="warnings", description="📋 Upozorenja korisnika")
@app_commands.checks.has_permissions(manage_messages=True)
async def warnings_cmd(i: discord.Interaction, korisnik: discord.Member):
    warns = get_warnings(i.guild.id, korisnik.id)
    if not warns:
        return await i.response.send_message(embed=em(f"📋 {korisnik.display_name}", "Nema upozorenja! ✅", color=COLORS["success"]), ephemeral=True)
    desc = "\n".join([f"`{n+1}.` **{w['razlog']}** — {w['vreme']}" for n, w in enumerate(warns)])
    await i.response.send_message(embed=em(f"📋 {korisnik.display_name} — Upozorenja", desc, color=COLORS["warning"], thumb=korisnik.display_avatar.url), ephemeral=True)

@bot.tree.command(name="clearwarnings", description="🗑️ Obriši upozorenja")
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def clearwarnings(i: discord.Interaction, korisnik: discord.Member):
    data["warnings"].get(str(i.guild.id), {}).pop(str(korisnik.id), None)
    save_data()
    await i.response.send_message(embed=em("✅ Obrisano", f"Sva upozorenja za {korisnik.mention} su uklonjena.", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="clear", description="🧹 Obriši poruke")
@app_commands.default_permissions(manage_messages=True)
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(i: discord.Interaction, kolicina: int = 10):
    await i.response.defer(ephemeral=True)
    deleted = await i.channel.purge(limit=max(1, min(kolicina, 100)))
    await i.followup.send(embed=em("🧹 Čišćenje završeno", color=COLORS["success"], fields=[
        ("🗑️ Obrisano", f"`{len(deleted)}` poruka", True), ("📌 Kanal", i.channel.mention, True),
    ]), ephemeral=True)

# ═══════════════════════════════════════════
#    EKONOMIJA & LEVEL
# ═══════════════════════════════════════════
@bot.tree.command(name="baki", description="💰 Provjeri stanje novca")
async def baki(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    d = get_economy(u.id)
    last = time.strftime("%H:%M", time.localtime(d["last_work"])) if d["last_work"] else "Nikad"
    await i.response.send_message(embed=em_pro(f"💰 Novčanik", f"💎 Stanje računa za {u.mention}", color=COLORS["gold"], thumb=u.display_avatar.url, author=u, fields=[
        ("💶 Balans", f"```yaml\n{d['balance']:,} 💶\n```", True), ("💼 Poslednji posao", f"`{last}`", True),
    ]))

@bot.tree.command(name="posao", description="💼 Radi i zaradi (svaki sat)")
@app_commands.checks.cooldown(1, 3600, key=lambda i: i.user.id)
async def posao(i: discord.Interaction):
    d = get_economy(i.user.id)
    earn = random.randint(150, 600)
    d["balance"] += earn; d["last_work"] = time.time(); save_data()
    quest_progress(i.user.id, "work3")
    await i.response.send_message(embed=em("💼 Posao završen!", f"*{random.choice(JOBS)}*", color=COLORS["success"], fields=[
        ("💶 Zarada", f"`+{earn} 💶`", True), ("🏦 Balans", f"`{d['balance']:,} 💶`", True), ("⏰ Sledeći", "za 1 sat", True),
    ]))

@bot.tree.command(name="daily", description="🎁 Dnevna nagrada")
@app_commands.checks.cooldown(1, 86400, key=lambda i: i.user.id)
async def daily(i: discord.Interaction):
    d = get_economy(i.user.id)
    reward = random.randint(300, 800)
    d["balance"] += reward; d["last_daily"] = time.time(); save_data()
    quest_progress(i.user.id, "daily1")
    await i.response.send_message(embed=em_pro("🎁 Dnevna Nagrada", "🌟 Tvoj dnevni poklon je stigao!\n*Vrati se sutra za novu nagradu* 🔄", color=COLORS["gold"], author=i.user, thumb=i.user.display_avatar.url, fields=[
        ("💶 Nagrada", f"```diff\n+ {reward} 💶\n```", True), ("🏦 Balans", f"```yaml\n{d['balance']:,} 💶\n```", True),
    ]))

@bot.tree.command(name="daj", description="🤝 Pošalji pare drugaru")
async def daj(i: discord.Interaction, korisnik: discord.Member, iznos: int):
    if iznos <= 0: return await i.response.send_message(embed=em("❌ Greška", "Iznos mora biti pozitivan!", color=COLORS["error"]), ephemeral=True)
    if korisnik.id == i.user.id: return await i.response.send_message(embed=em("❌ Greška", "Ne možeš sebi slati!", color=COLORS["error"]), ephemeral=True)
    s, r = get_economy(i.user.id), get_economy(korisnik.id)
    if s["balance"] < iznos: return await i.response.send_message(embed=em("❌ Nemaš dovoljno", f"Imaš samo `{s['balance']:,} 💶`!", color=COLORS["error"]), ephemeral=True)
    s["balance"] -= iznos; r["balance"] += iznos; save_data()
    await i.response.send_message(embed=em("🤝 Transakcija uspešna", color=COLORS["success"], fields=[
        ("📤 Od", i.user.mention, True), ("📥 Za", korisnik.mention, True), ("💶 Iznos", f"`{iznos:,} 💶`", True),
    ]))

@bot.tree.command(name="kradi", description="🕵️ Pokušaj ukrasti (rizično!)")
@app_commands.checks.cooldown(1, 7200, key=lambda i: i.user.id)
async def kradi(i: discord.Interaction, korisnik: discord.Member):
    if korisnik.id == i.user.id: return await i.response.send_message(embed=em("❌", "Ne možeš krasti sam sebe!", color=COLORS["error"]), ephemeral=True)
    if korisnik.bot: return await i.response.send_message(embed=em("❌", "Botovi nemaju para!", color=COLORS["error"]), ephemeral=True)
    s, r = get_economy(i.user.id), get_economy(korisnik.id)
    if r["balance"] < 100: return await i.response.send_message(embed=em("❌", "Siromašna žrtva, nema šta ukrasti.", color=COLORS["error"]), ephemeral=True)
    await i.response.defer()
    await asyncio.sleep(2)
    amount = random.randint(50, min(600, r["balance"]))
    if random.random() < 0.38:
        r["balance"] -= amount; s["balance"] += amount
        e = em("🕵️ Krađa uspešna!", "Niko te nije video. Za sad... 👀", color=COLORS["gold"], fields=[
            ("💰 Ukradeno", f"`{amount:,} 💶`", True), ("👤 Žrtva", korisnik.mention, True), ("🏦 Balans", f"`{s['balance']:,} 💶`", True),
        ])
    else:
        fine = random.randint(100, 350)
        s["balance"] = max(0, s["balance"] - fine)
        e = em("🚔 Uhvaćen si!", f"{korisnik.mention} te je prijavio policiji! 🤡", color=COLORS["error"], fields=[
            ("💸 Kazna", f"`{fine:,} 💶`", True), ("🏦 Balans", f"`{s['balance']:,} 💶`", True),
        ])
    save_data(); await i.followup.send(embed=e)

@bot.tree.command(name="rank", description="📈 Level i XP")
async def rank(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    d = get_xp(u.id)
    needed = d["level"] * 75
    filled = min(d["xp"] * 10 // needed, 10)
    bar = "🟪" * filled + "⬛" * (10 - filled)
    pct = round(d["xp"] / needed * 100)
    await i.response.send_message(embed=em_pro(f"📈 Rank Profil", f"{bar}\n`{'▰'*filled}{'▱'*(10-filled)}` **{pct}%**", color=COLORS["purple"], thumb=u.display_avatar.url, author=u, fields=[
        ("🏆 Level", f"```fix\n{d['level']}\n```", True), ("⭐ XP", f"```py\n{d['xp']}/{needed}\n```", True), ("📊 Progres", f"```css\n[{pct}%]\n```", True),
    ]))

@bot.tree.command(name="leaderboard", description="🏅 Top lista servera")
@app_commands.choices(tip=[app_commands.Choice(name="XP & Leveli", value="xp"), app_commands.Choice(name="Novac 💶", value="novac")])
async def leaderboard(i: discord.Interaction, tip: str = "xp"):
    await i.response.defer()
    medals = ["🥇", "🥈", "🥉"]
    if tip == "xp":
        srt = sorted(data["xp"].items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True)[:10]
        lines = []
        for n, (uid, d) in enumerate(srt):
            try: user = await bot.fetch_user(int(uid)); name = user.display_name
            except: name = f"#{uid[:4]}"
            lines.append(f"{medals[n] if n<3 else f'`{n+1}.`'} **{name}** — Level `{d['level']}` • `{d['xp']} XP`")
        e = em("🏅 Top Lista — XP", "\n".join(lines) or "Nema podataka.", color=COLORS["purple"])
    else:
        srt = sorted(data["economy"].items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
        lines = []
        for n, (uid, d) in enumerate(srt):
            try: user = await bot.fetch_user(int(uid)); name = user.display_name
            except: name = f"#{uid[:4]}"
            lines.append(f"{medals[n] if n<3 else f'`{n+1}.`'} **{name}** — `{d['balance']:,} 💶`")
        e = em("🏅 Top Lista — Bogatstvo", "\n".join(lines) or "Nema podataka.", color=COLORS["gold"])
    await i.followup.send(embed=e)

# ═══════════════════════════════════════════
#    IGRE
# ═══════════════════════════════════════════
class KPM(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=30); self.user = user; self.msg = None

    async def on_timeout(self):
        for c in self.children: c.disabled = True
        if self.msg: await self.msg.edit(embed=em("⏱️ Vreme isteklo!", "Igra otkazana.", color=COLORS["error"]), view=self)

    async def play(self, i, choice):
        if i.user != self.user: return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        bot_c = random.choice(["🪨 Kamen", "📄 Papir", "✂️ Makaze"])
        win_map = {("Kamen","Makaze"),("Papir","Kamen"),("Makaze","Papir")}
        cw, bw = choice.split()[1], bot_c.split()[1]
        if choice == bot_c: res, color = "🤝 Nerešeno!", COLORS["warning"]
        elif (cw, bw) in win_map: res, color = "🏆 Pobedio si!", COLORS["success"]
        else: res, color = "💀 Izgubio si!", COLORS["error"]
        for c in self.children: c.disabled = True
        await i.response.edit_message(embed=em(f"🎮 KPM — {res}", color=color, fields=[
            ("👤 Ti", choice, True), ("🤖 Bot", bot_c, True), ("📊 Rezultat", res, False),
        ]), view=self); self.stop()

    @discord.ui.button(label="Kamen",  emoji="🪨", style=discord.ButtonStyle.primary)
    async def r(self, i, b): await self.play(i, "🪨 Kamen")
    @discord.ui.button(label="Papir",  emoji="📄", style=discord.ButtonStyle.success)
    async def p(self, i, b): await self.play(i, "📄 Papir")
    @discord.ui.button(label="Makaze", emoji="✂️", style=discord.ButtonStyle.danger)
    async def s(self, i, b): await self.play(i, "✂️ Makaze")

@bot.tree.command(name="kpm", description="🎮 Kamen-Papir-Makaze")
async def kpm(i: discord.Interaction):
    v = KPM(i.user)
    await i.response.send_message(embed=em("🎮 Kamen-Papir-Makaze", f"{i.user.mention}, odaberi potez! ⏱️ 30s", color=COLORS["balkan"]), view=v)
    v.msg = await i.original_response()

@bot.tree.command(name="slots", description="🎰 Slot mašina")
@app_commands.checks.cooldown(1, 15, key=lambda i: i.user.id)
async def slots(i: discord.Interaction):
    await i.response.defer()
    await asyncio.sleep(1)
    symbols = ["🍒","🍋","🍊","🍇","💎","7️⃣","⭐","🔔"]
    reels = [random.choice(symbols) for _ in range(3)]
    d = get_economy(i.user.id)
    if reels[0]==reels[1]==reels[2]:
        reward = 1500 if reels[0] in ("💎","7️⃣") else 600
        res, color = f"🎉 JACKPOT! `+{reward} 💶`", COLORS["gold"]; d["balance"] += reward
    elif reels[0]==reels[1] or reels[1]==reels[2]:
        reward = 80; res, color = f"✨ Dobitak! `+{reward} 💶`", COLORS["success"]; d["balance"] += reward
    else:
        loss = 25; res, color = f"😢 Prazno. `-{loss} 💶`", COLORS["error"]; d["balance"] = max(0, d["balance"]-loss)
    save_data()
    await i.followup.send(embed=em("🎰 Slot Mašina", f"**{' ║ '.join(reels)}**", color=color, fields=[
        ("🎯 Rezultat", res, False), ("🏦 Balans", f"`{d['balance']:,} 💶`", True),
    ]))

@bot.tree.command(name="rulet", description="🔫 Ruski rulet (za hrabre!)")
@app_commands.checks.cooldown(1, 600, key=lambda i: i.user.id)
async def rulet(i: discord.Interaction):
    await i.response.defer(); await asyncio.sleep(2)
    d = get_economy(i.user.id)
    if random.random() < 0.167:
        e = em("💀 PUCANJ!", "Metak je bio u komori... 😵\nBolje sreće sledeći put — ako bude sledeći put.", color=COLORS["error"])
    else:
        reward = random.randint(300, 1000); d["balance"] += reward; save_data()
        e = em("🔫 Preživeo si!", "Klik. Metak nije bio tu. Nisi bogat, ali si živ! 😅", color=COLORS["success"], fields=[
            ("💶 Nagrada", f"`+{reward} 💶`", True), ("🏦 Balans", f"`{d['balance']:,} 💶`", True),
        ])
    await i.followup.send(embed=e)

@bot.tree.command(name="flip", description="🪙 Baci novčić — možeš kladiti")
async def flip(i: discord.Interaction, oklada: int = 0):
    d = get_economy(i.user.id)
    if oklada < 0: return await i.response.send_message(embed=em("❌", "Oklada ne može biti negativna!", color=COLORS["error"]), ephemeral=True)
    if oklada > d["balance"]: return await i.response.send_message(embed=em("❌ Nemaš dovoljno", f"Imaš `{d['balance']:,} 💶`", color=COLORS["error"]), ephemeral=True)
    await i.response.defer(); await asyncio.sleep(1)
    won = random.choice([True, False])
    if oklada > 0:
        if won: d["balance"] += oklada; extra = f"\n💶 Zaradio `+{oklada} 💶`!"
        else: d["balance"] -= oklada; extra = f"\n💸 Izgubio `-{oklada} 💶`!"
        save_data()
    else: extra = ""
    await i.followup.send(embed=em(f"🪙 {'Glava! 👤' if won else 'Pismo! 📜'}",
        f"**{'Glava 👤' if won else 'Pismo 📜'}**{extra}",
        color=COLORS["success"] if won else COLORS["error"],
        fields=[("🏦 Balans", f"`{d['balance']:,} 💶`", True)] if oklada>0 else None
    ))

@bot.tree.command(name="8ball", description="🎱 Postavi pitanje magičnoj kugli")
async def eightball(i: discord.Interaction, pitanje: str):
    await i.response.send_message(embed=em("🎱 Magična Kugla", color=COLORS["purple"], fields=[
        ("❓ Pitanje", pitanje, False), ("💬 Odgovor", random.choice(EIGHTBALL_REPLIES), False),
    ]))

@bot.tree.command(name="meme", description="🤣 Nasumični Balkan meme")
async def meme(i: discord.Interaction):
    await i.response.send_message(embed=em("🤣 Balkan Meme", get_next_meme(i.guild.id), color=COLORS["fun"]))

# ═══════════════════════════════════════════
#    VJEŠALA (Hangman)
# ═══════════════════════════════════════════
class VjesalaModal(discord.ui.Modal, title="Unesi slovo"):
    slovo = discord.ui.TextInput(label="Slovo (jedno)", min_length=1, max_length=1, placeholder="Npr: A")

    def __init__(self, hangman_view):
        super().__init__()
        self.hv = hangman_view

    async def on_submit(self, i: discord.Interaction):
        await self.hv.guess(i, self.slovo.value.upper().strip())

class VjesalaView(discord.ui.View):
    def __init__(self, user: discord.Member, word: str):
        super().__init__(timeout=300)
        self.user    = user
        self.word    = word.upper()
        self.guessed: set = set()
        self.wrong   = 0
        self.max_w   = 6
        self.over    = False

    def display_word(self):
        return " ".join(c if c in self.guessed else "\\_ " for c in self.word)

    def make_embed(self, title=None, color=None):
        wrong_letters = [l for l in sorted(self.guessed) if l not in self.word]
        right_letters = [l for l in sorted(self.guessed) if l in self.word]
        t = title or "🎮 Vješala"
        c = color or COLORS["balkan"]
        e = discord.Embed(title=t, color=c, timestamp=datetime.now(timezone.utc))
        e.add_field(name="🔤 Riječ", value=f"`{self.display_word()}`", inline=False)
        e.add_field(name="💀 Vješalo", value=VJASALA_FAZE[self.wrong], inline=True)
        e.add_field(name="❌ Pogrešna", value=" ".join(wrong_letters) or "—", inline=True)
        e.add_field(name="✅ Tačna", value=" ".join(right_letters) or "—", inline=True)
        e.add_field(name="❤️ Životi", value=f"`{self.max_w - self.wrong}/{self.max_w}`", inline=True)
        e.set_footer(text=f"{BOT_NAME} {VERSION} • Pogodi slovo klikom!")
        return e

    async def guess(self, i: discord.Interaction, letter: str):
        if i.user != self.user:
            return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        if not letter.isalpha():
            return await i.response.send_message(embed=em("❌", "Unesi samo slovo!", color=COLORS["error"]), ephemeral=True)
        if letter in self.guessed:
            return await i.response.send_message(embed=em("⚠️", f"Slovo **{letter}** si već pokušao!", color=COLORS["warning"]), ephemeral=True)
        self.guessed.add(letter)
        if letter not in self.word:
            self.wrong += 1
        won  = all(c in self.guessed for c in self.word)
        lost = self.wrong >= self.max_w
        if won:
            self.over = True; self.children[0].disabled = True
            await i.response.edit_message(embed=self.make_embed(f"🏆 Pobijedio si! Riječ: **{self.word}**", COLORS["success"]), view=self)
            self.stop()
        elif lost:
            self.over = True; self.children[0].disabled = True
            await i.response.edit_message(embed=self.make_embed(f"💀 Izgubio si! Bila je: **{self.word}**", COLORS["error"]), view=self)
            self.stop()
        else:
            await i.response.edit_message(embed=self.make_embed(), view=self)

    async def on_timeout(self):
        if not self.over:
            self.children[0].disabled = True
            try:
                await self.message.edit(embed=self.make_embed(f"⏱️ Vreme isteklo! Bila je: **{self.word}**", COLORS["error"]), view=self)
            except: pass

    @discord.ui.button(label="Unesi slovo", style=discord.ButtonStyle.primary, emoji="✏️")
    async def enter(self, i: discord.Interaction, b: discord.ui.Button):
        if i.user != self.user:
            return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        await i.response.send_modal(VjesalaModal(self))

    @discord.ui.button(label="Predaj se", emoji="🏳️", style=discord.ButtonStyle.danger)
    async def give_up(self, i: discord.Interaction, b: discord.ui.Button):
        if i.user != self.user:
            return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        self.over = True
        for c in self.children: c.disabled = True
        await i.response.edit_message(embed=self.make_embed(f"🏳️ Predao si! Bila je: **{self.word}**", COLORS["warning"]), view=self)
        self.stop()

@bot.tree.command(name="vjasala", description="🎮 Igra Vješala — pogodi skrivenu riječ!")
async def vjasala(i: discord.Interaction):
    word = random.choice(VJASALA_RJECNIK)
    v    = VjesalaView(i.user, word)
    await i.response.send_message(embed=v.make_embed(), view=v)
    v.message = await i.original_response()

# ═══════════════════════════════════════════
#    KALADONT
# ═══════════════════════════════════════════
KALADONT_START_WORDS = [
    "BALKON","RAKIJA","KAFANA","FUDBAL","TANJIR","SUNCE","ZIVOT","RIJEKA",
    "PLANINA","DRVO","KAMEN","VATRA","ZEMLJA","VJETAR","OBLAK","JEZERO",
    "MOST","GRAD","SELO","POLJE","BRDO","DOLINA","SPILJA","OCEAN",
    "MAJKA","OTAC","BRAT","SESTRA","BAKA","DJED","PRIJATELJ","KOMŠIJA",
    "GITARA","MUZIKA","PJESMA","PLES","RADIO","POZORIŠTE","BIOSKOP",
    "AUTOMOBIL","AVION","BROD","VAGON","BICIKL","MOTOCIKL","TRAKTOR",
    "JABUKA","KRUŠKA","ŠLJIVA","TREŠNJA","BANANA","NARANDZA","GROŽĐE",
    "CEVAPI","BUREK","SARMA","KAJMAK","PITA","PALAČINKA","KOLAC",
    "ŠKOLA","BOLNICA","CRKVA","DŽAMIJA","STADION","BIBLIOTEKA","MUZEJ",
]

kaladont_games: dict = {}  # channel_id -> {word, used, starter, letters, chain, msg}

KALADONT_ICONS = ["🔵","🟣","🟤","🟠","🟡","🟢","🩵","🩶"]

def kaladont_start_embed(game: dict, mention: str):
    word    = game["word"]
    letters = game["letters"]
    req     = word[-letters:]
    e = discord.Embed(
        title="🔤  K A L A D O N T",
        description=(
            f"## 🟢  {word}  ·  *🤖 Bot*\n"
            f"─────────────────────────────\n"
            f"➡️  Sledeća mora početi sa  **` {req} `**\n\n"
            f"*Piši direktno u chat — bez klikanja!*"
        ),
        color=0x1ABC9C,
        timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="🔢 Težina",  value=f"`{letters}` slova", inline=True)
    e.add_field(name="📊 Rijeci", value="`1`",                inline=True)
    e.set_footer(text=f"Pokrenuo {mention}  •  {BOT_NAME} {VERSION}  •  Pritisni 🏁 za kraj")
    return e

def kaladont_active_embed(game: dict):
    word    = game["word"]
    letters = game["letters"]
    req     = word[-letters:]
    count   = len(game["chain"])
    e = discord.Embed(
        title="🔤  K A L A D O N T  —  aktivna igra",
        description=f"➡️  Sledeća mora početi sa  **` {req} `**",
        color=0x1ABC9C,
        timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="🎯 Zadnja",  value=f"`{word}`",         inline=True)
    e.add_field(name="📊 Rijeci", value=f"`{count}`",         inline=True)
    e.set_footer(text=f"{BOT_NAME} {VERSION}  •  Pritisni 🏁 za kraj igre")
    return e

def kaladont_word_card(word: str, player: str, req: str, count: int):
    icon = KALADONT_ICONS[(count - 1) % len(KALADONT_ICONS)]
    e = discord.Embed(
        description=(
            f"## {icon}  {word}  ·  *{player}*\n"
            f"─────────────────────────────\n"
            f"➡️  Sledeća počinje sa  **` {req} `**"
        ),
        color=0x2ECC71,
        timestamp=datetime.now(timezone.utc)
    )
    e.set_footer(text=f"#{count}  •  {BOT_NAME} {VERSION}")
    return e

class KaladontView(discord.ui.View):
    def __init__(self, channel_id: int):
        super().__init__(timeout=None)
        self.channel_id = channel_id

    @discord.ui.button(label="Završi igru", emoji="🏁", style=discord.ButtonStyle.danger)
    async def zavrsi(self, i: discord.Interaction, b: discord.ui.Button):
        game = kaladont_games.get(self.channel_id)
        if not game:
            return await i.response.send_message(embed=em("❌", "Nema aktivne igre.", color=COLORS["error"]), ephemeral=True)
        if i.user.id != game["starter"] and not i.user.guild_permissions.manage_messages:
            return await i.response.send_message(embed=em("❌", "Samo pokretač ili mod može završiti igru!", color=COLORS["error"]), ephemeral=True)
        count = len(game["chain"])
        del kaladont_games[self.channel_id]
        b.disabled = True
        e = discord.Embed(
            title="🏁 Kaladont završen!",
            description=f"Igra gotova! Ukupno izgovoreno **{count}** rijeci. 🎉",
            color=COLORS["gold"], timestamp=datetime.now(timezone.utc)
        )
        e.set_footer(text=f"{BOT_NAME} {VERSION}")
        await i.response.edit_message(embed=e, view=self)
        self.stop()

@bot.tree.command(name="kaladont", description="🔤 Pokretanje igre Kaladont — ulančaj riječi!")
@app_commands.describe(slova="Koliko zadnjih slova mora nova rijec početi (1, 2 ili 3)")
@app_commands.choices(slova=[
    app_commands.Choice(name="1 slovo (lakše)", value=1),
    app_commands.Choice(name="2 slova (normalno)", value=2),
    app_commands.Choice(name="3 slova (teže)", value=3),
])
async def kaladont(i: discord.Interaction, slova: int = 2):
    if i.channel.id in kaladont_games:
        return await i.response.send_message(
            embed=em("⚠️ Igra već teče!", "U ovom kanalu je već aktivan Kaladont. Završi prvu!", color=COLORS["warning"]), ephemeral=True)
    start_word = random.choice(KALADONT_START_WORDS)
    game = {
        "word":    start_word,
        "used":    {start_word},
        "starter": i.user.id,
        "letters": slova,
        "chain":   [(start_word, "🤖 Bot")],
        "msg":     None,
    }
    kaladont_games[i.channel.id] = game
    v = KaladontView(i.channel.id)
    await i.response.send_message(embed=kaladont_start_embed(game, i.user.display_name), view=v)
    resp = await i.original_response()
    game["msg"] = resp

@bot.tree.command(name="kaladont-stop", description="🔤 Zaustavi trenutnu Kaladont igru u ovom kanalu")
async def kaladont_stop(i: discord.Interaction):
    game = kaladont_games.get(i.channel.id)
    if not game:
        return await i.response.send_message(
            embed=em("ℹ️", "Nema aktivne Kaladont igre u ovom kanalu.", color=COLORS["info"]),
            ephemeral=True
        )
    is_admin = i.user.guild_permissions.administrator
    if i.user.id != game["starter"] and not is_admin:
        return await i.response.send_message(
            embed=em("🚫", "Samo onaj ko je pokrenuo igru ili admin može zaustaviti!", color=COLORS["error"]),
            ephemeral=True
        )
    chain = game.get("chain", [])
    count = len(chain)
    last_word = game.get("word", "—")
    del kaladont_games[i.channel.id]
    e = discord.Embed(
        title="🛑 Kaladont zaustavljen",
        description=(
            f"Igru zaustavio: {i.user.mention}\n\n"
            f"📊 **Riječi u nizu:** `{count}`\n"
            f"🔤 **Zadnja riječ:** `{last_word}`"
        ),
        color=COLORS["warning"], timestamp=datetime.now(timezone.utc)
    )
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

# ═══════════════════════════════════════════
#    TOPLO-HLADNO
# ═══════════════════════════════════════════
toplo_games: dict = {}  # channel_id -> {"secret": int, "guesses": int, "starter": int, "min": int, "max": int}

TEMPERATURE = [
    (0,  0,   "🎯 TAČNO!",       COLORS["gold"]),
    (1,  5,   "🔥 VRELO je!",    0xFF4500),
    (6,  15,  "♨️ Jako toplo!",  COLORS["error"]),
    (16, 30,  "🌡️ Toplo...",     COLORS["warning"]),
    (31, 60,  "😐 Mlako...",     COLORS["info"]),
    (61, 120, "❄️ Hladno!",      0x87CEEB),
    (121,999, "🥶 Ledeno!",      0x4169E1),
]

def get_temperature(diff: int):
    for lo, hi, label, color in TEMPERATURE:
        if lo <= diff <= hi:
            return label, color
    return "🥶 Ledeno!", 0x4169E1

class ToploModal(discord.ui.Modal, title="Toplo-Hladno — Pogodi broj!"):
    broj = discord.ui.TextInput(label="Tvoj broj", min_length=1, max_length=5, placeholder="Unesi broj...")

    def __init__(self, view):
        super().__init__(); self.tv = view

    async def on_submit(self, i: discord.Interaction):
        try:
            guess = int(self.broj.value.strip())
        except ValueError:
            return await i.response.send_message(embed=em("❌", "Unesi cijeli broj!", color=COLORS["error"]), ephemeral=True)
        await self.tv.process_guess(i, guess)

class ToploView(discord.ui.View):
    def __init__(self, channel_id: int, starter: discord.Member, secret: int, max_num: int):
        super().__init__(timeout=None)
        self.channel_id = channel_id
        self.max_num    = max_num
        toplo_games[channel_id] = {"secret": secret, "guesses": 0, "starter": starter.id, "history": []}

    def make_embed(self, result: str = "", color=None, solved=False):
        game = toplo_games.get(self.channel_id, {})
        guesses = game.get("guesses", 0)
        history = game.get("history", [])[-5:]
        c = color or COLORS["info"]
        e = discord.Embed(title="🌡️ Toplo-Hladno", color=c, timestamp=datetime.now(timezone.utc))
        e.add_field(name="🎯 Raspon", value=f"`1 — {self.max_num}`", inline=True)
        e.add_field(name="🔢 Pokušaji", value=f"`{guesses}`", inline=True)
        if result: e.add_field(name="📡 Signal", value=result, inline=False)
        if history and not solved:
            e.add_field(name="📜 Zadnji pokušaji", value="\n".join(history), inline=False)
        e.set_footer(text=f"{BOT_NAME} {VERSION} • Klikni i pogodi broj!")
        return e

    async def process_guess(self, i: discord.Interaction, guess: int):
        game = toplo_games.get(self.channel_id)
        if not game:
            return await i.response.send_message(embed=em("❌", "Igra nije aktivna!", color=COLORS["error"]), ephemeral=True)
        if not 1 <= guess <= self.max_num:
            return await i.response.send_message(
                embed=em("❌ Van raspona!", f"Unesi broj između `1` i `{self.max_num}`!", color=COLORS["error"]), ephemeral=True)
        game["guesses"] += 1
        secret = game["secret"]
        diff   = abs(guess - secret)
        label, color = get_temperature(diff)
        direction = "⬆️ više" if guess < secret else "⬇️ manje" if guess > secret else ""
        hint = f"`{guess}` → {label}" + (f" ({direction})" if direction else "")
        game["history"].append(hint)
        if diff == 0:
            for c in self.children: c.disabled = True
            del toplo_games[self.channel_id]
            e = discord.Embed(
                title=f"🎯 {i.user.mention} pogodio/la!",
                description=f"Tajna je bila **`{secret}`**!\n🏆 Pogođeno za **{game['guesses']}** pokušaja!",
                color=COLORS["gold"], timestamp=datetime.now(timezone.utc)
            )
            e.set_footer(text=f"{BOT_NAME} {VERSION}")
            await i.response.edit_message(embed=e, view=self)
            self.stop()
        else:
            await i.response.edit_message(embed=self.make_embed(hint, color), view=self)

    @discord.ui.button(label="Pogodi broj", emoji="🌡️", style=discord.ButtonStyle.primary)
    async def guess_btn(self, i: discord.Interaction, b: discord.ui.Button):
        if self.channel_id not in toplo_games:
            return await i.response.send_message(embed=em("❌", "Igra nije aktivna.", color=COLORS["error"]), ephemeral=True)
        await i.response.send_modal(ToploModal(self))

    @discord.ui.button(label="Završi igru", emoji="🏁", style=discord.ButtonStyle.danger)
    async def zavrsi(self, i: discord.Interaction, b: discord.ui.Button):
        game = toplo_games.get(self.channel_id)
        if not game:
            return await i.response.send_message(embed=em("❌", "Nema aktivne igre.", color=COLORS["error"]), ephemeral=True)
        if i.user.id != game["starter"] and not i.user.guild_permissions.manage_messages:
            return await i.response.send_message(embed=em("❌", "Samo pokretač ili mod može završiti igru!", color=COLORS["error"]), ephemeral=True)
        secret = game["secret"]
        del toplo_games[self.channel_id]
        for c in self.children: c.disabled = True
        e = discord.Embed(title="🏁 Igra završena!",
            description=f"Tajna je bila **`{secret}`**!\nNiko nije pogodio ovaj put. 😅",
            color=COLORS["warning"], timestamp=datetime.now(timezone.utc))
        e.set_footer(text=f"{BOT_NAME} {VERSION}")
        await i.response.edit_message(embed=e, view=self)
        self.stop()

@bot.tree.command(name="toplo-hladno", description="🌡️ Pogodi tajni broj — Toplo ili Hladno!")
@app_commands.describe(maksimum="Maksimalni broj (default 100, max 1000)")
async def toplo_hladno(i: discord.Interaction, maksimum: int = 100):
    if i.channel.id in toplo_games:
        return await i.response.send_message(
            embed=em("⚠️ Igra već teče!", "U ovom kanalu je već aktivna igra. Završi prvu!", color=COLORS["warning"]), ephemeral=True)
    maksimum = max(10, min(maksimum, 1000))
    secret = random.randint(1, maksimum)
    v = ToploView(i.channel.id, i.user, secret, maksimum)
    await i.response.send_message(
        embed=v.make_embed(f"🎮 {i.user.mention} pokrenuo igru!\nPogodi broj od `1` do `{maksimum}`!", COLORS["info"]),
        view=v
    )

# ═══════════════════════════════════════════
#    AMONG US — AMOGUS
# ═══════════════════════════════════════════
PLAYER_COLORS   = ["🔴","🟠","🟡","🟢","🔵","🟣","⚫","⚪","🟤","🩷"]
IMPOSTOR_COUNTS = {4:1, 5:1, 6:1, 7:2, 8:2, 9:2, 10:3}
TASKS_PER_PLAYER = 3
KILL_COOLDOWN_SEC = 30

AMOGUS_TASKS = [
    {"q":"📐 Koliko je 17 × 6?",              "a":"102"},
    {"q":"📐 Koliko je 144 ÷ 12?",             "a":"12"},
    {"q":"📐 Koliko je 23 × 4 − 7?",           "a":"85"},
    {"q":"📐 Kvadratni korijen od 144?",        "a":"12"},
    {"q":"🔢 Niz: 2, 4, 8, 16, __?",           "a":"32"},
    {"q":"🔢 Niz: 1, 3, 6, 10, 15, __?",       "a":"21"},
    {"q":"🔢 Niz: 5, 10, 20, 40, __?",         "a":"80"},
    {"q":"🔢 Sljedeći prost broj nakon 7?",     "a":"11"},
    {"q":"⌨️ Upiši: WARP_DRIVE_ON",            "a":"WARP_DRIVE_ON"},
    {"q":"⌨️ Upiši: REACTOR_CORE_7",           "a":"REACTOR_CORE_7"},
    {"q":"⌨️ Upiši: AMOGUS_IMPOSTOR",          "a":"AMOGUS_IMPOSTOR"},
    {"q":"⌨️ Upiši: KABINA_7_ONLINE",          "a":"KABINA_7_ONLINE"},
    {"q":"⌨️ Upiši: MEDIC_BAY_SCAN",           "a":"MEDIC_BAY_SCAN"},
    {"q":"🧠 Glavni grad Srbije?",              "a":"Beograd"},
    {"q":"🧠 Glavni grad Bosne i Hercegovine?", "a":"Sarajevo"},
]

amogus_games: dict = {}  # channel_id -> state

def _ag(cid):
    return amogus_games.get(cid)

def _task_bar(done, total):
    filled = int((done / total) * 10) if total else 0
    return "🟩"*filled + "⬜"*(10-filled) + f" `{done}/{total}`"

def _ag_player_list(players, show_roles=False):
    lines = []
    for uid, p in players.items():
        dead = "💀 ~~" if not p["alive"] else ""
        end  = "~~" if not p["alive"] else ""
        role = f" — **{'🔴 IMP' if p['role']=='impostor' else '🔵 CREW'}**" if show_roles else ""
        td   = f" [{p['tasks_done']}/{TASKS_PER_PLAYER}]" if p["alive"] and not show_roles else ""
        lines.append(f"{dead}{p['color']} {p['name']}{td}{role}{end}")
    return "\n".join(lines) or "*Nema igrača*"

def _ag_lobby_embed(state):
    players = state["players"]
    e = discord.Embed(title="🚀 Among Us — Lobby", color=0x1B1B2F,
                      description="Pridruži se i čekaj da host pokrene igru!\n**Min 4 • Max 10 igrača**",
                      timestamp=datetime.now(timezone.utc))
    e.add_field(name=f"👥 Igrači ({len(players)}/10)",
                value="\n".join(f"{p['color']} {p['name']}" for p in players.values()) or "*Čekamo...*",
                inline=False)
    e.set_footer(text="Host: klikni ▶️ Pokreni igru kad ste svi tu!")
    return e

def _ag_game_embed(state):
    alive = [p for p in state["players"].values() if p["alive"]]
    ac = sum(1 for p in alive if p["role"]=="crewmate")
    ai = sum(1 for p in alive if p["role"]=="impostor")
    e = discord.Embed(title="🚀 Among Us — U Toku", color=0x1B1B2F, timestamp=datetime.now(timezone.utc))
    e.add_field(name="👥 Igrači", value=_ag_player_list(state["players"]), inline=False)
    e.add_field(name="📋 Zadaci", value=_task_bar(state["done_tasks"], state["total_tasks"]), inline=True)
    e.add_field(name="🎭 Živi", value=f"🔵 {ac} crew | 🔴 {ai} imp", inline=True)
    e.set_footer(text="📋 Zadatak  •  🚨 Alarm  •  🔪 Akcija (impostor)")
    return e

async def _ag_check_win(state, channel) -> bool:
    alive = [p for p in state["players"].values() if p["alive"]]
    ac = [p for p in alive if p["role"]=="crewmate"]
    ai = [p for p in alive if p["role"]=="impostor"]
    if not ai:
        await _ag_end(state, channel, "🔵 CREWMATI POBIJEDE!", "Svi impostori eliminirani! ✅", COLORS["success"])
        return True
    if len(ai) >= len(ac):
        await _ag_end(state, channel, "🔴 IMPOSTORI POBIJEDE!", "Impostori preuzeli brod! ☠️", COLORS["error"])
        return True
    if state["done_tasks"] >= state["total_tasks"] > 0:
        await _ag_end(state, channel, "🔵 CREWMATI POBIJEDE!", "Svi zadaci završeni! 🎉", COLORS["success"])
        return True
    return False

async def _ag_end(state, channel, title, desc, color):
    state["phase"] = "ended"
    reveal = "\n".join(
        f"{'🔴' if p['role']=='impostor' else '🔵'} {p['color']} **{p['name']}** — {p['role'].upper()}"
        for p in state["players"].values()
    )
    e = discord.Embed(title=f"🏁 {title}", description=desc, color=color, timestamp=datetime.now(timezone.utc))
    e.add_field(name="🎭 Otkrivene uloge", value=reveal, inline=False)
    e.set_footer(text=f"{BOT_NAME} • Among Us")
    await channel.send(embed=e)
    amogus_games.pop(channel.id, None)

async def _ag_tally(channel, state):
    tally = Counter(v for v in state["votes"].values() if v is not None)
    if not tally:
        state["phase"] = "playing"; state["votes"] = {}
        await channel.send(embed=em("⏭️ Niko nije eliminisan", "Svi su preskočili — igra se nastavlja!", color=COLORS["warning"]))
        gv = state.get("game_view")
        if gv: await channel.send(embed=_ag_game_embed(state), view=gv)
        return
    max_v   = max(tally.values())
    winners = [uid for uid, c in tally.items() if c == max_v]
    if len(winners) > 1:
        state["phase"] = "playing"; state["votes"] = {}
        await channel.send(embed=em("⚖️ Izjednačeno!", "Glasanje neodlučeno — niko nije eliminisan!", color=COLORS["warning"]))
        gv = state.get("game_view")
        if gv: await channel.send(embed=_ag_game_embed(state), view=gv)
        return
    ejected_id = winners[0]
    ejected_p  = state["players"][ejected_id]
    ejected_p["alive"] = False
    role_txt = "🔴 **IMPOSTOR**" if ejected_p["role"] == "impostor" else "🔵 **CREWMATE**"
    e = discord.Embed(
        title=f"🚀 {ejected_p['name']} je izbačen/a!",
        description=f"{ejected_p['color']} **{ejected_p['name']}** eliminisan/a sa **{max_v}** glasova.\nBio/la je: {role_txt}",
        color=COLORS["error"] if ejected_p["role"]=="impostor" else COLORS["warning"],
        timestamp=datetime.now(timezone.utc)
    )
    await channel.send(embed=e)
    if not await _ag_check_win(state, channel):
        state["phase"] = "playing"; state["votes"] = {}
        gv = state.get("game_view")
        if gv: await channel.send(embed=_ag_game_embed(state), view=gv)

# ── Views ──────────────────────────────────────────────────

class AmogusLobbyView(discord.ui.View):
    def __init__(self, cid):
        super().__init__(timeout=300)
        self.cid = cid

    @discord.ui.button(label="Pridruži se", emoji="🚀", style=discord.ButtonStyle.success)
    async def join(self, i: discord.Interaction, b):
        state = _ag(self.cid)
        if not state or state["phase"] != "lobby":
            return await i.response.send_message(embed=em("❌","Lobby je zatvoren!",color=COLORS["error"]),ephemeral=True)
        uid = str(i.user.id)
        if uid in state["players"]:
            return await i.response.send_message(embed=em("✅","Već si tu!",color=COLORS["warning"]),ephemeral=True)
        if len(state["players"]) >= 10:
            return await i.response.send_message(embed=em("❌","Lobby pun (10/10)!",color=COLORS["error"]),ephemeral=True)
        idx = len(state["players"]) % len(PLAYER_COLORS)
        state["players"][uid] = {"name":i.user.display_name,"alive":True,"role":None,
                                  "color":PLAYER_COLORS[idx],"tasks":[],"tasks_done":0,"kill_cd":0}
        await i.response.edit_message(embed=_ag_lobby_embed(state), view=self)

    @discord.ui.button(label="Napusti", emoji="🚪", style=discord.ButtonStyle.secondary)
    async def leave(self, i: discord.Interaction, b):
        state = _ag(self.cid)
        if not state or state["phase"] != "lobby":
            return await i.response.send_message(embed=em("❌","Lobby zatvoren!",color=COLORS["error"]),ephemeral=True)
        uid = str(i.user.id)
        if uid not in state["players"]:
            return await i.response.send_message(embed=em("❌","Nisi u lobby-u!",color=COLORS["error"]),ephemeral=True)
        del state["players"][uid]
        if not state["players"]:
            amogus_games.pop(self.cid, None)
            return await i.response.edit_message(embed=em("🚪","Lobby zatvoren.",color=COLORS["error"]),view=None)
        if state["host"] == i.user.id:
            state["host"] = int(next(iter(state["players"])))
        await i.response.edit_message(embed=_ag_lobby_embed(state), view=self)

    @discord.ui.button(label="Pokreni igru", emoji="▶️", style=discord.ButtonStyle.primary)
    async def start(self, i: discord.Interaction, b):
        state = _ag(self.cid)
        if not state:
            return await i.response.send_message(embed=em("❌","Nema lobby-a!",color=COLORS["error"]),ephemeral=True)
        if i.user.id != state["host"]:
            return await i.response.send_message(embed=em("❌","Samo host može pokrenuti!",color=COLORS["error"]),ephemeral=True)
        if len(state["players"]) < 4:
            return await i.response.send_message(embed=em("❌",f"Treba min **4 igrača**! Sad: `{len(state['players'])}`",color=COLORS["error"]),ephemeral=True)
        await i.response.defer()
        n     = len(state["players"])
        n_imp = IMPOSTOR_COUNTS.get(n, 1)
        ids   = list(state["players"].keys())
        random.shuffle(ids)
        for idx, uid in enumerate(ids):
            role = "impostor" if idx < n_imp else "crewmate"
            state["players"][uid]["role"] = role
            state["players"][uid]["tasks"] = [dict(t, done=False) for t in random.sample(AMOGUS_TASKS, TASKS_PER_PLAYER)]
        state["total_tasks"] = (n - n_imp) * TASKS_PER_PLAYER
        state["done_tasks"]  = 0
        state["phase"]       = "playing"
        # DMs
        bad_dm = []
        for uid, p in state["players"].items():
            member = i.guild.get_member(int(uid))
            if not member: continue
            is_imp = p["role"] == "impostor"
            dm_e = discord.Embed(
                title=f"{'🔴 IMPOSTOR' if is_imp else '🔵 CREWMATE'} — Tvoja uloga!",
                description=("🔴 **Eliminiši crewmate-e, ne budi uhvaćen!**\nKoristi dugme 🔪 **Akcija** za ubijanje."
                             if is_imp else
                             "🔵 **Završi zadatke, pronađi impostora!**\nKoristi dugme 📋 **Zadatak** za rad."),
                color=COLORS["error"] if is_imp else COLORS["info"]
            )
            if is_imp:
                partners = [state["players"][x]["name"] for x in ids[:n_imp] if x != uid]
                if partners: dm_e.add_field(name="🔴 Saimpostori", value="\n".join(partners))
            dm_e.set_footer(text=f"{BOT_NAME} • Samo ti vidiš ovo!")
            try: await member.send(embed=dm_e)
            except: bad_dm.append(p["name"])
        gv = AmogusGameView(self.cid)
        state["game_view"] = gv
        extra = f"\n⚠️ Nije mogao primiti DM: {', '.join(bad_dm)}" if bad_dm else ""
        start_e = discord.Embed(title="🚀 Igra počinje!", description=f"Uloge podijeljene! Provjeri **DM** za svoju ulogu.{extra}",
                                color=0x1B1B2F, timestamp=datetime.now(timezone.utc))
        await i.edit_original_response(embed=start_e, view=None)
        await i.channel.send(embed=_ag_game_embed(state), view=gv)

class AmogusTaskModal(discord.ui.Modal, title="📋 Zadatak"):
    odgovor = discord.ui.TextInput(label="Odgovor:", placeholder="Upiši odgovor...", max_length=60)
    def __init__(self, cid, uid, tidx):
        super().__init__()
        self.cid  = cid
        self.uid  = uid
        self.tidx = tidx
        state = _ag(cid)
        if state and uid in state["players"]:
            q = state["players"][uid]["tasks"][tidx]["q"]
            self.odgovor.label = q[:45]
    async def on_submit(self, i: discord.Interaction):
        state = _ag(self.cid)
        if not state or state["phase"] != "playing":
            return await i.response.send_message(embed=em("❌","Igra nije aktivna!",color=COLORS["error"]),ephemeral=True)
        p    = state["players"][self.uid]
        task = p["tasks"][self.tidx]
        if self.odgovor.value.strip().lower() == task["a"].strip().lower():
            task["done"] = True
            p["tasks_done"] += 1
            state["done_tasks"] += 1
            rem = TASKS_PER_PLAYER - p["tasks_done"]
            msg = f"✅ Tačno! Ostalo zadataka: **{rem}**" if rem else "✅ Svi zadaci završeni! 🎉"
            await i.response.send_message(embed=em("📋 Zadatak završen!", msg, color=COLORS["success"]), ephemeral=True)
            gv = state.get("game_view")
            try: await i.message.edit(embed=_ag_game_embed(state), view=gv)
            except: pass
            await _ag_check_win(state, i.channel)
        else:
            await i.response.send_message(embed=em("❌ Pogrešno!","Pokušaj ponovo!", color=COLORS["error"]), ephemeral=True)

class AmogusKillSelect(discord.ui.View):
    def __init__(self, cid, killer_id):
        super().__init__(timeout=20)
        self.cid       = cid
        self.killer_id = killer_id
        state = _ag(cid)
        if not state: return
        opts = [discord.SelectOption(label=p["name"], value=uid, emoji=p["color"])
                for uid, p in state["players"].items()
                if p["alive"] and uid != str(killer_id) and p["role"] == "crewmate"]
        if opts:
            s = discord.ui.Select(placeholder="Odaberi žrtvu...", options=opts[:25])
            s.callback = self.do_kill
            self.add_item(s)
    async def do_kill(self, i: discord.Interaction):
        state = _ag(self.cid)
        if not state or state["phase"] != "playing":
            return await i.response.send_message(embed=em("❌","Igra nije aktivna!",color=COLORS["error"]),ephemeral=True)
        ks  = str(self.killer_id)
        kp  = state["players"].get(ks)
        if not kp or not kp["alive"]:
            return await i.response.send_message(embed=em("❌","Ne možeš ubijati!",color=COLORS["error"]),ephemeral=True)
        now = time.time()
        if now - kp.get("kill_cd",0) < KILL_COOLDOWN_SEC:
            left = int(KILL_COOLDOWN_SEC-(now-kp["kill_cd"]))
            return await i.response.send_message(embed=em("⏳",f"Cooldown! Čekaj još `{left}s`",color=COLORS["warning"]),ephemeral=True)
        vid = i.data["values"][0]
        vp  = state["players"].get(vid)
        if not vp or not vp["alive"]:
            return await i.response.send_message(embed=em("❌","Taj igrač nije dostupan!",color=COLORS["error"]),ephemeral=True)
        vp["alive"] = False
        kp["kill_cd"] = now
        # reduce total tasks
        state["total_tasks"] = max(0, state["total_tasks"] - (TASKS_PER_PLAYER - vp["tasks_done"]))
        await i.response.send_message(embed=em("🔪 Eliminirano!",f"**{vp['name']}** je eliminisan/a! Niko ne zna...",color=COLORS["error"]),ephemeral=True)
        vm = i.guild.get_member(int(vid))
        if vm:
            try: await vm.send(embed=em("💀 Eliminisan/a si!",f"**{kp['name']}** te je eliminisao/la. Možeš promatrati igru.",color=COLORS["error"]))
            except: pass
        gv = state.get("game_view")
        try: await i.message.edit(embed=_ag_game_embed(state), view=gv)
        except: pass
        await _ag_check_win(state, i.channel)
        self.stop()

class AmogusGameView(discord.ui.View):
    def __init__(self, cid):
        super().__init__(timeout=None)
        self.cid = cid

    @discord.ui.button(label="Zadatak", emoji="📋", style=discord.ButtonStyle.primary)
    async def task_btn(self, i: discord.Interaction, b):
        state = _ag(self.cid)
        if not state or state["phase"] != "playing":
            return await i.response.send_message(embed=em("❌","Igra nije aktivna!",color=COLORS["error"]),ephemeral=True)
        uid = str(i.user.id)
        if uid not in state["players"]:
            return await i.response.send_message(embed=em("❌","Nisi u igri!",color=COLORS["error"]),ephemeral=True)
        p = state["players"][uid]
        if not p["alive"]:
            return await i.response.send_message(embed=em("💀","Mrtvi ne mogu raditi zadatke!",color=COLORS["error"]),ephemeral=True)
        tidx = next((idx for idx,t in enumerate(p["tasks"]) if not t["done"]), None)
        if tidx is None:
            return await i.response.send_message(embed=em("✅ Sve završeno!","Čekaj ostatak tima! 🎉",color=COLORS["success"]),ephemeral=True)
        await i.response.send_modal(AmogusTaskModal(self.cid, uid, tidx))

    @discord.ui.button(label="Alarm!", emoji="🚨", style=discord.ButtonStyle.danger)
    async def alarm_btn(self, i: discord.Interaction, b):
        state = _ag(self.cid)
        if not state or state["phase"] != "playing":
            return await i.response.send_message(embed=em("❌","Igra nije aktivna!",color=COLORS["error"]),ephemeral=True)
        uid = str(i.user.id)
        if uid not in state["players"] or not state["players"][uid]["alive"]:
            return await i.response.send_message(embed=em("❌","Ne možeš sazvati meeting!",color=COLORS["error"]),ephemeral=True)
        state["phase"]      = "meeting"
        state["votes"]      = {}
        state["meeting_by"] = i.user.id
        alive_pl = [(k, v["name"]) for k,v in state["players"].items() if v["alive"]]
        mv = AmogusMeetingView(self.cid, alive_pl)
        state["meeting_view"] = mv
        me = _ag_meeting_embed(state, state["players"][uid]["name"], "Emergency Meeting 🚨")
        await i.response.send_message(embed=me, view=mv)

    @discord.ui.button(label="Akcija", emoji="🔪", style=discord.ButtonStyle.secondary)
    async def action_btn(self, i: discord.Interaction, b):
        state = _ag(self.cid)
        if not state or state["phase"] != "playing":
            return await i.response.send_message(embed=em("❌","Igra nije aktivna!",color=COLORS["error"]),ephemeral=True)
        uid = str(i.user.id)
        if uid not in state["players"]:
            return await i.response.send_message(embed=em("❌","Nisi u igri!",color=COLORS["error"]),ephemeral=True)
        p = state["players"][uid]
        if not p["alive"]:
            return await i.response.send_message(embed=em("💀","Mrtvi ništa ne mogu!",color=COLORS["error"]),ephemeral=True)
        if p["role"] != "impostor":
            return await i.response.send_message(embed=em("🔵 Ti si Crewmate!","Samo impostori mogu koristiti Akciju.",color=COLORS["info"]),ephemeral=True)
        kv = AmogusKillSelect(self.cid, i.user.id)
        if not kv.children:
            return await i.response.send_message(embed=em("❌","Nema živih crewmate-a!",color=COLORS["error"]),ephemeral=True)
        await i.response.send_message(embed=em("🔪 Odaberi žrtvu","Samo ti vidiš ovo!",color=COLORS["error"]),view=kv,ephemeral=True)

def _ag_meeting_embed(state, caller, reason):
    e = discord.Embed(title="🚨 EMERGENCY MEETING!", color=0xFF0000,
                      description=f"**{caller}** je sazvao/la meeting!\n*{reason}*\n\n**Glasajte koga eliminišete!**",
                      timestamp=datetime.now(timezone.utc))
    alive = {k:v for k,v in state["players"].items() if v["alive"]}
    e.add_field(name="👥 Živi igrači", value=_ag_player_list(alive), inline=False)
    total_alive = len(alive)
    e.add_field(name="🗳️ Glasanje", value=f"`0` od `{total_alive}` glasalo", inline=True)
    e.set_footer(text="Glasajte mudro! Eliminisani igrač otkrije svoju ulogu.")
    return e

class AmogusMeetingView(discord.ui.View):
    def __init__(self, cid, alive_players):
        super().__init__(timeout=90)
        self.cid           = cid
        self.alive_players = alive_players
        for uid, name in alive_players:
            btn = discord.ui.Button(label=name[:20], custom_id=f"agv_{uid}", style=discord.ButtonStyle.secondary)
            btn.callback = self._vote_cb(uid, name)
            self.add_item(btn)
        skip = discord.ui.Button(label="Preskoči", emoji="⏭️", custom_id="agv_skip", style=discord.ButtonStyle.secondary)
        skip.callback = self._vote_cb(None, "Preskoči")
        self.add_item(skip)

    def _vote_cb(self, tid, tname):
        async def cb(i: discord.Interaction):
            state = _ag(self.cid)
            if not state or state["phase"] != "meeting":
                return await i.response.send_message(embed=em("❌","Meeting završen!",color=COLORS["error"]),ephemeral=True)
            uid = str(i.user.id)
            if uid not in state["players"] or not state["players"][uid]["alive"]:
                return await i.response.send_message(embed=em("❌","Ne možeš glasati!",color=COLORS["error"]),ephemeral=True)
            if uid in state["votes"]:
                return await i.response.send_message(embed=em("⚠️","Već si glasao/la!",color=COLORS["warning"]),ephemeral=True)
            state["votes"][uid] = tid
            label = f"**{tname}**" if tid else "Preskoči"
            await i.response.send_message(embed=em("🗳️ Glas zabilježen!",f"Glasao/la si za: {label}",color=COLORS["success"]),ephemeral=True)
            alive_cnt = sum(1 for p in state["players"].values() if p["alive"])
            # Update meeting embed vote count
            try:
                me = i.message.embeds[0]
                me.set_field_at(1, name="🗳️ Glasanje", value=f"`{len(state['votes'])}` od `{alive_cnt}` glasalo", inline=True)
                await i.message.edit(embed=me)
            except: pass
            if len(state["votes"]) >= alive_cnt:
                self.stop()
                await _ag_tally(i.channel, state)
        return cb

    async def on_timeout(self):
        state = _ag(self.cid)
        if not state or state["phase"] != "meeting": return
        for guild in bot.guilds:
            chan = guild.get_channel(self.cid)
            if chan:
                await chan.send(embed=em("⏱️ Glasanje isteklo!","Premalo glasova — niko nije eliminisan.", color=COLORS["warning"]))
                await _ag_tally(chan, state)
                break

@bot.tree.command(name="amogus", description="🚀 Pokreni Among Us igru!")
async def amogus_cmd(i: discord.Interaction):
    if i.channel.id in amogus_games:
        return await i.response.send_message(embed=em("❌","Igra je već aktivna! Koristi `/amogus-stop` za kraj.",color=COLORS["error"]),ephemeral=True)
    state = {"phase":"lobby","host":i.user.id,"channel_id":i.channel.id,
             "players":{},"total_tasks":0,"done_tasks":0,"votes":{},"game_view":None,"meeting_view":None}
    state["players"][str(i.user.id)] = {
        "name":i.user.display_name,"alive":True,"role":None,
        "color":PLAYER_COLORS[0],"tasks":[],"tasks_done":0,"kill_cd":0
    }
    amogus_games[i.channel.id] = state
    await i.response.send_message(embed=_ag_lobby_embed(state), view=AmogusLobbyView(i.channel.id))

@bot.tree.command(name="amogus-stop", description="🚀 Zaustavi Among Us igru [HOST/ADMIN]")
async def amogus_stop(i: discord.Interaction):
    state = _ag(i.channel.id)
    if not state:
        return await i.response.send_message(embed=em("❌","Nema aktivne igre!",color=COLORS["error"]),ephemeral=True)
    if i.user.id != state["host"] and not i.user.guild_permissions.manage_messages:
        return await i.response.send_message(embed=em("❌","Samo host ili admin može zaustaviti igru!",color=COLORS["error"]),ephemeral=True)
    amogus_games.pop(i.channel.id, None)
    await i.response.send_message(embed=em("🚀 Igra zaustavljena","Among Us igra je prekinuta.", color=COLORS["warning"]))

# ═══════════════════════════════════════════
#    LJUBAVNE / SOCIJALNE KOMANDE
# ═══════════════════════════════════════════
async def social_cmd(i: discord.Interaction, target: discord.Member, action: str, txt: str, color_key: str = "love"):
    await i.response.defer()
    gif = await get_gif(action)
    opis = txt.replace("{from}", i.user.mention).replace("{to}", target.mention)
    e = discord.Embed(description=opis, color=COLORS[color_key], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    if gif: e.set_image(url=gif)
    await i.followup.send(embed=e)

@bot.tree.command(name="zagrljaj", description="🤗 Zagrli nekog na serveru")
async def zagrljaj(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "hug", "🤗 {from} grli {to}! Aww, tako slatko! 💕", "love")

@bot.tree.command(name="poljubac", description="💋 Pošalji poljubac nekome")
async def poljubac(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "kiss", "💋 {from} šalje poljubac {to}! 😘", "pink")

@bot.tree.command(name="mazi", description="🥰 Pomazi nekoga nježno")
async def mazi(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "pat", "🥰 {from} mazi {to} po glavi! Predobro! ✨", "love")

@bot.tree.command(name="tapsi", description="👋 Tapši nekoga prijateljski")
async def tapsi(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "handshake", "👋 {from} tapše {to}! Aj, brate! 🤝", "teal")

@bot.tree.command(name="high5", description="🙌 Daj peticu nekome")
async def high5(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "highfive", "🙌 {from} daje peticu {to}! Dobra ekipa! ⚡", "success")

@bot.tree.command(name="cudan", description="😠 Budi ćudan prema nekome")
async def cudan(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "poke", "😠 {from} je ćudan prema {to}! Ajde, brate... 😤", "warning")

@bot.tree.command(name="pocetkaj", description="🤕 Pocektaj nekoga za fun")
async def pocetkaj(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "slap", "🤕 {from} pocektao {to}! Za malu ljutu... 😵", "error")

@bot.tree.command(name="srce", description="❤️ Pošalji srce nekome")
async def srce(i: discord.Interaction, korisnik: discord.Member):
    poruke = [
        "❤️ {from} šalje srce {to}! Aww! 🥺",
        "💖 {from} voli {to}! Toliko slatko! 💕",
        "🌹 {from} poklanja ruže {to}! Romantično! 🌹",
        "💝 {from} šalje ljubav {to}! Neka traje! 💝",
    ]
    e = discord.Embed(description=random.choice(poruke).replace("{from}", i.user.mention).replace("{to}", korisnik.mention), color=COLORS["love"], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

@bot.tree.command(name="brak", description="💍 Zaprosio nekoga (za fun)")
async def brak(i: discord.Interaction, korisnik: discord.Member):
    if korisnik.id == i.user.id:
        return await i.response.send_message(embed=em("❌", "Ne možeš se zarositi sam sebi!", color=COLORS["error"]), ephemeral=True)
    odgovori = [
        f"💍 {i.user.mention} zaprosio {korisnik.mention}! 😍 Hoćeš li? 🥂",
        f"💒 {i.user.mention} klekne pred {korisnik.mention} i kaže: 'Hoćeš li biti moj/moja?' 💍",
        f"🌹 {i.user.mention} donosi ruže i prsten {korisnik.mention}! Romantika! 😘",
    ]
    e = discord.Embed(description=random.choice(odgovori), color=COLORS["love"], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

# ═══════════════════════════════════════════
#    POZDRAVI & MUVANJE
# ═══════════════════════════════════════════
_fun_cd: dict = {}  # (user_id, cmd) -> expires_at

async def fun_cooldown(i: discord.Interaction, cmd: str) -> bool:
    """Vrati True (i pošalji grešku) ako je korisnik na cooldownu."""
    key = (i.user.id, cmd)
    now = time.time()
    if key in _fun_cd and now < _fun_cd[key]:
        left = round(_fun_cd[key] - now, 1)
        await i.response.send_message(
            embed=em("⏳ Polako!", f"Čekaj još `{left}s` pa pošalji ponovo! 😅", color=COLORS["warning"]),
            ephemeral=True
        )
        return True
    _fun_cd[key] = now + random.randint(5, 7)
    return False

POZZ_PORUKE = [
    "{user} je toliko nesretan/nesretna da bi kiša padala samo na njega/nju! ☔😂",
    "{user} se pojavio/la! Svima odmah postalo malo bolje. Ili gore. Još ne znamo. 🤔",
    "{user} je stigao/la! Server je upravo dobio +1 na kaos. 🎲",
    "Oh, {user} je tu! Čak i WiFi malo usporio od uzbuđenja. 📶😂",
    "{user} je ušao/la kao da nosi sav teret Balkana na leđima. Budi jači/a, brate/sestro! 💪",
    "{user} se pojavio/la, oblaci su se razišli... al samo da ga/je bolje vide. ☁️👀",
    "{user} je stigao/la! Temperatura u sobi pala za 2 stepena. Brrr. 🥶",
    "{user} je tu! Neko je trebao doći kasno, i evo ga/je. ⏰😂",
    "{user} je ušao/la onako kako ulaze heroji — tiho, neopaženo, i malo zbunjeno. 🦸",
    "{user} se pojavio/la! Baba bi rekla: 'Ajde sine/ćeri, jesil jeo/jela?' 👵🍽️",
    "{user} je stigao/la! Google Maps kaže da si trebao/la biti tu prije 45 minuta. 🗺️😅",
    "{user} se prijavio/la na server! Anđeli plaču, a đavoli aplaudiraju. 😈😇",
    "{user} je tu! Čak i mačke na ulici znale da nešto nije u redu. 🐱",
    "Alarm! {user} je online! Sklanjajte sve vrijedno! 🚨😂",
    "{user} je ušao/la onako tiho kao slon u prodavnici porculana. 🐘",
]

KOMPLI_PORUKE = [
    "🌹 {from} kaže {to}: 'Ti si razlog zašto dan počinje sa osmijehom. 😍'",
    "💫 {from} za {to}: 'Tvoje oči sjaje više nego moj monitor u 3 ujutru. 😘'",
    "🌸 {from} {to}: 'Kad se smiješiš, čak i bots-ovi izgube koncentraciju. 💕'",
    "🎇 {from} kaže {to}: 'Ti si jedina osoba zbog koje bih zatvorio YouTube. I to je PUNO. 😅💖'",
    "🦋 {from} za {to}: 'Pored tebe, sve ostale zvezde izgledaju kao noćne lampice. ✨'",
    "🍀 {from} {to}: 'Ako si ti greška, onda je svemir trebao praviti više grešaka. 💝'",
    "🌙 {from} kaže {to}: 'Ti si razlog zašto pjesnici još uvijek pišu stihove. 📜💕'",
    "🔥 {from} za {to}: 'Toliko si cool da ni klima u mom sobi ne može da te dostigne. ❄️😍'",
    "🎀 {from} {to}: 'Kad si ti tu, cio server osjeti razliku. Kao sunce posle kiše. 🌈'",
    "💌 {from} kaže {to}: 'Nisi savršen/na, ali si savršen/na za mene. I to je sve što treba. 😘'",
    "🌺 {from} za {to}: 'Tvoj smijeh zvuči kao melodija koje bi slušao/la cio dan. 🎵💕'",
    "⭐ {from} {to}: 'Ti si dokaz da Bog ponekad ima dobrog dana. 😇✨'",
]

FORA_PORUKE = [
    "😂 {from} je pogledao/la {to} i shvatio/la: 'Brate/sestro, ti si dokaz da evolucija nije uvijek napredak.' 🐒",
    "🎭 {from} za {to}: 'Tražiš razlog da se smiješ? Pogledaj se u ogledalo!' 😭😂",
    "💀 {from} {to}: 'Toliko si prosječan/na da Google ne zna ni da te indexuje.' 🔍",
    "😤 {from} za {to}: 'Tvoja ex je bila u pravu za jedno — čekanje nije uvijek vrijedno.' 💔😂",
    "🧠 {from} {to}: 'Mislio/la sam da si pametan/na... al to bi mi bila prva greška.' 🤓",
    "🎪 {from} za {to}: 'Jedina stvar koja radi brže od tebe je moj internet kad ga fakturiram.' 📡😂",
    "😅 {from} {to}: 'Rekli su mi da budem ljubazan/na... al ni ja ne znam kako.' 💀",
    "👀 {from} za {to}: 'Svaki put kad pišeš, autocorrect se zapita je li vredno popraviti.' 📱😂",
    "🤦 {from} {to}: 'IQ ti je manji od temp u frižideru. I to zimski frižider.' ❄️",
    "🏆 {from} za {to}: 'Nagradu za originalnost si propustio/la zajedno sa svakom drugom nagradom.' 😂",
]

@bot.tree.command(name="pozz", description="👋 Pozdravi server ili nekoga (sa humorom!)")
@discord.app_commands.describe(korisnik="Korisnik koga pozdravljaš (opcionalno)")
async def pozz(i: discord.Interaction, korisnik: discord.Member = None):
    if await fun_cooldown(i, "pozz"): return
    target = korisnik or i.user
    poruka = random.choice(POZZ_PORUKE).replace("{user}", target.mention)
    e = discord.Embed(description=f"👋 **Pozz!**\n\n{poruka}", color=COLORS["fun"], timestamp=datetime.now(timezone.utc))
    e.set_thumbnail(url=target.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Pozdravi")
    await i.response.send_message(embed=e)

@bot.tree.command(name="kompli", description="🌹 Pošalji slatki kompliment nekome")
@discord.app_commands.describe(korisnik="Kome šalješ kompliment")
async def kompli(i: discord.Interaction, korisnik: discord.Member):
    if await fun_cooldown(i, "kompli"): return
    if korisnik.id == i.user.id:
        poruka = "🤡 Hm, komplimentiraš samog/samu sebe? Ajde, prihvatamo to!"
    else:
        poruka = random.choice(KOMPLI_PORUKE).replace("{from}", i.user.mention).replace("{to}", korisnik.mention)
    e = discord.Embed(description=poruka, color=COLORS["pink"], timestamp=datetime.now(timezone.utc))
    e.set_thumbnail(url=korisnik.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Muvanje 101 💕")
    await i.response.send_message(embed=e)

@bot.tree.command(name="fora", description="😂 Ubaci foru na račun nekoga (sve u šali!)")
@discord.app_commands.describe(korisnik="Ko prima foru")
async def fora(i: discord.Interaction, korisnik: discord.Member):
    if await fun_cooldown(i, "fora"): return
    if korisnik.id == i.user.id:
        poruka = "😂 Fora na vlastiti račun? Poštujemo samokritiku!"
    else:
        poruka = random.choice(FORA_PORUKE).replace("{from}", i.user.mention).replace("{to}", korisnik.mention)
    e = discord.Embed(description=poruka, color=COLORS["fun"], timestamp=datetime.now(timezone.utc))
    e.set_thumbnail(url=korisnik.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Sve u šali! 😂")
    await i.response.send_message(embed=e)

@bot.tree.command(name="muv", description="😏 Muvaj nekoga Balkan stilom")
@discord.app_commands.describe(korisnik="Ko je sretan/na da ga/ju muvaš")
async def muv(i: discord.Interaction, korisnik: discord.Member):
    if await fun_cooldown(i, "muv"): return
    if korisnik.id == i.user.id:
        return await i.response.send_message(embed=em("😅", "Ne možeš muvati samog/samu sebe, brate/sestro!", color=COLORS["error"]), ephemeral=True)
    muv_poruke = [
        f"😏 {i.user.mention} {korisnik.mention}: 'Jesi li ti WiFi? Jer osjećam konekciju između nas.' 📶💕",
        f"🌹 {i.user.mention} {korisnik.mention}: 'Daj mi broj, hoću te zvati svaki dan... osim kad nemam kredit.' 😂💖",
        f"🔥 {i.user.mention} {korisnik.mention}: 'Ti si kao kebab u 3 ujutru — ne znam zašto, ali baš te trebam.' 🌯😍",
        f"💫 {i.user.mention} kaže {korisnik.mention}: 'Slika ti se hvata svuda — čak i u mojim snovima. 📸💕'",
        f"😘 {i.user.mention} {korisnik.mention}: 'Da sam Google, stavil/la bih te na prvu stranicu. 🔍💝'",
        f"🎯 {i.user.mention} {korisnik.mention}: 'Znaš šta te razlikuje od ostalih? Sve. 😍✨'",
        f"🏹 {i.user.mention} {korisnik.mention}: 'Cupid me pogodio strelicom, ali mislim da si ti sljedeća meta. 😳💘'",
        f"🌙 {i.user.mention} {korisnik.mention}: 'Astronomija je dokazala da zvijezde padaju. Ali ti... ti nikad ne padaš s mog uma. 🌟'",
        f"☕ {i.user.mention} {korisnik.mention}: 'Ti si mi kao kafa ujutru — ne mogu bez tebe ni dan. 😏☕'",
        f"🎵 {i.user.mention} {korisnik.mention}: 'Svaka pjesma koju čujem podsjeti me na tebe. Čak i folk. 🎶💕'",
    ]
    e = discord.Embed(description=random.choice(muv_poruke), color=COLORS["love"], timestamp=datetime.now(timezone.utc))
    e.set_thumbnail(url=korisnik.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Balkan Muvanje™ 😏")
    await i.response.send_message(embed=e)

@bot.tree.command(name="crush", description="💘 Otkrij ko je tvoj tajni crush na serveru!")
async def crush(i: discord.Interaction):
    if await fun_cooldown(i, "crush"): return
    members = [m for m in i.guild.members if not m.bot and m.id != i.user.id]
    if not members:
        return await i.response.send_message(embed=em("❌", "Nema dovoljno članova!", color=COLORS["error"]), ephemeral=True)
    random.seed(i.user.id + i.guild.id)
    picked = random.choice(members)
    random.seed()
    poruke = [
        f"💘 Po zvijezdama i kafanskim računima, tvoj tajni crush je... **{picked.display_name}**! 😳",
        f"🔮 Kristalna kugla kaže: **{picked.display_name}** ti se sviđa više nego što priznaješ! 💕",
        f"💌 Baka bi rekla: 'Idi, pitaj ga/je na kafu!' — tvoj crush: **{picked.display_name}** ☕😍",
    ]
    e = discord.Embed(description=random.choice(poruke), color=COLORS["love"], timestamp=datetime.now(timezone.utc))
    e.set_thumbnail(url=picked.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Crush Otkrivač™ | Samo za zabavu!")
    await i.response.send_message(embed=e)

# ═══════════════════════════════════════════
#    OWO — ŽIVOTINJE SISTEM
# ═══════════════════════════════════════════
ANIMALS = {
    # ime: (emoji, rarity, power, value)
    "Riba":            ("🐟", "common",    1,   5),
    "Ptica":           ("🐦", "common",    1,   5),
    "Patka":           ("🦆", "common",    1,   6),
    "Kokoška":         ("🐔", "common",    1,   6),
    "Zec":             ("🐇", "common",    2,   8),
    "Vjeverica":       ("🐿️","common",    2,   8),
    "Gušter":          ("🦎", "common",    2,   8),
    "Puž":             ("🐌", "common",    1,   5),
    "Miš":             ("🐭", "common",    2,   7),
    "Lisica":          ("🦊", "uncommon",  5,  25),
    "Jazavac":         ("🦡", "uncommon",  4,  22),
    "Vuk":             ("🐺", "uncommon",  7,  40),
    "Rakun":           ("🦝", "uncommon",  5,  30),
    "Kornjača":        ("🐢", "uncommon",  3,  28),
    "Majmun":          ("🐒", "uncommon",  5,  32),
    "Medvjed":         ("🐻", "rare",     12,  90),
    "Lav":             ("🦁", "rare",     14, 110),
    "Tigar":           ("🐯", "rare",     13, 105),
    "Orao":            ("🦅", "rare",     10, 100),
    "Ajkula":          ("🦈", "rare",     13, 115),
    "Nilski konj":     ("🦛", "rare",     11,  95),
    "Zmaj":            ("🐉", "epic",     28, 320),
    "Jednorog":        ("🦄", "epic",     22, 270),
    "Krokodil":        ("🐊", "epic",     25, 290),
    "Gorila":          ("🦍", "epic",     20, 260),
    "Feniks":          ("🔥", "legendary",55, 900),
    "Morski Lav":      ("🌊", "legendary",50, 820),
    "Noćni Zmaj":      ("🐲", "legendary",60, 980),
    "Kristalni Jednorog":("💎","mythical",110,5000),
    "Dugin Feniks":    ("🌈", "mythical", 130,7000),
    "Nebeski Zmaj":    ("✨", "mythical", 150,9999),
}

RARITY_ORDER  = ["common","uncommon","rare","epic","legendary","mythical"]
RARITY_EMOJI  = {"common":"⚪","uncommon":"🟢","rare":"🔵","epic":"🟣","legendary":"🟡","mythical":"🌸"}
RARITY_COLORS = {"common":0x9B9B9B,"uncommon":0x2ECC71,"rare":0x3498DB,"epic":0x9B59B6,"legendary":0xF1C40F,"mythical":0xFF69B4}
RARITY_WEIGHTS= {"common":50,"uncommon":26,"rare":15,"epic":7,"legendary":2,"mythical":0.3}

HUNT_MISS = [
    "Ništa nisi uhvatio... životinja je pobjegla! 💨",
    "Prazne ruke! Vrati se kad si odmorniji. 😴",
    "Tišina u šumi... nema ničega danas. 🌲",
    "Promašio si! Trebao si ići lijevo. ⬅️",
    "Životinja te vidjela prije nego ti nju. 👀",
]

def pick_animal() -> str | None:
    if random.random() < 0.12:
        return None  # miss
    rarities = list(RARITY_WEIGHTS.keys())
    weights  = [RARITY_WEIGHTS[r] for r in rarities]
    chosen   = random.choices(rarities, weights=weights, k=1)[0]
    pool     = [n for n, (_, r, _, _) in ANIMALS.items() if r == chosen]
    return random.choice(pool) if pool else None

def zoo_power(uid) -> int:
    zoo  = get_zoo(uid)
    total = 0
    for name, cnt in zoo.items():
        if name in ANIMALS and cnt > 0:
            total += ANIMALS[name][2] * cnt
    return total

HUNT_COOLDOWNS: dict = {}

@bot.tree.command(name="hunt", description="🏹 Idi u lov na životinje! (kao owo hunt)")
async def hunt(i: discord.Interaction):
    now = time.time()
    last = HUNT_COOLDOWNS.get(i.user.id, 0)
    remaining = 7 - (now - last)
    if remaining > 0:
        return await i.response.send_message(
            embed=em("⏳ Previše si lovio!", f"Čekaj još `{remaining:.1f}s`", color=COLORS["warning"]),
            ephemeral=True
        )
    HUNT_COOLDOWNS[i.user.id] = now
    await i.response.defer()
    await asyncio.sleep(1.2)

    animal = pick_animal()
    if not animal:
        e = discord.Embed(description=f"🏹  {random.choice(HUNT_MISS)}", color=0x555555, timestamp=datetime.now(timezone.utc))
        e.set_footer(text=f"{BOT_NAME} {VERSION} • Pokušaj ponovo za 7s")
        return await i.followup.send(embed=e)

    emoji, rarity, power, value = ANIMALS[animal]
    zoo = get_zoo(i.user.id)
    zoo[animal] = zoo.get(animal, 0) + 1
    save_data()
    quest_progress(i.user.id, "hunt5")
    quest_progress(i.user.id, "hunt10")

    color = RARITY_COLORS[rarity]
    ri    = RARITY_EMOJI[rarity]
    e = discord.Embed(
        title=f"🏹  Uhvatio si životinje!",
        description=f"## {emoji}  {animal}\n{ri} **{rarity.capitalize()}**  ·  ⚔️ Snaga `{power}`",
        color=color,
        timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="🔢 Imaš ukupno", value=f"`{zoo[animal]}x {emoji} {animal}`", inline=True)
    e.add_field(name="💶 Vrijednost",   value=f"`{value} 💶`",                       inline=True)
    e.set_footer(text=f"{i.user.display_name} • {BOT_NAME} {VERSION}")
    await i.followup.send(embed=e)

@bot.tree.command(name="zoo", description="🦁 Pogledaj svoju zbirku životinja (kao owo zoo)")
async def zoo_cmd(i: discord.Interaction, korisnik: discord.Member = None):
    u   = korisnik or i.user
    zoo = get_zoo(u.id)
    if not zoo or all(v == 0 for v in zoo.values()):
        return await i.response.send_message(
            embed=em(f"🦁 {u.display_name} — Zoo", "Prazno! Idi u `/hunt` i uhvati neku životinje. 🏹", color=COLORS["info"]), ephemeral=True
        )

    sections = []
    for rarity in RARITY_ORDER:
        animals = [(n, cnt) for n, cnt in zoo.items() if n in ANIMALS and ANIMALS[n][1] == rarity and cnt > 0]
        if not animals:
            continue
        ri   = RARITY_EMOJI[rarity]
        rows = [f"{ANIMALS[n][0]} **{n}** `×{cnt}`" for n, cnt in sorted(animals)]
        sections.append(f"{ri} **{rarity.capitalize()}**\n" + "  ".join(rows))

    total   = sum(zoo.values())
    power   = zoo_power(u.id)
    e = discord.Embed(
        title=f"🦁 {u.display_name} — Zoo",
        description="\n\n".join(sections),
        color=COLORS["purple"],
        timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="📦 Ukupno",   value=f"`{total}` životinja", inline=True)
    e.add_field(name="⚔️ Snaga",    value=f"`{power}`",           inline=True)
    e.set_thumbnail(url=u.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

@bot.tree.command(name="battle", description="⚔️ Bori se sa nekim (kao owo battle)")
async def battle(i: discord.Interaction, korisnik: discord.Member):
    if korisnik.id == i.user.id:
        return await i.response.send_message(embed=em("❌", "Ne možeš se boriti sam sa sobom!", color=COLORS["error"]), ephemeral=True)
    if korisnik.bot:
        return await i.response.send_message(embed=em("❌", "Botovi ne znaju se boriti!", color=COLORS["error"]), ephemeral=True)

    await i.response.defer()
    await asyncio.sleep(2)

    p1 = zoo_power(i.user.id) + random.randint(1, 30)
    p2 = zoo_power(korisnik.id) + random.randint(1, 30)

    if p1 == p2:
        p1 += 1

    winner = i.user if p1 > p2 else korisnik
    loser  = korisnik if p1 > p2 else i.user
    wp, lp = (p1, p2) if p1 > p2 else (p2, p1)

    reward = random.randint(80, 300)
    get_economy(winner.id)["balance"] += reward
    save_data()

    bar_total = 20
    p1_fill = round((p1 / (p1 + p2)) * bar_total)
    p2_fill = bar_total - p1_fill
    bar = f"`{'█' * p1_fill}{'░' * p2_fill}`"

    e = discord.Embed(
        title="⚔️  BITKA!",
        description=(
            f"**{i.user.display_name}** vs **{korisnik.display_name}**\n"
            f"{bar}\n"
            f"⚔️ `{p1}` vs `{p2}` ⚔️"
        ),
        color=COLORS["gold"],
        timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="🏆 Pobjednik",  value=f"**{winner.mention}**",      inline=True)
    e.add_field(name="💀 Poražen",    value=f"{loser.mention}",           inline=True)
    e.add_field(name="💶 Nagrada",    value=f"`+{reward} 💶`",            inline=False)
    e.set_thumbnail(url=winner.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.followup.send(embed=e)

@bot.tree.command(name="sell", description="💰 Prodaj životinje iz zoo-a (kao owo sell)")
@app_commands.describe(zivotinja="Ime životinje (npr. Riba)", kolicina="Koliko prodaješ (default 1)")
async def sell(i: discord.Interaction, zivotinja: str, kolicina: int = 1):
    name = zivotinja.strip().capitalize()
    if name not in ANIMALS:
        names = ", ".join(f"`{n}`" for n in list(ANIMALS.keys())[:15])
        return await i.response.send_message(
            embed=em("❌ Nepoznata životinja", f"Provjeri `/zoo` za listu svojih životinja.\nPrimjeri: {names}", color=COLORS["error"]), ephemeral=True
        )
    zoo = get_zoo(i.user.id)
    owned = zoo.get(name, 0)
    if owned < kolicina or kolicina < 1:
        return await i.response.send_message(
            embed=em("❌ Nemaš dovoljno", f"Imaš samo `{owned}x {ANIMALS[name][0]} {name}`.", color=COLORS["error"]), ephemeral=True
        )
    emoji, rarity, power, value = ANIMALS[name]
    total_earn = value * kolicina
    zoo[name]  = owned - kolicina
    get_economy(i.user.id)["balance"] += total_earn
    save_data()
    await i.response.send_message(embed=em(
        f"💰 Prodato!",
        f"Prodao si `{kolicina}x {emoji} {name}` za **{total_earn} 💶**!",
        color=COLORS["success"],
        fields=[("🏦 Balans", f"`{get_economy(i.user.id)['balance']:,} 💶`", True)]
    ))

@bot.tree.command(name="animals", description="📋 Listu svih životinja i raritet (kao owo animals)")
async def animals_cmd(i: discord.Interaction):
    e = discord.Embed(title="📋 Sve životinje — Raritetna lista", color=COLORS["purple"], timestamp=datetime.now(timezone.utc))
    for rarity in RARITY_ORDER:
        ri    = RARITY_EMOJI[rarity]
        pool  = [(n, d[0], d[2], d[3]) for n, d in ANIMALS.items() if d[1] == rarity]
        lines = [f"{em2} **{n}** — ⚔️`{pw}` 💶`{val}`" for n, em2, pw, val in pool]
        e.add_field(name=f"{ri} {rarity.capitalize()}", value="\n".join(lines), inline=True)
    e.set_footer(text=f"{BOT_NAME} {VERSION} • /hunt za loviti!")
    await i.response.send_message(embed=e)

@bot.tree.command(name="pray", description="🙏 Pomoli se za nekoga (kao owo pray)")
async def pray(i: discord.Interaction, korisnik: discord.Member):
    if korisnik.id == i.user.id:
        return await i.response.send_message(embed=em("❌", "Ne možeš moliti za sebe!", color=COLORS["error"]), ephemeral=True)
    bonus = random.randint(20, 100)
    get_economy(korisnik.id)["balance"] += bonus
    save_data()
    msgs = [
        f"🙏 {i.user.mention} moli se za {korisnik.mention}! Nebo čuje — `+{bonus} 💶` palo s neba!",
        f"✨ {i.user.mention} šalje dobre vibracije {korisnik.mention}! `+{bonus} 💶` u džep!",
        f"🕊️ Zbog molitve {i.user.mention}, {korisnik.mention} je blagosloven sa `{bonus} 💶`!",
    ]
    e = discord.Embed(description=random.choice(msgs), color=0xFFD700, timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

@bot.tree.command(name="curse", description="😈 Prokuni nekoga (kao owo curse)")
async def curse(i: discord.Interaction, korisnik: discord.Member):
    if korisnik.id == i.user.id:
        return await i.response.send_message(embed=em("❌", "Ne možeš prokleti sebe!", color=COLORS["error"]), ephemeral=True)
    if korisnik.bot:
        return await i.response.send_message(embed=em("❌", "Botovi su imuni na kletvu! 🤖", color=COLORS["error"]), ephemeral=True)
    amount = random.randint(10, 80)
    target_eco = get_economy(korisnik.id)
    target_eco["balance"] = max(0, target_eco["balance"] - amount)
    save_data()
    msgs = [
        f"😈 {i.user.mention} baci kletvu na {korisnik.mention}! `-{amount} 💶` nestalo!",
        f"💀 Crna magija {i.user.mention} pogodila {korisnik.mention}! Izgubio `-{amount} 💶`!",
        f"🔮 {i.user.mention} izgovori drevnu kletvu! {korisnik.mention} izgubi `-{amount} 💶`!",
    ]
    e = discord.Embed(description=random.choice(msgs), color=0x8B0000, timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

# ═══════════════════════════════════════════
#    AUTO-MOD (Anti-Spam + Bad Words)
# ═══════════════════════════════════════════
SPAM_WINDOW = 5
SPAM_LIMIT  = 7
BAD_WORDS: set = set()  # add bad words here: BAD_WORDS = {"rijec1", "rijec2"}
user_msg_times: dict = defaultdict(deque)

# ── Anti-NSFW (pornografija, slike) ─────────────────────
# ⚠️  Psovke u tekstu su DOZVOLJENE — filtriramo samo NSFW linkove i slike

# Pornografski sajtovi — blokirani kao linkovi/embeds
NSFW_SITES = [
    "pornhub", "xvideos", "xnxx", "redtube", "youporn", "onlyfans",
    "rule34", "e-hentai", "xhamster", "spankbang", "chaturbate",
    "pornpics", "porn.com", "xtube", "4tube", "tube8", "sex.com",
]

# Eksplicitni nazivi fajlova (slike kurca/picke) — blokirani u uploadima
NSFW_FILENAMES = [
    "dick", "cock", "penis", "pussy", "vagina", "kurac", "picka", "pička",
    "pizda", "nude", "nudes", "naked", "cumshot", "blowjob", "anal",
    "hentai", "xxx", "porn", "nsfw", "boobs", "tits",
]

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".mov", ".avi", ".webm"}

# Sigurni domeni — GIF-ovi s ovih servisa su uvijek OK (Discord GIF picker, Tenor, Giphy)
SAFE_DOMAINS = (
    "tenor.com", "media.tenor.com", "tenor.googleapis.com",
    "giphy.com", "media.giphy.com", "media0.giphy.com",
    "media1.giphy.com", "media2.giphy.com",
    "cdn.discordapp.com", "media.discordapp.net",
    "discord.com/channels",
)

def _contains_nsfw_site(text: str) -> str | None:
    if not text: return None
    t = text.lower()
    for w in NSFW_SITES:
        if w in t:
            return w
    return None

def _contains_nsfw_filename(text: str) -> str | None:
    if not text: return None
    t = text.lower()
    for w in NSFW_FILENAMES:
        if w in t:
            return w
    return None

async def check_nsfw(message) -> bool:
    """Briše NSFW sadržaj (slike/linkovi). Vraća True ako je obrisao.
    NAPOMENA: Psovke u tekstu su DOZVOLJENE — ne filtriramo tekst poruke."""
    if message.channel.is_nsfw():  # NSFW kanal je dozvoljen
        return False
    found = None

    # 1) Pornografski sajtovi u tekstu/linkovima poruke
    found = _contains_nsfw_site(message.content)

    # 2) Attachmenti (slike/videi) — provjeri naziv fajla
    if not found:
        for att in message.attachments:
            # Discord CDN i sigurni servisi — uvijek OK
            if any(d in att.url.lower() for d in SAFE_DOMAINS):
                continue
            ext = _os.path.splitext(att.filename.lower())[1]
            if ext in IMAGE_EXTS:
                found = _contains_nsfw_filename(att.filename)
                if not found:
                    found = _contains_nsfw_site(att.url)
            if found: break

    # 3) Embeds — provjeri URL i title za NSFW sajtove
    # GIF-ovi sa Tenor/Giphy (Discord GIF picker) su uvijek OK
    if not found:
        for emb in message.embeds:
            url = emb.url or ""
            if any(d in url.lower() for d in SAFE_DOMAINS):
                continue  # Tenor / Giphy GIF — preskoci
            for field in [url, emb.title, emb.description]:
                if field and (found := _contains_nsfw_site(str(field))): break
            if found: break

    if not found: return False
    # OBRIŠI
    try:
        await message.delete()
    except: pass
    # Upozorenje korisniku
    try:
        await message.channel.send(
            embed=em("🔞 NSFW Sadržaj Zabranjen",
                     f"{message.author.mention} — pornografija/eksplicitan sadržaj nije dozvoljen!\n"
                     f"⚠️ Detektovano: `{found}`\n"
                     f"💡 Za NSFW koristi posebne **age-restricted** kanale.",
                     color=COLORS["error"]),
            delete_after=10
        )
    except: pass
    # Auto-warn + log
    try:
        await audit_log(message.guild, "🔞 Anti-NSFW",
                        f"{message.author.mention} pokušao slati NSFW u {message.channel.mention}\n**Trigger:** `{found}`")
    except: pass
    # 3+ NSFW = timeout 1h
    nsfw_strikes = data.setdefault("nsfw_strikes", {})
    skey = f"{message.guild.id}:{message.author.id}"
    nsfw_strikes[skey] = nsfw_strikes.get(skey, 0) + 1
    save_data()
    if nsfw_strikes[skey] >= 3:
        try:
            await message.author.timeout(timedelta(hours=1), reason="Anti-NSFW: 3+ pokušaja")
            await message.channel.send(
                embed=em("🔇 Timeout", f"{message.author.mention} dobio **1h timeout** zbog ponovljenog NSFW sadržaja!", color=COLORS["error"]),
                delete_after=15
            )
            nsfw_strikes[skey] = 0; save_data()
        except: pass
    return True

# ── Anti-Invite (drugi serveri) ─────────────────────────
INVITE_REGEX = re.compile(
    r"(?:"
    r"discord\s*\.\s*(?:gg|io|me|li)\s*\/\s*[a-zA-Z0-9-]+"
    r"|discord(?:app)?\s*\.\s*com\s*\/\s*invite\s*\/\s*[a-zA-Z0-9-]+"
    r"|dsc\s*\.\s*gg\s*\/\s*[a-zA-Z0-9-]+"
    r"|(?<![a-zA-Z0-9])\.gg\/[a-zA-Z0-9-]+"
    r")",
    re.I
)

async def check_automod(message) -> bool:
    if message.author.guild_permissions.administrator:
        return False
    # ── Anti-Invite filter ──────────────────────────
    if INVITE_REGEX.search(message.content):
        try:
            await message.delete()
            await message.channel.send(
                embed=em("🚫 Reklama zabranjena", f"{message.author.mention} — invite linkovi drugih servera nisu dozvoljeni!", color=COLORS["error"]),
                delete_after=8
            )
            await audit_log(message.guild, "🚫 Anti-Invite", f"{message.author.mention} pokušao reklamirati drugi server u {message.channel.mention}")
        except: pass
        return True
    content_lower = message.content.lower()
    for word in BAD_WORDS:
        if word in content_lower:
            try:
                await message.delete()
                await message.channel.send(
                    embed=em("🛡️ Auto-Mod", f"{message.author.mention} — zabranjene riječi!", color=COLORS["warning"]),
                    delete_after=5
                )
            except Exception:
                pass
            return True
    uid = message.author.id
    now = time.time()
    dq  = user_msg_times[uid]
    dq.append(now)
    while dq and dq[0] < now - SPAM_WINDOW:
        dq.popleft()
    if len(dq) >= SPAM_LIMIT:
        dq.clear()
        try:
            await message.author.timeout(timedelta(seconds=30), reason="Auto-Mod: Spam")
            await message.channel.send(
                embed=em("🛡️ Anti-Spam", f"{message.author.mention} dobio/la timeout od **30s** zbog spama! 🔇", color=COLORS["warning"]),
                delete_after=8
            )
        except Exception:
            pass
    return False

# ═══════════════════════════════════════════
#    BLACKJACK
# ═══════════════════════════════════════════
_RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
_VALS  = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
_SUITS = ['♠','♥','♦','♣']

def _new_deck():
    d = [(r, s) for r in _RANKS for s in _SUITS]
    random.shuffle(d)
    return d

def _bj_val(hand):
    val  = sum(_VALS[r] for r, _ in hand)
    aces = sum(1 for r, _ in hand if r == 'A')
    while val > 21 and aces:
        val -= 10; aces -= 1
    return val

def _bj_str(hand, hide=False):
    if hide:
        return f"`{hand[0][0]}{hand[0][1]}`  `🂠`"
    return "  ".join(f"`{r}{s}`" for r, s in hand)

def _bj_embed(player, dealer, oklada, note="", hide=True):
    e = discord.Embed(title="🃏 Blackjack", color=COLORS["dark"], timestamp=datetime.now(timezone.utc))
    e.add_field(name=f"Tvoje karte  ({_bj_val(player)})", value=_bj_str(player),         inline=False)
    e.add_field(name=f"Dealer  {'(?)' if hide else f'({_bj_val(dealer)})'}", value=_bj_str(dealer, hide), inline=False)
    if note:
        e.add_field(name="Rezultat", value=note, inline=False)
    e.set_footer(text=f"Oklada: {oklada:,} 💶 • {BOT_NAME}")
    return e

class BjView(discord.ui.View):
    def __init__(self, deck, player, dealer, oklada, uid):
        super().__init__(timeout=30)
        self.deck = deck; self.player = player; self.dealer = dealer
        self.oklada = oklada; self.uid = uid

    async def _finish(self, i, note, delta, color):
        eco = get_economy(self.uid)
        eco["balance"] = max(0, eco["balance"] + delta)
        save_data()
        self.clear_items()
        e = _bj_embed(self.player, self.dealer, self.oklada, note, hide=False)
        e.color = color
        await i.response.edit_message(embed=e, view=self)

    @discord.ui.button(label="Hit", emoji="🃏", style=discord.ButtonStyle.primary)
    async def hit(self, i: discord.Interaction, b):
        if i.user.id != self.uid:
            return await i.response.send_message("Ovo nije tvoja igra!", ephemeral=True)
        self.player.append(self.deck.pop())
        val = _bj_val(self.player)
        if val > 21:
            await self._finish(i, f"💥 **BUST!** Izgubio/la si `{self.oklada:,} 💶`", -self.oklada, COLORS["error"])
        elif val == 21:
            await self.stand.callback(self, i, b)
        else:
            await i.response.edit_message(embed=_bj_embed(self.player, self.dealer, self.oklada), view=self)

    @discord.ui.button(label="Stand", emoji="✋", style=discord.ButtonStyle.secondary)
    async def stand(self, i: discord.Interaction, b):
        if i.user.id != self.uid:
            return await i.response.send_message("Ovo nije tvoja igra!", ephemeral=True)
        while _bj_val(self.dealer) < 17:
            self.dealer.append(self.deck.pop())
        pv, dv = _bj_val(self.player), _bj_val(self.dealer)
        if dv > 21 or pv > dv:
            await self._finish(i, f"🏆 **Pobijedio/la si!** `+{self.oklada:,} 💶`", self.oklada, COLORS["success"])
        elif pv == dv:
            await self._finish(i, "🤝 **Nerješeno!** Oklada vraćena.", 0, COLORS["warning"])
        else:
            await self._finish(i, f"😢 **Dealer pobijedio!** `-{self.oklada:,} 💶`", -self.oklada, COLORS["error"])

    async def on_timeout(self):
        self.clear_items()

@bot.tree.command(name="blackjack", description="🃏 Igraj Blackjack protiv dilera!")
@app_commands.describe(oklada="Koliko 💶 ulažeš (min 10)")
async def blackjack(i: discord.Interaction, oklada: int):
    eco = get_economy(i.user.id)
    if oklada < 10:
        return await i.response.send_message(embed=em("❌", "Minimum oklada je `10 💶`!", color=COLORS["error"]), ephemeral=True)
    if eco["balance"] < oklada:
        return await i.response.send_message(embed=em("❌", f"Nemaš dovoljno! Imaš `{eco['balance']:,} 💶`.", color=COLORS["error"]), ephemeral=True)
    deck = _new_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    if _bj_val(player) == 21:
        won = int(oklada * 1.5)
        eco["balance"] += won
        save_data()
        e = _bj_embed(player, dealer, oklada, f"🎉 **BLACKJACK!** `+{won:,} 💶`!", hide=False)
        e.color = COLORS["gold"]
        return await i.response.send_message(embed=e)
    view = BjView(deck, player, dealer, oklada, i.user.id)
    await i.response.send_message(embed=_bj_embed(player, dealer, oklada), view=view)

# ═══════════════════════════════════════════
#    TRIVIA / KVIZ
# ═══════════════════════════════════════════
TRIVIA_QS = [
    ("Koji grad je glavni grad Bosne i Hercegovine?", "Sarajevo", ["Mostar","Banja Luka","Tuzla"]),
    ("Koja rijeka teče kroz Beograd?", "Sava", ["Dunav","Drina","Morava"]),
    ("U kojoj godini je Hrvatska ušla u EU?", "2013.", ["2007.","2004.","2015."]),
    ("Ko je napisao 'Na Drini ćuprija'?", "Ivo Andrić", ["Meša Selimović","Branko Ćopić","Dobrica Ćosić"]),
    ("Koliko država je nastalo raspadom Jugoslavije?", "6", ["5","7","4"]),
    ("Koji je najveći grad u Srbiji?", "Beograd", ["Novi Sad","Niš","Kragujevac"]),
    ("Koja je najpopularnija hrana u BiH?", "Ćevapi", ["Sarma","Burek","Pita"]),
    ("Koliko Grand Slam titula ima Novak Đoković?", "24", ["20","22","21"]),
    ("Koji planinski vrh je najviši u Bosni?", "Maglić", ["Bjelašnica","Jahorina","Treskavica"]),
    ("Koji grad je poznat po Guča trubačkom festivalu?", "Guča", ["Niš","Beograd","Čačak"]),
    ("Što znači 'merhaba' na bosanskom?", "Zdravo", ["Hvala","Molim","Doviđenja"]),
    ("Koja je zastava Srbije?", "Crvena, plava, bijela", ["Zelena, bijela, crvena","Plava, žuta, crvena","Bijela, zelena, plava"]),
    ("Koji je broj igrača u ekipi fudbala?", "11", ["10","12","9"]),
    ("Koja zemlja je domaćin Eurosonga 2024?", "Švicarska", ["Švedska","Italija","Hrvatska"]),
    ("Ko je pjevao 'Dragana' na Balkanu?", "Ceca", ["Lepa Brena","Jelena Karleuša","Zorana"]),
    ("Koji je glavni grad Hrvatske?", "Zagreb", ["Split","Rijeka","Osijek"]),
    ("Koliko km² ima Srbija?", "77,474", ["88,000","65,000","92,000"]),
    ("Šta je 'kajmak'?", "Mlječni proizvod", ["Vrsta sira","Vrsta mesa","Vrsta hljeba"]),
    ("Koji je najstariji grad na Balkanu?", "Plovdiv", ["Beograd","Sarajevo","Skoplje"]),
    ("Ko je 'Kralj Balkana' u košarci?", "Novak Đoković", ["Nikola Jokić","Goran Dragić","Predrag Stojaković"]),
]

class TriviaView(discord.ui.View):
    def __init__(self, correct, wrong, oklada, uid, pool=None, title="🧠 Balkan Trivia", combo=1, total_won=0):
        super().__init__(timeout=20)
        self.correct = correct; self.oklada = oklada; self.uid = uid
        self.pool = pool; self.title = title
        self.combo = combo; self.total_won = total_won
        opts = wrong[:3] + [correct]
        random.shuffle(opts)
        for opt in opts:
            btn = discord.ui.Button(label=opt[:80], style=discord.ButtonStyle.primary)
            btn.callback = self._make_cb(opt)
            self.add_item(btn)

    def _make_cb(self, choice):
        async def cb(i: discord.Interaction):
            if i.user.id != self.uid:
                return await i.response.send_message("Ovo nije tvoja igra!", ephemeral=True)
            self.clear_items()
            eco = get_economy(self.uid)
            if choice == self.correct:
                # combo multiplier — više tačnih = veća nagrada
                reward = int(self.oklada * self.combo)
                xp_gain = 25 * self.combo
                eco["balance"] += reward
                add_xp(self.uid, xp_gain); save_data()
                new_total = self.total_won + reward
                # nastavi sa novim pitanjem
                if self.pool:
                    q, c, w = random.choice(self.pool)
                    new_view = TriviaView(c, w, self.oklada, self.uid,
                                          pool=self.pool, title=self.title,
                                          combo=self.combo + 1, total_won=new_total)
                    e = discord.Embed(
                        title=self.title,
                        description=(
                            f"✅ **Tačno!** `+{reward:,} 💶` `+{xp_gain} XP`\n"
                            f"🔥 **Combo:** `x{self.combo}` → sljedeće `x{self.combo+1}`\n"
                            f"💰 **Ukupno osvojeno:** `{new_total:,} 💶`\n\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n\n"
                            f"**{q}**"
                        ),
                        color=COLORS["success"], timestamp=datetime.now(timezone.utc)
                    )
                    e.add_field(name="💶 Oklada", value=f"`{self.oklada}`", inline=True)
                    e.add_field(name="🔥 Combo", value=f"`x{self.combo+1}`", inline=True)
                    e.add_field(name="⏱️ Vrijeme", value="`20s`", inline=True)
                    e.set_footer(text=f"{BOT_NAME} • Nastavi nizom!")
                    return await i.response.edit_message(embed=e, view=new_view)
                # fallback bez pool-a
                result = em("✅ Tačno!", f"**{self.correct}**\n`+{reward} 💶` i `+{xp_gain} XP`!", color=COLORS["success"])
            else:
                eco["balance"] = max(0, eco["balance"] - self.oklada)
                save_data()
                desc = f"Tačan odgovor: **{self.correct}**\n`-{self.oklada} 💶`"
                if self.combo > 1:
                    desc += f"\n\n🔥 Combo prekinut na `x{self.combo}`!\n💰 Osvojeno u nizu: `{self.total_won:,} 💶`"
                result = em("❌ Netačno!", desc, color=COLORS["error"])
            await i.response.edit_message(embed=result, view=self)
        return cb

    async def on_timeout(self):
        self.clear_items()

@bot.tree.command(name="kviz", description="🧠 Odgovori na Balkan pitanje i osvoji pare!")
@app_commands.describe(oklada="Koliko 💶 ulažeš (default 50)")
async def kviz(i: discord.Interaction, oklada: int = 50):
    eco = get_economy(i.user.id)
    if oklada < 10:
        return await i.response.send_message(embed=em("❌", "Minimum je `10 💶`!", color=COLORS["error"]), ephemeral=True)
    if eco["balance"] < oklada:
        return await i.response.send_message(embed=em("❌", f"Nemaš dovoljno! Imaš `{eco['balance']:,} 💶`.", color=COLORS["error"]), ephemeral=True)
    question, correct, wrong = random.choice(TRIVIA_QS)
    view = TriviaView(correct, wrong, oklada, i.user.id, pool=TRIVIA_QS, title="🧠 Balkan Trivia")
    e = discord.Embed(title="🧠 Balkan Trivia", description=f"**{question}**", color=COLORS["purple"], timestamp=datetime.now(timezone.utc))
    e.add_field(name="💶 Oklada", value=f"`{oklada}`", inline=True)
    e.add_field(name="⏱️ Vrijeme", value="`20 sekundi`", inline=True)
    e.set_footer(text=f"{BOT_NAME} • Biraj pažljivo!")
    await i.response.send_message(embed=e, view=view)

# ═══════════════════════════════════════════
#    GEOGRAFIJA
# ═══════════════════════════════════════════
GEOGRAFIJA_QS = [
    # ── Balkan ──
    ("🇷🇸 Glavni grad Srbije?", "Beograd", ["Novi Sad", "Niš", "Kragujevac"]),
    ("🇭🇷 Glavni grad Hrvatske?", "Zagreb", ["Split", "Rijeka", "Osijek"]),
    ("🇧🇦 Glavni grad Bosne i Hercegovine?", "Sarajevo", ["Mostar", "Banja Luka", "Tuzla"]),
    ("🇲🇪 Glavni grad Crne Gore?", "Podgorica", ["Cetinje", "Nikšić", "Budva"]),
    ("🇲🇰 Glavni grad Sjeverne Makedonije?", "Skoplje", ["Bitola", "Ohrid", "Tetovo"]),
    ("🇸🇮 Glavni grad Slovenije?", "Ljubljana", ["Maribor", "Celje", "Koper"]),
    ("🇦🇱 Glavni grad Albanije?", "Tirana", ["Drač", "Skadar", "Vlora"]),
    ("🇧🇬 Glavni grad Bugarske?", "Sofija", ["Plovdiv", "Varna", "Burgas"]),
    ("🇬🇷 Glavni grad Grčke?", "Atina", ["Solun", "Patras", "Pirej"]),
    ("🇷🇴 Glavni grad Rumunije?", "Bukurešt", ["Kluž", "Brašov", "Temišvar"]),
    ("🇽🇰 Glavni grad Kosova?", "Priština", ["Prizren", "Peć", "Đakovica"]),
    ("Najduža rijeka kroz Srbiju?", "Dunav", ["Sava", "Morava", "Drina"]),
    ("Najviši vrh na Balkanu?", "Musala", ["Triglav", "Olimp", "Đeravica"]),
    ("U kojoj državi se nalazi Plitvička jezera?", "Hrvatska", ["BiH", "Slovenija", "Crna Gora"]),
    ("Koje more okružuje Crnu Goru?", "Jadransko", ["Egejsko", "Crno", "Sredozemno"]),
    ("Najveći grad u Bosni i Hercegovini?", "Sarajevo", ["Banja Luka", "Tuzla", "Mostar"]),
    ("Rijeka koja teče kroz Mostar?", "Neretva", ["Bosna", "Vrbas", "Una"]),
    ("Koja rijeka razdvaja Srbiju i Rumuniju?", "Dunav", ["Tisa", "Sava", "Drina"]),
    ("Najveće jezero na Balkanu?", "Skadarsko", ["Ohridsko", "Prespansko", "Plavsko"]),
    # ── Svijet ──
    ("Glavni grad Francuske?", "Pariz", ["Lion", "Marseilles", "Nica"]),
    ("Glavni grad Njemačke?", "Berlin", ["Minhen", "Hamburg", "Frankfurt"]),
    ("Glavni grad Italije?", "Rim", ["Milano", "Napulj", "Venecija"]),
    ("Glavni grad Španije?", "Madrid", ["Barcelona", "Sevilja", "Valensija"]),
    ("Glavni grad Engleske?", "London", ["Liverpul", "Mančester", "Oksford"]),
    ("Glavni grad SAD-a?", "Washington", ["New York", "Los Angeles", "Chicago"]),
    ("Glavni grad Rusije?", "Moskva", ["Sankt Peterburg", "Kazan", "Soči"]),
    ("Glavni grad Japana?", "Tokio", ["Kjoto", "Osaka", "Hirošima"]),
    ("Glavni grad Kine?", "Peking", ["Šangaj", "Hong Kong", "Guangžou"]),
    ("Glavni grad Australije?", "Canberra", ["Sydney", "Melbourne", "Perth"]),
    ("Glavni grad Brazila?", "Brasilia", ["Rio de Janeiro", "São Paulo", "Salvador"]),
    ("Glavni grad Argentine?", "Buenos Aires", ["Kordoba", "Rosario", "Mendoza"]),
    ("Glavni grad Egipta?", "Kairo", ["Aleksandrija", "Luksor", "Giza"]),
    ("Glavni grad Turske?", "Ankara", ["Istanbul", "Izmir", "Antalija"]),
    ("Najduža rijeka na svijetu?", "Nil", ["Amazon", "Misisipi", "Jangcekjang"]),
    ("Najviši vrh na svijetu?", "Mount Everest", ["K2", "Kangčendžunga", "Lhotse"]),
    ("Najveći okean?", "Tihi", ["Atlantski", "Indijski", "Arktički"]),
    ("Najveće jezero na svijetu?", "Kaspijsko", ["Bajkalsko", "Gornje", "Viktorijino"]),
    ("Najveći kontinent po površini?", "Azija", ["Afrika", "Sjeverna Amerika", "Evropa"]),
    ("Najveća pustinja na svijetu?", "Sahara", ["Gobi", "Kalahari", "Atakama"]),
    ("U kojoj zemlji je Eiffelov toranj?", "Francuska", ["Italija", "Njemačka", "Belgija"]),
    ("U kojoj zemlji je Coloseum?", "Italija", ["Grčka", "Španija", "Francuska"]),
    ("U kojoj zemlji se nalazi Statua slobode?", "SAD", ["Francuska", "Kanada", "Meksiko"]),
    ("Koja zemlja ima najviše stanovnika?", "Indija", ["Kina", "SAD", "Indonezija"]),
    ("Koliko kontinenata postoji?", "7", ["5", "6", "8"]),
    ("U kojem oceanu se nalaze Maldivi?", "Indijski", ["Tihi", "Atlantski", "Arktički"]),
    ("Glavni grad Holandije?", "Amsterdam", ["Hag", "Roterdam", "Utreht"]),
    ("Glavni grad Švicarske?", "Bern", ["Zurih", "Ženeva", "Bazel"]),
    ("Glavni grad Norveške?", "Oslo", ["Bergen", "Trondheim", "Stavanger"]),
    ("Glavni grad Švedske?", "Stockholm", ["Geteborg", "Malme", "Upsala"]),
    ("Glavni grad Finske?", "Helsinki", ["Tampere", "Turku", "Espoo"]),
]

@bot.tree.command(name="geografija", description="🌍 Geografski kviz — pogodi i osvoji pare!")
@app_commands.describe(oklada="Koliko 💶 ulažeš (default 50)")
async def geografija(i: discord.Interaction, oklada: int = 50):
    eco = get_economy(i.user.id)
    if oklada < 10:
        return await i.response.send_message(embed=em("❌", "Minimum je `10 💶`!", color=COLORS["error"]), ephemeral=True)
    if eco["balance"] < oklada:
        return await i.response.send_message(embed=em("❌", f"Nemaš dovoljno! Imaš `{eco['balance']:,} 💶`.", color=COLORS["error"]), ephemeral=True)
    question, correct, wrong = random.choice(GEOGRAFIJA_QS)
    view = TriviaView(correct, wrong, oklada, i.user.id, pool=GEOGRAFIJA_QS, title="🌍 Geografija")
    e = discord.Embed(title="🌍 Geografija", description=f"**{question}**", color=COLORS["info"], timestamp=datetime.now(timezone.utc))
    e.add_field(name="💶 Oklada", value=f"`{oklada}`", inline=True)
    e.add_field(name="⏱️ Vrijeme", value="`20 sekundi`", inline=True)
    e.set_footer(text=f"{BOT_NAME} • Putuj svijetom!")
    await i.response.send_message(embed=e, view=view)

# ═══════════════════════════════════════════
#    KOCKA (DICE)
# ═══════════════════════════════════════════
_DICE_FACES = {1:"⚀",2:"⚁",3:"⚂",4:"⚃",5:"⚄",6:"⚅"}

@bot.tree.command(name="kocka", description="🎲 Baci kocku protiv nekoga!")
@app_commands.describe(korisnik="Tvoj protivnik", oklada="Koliko 💶 ulažeš")
async def kocka(i: discord.Interaction, korisnik: discord.Member, oklada: int = 100):
    if korisnik.id == i.user.id or korisnik.bot:
        return await i.response.send_message(embed=em("❌", "Ne možeš igrati sam ili sa botom!", color=COLORS["error"]), ephemeral=True)
    e1 = get_economy(i.user.id); e2 = get_economy(korisnik.id)
    if e1["balance"] < oklada:
        return await i.response.send_message(embed=em("❌", f"Nemaš dovoljno! Imaš `{e1['balance']:,} 💶`.", color=COLORS["error"]), ephemeral=True)
    if e2["balance"] < oklada:
        return await i.response.send_message(embed=em("❌", f"{korisnik.display_name} nema dovoljno para!", color=COLORS["error"]), ephemeral=True)
    await i.response.defer()
    await asyncio.sleep(1.5)
    d1 = random.randint(1, 6); d2 = random.randint(1, 6)
    while d1 == d2:
        d2 = random.randint(1, 6)
    winner = i.user if d1 > d2 else korisnik
    loser  = korisnik if d1 > d2 else i.user
    get_economy(winner.id)["balance"] += oklada
    get_economy(loser.id)["balance"]   = max(0, get_economy(loser.id)["balance"] - oklada)
    save_data()
    e = discord.Embed(
        title="🎲 Kocka!",
        description=(
            f"{i.user.mention} {_DICE_FACES[d1]} **{d1}** vs **{d2}** {_DICE_FACES[d2]} {korisnik.mention}\n\n"
            f"🏆 **{winner.mention}** pobijedio/la! `+{oklada:,} 💶`"
        ),
        color=COLORS["gold"], timestamp=datetime.now(timezone.utc)
    )
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.followup.send(embed=e)

# ═══════════════════════════════════════════
#    SHOP + KUPI
# ═══════════════════════════════════════════
SHOP_ITEMS = {
    "lucky_hunter": {"name": "🍀 Srećni Lovac", "desc":"2× šansa za lov na životinju (1h)",  "price":800,  "duration":3600},
    "xp_boost":     {"name": "⚡ XP Boost",      "desc":"2× XP od poruka (1h)",               "price":1000, "duration":3600},
    "shield":       {"name": "🛡️ Štit",         "desc":"Zaštita od krađe (24h)",             "price":600,  "duration":86400},
    "double_steal": {"name": "💣 Bomba",         "desc":"Sljedeća krađa donosi duplo",        "price":400,  "duration":None},
    "daily_boost":  {"name": "📅 Daily Boost",   "desc":"+500 💶 bonusa na sljedeći /daily",  "price":350,  "duration":None},
}

def get_items(uid):
    eco = get_economy(uid)
    eco.setdefault("items", {})
    return eco["items"]

def has_item(uid, key):
    items = get_items(uid)
    if key not in items:
        return False
    item = SHOP_ITEMS.get(key, {})
    if item.get("duration"):
        if time.time() > items[key]:
            del items[key]; return False
        return True
    return bool(items.get(key))

@bot.tree.command(name="shop", description="🛒 Pogledaj šta možeš kupiti")
async def shop(i: discord.Interaction):
    e = discord.Embed(title="🛒 GIANNI Shop", description="Kupi predmete sa `/kupi <id>` komandom:", color=COLORS["purple"], timestamp=datetime.now(timezone.utc))
    for key, item in SHOP_ITEMS.items():
        dur = "Jednom" if not item["duration"] else f"{item['duration']//3600}h" if item["duration"] >= 3600 else f"{item['duration']//60}min"
        e.add_field(name=item["name"], value=f"**ID:** `{key}`\n{item['desc']}\n⏳ `{dur}` • 💶 `{item['price']:,}`", inline=True)
    e.set_footer(text=f"{BOT_NAME} • /kupi <id> za kupovinu")
    await i.response.send_message(embed=e)

@bot.tree.command(name="kupi", description="💳 Kupi predmet iz shopa")
@app_commands.describe(predmet="ID predmeta iz /shop")
async def kupi(i: discord.Interaction, predmet: str):
    if predmet not in SHOP_ITEMS:
        return await i.response.send_message(embed=em("❌", "Nepoznat predmet! Provjeri `/shop` za listu.", color=COLORS["error"]), ephemeral=True)
    item = SHOP_ITEMS[predmet]
    eco  = get_economy(i.user.id)
    if eco["balance"] < item["price"]:
        return await i.response.send_message(embed=em("❌", f"Nemaš dovoljno! Trebaš `{item['price']:,} 💶`.", color=COLORS["error"]), ephemeral=True)
    eco["balance"] -= item["price"]
    items = get_items(i.user.id)
    items[predmet] = (time.time() + item["duration"]) if item["duration"] else True
    save_data()
    await i.response.send_message(embed=em_pro(
        f"✅ Kupovina Uspješna",
        f"🎁 Nabavio si **{item['name']}**!\n*{item['desc']}*",
        color=COLORS["success"], author=i.user, thumb=i.user.display_avatar.url, fields=[
            ("💸 Cijena", f"```diff\n- {item['price']:,} 💶\n```", True),
            ("🏦 Balans", f"```yaml\n{eco['balance']:,} 💶\n```", True),
        ]
    ))

# ═══════════════════════════════════════════
#    QUESTS / DNEVNI ZADACI
# ═══════════════════════════════════════════
QUEST_POOL = [
    {"id":"hunt5",   "name": "🏹 Lovac",      "desc":"Ulovi 5 životinja",           "target":5,  "reward":200},
    {"id":"work3",   "name": "💼 Radnik",      "desc":"Radi posao 3 puta",           "target":3,  "reward":300},
    {"id":"msgs20",  "name": "💬 Pričalo",     "desc":"Pošalji 20 poruka",           "target":20, "reward":150},
    {"id":"bj_win",  "name": "🃏 Kockar",      "desc":"Pobijedi u Blackjacku",       "target":1,  "reward":500},
    {"id":"kviz3",   "name": "🧠 Znalac",      "desc":"Tačno odgovori na 3 kviz pitanja","target":3,"reward":400},
    {"id":"hunt10",  "name": "🎯 Pro Lovac",   "desc":"Ulovi 10 životinja",          "target":10, "reward":500},
    {"id":"daily1",  "name": "📅 Redovan",     "desc":"Uzmi /daily nagradu",         "target":1,  "reward":250},
]

def get_quests(uid):
    key   = str(uid)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    data["quests"].setdefault(key, {})
    if data["quests"][key].get("date") != today:
        chosen = random.sample(QUEST_POOL, 3)
        data["quests"][key] = {
            "date":     today,
            "assigned": [q["id"] for q in chosen],
            "progress": {q["id"]: 0 for q in chosen},
            "done":     {q["id"]: False for q in chosen},
        }
    return data["quests"][key]

def quest_progress(uid, quest_id, amount=1):
    qd = get_quests(uid)
    if quest_id not in qd["progress"] or qd["done"].get(quest_id):
        return None
    qd["progress"][quest_id] += amount
    quest = next((q for q in QUEST_POOL if q["id"] == quest_id), None)
    if quest and qd["progress"][quest_id] >= quest["target"]:
        qd["done"][quest_id] = True
        get_economy(uid)["balance"] += quest["reward"]
        save_data()
        return quest
    save_data()
    return None

@bot.tree.command(name="quests", description="📋 Pogledaj svoje dnevne zadatke")
async def quests_cmd(i: discord.Interaction):
    qd    = get_quests(i.user.id)
    save_data()
    lines = []
    for qid in qd["assigned"]:
        quest = next(q for q in QUEST_POOL if q["id"] == qid)
        prog  = qd["progress"].get(qid, 0)
        done  = qd["done"].get(qid, False)
        check = "✅" if done else "⬜"
        fill  = min(prog, quest["target"])
        bar   = f"`{'█' * fill}{'░' * (quest['target'] - fill)}`"
        lines.append(f"{check} **{quest['name']}** — {quest['desc']}\n{bar} `{prog}/{quest['target']}` • 💶 `+{quest['reward']}`")
    done_count = sum(1 for qid in qd["assigned"] if qd["done"].get(qid))
    e = discord.Embed(
        title="📋 Dnevni Zadaci",
        description="\n\n".join(lines),
        color=COLORS["info"], timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="✅ Završeno", value=f"`{done_count}/3`", inline=True)
    e.set_footer(text=f"Resetuju se u ponoć UTC • {BOT_NAME}")
    await i.response.send_message(embed=e)

# ═══════════════════════════════════════════
#    GIVEAWAY
# ═══════════════════════════════════════════
active_giveaways: dict = {}

class GiveawayView(discord.ui.View):
    def __init__(self, msg_id=None):
        super().__init__(timeout=None)
        self.msg_id = msg_id

    @discord.ui.button(label="Učestvuj", emoji="🎉", style=discord.ButtonStyle.success, custom_id="ga_enter")
    async def enter(self, i: discord.Interaction, b):
        ga = active_giveaways.get(self.msg_id)
        if not ga:
            return await i.response.send_message("Nagradna igra je završena!", ephemeral=True)
        if i.user.id in ga["entrants"]:
            ga["entrants"].discard(i.user.id)
            await i.response.send_message("Odjavljen/a si sa nagradne igre.", ephemeral=True)
        else:
            ga["entrants"].add(i.user.id)
            await i.response.send_message("✅ Prijavljen/a si! Sretno! 🍀", ephemeral=True)
        try:
            msg = await i.channel.fetch_message(self.msg_id)
            e   = msg.embeds[0]
            e.set_field_at(1, name="👥 Učesnici", value=f"`{len(ga['entrants'])}`", inline=True)
            await msg.edit(embed=e)
        except Exception:
            pass

giveaway_group = app_commands.Group(name="giveaway", description="🎉 Nagradne igre")

@giveaway_group.command(name="start", description="🎉 Pokreni nagradnu igru")
@app_commands.describe(nagrada="Šta se osvaja", minuta="Koliko minuta traje", kanal="Kanal (default ovaj)")
@app_commands.default_permissions(manage_guild=True)
@app_commands.checks.has_permissions(manage_guild=True)
async def giveaway_start(i: discord.Interaction, nagrada: str, minuta: int = 60, kanal: discord.TextChannel = None):
    chan = kanal or i.channel
    end  = datetime.now(timezone.utc) + timedelta(minutes=minuta)
    e = discord.Embed(
        title="🎉 NAGRADNA IGRA!",
        description=f"## 🏆  {nagrada}\n\nKlikni dugme da se prijaviš!",
        color=COLORS["gold"], timestamp=end
    )
    e.add_field(name="⏰ Kraj",       value=f"<t:{int(end.timestamp())}:R>", inline=True)
    e.add_field(name="👥 Učesnici",  value="`0`",                            inline=True)
    e.add_field(name="🎟️ Domaćin",  value=i.user.mention,                  inline=True)
    e.set_footer(text=f"Završava se • {BOT_NAME}")
    await i.response.send_message("✅ Nagradna igra pokrenuta!", ephemeral=True)
    msg = await chan.send(embed=e)
    ga  = {"entrants": set(), "prize": nagrada, "channel_id": chan.id, "msg_id": msg.id}
    active_giveaways[msg.id] = ga
    await msg.edit(view=GiveawayView(msg.id))
    await asyncio.sleep(minuta * 60)
    await _end_giveaway(msg.id, chan)

@giveaway_group.command(name="end", description="🏁 Završi nagradnu igru odmah")
@app_commands.default_permissions(manage_guild=True)
@app_commands.checks.has_permissions(manage_guild=True)
async def giveaway_end(i: discord.Interaction):
    for mid, ga in list(active_giveaways.items()):
        if ga["channel_id"] == i.channel_id:
            await i.response.send_message("Završavam nagradnu igru...", ephemeral=True)
            await _end_giveaway(mid, i.channel)
            return
    await i.response.send_message("Nema aktivnih nagradnih igara u ovom kanalu!", ephemeral=True)

async def _end_giveaway(msg_id, channel):
    ga = active_giveaways.pop(msg_id, None)
    if not ga: return
    try: msg = await channel.fetch_message(msg_id)
    except: return
    if not ga["entrants"]:
        e = discord.Embed(title="🎉 Nagradna igra završena", description="Niko se nije prijavio! 😢", color=COLORS["error"])
        await msg.edit(embed=e, view=None); return
    winner_id = random.choice(list(ga["entrants"]))
    winner    = channel.guild.get_member(winner_id)
    e = discord.Embed(
        title="🎉 Nagradna igra ZAVRŠENA!",
        description=f"## 🏆 {ga['prize']}\n\n🥳 Pobjednik: **{winner.mention if winner else f'<@{winner_id}>'}**!",
        color=COLORS["gold"], timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="👥 Učesnici", value=f"`{len(ga['entrants'])}`", inline=True)
    e.set_footer(text=f"{BOT_NAME} • Čestitamo!")
    await msg.edit(embed=e, view=None)
    await channel.send(f"🎊 Čestitamo {winner.mention if winner else f'<@{winner_id}>'}! Pobijedio/la si **{ga['prize']}**! 🏆")

bot.tree.add_command(giveaway_group)

# ═══════════════════════════════════════════
#    🔄 RESET GIVEAWAY (5 min)
# ═══════════════════════════════════════════
@bot.tree.command(name="reset-gw", description="🔄 [ADMIN] Resetuj i ponovo pokreni giveaway za 5 minuta")
@app_commands.describe(nagrada="Nagrada za novi giveaway", kanal="Kanal (default ovaj)")
@app_commands.default_permissions(manage_guild=True)
@app_commands.checks.has_permissions(manage_guild=True)
async def reset_gw_cmd(i: discord.Interaction, nagrada: str, kanal: discord.TextChannel = None):
    chan = kanal or i.channel
    for mid, ga in list(active_giveaways.items()):
        if ga["channel_id"] == chan.id:
            active_giveaways.pop(mid, None)
    sep = "═══════════════════════════"
    countdown_e = discord.Embed(
        title="🔄 ɢɪᴠᴇᴀᴡᴀʏ ʀᴇꜱᴇᴛ!",
        description=(
            f"```ansi\n\u001b[1;36m{sep}\u001b[0m\n```"
            f"⏳ **Novi giveaway počinje za 5 minuta!**\n\n"
            f"```yaml\n"
            f"Nagrada  : {nagrada}\n"
            f"Kanal    : #{chan.name}\n"
            f"Pokrece  : {i.user.display_name}\n"
            f"```"
        ),
        color=COLORS["aqua"], timestamp=datetime.now(timezone.utc)
    )
    countdown_e.set_footer(text=f"🎉 {BOT_NAME} • Giveaway Reset")
    await i.response.send_message(embed=countdown_e)
    await asyncio.sleep(300)
    end = datetime.now(timezone.utc) + timedelta(minutes=60)
    ga_e = discord.Embed(
        title="🎉 NAGRADNA IGRA!",
        description=f"## 🏆  {nagrada}\n\nKlikni dugme da se prijaviš!",
        color=COLORS["gold"], timestamp=end
    )
    ga_e.add_field(name="⏰ Kraj",      value=f"<t:{int(end.timestamp())}:R>", inline=True)
    ga_e.add_field(name="👥 Učesnici", value="`0`",                            inline=True)
    ga_e.add_field(name="🎟️ Domaćin", value=i.user.mention,                  inline=True)
    ga_e.set_footer(text=f"Završava se • {BOT_NAME}")
    msg = await chan.send(embed=ga_e)
    ga = {"entrants": set(), "prize": nagrada, "channel_id": chan.id, "msg_id": msg.id}
    active_giveaways[msg.id] = ga
    await msg.edit(view=GiveawayView(msg.id))
    await asyncio.sleep(3600)
    await _end_giveaway(msg.id, chan)

# ═══════════════════════════════════════════
#    💰 OWNER-ONLY: DODAJ / ODUZMI NOVAC
# ═══════════════════════════════════════════
@bot.tree.command(name="dodaj-novac", description="💰 [OWNER] Dodaj coina korisniku")
@app_commands.describe(korisnik="Kome dodajemo", iznos="Koliko coina")
async def dodaj_novac(i: discord.Interaction, korisnik: discord.Member, iznos: int):
    if i.user.id not in OWNER_IDS:
        return await i.response.send_message(
            embed=em("⛔ Zabranjen pristup!", "Ova komanda je samo za **Vlasnika** bota.", color=COLORS["error"]),
            ephemeral=True
        )
    if iznos <= 0:
        return await i.response.send_message(embed=em("❌", "Iznos mora biti pozitivan!", color=COLORS["error"]), ephemeral=True)
    eco = get_economy(korisnik.id)
    eco["balance"] += iznos
    save_data()
    await i.response.send_message(embed=discord.Embed(
        title="💰 ᴅᴏᴅᴀɴᴏ ᴄᴏɪɴᴀ!",
        description=(
            f"```yaml\n"
            f"Korisnik : {korisnik.display_name}\n"
            f"Dodano   : +{iznos:,} coina\n"
            f"Novi bal : {eco['balance']:,} coina\n"
            f"Vlasnik  : {i.user.display_name}\n"
            f"```"
        ),
        color=COLORS["aqua"], timestamp=datetime.now(timezone.utc)
    ).set_footer(text=f"💰 {BOT_NAME} • Owner Komanda"), ephemeral=True)

@bot.tree.command(name="oduzmi-novac", description="💸 [OWNER] Oduzmi coina korisniku")
@app_commands.describe(korisnik="Kome oduzimamo", iznos="Koliko coina")
async def oduzmi_novac(i: discord.Interaction, korisnik: discord.Member, iznos: int):
    if i.user.id not in OWNER_IDS:
        return await i.response.send_message(
            embed=em("⛔ Zabranjen pristup!", "Ova komanda je samo za **Vlasnika** bota.", color=COLORS["error"]),
            ephemeral=True
        )
    if iznos <= 0:
        return await i.response.send_message(embed=em("❌", "Iznos mora biti pozitivan!", color=COLORS["error"]), ephemeral=True)
    eco = get_economy(korisnik.id)
    eco["balance"] = max(0, eco["balance"] - iznos)
    save_data()
    await i.response.send_message(embed=discord.Embed(
        title="💸 ᴏᴅᴜᴢᴇᴛᴏ ᴄᴏɪɴᴀ!",
        description=(
            f"```yaml\n"
            f"Korisnik : {korisnik.display_name}\n"
            f"Oduzeto  : -{iznos:,} coina\n"
            f"Novi bal : {eco['balance']:,} coina\n"
            f"Vlasnik  : {i.user.display_name}\n"
            f"```"
        ),
        color=COLORS["warning"], timestamp=datetime.now(timezone.utc)
    ).set_footer(text=f"💸 {BOT_NAME} • Owner Komanda"), ephemeral=True)

# ═══════════════════════════════════════════
#    POLL / GLASANJE
# ═══════════════════════════════════════════
@bot.tree.command(name="poll", description="📊 Napravi glasanje sa reakcijama")
@app_commands.describe(pitanje="Pitanje", opcija1="1. opcija", opcija2="2. opcija", opcija3="3. opcija (opcionalno)", opcija4="4. opcija (opcionalno)")
async def poll(i: discord.Interaction, pitanje: str, opcija1: str, opcija2: str, opcija3: str = None, opcija4: str = None):
    opts   = [o for o in [opcija1, opcija2, opcija3, opcija4] if o]
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣"]
    desc   = "\n".join(f"{emojis[idx]}  **{opt}**" for idx, opt in enumerate(opts))
    e = discord.Embed(title=f"📊 {pitanje}", description=desc, color=COLORS["info"], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"Glasaj sa emoji reakcijama • {BOT_NAME}")
    e.set_author(name=i.user.display_name, icon_url=i.user.display_avatar.url)
    await i.response.send_message(embed=e)
    msg = await i.original_response()
    for idx in range(len(opts)):
        await msg.add_reaction(emojis[idx])

# ═══════════════════════════════════════════
#    TICKET SISTEM
# ═══════════════════════════════════════════
class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Zatvori Ticket", emoji="🔒", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    async def close(self, i: discord.Interaction, b):
        await i.response.send_message("🔒 Ticket se zatvara za 5 sekundi...", ephemeral=False)
        await asyncio.sleep(5)
        try:
            await i.channel.delete(reason=f"Ticket zatvorio {i.user}")
        except discord.Forbidden:
            await i.channel.send("❌ Nemam permisiju da obrišem kanal. Obriši ručno.")
        except Exception:
            pass

class TicketOpenView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Otvori Ticket", emoji="🎫", style=discord.ButtonStyle.primary, custom_id="ticket_open")
    async def open_ticket(self, i: discord.Interaction, b):
        await i.response.defer(ephemeral=True)
        guild    = i.guild
        safe_name = "".join(c for c in i.user.name.lower() if c.isalnum() or c in "-_")[:20] or str(i.user.id)
        existing  = discord.utils.get(guild.text_channels, name=f"ticket-{safe_name}")
        if existing:
            return await i.followup.send(f"Već imaš otvoren ticket: {existing.mention}", ephemeral=True)

        # Check bot has Manage Channels
        if not guild.me.guild_permissions.manage_channels:
            return await i.followup.send("❌ Bot nema **Manage Channels** permisiju. Daj mu je u Server Settings!", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            i.user:             discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me:           discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True),
        }
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        try:
            # Try to put tickets in a "tickets" category if it exists
            category = discord.utils.get(guild.categories, name="Tickets") or \
                       discord.utils.get(guild.categories, name="tickets")
            chan = await guild.create_text_channel(
                f"ticket-{safe_name}",
                overwrites=overwrites,
                category=category,
                reason=f"Ticket od {i.user}",
                topic=f"Ticket od {i.user} ({i.user.id})"
            )
        except discord.Forbidden:
            return await i.followup.send("❌ Bot nema permisiju da kreira kanale! Dodaj **Manage Channels** u server settings.", ephemeral=True)
        except Exception as ex:
            return await i.followup.send(f"❌ Greška: `{ex}`", ephemeral=True)

        e = discord.Embed(
            title="🎫 Ticket Otvoren",
            description=(
                f"Zdravo {i.user.mention}! 👋\n\n"
                f"Opiši problem ili pitanje i tim će ti odgovoriti uskoro. 🙏\n\n"
                f"Kad završiš, klikni **Zatvori Ticket** ispod."
            ),
            color=COLORS["info"], timestamp=datetime.now(timezone.utc)
        )
        e.set_thumbnail(url=i.user.display_avatar.url)
        e.set_footer(text=f"{BOT_NAME} • Ticket Sistem")
        await chan.send(content=i.user.mention, embed=e, view=TicketCloseView())
        await i.followup.send(f"✅ Ticket otvoren: {chan.mention}", ephemeral=True)

@bot.tree.command(name="ticket-setup", description="🎫 Postavi ticket sistem u ovaj kanal")
@app_commands.default_permissions(manage_channels=True)
@app_commands.checks.has_permissions(administrator=True)
async def ticket_setup(i: discord.Interaction):
    # Respond FIRST, then send the panel
    await i.response.defer(ephemeral=True)

    # Check bot permissions
    missing = []
    perms = i.guild.me.guild_permissions
    if not perms.manage_channels: missing.append("`Manage Channels`")
    if not perms.manage_roles:    missing.append("`Manage Roles`")
    if not perms.send_messages:   missing.append("`Send Messages`")
    if missing:
        return await i.followup.send(
            f"❌ Botu nedostaju permisije: {', '.join(missing)}\n"
            f"Dodaj ih u **Server Settings → Roles → GIANNI (Custom Game Vanity)** (bot) pa pokušaj ponovo.",
            ephemeral=True
        )

    e = discord.Embed(
        title="🎫 Sistem Podrške",
        description=(
            "Imaš problem ili pitanje? Klikni dugme ispod!\n\n"
            "Otvorit će ti se privatni kanal sa timom.\n"
            "Odgovorit ćemo što prije! 🙏"
        ),
        color=COLORS["info"], timestamp=datetime.now(timezone.utc)
    )
    if i.guild.icon:
        e.set_thumbnail(url=i.guild.icon.url)
    e.set_footer(text=f"{BOT_NAME} • Ticket Sistem")
    try:
        await i.channel.send(embed=e, view=TicketOpenView())
        await i.followup.send("✅ Ticket sistem postavljen uspješno!", ephemeral=True)
    except discord.Forbidden:
        await i.followup.send("❌ Nemam permisiju da pišem u ovaj kanal!", ephemeral=True)

# ═══════════════════════════════════════════
#    SETUP ROLES — GIANNI
# ═══════════════════════════════════════════
PERM_ADMIN = discord.Permissions(administrator=True)
PERM_MOD = discord.Permissions(
    ban_members=True, kick_members=True,
    manage_messages=True, moderate_members=True,
    view_channel=True, send_messages=True,
    read_message_history=True, manage_threads=True
)
PERM_MEMBER = discord.Permissions(
    view_channel=True, send_messages=True,
    read_message_history=True, connect=True, speak=True,
    attach_files=True, embed_links=True, add_reactions=True
)
PERM_BOT = discord.Permissions(
    view_channel=True, send_messages=True,
    read_message_history=True, manage_messages=True,
    embed_links=True, attach_files=True, add_reactions=True,
    connect=True, speak=True
)
PERM_BASIC = discord.Permissions(
    view_channel=True, send_messages=True,
    read_message_history=True, add_reactions=True
)
PERM_VOICE = discord.Permissions(
    view_channel=True, connect=True, speak=True,
    use_voice_activation=True, stream=True
)

GIANNI_ROLES = [
    # ═══ JEDINA ULOGA SA POWER-OM (ban/kick/admin) ═══
    {"name": "〢 /GIANNI",                     "color": discord.Color.from_str("#FFD700"), "permissions": PERM_ADMIN,  "hoist": True,  "desc": "Glavni admin — ban/kick/sve"},
    # ═══ DEKORATIVNE TOP ULOGE ═══
    {"name": "〢 Cryptid Gianni ( Vlasnik )", "color": discord.Color.from_str("#FF3B3B"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Vlasnik (dekorativna)"},
    {"name": "〢 High Masculinity",            "color": discord.Color.from_str("#1F2A44"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "High Masculinity"},
    {"name": "〢 Cristal De Gianni",           "color": discord.Color.from_str("#A569FF"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Cristal De Gianni"},
    {"name": "〢 Toxic Command ™",             "color": discord.Color.from_str("#00E676"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Toxic Command"},
    # ═══ STAFF (dekorativno) ═══
    {"name": "〢 Owners",                      "color": discord.Color.from_str("#FFC400"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Vlasnici"},
    {"name": "〢 Founders",                    "color": discord.Color.from_str("#FF8A00"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Osnivači"},
    {"name": "〢 Creators",                    "color": discord.Color.from_str("#5DADE2"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Kreatori"},
    {"name": "〢 Administrator",               "color": discord.Color.from_str("#EC407A"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Administrator (dekorativna)"},
    {"name": "〢 Hello Kitty Moderator",       "color": discord.Color.from_str("#FF85C8"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Hello Kitty Moderator"},
    {"name": "〢 Moderator",                   "color": discord.Color.from_str("#42A5F5"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Moderator (dekorativna)"},
    {"name": "〢 StaffTeam",                   "color": discord.Color.from_str("#26C6A4"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Staff Team"},
    # ═══ SPECIJALNE ULOGE ═══
    {"name": "〢 Mjauch",                      "color": discord.Color.from_str("#FF9ECF"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Mjauch ✨"},
    {"name": "〢 Samo Njoj",                   "color": discord.Color.from_str("#FF4FA3"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Samo Njoj"},
    {"name": "〢 Girly Pop",                   "color": discord.Color.from_str("#FFB7D5"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Girly Pop"},
    {"name": "〢 Slay Queen",                  "color": discord.Color.from_str("#E91EFF"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Slay Queen"},
    {"name": "〢 67 Pookie",                   "color": discord.Color.from_str("#C58CFF"), "permissions": PERM_MEMBER, "hoist": False, "desc": "67 Pookie"},
    {"name": "〢 Sexy",                        "color": discord.Color.from_str("#D81B60"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Sexy"},
    {"name": "〢 Hello Kitty",                 "color": discord.Color.from_str("#FFC9DD"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Hello Kitty"},
    # ═══ ČLANSTVO & PERMISIJE ═══
    {"name": "〢 Members for /Gianni !",       "color": discord.Color.from_str("#8E44AD"), "permissions": PERM_MEMBER, "hoist": True,  "desc": "Verificirani članovi"},
    {"name": "〢 Chatter",                     "color": discord.Color.from_str("#3DDC97"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Aktivni chatter"},
    {"name": "〢 Main Permission",             "color": discord.Color.from_str("#B0BEC5"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Glavna permisija"},
    {"name": "〢 Voice Permission",            "color": discord.Color.from_str("#78909C"), "permissions": PERM_VOICE,  "hoist": False, "desc": "Voice permisija"},
    # ═══ POL & KATEGORIJE ═══
    {"name": "〢 Musko",                       "color": discord.Color.from_str("#4FC3F7"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Muški članovi"},
    {"name": "〢 Zensko",                      "color": discord.Color.from_str("#F48FB1"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Ženski članovi"},
    {"name": "〢 Radio",                       "color": discord.Color.from_str("#FF5252"), "permissions": PERM_VOICE,  "hoist": False, "desc": "Radio uloga"},
    {"name": "〢 Bots",                        "color": discord.Color.from_str("#90A4AE"), "permissions": PERM_BOT,    "hoist": False, "desc": "Bot uloga"},
    {"name": "〢 Streaks",                     "color": discord.Color.from_str("#AB47BC"), "permissions": PERM_MEMBER, "hoist": False, "desc": "Streak uloga"},
    # ═══ DRŽAVE ═══
    {"name": "〢 Bosnia and Herzegovina",      "color": discord.Color.from_str("#FFCE00"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Bosna i Hercegovina"},
    {"name": "〢 Croatia",                     "color": discord.Color.from_str("#E53935"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Hrvatska"},
    {"name": "〢 Serbia",                      "color": discord.Color.from_str("#1E88E5"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Srbija"},
    {"name": "〢 Macedonia",                   "color": discord.Color.from_str("#FB8C00"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Makedonija"},
    {"name": "〢 Europe",                      "color": discord.Color.from_str("#26A69A"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Europa"},
    # ═══ GODINE ═══
    {"name": "〢 20+",                         "color": discord.Color.from_str("#00897B"), "permissions": PERM_BASIC,  "hoist": False, "desc": "20+ godina"},
    {"name": "〢 18+",                         "color": discord.Color.from_str("#43A047"), "permissions": PERM_BASIC,  "hoist": False, "desc": "18+ godina"},
    {"name": "〢 15+",                         "color": discord.Color.from_str("#FB8C00"), "permissions": PERM_BASIC,  "hoist": False, "desc": "15+ godina"},
    {"name": "〢 14+",                         "color": discord.Color.from_str("#E65100"), "permissions": PERM_BASIC,  "hoist": False, "desc": "14+ godina"},
    # ═══ BOJE (Color Roles) ═══
    {"name": "〢 Bela",                      "color": discord.Color.from_str("#F5F5F5"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Bijela boja"},
    {"name": "〢 Zelena",                    "color": discord.Color.from_str("#4CAF50"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Zelena boja"},
    {"name": "〢 Aqea",                      "color": discord.Color.from_str("#00BCD4"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Aqua boja"},
    {"name": "〢 Žuta",                      "color": discord.Color.from_str("#FFEB3B"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Žuta boja"},
    {"name": "〢 Plava",                     "color": discord.Color.from_str("#2196F3"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Plava boja"},
    {"name": "〢 Roza",                      "color": discord.Color.from_str("#FF4081"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Roza boja"},
    {"name": "〢 Crvena",                    "color": discord.Color.from_str("#F44336"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Crvena boja"},
    {"name": "〢 Crna",                      "color": discord.Color.from_str("#1A1B1E"), "permissions": PERM_BASIC,  "hoist": False, "desc": "Crna boja"},
]

@bot.tree.command(name="sort-roles", description="📋 Poredaj GIANNI uloge u pravi redoslijed [ADMIN]")
@app_commands.default_permissions(administrator=True)
async def sort_roles(i: discord.Interaction):
    await i.response.defer(ephemeral=True)
    guild = i.guild
    desired_order = [r["name"] for r in GIANNI_ROLES]
    role_map = {r.name: r for r in guild.roles}
    found, missing = [], []
    for name in desired_order:
        if name in role_map:
            found.append((name, role_map[name]))
        else:
            missing.append(name)
    if not found:
        return await i.followup.send(embed=em("❌", "Nema GIANNI uloga! Prvo pokreni `/setup-roles`.", color=COLORS["error"]), ephemeral=True)
    try:
        positions = {}
        base = 1
        for idx, (name, role) in enumerate(reversed(found)):
            positions[role] = base + idx
        await guild.edit_role_positions(positions=positions)
        ordered_txt = "\n".join(f"`{idx+1}.` {name}" for idx, (name, _) in enumerate(found))
        e = discord.Embed(title="✅ Uloge poređane!", color=COLORS["success"], timestamp=datetime.now(timezone.utc))
        e.add_field(name="📋 Novi redoslijed (gore → dolje)", value=ordered_txt, inline=False)
        if missing:
            e.add_field(name="⚠️ Nisu pronađene na serveru", value="\n".join(missing), inline=False)
        e.set_footer(text=f"{BOT_NAME} • GIANNI Role Sort")
        await i.followup.send(embed=e, ephemeral=True)
    except discord.Forbidden:
        await i.followup.send(embed=em("❌", "Bot nema permisiju da mjenja redoslijed uloga!\nDaj botu **Administrator** permisiju.", color=COLORS["error"]), ephemeral=True)
    except Exception as ex:
        await i.followup.send(embed=em("❌", f"Greška: `{ex}`", color=COLORS["error"]), ephemeral=True)

@bot.tree.command(name="setup-roles", description="🏷️ Kreiraj sve GIANNI uloge odjednom [ADMIN]")
@app_commands.default_permissions(administrator=True)
async def setup_roles(i: discord.Interaction):
    await i.response.defer(ephemeral=True)
    guild = i.guild
    existing = [r.name for r in guild.roles]
    created, skipped = [], []

    for role_data in GIANNI_ROLES:
        if role_data["name"] in existing:
            skipped.append(role_data["name"])
            continue
        try:
            await guild.create_role(
                name=role_data["name"],
                color=role_data["color"],
                permissions=role_data["permissions"],
                hoist=role_data["hoist"],
                reason=f"GIANNI setup — kreirao {i.user}"
            )
            created.append(role_data["name"])
        except Exception as ex:
            skipped.append(f"{role_data['name']} ❌ ({ex})")

    e = discord.Embed(
        title="🏷️ GIANNI Uloge — Setup Završen!",
        color=COLORS["gold"],
        timestamp=datetime.now(timezone.utc)
    )
    if created:
        e.add_field(
            name=f"✅ Kreirano ({len(created)})",
            value="\n".join(created),
            inline=False
        )
    if skipped:
        e.add_field(
            name=f"⏭️ Preskočeno ({len(skipped)}) — već postoje",
            value="\n".join(skipped),
            inline=False
        )
    e.add_field(
        name="📋 Slijedeći korak",
        value=(
            "**Server Settings → Roles** — Povuci uloge u željeni redosljed!\n"
            "Dodijeli `〢 Cryptid Gianni ( Vlasnik )` sebi, `〢 Bots` botu."
        ),
        inline=False
    )
    e.set_footer(text=f"{BOT_NAME} • GIANNI Server Setup")
    await i.followup.send(embed=e, ephemeral=True)

# ═══════════════════════════════════════════
#    SERVER SETUP KOMANDE
# ═══════════════════════════════════════════
@bot.tree.command(name="setup", description="⚙️ Postavi sve kanale i uloge servera odjednom [ADMIN]")
@app_commands.default_permissions(administrator=True)
@discord.app_commands.describe(
    welcome="Kanal za dobrodošlicu novih članova",
    leave="Kanal za odlaske (ako se ne postavi, koristi welcome kanal)",
    log="Kanal za logove (edit, delete, join, ban...)",
    starboard="Starboard kanal (popularne poruke sa ⭐)",
    birthday="Kanal za čestitanje rođendana",
    autorole="Uloga koja se automatski daje svim novim članovima",
    welcome_poruka="Custom welcome poruka ({user} = mention, {server} = ime servera)",
    starboard_zvjezdice="Broj ⭐ potrebnih za starboard (default: 3)"
)
@discord.app_commands.default_permissions(manage_guild=True)
async def setup_all(
    i: discord.Interaction,
    welcome:             discord.TextChannel = None,
    leave:               discord.TextChannel = None,
    log:                 discord.TextChannel = None,
    starboard:           discord.TextChannel = None,
    birthday:            discord.TextChannel = None,
    autorole:            discord.Role        = None,
    welcome_poruka:      str = "",
    starboard_zvjezdice: int = 3,
):
    cfg = get_guild_config(i.guild.id)
    lines = []

    if welcome:
        cfg["welcome_channel"] = welcome.id
        lines.append(f"👋 **Welcome:** {welcome.mention}")
    if welcome_poruka:
        cfg["welcome_message"] = welcome_poruka
        lines.append(f"📝 **Welcome poruka:** *{welcome_poruka[:80]}*")
    if leave:
        cfg["leave_channel"] = leave.id
        lines.append(f"👋 **Leave:** {leave.mention}")
    if log:
        cfg["log_channel"] = log.id
        lines.append(f"📋 **Log:** {log.mention}")
    if starboard:
        cfg["starboard_channel"]   = starboard.id
        cfg["starboard_threshold"] = max(1, starboard_zvjezdice)
        lines.append(f"⭐ **Starboard:** {starboard.mention} (min {starboard_zvjezdice}⭐)")
    if birthday:
        cfg["birthday_channel"] = birthday.id
        lines.append(f"🎂 **Rođendani:** {birthday.mention}")
    if autorole:
        if autorole >= i.guild.me.top_role:
            lines.append(f"❌ **Auto-uloga:** `{autorole.name}` je viša od moje — preskočeno!")
        else:
            cfg["auto_role"] = autorole.id
            lines.append(f"🏷️ **Auto-uloga:** {autorole.mention}")

    if not lines:
        return await i.response.send_message(
            embed=em("⚠️ Ništa nije postavljeno",
                     "Proslijedi barem jedan parametar!\nPrimjer:\n`/setup welcome:#dobrodošlica log:#logs autorole:@Member`",
                     color=COLORS["warning"]),
            ephemeral=True
        )

    save_data()
    e = discord.Embed(
        title="✅ Server konfigurisan!",
        description="\n".join(lines),
        color=COLORS["success"],
        timestamp=datetime.now(timezone.utc)
    )
    e.set_footer(text=f"Pregled svih postavki: /server-config | {BOT_NAME}")
    await i.response.send_message(embed=e, ephemeral=True)

@bot.tree.command(name="setup-welcome", description="⚙️ Postavi welcome kanal [ADMIN]")
@discord.app_commands.describe(kanal="Welcome kanal", poruka="Custom poruka ({user} = mention, {server} = ime servera)")
@discord.app_commands.default_permissions(manage_guild=True)
async def setup_welcome(i: discord.Interaction, kanal: discord.TextChannel, poruka: str = ""):
    cfg = get_guild_config(i.guild.id)
    cfg["welcome_channel"] = kanal.id
    if poruka: cfg["welcome_message"] = poruka
    save_data()
    preview = poruka.replace("{user}", i.user.mention).replace("{server}", i.guild.name) if poruka else f"Hej {i.user.mention}! Drago nam je što si stigao! 🇷🇸"
    await i.response.send_message(embed=em("✅ Welcome kanal postavljen!", f"Kanal: {kanal.mention}\nPoruka: *{preview}*", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="setup-leave", description="⚙️ Postavi leave kanal [ADMIN]")
@discord.app_commands.describe(kanal="Leave kanal")
@discord.app_commands.default_permissions(manage_guild=True)
async def setup_leave(i: discord.Interaction, kanal: discord.TextChannel):
    get_guild_config(i.guild.id)["leave_channel"] = kanal.id
    save_data()
    await i.response.send_message(embed=em("✅ Leave kanal postavljen!", f"Kanal: {kanal.mention}", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="setup-autorole", description="⚙️ Postavi automatsku ulogu pri ulasku [ADMIN]")
@discord.app_commands.describe(uloga="Uloga koja se daje svim novim članovima")
@discord.app_commands.default_permissions(manage_roles=True)
async def setup_autorole(i: discord.Interaction, uloga: discord.Role):
    if uloga >= i.guild.me.top_role:
        return await i.response.send_message(embed=em("❌", "Ta uloga je viša od moje! Ne mogu je davati.", color=COLORS["error"]), ephemeral=True)
    get_guild_config(i.guild.id)["auto_role"] = uloga.id
    save_data()
    await i.response.send_message(embed=em("✅ Auto-Uloga postavljena!", f"Svaki novi član dobije: {uloga.mention}", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="setup-log", description="⚙️ Postavi log kanal [ADMIN]")
@discord.app_commands.describe(kanal="Log kanal gdje bot šalje editovane/obrisane poruke, join/leave, banove")
@discord.app_commands.default_permissions(manage_guild=True)
async def setup_log(i: discord.Interaction, kanal: discord.TextChannel):
    get_guild_config(i.guild.id)["log_channel"] = kanal.id
    save_data()
    await i.response.send_message(embed=em("✅ Log kanal postavljen!", f"Kanal: {kanal.mention}\nBiće logovano: join/leave, edit, delete, ban.", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="setup-starboard", description="⚙️ Postavi starboard kanal [ADMIN]")
@discord.app_commands.describe(kanal="Starboard kanal", zvjezdice="Broj ⭐ za pin (default: 3)")
@discord.app_commands.default_permissions(manage_guild=True)
async def setup_starboard(i: discord.Interaction, kanal: discord.TextChannel, zvjezdice: int = 3):
    cfg = get_guild_config(i.guild.id)
    cfg["starboard_channel"]   = kanal.id
    cfg["starboard_threshold"] = max(1, zvjezdice)
    save_data()
    await i.response.send_message(embed=em("✅ Starboard postavljen!", f"Kanal: {kanal.mention}\nPotrebno ⭐: `{zvjezdice}`", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="setup-levelrole", description="⚙️ Postavi ulogu za određeni level [ADMIN]")
@discord.app_commands.describe(level="Level za koji se daje uloga", uloga="Uloga koja se daje")
@discord.app_commands.default_permissions(manage_roles=True)
async def setup_levelrole(i: discord.Interaction, level: int, uloga: discord.Role):
    if level < 1 or level > 1000:
        return await i.response.send_message(embed=em("❌", "Level mora biti između 1 i 1000.", color=COLORS["error"]), ephemeral=True)
    cfg = get_guild_config(i.guild.id)
    cfg.setdefault("level_roles", {})[str(level)] = uloga.id
    save_data()
    await i.response.send_message(embed=em("✅ Level uloga postavljena!", f"Level **{level}** → {uloga.mention}", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="server-config", description="⚙️ Pregled konfiguracije servera [ADMIN]")
@discord.app_commands.default_permissions(manage_guild=True)
async def server_config_cmd(i: discord.Interaction):
    cfg = get_guild_config(i.guild.id)
    def ch(cid): return f"<#{cid}>" if cid else "*nije postavljeno*"
    def ro(rid): return f"<@&{rid}>" if rid else "*nije postavljeno*"
    lr = cfg.get("level_roles", {})
    lr_txt = "\n".join(f"Level **{k}** → <@&{v}>" for k, v in sorted(lr.items(), key=lambda x: int(x[0]))) or "*nema*"
    e = discord.Embed(title=f"⚙️ Konfiguracija — {i.guild.name}", color=COLORS["purple"], timestamp=datetime.now(timezone.utc))
    e.add_field(name="👋 Welcome kanal",    value=ch(cfg.get("welcome_channel")),   inline=True)
    e.add_field(name="👋 Leave kanal",      value=ch(cfg.get("leave_channel")),     inline=True)
    e.add_field(name="🏷️ Auto-Uloga",      value=ro(cfg.get("auto_role")),         inline=True)
    e.add_field(name="📋 Log kanal",        value=ch(cfg.get("log_channel")),       inline=True)
    e.add_field(name="⭐ Starboard",        value=f"{ch(cfg.get('starboard_channel'))} (min {cfg.get('starboard_threshold', 3)}⭐)", inline=True)
    e.add_field(name="🎂 Birthday kanal",   value=ch(cfg.get("birthday_channel")),  inline=True)
    e.add_field(name="🎊 Level uloge",      value=lr_txt, inline=False)
    await i.response.send_message(embed=e, ephemeral=True)

@bot.tree.command(name="afk", description="😴 Postavi AFK status")
@discord.app_commands.describe(razlog="Razlog zašto si AFK")
async def afk_cmd(i: discord.Interaction, razlog: str = "AFK"):
    uid = str(i.user.id)
    data["afk"][uid] = {"reason": razlog, "since": time.time()}
    save_data()
    await i.response.send_message(embed=em(f"😴 {i.user.display_name} je sada AFK", f"Razlog: *{razlog}*\nBiće skinut AFK kada sljedeći put pišeš.", color=COLORS["warning"]))



@bot.tree.command(name="suggest", description="💡 Pošalji prijedlog moderatorima")
@discord.app_commands.describe(prijedlog="Tvoj prijedlog ili ideja za server")
async def suggest_cmd(i: discord.Interaction, prijedlog: str):
    cfg = get_guild_config(i.guild_id)
    ch_id = cfg.get("suggest_channel")
    ch = i.guild.get_channel(ch_id) if ch_id else None
    if not ch:
        return await i.response.send_message(embed=em("❌", "Kanal za prijedloge nije postavljen! Admini trebaju koristiti `/setchannel suggest`.", color=COLORS["error"]), ephemeral=True)
    data["suggest_count"] = data.get("suggest_count", 0) + 1
    cnt = data["suggest_count"]
    save_data()
    se = discord.Embed(
        title=f"💡 Prijedlog #{cnt}",
        description=prijedlog[:1500],
        color=COLORS["default"],
        timestamp=datetime.now(timezone.utc)
    )
    se.set_author(name=i.user.display_name, icon_url=i.user.display_avatar.url)
    se.set_footer(text=f"Prijedlog od: {i.user} • {i.guild.name}")
    try:
        msg = await ch.send(embed=se)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
    except Exception:
        return await i.response.send_message(embed=em("❌", "Nisam mogao poslati prijedlog. Provjeri moje permisije u kanalu.", color=COLORS["error"]), ephemeral=True)
    await i.response.send_message(embed=em("✅ Prijedlog poslan!", f"Tvoj prijedlog **#{cnt}** je proslijeđen moderatorima!\n\n> {prijedlog[:200]}", color=COLORS["success"]), ephemeral=True)

# ═══════════════════════════════════════════
#    SELF ROLES
# ═══════════════════════════════════════════
def _selfrole_key(guild_id: int, channel_id: int) -> str:
    return f"{guild_id}:{channel_id}"

def _build_selfrole_view(key: str) -> discord.ui.View:
    panel = data["selfroles"].get(key, {})
    view  = discord.ui.View(timeout=None)
    for r in panel.get("roles", []):
        emoji = r.get("emoji") or None
        btn   = discord.ui.Button(
            label=r["label"],
            emoji=emoji,
            custom_id=f"sr_{key}_{r['role_id']}",
            style=discord.ButtonStyle.secondary,
        )
        async def _cb(interaction: discord.Interaction, role_id=r["role_id"], label=r["label"]):
            try:
                try:
                    await interaction.response.defer(ephemeral=True, thinking=False)
                except (discord.NotFound, discord.InteractionResponded):
                    pass
                role = interaction.guild.get_role(role_id)
                if not role:
                    try: await interaction.followup.send("❌ Uloga ne postoji!", ephemeral=True)
                    except: pass
                    return
                me = interaction.guild.me
                if role >= me.top_role:
                    try: await interaction.followup.send(embed=em("❌", f"Uloga **{label}** je viša od moje! Admin: pomjeri moju ulogu iznad nje.", color=COLORS["error"]), ephemeral=True)
                    except: pass
                    return
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role, reason="Self-role panel")
                    try: await interaction.followup.send(embed=em("🏷️", f"Uklonjena uloga **{label}**!", color=COLORS["error"]), ephemeral=True)
                    except: pass
                else:
                    await interaction.user.add_roles(role, reason="Self-role panel")
                    try: await interaction.followup.send(embed=em("✅", f"Dobio/la si ulogu **{label}**!", color=COLORS["success"]), ephemeral=True)
                    except: pass
            except discord.Forbidden:
                try: await interaction.followup.send(embed=em("❌", "Nemam dozvolu za upravljanje tom ulogom!", color=COLORS["error"]), ephemeral=True)
                except: pass
            except Exception as ex:
                print(f"[selfrole _cb] {type(ex).__name__}: {ex}")
        btn.callback = _cb
        view.add_item(btn)
    return view

def _selfrole_embed(panel: dict) -> discord.Embed:
    e = discord.Embed(
        title=panel.get("title", "🏷️ Self Roles"),
        description=panel.get("description", "Klikni dugme da dobiješ/skineš ulogu!"),
        color=0x9B59B6,
        timestamp=datetime.now(timezone.utc)
    )
    roles_txt = "\n".join(
        f"{r.get('emoji', '▸')} **{r['label']}**" for r in panel.get("roles", [])
    ) or "*Nema uloga. Admin treba dodati `/selfroles-add`.*"
    e.add_field(name="Dostupne uloge", value=roles_txt, inline=False)
    e.set_footer(text="Klikni dugme ispod ↓")
    return e

# ═══════════════════════════════════════════
#    AUTO SETUP — SVA 3 PANELA ODJEDNOM
# ═══════════════════════════════════════════
PANEL_PRESETS = [
    {
        "title": "🌍 Odaberi svoju državu",
        "description": "Klikni dugme da dobiješ/skineš ulogu!",
        "roles": [
            {"name": "〢 Bosnia and Herzegovina", "label": "Bosnia and Herzegovina", "emoji": "🇧🇦"},
            {"name": "〢 Croatia",                 "label": "Croatia",                 "emoji": "🇭🇷"},
            {"name": "〢 Serbia",                  "label": "Serbia",                  "emoji": "🇷🇸"},
            {"name": "〢 Macedonia",               "label": "Macedonia",               "emoji": "🇲🇰"},
        ],
    },
    {
        "title": "Odaberi svoju malenokst",
        "description": "Klikni dugme da dobiješ/skineš ulogu!",
        "roles": [
            {"name": "〢 Musko",  "label": "Musko",  "emoji": "👦"},
            {"name": "〢 Zensko", "label": "Zensko", "emoji": "👧"},
        ],
    },
    {
        "title": "Klasične Permisije",
        "description": "Klikni dugme da dobiješ/skineš ulogu!",
        "roles": [
            {"name": "〢 Chatter",          "label": "Chatter",          "emoji": "💬"},
            {"name": "〢 Voice Permission", "label": "Voice Permission", "emoji": "🔊"},
            {"name": "〢 Main Permission",  "label": "Main Permission",  "emoji": "✅"},
        ],
    },
]

@bot.tree.command(name="setup-panels", description="🏷️ [ADMIN] Auto-kreiraj sva 3 self-role panela odjednom")
@app_commands.default_permissions(administrator=True)
async def setup_panels_cmd(i: discord.Interaction, kanal: discord.TextChannel = None):
    if not i.user.guild_permissions.administrator:
        return await i.response.send_message("❌ Samo admin.", ephemeral=True)
    ch = kanal or i.channel
    await i.response.send_message(embed=em("⏳", f"Kreiram panele u {ch.mention}...", color=COLORS["info"]), ephemeral=True)
    created, missing = [], []
    for idx, preset in enumerate(PANEL_PRESETS):
        key = _selfrole_key(i.guild.id, ch.id) + f":{idx}"
        # pronađi uloge po imenu (probaj tačan match, pa case-insensitive)
        roles_found = []
        for r in preset["roles"]:
            role = discord.utils.get(i.guild.roles, name=r["name"])
            if not role:
                role = next((rr for rr in i.guild.roles if rr.name.lower().strip() == r["name"].lower().strip()), None)
            if not role:
                role = next((rr for rr in i.guild.roles if r["label"].lower() in rr.name.lower()), None)
            if role:
                roles_found.append({"role_id": role.id, "label": r["label"], "emoji": r["emoji"]})
            else:
                missing.append(r["name"])
        if not roles_found: continue
        data["selfroles"][key] = {
            "guild_id": i.guild.id, "channel_id": ch.id, "message_id": None,
            "title": preset["title"], "description": preset["description"], "roles": roles_found
        }
        view = _build_selfrole_view(key)
        msg = await ch.send(embed=_selfrole_embed(data["selfroles"][key]), view=view)
        data["selfroles"][key]["message_id"] = msg.id
        bot.add_view(view, message_id=msg.id)
        created.append(preset["title"])
    save_data()
    desc = f"✅ Kreirano: **{len(created)}** panela\n" + "\n".join(f"• {t}" for t in created)
    if missing:
        desc += f"\n\n⚠️ Nisu pronađene uloge: {', '.join(set(missing))}\n*(Pokreni `/setup-uloge` ako ih nemaš)*"
    await i.followup.send(embed=em("🎉 Paneli postavljeni!", desc, color=COLORS["success"]), ephemeral=True)


# ═══════════════════════════════════════════
#    HELP
# ═══════════════════════════════════════════
@bot.tree.command(name="help", description="📖 Sve dostupne komande bota")
async def help_cmd(i: discord.Interaction):
    is_admin = False
    is_owner = i.user.id in OWNER_IDS
    try:
        is_admin = i.user.guild_permissions.administrator or any(r.name == "〢 /GIANNI" for r in i.user.roles)
    except: pass

    BAR = "═══════════════════════════════════"

    e = discord.Embed(
        title="✦ × G I A N N I  —  K O M A N D E  ✦",
        description=(
            f"```ansi\n\u001b[1;36m{BAR}\n"
            f"  ✦ Dobrodošli u GIANNI komandni centar! ✦\n"
            f"{BAR}\u001b[0m```\n"
            f"📌 Verzija **{VERSION}** · Ukupno komandi: **~97**\n"
            f"🔮 Sve komande se koriste sa `/`"
        ),
        color=0x00BCD4,
        timestamp=datetime.now(timezone.utc),
    )
    e.set_thumbnail(url=bot.user.display_avatar.url)

    e.add_field(
        name="╔═ ℹ️  INFO & UTILITI",
        value=(
            "> `/ping` `/serverinfo` `/userinfo` `/avatar`\n"
            "> `/invite` `/spotify` `/qr` `/vanity`\n"
            "> `/topchatters` `/serverstats`"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ 😴  AFK & SOCIJALNO",
        value=(
            "> `/afk` — Postavi AFK status\n"
            "> `/suggest` — Pošalji prijedlog adminu"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ 💰  EKONOMIJA",
        value=(
            "> `/baki` `/posao` `/daily` `/daj` `/kradi`\n"
            "> `/rank` `/leaderboard` `/shop` `/kupi`\n"
            "> `/bank` `/lottery` `/heist`"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ 🎮  IGRE & ZABAVA",
        value=(
            "> `/kpm` `/slots` `/rulet` `/flip` `/8ball`\n"
            "> `/vjasala` `/kaladont` `/toplo-hladno` `/meme`\n"
            "> `/blackjack` `/kviz` `/kocka` `/geografija`\n"
            "> `/amogus` `/amogus-stop`"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ 🎱  BINGO",
        value=(
            "> `/bingo` — Pokreni bingo rundu\n"
            "> 🔄 Auto-bingo svakih **3 sata** automatski!\n"
            "> 🎫 Klikni **Uzmi tiket** → unesi 5 brojeva (1-75)\n"
            "> 💰 Nagrade: `2✓=10k` · `3✓=30k` · `4✓=75k` · `5✓=250k 🏆`\n"
            "> ⏱️ Rezultati se objavljuju **javno** nakon 2 minute"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ 🐾  OWO — ŽIVOTINJE",
        value=(
            "> `/hunt` `/zoo` `/battle` `/sell`\n"
            "> `/animals` `/pray` `/curse`"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ ❤️  LJUBAV & AKCIJE",
        value=(
            "> `/zagrljaj` `/poljubac` `/mazi` `/tapsi`\n"
            "> `/high5` `/srce` `/brak` `/pocetkaj` `/cudan`"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ 📋  QUESTS, POLL & SOCIAL",
        value=(
            "> `/quests` — Dnevni zadaci za XP i novac\n"
            "> `/poll` — Napravi glasanje\n"
            "> `/confess` — Anonimna ispovjed\n"
            "> `/report` — Prijavi člana"
        ),
        inline=False,
    )
    e.add_field(
        name="╠═ 🔢  BROJANJE",
        value=("> `/brojanje-postavi` `/brojanje-info`"),
        inline=False,
    )

    if is_admin or is_owner:
        e.add_field(
            name="╠═ ⚙️  SERVER SETUP  〔ADMIN〕",
            value=(
                "> `/setup` `/setup-levelrole` `/server-config`\n"
                "> `/setup-welcome` `/setup-leave` `/setup-autorole`\n"
                "> `/setup-log` `/setup-starboard` `/setchannel`\n"
                "> `/setup-panels` — Self-role paneli"
            ),
            inline=False,
        )
        e.add_field(
            name="╠═ 🛡️  MODERACIJA  〔ADMIN〕",
            value=(
                "> `/ban` `/kick` `/timeout` `/warn`\n"
                "> `/warnings` `/clearwarnings` `/clear`"
            ),
            inline=False,
        )
        e.add_field(
            name="╠═ 🎁  GIVEAWAY  〔ADMIN〕",
            value=("> `/giveaway start` `/giveaway end` `/reset-gw`"),
            inline=False,
        )
        e.add_field(
            name="╠═ 🎫  TICKET & BOT  〔ADMIN〕",
            value=(
                "> `/ticket-setup` `/say` `/setname`\n"
                "> `/setavatar` `/sort-roles` `/setup-roles`"
            ),
            inline=False,
        )
        e.add_field(
            name="╠═ 🤖  AUTO-MOD  〔AUTOMATSKI〕",
            value=(
                "> 🚫 Anti-Spam: 7 poruka/5s → 30s timeout\n"
                "> 🛡️ Anti-Nuke: masovna zaštita kanala/uloga\n"
                "> 🔒 Anti-Raid: zaštita od botova pri joinu\n"
                "> ✅ Sve aktivno bez ikakve konfiguracije!"
            ),
            inline=False,
        )

    if is_owner:
        e.add_field(
            name="╠═ 👑  OWNER KOMANDE  〔VLASNIK〕",
            value=(
                "> `/dodaj-novac` `/oduzmi-novac`\n"
                "> `/event` — Objavi event (naslov + opis)"
            ),
            inline=False,
        )

    e.add_field(
        name="╚═ 💡  SAVJET",
        value=(
            "> Bingo tiket košta **500 coina** 🪙\n"
            "> Koristi `/posao` i `/daily` za zaradu!\n"
            "> Za pomoć: kontaktiraj staff servera 💬"
        ),
        inline=False,
    )

    e.set_footer(text=f"✦ {BOT_NAME} {VERSION} · {'👑 Owner pristup' if is_owner else ('🛡️ Admin pristup' if is_admin else '👤 Member pristup')} ✦")
    await i.response.send_message(embed=e, ephemeral=True)


# ═══════════════════════════════════════════
#    🎪 EVENT — samo vlasnik
# ═══════════════════════════════════════════
@bot.tree.command(name="event", description="🎪 Objavi event na serveru (samo vlasnik)")
@discord.app_commands.describe(
    naslov="Naslov eventa",
    opis="Opis eventa — šta, kada, gdje, nagrade itd."
)
async def event_cmd(i: discord.Interaction, naslov: str, opis: str):
    if i.user.id not in OWNER_IDS:
        return await i.response.send_message(
            embed=em("👑 Nemaš pristup!", "Ova komanda je rezervisana samo za **Vlasnika** bota.", color=COLORS["error"]),
            ephemeral=True,
        )
    BAR = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    e = discord.Embed(
        title=f"🎪  {naslov}",
        description=f"{BAR}\n\n{opis}\n\n{BAR}",
        color=0xFF6B35,
        timestamp=datetime.now(timezone.utc),
    )
    e.set_author(
        name=f"× GIANNI — NOVI EVENT!",
        icon_url=bot.user.display_avatar.url,
    )
    e.set_footer(text=f"📢 Event objavio: {i.user.display_name}  ·  {BOT_NAME}")
    e.set_thumbnail(url=bot.user.display_avatar.url)
    await i.response.send_message(embed=e)
    await i.followup.send(embed=em("✅ Event objavljen!", f"**{naslov}** je uspješno objavljen! 🎪", color=COLORS["success"]), ephemeral=True)

# ═══════════════════════════════════════════
#    ERROR HANDLING
# ═══════════════════════════════════════════
@bot.tree.error
async def on_app_error(i: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        mins, secs = divmod(int(error.retry_after), 60)
        t = f"{mins}min {secs}s" if mins else f"{secs}s"
        e = em("⏳ Cooldown!", f"Sačekaj još **{t}**.", color=COLORS["warning"])
    elif isinstance(error, app_commands.MissingPermissions):
        e = em("🛡️ Nemaš dozvole!", "Nisi ovlašćen za ovu komandu.", color=COLORS["error"])
    elif isinstance(error, app_commands.BotMissingPermissions):
        e = em("🤖 Bot nema dozvole!", "Daj mi potrebne dozvole.", color=COLORS["error"])
    else:
        e = em("❌ Greška!", f"`{str(error)[:200]}`", color=COLORS["error"])
        print(f"[ERROR] {error}")
    try:
        if i.response.is_done(): await i.followup.send(embed=e, ephemeral=True)
        else: await i.response.send_message(embed=e, ephemeral=True)
    except: pass

# ═══════════════════════════════════════════
#    /igre — UKLONJENO
# ═══════════════════════════════════════════
_REMOVED_IGRE = """
GAMES_CATALOG = [
    {
        "emoji": "🧠", "name": "Balkan Trivia", "cmd": "/kviz",
        "img": "attached_assets/games/kviz.png", "color": COLORS["purple"],
        "desc": "Odgovaraj na Balkan pitanja i osvajaj pare!",
        "kako": "Uložiš okladu, biraš jedan od 4 odgovora u 20s.",
        "nagrada": "Tačno → +oklada × combo + 25 XP. Combo raste sa svakim tačnim!"
    },
    {
        "emoji": "🌍", "name": "Geografija", "cmd": "/geografija",
        "img": "attached_assets/games/geografija.png", "color": COLORS["info"],
        "desc": "50+ pitanja o glavnim gradovima, rijekama i planinama.",
        "kako": "Uložiš okladu i biraš tačan odgovor.",
        "nagrada": "Tačno → +oklada × combo + 25 XP po nivou."
    },
    {
        "emoji": "🎲", "name": "Kocka", "cmd": "/kocka",
        "img": "attached_assets/games/kocka.png", "color": COLORS["gold"],
        "desc": "Baci kocku protiv prijatelja — veći broj pobjeđuje!",
        "kako": "Pozoveš protivnika i uložite jednaku okladu.",
        "nagrada": "Pobjednik uzima sve. Gubitnik plaća."
    },
    {
        "emoji": "🎰", "name": "Slot Mašina", "cmd": "/slots",
        "img": "attached_assets/games/slots.png", "color": COLORS["gold"],
        "desc": "Klasična slot mašina — uloži i okreni tri kotača!",
        "kako": "Postaviš ulog, vrtiš, čekaš kombinaciju.",
        "nagrada": "3 ista simbola = jackpot do 10x uloga!"
    },
    {
        "emoji": "🃏", "name": "Blackjack", "cmd": "/blackjack",
        "img": "attached_assets/games/blackjack.png", "color": COLORS["error"],
        "desc": "Pravi Blackjack protiv dilera. Cilj: 21 ili blizu!",
        "kako": "Hit za novu kartu, Stand da staneš. Diler igra po pravilu.",
        "nagrada": "Pobjeda = 2x uloga, Blackjack = 2.5x!"
    },
    {
        "emoji": "🚀", "name": "Among Us", "cmd": "/amogus",
        "img": "attached_assets/games/amogus.png", "color": COLORS["error"],
        "desc": "Kompletan Among Us u Discordu! Crewmates vs Impostor.",
        "kako": "Pokreni igru, čekaj igrače, zadaci/sastanci/glasanje.",
        "nagrada": "Pobjednička ekipa dobija nagradu i XP."
    },
    {
        "emoji": "🔤", "name": "Kaladont", "cmd": "/kaladont",
        "img": "attached_assets/games/kaladont.png", "color": COLORS["info"],
        "desc": "Klasični Balkan word game — ulanči riječi!",
        "kako": "Svaka nova riječ mora počinjati zadnjim slovima prošle.",
        "nagrada": "Što duži lanac, to više XP-a za sve!"
    },
    {
        "emoji": "🎮", "name": "Vješala", "cmd": "/vjasala",
        "img": "attached_assets/games/vjasala.png", "color": COLORS["warning"],
        "desc": "Pogodi skrivenu riječ slovo po slovo!",
        "kako": "6 grešaka i visi! Predloži slovo dugmetom.",
        "nagrada": "Pogodak = pare + XP, neuspjeh = ništa."
    },
    {
        "emoji": "🌡️", "name": "Toplo-Hladno", "cmd": "/toplo-hladno",
        "img": "attached_assets/games/toplohladno.png", "color": COLORS["info"],
        "desc": "Pogodi skriveni broj — bot ti govori toplije/hladnije!",
        "kako": "Bot bira tajni broj, ti pogađaš.",
        "nagrada": "Manje pokušaja = veća nagrada!"
    },
    {
        "emoji": "✊", "name": "Kamen-Papir-Makaze", "cmd": "/kpm",
        "img": "attached_assets/games/kpm.png", "color": COLORS["purple"],
        "desc": "Klasika protiv bota ili igrača!",
        "kako": "Klikneš dugme i čekaš ishod.",
        "nagrada": "Pobjeda = +pare, neriješeno = nazad ulog."
    },
    {
        "emoji": "🔫", "name": "Ruski Rulet", "cmd": "/rulet",
        "img": "attached_assets/games/rulet.png", "color": COLORS["error"],
        "desc": "Za hrabre — povuci obarač i pomoli se!",
        "kako": "1/6 šanse za 'metak'. Preživi i uzmi pare.",
        "nagrada": "Preživiš = veliki dobitak, padneš = timeout!"
    },
    {
        "emoji": "🪙", "name": "Novčić", "cmd": "/flip",
        "img": "attached_assets/games/flip.png", "color": COLORS["gold"],
        "desc": "Bacanje novčića — pismo ili glava?",
        "kako": "Postaviš ulog i pogađaš stranu.",
        "nagrada": "Pogodak = 2x uloga."
    },
    {
        "emoji": "🏹", "name": "Lov", "cmd": "/hunt",
        "img": "attached_assets/games/hunt.png", "color": COLORS["success"],
        "desc": "OWO-style lov! Uhvati životinje različitog rariteta.",
        "kako": "Komanda /hunt → bot izvuče nasumičnu životinju za tebe.",
        "nagrada": "Životinje idu u tvoj /zoo. Možeš ih /sell ili /battle."
    },
    {
        "emoji": "⚔️", "name": "Battle", "cmd": "/battle",
        "img": "attached_assets/games/battle.png", "color": COLORS["error"],
        "desc": "Bori se sa drugim igračem životinjama iz zoo-a!",
        "kako": "Izabereš protivnika, jača životinja pobjeđuje.",
        "nagrada": "Pobjeda = pare + XP boost."
    },
    {
        "emoji": "🔢", "name": "Brojanje", "cmd": "/brojanje-postavi",
        "img": "attached_assets/games/brojanje.png", "color": COLORS["info"],
        "desc": "Klasični sistem brojanja u kanalu — ne smiješ pogriješiti!",
        "kako": "Admin postavi kanal, svi pišu brojeve redom 1, 2, 3…",
        "nagrada": "Svaki 50. broj = +100 💶 +50 XP. Greška = reset!"
    },
]

class GamesView(discord.ui.View):
    def __init__(self, uid: int):
        super().__init__(timeout=180)
        self.uid = uid
        self.idx = 0
        self._update_buttons()

    def _update_buttons(self):
        self.prev_btn.disabled = self.idx == 0
        self.next_btn.disabled = self.idx == len(GAMES_CATALOG) - 1

    def _build_embed_and_file(self):
        g = GAMES_CATALOG[self.idx]
        e = discord.Embed(
            title=f"{g['emoji']}  {g['name']}",
            description=f"**`{g['cmd']}`**\n\n{g['desc']}",
            color=g["color"], timestamp=datetime.now(timezone.utc)
        )
        e.add_field(name="📖 Kako se igra", value=g["kako"], inline=False)
        e.add_field(name="💰 Nagrada", value=g["nagrada"], inline=False)
        e.set_footer(text=f"Igra {self.idx+1}/{len(GAMES_CATALOG)} • {BOT_NAME} {VERSION}")
        try:
            file = discord.File(g["img"], filename=f"game_{self.idx}.png")
            e.set_image(url=f"attachment://game_{self.idx}.png")
            return e, file
        except Exception:
            return e, None

    @discord.ui.button(label="◀ Nazad", style=discord.ButtonStyle.secondary)
    async def prev_btn(self, i: discord.Interaction, _):
        if i.user.id != self.uid:
            return await i.response.send_message("Ovo nije tvoj meni!", ephemeral=True)
        self.idx = max(0, self.idx - 1)
        self._update_buttons()
        e, file = self._build_embed_and_file()
        kwargs = {"embed": e, "view": self}
        if file: kwargs["attachments"] = [file]
        await i.response.edit_message(**kwargs)

    @discord.ui.button(label="Naprijed ▶", style=discord.ButtonStyle.primary)
    async def next_btn(self, i: discord.Interaction, _):
        if i.user.id != self.uid:
            return await i.response.send_message("Ovo nije tvoj meni!", ephemeral=True)
        self.idx = min(len(GAMES_CATALOG)-1, self.idx + 1)
        self._update_buttons()
        e, file = self._build_embed_and_file()
        kwargs = {"embed": e, "view": self}
        if file: kwargs["attachments"] = [file]
        await i.response.edit_message(**kwargs)

    @discord.ui.button(label="📋 Sve igre", style=discord.ButtonStyle.success)
    async def list_btn(self, i: discord.Interaction, _):
        if i.user.id != self.uid:
            return await i.response.send_message("Ovo nije tvoj meni!", ephemeral=True)
        lines = [f"{g['emoji']} `{g['cmd']:<22}` — {g['name']}" for g in GAMES_CATALOG]
        e = discord.Embed(
            title="🎮 Sve GIANNI igre",
            description="\n".join(lines) + f"\n\n*Ukupno: **{len(GAMES_CATALOG)} igara***",
            color=COLORS["gold"]
        )
        e.set_footer(text=f"{BOT_NAME} {VERSION}")
        await i.response.send_message(embed=e, ephemeral=True)

    @discord.ui.button(label="❌", style=discord.ButtonStyle.danger)
    async def close_btn(self, i: discord.Interaction, _):
        if i.user.id != self.uid:
            return await i.response.send_message("Ovo nije tvoj meni!", ephemeral=True)
        self.clear_items()
        await i.response.edit_message(content="Zatvoreno.", embed=None, view=self, attachments=[])

"""

# ═══════════════════════════════════════════
#    DODATNE KORISNE KOMANDE (v2.1)
# ═══════════════════════════════════════════
data.setdefault("bank", {})
data.setdefault("lottery", {"pot": 0, "tickets": {}, "last_draw": 0})
data.setdefault("reminders", [])
data.setdefault("heist_cooldown", {})
data.setdefault("confess_count", 0)
data.setdefault("suggest_count", 0)
data.setdefault("cmd_uses", {})

# ─── 📊 SERVER STATS ───
@bot.tree.command(name="serverstats", description="📊 Statistika servera")
async def serverstats_cmd(i: discord.Interaction):
    g = i.guild
    total_msgs = sum(v for k, v in data.get("msg_count", {}).items() if k.startswith(f"{g.id}:"))
    online = sum(1 for m in g.members if m.status != discord.Status.offline)
    bots = sum(1 for m in g.members if m.bot)
    boosts = g.premium_subscription_count or 0
    e = discord.Embed(title=f"📊 {g.name} — Statistika", color=COLORS["info"], timestamp=datetime.now(timezone.utc))
    if g.icon: e.set_thumbnail(url=g.icon.url)
    e.add_field(name="👥 Članovi", value=f"`{g.member_count}`", inline=True)
    e.add_field(name="🟢 Online", value=f"`{online}`", inline=True)
    e.add_field(name="🤖 Botovi", value=f"`{bots}`", inline=True)
    e.add_field(name="💬 Tekst kanali", value=f"`{len(g.text_channels)}`", inline=True)
    e.add_field(name="🔊 Voice kanali", value=f"`{len(g.voice_channels)}`", inline=True)
    e.add_field(name="🏷️ Uloge", value=f"`{len(g.roles)}`", inline=True)
    e.add_field(name="💎 Boostovi", value=f"`{boosts}` (Lvl {g.premium_tier})", inline=True)
    e.add_field(name="📨 Ukupno poruka", value=f"`{total_msgs:,}`", inline=True)
    e.add_field(name="📅 Server od", value=f"<t:{int(g.created_at.timestamp())}:R>", inline=True)
    await i.response.send_message(embed=e)

# ─── 🏆 TOP CHATTERS ───
@bot.tree.command(name="topchatters", description="🏆 Top 10 najaktivnijih chatera")
async def topchatters_cmd(i: discord.Interaction):
    gid = str(i.guild.id)
    rows = [(int(k.split(":")[1]), v) for k, v in data.get("msg_count", {}).items() if k.startswith(f"{gid}:")]
    rows.sort(key=lambda x: x[1], reverse=True)
    rows = rows[:10]
    if not rows:
        return await i.response.send_message(embed=em("🏆 Top Chatters", "Još nema podataka.", color=COLORS["warning"]))
    medals = ["🥇", "🥈", "🥉"] + [f"`#{n}`" for n in range(4, 11)]
    desc = []
    for idx, (uid, cnt) in enumerate(rows):
        m = i.guild.get_member(uid)
        name = m.display_name if m else f"User {uid}"
        desc.append(f"{medals[idx]} **{name}** — `{cnt:,}` poruka")
    e = discord.Embed(title="🏆 Top 10 Najaktivnijih", description="\n".join(desc), color=COLORS["success"], timestamp=datetime.now(timezone.utc))
    await i.response.send_message(embed=e)

# ─── 🏦 BANKA ───
@bot.tree.command(name="bank", description="🏦 Banka — deposit/withdraw/balance (5% nedjeljna kamata)")
async def bank_cmd(i: discord.Interaction, akcija: str = "balance", iznos: int = 0):
    uid = str(i.user.id)
    bnk = data["bank"].setdefault(uid, {"saved": 0, "last_interest": int(time.time())})
    eco = get_economy(i.user.id)
    # kamata
    weeks = (int(time.time()) - bnk["last_interest"]) // (7*86400)
    if weeks > 0 and bnk["saved"] > 0:
        for _ in range(weeks): bnk["saved"] = int(bnk["saved"] * 1.05)
        bnk["last_interest"] = int(time.time())
    a = akcija.lower()
    if a in ("balance", "bal", "stanje"):
        return await i.response.send_message(embed=em("🏦 Banka", f"💰 Wallet: `{eco['balance']:,}`\n🏦 Banka: `{bnk['saved']:,}`\n📈 Kamata: **5% / nedjeljno**", color=COLORS["info"]))
    if a in ("deposit", "dep", "ulozi"):
        if iznos <= 0 or iznos > eco["balance"]:
            return await i.response.send_message(embed=em("❌", "Nemaš toliko.", color=COLORS["error"]), ephemeral=True)
        eco["balance"] -= iznos; bnk["saved"] += iznos; save_data()
        return await i.response.send_message(embed=em("✅ Uloženo", f"Uloženo `{iznos:,}` u banku.", color=COLORS["success"]))
    if a in ("withdraw", "wd", "podigni"):
        if iznos <= 0 or iznos > bnk["saved"]:
            return await i.response.send_message(embed=em("❌", "Nemaš toliko u banci.", color=COLORS["error"]), ephemeral=True)
        eco["balance"] += iznos; bnk["saved"] -= iznos; save_data()
        return await i.response.send_message(embed=em("✅ Podignuto", f"Podigao `{iznos:,}` iz banke.", color=COLORS["success"]))
    await i.response.send_message(embed=em("🏦 Banka — pomoć", "`/bank balance` — stanje\n`/bank deposit 100` — uloži\n`/bank withdraw 50` — podigni", color=COLORS["info"]))

# ─── 🎰 LOTO ───
@bot.tree.command(name="lottery", description="🎰 Sedmična loto — kupi tiket za 100 coina")
async def lottery_cmd(i: discord.Interaction, akcija: str = "info"):
    lot = data["lottery"]
    uid = str(i.user.id)
    a = akcija.lower()
    # auto-žrijeb svake nedjelje
    if int(time.time()) - lot.get("last_draw", 0) > 7*86400 and lot["tickets"]:
        winner_uid = random.choice(list(lot["tickets"].keys()))
        prize = lot["pot"]
        get_economy(int(winner_uid))["balance"] += prize
        lot["pot"] = 0; lot["tickets"] = {}; lot["last_draw"] = int(time.time())
        save_data()
        try:
            w = await bot.fetch_user(int(winner_uid))
            await w.send(embed=em("🎉 LOTO POBJEDA!", f"Osvojio si **{prize:,}** coina! 💰", color=COLORS["success"]))
        except: pass
    if a == "buy":
        eco = get_economy(i.user.id)
        if eco["balance"] < 100:
            return await i.response.send_message(embed=em("❌", "Treba ti 100 coina.", color=COLORS["error"]), ephemeral=True)
        eco["balance"] -= 100; lot["pot"] += 100
        lot["tickets"][uid] = lot["tickets"].get(uid, 0) + 1
        save_data()
        return await i.response.send_message(embed=em("🎫 Tiket kupljen", f"Imaš `{lot['tickets'][uid]}` tiket(a).\n💰 Pot: `{lot['pot']:,}`", color=COLORS["success"]))
    total = sum(lot["tickets"].values())
    my = lot["tickets"].get(uid, 0)
    chance = (my/total*100) if total else 0
    next_draw = lot["last_draw"] + 7*86400
    e = discord.Embed(title="🎰 Sedmična Loto", color=COLORS["info"])
    e.add_field(name="💰 Pot", value=f"`{lot['pot']:,}` coina", inline=True)
    e.add_field(name="🎫 Tvoji tiketi", value=f"`{my}` / `{total}`", inline=True)
    e.add_field(name="🎯 Šansa", value=f"`{chance:.1f}%`", inline=True)
    e.add_field(name="⏰ Sljedeći žrijeb", value=f"<t:{next_draw}:R>", inline=False)
    e.set_footer(text="/lottery buy — kupi tiket za 100 coina")
    await i.response.send_message(embed=e)

# ─── 💰 HEIST (timski razboj) ───
@bot.tree.command(name="heist", description="💰 Timski razboj — okupi 3+ ljudi i dobijte 1000-5000")
async def heist_cmd(i: discord.Interaction):
    uid = str(i.user.id)
    cd = data["heist_cooldown"].get(uid, 0)
    if int(time.time()) < cd:
        return await i.response.send_message(embed=em("⏳", f"Pokušaj ponovo <t:{cd}:R>.", color=COLORS["warning"]), ephemeral=True)
    e = discord.Embed(title="💰 RAZBOJ U PRIPREMI", description=f"{i.user.mention} organizuje razboj!\n**Klikni dugme da se pridružiš** (treba 3+ ljudi za uspjeh)\n⏰ 30 sekundi do akcije!", color=COLORS["warning"])
    crew = {i.user.id}
    class HeistView(discord.ui.View):
        def __init__(self): super().__init__(timeout=30)
        @discord.ui.button(label="🤝 Pridruži se", style=discord.ButtonStyle.success)
        async def join(self, ix: discord.Interaction, _):
            crew.add(ix.user.id)
            await ix.response.send_message(f"✅ {ix.user.mention} u ekipi! ({len(crew)} članova)", ephemeral=True, delete_after=5)
    v = HeistView()
    await i.response.send_message(embed=e, view=v)
    await asyncio.sleep(30)
    n = len(crew)
    data["heist_cooldown"][uid] = int(time.time()) + 3600
    if n < 3:
        save_data()
        return await i.followup.send(embed=em("💥 PROPAO RAZBOJ", f"Samo {n} članova — premalo. Policija je došla! 🚓", color=COLORS["error"]))
    success = random.random() < (0.4 + n*0.05)
    if success:
        per = random.randint(1000, 5000) // n
        for cid in crew: get_economy(cid)["balance"] += per
        save_data()
        await i.followup.send(embed=em("🎉 USPJEŠAN RAZBOJ!", f"Ekipa od **{n}** članova podijelila plijen!\n💰 Svako je dobio: `{per:,}` coina", color=COLORS["success"]))
    else:
        for cid in crew:
            eco = get_economy(cid); eco["balance"] = max(0, eco["balance"] - 200)
        save_data()
        await i.followup.send(embed=em("🚓 UHVAĆENI!", f"Policija je sve pohvatala! Svako je izgubio 200 coina.", color=COLORS["error"]))

# ─── 📱 QR KOD ───
@bot.tree.command(name="qr", description="📱 Generiši QR kod iz teksta ili URL-a")
async def qr_cmd(i: discord.Interaction, tekst: str):
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={discord.utils.escape_markdown(tekst).replace(' ', '%20')}"
    e = discord.Embed(title="📱 QR Kod", description=f"```{tekst[:200]}```", color=COLORS["info"])
    e.set_image(url=url)
    e.set_footer(text=f"{BOT_NAME} • QR Generator")
    await i.response.send_message(embed=e)

# ─── 🤫 CONFESS (anonimno) ───
@bot.tree.command(name="confess", description="🤫 Pošalji anonimnu ispovjed u confess kanal")
async def confess_cmd(i: discord.Interaction, poruka: str):
    cfg = get_guild_config(i.guild.id)
    ch_id = cfg.get("confess_channel")
    ch = i.guild.get_channel(ch_id) if ch_id else None
    if not ch:
        return await i.response.send_message(embed=em("❌", "Confess kanal nije postavljen.\nAdmin: `/setconfess #kanal`", color=COLORS["error"]), ephemeral=True)
    data["confess_count"] += 1; save_data()
    e = discord.Embed(title=f"🤫 Anonimna Ispovjed #{data['confess_count']}", description=poruka[:1500], color=0x9b59b6, timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"Šalji svoju: /confess")
    await ch.send(embed=e)
    await i.response.send_message(embed=em("✅", "Ispovjed poslana anonimno!", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="setchannel", description="⚙️ [ADMIN] Postavi confess/suggest/report/birthday kanal")
@app_commands.describe(tip="Tip kanala", kanal="Kanal za taj tip")
@app_commands.choices(tip=[
    app_commands.Choice(name="confess",  value="confess_channel"),
    app_commands.Choice(name="suggest",  value="suggest_channel"),
    app_commands.Choice(name="report",   value="report_channel"),
    app_commands.Choice(name="birthday", value="birthday_channel"),
])
async def setchannel_cmd(i: discord.Interaction, tip: app_commands.Choice[str], kanal: discord.TextChannel):
    if not i.user.guild_permissions.administrator:
        return await i.response.send_message("❌ Samo admin.", ephemeral=True)
    get_guild_config(i.guild.id)[tip.value] = kanal.id; save_data()
    await i.response.send_message(embed=em("✅", f"{tip.name.capitalize()} kanal: {kanal.mention}", color=COLORS["success"]), ephemeral=True)

# ═══════════════════════════════════════════
#    🦋 VANITY ROLE — .gg/gianni u statusu
# ═══════════════════════════════════════════
@bot.tree.command(name="vanity", description="🦋 Postavi/pogledaj Vanity ulogu (član stavi tekst u status → dobija ulogu)")
@app_commands.describe(
    uloga="Uloga koju bot daje članu (ostavi prazno za pregled)",
    tekst="Tekst koji član mora imati u statusu (npr. .gg/gianni)"
)
async def vanity_cmd(i: discord.Interaction, uloga: discord.Role = None, tekst: str = None):
    cfg = get_guild_config(i.guild.id)
    if uloga is None and tekst is None:
        rid = cfg.get("vanity_role")
        txt = cfg.get("vanity_text", ".gg/gianni")
        role = i.guild.get_role(rid) if rid else None
        active = sum(1 for m in i.guild.members if rid and any(r.id == rid for r in m.roles))
        e = em("🦋 Vanity Role status",
            f"**Tekst:** `{txt}`\n**Uloga:** {role.mention if role else '*nije postavljena*'}\n**Trenutno aktivnih:** `{active}` članova\n\n*Kako:* član u svoj **Custom Status** (klikni avatar → Set Status) napiše `{txt}` i automatski dobija ulogu. Skine tekst → bot mu skine ulogu (provjera svake minute).",
            color=COLORS["balkan"])
        return await i.response.send_message(embed=e, ephemeral=True)
    if not i.user.guild_permissions.administrator:
        return await i.response.send_message("❌ Samo admin može mijenjati postavke.", ephemeral=True)
    if uloga:
        if uloga >= i.guild.me.top_role:
            return await i.response.send_message(embed=em("❌", "Ta uloga je viša od moje! Pomjeri moju ulogu iznad nje.", color=COLORS["error"]), ephemeral=True)
        cfg["vanity_role"] = uloga.id
    if tekst:
        cfg["vanity_text"] = tekst.strip()
    save_data()
    await i.response.send_message(embed=em("✅ Vanity postavljen!",
        f"**Tekst:** `{cfg.get('vanity_text', '.gg/gianni')}`\n**Uloga:** <@&{cfg.get('vanity_role')}>\n\nBot provjerava svaku minutu i automatski dodjeljuje/skida ulogu.",
        color=COLORS["success"]), ephemeral=True)

@tasks.loop(minutes=1)
async def vanity_loop():
    for guild in bot.guilds:
        cfg = get_guild_config(guild.id)
        rid = cfg.get("vanity_role")
        txt = (cfg.get("vanity_text") or ".gg/gianni").lower().strip()
        if not rid or not txt: continue
        role = guild.get_role(rid)
        if not role: continue
        for member in guild.members:
            if member.bot: continue
            has_text = False
            for act in (member.activities or []):
                if isinstance(act, discord.CustomActivity):
                    if act.name and txt in act.name.lower():
                        has_text = True; break
                # fallback: bilo koja activity sa state/name
                state = getattr(act, "state", None) or ""
                name  = getattr(act, "name", None)  or ""
                if txt in state.lower() or txt in name.lower():
                    has_text = True; break
            try:
                has_role = role in member.roles
                if has_text and not has_role:
                    await member.add_roles(role, reason="Vanity status detected")
                elif not has_text and has_role:
                    await member.remove_roles(role, reason="Vanity status removed")
            except (discord.Forbidden, discord.HTTPException):
                pass

@vanity_loop.before_loop
async def _vanity_wait(): await bot.wait_until_ready()

# ═══════════════════════════════════════════
#    🎱 AUTO BINGO — svakih 3h u chatu
# ═══════════════════════════════════════════
@tasks.loop(hours=3)
async def auto_game_loop():
    for guild in bot.guilds:
        chan = discord.utils.get(guild.text_channels, name="chat")
        if not chan: continue

        pool = list(range(1, 76))
        random.shuffle(pool)
        izvuceni = pool[:20]
        session = {"drawn": izvuceni, "players": {}}

        now_str = datetime.now(timezone.utc).strftime("%H:%M")
        e = discord.Embed(
            title="🎱  ✦  B  I  N  G  O  ✦  🎱",
            description=(
                "🎯 **Klikni dugme ispod i unesi 5 brojeva (1–75)!**\n"
                "🎫 Tiket košta samo **500 coina** 🪙\n\n"
                "⏱️ Imaš **2 minute** za tiket — brzo! 🔥\n"
                "📢 Rezultati se objavljuju **javno** za sve 🌍"
            ),
            color=0x00BCD4,
            timestamp=datetime.now(timezone.utc),
        )
        e.add_field(
            name="🏆  Nagradna lista",
            value=(
                "🥉 `2 pogotka`  ──  **10.000** coina\n"
                "🥈 `3 pogotka`  ──  **30.000** coina\n"
                "🥇 `4 pogotka`  ──  **75.000** coina\n"
                "👑 `5 pogodaka` ── **250.000** coina  🏆 **JACKPOT!**"
            ),
            inline=False,
        )
        e.set_footer(text=f"🎱 × GIANNI Auto-Bingo • svakih 3h • danas u {now_str} UTC")

        view = AutoBingoPupView(session)
        try:
            bingo_msg = await chan.send(embed=e, view=view)
            view.message = bingo_msg
        except: continue

        await asyncio.sleep(120)

        if not view.is_finished():
            view.stop()
        # Zaključaj dugme na originalnoj poruci
        try:
            await bingo_msg.edit(view=None)
        except: pass
        # Objavi javne rezultate
        await _bingo_reveal(session, chan)

@auto_game_loop.before_loop
async def _auto_game_wait(): await bot.wait_until_ready()

# ═══════════════════════════════════════════
#    🏆 ACTIVE MEMBER OF THE WEEK
# ═══════════════════════════════════════════
@tasks.loop(hours=24)
async def active_member_week():
    """Svaki ponedjeljak u 12:00 UTC objavi najaktivnijeg člana sedmice."""
    now = datetime.now(timezone.utc)
    if now.weekday() != 0 or now.hour != 12:
        return
    last = data.get("aotw_last")
    today_str = now.strftime("%Y-%m-%d")
    if last == today_str:
        return
    for guild in bot.guilds:
        cfg = get_guild_config(guild.id)
        weekly = data.get("msg_count_week", {})
        gprefix = f"{guild.id}:"
        gusers = [(k.split(":")[1], v) for k, v in weekly.items() if k.startswith(gprefix)]
        if not gusers:
            continue
        gusers.sort(key=lambda x: x[1], reverse=True)
        top_uid, top_count = gusers[0]
        try:
            top_member = guild.get_member(int(top_uid)) or await guild.fetch_member(int(top_uid))
        except: continue
        if not top_member: continue
        ch = guild.get_channel(cfg.get("welcome_channel") or 1494687347558715543) or guild.system_channel
        if not ch: continue
        # Bonus: 500 coina + 100 XP
        mkey = f"{guild.id}:{top_member.id}"
        data["money"][mkey] = data["money"].get(mkey, 0) + 500
        add_xp(top_member.id, 100)
        e = discord.Embed(
            title="🏆 ᴀᴄᴛɪᴠᴇ ᴍᴇᴍʙᴇʀ ᴏꜰ ᴛʜᴇ ᴡᴇᴇᴋ 🏆",
            description=(
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👑 Najaktivniji član ove sedmice je:\n\n"
                f"## {top_member.mention}\n\n"
                f"💬 Napisao/la **{top_count:,}** poruka u zadnjih 7 dana!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🎁 **Nagrada:** `+500 coina` 💰 + `+100 XP` ⚡\n"
                f"💜 Hvala što si dio × GIANNI porodice!"
            ),
            color=0xFFD700, timestamp=now
        )
        e.set_thumbnail(url=top_member.display_avatar.url)
        # Top 3
        top3 = gusers[:3]
        leaderboard = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (uid, cnt) in enumerate(top3):
            mem = guild.get_member(int(uid))
            if mem:
                leaderboard += f"{medals[i]} {mem.mention} — `{cnt:,}` poruka\n"
        if leaderboard:
            e.add_field(name="📊 Top 3 sedmice", value=leaderboard, inline=False)
        e.set_footer(text=f"{BOT_NAME} • Sljedeći AOTW za 7 dana 📅")
        try:
            await ch.send(embed=e)
        except Exception as _e: print(f"[AOTW] {_e}")
    # Resetuj weekly counter
    data["msg_count_week"] = {}
    data["aotw_last"] = today_str
    save_data()

@active_member_week.before_loop
async def _aotw_wait(): await bot.wait_until_ready()

# ─── 🎱 RUČNI BINGO ───
@bot.tree.command(name="bingo", description="🎱 Pokreni Bingo — klikni dugme, unesi 5 brojeva i osvoji nagradu!")
async def bingo_cmd(i: discord.Interaction):
    if i.user.id not in OWNER_IDS:
        return await i.response.send_message(
            embed=em("👑 Nemaš pristup!", "Komandu `/bingo` može pokrenuti samo **Vlasnik** bota.", color=COLORS["error"]),
            ephemeral=True,
        )
    pool = list(range(1, 76))
    random.shuffle(pool)
    izvuceni = pool[:20]
    session = {"drawn": izvuceni, "players": {}}

    now_str = datetime.now(timezone.utc).strftime("%H:%M")
    e = discord.Embed(
        title="🎱  ✦  B  I  N  G  O  ✦  🎱",
        description=(
            "🎯 **Klikni dugme ispod i unesi 5 brojeva (1–75)!**\n"
            "🎫 Tiket košta samo **500 coina** 🪙\n\n"
            "⏱️ Imaš **2 minute** za tiket — brzo! 🔥\n"
            "📢 Rezultati se objavljuju **javno** za sve 🌍"
        ),
        color=0x00BCD4,
        timestamp=datetime.now(timezone.utc),
    )
    e.set_author(name=f"🎱 Pokrenuo/la: {i.user.display_name}", icon_url=i.user.display_avatar.url)
    e.add_field(
        name="🏆  Nagradna lista",
        value=(
            "🥉 `2 pogotka`  ──  **10.000** coina\n"
            "🥈 `3 pogotka`  ──  **30.000** coina\n"
            "🥇 `4 pogotka`  ──  **75.000** coina\n"
            "👑 `5 pogodaka` ── **250.000** coina  🏆 **JACKPOT!**"
        ),
        inline=False,
    )
    e.set_footer(text=f"🎱 × GIANNI Bingo • danas u {now_str} UTC • Cijena tiketa: 500 coina 🪙")

    view = AutoBingoPupView(session)
    await i.response.send_message(embed=e, view=view)
    view.message = await i.original_response()

    await asyncio.sleep(120)

    if not view.is_finished():
        view.stop()
    # Zaključaj dugme na originalnoj poruci
    try:
        await view.message.edit(view=None)
    except: pass
    # Objavi javne rezultate u istom kanalu
    await _bingo_reveal(session, i.channel)


# ═══════════════════════════════════════════
#    🎟️ PUP — BINGO LISTIĆ (dugme + modal)
# ═══════════════════════════════════════════
# Nagrade: 2=10k | 3=30k | 4=75k | 5=250k (JACKPOT)
# Cijena listića: 500 coina | Brojevi: 1-75 | Izvlači se 20
# ═══════════════════════════════════════════

PUP_CIJENA = 500
PUP_NAGRADE = {2: 10_000, 3: 30_000, 4: 75_000, 5: 250_000}
PUP_XP      = {2: 50,     3: 100,    4: 200,     5: 500}

class PupModal(discord.ui.Modal, title="🎟️ Unesi 5 brojeva (1–75)"):
    brojevi_input = discord.ui.TextInput(
        label="Unesi 5 različitih brojeva odvojenih razmakom",
        placeholder="Primjer:  7  15  33  55  72",
        min_length=5,
        max_length=30,
        style=discord.TextStyle.short,
    )

    def __init__(self, session: dict):
        super().__init__()
        self.session = session

    async def on_submit(self, i: discord.Interaction):
        uid = i.user.id

        # ── Provjera duplikata ──
        if uid in self.session["players"]:
            return await i.response.send_message(
                embed=em("❌ Već si uzeo/la tiket", "Možeš uzeti samo jedan tiket po bingu!", color=COLORS["error"]),
                ephemeral=True,
            )

        # ── Parsiranje ──
        parts = self.brojevi_input.value.strip().split()
        if len(parts) != 5:
            return await i.response.send_message(
                embed=em("❌ Pogrešan unos", "Moraš unijeti **tačno 5 brojeva**!\n💡 Primjer: `7 15 33 55 72`", color=COLORS["error"]),
                ephemeral=True,
            )
        try:
            odabrani = [int(x) for x in parts]
        except ValueError:
            return await i.response.send_message(
                embed=em("❌ Pogrešan unos", "Svi unosi moraju biti **cijeli brojevi**!", color=COLORS["error"]),
                ephemeral=True,
            )
        if any(n < 1 or n > 75 for n in odabrani):
            return await i.response.send_message(
                embed=em("❌ Broj izvan raspona", "Svi brojevi moraju biti između **1** i **75**!", color=COLORS["error"]),
                ephemeral=True,
            )
        if len(set(odabrani)) != 5:
            return await i.response.send_message(
                embed=em("❌ Duplikati", "Svih 5 brojeva mora biti **različito**!", color=COLORS["error"]),
                ephemeral=True,
            )

        # ── Balans ──
        eco = get_economy(uid)
        if eco.get("balance", 0) < PUP_CIJENA:
            return await i.response.send_message(
                embed=em(
                    "❌ Nema dovoljno coina",
                    f"Cijena listića je **{PUP_CIJENA:,} coina**.\n"
                    f"Tvoj balans: **{eco.get('balance', 0):,}** coina 💸\n\n"
                    f"Zaradi više sa `/posao` ili `/daily`!",
                    color=COLORS["error"],
                ),
                ephemeral=True,
            )

        # ── Oduzmi cijenu i sačuvaj tiket (bez otkrivanja rezultata!) ──
        eco["balance"] = eco.get("balance", 0) - PUP_CIJENA
        self.session["players"][uid] = {"brojevi": odabrani, "user": i.user.display_name, "avatar": str(i.user.display_avatar.url)}
        save_data()

        # ── Potvrda — rezultati se otkrivaju tek nakon 2 minute ──
        potvrda = discord.Embed(
            title="🎟️  Tiket primljen!  ✅",
            description=(
                f"✔️ Tvoji brojevi su **tajno zabilježeni** i čekaju kraj runde!\n"
                f"🤞 Drži fige i čekaj objavu!"
            ),
            color=0x00E5FF,
            timestamp=datetime.now(timezone.utc),
        )
        potvrda.add_field(
            name="🔢  Tvoji odabrani brojevi",
            value=" ".join(f"`{n:02d}`" for n in sorted(odabrani)),
            inline=False,
        )
        potvrda.add_field(name="💰  Plaćeno", value=f"**{PUP_CIJENA:,} coina** 🪙", inline=True)
        potvrda.add_field(name="⏳  Rezultati", value="**za ~2 minute** — javno! 📢", inline=True)
        potvrda.set_footer(text="🎱 × GIANNI Bingo • Sreće ti! 🍀")
        await i.response.send_message(embed=potvrda, ephemeral=True)


async def _bingo_reveal(session: dict, channel: discord.TextChannel):
    """Nakon 2 minute — javno objavi rezultate za sve igrače."""
    drawn     = sorted(session["drawn"])
    drawn_set = set(drawn)
    players   = session.get("players", {})

    # ── Red izvučenih 20 brojeva (vizualni prikaz) ──
    drawn_display = " ".join(f"`{n:02d}`" for n in drawn)

    if not players:
        e = discord.Embed(
            title="🎱  Bingo — Runda završena",
            description="😔 **Niko nije uzeo tiket ovaj put.**\n💡 Sljedeći auto-bingo za **~3 sata**! ⏰",
            color=0x00BCD4,
            timestamp=datetime.now(timezone.utc),
        )
        e.add_field(
            name="🎲  Izvučenih 20 brojeva",
            value=drawn_display,
            inline=False,
        )
        e.set_footer(text="🎱 × GIANNI Bingo • Budi brži/a idući put! 🍀")
        try:
            await channel.send(embed=e)
        except Exception:
            pass
        return

    # ── Izračunaj rezultate za svakog igrača ──
    results      = []
    total_prizes = 0
    jackpot_uid  = None

    for uid_str, info in players.items():
        uid     = int(uid_str)
        odabrani = info["brojevi"] if isinstance(info, dict) else info
        ime      = info["user"]    if isinstance(info, dict) else f"Igrač#{uid}"
        pogoci   = sorted(set(odabrani) & drawn_set)
        br       = len(pogoci)
        nagrada  = PUP_NAGRADE.get(br, 0)
        xp_n     = PUP_XP.get(br, 0)

        if nagrada > 0:
            eco = get_economy(uid)
            eco["balance"] = eco.get("balance", 0) + nagrada
            add_xp(uid, xp_n)
            total_prizes += nagrada
            if br == 5:
                jackpot_uid = uid

        results.append({
            "uid": uid, "ime": ime,
            "odabrani": sorted(odabrani), "pogoci": pogoci,
            "br": br, "nagrada": nagrada,
        })

    save_data()

    # ── Sortiraj po broju pogodaka (desc) ──
    results.sort(key=lambda x: x["br"], reverse=True)

    # ── Napravi listu rezultata ──
    icon = {0: "💨", 1: "💨", 2: "🪙", 3: "🪙🪙", 4: "🪙🪙🪙", 5: "🏆"}
    medal = {0: "▫️", 1: "▫️", 2: "🥉", 3: "🥈", 4: "🥇", 5: "👑"}
    rows = []
    for r in results:
        br_icon   = icon.get(r["br"], "")
        med       = medal.get(r["br"], "▫️")
        odab_str  = " ".join(f"`{n:02d}`" for n in r["odabrani"])
        pogoc_str = " ".join(f"**`{n:02d}`**" for n in r["pogoci"]) if r["pogoci"] else "`—`"
        nagrada_str = f"**+{r['nagrada']:,} coina** 🪙" if r["nagrada"] > 0 else "_bez nagrade_"
        rows.append(
            f"{med} {br_icon} **{r['ime']}**  •  {r['br']}/5 ✓  •  {nagrada_str}\n"
            f"> 🔢 {odab_str}\n"
            f"> 🎯 Pogoci: {pogoc_str}"
        )

    results_txt = "\n\n".join(rows) if rows else "*Niko nije igrao.*"

    title = "🏆  ✦  J A C K P O T  ✦  🏆" if jackpot_uid else "🎱  ✦  B I N G O  —  Rezultati  ✦"
    color = 0xFFD700 if jackpot_uid else 0x00BCD4

    e = discord.Embed(
        title=title,
        description="🎉 Runda je gotova! Pogledaj ko je pobijedio!" if total_prizes > 0 else "Ovaj put nema pobjednika. Sreće idući put!",
        color=color,
        timestamp=datetime.now(timezone.utc),
    )
    e.add_field(
        name="🎲  Izvučenih 20 brojeva",
        value=drawn_display,
        inline=False,
    )
    e.add_field(name=f"📋  Rezultati  ({len(results)} igrača)", value=results_txt[:1020], inline=False)
    if total_prizes > 0:
        e.add_field(name="💰  Ukupno podijeljeno", value=f"**{total_prizes:,} coina** 🪙", inline=True)
        e.add_field(name="🏅  Pobjednici", value=f"**{sum(1 for r in results if r['nagrada'] > 0)}** igrača", inline=True)
    e.set_footer(text="🎱 × GIANNI Bingo • Čestitamo pobjednicima! 🎉")
    try:
        await channel.send(embed=e)
    except Exception:
        pass


class AutoBingoPupView(discord.ui.View):
    """View za auto bingo loop — dugme Uzmi tiket otvara modal."""
    def __init__(self, session: dict):
        super().__init__(timeout=120)
        self.session = session
        self.message: discord.Message | None = None

    @discord.ui.button(label="Uzmi tiket", emoji="🎱", style=discord.ButtonStyle.primary)
    async def uzmi_tiket(self, i: discord.Interaction, _btn: discord.ui.Button):
        await i.response.send_modal(PupModal(self.session))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass

# ═══════════════════════════════════════════
#    📊 USAGE TRACKING — broji koliko se koja komanda koristi
# ═══════════════════════════════════════════

# ═══════════════════════════════════════════
#    🔊 PRIVATE VOICE — Join To Create
# ═══════════════════════════════════════════
JTC_VOICE_ID = 1494043959213953114  # Glavni "Kreiraj svoj kanal" voice
PVC_INFO_CHANNEL_ID = 1494043958681145570  # Kanal gdje se postavlja uputstvo
data.setdefault("private_voices", {})  # {channel_id: owner_id}
data.setdefault("pvc_info_posted", False)

async def post_pvc_info():
    """Jednom postavi lijep uputstvo embed u info kanal."""
    if data.get("pvc_info_posted"): return
    for guild in bot.guilds:
        ch = guild.get_channel(PVC_INFO_CHANNEL_ID)
        if not ch: continue
        try:
            sep = "━━━━━━━━━━━━━━━━━━━━━━"
            e = discord.Embed(
                title="🔊 ᴋᴀᴋᴏ ᴋᴏʀɪꜱᴛɪᴛɪ ᴘʀɪᴠᴀᴛɴɪ ᴠᴏɪᴄᴇ?",
                description=(
                    f"{sep}\n"
                    f"💡 Napravi **svoj vlastiti voice kanal** koji možeš zaključati, sakriti, "
                    f"renamati, postaviti limit i još mnogo toga!\n"
                    f"{sep}"
                ),
                color=0x9B59B6
            )
            e.add_field(
                name="1️⃣ Kako napraviti svoj kanal",
                value=(
                    f"➜ Uđi u voice kanal **🔊 Kreiraj svoj kanal** <#{JTC_VOICE_ID}>\n"
                    f"➜ Bot će ti **automatski** napraviti privatni voice\n"
                    f"➜ I **odmah** te prebaciti u njega\n"
                    f"➜ Postaješ **vlasnik** 👑 i dobijaš kontrolni panel!\n{sep}"
                ),
                inline=False
            )
            e.add_field(
                name="2️⃣ Kontrolni panel (dugmad u tvom VC-u)",
                value=(
                    "🔒 **Lock** — niko ne može ući u tvoj kanal\n"
                    "🔓 **Unlock** — svi mogu ući\n"
                    "👁️ **Hide** — sakrij kanal od svih\n"
                    "👀 **Show** — vrati kanal vidljiv\n"
                    "✏️ **Rename** — promijeni ime kanala\n"
                    "👥 **Limit** — postavi max broj članova (1-99)\n"
                    "🚫 **Kick** — izbaci nekog iz tvog kanala\n"
                    "👑 **Owner** — prebaci vlasništvo na drugog\n"
                    "❌ **Delete** — odmah obriši kanal\n"
                    f"{sep}"
                ),
                inline=False
            )
            e.add_field(
                name="3️⃣ Automatsko brisanje",
                value=(
                    "🗑️ Kad **svi izađu**, kanal se **automatski briše**\n"
                    "💾 Ne brini o čišćenju — bot to radi za tebe!\n"
                    f"{sep}"
                ),
                inline=False
            )
            e.add_field(
                name="💡 Korisni Tip",
                value=(
                    "✨ Lock + Hide = potpuno privatan VC samo za tebe i prijatelje\n"
                    "🎮 Pozovi prijatelje preko **Invite to channel** desnim klikom\n"
                    "👑 Prebaci vlasništvo prije izlaska ako želiš da kanal ostane"
                ),
                inline=False
            )
            e.set_footer(text=f"{BOT_NAME} • Privatni Voice Sistem 🔊")
            e.set_thumbnail(url="https://cdn.discordapp.com/emojis/963322998568083477.gif")
            await ch.send(embed=e)
            data["pvc_info_posted"] = True
            save_data()
        except Exception as _e:
            print(f"[pvc-info] {_e}")

class PrivateVCPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def _check_owner(self, interaction):
        ch = interaction.user.voice.channel if interaction.user.voice else None
        if not ch or str(ch.id) not in data.get("private_voices", {}):
            await interaction.response.send_message("❌ Nisi u privatnom voice kanalu!", ephemeral=True)
            return None
        if data["private_voices"][str(ch.id)] != interaction.user.id:
            await interaction.response.send_message("❌ Nisi vlasnik ovog kanala!", ephemeral=True)
            return None
        return ch

    @discord.ui.button(label="🔒 Lock", style=discord.ButtonStyle.danger, custom_id="pvc_lock")
    async def lock(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        await ch.set_permissions(i.guild.default_role, connect=False)
        await i.response.send_message("🔒 Kanal **zaključan** — niko ne može ući!", ephemeral=True)

    @discord.ui.button(label="🔓 Unlock", style=discord.ButtonStyle.success, custom_id="pvc_unlock")
    async def unlock(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        await ch.set_permissions(i.guild.default_role, connect=None)
        await i.response.send_message("🔓 Kanal **otključan** — svi mogu ući!", ephemeral=True)

    @discord.ui.button(label="👁️ Hide", style=discord.ButtonStyle.secondary, custom_id="pvc_hide")
    async def hide(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        await ch.set_permissions(i.guild.default_role, view_channel=False)
        await i.response.send_message("👁️ Kanal **sakriven** — niko ga ne vidi!", ephemeral=True)

    @discord.ui.button(label="👀 Show", style=discord.ButtonStyle.secondary, custom_id="pvc_show")
    async def show(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        await ch.set_permissions(i.guild.default_role, view_channel=None)
        await i.response.send_message("👀 Kanal **vidljiv** svima!", ephemeral=True)

    @discord.ui.button(label="✏️ Rename", style=discord.ButtonStyle.primary, custom_id="pvc_rename")
    async def rename(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        modal = discord.ui.Modal(title="✏️ Promijeni ime kanala")
        name_in = discord.ui.TextInput(label="Novo ime", placeholder="🔊 Moj kanal", max_length=50)
        modal.add_item(name_in)
        async def cb(m_int):
            await ch.edit(name=name_in.value)
            await m_int.response.send_message(f"✅ Ime promijenjeno u: **{name_in.value}**", ephemeral=True)
        modal.on_submit = cb
        await i.response.send_modal(modal)

    @discord.ui.button(label="👥 Limit", style=discord.ButtonStyle.primary, custom_id="pvc_limit")
    async def limit(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        modal = discord.ui.Modal(title="👥 Postavi limit članova")
        lim_in = discord.ui.TextInput(label="Broj (0 = bez limita, max 99)", placeholder="5")
        modal.add_item(lim_in)
        async def cb(m_int):
            try: n = max(0, min(99, int(lim_in.value)))
            except: return await m_int.response.send_message("❌ Mora biti broj!", ephemeral=True)
            await ch.edit(user_limit=n)
            await m_int.response.send_message(f"✅ Limit postavljen na **{n}** {'(bez limita)' if n==0 else 'članova'}", ephemeral=True)
        modal.on_submit = cb
        await i.response.send_modal(modal)

    @discord.ui.button(label="🚫 Kick", style=discord.ButtonStyle.danger, custom_id="pvc_kick", row=1)
    async def kick(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        if not ch.members or len([m for m in ch.members if m.id != i.user.id]) == 0:
            return await i.response.send_message("❌ Nema nikog za izbacit!", ephemeral=True)
        opts = [discord.SelectOption(label=m.display_name, value=str(m.id))
                for m in ch.members if m.id != i.user.id][:25]
        sel = discord.ui.Select(placeholder="Izaberi koga da izbaciš", options=opts)
        async def sel_cb(s_int):
            mid = int(sel.values[0])
            mem = ch.guild.get_member(mid)
            if mem and mem.voice and mem.voice.channel == ch:
                await mem.move_to(None)
                await s_int.response.send_message(f"🚫 {mem.mention} izbačen iz kanala!", ephemeral=True)
            else:
                await s_int.response.send_message("❌ Već nije u kanalu.", ephemeral=True)
        sel.callback = sel_cb
        view = discord.ui.View(timeout=60)
        view.add_item(sel)
        await i.response.send_message("Izaberi člana:", view=view, ephemeral=True)

    @discord.ui.button(label="👑 Owner", style=discord.ButtonStyle.secondary, custom_id="pvc_transfer", row=1)
    async def transfer(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        opts = [discord.SelectOption(label=m.display_name, value=str(m.id))
                for m in ch.members if m.id != i.user.id and not m.bot][:25]
        if not opts:
            return await i.response.send_message("❌ Nema nikog kome bi prebacio vlasništvo!", ephemeral=True)
        sel = discord.ui.Select(placeholder="Novi vlasnik", options=opts)
        async def sel_cb(s_int):
            new_id = int(sel.values[0])
            new_owner = ch.guild.get_member(new_id)
            data["private_voices"][str(ch.id)] = new_id
            save_data()
            await ch.set_permissions(i.user, overwrite=None)
            await ch.set_permissions(new_owner, manage_channels=True, move_members=True, mute_members=True, deafen_members=True)
            await s_int.response.send_message(f"👑 Vlasništvo prebačeno na {new_owner.mention}!", ephemeral=True)
        sel.callback = sel_cb
        view = discord.ui.View(timeout=60)
        view.add_item(sel)
        await i.response.send_message("Izaberi novog vlasnika:", view=view, ephemeral=True)

    @discord.ui.button(label="❌ Delete", style=discord.ButtonStyle.danger, custom_id="pvc_delete", row=1)
    async def delete(self, i: discord.Interaction, b):
        ch = await self._check_owner(i)
        if not ch: return
        await i.response.send_message("❌ Brišem kanal za 3s...", ephemeral=True)
        await asyncio.sleep(3)
        try:
            data["private_voices"].pop(str(ch.id), None)
            save_data()
            await ch.delete(reason="Vlasnik obrisao privatni VC")
        except: pass

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    # ── KREIRAJ NOVI PRIVATNI VC ──
    if after.channel and after.channel.id == JTC_VOICE_ID:
        try:
            cat = after.channel.category
            new_ch = await member.guild.create_voice_channel(
                name=f"🔊 {member.display_name}",
                category=cat,
                reason=f"Privatni VC za {member}"
            )
            await new_ch.set_permissions(member, manage_channels=True, move_members=True,
                mute_members=True, deafen_members=True, connect=True, view_channel=True)
            data["private_voices"][str(new_ch.id)] = member.id
            save_data()
            await member.move_to(new_ch)
            # Pošalji panel u kanal (text chat unutar VC-a, Discord 2024+ feature)
            try:
                e = discord.Embed(
                    title=f"🔊 Dobrodošao u svoj kanal, {member.display_name}!",
                    description=(
                        "**Ti si vlasnik!** 👑 Koristi dugmad ispod:\n\n"
                        "🔒 **Lock** — niko ne može ući\n"
                        "🔓 **Unlock** — svi mogu ući\n"
                        "👁️ **Hide / Show** — sakrij/pokaži kanal\n"
                        "✏️ **Rename** — promijeni ime\n"
                        "👥 **Limit** — postavi max članova\n"
                        "🚫 **Kick** — izbaci nekog iz kanala\n"
                        "👑 **Owner** — prebaci vlasništvo\n"
                        "❌ **Delete** — obriši kanal\n\n"
                        "*Kanal se automatski briše kad ostane prazan.*"
                    ),
                    color=COLORS.get("balkan", 0x9B59B6)
                )
                e.set_footer(text=f"{BOT_NAME} • Privatni Voice Sistem")
                await new_ch.send(content=member.mention, embed=e, view=PrivateVCPanel())
            except Exception as _e: print(f"[pvc panel] {_e}")
        except Exception as _e: print(f"[pvc create] {_e}")

    # ── OBRIŠI PRAZAN PRIVATNI VC ──
    if before.channel and str(before.channel.id) in data.get("private_voices", {}):
        if len([m for m in before.channel.members if not m.bot]) == 0:
            try:
                data["private_voices"].pop(str(before.channel.id), None)
                save_data()
                await before.channel.delete(reason="Privatni VC prazan")
            except Exception as _e: print(f"[pvc delete] {_e}")

@bot.tree.error
async def _tree_err(interaction, error):
    print(f"[tree.error] {type(error).__name__}: {error}")

@bot.event
async def on_app_command_completion(interaction, command):
    try:
        n = command.qualified_name if hasattr(command, "qualified_name") else command.name
        data["cmd_uses"][n] = data["cmd_uses"].get(n, 0) + 1
    except Exception: pass

# ─── 🚨 REPORT (anoniman) ───
@bot.tree.command(name="report", description="🚨 Anonimno prijavi korisnika moderatorima")
async def report_cmd(i: discord.Interaction, korisnik: discord.Member, razlog: str):
    cfg = get_guild_config(i.guild.id)
    ch_id = cfg.get("report_channel") or cfg.get("log_channel")
    ch = i.guild.get_channel(ch_id) if ch_id else None
    if not ch:
        return await i.response.send_message(embed=em("❌", "Report kanal nije postavljen.\nAdmin: `/setreport #kanal`", color=COLORS["error"]), ephemeral=True)
    e = discord.Embed(title="🚨 Anonimni Report", color=COLORS["error"], timestamp=datetime.now(timezone.utc))
    e.add_field(name="👤 Prijavljen", value=korisnik.mention, inline=True)
    e.add_field(name="📅 Nalog star", value=f"<t:{int(korisnik.created_at.timestamp())}:R>", inline=True)
    e.add_field(name="📝 Razlog", value=razlog[:1000], inline=False)
    e.set_thumbnail(url=korisnik.display_avatar.url)
    await ch.send(embed=e)
    await i.response.send_message(embed=em("✅", "Report poslan anonimno moderatorima!", color=COLORS["success"]), ephemeral=True)

# ═══════════════════════════════════════════
#    POKRETANJE
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print(f"\n{BOT_NAME} {VERSION} STARTUJE...\n")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("POGRESAN TOKEN!")
    except Exception as e:
        print(f"Greška: {e}")
