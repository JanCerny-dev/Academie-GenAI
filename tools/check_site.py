# -*- coding: utf-8 -*-
"""Kontrola vygenerovaného webu CT-GenAI (invarianty převzaté z webu CTFL a upravené).

Spuštění (ze složky projektu):

    python tools/check_site.py              kontroluje web/ proti obsah/ a data/
    python tools/check_site.py --testdata   kontroluje tools/_testdata/web/

Invarianty:
  1. každý zdrojový .md má svou stránku
  2. počet slov na stránce odpovídá zdroji (text se při převodu neztrácí)
  3. každý h2 má kotvu a je v bočním obsahu
  4. všechny vnitřní odkazy a kotvy někam vedou
  5. odkazované CSS a JS existují; každá třída z HTML má pravidlo v CSS
  6. každá otázka má platné „spravne“, en i cz stejný počet možností a LO z rozpisu
     (zdrojová data i vygenerované .js)
  7. cvičné zkoušky splňují rozpis: 40 otázek, 46 bodů, počty po LO
  8. žádný soubor mimo web/lokalni/ neobsahuje id ani text otázek z data/udemy/
  9. ve web/ nejsou PDF, DOCX, PPTX ani ZIP
 10. Praxe: každý obsah/praxe/*.md má stránku a kartu na praxe.html, počet slov a kotvy sedí,
     frontmatter má povinná pole, cvičení mají kotvu a zaškrtávátko

Návratový kód 0 = vše v pořádku, 1 = nalezeny chyby.
"""

from __future__ import annotations

import html as html_mod
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

import obsah as obsah_mod
import otazky as Q
import praxe as praxe_mod
from konfig import (CELKEM_BODU, CELKEM_OTAZEK, PISMENA, ROZPIS, body_lo, cesty, nacti_json,
                    pocet_slov, soubory_kapitol)

# Třídy, které do HTML přidává až JavaScript za běhu.
TRIDY_ZE_SKRIPTU = {"aktivni"}
BLOKOVE = {"p", "div", "li", "ul", "ol", "td", "th", "tr", "table", "thead", "tbody", "h1", "h2", "h3",
           "h4", "h5", "h6", "pre", "blockquote", "aside", "section", "article", "br", "hr", "dt", "dd",
           "dl", "header", "footer", "nav", "main", "details", "summary", "figure", "figcaption"}


class Rozbor(HTMLParser):
    """Text sledovaných oblastí (h1, .podtitul, #text), id, odkazy, zdroje, třídy, boční obsah."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.zasobnik: list[tuple[str, bool, bool, bool]] = []
        self.hloubka_obsahu = 0
        self.hloubka_ignorace = 0
        self.hloubka_stromu = 0
        self.text: list[str] = []
        self.identifikatory: set[str] = set()
        self.odkazy: list[str] = []
        self.zdroje: list[str] = []
        self.tridy: set[str] = set()
        self.strom_kotvy: list[str] = []
        self.h2: list[str | None] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        tridy = set((a.get("class") or "").split())
        self.tridy |= tridy
        if a.get("id"):
            self.identifikatory.add(a["id"])
        if tag == "h2" and self.hloubka_obsahu and not self.hloubka_stromu:
            self.h2.append(a.get("id"))
        if tag == "a" and a.get("href"):
            self.odkazy.append(a["href"])
            if self.hloubka_stromu:
                self.strom_kotvy.append(a["href"])
        if tag == "link" and a.get("href"):
            self.zdroje.append(a["href"])
        if tag == "script" and a.get("src"):
            self.zdroje.append(a["src"])
        if tag in ("link", "meta", "img", "input", "br", "hr"):
            if tag in BLOKOVE and self.hloubka_obsahu:
                self.text.append(" ")
            return
        sleduj = tag == "h1" or "podtitul" in tridy or a.get("id") == "text"
        strom = "strom" in tridy
        # data-nepocitat: text, který přidává generátor (např. „Hotovo“ u cvičení Praxe), ne zdroj
        ignoruj = tag in ("script", "style") or "data-nepocitat" in a
        self.hloubka_obsahu += sleduj
        self.hloubka_stromu += strom
        self.hloubka_ignorace += ignoruj
        self.zasobnik.append((tag, sleduj, strom, ignoruj))
        if tag in BLOKOVE and self.hloubka_obsahu:
            self.text.append(" ")

    def handle_endtag(self, tag):
        while self.zasobnik:
            znacka, sleduj, strom, ignoruj = self.zasobnik.pop()
            if znacka in BLOKOVE and self.hloubka_obsahu:
                self.text.append(" ")
            self.hloubka_obsahu -= sleduj
            self.hloubka_stromu -= strom
            self.hloubka_ignorace -= ignoruj
            if znacka == tag:
                break

    def handle_data(self, data):
        if self.hloubka_obsahu > 0 and self.hloubka_ignorace == 0:
            self.text.append(data)

    @property
    def slova(self) -> int:
        return pocet_slov("".join(self.text))


def rozeber(cesta: Path) -> Rozbor:
    r = Rozbor()
    r.feed(cesta.read_text(encoding="utf-8"))
    r.close()
    return r


def nacti_js(cesta: Path):
    """window.X = {…}; -> objekt."""
    text = cesta.read_text(encoding="utf-8")
    m = re.search(r"window\.\w+\s*=\s*(.*);\s*$", text, flags=re.S)
    return json.loads(m.group(1)) if m else None


def zkontroluj_web_otazku(q: dict, kde: str, chyby: list[str], lo_povinne: bool = True) -> None:
    pocty = {}
    for j in ("en", "cz"):
        t = q.get(j)
        if not t or not t.get("q") or not isinstance(t.get("m"), list) or len(t["m"]) < 2:
            chyby.append(f"{kde} {q.get('id')}: chybí {j} znění nebo možnosti")
            continue
        pocty[j] = len(t["m"])
    if len(pocty) == 2 and pocty["en"] != pocty["cz"]:
        chyby.append(f"{kde} {q.get('id')}: en má {pocty['en']} možností, cz {pocty['cz']}")
    n = min(pocty.values()) if pocty else 0
    ok = q.get("ok") or []
    if not ok or not all(isinstance(i, int) and 0 <= i < n for i in ok) or len(set(ok)) != len(ok):
        chyby.append(f"{kde} {q.get('id')}: neplatné správné odpovědi {ok}")
    if q.get("vyber") != len(ok):
        chyby.append(f"{kde} {q.get('id')}: vyber={q.get('vyber')} nesedí s počtem správných")
    if lo_povinne and q.get("lo") not in ROZPIS:
        chyby.append(f"{kde} {q.get('id')}: LO „{q.get('lo')}“ není v rozpisu")
    if q.get("lo") in ROZPIS and q.get("body") != body_lo(q["lo"]):
        chyby.append(f"{kde} {q.get('id')}: body={q.get('body')}, podle K-úrovně LO má být {body_lo(q['lo'])}")


def _udemy_otisky(data_dir: Path, varovani: list[str]) -> tuple[set[str], set[str]]:
    """Id a úryvky textů (≥ 40 znaků) otázek z data/udemy/."""
    ids: set[str] = set()
    texty: set[str] = set()
    slozka = data_dir / "udemy"
    if not slozka.exists():
        return ids, texty

    def otazky(data):
        if isinstance(data, dict) and isinstance(data.get("testy"), list):
            for t in data["testy"]:
                yield from t.get("otazky") or []
        elif isinstance(data, dict):
            yield from data.get("otazky") or []
        elif isinstance(data, list):
            yield from data

    for cesta in slozka.glob("*.json"):
        data = nacti_json(cesta, varovani)
        for q in otazky(data) if data is not None else []:
            if not isinstance(q, dict):
                continue
            if q.get("id"):
                ids.add(str(q["id"]))
            for j in ("en", "cz"):
                t = q.get(j) or {}
                holy = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_mod.unescape(t.get("q") or ""))).strip()
                if len(holy) >= 40:
                    texty.add(holy[:80])
    return ids, texty


def zkontroluj(argv: list[str] | None = None) -> int:
    c = cesty(argv)
    web = c.web
    chyby: list[str] = []
    varovani: list[str] = []

    if not web.exists():
        print(f"Složka {web} neexistuje. Spusť nejdřív: python tools/build_site.py", file=sys.stderr)
        return 1

    rozbory: dict[Path, Rozbor] = {}
    dokumenty = obsah_mod.nacti_vse(c.obsah, [])

    print("1–3) Stránky kapitol, počet slov, kotvy oddílů")
    print("-" * 72)
    for (k, v), d in sorted(dokumenty.items()):
        popis = f"kapitola-{k}/{v}.html"
        cesta = web / popis
        if not cesta.exists():
            chyby.append(f"{popis}: stránka chybí")
            continue
        r = rozeber(cesta)
        rozbory[cesta.resolve()] = r
        rozdil = r.slova - d.slova_zdroje
        print(f"  {'OK   ' if rozdil == 0 else 'CHYBA'} {popis:<26} {r.slova:>6} / {d.slova_zdroje:>6} slov")
        if rozdil:
            chyby.append(f"{popis}: počet slov nesedí — na stránce {r.slova}, ve zdroji {d.slova_zdroje} "
                         f"(rozdíl {rozdil:+d})")
        kotvy_stromu = {unquote(h.lstrip("#")) for h in r.strom_kotvy if h.startswith("#")}
        for o in d.oddily_h2:
            if o.kotva not in r.identifikatory:
                chyby.append(f"{popis}: oddíl „{o.text[:40]}“ nemá kotvu #{o.kotva}")
            if o.kotva not in kotvy_stromu:
                chyby.append(f"{popis}: oddíl „{o.text[:40]}“ chybí v bočním obsahu")
        if any(h is None for h in r.h2):
            chyby.append(f"{popis}: některý h2 v textu nemá id")

    print("\n1–3, 10) Praxe: stránky modulů, počet slov, kotvy, frontmatter, cvičení")
    print("-" * 72)
    moduly = praxe_mod.nacti_vse(c.obsah / "praxe", [])
    praxe_html = web / "praxe.html"
    rozcestnik = rozeber(praxe_html) if praxe_html.exists() else Rozbor()
    for m in moduly:
        popis = m.stranka
        chyby_meta, _ = praxe_mod.kontrola_meta(m.meta, m.stem)
        chyby.extend(f"obsah/praxe/{m.soubor.name}: {x}" for x in chyby_meta)
        cesta = web / popis
        if not cesta.exists():
            chyby.append(f"{popis}: stránka chybí")
            continue
        r = rozeber(cesta)
        rozbory[cesta.resolve()] = r
        rozdil = r.slova - m.slova_zdroje
        print(f"  {'OK   ' if rozdil == 0 and not chyby_meta else 'CHYBA'} {popis:<34} "
              f"{r.slova:>6} / {m.slova_zdroje:>6} slov, {len(m.cviceni)} cvičení")
        if rozdil:
            chyby.append(f"{popis}: počet slov nesedí — na stránce {r.slova}, ve zdroji {m.slova_zdroje} "
                         f"(rozdíl {rozdil:+d})")
        kotvy_stromu = {unquote(h.lstrip("#")) for h in r.strom_kotvy if h.startswith("#")}
        for o in m.oddily_h2:
            if o.kotva not in r.identifikatory:
                chyby.append(f"{popis}: oddíl „{o.text[:40]}“ nemá kotvu #{o.kotva}")
            if o.kotva not in kotvy_stromu:
                chyby.append(f"{popis}: oddíl „{o.text[:40]}“ chybí v bočním obsahu")
        if any(h is None for h in r.h2):
            chyby.append(f"{popis}: některý h2 v textu nemá id")
        html_stranky = cesta.read_text(encoding="utf-8")
        for ident, _ in m.cviceni:
            if ident not in r.identifikatory or f'data-praxe-hotovo="{ident}"' not in html_stranky:
                chyby.append(f"{popis}: cvičení {ident} nemá kotvu nebo zaškrtávátko")
        if "modul:" in html_stranky and re.search(r'href="modul:', html_stranky):
            chyby.append(f"{popis}: zůstal nevyřešený odkaz modul:…")
        if f"modul-{m.stem}" not in rozcestnik.identifikatory:
            chyby.append(f"praxe.html: chybí karta modulu {m.stem}")
    if not moduly:
        print("  obsah/praxe/ je prázdná nebo neexistuje — žádné moduly")

    for nazev in ("index.html", "kapitoly.html", "slovnik.html", "karticky.html", "prirazovani.html",
                  "cviceni.html", "praxe.html", "cile.html", "zkouska.html", "zdroje.html"):
        if not (web / nazev).exists():
            chyby.append(f"{nazev}: stránka chybí")

    print("\n4–5) Odkazy, kotvy, CSS a JS")
    print("-" * 72)
    vsechny_html = sorted(web.rglob("*.html"))
    for cesta in vsechny_html:
        rozbory.setdefault(cesta.resolve(), rozeber(cesta))
    pocet_odkazu = 0
    for cesta in vsechny_html:
        r = rozbory[cesta.resolve()]
        popis = cesta.relative_to(web).as_posix()
        for src in r.zdroje:
            if src.startswith(("http://", "https://")):
                continue
            if not (cesta.parent / unquote(urlparse(src).path)).exists():
                chyby.append(f"{popis}: odkazovaný soubor „{src}“ neexistuje")
        for href in r.odkazy:
            pocet_odkazu += 1
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            u = urlparse(href)
            if u.path:
                cil = (cesta.parent / unquote(u.path)).resolve()
                if not cil.exists():
                    chyby.append(f"{popis}: odkaz vede na neexistující soubor „{href}“")
                    continue
                if u.fragment and cil.suffix == ".html":
                    cr = rozbory.get(cil) or rozbory.setdefault(cil, rozeber(cil))
                    if unquote(u.fragment) not in cr.identifikatory:
                        chyby.append(f"{popis}: kotva „{href}“ v cílové stránce neexistuje")
            elif u.fragment and unquote(u.fragment) not in r.identifikatory:
                chyby.append(f"{popis}: kotva „{href}“ na stránce neexistuje")
    print(f"  prověřeno {pocet_odkazu} odkazů v {len(vsechny_html)} stránkách")

    # odkazy do výkladu ve vygenerovaných datech otázek, slovníku a cvičení
    js_soubory = sorted(web.rglob("*.js"))
    data_js = {p: nacti_js(p) for p in js_soubory if "data" in p.parent.parts}
    for p, data in data_js.items():
        if not isinstance(data, dict):
            continue
        for q in (data.get("otazky") or []) + (data.get("pojmy") or []):
            href = (q.get("kap") or {}).get("href") if isinstance(q.get("kap"), dict) else q.get("href")
            if not href:
                continue
            u = urlparse(href)
            cil = (web / unquote(u.path)).resolve()
            if not cil.exists():
                chyby.append(f"{p.relative_to(web).as_posix()} {q.get('id')}: odkaz „{href}“ vede na neexistující soubor")
            elif u.fragment and unquote(u.fragment) not in rozbory.get(cil, Rozbor()).identifikatory:
                chyby.append(f"{p.relative_to(web).as_posix()} {q.get('id')}: kotva „{href}“ neexistuje")

    styl = web / "assets" / "styl.css"
    if not styl.exists():
        chyby.append("chybí assets/styl.css")
    else:
        css = re.sub(r"/\*.*?\*/", "", styl.read_text(encoding="utf-8"), flags=re.S)
        v_css = set(re.findall(r"\.([a-zA-Z_][\w-]*)", css)) | TRIDY_ZE_SKRIPTU
        pouzite: dict[str, str] = {}
        for cesta in vsechny_html:
            for skupina in re.findall(r'class="([^"]+)"', cesta.read_text(encoding="utf-8")):
                for t in skupina.split():
                    pouzite.setdefault(t, cesta.relative_to(web).as_posix())
        for t, kde in sorted(pouzite.items()):
            if t not in v_css:
                chyby.append(f"třída „{t}“ se používá v HTML ({kde}), ale nemá pravidlo v CSS")
        print(f"  {len(pouzite)} tříd v HTML zkontrolováno proti CSS")
    if not (web / ".nojekyll").exists():
        chyby.append("chybí web/.nojekyll")

    print("\n6) Otázky — zdrojová data")
    print("-" * 72)
    pocet = 0
    for k, cesta in soubory_kapitol(c.data / "cvicne-otazky"):
        data = nacti_json(cesta, chyby)
        for q in (data or {}).get("otazky", []) if isinstance(data, dict) else []:
            pocet += 1
            for ch in Q.chyby_otazky(q):
                chyby.append(f"cvicne-otazky/{cesta.name} {q.get('id')}: {ch}")
    data = nacti_json(c.data / "vzorova-zkouska-a.json", chyby)
    for q in (data or {}).get("otazky", []) if isinstance(data, dict) else []:
        pocet += 1
        ch = Q.chyby_dodatkove(q) if q.get("navic") else Q.chyby_otazky(q)
        chyby.extend(f"vzorova-zkouska-a.json {q.get('id')}: {x}" for x in ch)
    u_var: list[str] = []
    for t in Q.nacti_udemy(c.data, u_var):
        pocet += len(t["otazky"])
    # Neplatné otázky Udemy build vynechá s varováním; tady jsou to chyby datového kontraktu.
    chyby.extend(v for v in u_var if "vynecháno" in v)
    varovani.extend(v for v in u_var if "vynecháno" not in v)
    print(f"  prověřeno {pocet} otázek")

    print("\n6–7) Otázky na webu a rozpis cvičných zkoušek")
    print("-" * 72)
    for p, data in sorted(data_js.items()):
        rel = p.relative_to(web).as_posix()
        if not isinstance(data, dict) or not isinstance(data.get("otazky"), list) or "pojmy" in data:
            continue
        if "DODATKOVE" in p.read_text(encoding="utf-8")[:300] or p.name.endswith("-dodatkove.js"):
            continue
        lokalni_test = rel.startswith("lokalni/") and p.name.startswith("test-")
        ids = Counter(q.get("id") for q in data["otazky"])
        for i, n in ids.items():
            if n > 1:
                chyby.append(f"{rel}: id {i} je v souboru {n}×")
        for q in data["otazky"]:
            zkontroluj_web_otazku(q, rel, chyby, lo_povinne=not lokalni_test)
        if re.fullmatch(r"cvicna-\d+\.js", p.name):
            otazky = data["otazky"]
            body = sum(q.get("body", 0) for q in otazky)
            po_lo = Counter(q.get("lo") for q in otazky)
            spatne = {lo: (po_lo.get(lo, 0), n) for lo, n in ROZPIS.items() if po_lo.get(lo, 0) != n}
            stav = "OK" if len(otazky) == CELKEM_OTAZEK and body == CELKEM_BODU and not spatne else "CHYBA"
            pismena = Counter(PISMENA[q["ok"][0]] for q in otazky if len(q["ok"]) == 1)
            print(f"  {stav:<5} {rel}: {len(otazky)} otázek, {body} bodů, správné {dict(sorted(pismena.items()))}")
            if pismena and max(pismena.values()) - min(pismena.get(x, 0) for x in "abcd") > 6:
                varovani.append(f"{rel}: správné odpovědi nejsou rovnoměrně mezi a–d {dict(sorted(pismena.items()))}")
            if len(otazky) != CELKEM_OTAZEK or body != CELKEM_BODU:
                chyby.append(f"{rel}: {len(otazky)} otázek / {body} bodů (má být 40 / 46)")
            for lo, (ma, mel) in spatne.items():
                chyby.append(f"{rel}: {lo} má {ma} otázek, rozpis {mel}")
        if p.name in ("otazky-vse.js", "vse.js") and data.get("rozpis") != ROZPIS:
            chyby.append(f"{rel}: rozpis v datech nesedí s tools/lo.json")

    print("\n8–9) Oddělení lokálních dat a publikovatelnost web/")
    print("-" * 72)
    ids, texty = _udemy_otisky(c.data, varovani)
    # Některé kurzy přebírají oficiální otázky Sample Exam A doslova; ty jsou veřejné, nehlásit.
    sample = c.data / "vzorova-zkouska-a.json"
    if sample.exists():
        sample_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_mod.unescape(sample.read_text(encoding="utf-8"))))
        oficialni = {t for t in texty if t in sample_text}
        if oficialni:
            print(f"  {len(oficialni)} textů z Udemy je doslova v Sample Exam A — nepočítají se jako únik")
        texty -= oficialni
    if ids or texty:
        vzor_id = re.compile(r'"id"\s*:\s*"(' + "|".join(re.escape(i) for i in sorted(ids)) + r')"') if ids else None
        lokalni = (web / "lokalni").resolve()
        nalezy = 0
        for p in web.rglob("*"):
            if not p.is_file() or lokalni in p.resolve().parents or p.suffix.lower() not in (".html", ".js", ".css", ".json", ".txt"):
                continue
            obsah = p.read_text(encoding="utf-8", errors="replace")
            holy = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_mod.unescape(obsah.replace("<\\/", "</"))))
            m = vzor_id.search(obsah) if vzor_id else None
            if m:
                nalezy += 1
                chyby.append(f"{p.relative_to(web).as_posix()}: obsahuje id otázky z Udemy „{m.group(1)}“")
            for t in texty:
                if t in holy:
                    nalezy += 1
                    chyby.append(f"{p.relative_to(web).as_posix()}: obsahuje text otázky z Udemy „{t[:50]}…“")
                    break
        print(f"  {len(ids)} id a {len(texty)} textů z data/udemy/ — mimo web/lokalni/ nalezeno {nalezy}")
    else:
        print("  data/udemy/ nejsou — nic ke kontrole")
    zakazane = [p.relative_to(web).as_posix() for p in web.rglob("*")
                if p.is_file() and p.suffix.lower() in {".pdf", ".docx", ".pptx", ".zip"}]
    if zakazane:
        chyby.append("ve web/ jsou soubory, které se nemají publikovat: " + ", ".join(zakazane))
    velikost = sum(p.stat().st_size for p in web.rglob("*") if p.is_file())
    print(f"  celkem {sum(1 for p in web.rglob('*') if p.is_file())} souborů, {velikost / 1024:.0f} kB")

    print("\n" + "=" * 72)
    for v in varovani:
        print(f"  varování: {v}")
    if chyby:
        print(f"NALEZENO {len(chyby)} CHYB:")
        for ch in chyby:
            print(f"  - {ch}")
        return 1
    print(f"VŠE V POŘÁDKU — {len(vsechny_html)} stránek, {sum(d.slova_zdroje for d in dokumenty.values()):,} slov výkladu"
          .replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(zkontroluj())
