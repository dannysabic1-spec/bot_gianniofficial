
╔══════════════════════════════════════════════════════════════════════╗
║           ✦ × G I A N N I   B O T   v 2 . 0  ×  ✦                 ║
║          Kompletan vodič — 100 komandi — Bosnian/Serbian UI         ║
╚══════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SADRŽAJ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Opis bota
  2. Instalacija i pokretanje
  3. Konfiguracija servera (obavezno prvi korak)
  4. Sve komande — po kategoriji
  5. Ticket sistem (/tiket i /ticket-setup)
  6. Staff prijava (/tiket-staff)
  7. Bingo sistem (auto + ručni)
  8. Ekonomija i levelovanje
  9. Auto-moderacija (anti-spam, anti-raid, anti-nuke, anti-NSFW)
 10. Giveaway sistem
 11. Privatni Voice kanali
 12. Vanity uloga
 13. Owner komande
 14. Fajlovi i struktura

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. OPIS BOTA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GIANNI v2.0 je multi-funkcionalni Discord bot napisan u Pythonu (discord.py 2.x)
sa 100 slash (/) komandi. Dizajniran je za Bosnian/Serbian zajednice.

Ključne funkcionalnosti:
  • Ticket sistem — podrška + staff prijave
  • Bingo — auto-bingo svakih 3 sata + ručni bingo
  • Ekonomija — novac, XP, leveli, shop, bank, heist, lottery
  • Igre — kaladont, vjasala, blackjack, kviz, kpm, rulet, bingo, amogus...
  • OWO sistem — hunt, zoo, battle, sell, animals
  • Ljubavne akcije — zagrljaj, poljubac, mazi, crush, brak...
  • Auto-moderacija — anti-spam, anti-raid, anti-nuke, anti-NSFW, anti-invite
  • Giveaway — sa tajmerom i auto-završavanjem
  • Privatni Voice kanali — korisnik kreira vlastiti VC
  • Vanity uloga — uloga za custom Discord status
  • Self-role paneli — 3 panela (spol, dob, zemlja)
  • Brojanje — kanal za brojanje sa pravilima
  • Welcome/Leave poruke
  • Starboard — najboije poruke
  • Confess/Report/Suggest sistem

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2. INSTALACIJA I POKRETANJE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ZAHTJEVI:
  - Python 3.10 ili noviji
  - Paketi iz requirements.txt

KORACI:

  A) Instalacija paketa:
     pip install -r requirements.txt

  B) Token bota:
     Postavi TOKEN u environment varijablu ili direktno u bot.py:
     TOKEN = "tvoj_token_ovdje"
     ⚠️  NIKAD ne dijeli token javno!

  C) Owner ID:
     U bot.py pronađi: OWNER_IDS = {984906640509788180}
     Zamijeni sa tvojim Discord User ID-em.

  D) Pokretanje:
     python bot.py

  E) Hosting (Railway / Heroku / VPS):
     Procfile   → web: python bot.py
     runtime.txt→ python-3.11.x

  F) Slash komande sync:
     Komande se automatski sync-uju pri pokretanju. Može trajati do 1h
     da se pojave globalno. Za instant sync: pozovi /ping ili restartaj.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3. KONFIGURACIJA SERVERA (prvi korak nakon dodavanja bota)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Preporučeni redoslijed postavljanja:

  1. /setup-roles        → Kreira sve GIANNI uloge odjednom
  2. /setup              → Kreira sve kanale i kategorije
  3. /setup-welcome #k   → Postavi welcome kanal
  4. /setup-leave #k     → Postavi leave kanal
  5. /setup-autorole @u  → Automatska uloga pri ulasku
  6. /setup-log #k       → Log kanal (ban, kick, join, leave...)
  7. /setup-starboard #k → Starboard kanal
  8. /setchannel staff-apps #k → Kanal za staff notifikacije
  9. /setchannel confess #k    → Kanal za anonimne ispovjedi
 10. /setchannel report #k     → Kanal za reporte
 11. /setup-panels       → Kreira 3 self-role panela (spol/dob/zemlja)
 12. /ticket-setup       → Panel za otvaranje tiketa u support kanalu
 13. /vanity @uloga      → Postavi vanity ulogu za custom status

Provjera konfiguracije: /server-config

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4. SVE KOMANDE — PO KATEGORIJI (100 ukupno)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

──────────────────────────────────────────────────────────────────────
  ℹ️  INFO & UTILITI (10)
──────────────────────────────────────────────────────────────────────
  /ping           → Latencija bota i API status
  /serverinfo     → Statistike servera (članovi, kanali, uloge, boostovi)
  /userinfo       → Profil korisnika (uloge, nalog, ID, avatar)
  /avatar         → Prikaži avatar korisnika u punoj veličini
  /invite         → Statistika korisnika (poruke + invite-ovi)
  /spotify        → Prikaži šta neko sluša na Spotifyu (Spotify aktivnost)
  /qr             → Generiši QR kod iz teksta ili URL-a
  /vanity         → Postavi/pogledaj Vanity ulogu (custom Discord status)
  /topchatters    → Top 10 najaktivnijih članova (ukupne poruke)
  /serverstats    → Detaljne statistike servera

──────────────────────────────────────────────────────────────────────
  😴  AFK & SOCIJALNO (2)
──────────────────────────────────────────────────────────────────────
  /afk [razlog]   → Postavi AFK status. Bot automatski javlja
                    ostalima da si AFK kad te označe. Status se
                    skida čim pošalješ poruku.
  /suggest [tekst]→ Pošalji prijedlog adminu u suggest kanal

──────────────────────────────────────────────────────────────────────
  💰  EKONOMIJA (13)
──────────────────────────────────────────────────────────────────────
  /baki           → Provjeri stanje coina (novčanik + banka)
  /posao          → Radi i zaradi (cooldown: 1 sat, ~50-200 coina)
  /daily          → Dnevna nagrada (150-300 coina, streakovi daju bonus)
  /daj @k broj    → Pošalji coina drugom korisniku
  /kradi @k       → Pokušaj ukrasti. Ako uspiješ — profit. Ako ne — kazna.
  /rank           → Tvoj level, XP, rang na serveru
  /leaderboard    → Top 10 po XP-u/levelima
  /shop           → Pogledaj šta možeš kupiti (predmeti za coin)
  /kupi [predmet] → Kupi predmet iz shopa
  /bank           → Banka — uplaćuj/isplaćuj, 5% nedjeljna kamata
  /lottery        → Sedmična loto — tiket za 100 coina (jackpot raste)
  /heist          → Timski razboj — 3+ igrača, osvajate 1000-5000 coina
  /quests         → Dnevni zadaci — završi za bonus XP i coine

──────────────────────────────────────────────────────────────────────
  🎮  IGRE & ZABAVA (17)
──────────────────────────────────────────────────────────────────────
  /kpm            → Kamen-Papir-Makaze protiv bota
  /slots          → Slot mašina (jednoruki bandita)
  /rulet          → Ruski rulet (6 komora, jedna metka)
  /flip [iznos]   → Baci novčić — kladis se na glavu/pismo
  /8ball [pitanje]→ Magična kugle odgovara na tvoje pitanje
  /vjasala        → Vješala — pogodi skrivenu bosansku/srpsku riječ
                    (po slogovima, 6 pokušaja)
  /kaladont       → Pokreni Kaladont igru u kanalu — ulančaj riječi
                    (svaka nova riječ počinje zadnjim slovom prethodne)
  /kaladont-stop  → Zaustavi aktivnu Kaladont igru u kanalu
  /toplo-hladno   → Pogodi tajni broj 1-100 (bot govori toplo/hladno)
  /blackjack      → Klasični Blackjack — ti vs diler (21 ili explode)
  /kviz           → Balkan trivia pitanje — tačan odgovor = coini
  /geografija     → Geografski kviz — grad/zemlja/planina
  /kocka @k       → Baci kocku vs drugi igrač — veći broj pobjeđuje
  /amogus         → Pokreni Among Us igru u glasovnom kanalu
  /amogus-stop    → Zaustavi Among Us igru [host/admin]
  /meme           → Nasumični Balkan meme iz kolekcije
  /sort-roles     → Poredaj GIANNI uloge u pravi redoslijed [admin]

──────────────────────────────────────────────────────────────────────
  🎱  BINGO (1 komanda + auto sistem)
──────────────────────────────────────────────────────────────────────
  /bingo          → Pokreni ručnu bingo rundu (samo vlasnik)

  AUTO-BINGO (bez komande — radi sam):
    → Pokreće se automatski svakih 3 sata
    → Bot objavljuje "Uzmi tiket" dugme u #casino kanalu
    → Igrač klikne dugme → unosi 5 brojeva od 1-75
    → Nakon 2 minute bot objavljuje izvučenih 5 brojeva javno
    → Računa se koliko se pogodaka poklapa:
        2 pogotka  →   10.000 coina
        3 pogotka  →   30.000 coina
        4 pogotka  →   75.000 coina
        5 pogotaka → 250.000 coina 🏆
    → Tiket košta: 500 coina
    → Jedan tiket po igraču po rundi

──────────────────────────────────────────────────────────────────────
  🐾  OWO — ŽIVOTINJE (7)
──────────────────────────────────────────────────────────────────────
  /hunt           → Idi u lov — uhvati životinju (razne raritetnosti)
  /zoo            → Pogledaj svoju zbirku ulovljenih životinja
  /battle @k      → Bori se sa nekim koristeći svoje životinje
  /sell [životinja]→ Prodaj životinju iz zoo-a za coine
  /animals        → Lista svih životinja sa raritetima i vrijeddnostima
  /pray @k        → Pomoli se za korisnika (kao owo pray)
  /curse @k       → Prokuni korisnika (kao owo curse)

──────────────────────────────────────────────────────────────────────
  ❤️  LJUBAV & AKCIJE (14)
──────────────────────────────────────────────────────────────────────
  /zagrljaj @k    → Zagrli nekoga (sa slučajnom animacijom/GIF-om)
  /poljubac @k    → Pošalji poljubac
  /mazi @k        → Pomazi nekoga nježno
  /tapsi @k       → Tapsi nekoga prijateljski
  /high5 @k       → Daj peticu
  /srce @k        → Pošalji srce
  /brak @k        → Zaprosi nekoga (za fun — nema efekta)
  /pocetkaj @k    → Pocektaj nekoga
  /cudan @k       → Budi ćudan prema nekome
  /pozz [@k]      → Pozdravi server ili konkretnu osobu (sa humorom)
  /kompli @k      → Pošalji slatki komplement
  /fora @k        → Ubaci foru na račun nekoga
  /muv @k         → Muvaj nekoga Balkan stilom
  /crush          → Slučajno otkrije ko je tvoj "tajni crush" na serveru

──────────────────────────────────────────────────────────────────────
  📋  QUESTS, POLL & SOCIAL (6)
──────────────────────────────────────────────────────────────────────
  /quests         → Dnevni zadaci — lista aktivnih zadataka + napredak
  /poll [tekst]   → Napravi glasanje sa emoji reakcijama (do 4 opcije)
  /confess [tekst]→ Pošalji anonimnu ispovjed u confess kanal
                    (niko ne vidi ko je poslao)
  /report @k [r]  → Anonimno prijavi korisnika moderatorima
  /tiket          → 🎫 Otvori tiket za podršku — detalji ispod (sekcija 5)
  /tiket-staff    → 📋 Prijavi se za Staff — detalji ispod (sekcija 6)

──────────────────────────────────────────────────────────────────────
  🔢  BROJANJE (3)
──────────────────────────────────────────────────────────────────────
  /brojanje-postavi #k  → Postavi kanal za brojanje (admin)
                          Pravilo: svaki igrač broji jedan po jedan,
                          isti igrač ne smije redom dva puta
  /brojanje-info        → Pokaži trenutni broj i status
  /brojanje-reset       → Resetuj brojanje na 0 (admin)

──────────────────────────────────────────────────────────────────────
  ⚙️  SERVER SETUP — ADMIN (10)
──────────────────────────────────────────────────────────────────────
  /setup              → Auto-kreira sve kanale, kategorije i permisije
  /setup-roles        → Kreira sve GIANNI uloge (boje, permisije, redoslijed)
  /setup-welcome #k   → Postavi kanal za welcome poruke
  /setup-leave #k     → Postavi kanal za leave poruke
  /setup-autorole @u  → Uloga koja se automatski daje novim članovima
  /setup-log #k       → Log kanal za ban/kick/join/leave/edit/delete
  /setup-starboard #k → Starboard kanal (poruke sa 5+ ⭐ se prikazuju)
  /setup-levelrole [l] @u → Dodjeli ulogu na određeni level
  /setchannel [tip] #k    → Postavi specifični kanal:
                            confess / report / suggest / birthday / staff-apps
  /setup-panels       → Auto-kreira sva 3 self-role panela:
                         Panel 1: Spol (Muško/Žensko)
                         Panel 2: Dob (14+ 15+ 18+ 20+)
                         Panel 3: Zemlja (BiH, HR, SRB, MK, Europa)

──────────────────────────────────────────────────────────────────────
  🛡️  MODERACIJA — ADMIN (7)
──────────────────────────────────────────────────────────────────────
  /ban @k [razlog]      → Banuj korisnika (logira se u log kanal)
  /kick @k [razlog]     → Izbaci korisnika
  /timeout @k [min]     → Ućutkaj korisnika na X minuta
  /warn @k [razlog]     → Upozori korisnika (čuva se u bazi)
  /warnings @k          → Pogledaj sva upozorenja korisnika
  /clearwarnings @k     → Obriši sva upozorenja korisnika
  /clear [broj]         → Obriši X poruka iz kanala (max 100)

  /server-config        → Pregled kompletne konfiguracije servera

──────────────────────────────────────────────────────────────────────
  🎁  GIVEAWAY — ADMIN (3)
──────────────────────────────────────────────────────────────────────
  /giveaway start       → Pokreni nagradnu igru (trajanje, nagrada, kanal)
  /giveaway end         → Završi giveaway odmah i objavi pobjednika
  /reset-gw             → Resetuj i ponovo pokreni giveaway za 5 minuta

──────────────────────────────────────────────────────────────────────
  🎫  TICKET & BOT — ADMIN (6)
──────────────────────────────────────────────────────────────────────
  /tiket              → Direktno otvori tiket (bez panela) — detalji ispod
  /ticket-setup       → Postavi ticket panel (dugme "Otvori Ticket") u kanal
  /say [tekst]        → Bot šalje poruku u trenutni kanal
  /setname [ime]      → Promijeni ime bota
  /setavatar [url]    → Promijeni avatar bota
  /sort-roles         → Poredaj GIANNI uloge u pravilni redoslijed

──────────────────────────────────────────────────────────────────────
  🤖  AUTO-MOD (bez komandi — radi automatski)
──────────────────────────────────────────────────────────────────────
  Anti-Spam:
    → 7 poruka u 5 sekundi → 30 sekundi timeout
    → Logira se u log kanal

  Anti-NSFW:
    → Detektuje NSFW slike u svim kanalima
    → Na prvom prekršaju: upozorenje + brisanje slike
    → Na trećem prekršaju: 10-minutni timeout
    → DM korisniku pri kažnjavanju

  Anti-Invite:
    → Briše Discord invite linkove iz poruka i slash komandi
    → Isključeno za administratore

  Anti-Raid:
    → Detektuje masovni join botova (5+ za kratko)
    → Automatski lockdown servera
    → Obavještava admina u log kanal

  Anti-Nuke:
    → Štiti od masovnog brisanja kanala/uloga
    → Detektuje sumnjive masovne akcije
    → Automatska zaštita

──────────────────────────────────────────────────────────────────────
  👑  OWNER KOMANDE (3)
──────────────────────────────────────────────────────────────────────
  /dodaj-novac @k broj  → Dodaj coina korisniku (samo vlasnik bota)
  /oduzmi-novac @k broj → Oduzmi coina korisniku (samo vlasnik bota)
  /event [naslov][opis] → Objavi event na serveru (samo vlasnik bota)
                          Šalje beautifully styled embed u trenutni kanal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5. TICKET SISTEM (/tiket i /ticket-setup)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OPCIJA A — Direktni tiket (/tiket):
    1. Korisnik piše /tiket
    2. Otvara se MODAL sa 3 polja:
         • Razlog tiketa (kratko, max 100 znakova)
         • Opiši problem detaljno (do 800 znakova)
         • Šta si već pokušao/la? (opcionalno)
    3. Nakon submit-a kreira se PRIVATNI kanal "ticket-{ime}"
    4. Kanal vide: korisnik + svi admini
    5. U kanalu je lijepi aqua embed sa svim detaljima + dugme "Zatvori Ticket"
    6. Korisnik dobija ephemeral potvrdu sa linkom na kanal

  OPCIJA B — Panel tiket (/ticket-setup):
    1. Admin uradi /ticket-setup u support kanalu
    2. Kanal dobija embed sa dugmetom "Otvori Ticket"
    3. Korisnik klikne dugme → isto kreira privatni kanal
    4. Panel ostaje aktivan trajno (persistent view)

  ZATVARANJE TIKETA:
    → Klikni "Zatvori Ticket" dugme unutar kanala
    → Kanal se briše nakon 5 sekundi

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6. STAFF PRIJAVA (/tiket-staff)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  FLOW:
    1. Korisnik piše /tiket-staff
    2. Otvara se MODAL "📋 Prijava za Staff" sa 5 polja:
         • Koliko imaš godina?
         • Imaš li iskustva kao mod/staff? (min 10 znakova)
         • Zašto želiš biti staff? (min 20 znakova)
         • Koliko igrača možeš dovesti na server?
         • Koliko sati dnevno + timezone zona?
    3. Nakon submit-a kreira se JAVNI kanal "prijava-{ime}"
    4. Kanal VIDE SVI ČLANOVI — ali samo admini/staff mogu pisati
    5. U kanalu se objavljuje:
         → Lijepi aqua embed sa svim odgovorima
         → Dugmad za admin glasanje:
              ✅ PRIHVATI → DM kandidatu, poruka za admina, kanal briše za 10s
              ❌ ODBIJ    → DM kandidatu, poruka za admina, kanal briše za 10s
              ⏳ NA ČEKANJU → Kanal ostaje, diskusija se nastavlja
    6. Korisnik dobija ephemeral potvrdu sa linkom na kanal
    7. Ako je konfigurisan staff-apps kanal → šalje se i tamo notifikacija

  NAPOMENE:
    → Bot ne dodjeljuje Staff ulogu automatski — admin mora ručno
    → Ako korisnik pokuša ponovo prijaviti dok ima aktivnu prijavu
      → bot javlja grešku i linkuje postojeći kanal
    → Glasanje mogu vršiti samo korisnici sa "Manage Roles" permisijom

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7. BINGO SISTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  AUTO-BINGO (svaka 3 sata, bez akcije admina):
    → Bot automatski traži #casino kanal
    → Objavljuje embed sa dugmetom "Uzmi tiket" (aqua stil)
    → Igrači klikaju → unose 5 RAZLIČITIH brojeva od 1 do 75
    → Tiket košta 500 coina (odbija se odmah)
    → Nema duplikata — svaki igrač jedan tiket
    → Nakon 2 minute bot vuče 5 nasumičnih brojeva
    → Objavljuje rezultate JAVNO u kanalu:
         Pobjednici su poredani od najboljeg
         Svaki dobija coine automatski
    → Nagrade: 2 pogotka=10k, 3=30k, 4=75k, 5=250k
    → Sljedeći bingo se najavljuje automatski

  RUČNI BINGO (/bingo):
    → Samo vlasnik bota može pokrenuti
    → Isti mehanizam kao auto-bingo
    → Korisno za testiranje ili specijalne evente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  8. EKONOMIJA I LEVELOVANJE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ZARAĐIVANJE COINA:
    /posao    → 50-200 coina (cooldown 1h)
    /daily    → 150-300 coina + streak bonus (cooldown 24h)
    /kviz     → Tačan odgovor = coin nagrada
    /geografija → Tačan odgovor = coin nagrada
    /hunt     → Prodaj ulovljene životinje (/sell)
    /bingo    → Do 250.000 coina
    /lottery  → Jackpot raste svake sedmice
    /heist    → 1000-5000 za grupu

  XP I LEVELI:
    → Svaka poruka daje XP (boosted za boostere)
    → Nivo se povećava exponencijalno
    → Admin može podesiti nagrade (uloge) za level: /setup-levelrole
    → /rank → vidi svoj nivo i XP
    → /leaderboard → top 10 servera

  BANKA:
    /bank deposit [x]  → Uplati na štednju
    /bank withdraw [x] → Isplati sa štednje
    /bank balance      → Provjeri stanje banke
    → 5% kamata sedmično na stanje u banci

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  9. AUTO-MODERACIJA (sve radi bez podešavanja)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Anti-Spam:
    Trigger: 7 poruka u 5 sekundi
    Akcija:  Timeout 30 sekundi + log
    Izuzeci: Admini i vlasnik

  Anti-NSFW:
    Trigger: NSFW sadržaj u bilo kom kanalu
    1. prekršaj → Upozorenje + brisanje
    2. prekršaj → Isto
    3. prekršaj → 10-minutni timeout + DM obavijest
    Izuzeci:     Kanali označeni kao NSFW u Discord postavkama

  Anti-Invite:
    Trigger: Discord invite link u poruci ili slash komandi
    Akcija:  Brisanje poruke + obavijest korisniku
    Izuzeci: Admini

  Anti-Raid:
    Trigger: 5+ novih članova za kratko + sumnjivi profili
    Akcija:  Lockdown servera + log adminima

  Anti-Nuke:
    Trigger: Masovno brisanje kanala ili uloga
    Akcija:  Automatska zaštita + obavijest

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  10. GIVEAWAY SISTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  /giveaway start:
    → Uneseš trajanje (npr. 1h, 30m), nagradu i kanal
    → Bot objavljuje embed sa dugmetom "Ulazi"
    → Igrači klikaju dugme (svako jednom)
    → Po isteku tajmera bot bira pobjednika nasumično
    → Objavljuje pobjednika + ping

  /giveaway end:
    → Odmah završi aktivan giveaway i proglasi pobjednika

  /reset-gw:
    → Restartuje giveaway za 5 minuta (korisno ako niko nije ušao)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  11. PRIVATNI VOICE KANALI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  → Korisnik uđe u "Create Voice" VC kanal
  → Bot automatski kreira privatni VC kanal za njega
  → Pojavljuje se panel za upravljanje VC-om:
       🔒 Lock/Unlock   → zatvori/otvori kanal za ostale
       👥 Limit         → postavi limit korisnika
       ✏️ Rename        → preimenuj kanal
       👢 Kick          → izbaci korisnika iz VC-a
  → Kanal se automatski briše kad ga vlasnik napusti i ostane prazan

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  12. VANITY ULOGA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  /vanity @uloga [tekst]:
    → Admin postavi vanity tekst koji korisnik mora imati u Discord statusu
    → Bot svakih nekoliko minuta provjerava ko ima taj tekst u statusu
    → Korisnici koji imaju → automatski dobijaju Vanity ulogu
    → Korisnici koji uklone tekst → uloga se oduzima automatski
    → Korisno za server partners, promotere, streamere

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  13. OWNER KOMANDE (samo za OWNER_IDS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  /dodaj-novac @k [iznos]:
    → Direktno dodaje coina korisniku
    → Vidljivo samo vlasniku u /help

  /oduzmi-novac @k [iznos]:
    → Direktno oduzima coina korisniku

  /event [naslov] [opis]:
    → Objavljuje event embed (narančaste boje) u trenutni kanal
    → Samo vlasnik bota može koristiti
    → Embed uključuje naslov, opis, timestamp i potpis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  14. FAJLOVI I STRUKTURA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  bot.py
    → Cijeli bot — ~6500 linija, 100 slash komandi
    → Jedini fajl koji se pokreće: python bot.py

  oleun_data.json
    → Baza podataka (čuva se lokalno)
    → Sadržaj:
         xp            → XP po korisniku po serveru
         coins         → Novac po korisniku
         bank          → Štednja po korisniku
         warnings      → Upozorenja korisnika
         guild_configs → Konfiguracija po serveru (kanali, uloge)
         animals       → Zbirke životinja (hunt/zoo)
         cmd_uses      → Statistike korištenja komandi
         nsfw_strikes  → Evidencija NSFW prekršaja

  requirements.txt
    → discord.py>=2.3.0
    → aiohttp
    → Ostali dependenciji

  Procfile
    → web: python bot.py
    → Za Railway / Heroku hosting

  runtime.txt
    → python-3.11.x

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BRZI SETUP CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [ ] TOKEN postavljen u bot.py ili .env
  [ ] OWNER_IDS postavljen na tvoj Discord ID
  [ ] pip install -r requirements.txt
  [ ] python bot.py → provjeri da se bot pojavio online
  [ ] /setup-roles → kreiraj uloge
  [ ] /setup → kreiraj kanale
  [ ] /setup-welcome #dobrodosli → welcome poruke
  [ ] /setup-log #log → log kanal
  [ ] /setup-panels → self-role paneli
  [ ] /ticket-setup → ticket panel u support kanalu
  [ ] /setchannel staff-apps #kanal → kanal za staff notifikacije
  [ ] /setchannel confess #kanal → confess kanal
  [ ] /setchannel report #kanal → report kanal
  [ ] /vanity @uloga [tekst] → vanity setup (opcionalno)
  [ ] /giveaway start → prvi giveaway (opcionalno)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VERZIJA: v2.0 — April 2026
  Bot: GIANNI | Komande: 100 | Linija koda: ~6500
  Jezik UI: Bosnian / Serbian
  Boja teme: Aqua #00BCD4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
