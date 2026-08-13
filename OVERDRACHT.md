# Overdracht — website De Badgast

Dit document is voor Gerard, of voor wie de website beheert. Je hebt geen programmeerkennis nodig: alles wat je wilt wijzigen doe je via invulvelden in de browser.

## In het kort

De teksten en foto's van de website staan los van de opmaak. Jij bewerkt de **inhoud** in een bewerkomgeving met gewone invulvelden; de website wordt daarna automatisch opnieuw opgebouwd en staat binnen een paar minuten live. Er is geen server om bij te houden, geen database, en geen abonnement.

## Inloggen op de bewerkomgeving

1. Ga naar **https://app.pagescms.org** en log in met het GitHub-account dat bij de overdracht is aangemaakt.
2. Kies de website `debadgast`.

Je ziet dan zes onderdelen in het menu:

| Onderdeel | Waarvoor |
|---|---|
| **Projecten** | De uitgevoerde badkamers en toiletten |
| **Recensies** | Alle recensies van klanten |
| **Homepage** | Alle teksten op de voorpagina |
| **Contactgegevens** | Telefoonnummer, e-mail, werkgebied, KvK en BTW |
| **Algemene voorwaarden** | De voorwaarden, per artikel |
| **Privacyverklaring** | Hoe De Badgast met klantgegevens omgaat |

Na elke wijziging klik je op **Save**. Een paar minuten later staat het live. Verversen van de site kan nodig zijn (Ctrl+F5 of Cmd+Shift+R).

## Een recensie toevoegen

**Recensies** → **Add an entry** → invullen:

- **Naam** — zoals de klant het geschreven heeft
- **Plaats** en **Datum** — bijvoorbeeld `Roosendaal` en `12 maart 2027`
- **Recensie** — de tekst zelf
- **Op de homepage tonen** — aanvinken als je hem bij de drie uitgelichte wilt. Zet er dan ook een **ingekorte versie** bij, anders wordt de kaart op de homepage erg lang.

Nieuwe recensies horen bovenaan; je kunt ze in de lijst omhoog slepen.

## Een recensie die via de website binnenkomt

Op de recensiepagina kunnen klanten zelf een recensie achterlaten. **Die komt
niet automatisch op de site.** Hij wordt als e-mail naar info@debadgast.nl
gestuurd, met het onderwerp *"Nieuwe recensie via debadgast.nl — nog niet
geplaatst"*. Jij beslist of hij erop komt.

Wil je hem plaatsen, neem dan de tekst over via **Recensies → Add an entry**,
zoals hierboven beschreven. Wil je hem niet plaatsen, doe dan niets: er gebeurt
verder niets met de mail.

In de mail staat ook het e-mailadres van de inzender. Dat is voor jou, om
contact op te nemen als er iets niet klopt. **Zet dat adres niet op de
website** — de inzender heeft alleen toestemming gegeven voor zijn naam en
woonplaats.

## Foto's toevoegen aan een project

De foto's van elk project staan in een eigen map. Die maps staan onder `assets/projecten/`, met per project een korte naam (bijvoorbeeld `musters`).

1. Ga in de bewerkomgeving naar **Media** → map van het project
2. Sleep de foto's erin
3. Geef ze een naam met een nummer: `06.jpg`, `07.jpg` — ze verschijnen op volgorde van naam

De foto met de laagste naam (meestal `01.jpg`) is de omslagfoto op de homepage. Wil je een andere omslagfoto? Hernoem die foto dan naar `01.jpg` en de oude naar iets hogers.

**Formaat:** maak foto's niet breder dan ongeveer 1800 pixels en houd ze onder een halve megabyte, anders wordt de site traag. Dat kan gratis via squoosh.app: foto erin slepen, breedte op 1800 zetten, downloaden.

## Een nieuw project toevoegen

1. Maak eerst de fotomap: **Media** → **assets/projecten** → nieuwe map met een korte naam zonder spaties of hoofdletters, bijvoorbeeld `jansen-badkamer`. Zet de foto's erin, genummerd.
2. Ga naar **Projecten** → **Add an entry** en vul in:
   - **Titel** — beschrijvend, bijvoorbeeld *Badkamer met inloopdouche en dubbele wastafel*
   - **Mapnaam van de foto's** — exact dezelfde naam als de map die je net maakte
   - **Soort** — badkamer, toilet, of allebei
   - **Korte typering** — het regeltje boven de titel, bijvoorbeeld *Warm en natuurlijk*
   - **Omschrijving** — twee zinnen over wat het geworden is
   - **Kenmerken** — losse woorden die als labeltjes verschijnen
   - **Wat ik heb gedaan** — de stappen, elk op een eigen regel
   - **Plaats** en **Doorlooptijd** — mogen leeg blijven als je ze niet weet
3. Sleep het project naar de plek in de lijst waar je het wilt hebben. Bovenaan staat vooraan op de website.

> **Let op:** de mapnaam bij *Mapnaam van de foto's* moet exact kloppen. Staat er een typefout in, dan blijft het project leeg.

## Teksten op de homepage wijzigen

**Homepage** — alle teksten staan er per onderdeel in: de kop bovenaan, Over Gerard, De formule, Diensten, Werkwijze, en het offerteformulier. Wijzig wat je wilt en klik op Save.

Telefoonnummer, e-mailadres, werkgebied en KvK-nummer staan apart onder **Contactgegevens**, omdat die op meerdere plekken tegelijk gebruikt worden. Wijzig je ze daar, dan veranderen ze overal.

## Het offerteformulier

Aanvragen komen per e-mail binnen op **info@debadgast.nl**, via de gratis dienst [FormSubmit](https://formsubmit.co). Er is geen account of wachtwoord.

Moeten aanvragen naar een ander adres? Dat zit niet in de bewerkomgeving; daarvoor is hulp van een technisch iemand nodig (het adres staat in `assets/site.js`). **Let op:** bij de eerste aanvraag naar een nieuw adres stuurt FormSubmit één activatiemail — daarin moet op de bevestigingslink geklikt worden, anders komen aanvragen niet aan.

## Iets kwijt of stukgemaakt?

Alles is terug te draaien. Elke wijziging wordt bewaard met datum en tijd. Op **github.com/loubartels/debadgast** onder **Commits** zie je precies wat er veranderd is en kun je het terugzetten.

## Voor de technisch beheerder

- **Bron:** GitHub, `content/*.json` bevat de inhoud, `tools/bouw.py` bouwt daaruit alle HTML-pagina's plus `sitemap.xml` en `robots.txt`.
- **De HTML-bestanden nooit met de hand aanpassen** — ze worden bij elke bouw overschreven.
- **Publiceren:** Vercel bouwt bij elke wijziging opnieuw (`vercel.json`). Doorverwijzingen van de oude adressen staan daar ook in.
- **Lokaal draaien:** `python3 tools/bouw.py && python3 -m http.server 8000`
- **Domein en e-mail:** debadgast.nl staat bij Antagonist. De e-mail loopt via Antagonist en staat los van de website; zolang de MX-records ongemoeid blijven, raakt een wijziging aan de website de e-mail niet.
