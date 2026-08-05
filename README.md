# De Badgast — website

One-pager voor **De Badgast**, het badkamerrenovatiebedrijf van Gerard Bartels in Roosendaal. Gebouwd op basis van het ontwerp uit Claude Design (handoff-bundel "De Badgast hero sectie", bestand *De Badgast One-pager*).

## Bestanden

| Bestand | Wat |
|---------|-----|
| `index.html`, `recensies.html`, `voorwaarden.html`, `projecten/*.html` | **Gegenereerd** — niet met de hand aanpassen, wijzigingen worden overschreven. |
| `assets/site.css` | Gedeelde stylesheet voor beide pagina's. |
| `assets/site.js` | Gedeeld gedrag: sticky header met glas-effect, fade-in bij scrollen, projectencarrousel, offerteformulier. |
| `content/*.json` | **De inhoud**: teksten, projecten, recensies, algemene voorwaarden en contactgegevens. Dit is wat de bewerkomgeving aanpast. |
| `tools/bouw.py` | Bouwt uit `content/` de complete site. |
| `.pages.yml` | Instellingen van de bewerkomgeving (Pages CMS). |
| `vercel.json` | Doorverwijzingen van oude adressen en de bouwopdracht voor Vercel. |
| `DNS.md` | De DNS-records zoals ze vóór de verhuizing stonden, met per record wat ermee moet. |
| `assets/` | Logo, embleem en foto's. Projectfoto's staan per project in `assets/projecten/<slug>/`. |
| `design.md` | Ouder merk-fundament uit de eerste (strandpaviljoen-)versie van dit project; niet meer leidend voor het huidige ontwerp. |

De inhoud staat in `content/` en wordt door `tools/bouw.py` omgezet naar HTML. Het resultaat is een statische site zonder afhankelijkheden, op Google Fonts (Manrope) na; iconen zitten als SVG in de pagina's.

```bash
python3 tools/bouw.py    # bouwt index.html, recensies.html en projecten/*.html
```

**Pas de HTML-bestanden niet met de hand aan** — wijzig `content/` en bouw opnieuw.

## Lokaal bekijken

```bash
python3 -m http.server 8000
```

Open daarna `http://localhost:8000`.

## Live zetten

De site draait op **Vercel**. Elke wijziging in de repository start automatisch een nieuwe publicatie: Vercel draait `python3 tools/bouw.py` en zet het resultaat online. De doorverwijzingen van de oude adressen staan in `vercel.json`.

### Eenmalig instellen

1. Maak een account op vercel.com en koppel de GitHub-repository (**Add New… → Project**).
2. Vercel leest `vercel.json`; de bouwinstellingen hoeven niet handmatig ingevuld te worden.
3. **Settings → Domains** → `debadgast.nl` toevoegen. Vercel toont welke DNS-records nodig zijn.
4. Die records zetten in het DNS-beheer van Antagonist: een A-record voor `debadgast.nl` en een CNAME voor `www`. **De MX-records ongemoeid laten** — daar loopt de e-mail over.
5. Wachten tot Vercel het domein als geldig markeert; het certificaat wordt automatisch aangevraagd.

### Bewerkomgeving

De inhoud wordt beheerd via [Pages CMS](https://pagescms.org): inloggen met GitHub op app.pagescms.org, en de velden komen uit `.pages.yml`. Een wijziging daar is een commit in de repository, wat weer een publicatie op Vercel start. Zie `OVERDRACHT.md`.

### Alternatief: uploaden naar een gewone webserver

Blijft de site bij Antagonist of een andere Apache-host, dan werkt dat ook — inclusief de doorverwijzingen, want die staan óók in `.htaccess`:

1. `python3 tools/maak-uploadpakket.py`
2. `debadgast-site.zip` uitpakken en de inhoud in de webmap zetten (meestal `httpdocs` of `public_html`).

Nadeel: elke wijziging moet dan handmatig geüpload worden, en de bewerkomgeving heeft daar geen zin meer.

**Let op bij verhuizen:** de oude site heeft losse pagina's (`/wiebenik`, `/werkwijze`, `/fotos`, `/contact`, `/recensies`) die nu secties op de homepage zijn. Zowel `vercel.json` als `.htaccess` stuurt die door, zodat bestaande links uit Google blijven werken.

## Offerteformulier

Het formulier verstuurt via [FormSubmit](https://formsubmit.co) naar `info@debadgast.nl` (geen account nodig). **Bij de allereerste inzending stuurt FormSubmit één activatiemail naar dat adres — klik daarin op de bevestigingsknop, daarna komen aanvragen gewoon per mail binnen.** Ander e-mailadres? Pas het adres aan in `assets/site.js` bij het blok "Offerteformulier".

## Projecten en foto's

Elk project heeft een eigen pagina met een fotogalerij; vanaf de homepage klik je erop door.

De tien projecten komen uit Gerards Drive-map *Lou fotomateriaal website*, en wel uit zijn eigen "web"-selectie per klantmap. De mappen heten op de site bewust niet naar de klant; projecten hebben een beschrijvende titel. Het jaartal komt uit de opnamedatum van de foto's. **Plaats en doorlooptijd staan nog leeg** — die zijn nergens vastgelegd; vul ze in de bewerkomgeving in zodra Gerard ze doorgeeft, dan verschijnen ze vanzelf.

Nog niet verwerkt zijn de vier grote fotodumps in de Drive-map (*Becker*, *JPEG*, *de kreij badk jpg*, *de kreij toilet1 jpg*, samen ~185 foto's) en de RAW-bestanden (`.ARW`), waar een browser niets mee kan.

Foto's toevoegen: zet ze in `assets/projecten/<slug>/`, genummerd (`01.jpg`, `02.jpg`) — de eerste is de omslagfoto. Een nieuw project voeg je toe aan `content/projecten.json`, waarbij `slug` gelijk moet zijn aan de mapnaam.

Voor het dagelijks beheer is dat allemaal niet nodig: zie `OVERDRACHT.md` voor de bewerkomgeving.

## Nog regelen

- [ ] **FormSubmit activeren.** Doe één testinzending op de live site en klik op de link in de activatiemail aan info@debadgast.nl.
- [ ] **Plaats en doorlooptijd per project invullen** via de bewerkomgeving.
- [ ] **Projecttitels en -omschrijvingen laten nakijken door Gerard.** Ze zijn geschreven op wat op de foto's te zien is, niet op zijn eigen aantekeningen.
- [ ] **De vier grote fotodumps verwerken** (Becker, JPEG, de Kreij ×2) — daaruit moet nog een selectie gemaakt worden.
