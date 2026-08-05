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

## Waarschuwing: vergeet de AAAA-records niet

Dit is de valkuil waar mensen het vaakst in trappen. Als je alleen de
**A**-records naar Vercel wijst maar de **AAAA**-records naar Antagonist laten
wijzen, dan krijgt iedereen met een IPv6-verbinding — en dat is een flink deel
van de bezoekers — nog steeds de **oude** website te zien. Je ziet zelf dan
misschien de nieuwe site en denkt dat alles goed is.

Verwijder daarom de AAAA-records van `debadgast.nl` en `www`, tenzij Vercel je
een eigen IPv6-adres geeft. Alle andere AAAA-records (mail, smtp, pop, ftp)
blijven staan.

## Opmerking bij het SPF-record

Het SPF-record bevat de regel `a`, wat betekent: "de server waar het A-record
naar wijst mag ook e-mail namens dit domein versturen". Zodra het A-record naar
Vercel wijst, geldt die toestemming dus voor Vercel. Dat breekt niets — Vercel
verstuurt geen mail namens dit domein — maar het is netter om `a` te
verwijderen, zodat het record wordt:

    v=spf1 mx include:_spf.webhostingserver.nl ~all

Alleen doen als je zeker weet dat er geen mail vanaf de webserver wordt
verstuurd. Bij twijfel: laten staan, het is geen probleem.

## Wat je bij Vercel invult

Vercel geeft bij **Settings → Domains** zelf de exacte waarden. Gebruik altijd
wat Vercel toont, niet wat hier staat — die adressen kunnen wijzigen.

- `debadgast.nl` → een **A**-record naar het IP-adres dat Vercel geeft
- `www` → een **CNAME** naar het adres dat Vercel geeft

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
