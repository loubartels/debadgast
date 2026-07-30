# De Badgast — website

One-pager website voor strandpaviljoen **De Badgast**, gebouwd volgens de [Claude Design Cursus](https://github.com/novusordos666/claude-design-cursus)-methode: eerst een `design.md` als merk-fundament, daarna een one-pager met één verhaallijn (*aankomen → thuisvoelen → proeven → blijven*).

## Bestanden

| Bestand | Wat |
|---------|-----|
| `design.md` | Het merk-fundament: kleuren, typografie, vormtaal, tone of voice. Gebruik in elke design-prompt: **"use my design.md"**. |
| `index.html` | De complete one-pager (HTML + CSS + JS in één bestand, geen build stap nodig). |

## Lokaal bekijken

```bash
python3 -m http.server 8000
```

Open daarna `http://localhost:8000`.

## Live zetten

De site is één statisch bestand, dus alles werkt:

- **Vercel:** `vercel` in deze map (zie Les 6 van de cursus)
- **GitHub Pages:** Settings → Pages → deploy vanaf deze branch

## Nog invullen

De teksten zijn een startpunt. Check vooral even:

- [ ] Openingstijden (sectie *Praktisch*)
- [ ] Locatie/strandopgang (sectie *Praktisch*)
- [ ] E-mailadres — nu `hallo@debadgast.nl` als placeholder
- [ ] Eventueel echte foto's of video in de hero (Les 5 van de cursus)
