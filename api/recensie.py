"""Neemt een recensie van de website aan en zet hem meteen op de site.

Dit is het enige stukje van debadgast.nl dat draait terwijl een bezoeker op de
site is. De rest is statisch: kant-en-klare bestanden, niets dat rekent. Dit
bestand is dus ook het enige waar een aanvaller iets aan heeft, en daarom staat
er hieronder meer controle dan code.

Hoe het werkt: de recensie wordt gecontroleerd, in content/recensies.json gezet
en als commit naar GitHub gestuurd. Die commit start een nieuwe publicatie op
Vercel, en ongeveer een minuut later staat de recensie op de pagina. Er wordt
niets in een database bewaard, want die is er niet.

Wat er nodig is aan instellingen (in Vercel onder Settings → Environment
Variables):

    RECENSIE_TOKEN      een fijnmazige GitHub-token, alleen voor deze
                        repository, met Contents: Read and write. Meer niet.
    RECENSIE_REPO       eigenaar/repo, standaard loubartels/debadgast
    RECENSIE_BRANCH     de tak waar Vercel van publiceert
    RECENSIE_MELDADRES  waar het seintje naartoe gaat, standaard info@debadgast.nl

Zonder RECENSIE_TOKEN weigert dit bestand elke inzending. Dat is met opzet:
liever een formulier dat zegt dat het niet lukt dan eentje dat stilletjes niets
doet.
"""

import base64
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler

REPO = os.environ.get("RECENSIE_REPO", "loubartels/debadgast")
BRANCH = os.environ.get("RECENSIE_BRANCH", "claude/badgast-website-hlpmd2")
TOKEN = os.environ.get("RECENSIE_TOKEN", "")
MELDADRES = os.environ.get("RECENSIE_MELDADRES", "info@debadgast.nl")
PAD = "content/recensies.json"

# Alleen formulieren op de site zelf. Iemand die met een eigen script langskomt
# stuurt gewoon geen Origin mee of verzint er een; dit houdt dus geen aanvaller
# tegen, wel een andere website die het formulier van hier wil misbruiken.
HERKOMST = {"https://debadgast.nl", "https://www.debadgast.nl"}

MAANDEN = ("januari", "februari", "maart", "april", "mei", "juni", "juli",
           "augustus", "september", "oktober", "november", "december")

# Hoeveel recensies er op één dag bij mogen komen. Ligt ver boven wat er in
# werkelijkheid gebeurt (een handvol per maand) en ver onder wat iemand met
# een script zou willen. Bij overschrijding gaat de rest van de dag op slot.
MAX_PER_DAG = 8

NAAM = re.compile(r"^[^\W\d_][\w .'\-]{1,59}$", re.UNICODE)
PLAATS = re.compile(r"^[^\W\d_][\w .'\-]{1,39}$", re.UNICODE)
EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,190}\.[A-Za-z]{2,24}$")

# Links zijn waar bijna alle formulierspam om draait. Een echte klant die over
# zijn badkamer schrijft heeft er geen nodig.
LINK = re.compile(
    r"https?://|www\.|\b[a-z0-9-]{2,}\.(com|net|org|nl|be|de|ru|cn|xyz|top|shop|info|biz|club|online|site)\b"
    r"|\[url|\bhref\s*=|\bmailto:",
    re.I)

# Tekens waarmee iemand HTML of een script zou willen binnensmokkelen. Het
# bouwscript ontsmet alles al voordat het op de pagina komt, dus dit is de
# tweede deur en niet de eerste. Twee deuren is hier het punt.
MARKUP = re.compile(r"<\s*[a-zA-Z/!]|&#|&[a-zA-Z]{2,10};|\bjavascript:", re.I)

ROTZOOI = re.compile(
    r"\b(viagra|cialis|casino|crypto|bitcoin|porn|xxx|sex\s*cam|loan|escort|"
    r"seo\s*service|betting|payday)\b", re.I)


class Geweigerd(Exception):
    """Inzending klopt niet. De tekst gaat terug naar de bezoeker."""

    def __init__(self, bericht, code=400):
        super().__init__(bericht)
        self.bericht = bericht
        self.code = code


# ------------------------------------------------------------ controleren ----

def tekstveld(gegevens, sleutel, naam, minimaal, maximaal):
    waarde = gegevens.get(sleutel)
    if not isinstance(waarde, str):
        raise Geweigerd(f"{naam} ontbreekt.")
    waarde = " ".join(waarde.split())
    if len(waarde) < minimaal:
        raise Geweigerd(f"{naam} is te kort.")
    if len(waarde) > maximaal:
        raise Geweigerd(f"{naam} is te lang.")
    return waarde


def controleer(gegevens):
    """Maakt van de binnengekomen gegevens een schone recensie, of weigert."""
    if gegevens.get("_honey"):
        # Onzichtbaar veld. Alleen een bot vult dit in. We doen alsof het goed
        # ging, zodat hij niet gaat zitten puzzelen waarom het niet werkte.
        raise Geweigerd("", code=200)

    naam = tekstveld(gegevens, "naam", "Uw naam", 2, 60)
    if not NAAM.match(naam):
        raise Geweigerd("Die naam kan ik niet plaatsen. Gebruik gewone letters.")

    plaats = tekstveld(gegevens, "plaats", "De plaats", 2, 40)
    if not PLAATS.match(plaats):
        raise Geweigerd("Die plaatsnaam kan ik niet plaatsen.")

    email = tekstveld(gegevens, "email", "Het e-mailadres", 5, 254)
    if not EMAIL.match(email):
        raise Geweigerd("Dat e-mailadres klopt niet.")

    tekst = tekstveld(gegevens, "recensie", "Uw ervaring", 40, 2000)

    try:
        sterren = int(gegevens.get("sterren"))
    except (TypeError, ValueError):
        raise Geweigerd("Kies hoeveel sterren u geeft.")
    if not 1 <= sterren <= 5:
        raise Geweigerd("Kies hoeveel sterren u geeft.")

    if gegevens.get("toestemming") not in (True, "ja", "on", "true"):
        raise Geweigerd("Zonder uw toestemming kan ik de recensie niet plaatsen.")

    for veld, waarde in (("uw ervaring", tekst), ("uw naam", naam), ("de plaats", plaats)):
        if LINK.search(waarde):
            raise Geweigerd(
                f"Er staat een link in {veld}. Laat die weg; dit gaat over uw badkamer.")
        if MARKUP.search(waarde):
            raise Geweigerd(f"Er staan rare tekens in {veld}.")
    if ROTZOOI.search(tekst):
        raise Geweigerd("Deze tekst gaat niet over een badkamer.")

    return {
        "naam": naam,
        "plaats": plaats,
        "datum": vandaag(),
        "sterren": sterren,
        "tekst": tekst,
    }, email


def vandaag():
    """Nederlandse datum, in Nederlandse tijd."""
    nu = datetime.now(timezone.utc) + timedelta(hours=1)
    return f"{nu.day} {MAANDEN[nu.month - 1]} {nu.year}"


# -------------------------------------------------------------- opslaan ----

def github(methode, pad, lichaam=None):
    verzoek = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{pad}",
        method=methode,
        data=json.dumps(lichaam).encode() if lichaam is not None else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "debadgast-recensies",
        },
    )
    with urllib.request.urlopen(verzoek, timeout=8) as antwoord:
        return json.loads(antwoord.read().decode())


def plaats_recensie(recensie):
    """Zet de recensie in het bestand en stuurt dat als commit naar GitHub.

    Twee mensen kunnen tegelijk op versturen drukken. GitHub weigert dan de
    tweede omdat het bestand intussen veranderd is; daarom proberen we het
    een paar keer opnieuw met de verse versie.
    """
    for poging in range(4):
        huidig = github("GET", f"contents/{urllib.parse.quote(PAD)}?ref={urllib.parse.quote(BRANCH)}")
        recensies = json.loads(base64.b64decode(huidig["content"]).decode())

        vandaag_al = sum(1 for r in recensies if r.get("datum") == recensie["datum"])
        if vandaag_al >= MAX_PER_DAG:
            raise Geweigerd(
                "Er zijn vandaag al veel recensies binnengekomen. Probeer het "
                "morgen nog eens, of mail uw recensie.", code=429)

        if any(r.get("tekst") == recensie["tekst"] for r in recensies):
            # Dubbel klikken, of iemand die het twee keer stuurt.
            return

        recensies.insert(0, recensie)
        nieuw = json.dumps(recensies, ensure_ascii=False, indent=2) + "\n"

        try:
            github("PUT", f"contents/{urllib.parse.quote(PAD)}", {
                "message": f"Recensie van {recensie['naam']} uit {recensie['plaats']}",
                "content": base64.b64encode(nieuw.encode()).decode(),
                "sha": huidig["sha"],
                "branch": BRANCH,
            })
            return
        except urllib.error.HTTPError as fout:
            if fout.code == 409 and poging < 3:
                time.sleep(0.4 * (poging + 1))
                continue
            raise

    raise Geweigerd("Het lukte even niet. Probeert u het zo nog eens.", code=503)


def meld_aan_gerard(recensie, email):
    """Seintje per mail. Mislukt dit, dan staat de recensie er nog steeds."""
    regels = [
        f"{recensie['sterren']} van de 5 sterren",
        f"{recensie['naam']} uit {recensie['plaats']}",
        f"E-mailadres (staat NIET op de site): {email}",
        "",
        recensie["tekst"],
        "",
        "Deze recensie staat inmiddels op https://debadgast.nl/recensies.html",
        "Wilt u hem eraf halen? Dat kan in de bewerkomgeving op app.pagescms.org,",
        "onder Recensies.",
    ]
    gegevens = urllib.parse.urlencode({
        "_subject": f"Nieuwe recensie op debadgast.nl ({recensie['sterren']} sterren)",
        "_captcha": "false",
        "bericht": "\n".join(regels),
    }).encode()
    verzoek = urllib.request.Request(
        f"https://formsubmit.co/ajax/{urllib.parse.quote(MELDADRES)}",
        data=gegevens, method="POST",
        headers={"Accept": "application/json", "User-Agent": "debadgast-recensies"})
    try:
        urllib.request.urlopen(verzoek, timeout=5).read()
    except Exception as fout:      # noqa: BLE001 — het seintje mag nooit de recensie tegenhouden
        print(f"Seintje naar {MELDADRES} mislukt: {fout}")


# --------------------------------------------------------------- afhandeling ----

class handler(BaseHTTPRequestHandler):

    def antwoord(self, code, gegevens):
        lichaam = json.dumps(gegevens).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(lichaam)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(lichaam)

    def do_GET(self):
        self.antwoord(405, {"fout": "Hier valt niets op te halen."})

    def do_POST(self):
        try:
            herkomst = self.headers.get("Origin")
            if herkomst and herkomst not in HERKOMST:
                raise Geweigerd("Dit formulier hoort bij debadgast.nl.", code=403)

            if not TOKEN:
                print("RECENSIE_TOKEN ontbreekt; inzending geweigerd.")
                raise Geweigerd(
                    "Het formulier is nog niet ingesteld. Mailt u uw recensie?", code=503)

            lengte = int(self.headers.get("Content-Length") or 0)
            if lengte <= 0 or lengte > 16000:
                raise Geweigerd("Er kwam niets bruikbaars binnen.")
            try:
                gegevens = json.loads(self.rfile.read(lengte).decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                raise Geweigerd("Er kwam niets bruikbaars binnen.")
            if not isinstance(gegevens, dict):
                raise Geweigerd("Er kwam niets bruikbaars binnen.")

            recensie, email = controleer(gegevens)
            plaats_recensie(recensie)
            meld_aan_gerard(recensie, email)
            self.antwoord(200, {"goed": True})

        except Geweigerd as weigering:
            if weigering.code == 200:
                self.antwoord(200, {"goed": True})
            else:
                self.antwoord(weigering.code, {"fout": weigering.bericht})
        except Exception as fout:      # noqa: BLE001
            # Nooit de echte fout naar buiten: daar staat zo weer in welke
            # repository en welke tak het is.
            print(f"Onverwachte fout bij een recensie: {fout!r}")
            self.antwoord(500, {"fout": "Het lukte even niet. Probeert u het zo nog eens."})
