# De Badgast — website

One-pager voor **De Badgast**, het badkamerrenovatiebedrijf van Gerard Bartels in Roosendaal. Gebouwd op basis van het ontwerp uit Claude Design (handoff-bundel "De Badgast hero sectie", bestand *De Badgast One-pager*).

## Bestanden

| Bestand | Wat |
|---------|-----|
| `index.html` | De one-pager: hero, over Gerard, de formule, diensten, werkwijze, projecten, recensies, offerteformulier. |
| `recensies.html` | Losse pagina met alle recensies (gelinkt vanaf de one-pager). |
| `assets/site.css` | Gedeelde stylesheet voor beide pagina's. |
| `assets/site.js` | Gedeeld gedrag: sticky header met glas-effect, fade-in bij scrollen, projectencarrousel, offerteformulier. |
| `assets/` | Logo, embleem en foto's. |
| `design.md` | Ouder merk-fundament uit de eerste (strandpaviljoen-)versie van dit project; niet meer leidend voor het huidige ontwerp. |

Geen build-stap nodig: het is een statische site (HTML + CSS + JS), met alleen Google Fonts (Manrope) als externe afhankelijkheid. Iconen (Lucide) zijn als SVG in de pagina's opgenomen.

## Lokaal bekijken

```bash
python3 -m http.server 8000
```

Open daarna `http://localhost:8000`.

## Live zetten

De site wordt automatisch naar **GitHub Pages** gepubliceerd bij elke push naar de standaardbranch (workflow: `.github/workflows/pages.yml`). URL: `https://loubartels.github.io/debadgast/`. Een eigen domein koppel je via Settings → Pages → Custom domain.

## Offerteformulier

Het formulier verstuurt via [FormSubmit](https://formsubmit.co) naar `info@debadgast.nl` (geen account nodig). **Bij de allereerste inzending stuurt FormSubmit één activatiemail naar dat adres — klik daarin op de bevestigingsknop, daarna komen aanvragen gewoon per mail binnen.** Ander e-mailadres? Pas het adres aan in `assets/site.js` bij het blok "Offerteformulier".

## Nog regelen

- [ ] **FormSubmit activeren.** Doe één testinzending op de live site en klik op de link in de activatiemail aan info@debadgast.nl.
- [ ] **Projectfoto's in hogere resolutie.** De drie carrouselfoto's (`assets/project-*.webp`) komen uit de design-tool en zijn gecomprimeerd; vervang ze eventueel door de originelen.
