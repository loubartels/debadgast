# DNS-records debadgast.nl

Vastgelegd op 5 augustus 2026, vóór de verhuizing van de website naar Vercel.
Beheer: Antagonist (DirectAdmin). Naamservers: `ns1/ns2/ns3.webhostingserver.nl`.

**Dit document is de terugdraaiknop.** Gaat er iets mis, zet dan de records uit de
tabel hieronder terug zoals ze waren en de oude situatie is hersteld.

## De situatie vooraf

Alles wees naar één server bij Antagonist: `141.138.169.212` (IPv4) en
`2a03:3c00:a002:212::1000` (IPv6).

| Naam | Type | Waarde | Wat ermee gebeurt |
|---|---|---|---|
| `debadgast.nl.` | A | 141.138.169.212 | **Wijzigen** → adres van Vercel |
| `www` | A | 141.138.169.212 | **Wijzigen** → adres van Vercel |
| `debadgast.nl.` | AAAA | 2a03:3c00:a002:212:0:0:0:1000 | **Verwijderen** (zie waarschuwing) |
| `www` | AAAA | 2a03:3c00:a002:212:0:0:0:1000 | **Verwijderen** (zie waarschuwing) |
| `debadgast.nl.` | MX | 10 mail.debadgast.nl. | Met rust laten — hierover loopt de e-mail |
| `mail` | A / AAAA | 141.138.169.212 / 2a03:…:1000 | Met rust laten — mailserver |
| `smtp` | A / AAAA | 141.138.169.212 / 2a03:…:1000 | Met rust laten — uitgaande mail |
| `pop` | A / AAAA | 141.138.169.212 / 2a03:…:1000 | Met rust laten — inkomende mail |
| `autoconfig` | CNAME | mail.antagonist.nl. | Met rust laten — automatische mailinstellingen |
| `autodiscover` | CNAME | mail.antagonist.nl. | Met rust laten — idem |
| `whs1._domainkey` | CNAME | 77rzmlg5jbisxqvptsyrgl5rsa.whs1.dkim.webhostingserver.nl. | Met rust laten — DKIM, ondertekent uitgaande mail |
| `whs2._domainkey` | CNAME | 77rzmlg5jbisxqvptsyrgl5rsa.whs2.dkim.webhostingserver.nl. | Met rust laten — DKIM |
| `whs3._domainkey` | CNAME | 77rzmlg5jbisxqvptsyrgl5rsa.whs3.dkim.webhostingserver.nl. | Met rust laten — DKIM |
| `_dmarc` | TXT | `v=DMARC1; p=quarantine` | Met rust laten — mailbeleid |
| `debadgast.nl.` | TXT | `v=spf1 a mx include:_spf.webhostingserver.nl ~all` | Met rust laten — SPF (zie opmerking) |
| `_25._tcp.mail` | TLSA | 3 1 1 0272e326eaf032aef82bda2156fc3a35432316c5b9c8fda8907864f50d224d7 | Met rust laten — versleuteling mailverkeer |
| `_A744CE31666ED8FFDAA8B7F5A0E31491` | CNAME | 062972BE0785BC86D9CC86312EB9E714.6300A2B3466FFD7061B787DAD2042614.bpy2nssB8Ua0SfN8W2ae.sectigo.com. | Met rust laten — controle SSL-certificaat Antagonist |
| `ftp` | A / AAAA | 141.138.169.212 / 2a03:…:1000 | Met rust laten |
| `localhost` | A / AAAA | 127.0.0.1 / ::1 | Met rust laten |
| `debadgast.nl.` | NS | ns1/ns2/ns3.webhostingserver.nl. | Met rust laten — naamservers |

## Back-up van de oude site maken

Doe dit vóórdat je de records aanpast. De oude site blijft weliswaar op de
server staan, maar een eigen kopie is de zekerheid dat je nooit iets kwijtraakt.

**De complete manier — via de back-upfunctie (aanbevolen).** Deze pakt ook de
e-mail mee, en dat is precies wat een losse mappen-download níet doet.

1. Log in op DirectAdmin via <https://onehome.antagonist.nl/websites/44537>
2. Ga naar **Geavanceerde functies → Back-ups maken/terugzetten**
   (soms *Create/Restore Backups*)
3. Kies **Back-up maken**, en vink aan: *Website-bestanden*, *E-mail accounts*,
   *E-mail berichten*, *Databases*, *DNS-instellingen*
4. Bevestigen. De back-up wordt gemaakt en komt als één `.tar.gz` in de map
   `backups/` te staan
5. Ga naar **Mijn bestanden**, open `backups/`, en klik het bestand aan om het
   te downloaden

**Alleen de website-bestanden — via Mijn bestanden.**

1. **Mijn bestanden** → open de map `domains`
2. Vink `domains` aan (of ga een niveau dieper naar
   `domains/debadgast.nl/public_html` en vink daar alles aan)
3. Klik op **Meer** → **Comprimeren**, kies `.zip` en bevestig
4. Het zipbestand verschijnt in dezelfde map; klik erop om het te downloaden

**Via FTP.** Werkt ook, en is handiger bij veel bestanden: gebruik
[FileZilla](https://filezilla-project.org) met de FTP-gegevens uit DirectAdmin
(**FTP-beheer**), en sleep de map `domains` naar je eigen computer.

### Gedaan op 5 augustus 2026

De back-up is gemaakt en gedownload (2,43 GB: bestanden, e-mail en database) en
staat buiten deze repository. Uit de databasedump `deb41509_debadgast.sql` bleek
de oude site 92 recensies, 6 paginateksten, 62 fotogroepen en 342 foto's te
bevatten.

Die dump is gebruikt om de nieuwe site tegen de bron te controleren:

- **92 van de 92 recensies** komen exact overeen met `content/recensies.json` —
  naam, plaats, datum en volledige tekst, nul afwijkingen.
- **De algemene voorwaarden** komen woord voor woord overeen met
  `content/voorwaarden.json`, 24 artikelen.

> **De databasedump hoort niet in deze repository.** Er staan 87
> e-mailadressen van klanten in, gekoppeld aan naam en woonplaats. Bewaar hem
> privé. Op de website staan daarom alleen naam, plaats en tekst.

Bewaar de back-up op je eigen computer én ergens anders (externe schijf of
clouddrive). Zolang het hostingpakket bij Antagonist blijft draaien, is dit
strikt genomen niet nodig — maar het kost tien minuten en dekt de rest af.

## Waarschuwing: vergeet de AAAA-records niet

Dit is de valkuil waar mensen het vaakst in trappen. Als je alleen de
**A**-records naar Vercel wijst maar de **AAAA**-records naar Antagonist laten
wijzen, dan krijgt iedereen met een IPv6-verbinding — en dat is een flink deel
van de bezoekers — nog steeds de **oude** website te zien. Je ziet zelf dan
misschien de nieuwe site en denkt dat alles goed is.

Verwijder daarom de AAAA-records van `debadgast.nl` en `www`, tenzij Vercel je
een eigen IPv6-adres geeft. Alle andere AAAA-records (mail, smtp, pop, ftp)
blijven staan.

## E-mail: er hoeft niets te gebeuren

De e-mail verhuist niet mee. Alleen de website gaat naar Vercel; het domein, de
mailboxen en de mailserver blijven bij Antagonist staan waar ze staan.

| Wat | Waar het blijft |
|---|---|
| Domeinnaam `debadgast.nl` | Antagonist |
| DNS-beheer | Antagonist |
| E-mail (`info@debadgast.nl` en de rest) | Antagonist |
| Webmail, IMAP/POP/SMTP-instellingen | Antagonist, ongewijzigd |
| De website zelf | Vercel |

Dat betekent concreet: **niets aanpassen in Outlook, op de telefoon, of in de
webmail.** Alle serveradressen (`mail.debadgast.nl`, `smtp.debadgast.nl`,
`pop.debadgast.nl`) blijven precies hetzelfde, want die records blijven naar
Antagonist wijzen. De enige records die veranderen zijn de A- en AAAA-records
van `debadgast.nl` en `www` — en daar loopt geen mail overheen.

> **Zeg het hostingpakket bij Antagonist niet op.** De mailboxen zitten in dat
> pakket. Vervalt het pakket, dan vervalt de e-mail, ook al staat de website
> ergens anders.

## Opmerking bij het SPF-record

Het SPF-record bevat de regel `a`, wat betekent: "de server waar het A-record
naar wijst mag ook e-mail namens dit domein versturen". Zodra het A-record naar
Vercel wijst, geldt die toestemming dus voor Vercel. Dat breekt niets — Vercel
verstuurt geen mail namens dit domein — maar het is netter om `a` te
verwijderen, zodat het record wordt:

    v=spf1 mx include:_spf.webhostingserver.nl ~all

Alleen doen als je zeker weet dat er geen mail vanaf de webserver wordt
verstuurd. Bij twijfel: laten staan, het is geen probleem.

## De nieuwe situatie

In Vercel staat `debadgast.nl` op Production en stuurt `www.debadgast.nl` er met
een 308 naartoe. Het adres `debadgast.vercel.app` blijft daarnaast werken en is
handig als reserve: daarmee kun je de site bekijken los van het domein.

Vercel gaf op 5 augustus 2026 deze waarden:

| Naam | Type | Waarde |
|---|---|---|
| `debadgast.nl.` (`@`) | A | `216.198.79.1` |
| `www` | CNAME | `947203984157755f.vercel-dns-017.com.` |

Vercels oudere adressen (`76.76.21.21` en `cname.vercel-dns.com`) blijven werken,
maar zijn niet meer wat hij aanraadt. **Kijk altijd eerst wat Vercel zelf toont
bij Settings → Domains** — deze waarden kunnen veranderen, en de CNAME is
projectspecifiek.

Volgorde in DirectAdmin: eerst het oude `www` A-record en de twee AAAA-records
weg, dan pas de CNAME toevoegen. Een naam kan niet tegelijk een A-record en een
CNAME hebben.

Let op de punt aan het eind van de CNAME-waarde. Ontbreekt hij, dan plakt
DirectAdmin het domein eraan vast en wordt het `…vercel-dns-017.com.debadgast.nl`.

Een CNAME kan niet op het hoofddomein (`debadgast.nl`) zelf; daarvoor is altijd
een A-record nodig. Dat is normaal en verwacht.

## Volgorde en terugdraaien

1. Deze tabel bewaren (of een schermafdruk van het DNS-overzicht).
2. Domein toevoegen in Vercel, records overnemen.
3. A- en AAAA-records van `debadgast.nl` en `www` aanpassen.
4. Wachten: doorgaans binnen een uur, soms tot 24 uur.
5. Controleren: homepage, een projectpagina, en `debadgast.nl/wiebenik`
   (moet doorsturen naar de sectie Over Gerard).
6. **E-mail testen**: stuur een mail naar info@debadgast.nl en verstuur er zelf
   een. Werkt dat, dan is er aan de mailkant niets veranderd.

Terugdraaien = de A- en AAAA-records terugzetten zoals in de tabel hierboven.
Zolang het hostingpakket bij Antagonist blijft bestaan, staat de oude website er
nog gewoon en is hij daarmee direct terug.
