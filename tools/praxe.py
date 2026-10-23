# -*- coding: utf-8 -*-
"""Sekce Praxe: moduly obsah/praxe/NN-slug.md -> web/praxe/NN-slug.html a rozcestník web/praxe.html.

Formát modulu: PRAVIDLA_ZPRACOVANI.md, kap. 7b. Zvláštní soubory ve stejné složce:
  tahak.md    tahák nástrojů (modul: 0)
  projekt.md  závěrečný projekt skupiny (modul: 99)

Odkaz na jiný modul se v Markdownu píše [text](modul:klicove-slovo). Generátor ho nasměruje
na modul, jehož název souboru, název nebo nástroje klíčové slovo obsahují. Když takový modul
zatím není, vykreslí se jen text (bez odkazu), takže stránka funguje i v rozpracovaném stavu.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import markdown_min
from konfig import (KAPITOLY, PRAXE_ODHAD, PRAXE_POVINNA_POLE, PRAXE_SKUPINY, PRAXE_UROVNE,
                    SLOV_ZA_MINUTU_CTENI, bez_diakritiky, pocet_slov, slug)
from markdown_min import inline
from rozvrzeni import Web, a, e, tlacitko_splneno

ZVLASTNI = {"tahak": (0, "Tahák nástrojů"), "projekt": (99, "Závěrečný projekt")}
_SOUBOR = re.compile(r"(\d{2})-[a-z0-9][a-z0-9-]*")
_ODKAZ_MODUL = re.compile(r'<a href="modul:([^"]+)">(.*?)</a>', re.S)
NAZEV_SKUPINY = {k: n for k, n, _, _ in PRAXE_SKUPINY}


def minuty(slov: int) -> int:
    return max(1, round(slov / SLOV_ZA_MINUTU_CTENI))


def cesky_pocet(n: int, jedna: str, dve: str, pet: str) -> str:
    return jedna if n == 1 else dve if 2 <= n <= 4 else pet


@dataclass
class Modul:
    soubor: Path
    stem: str
    cislo: int | None
    meta: dict
    nazev: str
    podtitul: str
    html: str
    oddily: list = field(default_factory=list)
    cviceni: list = field(default_factory=list)  # [(id, název)]
    slova_zdroje: int = 0
    kapitoly: list = field(default_factory=list)
    skupina: str = "chat"

    @property
    def zvlastni(self) -> str:
        return self.stem if self.stem in ZVLASTNI else ""

    @property
    def oddily_h2(self):
        return [o for o in self.oddily if o.uroven == 2]

    @property
    def stranka(self) -> str:
        """Cesta stránky relativně ke kořeni webu."""
        return f"praxe/{self.stem}.html"


# --- frontmatter ------------------------------------------------------------


def kapitoly_z_meta(hodnota: str) -> list[int]:
    return [int(x) for x in re.findall(r"\d+", hodnota or "")]


def ocekavane_cislo(stem: str) -> int | None:
    if stem in ZVLASTNI:
        return ZVLASTNI[stem][0]
    m = _SOUBOR.fullmatch(stem)
    return int(m.group(1)) if m else None


def kontrola_meta(meta: dict, stem: str) -> tuple[list[str], list[str]]:
    """(chyby, varování) frontmatteru. Chyby hlásí check_site.py, build je vypíše jako varování."""
    chyby: list[str] = []
    varovani: list[str] = []
    for pole in PRAXE_POVINNA_POLE:
        if not str(meta.get(pole, "")).strip():
            chyby.append(f"frontmatter: chybí pole „{pole}“")
    cislo = (meta.get("modul") or "").strip()
    ocekavane = ocekavane_cislo(stem)
    if cislo and not cislo.isdigit():
        chyby.append(f"frontmatter: modul={cislo} není číslo")
    elif cislo and ocekavane is not None and int(cislo) != ocekavane:
        chyby.append(f"frontmatter: modul={cislo} nesedí s názvem souboru (čeká se {ocekavane})")
    if ocekavane is None:
        varovani.append("název souboru neodpovídá vzoru NN-slug.md (ani tahak.md / projekt.md)")
    for k in kapitoly_z_meta(meta.get("kapitoly", "")):
        if k not in KAPITOLY:
            chyby.append(f"frontmatter: kapitoly obsahují neexistující kapitolu {k}")
    uroven = (meta.get("uroven") or "").strip()
    if uroven and uroven not in PRAXE_UROVNE:
        varovani.append(f"frontmatter: úroveň „{uroven}“ není jedna z: {', '.join(PRAXE_UROVNE)}")
    if meta.get("skupina") and _skupina_z_pole(meta["skupina"]) is None:
        varovani.append(f"frontmatter: neznámá skupina „{meta['skupina']}“ — zařazeno podle nástrojů")
    return chyby, varovani


def _skupina_z_pole(hodnota: str) -> str | None:
    h = slug(hodnota)
    for klic, nazev, _, _ in PRAXE_SKUPINY:
        if h in (klic, slug(nazev)):
            return klic
    return None


def odhad_skupiny(meta: dict, stem: str) -> str:
    if meta.get("skupina"):
        klic = _skupina_z_pole(meta["skupina"])
        if klic:
            return klic
    # Rozhoduje první nástroj v seznamu, který patří některé skupině (hlavní nástroj se píše první).
    # Když nástroje nic neurčí, zkusí se název modulu a název souboru, pak pořadí PRAXE_ODHAD.
    slova = {k: [bez_diakritiky(s) for s in sl] for k, _, _, sl in PRAXE_SKUPINY}
    for zdroj in (meta.get("nastroje", ""), meta.get("nazev", "") + " " + stem.replace("-", " ")):
        text = bez_diakritiky(zdroj).lower()
        nalezy = []
        for poradi, klic in enumerate(PRAXE_ODHAD):
            for s in slova[klic]:
                i = text.find(s)
                if i >= 0:
                    nalezy.append((i, poradi, klic))
        if nalezy:
            return min(nalezy)[2]
    return PRAXE_ODHAD[-1]


# --- načtení ----------------------------------------------------------------


def nacti(cesta: Path, varovani: list[str]) -> Modul:
    surovy = cesta.read_text(encoding="utf-8-sig")
    meta, telo = markdown_min.frontmatter(surovy)
    stem = cesta.stem
    popis = f"praxe/{cesta.name}"
    chyby, var = kontrola_meta(meta, stem)
    varovani.extend(f"{popis}: {x}" for x in chyby + var)
    nazev = meta.get("nazev") or ZVLASTNI.get(stem, (0, stem))[1]
    podtitul = meta.get("podtitul", "")
    cislo = meta.get("modul", "").strip()
    cislo_int = int(cislo) if cislo.isdigit() else ocekavane_cislo(stem)
    v = markdown_min.prevod(telo, praxe=f"praxe-{stem}")
    varovani.extend(f"{popis}: {x}" for x in v.varovani)
    slova = pocet_slov(nazev) + pocet_slov(podtitul) + pocet_slov(markdown_min.text_pro_pocet(telo))
    return Modul(soubor=cesta, stem=stem, cislo=cislo_int, meta=meta, nazev=nazev, podtitul=podtitul,
                 html=v.html, oddily=v.oddily, cviceni=v.cviceni, slova_zdroje=slova,
                 kapitoly=[k for k in kapitoly_z_meta(meta.get("kapitoly", "")) if k in KAPITOLY],
                 skupina=odhad_skupiny(meta, stem))


def nacti_vse(slozka: Path, varovani: list[str]) -> list[Modul]:
    if not slozka.exists():
        varovani.append(f"složka {slozka} neexistuje — sekce Praxe je bez modulů")
        return []
    moduly = [nacti(p, varovani) for p in sorted(slozka.glob("*.md")) if p.stat().st_size > 0]
    moduly.sort(key=lambda m: (m.cislo if m.cislo is not None else 50, m.stem))
    ids: dict[str, str] = {}
    for m in moduly:
        for i, _ in m.cviceni:
            if i in ids:
                varovani.append(f"praxe/{m.stem}.md: id cvičení {i} je i v {ids[i]}")
            ids[i] = m.stem
    return moduly


def cislovane(moduly: list[Modul]) -> list[Modul]:
    return [m for m in moduly if not m.zvlastni]


# --- odkazy mezi moduly -----------------------------------------------------


def najdi_modul(klic: str, moduly: list[Modul], sam: Modul | None = None) -> Modul | None:
    """Pořadí: název souboru, pak název modulu, pak nástroje. Tahák a projekt jen podle názvu souboru."""
    hledat = slug(klic)
    kandidati = [m for m in moduly if m is not sam]
    for m in kandidati:
        if hledat == m.stem or hledat in m.stem:
            return m
    cislovane_ = [m for m in kandidati if not m.zvlastni]
    for m in cislovane_:
        if hledat in slug(m.nazev):
            return m
    for m in cislovane_:
        if hledat in slug(m.meta.get("nastroje", "")):
            return m
    return None


def vyres_odkazy(html: str, moduly: list[Modul], predpona: str = "", sam: Modul | None = None) -> str:
    """<a href="modul:klic">text</a> -> odkaz na stránku modulu, nebo jen text, když modul není."""
    def nahrad(mt: re.Match) -> str:
        cil = najdi_modul(mt.group(1), moduly, sam)
        if cil:
            return f'<a href="{predpona}{cil.stem}.html">{mt.group(2)}</a>'
        return f'<span class="praxe-pripravuje" title="Modul se připravuje">{mt.group(2)}</span>'
    return _ODKAZ_MODUL.sub(nahrad, html)


# --- stránka modulu ---------------------------------------------------------


def _drobky(m: Modul) -> str:
    if m.zvlastni:
        return f"Praxe · {ZVLASTNI[m.stem][1]}"
    return f"Praxe · Modul {m.cislo}" if m.cislo is not None else "Praxe"


def _strom(m: Modul) -> str:
    skupiny: list[tuple] = []
    for o in m.oddily:
        if o.uroven == 2:
            skupiny.append((o, []))
        elif skupiny:
            skupiny[-1][1].append(o)
    if not skupiny:
        return ""
    polozky = []
    for h2, deti in skupiny:
        vnorene = "".join(f'<li><a href="#{o.kotva}">{inline(o.text)}</a></li>' for o in deti)
        vnorene = f"<ol>{vnorene}</ol>" if vnorene else ""
        polozky.append(f'<li><a href="#{h2.kotva}">{inline(h2.text)}</a>{vnorene}</li>')
    nadpis = "Na této stránce" if m.zvlastni else "V tomto modulu"
    return (f'<aside class="strom" aria-label="Obsah stránky"><h2>{nadpis}</h2>'
            f"<ol>{''.join(polozky)}</ol></aside>")


def _sousede(m: Modul, moduly: list[Modul]) -> str:
    rada = cislovane(moduly)
    odkazy = []
    if m in rada:
        i = rada.index(m)
        if i > 0:
            p = rada[i - 1]
            odkazy.append(f'<a href="{p.stem}.html">← {p.cislo}. {e(p.nazev)}</a>')
        odkazy.append('<a href="../praxe.html">Všechny moduly</a>')
        if i + 1 < len(rada):
            n = rada[i + 1]
            odkazy.append(f'<a href="{n.stem}.html">{n.cislo}. {e(n.nazev)} →</a>')
    else:
        odkazy.append('<a href="../praxe.html">← Všechny moduly</a>')
        for jiny in moduly:
            if jiny.zvlastni and jiny is not m:
                odkazy.append(f'<a href="{jiny.stem}.html">{e(jiny.nazev)} →</a>')
    return f'<nav class="naradi sousede" aria-label="Sousední moduly">{"".join(odkazy)}</nav>'


def _souvislosti(web: Web, m: Modul) -> str:
    kusy = []
    if m.kapitoly:
        odkazy = []
        for k in m.kapitoly:
            cil = web.cil_kapitoly(k, "vyklad")
            popisek = f"{k}. {e(KAPITOLY[k]['kratce'])}"
            odkazy.append(f'<a href="../{cil}">{popisek}</a>' if cil else popisek)
        kusy.append(f'<span>Souvisí s kapitolami CT-GenAI: {" · ".join(odkazy)}</span>')
    zdroje = (m.meta.get("zdroje") or "").strip()
    if zdroje:
        kusy.append(f"<span>Zdroje: {e(zdroje)}</span>")
    return f'<p class="praxe-souvislosti">{"".join(kusy)}</p>' if kusy else ""


def stranka_modulu(web: Web, m: Modul, moduly: list[Modul]) -> str:
    slov = m.slova_zdroje
    meta = []
    for klic, popis in (("cas", "Čas"), ("uroven", "Úroveň"), ("nastroje", "Nástroje")):
        if m.meta.get(klic):
            meta.append(f"{popis}: {m.meta[klic]}")
    meta += [f"{slov:,} slov".replace(",", " "), f"≈ {minuty(slov)} min čtení"]
    if m.cviceni:
        meta.append(f"{len(m.cviceni)} {cesky_pocet(len(m.cviceni), 'cvičení', 'cvičení', 'cvičení')}")
    ids = " ".join(i for i, _ in m.cviceni)
    n = len(m.cviceni)
    souhrn = (f'<p class="napoveda" id="praxe-souhrn" aria-live="polite" data-praxe-cviceni="{a(ids)}">'
              f'<span data-praxe-postup>{n} cvičení</span>. Hotová cvičení si odškrtni, '
              f'stav se ukládá v tomto prohlížeči, po přihlášení i v účtu.</p>' if n else "")
    telo = f"""<div class="stranka">
<div class="layout">
<main>
<div class="zahlavi">
  <p class="drobky"><a href="../praxe.html">Praxe</a>{e(_drobky(m)[len("Praxe"):])}</p>
  <h1>{e(m.nazev)}</h1>
  <p class="podtitul">{e(m.podtitul)}</p>
  <ul class="meta">{''.join(f'<li>{e(x)}</li>' for x in meta)}</ul>
  {_souvislosti(web, m)}
  {souhrn}
</div>
<article class="{'text praxe-siroky' if m.stem == 'tahak' else 'text'}" id="text">
{vyres_odkazy(m.html, moduly, sam=m)}
</article>
{tlacitko_splneno(f"modul-{m.stem}")}
{_sousede(m, moduly)}
</main>
{_strom(m)}
</div>
</div>"""
    from konfig import NAZEV_WEBU
    return web.stranka(titulek=f"{m.nazev} | Praxe | {NAZEV_WEBU}",
                       popis=f"Praxe CT-GenAI: {m.nazev}. {m.podtitul}".strip(),
                       telo=telo, koren="../", aktivni="praxe", atributy_body=' data-kapitola="6"')


# --- rozcestník -------------------------------------------------------------


def karta_modulu(m: Modul) -> str:
    ids = " ".join(i for i, _ in m.cviceni)
    meta = " · ".join(x for x in (m.meta.get("cas", ""), m.meta.get("uroven", "")) if x)
    n = len(m.cviceni)
    pocet = f"{n} {cesky_pocet(n, 'cvičení', 'cvičení', 'cvičení')}" if n else "bez cvičení"
    cislo = f"Modul {m.cislo}" if not m.zvlastni else ("Začni tady" if m.stem == "tahak" else "Na závěr")
    nastroje = (f'<p class="praxe-nastroje">{e(m.meta["nastroje"])}</p>' if m.meta.get("nastroje") else "")
    return f"""<li class="karta praxe-karta" id="modul-{a(m.stem)}" data-praxe-cviceni="{a(ids)}">
  <p class="karta-cislo">{e(cislo)}</p>
  <h3>{e(m.nazev)}</h3>
  <p class="praxe-podtitul">{e(m.podtitul)}</p>
  <p class="karta-meta">{e(meta)}</p>
  {nastroje}
  <p class="praxe-postup" data-praxe-postup>{e(pocet)}</p>
  <ul><li><a href="{a(m.stranka)}" class="hlavni" data-splneno-odkaz="modul-{a(m.stem)}">Otevřít<span>≈ {minuty(m.slova_zdroje)} min čtení</span></a></li></ul>
</li>"""


def stranka_praxe(web: Web, moduly: list[Modul]) -> str:
    from konfig import NAZEV_WEBU
    zvlastni = [m for m in moduly if m.zvlastni]
    rada = cislovane(moduly)
    sekce = []
    karty = (f'<ul class="mrizka">{"".join(karta_modulu(m) for m in zvlastni)}</ul>' if zvlastni
             else '<p class="karta-pripravuje">Tahák a projekt se připravují.</p>')
    sekce.append('<section class="sekce" id="rozcestnik"><h2>Tahák a závěrečný projekt</h2>'
                 '<p>Tahák porovnává všechny nástroje ze sekce na jedné stránce. Závěrečný projekt spojí '
                 f'moduly do jedné aplikace, kterou jde ukázat na GitHubu.</p>{karty}</section>')
    for klic, nazev, popis, _ in PRAXE_SKUPINY:
        ve_skupine = [m for m in rada if m.skupina == klic]
        obsah = (f'<ul class="mrizka">{"".join(karta_modulu(m) for m in ve_skupine)}</ul>' if ve_skupine
                 else '<p class="karta-pripravuje">Moduly se připravují.</p>')
        sekce.append(f'<section class="sekce" id="skupina-{klic}"><h2>{e(nazev)}</h2>'
                     f'<p class="praxe-skupina-popis">{e(popis)}</p>{obsah}</section>')
    vsechna = " ".join(i for m in moduly for i, _ in m.cviceni)
    celkem = len(vsechna.split()) if vsechna else 0
    postup = (f'<p class="napoveda" id="praxe-celkem" aria-live="polite" data-praxe-cviceni="{a(vsechna)}" '
              f'data-praxe-postup>{celkem} {cesky_pocet(celkem, "cvičení", "cvičení", "cvičení")}</p>'
              if celkem else "")
    telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava">
  <p class="drobky">Praktické kurzy · mimo zkoušku</p>
  <h1>Praxe</h1>
  <p class="perex">Návody krok za krokem, jak AI nástroje použít v testování: od chatbota přes GitHub Copilot,
  MCP a Claude Code po vlastní framework v Pythonu a běh v CI. Podklady jsou dva praktické kurzy
  (Rahul Shetty: AI Tools for QA, Gianni Bruno: GenAI v Pythonu), výklad je vlastními slovy.</p>
  <p class="poznamka"><strong>Do cloudových nástrojů nikdy firemní ani klientská data.</strong>
  Cvičení běží na veřejných demo aplikacích (EventHub z kurzu, webdriveruniversity.com, goal-tracker API)
  nebo na vlastních projektech. API klíče patří do proměnných prostředí, ne do kódu.</p>
  <p>Tahle sekce na zkoušku nepřipravuje. Ukazuje, jak pojmy ze sylabu (prompt chaining, RAG, agenti, LLMOps)
  vypadají v práci. U každého modulu je odkaz na související kapitoly.</p>
  {postup}
</div>
{''.join(sekce)}
<p class="zk-zdroj">Nástroje se rychle mění. Verze, ceny a podmínky v modulech platí k datu uvedenému v textu;
před použitím je ověř u výrobce.</p>
</main>
</div>"""
    return web.stranka(titulek=f"Praxe | {NAZEV_WEBU}",
                       popis="Praktické návody k AI nástrojům v testování: chat, GitHub Copilot, MCP, Claude Code, "
                             "Python s Behave a Playwright, CI/CD.",
                       telo=telo, aktivni="praxe", atributy_body=' data-kapitola="6"')
