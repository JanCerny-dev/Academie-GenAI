# -*- coding: utf-8 -*-
"""Načtení výkladů obsah/kapitola-N/{vyklad,zkracena}.md (PRAVIDLA, kap. 5 a 6)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import markdown_min
from konfig import KAPITOLY, VARIANTY, pocet_slov


@dataclass
class Dokument:
    kapitola: int
    varianta: str
    nadpis: str
    podtitul: str
    html: str
    oddily: list = field(default_factory=list)  # markdown_min.Oddil
    lo: list = field(default_factory=list)
    pojmy: list = field(default_factory=list)
    slova_zdroje: int = 0
    zdroj: Path | None = None

    @property
    def oddily_h2(self):
        return [o for o in self.oddily if o.uroven == 2]


def nacti(cesta: Path, kapitola: int, varianta: str, varovani: list[str]) -> Dokument:
    surovy = cesta.read_text(encoding="utf-8-sig")
    meta, telo = markdown_min.frontmatter(surovy)
    popis = f"{cesta.parent.name}/{cesta.name}"
    if not meta:
        varovani.append(f"{popis}: chybí frontmatter (---) — nadpis se vezme z konfigurace")
    if meta.get("kapitola") and meta["kapitola"] != str(kapitola):
        varovani.append(f"{popis}: frontmatter kapitola={meta['kapitola']} nesedí se složkou")
    if meta.get("varianta") and meta["varianta"] != varianta:
        varovani.append(f"{popis}: frontmatter varianta={meta['varianta']} nesedí s názvem souboru")
    nadpis = meta.get("nadpis") or KAPITOLY[kapitola]["cz"]
    podtitul = meta.get("podtitul", "")
    v = markdown_min.prevod(telo)
    varovani.extend(f"{popis}: {x}" for x in v.varovani)
    slova = pocet_slov(nadpis) + pocet_slov(podtitul) + pocet_slov(markdown_min.text_pro_pocet(telo))
    return Dokument(kapitola=kapitola, varianta=varianta, nadpis=nadpis, podtitul=podtitul,
                    html=v.html, oddily=v.oddily, lo=v.lo, pojmy=v.pojmy,
                    slova_zdroje=slova, zdroj=cesta)


def nacti_vse(slozka_obsahu: Path, varovani: list[str]) -> dict[tuple[int, str], Dokument]:
    dokumenty: dict[tuple[int, str], Dokument] = {}
    if not slozka_obsahu.exists():
        varovani.append(f"složka {slozka_obsahu} neexistuje — kapitoly se nevygenerují")
        return dokumenty
    for slozka in sorted(slozka_obsahu.glob("kapitola-*")):
        m = re.fullmatch(r"kapitola-(\d+)", slozka.name)
        if not m or int(m.group(1)) not in KAPITOLY:
            continue
        k = int(m.group(1))
        for varianta in VARIANTY:
            cesta = slozka / f"{varianta}.md"
            if cesta.exists() and cesta.stat().st_size > 0:
                dokumenty[(k, varianta)] = nacti(cesta, k, varianta, varovani)
    for k in KAPITOLY:
        for varianta in VARIANTY:
            if (k, varianta) not in dokumenty:
                varovani.append(f"kapitola-{k}/{varianta}.md zatím neexistuje — stránka vynechána")
    return dokumenty


def mapa_oddilu(dokumenty: dict) -> dict[str, tuple[str, str]]:
    """Číslo oddílu -> (název, odkaz relativně ke kořeni webu). Preferuje plný výklad."""
    mapa: dict[str, tuple[str, str]] = {}
    for varianta in reversed(VARIANTY):  # vyklad přepíše zkracenou
        for (k, v), d in sorted(dokumenty.items()):
            if v != varianta:
                continue
            for o in d.oddily:
                if o.cislo:
                    mapa[o.cislo] = (o.text, f"kapitola-{k}/{v}.html#{o.kotva}")
    return mapa


def odkaz_na_oddil(oddil: str, mapa: dict, dokumenty: dict) -> dict:
    """Oddíl "2.2.3" -> nejbližší existující oddíl (2.2.3, 2.2, jinak stránka kapitoly)."""
    casti = [c for c in (oddil or "").replace("GenAI-", "").split(".") if c]
    for delka in range(len(casti), 0, -1):
        klic = ".".join(casti[:delka])
        if klic in mapa:
            nazev, href = mapa[klic]
            return {"c": oddil, "nazev": nazev, "href": href}
    if casti and casti[0].isdigit():
        k = int(casti[0])
        for v in VARIANTY:
            if (k, v) in dokumenty:
                return {"c": oddil, "nazev": "", "href": f"kapitola-{k}/{v}.html"}
    return {"c": oddil, "nazev": "", "href": ""}
