# DESIGN.MD — De Badgast

> Het merk-fundament voor alle designwerk van De Badgast.
> Gebruik dit bestand in elke design-prompt: **"use my design.md"**.

## Merk

- **Naam:** De Badgast
- **Wat:** Strandpaviljoen aan de Nederlandse kust. Koffie in de ochtend, lunch in de middag, borrel tot zonsondergang.
- **Drie woorden:** Zonnig. Nuchter. Tijdloos.
- **Gevoel:** Een retro badplaats-affiche uit de jaren '50, maar fris en modern uitgevoerd. Geen kitsch, geen schelpjes-clipart.

## Referentie-merken

| Merk | Wat we meenemen |
|------|-----------------|
| Aesop | Rust, ruimte, typografie die het werk doet |
| Tony's Chocolonely | Durf met kleur en grote letters, Nederlandse eigenwijsheid |
| Patagonia | Eerlijke toon, geen marketingpraat |

## Kleuren

| Naam | Hex | Gebruik |
|------|-----|---------|
| Zand | `#f4ecdd` | Primaire achtergrond |
| Wit strandhuisje | `#fbf7ee` | Kaarten, lichte vlakken |
| Noordzee-inkt | `#123c4f` | Tekst, donkere secties |
| Diepzee | `#0c2b3a` | Footer, schaduwtinten |
| Zon | `#e8632c` | Accenten, CTA's, italic accentwoorden |
| Schuim | `#c9dcd2` | Subtiele lijnen en details op donker |

**Regels:** maximaal één accentkleur per sectie. Zon (`#e8632c`) is schaars — alleen voor het belangrijkste element. Nooit pure zwart of pure wit.

## Typografie

- **Display:** Fraunces (Google Fonts) — zwaar (700–900), krap gespatieerd, uppercase voor koppen. *Italic* voor accentwoorden in Zon-oranje.
- **Body & labels:** Instrument Sans — labels uppercase met ruime letter-spacing (0.14em), body 16–18px, regelafstand 1.6.
- **Nooit:** meer dan twee fontfamilies, geen script/handletter-fonts.

## Vormtaal

- Golf- en zonmotieven als **SVG-lijntekeningen**, nooit foto-cliparts.
- Grote afgeronde hoeken (24px) op kaarten, pill-vormige knoppen.
- Secties wisselen ritmisch: zand → inkt → zand → inkt (dag en zee).

## Animatie

- Secties faden subtiel omhoog bij scroll (IntersectionObserver, 500ms ease-out, 12px translate).
- Hover op knoppen: 150ms, kleur + 2px lift. Niet meer dan dat.
- `prefers-reduced-motion` altijd respecteren.

## Tone of voice

- **Altijd:** Nederlands, "je/jij", kort en warm, licht eigenwijs. Zoals een strandtent-eigenaar die je naam nog weet.
- **Nooit:** superlatieven-spam ("dé ultieme beleving"), Engels waar Nederlands kan, corporate taal.

## One-pager verhaallijn

`aankomen → thuisvoelen → proeven → blijven` — Hero → Over → Menu → Praktisch/CTA.
