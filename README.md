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

- **Vercel:** `vercel` in deze map
- **GitHub Pages:** Settings → Pages → deploy vanaf deze branch

## Nog regelen

- [ ] **Offerteformulier koppelen.** Het formulier toont nu alleen een bevestiging in de browser; er wordt nog niets verstuurd. Koppel een backend of formulierdienst (bijv. Formspree, of een eigen endpoint) in `assets/site.js` bij het blok "Offerteformulier".
- [ ] **Projectfoto's in hogere resolutie.** De drie carrouselfoto's (`assets/project-*.webp`) komen uit de design-tool en zijn gecomprimeerd; vervang ze eventueel door de originelen.
