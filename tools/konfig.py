# -*- coding: utf-8 -*-
"""Společné konstanty generátoru a kontroly webu CT-GenAI.

Rozpis zkoušky, kapitoly a studijní cíle (LO) se čtou z tools/lo.json,
aby generátor i kontrola pracovaly se stejnými čísly.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

NASTROJE = Path(__file__).resolve().parent
KOREN = NASTROJE.parent
TESTDATA = NASTROJE / "_testdata"
ASSETS_ZDROJ = NASTROJE / "assets"

NAZEV_WEBU = "ISTQB CT-GenAI"
PODNAZEV_WEBU = "česká studijní příručka"
PREFIX = "genai-"  # localStorage, aby se stav nemíchal s webem CTFL

SLOV_ZA_MINUTU_CTENI = 170
SLOV_ZA_MINUTU_POSLECHU = 145

VARIANTY = ["vyklad", "zkracena"]
VARIANTA_NAZEV = {"vyklad": "Plný výklad", "zkracena": "Zkrácená verze"}
VARIANTA_POPIS = {
    "vyklad": "Souvislý výklad kapitoly s příklady z praxe a doplňky nad rámec sylabu.",
    "zkracena": "Jen to, co je nutné znát ke zkoušce. K rychlému opakování.",
}

DRUHY_BLOKU = {
    "lo": "Studijní cíle (learning objectives)",
    "praxe": "Příklad z praxe",
    "nad-ramec": "Nad rámec sylabu",
    "zkouska": "Pozor u zkoušky",
    "pojem": "Pojem",
}

# Sekce Praxe (PRAVIDLA, kap. 7b): bloky navíc k DRUHY_BLOKU, povinný frontmatter, skupiny modulů.
DRUHY_BLOKU_PRAXE = {
    "pozor": "Pozor",
    "cviceni": "Cvičení",
    "krok": "Krok",
}
PRAXE_POVINNA_POLE = ["modul", "nazev", "podtitul", "cas", "uroven", "nastroje", "kapitoly", "zdroje"]
PRAXE_UROVNE = ["začátečník", "středně pokročilý", "pokročilý"]
# (klíč, název, popis, klíčová slova pro zařazení modulu bez pole „skupina“). Pořadí = pořadí na stránce;
# při odhadu skupiny se klíčová slova zkoušejí v pořadí PRAXE_ODHAD.
PRAXE_SKUPINY = [
    ("chat", "Nástroje v chatu",
     "Chatboti a aplikace bez programování: prompty pro testovací úlohy, práce s dokumenty, lokální modely.",
     ["chatgpt", "copilot chat", "microsoft copilot", "notebooklm", "gpt4all", "ollama", "contextqa", "chat"]),
    ("ide", "AI v IDE a agenti",
     "GitHub Copilot ve vývojovém prostředí, MCP servery, Claude Code a skills, n8n a další agenti.",
     ["github copilot", "mcp", "claude code", "agent", "skills", "n8n", "vs code", "intellij", "pycharm"]),
    ("python", "Automatizace v Pythonu",
     "Volání LLM z Pythonu přes API a testovací framework s Behave a Playwright.",
     ["python", "behave", "openai api", "anthropic api", "api z pythonu", "pytest", "sdk"]),
    ("ci", "CI/CD",
     "Spouštění testů a evaluací v Jenkinsu a GitHub Actions, kontejnery.",
     ["jenkins", "github actions", "ci/cd", "docker", "pipeline"]),
]
PRAXE_ODHAD = ["ci", "ide", "python", "chat"]
PRAXE_KLIC_HOTOVO = PREFIX + "praxe-hotovo"

PISMENA = "abcdef"
CELKEM_OTAZEK = 40
CELKEM_BODU = 46
HRANICE_BODU = 30
MINUT = 60
MINUT_PRODLOUZENO = 75

_LO = json.loads((NASTROJE / "lo.json").read_text(encoding="utf-8"))

KAPITOLY: dict[int, dict] = {int(k): v for k, v in _LO["kapitoly"].items()}
ODDILY_EN: dict[str, str] = _LO["oddily"]
LO_SEZNAM: list[dict] = _LO["lo"]
LO_INFO: dict[str, dict] = {x["lo"]: x for x in LO_SEZNAM}
# Rozpis: LO -> počet otázek ve zkoušce
ROZPIS: dict[str, int] = {x["lo"]: x["otazek"] for x in LO_SEZNAM}


def body_lo(lo: str) -> int:
    return 2 if LO_INFO[lo]["k"] == "K3" else 1


assert sum(ROZPIS.values()) == CELKEM_OTAZEK, "rozpis musí mít 40 otázek"
assert sum(n * body_lo(lo) for lo, n in ROZPIS.items()) == CELKEM_BODU, "rozpis musí mít 46 bodů"


def kapitola_lo(lo: str) -> int:
    return int(lo.replace("GenAI-", "").split(".")[0])


# --- pomocné ---------------------------------------------------------------

_SLOVO = re.compile(r"\w", re.UNICODE)


def pocet_slov(text: str) -> int:
    """Slovo = token oddělený mezerami, který obsahuje aspoň jedno písmeno nebo číslici.

    Samostatná interpunkce (pomlčka, šipka, hvězdička) se nepočítá, takže výsledek
    nezávisí na tom, jak se značkování převede na HTML.
    """
    return sum(1 for t in text.split() if _SLOVO.search(t))


def bez_diakritiky(text: str) -> str:
    rozlozeno = unicodedata.normalize("NFKD", text)
    return "".join(z for z in rozlozeno if not unicodedata.combining(z))


def slug(text: str) -> str:
    zaklad = bez_diakritiky(text).lower()
    zaklad = re.sub(r"[^a-z0-9]+", "-", zaklad).strip("-")
    return zaklad or "oddil"


def kotva_oddilu(cislo: str) -> str:
    return "oddil-" + cislo.replace(".", "-")


def kotva_lo(lo: str) -> str:
    return "lo-" + lo.replace("GenAI-", "").replace(".", "-")


@dataclass
class Cesty:
    """Odkud se čtou data a kam se píše web (normální běh nebo --testdata)."""

    zdroj: Path
    web: Path
    testdata: bool = False

    @property
    def obsah(self) -> Path:
        return self.zdroj / "obsah"

    @property
    def data(self) -> Path:
        return self.zdroj / "data"

    @property
    def readme(self) -> Path:
        return self.zdroj / "README.md"


def cesty(argv: list[str] | None = None) -> Cesty:
    argv = sys.argv[1:] if argv is None else argv
    if "--testdata" in argv:
        return Cesty(zdroj=TESTDATA, web=TESTDATA / "web", testdata=True)
    return Cesty(zdroj=KOREN, web=KOREN / "web")


def nacti_json(cesta: Path, varovani: list[str]):
    """Načte JSON; chybějící nebo rozbitý soubor vrátí None a zapíše varování."""
    if not cesta.exists():
        return None
    try:
        return json.loads(cesta.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError) as chyba:
        varovani.append(f"{cesta.name}: nejde načíst ({chyba}) — vynecháno")
        return None


def soubory_kapitol(slozka: Path) -> list[tuple[int, Path]]:
    """data/<druh>/kapitola-N.json seřazené podle N."""
    vysledek = []
    if not slozka.exists():
        return vysledek
    for p in slozka.glob("kapitola-*.json"):
        m = re.fullmatch(r"kapitola-(\d+)\.json", p.name)
        if m:
            vysledek.append((int(m.group(1)), p))
    return sorted(vysledek)
