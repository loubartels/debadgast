# Overdracht — website De Badgast

Dit document is voor degene die de website beheert. Je hebt geen programmeerkennis nodig voor de dagelijkse aanpassingen: tekst wijzigen en foto's toevoegen doe je gewoon in de browser.

## Wat je moet weten in één alinea

De website bestaat uit een paar losse bestanden (HTML, opmaak en foto's) die in een GitHub-repository staan: **https://github.com/loubartels/debadgast**. Zodra daar iets wijzigt, wordt de site binnen een minuut automatisch opnieuw gepubliceerd. Je hoeft dus niets te uploaden en er is geen inlogpaneel of CMS.

## Waar staat wat

| Bestand | Wat erin staat |
|---|---|
| `index.html` | De homepage: hero, over Gerard, de formule, diensten, werkwijze, projecten, recensies, offerteformulier. |
| `recensies.html` | Alle 92 recensies. |
| `projecten/*.html` | De projectpagina's. **Niet met de hand aanpassen** — die worden automatisch gemaakt (zie hieronder). |
| `tools/genereer-projecten.py` | Hierin staan de titels en gegevens van de projecten. |
| `assets/projecten/<project>/` | De foto's per project. |
| `assets/site.css` | Alle kleuren, lettertypen en opmaak. |
| `assets/site.js` | Het menu, de fotogalerij en het formulier. |

## Tekst aanpassen

1. Ga naar https://github.com/loubartels/debadgast
2. Klik op het bestand (`index.html` voor de homepage)
3. Klik op het potloodje rechtsboven (**Edit this file**)
4. Zoek de tekst die je wilt wijzigen en typ de nieuwe tekst
5. Klik op **Commit changes** → **Commit changes**

Klaar. Binnen een minuut staat het live.

> **Let op:** verander alleen tekst *tussen* de punthaken, dus `<h2>hier de tekst</h2>`. Blijf van de `<`- en `>`-tekens zelf af, anders raakt de opmaak in de war.

## Foto's toevoegen aan een bestaand project

1. Ga naar `assets/projecten/` en klik de projectmap aan (bijvoorbeeld `musters`)
2. **Add file** → **Upload files**, sleep de foto's erin
3. Geef ze een naam met een nummer: `06.jpg`, `07.jpg` — ze verschijnen op volgorde van naam
4. **Commit changes**

De projectpagina wordt automatisch bijgewerkt; de foto's staan er vanzelf bij. De laagste naam (meestal `01.jpg`) is de omslagfoto op de homepage.

**Formaat:** maak foto's niet breder dan ongeveer 1800 pixels en houd ze onder een halve megabyte, anders wordt de site traag. Elk fotobewerkingsprogramma kan dat; online kan het ook via bijvoorbeeld squoosh.app.

## Een nieuw project toevoegen

1. Maak een nieuwe map onder `assets/projecten/` met de foto's erin (bij **Add file → Create new file** typ je `assets/projecten/naam-van-project/01.jpg` — GitHub maakt de map dan aan; makkelijker is uploaden zoals hierboven)
2. Open `tools/genereer-projecten.py`
3. Kopieer een bestaand blok tussen `{` en `}` en pas het aan: `slug` moet exact gelijk zijn aan de mapnaam
4. **Commit changes**

## Een recensie toevoegen

Open `recensies.html`, kopieer een bestaand blok dat begint met `<figure class="rec-kaart"` tot en met `</figure>`, plak het bovenaan de lijst en pas de tekst, naam, plaats en datum aan.

Wil je die recensie ook op de homepage uitgelicht hebben, doe dan hetzelfde in `index.html` bij de sectie Recensies (daar staan er drie).

## Wat je beter niet zelf aanpast

- `projecten/*.html` — die worden automatisch gemaakt en jouw wijzigingen worden overschreven. Pas in plaats daarvan `tools/genereer-projecten.py` aan.
- `.github/workflows/pages.yml` — dat regelt het automatisch publiceren.

## Het offerteformulier

Aanvragen komen per e-mail binnen op **info@debadgast.nl**, via de gratis dienst [FormSubmit](https://formsubmit.co). Er is geen account en geen wachtwoord.

Wil je aanvragen naar een ander adres sturen? Pas dan in `assets/site.js` het e-mailadres aan in de regel met `formsubmit.co/ajax/`. **Let op:** bij de eerste aanvraag naar een nieuw adres stuurt FormSubmit één activatiemail; daarin moet je op de bevestigingslink klikken, anders komen aanvragen niet aan.

## Publiceren

Dat gaat vanzelf. Elke wijziging op de hoofdbranch (`claude/badgast-website-hlpmd2`) start automatisch een publicatie. Wil je zien of het gelukt is: tabblad **Actions** op GitHub — een groen vinkje betekent live.

Duurt het langer dan een paar minuten of zie je een rood kruisje, klik het dan aan; onderin staat wat er misging.

## Domein en hosting

- **Domein:** debadgast.nl, geregistreerd bij Antagonist.
- **E-mail:** blijft bij Antagonist en staat los van de website. Wat je met de website doet, raakt de e-mail niet — zolang de MX-instellingen ongemoeid blijven.
- **De website zelf:** zie het hoofdstuk *Live zetten* in `README.md`.

## Iets kwijt of stukgemaakt?

Alles is terug te draaien. Elke wijziging staat op GitHub met datum en tijd onder **Commits**. Klik een oudere versie aan en je ziet precies wat er veranderd is; via **Revert** draai je een wijziging terug.
