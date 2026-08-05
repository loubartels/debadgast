#!/usr/bin/env python3
"""Bouwt debadgast-site.zip: precies de bestanden die op de webserver horen.

Voor hosting waar je zelf uploadt (bijvoorbeeld Antagonist). Pak de zip uit en
zet de inhoud in de webmap (meestal httpdocs of public_html).

  python3 tools/maak-uploadpakket.py
"""

import subprocess
import sys
import zipfile
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent
ZIP = WORTEL / "debadgast-site.zip"

# Wat mee moet naar de webserver. De rest (README, tools, .github, .git) is
# alleen voor het beheer en heeft op de site niets te zoeken.
MEE = ["index.html", "recensies.html", "voorwaarden.html", "404.html", ".htaccess"]
MEE_MAPPEN = ["assets", "projecten"]


def main():
    # Eerst de projectpagina's bijwerken, zodat de zip nooit achterloopt.
    subprocess.run(
        [sys.executable, str(WORTEL / "tools" / "bouw.py")],
        check=True,
        stdout=subprocess.DEVNULL,
    )

    bestanden = []
    for naam in MEE:
        pad = WORTEL / naam
        if pad.is_file():
            bestanden.append(pad)
        else:
            print(f"  overgeslagen (bestaat niet): {naam}")
    for naam in MEE_MAPPEN:
        bestanden.extend(p for p in (WORTEL / naam).rglob("*") if p.is_file())

    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for pad in sorted(bestanden):
            z.write(pad, pad.relative_to(WORTEL))

    mb = ZIP.stat().st_size / 1e6
    print(f"{ZIP.name}: {len(bestanden)} bestanden, {mb:.1f} MB")
    print("Pak uit en zet de inhoud in de webmap van de hosting.")


if __name__ == "__main__":
    main()
