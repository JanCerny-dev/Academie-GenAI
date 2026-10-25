# -*- coding: utf-8 -*-
"""Minimální převodník Markdownu na HTML pro výklad CT-GenAI.

Vychází z markdown_min.py projektu CTFL a pokrývá jen to, co předepisují
PRAVIDLA_ZPRACOVANI.md, kap. 6:

  nadpisy ## a ### (číslo oddílu na začátku -> kotva oddil-2-1-1),
  odstavce, **tučně**, *kurzíva*, `kód`, [odkaz](url),
  odrážkové a číslované seznamy (vnořené o jednu úroveň),
  GFM tabulky se zarovnáním, citace >, vodorovná linka ---,
  bloky kódu ```jazyk (tlačítko Kopírovat přidává skript.js),
  bloky :::lo / :::praxe / :::nad-ramec / :::zkouska / :::pojem term="…".

Vedle HTML umí `text_pro_pocet` vytáhnout ze zdroje holý text jinou cestou
(odstraněním značek, ne převodem). Kontrola webu tak porovnává dva nezávislé
výpočty a pozná, když se při převodu ztratí text.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

from konfig import DRUHY_BLOKU, DRUHY_BLOKU_PRAXE, kotva_lo, kotva_oddilu, slug

_ODKAZ = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_TUCNE = re.compile(r"\*\*(.+?)\*\*")
_KURZIVA = re.compile(r"(?<![*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![*\w])")
_KOD = re.compile(r"`([^`]+)`")
_SEZNAM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
_NADPIS = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_BLOK = re.compile(r"^:::\s*([\w-]+)(.*)$")
_PLOT = re.compile(r"^\s*(```+|~~~+)\s*([\w+-]*)")
_CISLO = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")
_LO_RADEK = re.compile(r"^[-*]?\s*(GenAI-\d+\.\d+\.\d+)\s*\(?\s*(K[1-3])\s*\)?\s*[:–-]?\s*(.*)$")
_TERM = re.compile(r'term\s*=\s*"([^"]*)"')
_NAZEV = re.compile(r'nazev\s*=\s*"([^"]*)"')
_ATRIBUT_TEXT = re.compile(r'(?:term|nazev)\s*=\s*"([^"]*)"')  # atributy, které se vykreslí jako text


@dataclass
class Oddil:
    uroven: int  # 2 nebo 3
    cislo: str  # "2.1" nebo "" u nečíslovaných podnadpisů
    text: str
    kotva: str


@dataclass
class Vysledek:
    html: str
    oddily: list[Oddil] = field(default_factory=list)
    lo: list[str] = field(default_factory=list)
    pojmy: list[str] = field(default_factory=list)
    cviceni: list[tuple[str, str]] = field(default_factory=list)  # Praxe: (id, název)
    varovani: list[str] = field(default_factory=list)


# --- inline ---------------------------------------------------------------


def inline(text: str) -> str:
    """Escapuje HTML a přeloží inline značky. Kód se chrání před dalšími pravidly."""
    schranka: list[str] = []

    def uloz(obsah: str) -> str:
        schranka.append(obsah)
        return f"\x00{len(schranka) - 1}\x00"

    text = _KOD.sub(lambda m: uloz(f"<code>{html.escape(m.group(1), quote=False)}</code>"), text)
    text = html.escape(text, quote=False)

    def odkaz(m: re.Match) -> str:
        href = html.unescape(m.group(2))
        externi = href.startswith(("http://", "https://"))
        cil = ' target="_blank" rel="noopener noreferrer"' if externi else ""
        return uloz(f'<a href="{html.escape(href, quote=True)}"{cil}>') + m.group(1) + uloz("</a>")

    text = _ODKAZ.sub(odkaz, text)
    text = _TUCNE.sub(r"<strong>\1</strong>", text)
    text = _KURZIVA.sub(r"<em>\1</em>", text)
    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: schranka[int(m.group(1))], text)
    return text


# --- tabulky --------------------------------------------------------------


def _bunky(radek: str) -> list[str]:
    radek = radek.strip()
    if radek.startswith("|"):
        radek = radek[1:]
    if radek.endswith("|") and not radek.endswith("\\|"):
        radek = radek[:-1]
    return [b.strip().replace("\\|", "|") for b in re.split(r"(?<!\\)\|", radek)]


def _je_oddelovac(radek: str) -> bool:
    return bool(re.fullmatch(r"\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*", radek))


def _zarovnani(bunka: str) -> str:
    bunka = bunka.strip()
    if bunka.startswith(":") and bunka.endswith(":"):
        return ' style="text-align:center"'
    if bunka.endswith(":"):
        return ' style="text-align:right"'
    return ""


def _tabulka(hlavicka: str, oddelovac: str, telo: list[str]) -> str:
    hl = _bunky(hlavicka)
    zar = [_zarovnani(b) for b in _bunky(oddelovac)]
    out = ['<div class="tabulka-obal"><table>', "<thead><tr>"]
    for j, b in enumerate(hl):
        out.append(f"<th{zar[j] if j < len(zar) else ''}>{inline(b)}</th>")
    out.append("</tr></thead><tbody>")
    for r in telo:
        out.append("<tr>")
        for j, b in enumerate(_bunky(r)):
            out.append(f"<td{zar[j] if j < len(zar) else ''}>{inline(b)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


# --- seznamy --------------------------------------------------------------


def _seznam(radky: list[str]) -> str:
    """Seznam s nejvýš jednou úrovní vnoření (odsazení >= 2 mezery)."""
    polozky: list[dict] = []  # {text, cislovany, deti: [(text)], deti_cislovane}
    zakl_odsazeni = len(_SEZNAM.match(radky[0]).group(1).expandtabs(4))
    for r in radky:
        m = _SEZNAM.match(r)
        if m:
            odsazeni = len(m.group(1).expandtabs(4))
            cislovany = m.group(2)[0].isdigit()
            if odsazeni >= zakl_odsazeni + 2 and polozky:
                rodic = polozky[-1]
                rodic["deti"].append(m.group(3).strip())
                rodic.setdefault("deti_cislovane", cislovany)
            else:
                polozky.append({"text": m.group(3).strip(), "deti": [],
                                "cislovany": cislovany, "cislo": m.group(2)})
        elif polozky:
            # pokračovací řádek patří k poslední položce (nebo k jejímu dítěti)
            if polozky[-1]["deti"] and len(r) - len(r.lstrip()) >= zakl_odsazeni + 4:
                polozky[-1]["deti"][-1] += " " + r.strip()
            else:
                polozky[-1]["text"] += " " + r.strip()

    cislovany = polozky[0]["cislovany"]
    znacka = "ol" if cislovany else "ul"
    start = ""
    if cislovany:
        prvni = int(re.match(r"\d+", polozky[0]["cislo"]).group(0))
        if prvni != 1:
            start = f' start="{prvni}"'
    out = [f"<{znacka}{start}>"]
    for p in polozky:
        out.append(f"<li>{inline(p['text'])}")
        if p["deti"]:
            z = "ol" if p.get("deti_cislovane") else "ul"
            out.append(f"<{z}>" + "".join(f"<li>{inline(d)}</li>" for d in p["deti"]) + f"</{z}>")
        out.append("</li>")
    out.append(f"</{znacka}>")
    return "".join(out)


# --- převod ---------------------------------------------------------------


class _Prevod:
    def __init__(self, kotvy_lo: bool = True, praxe: str | None = None):
        self.vysledek = Vysledek(html="")
        self.pouzite: set[str] = set()
        self.kotvy_lo = kotvy_lo
        # Praxe: předpona id cvičení (např. "praxe-05-claude-code"); h2 bez čísla oddílu jsou v pořádku.
        self.praxe = praxe
        self.druhy = dict(DRUHY_BLOKU, **DRUHY_BLOKU_PRAXE) if praxe else DRUHY_BLOKU

    def unikatni(self, zaklad: str) -> str:
        kotva, n = zaklad, 2
        while kotva in self.pouzite:
            kotva = f"{zaklad}-{n}"
            n += 1
        self.pouzite.add(kotva)
        return kotva

    # bloky :::
    def blok(self, druh: str, atributy: str, vnitrek: list[str]) -> str:
        v = self.vysledek
        if druh not in self.druhy:
            v.varovani.append(f"neznámý blok :::{druh} — vykreslen jako obecná vsuvka")
            return f'<aside class="vsuvka" data-stitek="{html.escape(druh)}">{self.bloky(vnitrek)}</aside>'
        stitek = self.druhy[druh]
        if druh in DRUHY_BLOKU_PRAXE:
            return self.blok_praxe(druh, stitek, atributy, vnitrek)
        if druh == "lo":
            polozky = []
            for r in vnitrek:
                if not r.strip():
                    continue
                m = _LO_RADEK.match(r.strip())
                if m:
                    lo, k, text = m.groups()
                    v.lo.append(lo)
                    ident = ""
                    if self.kotvy_lo and kotva_lo(lo) not in self.pouzite:
                        ident = f' id="{self.unikatni(kotva_lo(lo))}"'
                    polozky.append(
                        f'<li class="lo {k.lower()}"{ident}><span class="lo-id">{html.escape(lo)}</span> '
                        f'<span class="lo-k" data-k="{k}">{k}</span> <span class="lo-text">{inline(text)}</span></li>'
                    )
                else:
                    polozky.append(f'<li class="lo">{inline(r.strip().lstrip("-* "))}</li>')
            return (f'<aside class="lo-blok" data-stitek="{stitek}" aria-label="{stitek}">'
                    f'<ul>{"".join(polozky)}</ul></aside>')
        if druh == "pojem":
            m = _TERM.search(atributy)
            term = m.group(1).strip() if m else ""
            hlava = ""
            ident = ""
            if term:
                v.pojmy.append(term)
                ident = f' id="{self.unikatni("pojem-" + slug(term))}"'
                hlava = f'<strong class="pojem-term">{inline(term)}</strong> – '
            # Termín patří do prvního odstavce definice. Samostatný anglický odstavec
            # zasekával Číst nahlas v Edge (přepíná jazyk hlasu).
            telo = self.bloky(vnitrek)
            if hlava and telo.startswith("<p>"):
                telo = "<p>" + hlava + telo[3:]
            elif hlava:
                telo = f"<p>{hlava.rstrip(' –')}</p>{telo}"
            return (f'<aside class="vsuvka vsuvka--pojem"{ident} data-stitek="{stitek}" aria-label="{stitek}">'
                    f"{telo}</aside>")
        return (f'<aside class="vsuvka vsuvka--{druh}" data-stitek="{stitek}" aria-label="{stitek}">'
                f"{self.bloky(vnitrek)}</aside>")

    def blok_praxe(self, druh: str, stitek: str, atributy: str, vnitrek: list[str]) -> str:
        """:::pozor, :::krok a :::cviceni nazev="…" (PRAVIDLA, kap. 7b).

        Text, který do stránky přidává generátor (zaškrtávátko „Hotovo“), nese data-nepocitat,
        aby ho kontrola počtu slov nebrala jako text zdroje. Štítek bloku je v CSS (data-stitek).
        """
        m = _NAZEV.search(atributy)
        nazev = m.group(1).strip() if m else ""
        hlava = f'<p class="praxe-blok-nazev">{inline(nazev)}</p>' if nazev else ""
        if druh != "cviceni":
            return (f'<aside class="vsuvka vsuvka--{druh}" data-stitek="{stitek}" aria-label="{stitek}">'
                    f"{hlava}{self.bloky(vnitrek)}</aside>")
        v = self.vysledek
        if not nazev:
            v.varovani.append(":::cviceni bez nazev=\"…\" — doplň název cvičení")
        zaklad = f"{self.praxe}-{slug(nazev) if nazev else 'cviceni-' + str(len(v.cviceni) + 1)}"
        ident = self.unikatni(zaklad)
        v.cviceni.append((ident, nazev))
        pata = (f'<p class="praxe-cviceni-pata" data-nepocitat><label class="zk-volba praxe-hotovo">'
                f'<input type="checkbox" data-praxe-hotovo="{html.escape(ident, quote=True)}"> Hotovo</label></p>')
        return (f'<aside class="vsuvka vsuvka--cviceni" id="{ident}" data-stitek="{stitek}" aria-label="{stitek}">'
                f"{hlava}{self.bloky(vnitrek)}{pata}</aside>")

    def nadpis(self, uroven: int, text: str) -> str:
        v = self.vysledek
        if uroven == 1:
            v.varovani.append(f"nadpis # „{text[:40]}“ — nadpis stránky je ve frontmatteru, vykreslen jako h2")
            uroven = 2
        uroven = min(uroven, 4)
        m = _CISLO.match(text)
        cislo = m.group(1) if m else ""
        if uroven == 2 and not cislo and not self.praxe:
            v.varovani.append(f"h2 „{text[:40]}“ nemá číslo oddílu sylabu na začátku")
        kotva = self.unikatni(kotva_oddilu(cislo) if cislo else slug(text))
        if uroven <= 3:
            v.oddily.append(Oddil(uroven=uroven, cislo=cislo, text=text, kotva=kotva))
        znak = "" if uroven > 3 else f'<a class="kotva" href="#{kotva}" aria-hidden="true" tabindex="-1"></a>'
        return f'<h{uroven} id="{kotva}">{inline(text)}{znak}</h{uroven}>'

    def bloky(self, radky: list[str]) -> str:
        out: list[str] = []
        i, n = 0, len(radky)
        while i < n:
            radek = radky[i]
            holy = radek.strip()

            if not holy:
                i += 1
                continue

            plot = _PLOT.match(radek)
            if plot:
                znaky, jazyk = plot.group(1), plot.group(2) or "text"
                obsah: list[str] = []
                i += 1
                while i < n and not radky[i].strip().startswith(znaky[:3]):
                    obsah.append(radky[i])
                    i += 1
                if i >= n:
                    self.vysledek.varovani.append("neuzavřený blok kódu ```")
                i += 1
                kod = html.escape("\n".join(obsah), quote=False)
                out.append(f'<div class="kod" data-jazyk="{html.escape(jazyk)}"><pre><code>{kod}</code></pre></div>')
                continue

            blok = _BLOK.match(holy)
            if blok and holy != ":::":
                druh, atributy = blok.group(1), blok.group(2)
                vnitrek: list[str] = []
                i += 1
                while i < n and radky[i].strip() != ":::":
                    vnitrek.append(radky[i])
                    i += 1
                if i >= n:
                    self.vysledek.varovani.append(f"neuzavřený blok :::{druh}")
                i += 1
                out.append(self.blok(druh, atributy, vnitrek))
                continue
            if holy == ":::":
                self.vysledek.varovani.append("osamocené ::: bez otevřeného bloku — vynecháno")
                i += 1
                continue

            if re.fullmatch(r"(-\s*){3,}|(\*\s*){3,}|(_\s*){3,}", holy):
                out.append("<hr>")
                i += 1
                continue

            nadpis = _NADPIS.match(holy)
            if nadpis:
                out.append(self.nadpis(len(nadpis.group(1)), nadpis.group(2)))
                i += 1
                continue

            if "|" in holy and i + 1 < n and _je_oddelovac(radky[i + 1]):
                hlavicka, oddelovac = holy, radky[i + 1]
                i += 2
                telo = []
                while i < n and radky[i].strip() and "|" in radky[i]:
                    telo.append(radky[i])
                    i += 1
                out.append(_tabulka(hlavicka, oddelovac, telo))
                continue

            if holy.startswith(">"):
                kusy = []
                while i < n and radky[i].strip().startswith(">"):
                    kusy.append(radky[i].strip()[1:].strip())
                    i += 1
                out.append(f'<blockquote><p>{inline(" ".join(k for k in kusy if k))}</p></blockquote>')
                continue

            if _SEZNAM.match(radek):
                prvni = _SEZNAM.match(radek)
                zakl = len(prvni.group(1).expandtabs(4))
                cislovany = prvni.group(2)[0].isdigit()

                def jiny_seznam(r: str) -> bool:
                    """Položka na základní úrovni jiného druhu (odrážky vs. čísla) začíná nový seznam."""
                    m = _SEZNAM.match(r)
                    return bool(m) and len(m.group(1).expandtabs(4)) <= zakl and m.group(2)[0].isdigit() != cislovany

                kus = [radek]
                i += 1
                while i < n:
                    r = radky[i]
                    if not r.strip():
                        # prázdný řádek ukončí seznam, pokud nenásleduje další položka téhož druhu
                        if i + 1 < n and _SEZNAM.match(radky[i + 1]) and not jiny_seznam(radky[i + 1]):
                            i += 1
                            continue
                        break
                    if jiny_seznam(r):
                        break
                    if _SEZNAM.match(r) or (r.startswith((" ", "\t")) and not _PLOT.match(r)):
                        kus.append(r)
                        i += 1
                        continue
                    break
                out.append(_seznam(kus))
                continue

            kusy = []
            while i < n:
                r = radky[i]
                h = r.strip()
                if (not h or _PLOT.match(r) or _NADPIS.match(h) or h.startswith((":::", ">"))
                        or _SEZNAM.match(r)
                        or ("|" in h and i + 1 < n and _je_oddelovac(radky[i + 1]))):
                    break
                kusy.append(h)
                i += 1
            if kusy:
                out.append(f'<p>{inline(" ".join(kusy))}</p>')
            else:
                i += 1
        return "\n".join(out)


def prevod(zdroj: str, *, kotvy_lo: bool = True, praxe: str | None = None) -> Vysledek:
    """praxe = předpona id cvičení; zapne bloky Praxe a vypne požadavek na číslo oddílu v h2."""
    p = _Prevod(kotvy_lo=kotvy_lo, praxe=praxe)
    radky = zdroj.replace("\r\n", "\n").split("\n")
    p.vysledek.html = p.bloky(radky)
    return p.vysledek


# --- frontmatter ----------------------------------------------------------


def frontmatter(zdroj: str) -> tuple[dict[str, str], str]:
    """Vrátí (metadata, tělo). Podporuje jen jednoduché řádky klíč: hodnota."""
    zdroj = zdroj.lstrip("﻿").replace("\r\n", "\n")
    if not zdroj.startswith("---\n"):
        return {}, zdroj
    konec = zdroj.find("\n---", 4)
    if konec < 0:
        return {}, zdroj
    meta: dict[str, str] = {}
    for r in zdroj[4:konec].split("\n"):
        if ":" in r and not r.lstrip().startswith("#"):
            k, v = r.split(":", 1)
            v = re.sub(r"\s+#.*$", "", v).strip().strip('"').strip("'")
            meta[k.strip()] = v
    zbytek = zdroj[konec + 4:]
    return meta, zbytek.split("\n", 1)[1] if "\n" in zbytek else ""


# --- holý text pro kontrolu počtu slov ------------------------------------


def text_pro_pocet(telo: str) -> str:
    """Holý text těla výkladu, získaný odstraněním značek (ne převodem na HTML)."""
    out: list[str] = []
    v_kodu = None
    radky = telo.replace("\r\n", "\n").split("\n")
    # Řádky tabulek (stejné pravidlo jako v převodu): jen v nich je „|“ oddělovač buněk.
    # Mimo tabulku zůstává, např. v `git grep -E "a|b"`.
    tabulka: set[int] = set()
    i = 0
    while i < len(radky):
        if "|" in radky[i] and i + 1 < len(radky) and _je_oddelovac(radky[i + 1]):
            j = i
            while j < len(radky) and radky[j].strip() and "|" in radky[j]:
                tabulka.add(j)
                j += 1
            i = j
        else:
            i += 1
    for cislo, r in enumerate(radky):
        plot = _PLOT.match(r)
        if v_kodu:
            if r.strip().startswith(v_kodu[:3]):
                v_kodu = None
            else:
                out.append(r)
            continue
        if plot:
            v_kodu = plot.group(1)
            continue
        h = r.strip()
        if h.startswith(":::"):
            out.extend(_ATRIBUT_TEXT.findall(h))
            continue
        if _je_oddelovac(r) and "-" in h:
            continue
        if re.fullmatch(r"(-\s*){3,}|(\*\s*){3,}|(_\s*){3,}", h):
            continue
        nadpis = bool(re.match(r"^#{1,6}\s+", h))
        h = re.sub(r"^#{1,6}\s+", "", h)
        h = re.sub(r"\s#+\s*$", "", h)
        h = re.sub(r"^(>\s*)+", "", h)
        if not nadpis:  # „### 1. Instalace“ je nadpis, ne položka seznamu: číslo zůstává
            h = re.sub(r"^([-*+]|\d+[.)])\s+", "", h)
        if cislo in tabulka:
            h = h.replace("\\|", " ").replace("|", " ")
        h = _ODKAZ.sub(lambda m: m.group(1), h)
        h = h.replace("`", "").replace("*", "")
        out.append(h)
    return "\n".join(out)
