# -*- coding: utf-8 -*-
"""Generátor statického webu se studijními materiály ISTQB CT-GenAI.

Spuštění (ze složky projektu):

    python tools/build_site.py              obsah/ + data/  ->  web/
    python tools/build_site.py --testdata   tools/_testdata/  ->  tools/_testdata/web/

Web funguje i otevřený z disku dvojklikem: relativní cesty, žádný fetch,
data jako .js soubory s window.X = …  (stejně jako web CTFL).
Generátor bere, co zrovna existuje; chybějící části vynechá a vypíše varování.
"""

from __future__ import annotations

import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import markdown_min
import obsah as obsah_mod
import otazky as otazky_mod
import praxe as praxe_mod
import zkousky
from konfig import (ASSETS_ZDROJ, KAPITOLY, LO_INFO, LO_SEZNAM, NAZEV_WEBU, ODDILY_EN, PREFIX,
                    SLOV_ZA_MINUTU_CTENI, SLOV_ZA_MINUTU_POSLECHU, VARIANTA_NAZEV, VARIANTA_POPIS,
                    VARIANTY, body_lo, cesty, kapitola_lo, kotva_lo, nacti_json, slug, soubory_kapitol)
from markdown_min import inline
from rozvrzeni import Web, a, e, tlacitko_splneno

ASSETS = ["styl.css", "skript.js", "zkouska.js", "procvicovani.js", "prirazovani.js",
          "karticky.js", "slovnik.js", "cile.js", "dodatkove.js", "ucet.js", "ucet-konfig.js"]


def minuty(slov: int, tempo: int) -> int:
    return max(1, round(slov / tempo))


def cesky_pocet(n: int, jedna: str, dve: str, pet: str) -> str:
    return jedna if n == 1 else dve if 2 <= n <= 4 else pet


# --- kapitoly ---------------------------------------------------------------


def prepinac_variant(web: Web, k: int, aktivni: str) -> str:
    kusy = []
    for v in VARIANTY:
        if (k, v) in web.dokumenty:
            aktualni = ' aria-current="page"' if v == aktivni else ""
            kusy.append(f'<a href="{v}.html"{aktualni}>{VARIANTA_NAZEV[v]}</a>')
        else:
            kusy.append(f'<span class="varianta-chybi">{VARIANTA_NAZEV[v]} · připravuje se</span>')
    return f'<nav class="varianty" aria-label="Varianta zpracování kapitoly {k}">{"".join(kusy)}</nav>'


def strom_oddilu(d) -> str:
    skupiny: list[tuple] = []  # (h2, [h3, …])
    for o in d.oddily:
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
    return ('<aside class="strom" aria-label="Obsah kapitoly"><h2>V této kapitole</h2>'
            f"<ol>{''.join(polozky)}</ol></aside>")


def sousedni_kapitoly(web: Web, k: int, varianta: str) -> str:
    odkazy = []
    for jiny, sipka in ((k - 1, "←"), (k + 1, "→")):
        cil = web.cil_kapitoly(jiny, varianta) if jiny in KAPITOLY else None
        if not cil:
            continue
        popisek = f"{jiny}. {e(KAPITOLY[jiny]['kratce'])}"
        text = f"{sipka} {popisek}" if sipka == "←" else f"{popisek} {sipka}"
        odkazy.append(f'<a href="../{cil}">{text}</a>')
    if not odkazy:
        return ""
    return f'<nav class="naradi sousede" aria-label="Sousední kapitoly">{"".join(odkazy)}</nav>'


def stranka_kapitoly(web: Web, d) -> str:
    slov = d.slova_zdroje
    h2 = len(d.oddily_h2)
    meta = [
        f"{slov:,} slov".replace(",", " "),
        f"≈ {minuty(slov, SLOV_ZA_MINUTU_CTENI)} min čtení",
        f"≈ {minuty(slov, SLOV_ZA_MINUTU_POSLECHU)} min poslechu",
        f"{h2} {cesky_pocet(h2, 'oddíl', 'oddíly', 'oddílů')}",
        f"{KAPITOLY[d.kapitola]['minuty']} min výuky podle sylabu",
    ]
    telo = f"""<div class="stranka">
<div class="layout">
<main>
<div class="zahlavi">
  <p class="drobky">Kapitola {d.kapitola} · {e(VARIANTA_NAZEV[d.varianta])}</p>
  <h1>{e(d.nadpis)}</h1>
  <p class="podtitul">{e(d.podtitul)}</p>
  <ul class="meta">{''.join(f'<li>{e(m)}</li>' for m in meta)}</ul>
</div>
{prepinac_variant(web, d.kapitola, d.varianta)}
<article class="text" id="text">
{d.html}
</article>
{tlacitko_splneno(f"kapitola-{d.kapitola}-{d.varianta}")}
{sousedni_kapitoly(web, d.kapitola, d.varianta)}
</main>
{strom_oddilu(d)}
</div>
</div>"""
    return web.stranka(
        titulek=f"{d.kapitola}. {KAPITOLY[d.kapitola]['kratce']} — {VARIANTA_NAZEV[d.varianta]} | {NAZEV_WEBU}",
        popis=f"{VARIANTA_NAZEV[d.varianta]} kapitoly {d.kapitola} sylabu ISTQB CT-GenAI v1.1: "
              f"{KAPITOLY[d.kapitola]['cz']}. {VARIANTA_POPIS[d.varianta]}",
        telo=telo, koren="../", aktivni="kapitoly", kapitola=d.kapitola, varianta=d.varianta)


def karta_kapitoly(web: Web, k: int) -> str:
    odkazy = []
    for v in VARIANTY:
        d = web.dokumenty.get((k, v))
        if d is None:
            continue
        trida = ' class="hlavni"' if v == "vyklad" or (k, "vyklad") not in web.dokumenty else ""
        odkazy.append(f'<li><a href="kapitola-{k}/{v}.html"{trida} data-splneno-odkaz="kapitola-{k}-{v}">'
                      f'{VARIANTA_NAZEV[v]}<span>≈ {minuty(d.slova_zdroje, SLOV_ZA_MINUTU_CTENI)} min</span></a></li>')
    if not odkazy:
        odkazy.append('<li><span class="karta-pripravuje">Výklad se připravuje</span></li>')
    lo = [x for x in LO_SEZNAM if kapitola_lo(x["lo"]) == k]
    otazek = sum(x["otazek"] for x in lo)
    bodu = sum(x["otazek"] * body_lo(x["lo"]) for x in lo)
    return f"""<li class="karta" id="kapitola-{k}" data-kapitola="{k}">
  <p class="karta-cislo">Kapitola {k}</p>
  <h3>{e(KAPITOLY[k]['cz'])}</h3>
  <p class="karta-en" lang="en">{e(KAPITOLY[k]['en'])}</p>
  <p class="karta-meta">{KAPITOLY[k]['minuty']} min výuky · {len(lo)} studijních cílů · ve zkoušce {otazek} otázek / {bodu} bodů</p>
  <ul>{''.join(odkazy)}</ul>
</li>"""


def stranka_kapitol(web: Web) -> str:
    karty = "".join(karta_kapitoly(web, k) for k in sorted(KAPITOLY))
    telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava uvod-hlava--strucna">
  <p class="drobky">Sylabus CT-GenAI v1.1</p>
  <h1>Kapitoly sylabu</h1>
  <p class="perex">Pět kapitol, každá jako plný výklad a zkrácená verze. Celkem 815 minut výuky podle sylabu.</p>
</div>
<ul class="mrizka">{karty}</ul>
</main>
</div>"""
    return web.stranka(titulek=f"Kapitoly sylabu | {NAZEV_WEBU}",
                       popis="Pět kapitol sylabu ISTQB CT-GenAI v1.1 česky s anglickou terminologií: "
                             "plný výklad a zkrácená verze.",
                       telo=telo, aktivni="kapitoly")


# --- úvod -------------------------------------------------------------------

# Řádky studijního plánu, které nepatří na veřejný web (pohovory, klienti).
_SOUKROME = re.compile(r"pohovor|\bVIG\b|\bUCB\b|Trask", re.I)


def studijni_plan(readme: Path, varovani: list[str]) -> str:
    if not readme.exists():
        varovani.append("README.md nenalezen — studijní plán na úvodní stránce chybí")
        return ""
    text = readme.read_text(encoding="utf-8-sig")
    m = re.search(r"^## Studijní plán.*?$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if not m:
        varovani.append("README.md: sekce „Studijní plán“ nenalezena")
        return ""
    radky = [r for r in m.group(1).split("\n") if not _SOUKROME.search(r)]
    # ### Týden 1 – … -> h3 (převodník dělá z ### h3); odkazy na ../ soubory mimo web vynechat
    plan = "\n".join(radky)
    plan = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]*\)", r"\1", plan)
    return markdown_min.prevod(plan).html


def prehled_postupu(web: Web, postup: dict) -> str:
    """Souhrn postupu na úvodní stránce. Čísla doplní skript.js z localStorage (po přihlášení i z účtu)."""
    kapitoly = " ".join(f"kapitola-{k}-{v}" for (k, v) in sorted(web.dokumenty))
    radky = [
        ("splneno", "kapitoly.html", "Prostudované kapitoly (výklad i zkrácená verze)", kapitoly, "", ""),
        ("mapa", "cviceni.html", "Praktická cvičení", " ".join(postup["cviceni"]), "genai-cviceni-hotovo", ""),
        ("splneno", "praxe.html", "Prostudované moduly Praxe", " ".join(postup["moduly"]), "", ""),
        ("mapa", "praxe.html", "Cvičení v Praxi", " ".join(postup["praxe"]), "genai-praxe-hotovo", ""),
        ("prirazovani", "prirazovani.html", "Přiřazovací sady na 100 %", "", "", str(postup["sad"])),
        ("karticky", "karticky.html", "Kartičky v 5. přihrádce", "", "", str(postup["pojmu"])),
        ("cile", "cile.html", "Studijní cíle, které umíš", "", "", str(postup["cilu"])),
        ("zkousky", "zkouska.html", "Splněné zkoušky", "", "", ""),
    ]
    polozky = []
    for typ, cil, popis, ids, klic, celkem in radky:
        if typ in ("splneno", "mapa") and not ids or celkem == "0":
            continue
        atr = f' data-prehled="{typ}"'
        atr += f' data-ids="{a(ids)}"' if ids else ""
        atr += f' data-klic="{klic}"' if klic else ""
        atr += f' data-celkem="{celkem}"' if celkem else ""
        polozky.append(f'<li{atr}><a href="{cil}">{e(popis)}</a><span class="prehled-hodnota" data-hodnota>–</span>'
                       f'<span class="prehled-pruh" aria-hidden="true"><span></span></span></li>')
    return f"""<section class="sekce" id="postup">
  <h2>Tvůj postup</h2>
  <ul class="prehled">{''.join(polozky)}</ul>
  <p class="napoveda">Kapitoly a moduly Praxe si označíš tlačítkem „Označit jako prostudované“ pod textem,
  cvičení zaškrtávátkem Hotovo. Testy a kartičky se počítají samy.</p>
  <p class="napoveda">Bez přihlášení se postup ukládá jen v tomto prohlížeči.</p>
  <p class="napoveda" data-ucet-info hidden>Chceš mít postup uložený na všech zařízeních, i po smazání historie
  prohlížeče? Přihlas se tlačítkem <strong>Přihlásit</strong> vpravo nahoře. Přihlásit se jde jen Google účtem.</p>
</section>"""


def stranka_uvodu(web: Web, cesty_, varovani: list[str], souhrn: dict, postup: dict) -> str:
    slov = sum(d.slova_zdroje for d in web.dokumenty.values())
    plan = studijni_plan(cesty_.readme, varovani)
    lokalni = ('<li data-jen-lokalne hidden><strong>Lokální testy</strong> — otázky z placených kurzů Udemy, jen na tomto počítači, '
               '<a href="lokalni/index.html">otevřít</a>.</li>') if web.lokalni else ""
    stav = []
    if web.dokumenty:
        stav.append(f"{len(web.dokumenty)} stránek výkladu ({slov // 1000 if slov >= 1000 else slov}"
                    f"{' tisíc' if slov >= 1000 else ''} slov)")
    for klic, popis in (("pojmu", "pojmů ve slovníku"), ("sad", "přiřazovacích sad"),
                        ("cviceni", "praktických cvičení"), ("otazek", "veřejných otázek"),
                        ("praxe", "modulů Praxe")):
        if souhrn.get(klic):
            stav.append(f"{souhrn[klic]} {popis}")
    stav_html = f'<p class="uvod-stav">Zatím hotovo: {", ".join(stav)}.</p>' if stav else ""
    telo = f"""<div class="stranka uvod">
<main id="text">

<div class="uvod-hlava">
  <p class="drobky">Specialist Level · sylabus v1.1</p>
  <h1>Příprava na ISTQB CT-GenAI v češtině</h1>
  <p class="perex">Certified Tester Testing with Generative AI: výklad česky s anglickou terminologií,
  slovník a kartičky, přiřazovací a praktická cvičení a simulace zkoušky v angličtině i češtině.</p>
  {stav_html}
</div>

{prehled_postupu(web, postup)}

<div class="uvod-sloupce">

<section class="sekce" id="zkouska-fakta">
  <h2>Co je CT-GenAI</h2>
  <p>Certifikace ISTQB pro testery, kteří používají generativní AI: prompt engineering pro testovací
  úlohy, rizika (halucinace, ochrana dat, prompt injection), infrastruktura s LLM (RAG, agenti, LLMOps)
  a zavedení GenAI do testovací organizace. Navazuje na Foundation Level.</p>
  <dl class="zkratky">
    <div><dt>40 otázek · 46 bodů</dt><dd>Otázka K3 (použití) má 2 body, ostatní 1 bod. K1 8 otázek, K2 26, K3 6.</dd></div>
    <div><dt>Hranice 30 bodů (65 %)</dt><dd>Počítají se body, ne počet správných odpovědí.</dd></div>
    <div><dt>60 minut, 75 minut</dt><dd>Prodloužení o 25 % pro ty, kdo zkoušku skládají v jiném než rodném jazyce.</dd></div>
    <div><dt>Jen anglicky</dt><dd>Zkouška není v češtině. Proto je u každého pojmu anglický termín.</dd></div>
    <div><dt>Podmínka: CTFL</dt><dd>Ke zkoušce je potřeba certifikát ISTQB Foundation Level.</dd></div>
  </dl>
</section>

<section class="sekce" id="jak-studovat">
  <h2>Jak web používat</h2>
  <p>Části webu jsou kroky jednoho postupu. Nejlépe fungují v tomto pořadí:</p>
  <ol class="postup-studia">
    <li><a href="kapitoly.html"><strong>Plný výklad</strong></a> — souvislý text kapitoly s příklady z praxe. Tudy začni.</li>
    <li><strong>Zkrácená verze</strong> — jen to, co je nutné ke zkoušce. K opakování.</li>
    <li><a href="slovnik.html"><strong>Slovník</strong></a> a <a href="karticky.html"><strong>kartičky</strong></a> —
    anglické termíny a jejich význam. Kartičky opakují Leitnerovou metodou.</li>
    <li><a href="prirazovani.html"><strong>Přiřazování</strong></a> — zařazení příkladů k pojmům a technikám.</li>
    <li><a href="cviceni.html"><strong>Praktická cvičení</strong></a> — prompty k vyzkoušení v chatbotu (hands-on objectives).</li>
    <li><a href="praxe.html"><strong>Praxe</strong></a> — návody k AI nástrojům v testování. Ke zkoušce nejsou nutné.</li>
    <li><a href="zkouska.html"><strong>Zkoušky česky</strong></a> — pochopit, na co se otázky ptají.</li>
    <li><a href="zkouska.html"><strong>Zkoušky anglicky se skrytým českým překladem</strong></a> — nácvik na ostrou zkoušku.
    Překlad odkryješ tlačítkem, jen když si nejsi jistý.</li>
    {lokalni}
  </ol>
  <p>Svůj postup po studijních cílech uvidíš na stránce <a href="cile.html">Cíle</a>,
  celkový přehled <a href="#postup">nahoře na této stránce</a>.</p>
</section>

</div>

<section class="sekce" id="praxe">
  <h2>Praxe: AI nástroje v testování</h2>
  <p>Vedle přípravy na zkoušku má web sekci <a href="praxe.html">Praxe</a>. Jsou v ní návody krok za krokem:
  prompty v chatu, GitHub Copilot a MCP, Claude Code, vlastní framework v Pythonu s Behave a Playwright
  a spuštění v CI. Patří k nim <a href="praxe.html#rozcestnik">tahák nástrojů a závěrečný projekt</a>.
  Na zkoušku se nezkouší, ale ukazuje pojmy ze sylabu v reálné práci.</p>
</section>

<section class="sekce" id="plan">
  <h2>Studijní plán na 6 týdnů</h2>
  <div class="md plan">{plan or '<p>Plán se připravuje.</p>'}</div>
</section>

<section class="sekce" id="predcitani">
  <h2>Nechte si to předčítat</h2>
  <dl class="zkratky">
    <div><dt>Ctrl + Shift + U</dt><dd>Spustí a zastaví předčítání v Microsoft Edge. Výklad je psaný tak,
    aby se dal poslouchat.</dd></div>
  </dl>
</section>

</main>
</div>"""
    return web.stranka(titulek=f"{NAZEV_WEBU} — česká studijní příručka",
                       popis="Česká studijní příručka k certifikaci ISTQB CT-GenAI (Testing with Generative AI): "
                             "výklad s anglickou terminologií, slovník, kartičky, cvičení a simulace zkoušky.",
                       telo=telo, aktivni="uvod")


# --- slovník a kartičky -----------------------------------------------------


def nacti_slovnik(cesty_, web: Web, mapa: dict, varovani: list[str]) -> list[dict]:
    sloucene: dict[str, dict] = {}
    for k, cesta in soubory_kapitol(cesty_.data / "slovnik"):
        data = nacti_json(cesta, varovani)
        if data is None:
            continue
        if not isinstance(data, list):
            varovani.append(f"slovnik/{cesta.name}: očekáván seznam pojmů — vynecháno")
            continue
        for p in data:
            if not isinstance(p, dict) or not p.get("en") or not p.get("cz") or not p.get("def"):
                varovani.append(f"slovnik/{cesta.name}: pojem bez en/cz/def ({str(p)[:50]}) — vynechán")
                continue
            kap = p.get("kap") or k
            klic = re.sub(r"\s+", " ", p["en"].strip().lower())
            oddil = str(p.get("oddil") or "")
            odkaz = obsah_mod.odkaz_na_oddil(oddil or str(kap), mapa, web.dokumenty)
            z = sloucene.get(klic)
            if z is None:
                z = sloucene[klic] = {"id": slug(p["en"]), "en": p["en"].strip(), "cz": p["cz"].strip(),
                                      "def": p["def"].strip(), "kap": [], "odkazy": [], "klicove": False,
                                      "poznamka": [], "dalsi_def": [], "dalsi_cz": []}
            else:
                if p["cz"].strip() != z["cz"] and p["cz"].strip() not in z["dalsi_cz"]:
                    z["dalsi_cz"].append(p["cz"].strip())
                if p["def"].strip() != z["def"]:
                    z["dalsi_def"].append(p["def"].strip())
            if kap not in z["kap"]:
                z["kap"].append(kap)
            if odkaz["href"] and all(o["href"] != odkaz["href"] for o in z["odkazy"]):
                z["odkazy"].append({"kap": kap, "oddil": oddil, "href": odkaz["href"]})
            z["klicove"] = z["klicove"] or bool(p.get("klicove"))
            if p.get("poznamka") and p["poznamka"] not in z["poznamka"]:
                z["poznamka"].append(p["poznamka"])
    pojmy = sorted(sloucene.values(), key=lambda z: markdown_bez(z["en"]).lower())
    for z in pojmy:
        z["kap"].sort()
    return pojmy


def markdown_bez(text: str) -> str:
    from konfig import bez_diakritiky
    return bez_diakritiky(text)


def stranka_slovniku(web: Web, pojmy: list[dict]) -> str:
    from konfig import bez_diakritiky
    polozky = []
    for z in pojmy:
        hledat = bez_diakritiky(" ".join([z["en"], z["cz"], *z["dalsi_cz"]])).lower()
        kap = " ".join(str(k) for k in z["kap"])
        odkazy = "".join(
            f'<a href="{a(o["href"])}">kap. {o["kap"]}{" · " + e(o["oddil"]) if o["oddil"] else ""} →</a>'
            for o in z["odkazy"])
        dalsi_cz = f' <span class="pojem-alt">({e(", ".join(z["dalsi_cz"]))})</span>' if z["dalsi_cz"] else ""
        dalsi_def = "".join(f'<p class="pojem-def pojem-def--dalsi">{inline(d)}</p>' for d in z["dalsi_def"])
        pozn = "".join(f'<p class="pojem-pozn">{inline(x)}</p>' for x in z["poznamka"])
        klic = '<span class="pojem-klic" title="Pojem ze seznamu Keywords v sylabu">K1</span>' if z["klicove"] else ""
        polozky.append(
            f'<li class="pojem-polozka" id="{a(z["id"])}" data-hledat="{a(hledat)}" data-kap="{kap}" '
            f'data-klicove="{1 if z["klicove"] else 0}">'
            f'<div class="pojem-hlava"><span class="pojem-en" lang="en">{e(z["en"])}</span>{klic}'
            f'<span class="pojem-cz">{e(z["cz"])}{dalsi_cz}</span></div>'
            f'<p class="pojem-def">{inline(z["def"])}</p>{dalsi_def}{pozn}'
            f'<p class="pojem-odkazy">Kapitola {", ".join(str(k) for k in z["kap"])}{" · " + odkazy if odkazy else ""}</p>'
            "</li>")
    kap_tl = "".join(f'<button type="button" class="zk-btn" data-filtr-kap="{k}" aria-pressed="false">Kapitola {k}</button>'
                     for k in sorted({k for z in pojmy for k in z["kap"]}))
    obsah_seznamu = (f'<ul class="slovnik" id="slovnik-seznam">{"".join(polozky)}</ul>'
                     if polozky else '<p class="poznamka">Slovník se připravuje.</p>')
    telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava uvod-hlava--strucna">
  <p class="drobky">Terminologie EN–CZ</p>
  <h1>Slovník pojmů</h1>
  <p class="perex">{len(pojmy)} pojmů ze všech kapitol. Anglický termín je ten, který uvidíš ve zkoušce.
  Pojmy označené <span class="pojem-klic">K1</span> jsou v seznamu Keywords sylabu a zkouší se na zapamatování.</p>
</div>
<div class="slovnik-filtr" id="slovnik-filtr" hidden>
  <label class="slovnik-hledat"><span>Hledat (EN i CZ, bez diakritiky)</span>
    <input type="search" id="slovnik-dotaz" autocomplete="off" placeholder="např. halucinace, RAG, few-shot"></label>
  <div class="zk-tlacitka">
    <button type="button" class="zk-btn" data-filtr-kap="vse" aria-pressed="true">Všechny kapitoly</button>{kap_tl}
  </div>
  <label class="zk-volba"><input type="checkbox" id="slovnik-klicove"> Jen klíčové pojmy (K1)</label>
  <p class="napoveda" id="slovnik-pocet" aria-live="polite"></p>
</div>
{obsah_seznamu}
</main>
</div>"""
    return web.stranka(titulek=f"Slovník pojmů | {NAZEV_WEBU}",
                       popis="Slovník pojmů ISTQB CT-GenAI anglicky a česky s definicemi a odkazy do výkladu.",
                       telo=telo, aktivni="slovnik", skripty=["assets/slovnik.js"])


def stranka_karticek(web: Web, pojmy: list[dict]) -> str:
    telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava uvod-hlava--strucna">
  <p class="drobky">Opakování pojmů</p>
  <h1>Kartičky</h1>
  <p class="perex">Na líci je anglický termín, na rubu český překlad a definice. Kartičky se řadí
  do pěti přihrádek (Leitnerova metoda): co umíš, posune se dál a vrací se méně často, co neumíš, jde zpět do první.</p>
  <p class="napoveda"><kbd>Mezerník</kbd> otočí kartičku, <kbd>→</kbd> umím, <kbd>←</kbd> neumím.
  Stav se ukládá jen v tomto prohlížeči.</p>
</div>
<div id="karticky" data-pocet="{len(pojmy)}">
  <noscript><p class="poznamka">Kartičky potřebují zapnutý JavaScript.</p></noscript>
</div>
</main>
</div>"""
    return web.stranka(titulek=f"Kartičky | {NAZEV_WEBU}",
                       popis="Kartičky s pojmy ISTQB CT-GenAI (EN–CZ) s opakováním Leitnerovou metodou.",
                       telo=telo, aktivni="karticky",
                       skripty=["assets/data/slovnik.js", "assets/karticky.js"])


# --- přiřazování ------------------------------------------------------------


def nacti_prirazovani(cesty_, varovani: list[str]) -> list[dict]:
    sady: list[dict] = []
    videne: set[str] = set()
    for k, cesta in soubory_kapitol(cesty_.data / "prirazovani"):
        data = nacti_json(cesta, varovani)
        if data is None:
            continue
        if not isinstance(data, list):
            varovani.append(f"prirazovani/{cesta.name}: očekáván seznam sad — vynecháno")
            continue
        for s in data:
            # Id stačí jedinečné v rámci kapitoly; na webu dostane předponu kapitoly.
            sid = f"k{k}-{s.get('id', '?')}" if isinstance(s, dict) else "?"
            chyby = []
            if not isinstance(s, dict):
                chyby.append("sada není objekt")
            else:
                for pole in ("id", "nazev", "otazka", "kat", "pol"):
                    if not s.get(pole):
                        chyby.append(f"chybí pole „{pole}“")
                if sid in videne:
                    chyby.append("duplicitní id sady")
                klice = [x[0] for x in s.get("kat") or [] if isinstance(x, list) and x]
                if len(klice) != len(set(klice)):
                    chyby.append("duplicitní klíč kategorie")
                if len(klice) > 9:
                    chyby.append("víc než 9 kategorií")
                if any(not isinstance(x, list) or len(x) < 2 for x in s.get("kat") or []):
                    chyby.append("kategorie má mít [klíč, název, (anglicky), (popis)]")
                for i, p in enumerate(s.get("pol") or []):
                    if not isinstance(p, list) or len(p) not in (3, 4):
                        chyby.append(f"položka {i}: má mít [text, kategorie, zdůvodnění]")
                    elif p[1] not in klice:
                        chyby.append(f"položka {i}: neznámá kategorie „{p[1]}“")
            if chyby:
                varovani.append(f"prirazovani/{cesta.name} {sid}: {'; '.join(chyby)} — sada vynechána")
                continue
            videne.add(sid)
            kat = [list(x) + [""] * (4 - len(x)) for x in s["kat"]]
            sady.append({"id": sid, "sek": str(s.get("sek") or k), "nazev": s["nazev"],
                         "zdroj": s.get("zdroj") or "", "otazka": s["otazka"], "kat": kat,
                         "pol": s["pol"], "kap": k})
    return sady


def stranka_prirazovani(web: Web, sady: list[dict]) -> str:
    polozek = sum(len(s["pol"]) for s in sady)
    telo = f"""<div class="stranka uvod">
<main id="text">

<section id="prehled">
  <div class="uvod-hlava">
    <p class="drobky">Procvičování</p>
    <h1>Přiřazovací cvičení</h1>
    <p class="perex">Dostaneš vždy jednu položku a zařadíš ji do správné kategorie: technika promptování,
    druh rizika, část architektury, fáze zavedení. Hned uvidíš, jestli jsi trefil, a proč.
    Na volby jde klikat, nebo mačkat čísla <kbd>1</kbd>–<kbd>9</kbd>; <kbd>Enter</kbd> posune dál.</p>
    <p class="pr-souhrn">{len(sady)} sad · {polozek} položek</p>
    <div class="pr-akce">
      <button type="button" class="pr-tl pr-tl--hlavni" id="tl-vzor" hidden>Jen položky ze vzorového testu</button>
      <button type="button" class="pr-tl" id="tl-slabe" hidden>Procvičit položky, ve kterých chybuju</button>
      <button type="button" class="pr-tl" id="tl-reset">Smazat uložené výsledky</button>
    </div>
    <p class="pr-napoveda">Výsledky se ukládají jen ve vašem prohlížeči.</p>
  </div>
  <div id="kapitoly-prirazovani">{'' if sady else '<p class="poznamka">Přiřazovací cvičení se připravují.</p>'}</div>
</section>

<section id="cviceni" class="pr-cviceni" hidden>
  <div class="pr-horni">
    <h1 id="c-nazev"></h1>
    <span class="pr-pocitadlo" id="c-pocitadlo"></span>
    <button type="button" class="pr-tl" id="c-zpet">← Přehled</button>
  </div>
  <div class="pr-lista"><span id="c-lista"></span></div>
  <div id="c-krok">
    <p class="pr-stitky"><span class="pr-stitek" id="c-stitek" hidden></span><span class="pr-vzor-znacka" id="c-vzor" hidden></span></p>
    <p class="pr-otazka" id="c-otazka"></p>
    <div class="pr-polozka" id="c-polozka"></div>
    <div class="pr-volby" id="c-volby"></div>
    <div id="c-zpetna" hidden></div>
    <div class="pr-dalsi" id="c-dalsi" hidden>
      <button type="button" class="pr-tl pr-tl--hlavni" id="c-tl-dalsi">Další →</button>
      <span class="pr-napoveda">nebo Enter</span>
    </div>
  </div>
  <div id="c-vysledek" hidden></div>
  <details class="pr-tahak">
    <summary>Tahák: co která kategorie znamená</summary>
    <dl id="c-tahak-obsah"></dl>
  </details>
</section>

<noscript><p class="poznamka">Cvičení potřebuje zapnutý JavaScript.</p></noscript>

</main>
</div>"""
    return web.stranka(titulek=f"Přiřazovací cvičení | {NAZEV_WEBU}",
                       popis="Přiřazovací cvičení k ISTQB CT-GenAI podle kapitol: ke každé položce vyberte správnou kategorii.",
                       telo=telo, aktivni="prirazovani",
                       skripty=["assets/data/prirazovani.js", "assets/prirazovani.js"])


# --- praktická cvičení ------------------------------------------------------

UROVEN_POPIS = {"H0": "H0 · ukázka", "H1": "H1 · řízené cvičení", "H2": "H2 · samostatné cvičení"}


def nacti_cviceni(cesty_, varovani: list[str]) -> list[dict]:
    vysledek = []
    videne: set[str] = set()
    for k, cesta in soubory_kapitol(cesty_.data / "cviceni"):
        data = nacti_json(cesta, varovani)
        if data is None:
            continue
        if not isinstance(data, list):
            varovani.append(f"cviceni/{cesta.name}: očekáván seznam cvičení — vynecháno")
            continue
        for c in data:
            if not isinstance(c, dict) or not c.get("id") or not c.get("nazev"):
                varovani.append(f"cviceni/{cesta.name}: cvičení bez id/nazev — vynecháno")
                continue
            if c["id"] in videne:
                varovani.append(f"cviceni/{cesta.name}: duplicitní id {c['id']} — vynecháno")
                continue
            if c.get("lo") and c["lo"] not in LO_INFO:
                varovani.append(f"cviceni/{cesta.name} {c['id']}: neznámý LO {c['lo']}")
            videne.add(c["id"])
            vysledek.append(dict(c, kap=k))
    return vysledek


def _seznam_textu(hodnota) -> list[str]:
    if isinstance(hodnota, list):
        return [str(x) for x in hodnota if str(x).strip()]
    return [str(hodnota)] if hodnota else []


def karta_cviceni(web: Web, c: dict, mapa: dict) -> str:
    uroven = str(c.get("uroven") or "").upper()
    lo = c.get("lo") or ""
    hlava = [f'<span class="cv-id">{e(c["id"])}</span>']
    if uroven:
        hlava.append(f'<span class="cv-uroven cv-{uroven.lower()}">{e(UROVEN_POPIS.get(uroven, uroven))}</span>')
    if lo:
        hlava.append(f'<a class="cv-lo" href="cile.html#{kotva_lo(lo)}">{e(lo)}</a>' if lo in LO_INFO
                     else f'<span class="cv-lo">{e(lo)}</span>')
    if c.get("cas_min"):
        hlava.append(f'<span class="cv-cas">≈ {e(c["cas_min"])} min</span>')
    if c.get("projekt"):
        hlava.append(f'<span class="cv-projekt">projekt: {e(c["projekt"])}</span>')
    casti = []
    if c.get("cil"):
        casti.append(f'<p class="cv-cil"><strong>Cíl:</strong> {inline(str(c["cil"]))}</p>')
    if c.get("zadani"):
        casti.append(f'<div class="cv-zadani">{markdown_min.prevod(str(c["zadani"]), kotvy_lo=False).html}</div>')
    kroky = _seznam_textu(c.get("kroky"))
    if kroky:
        casti.append('<h4>Kroky</h4><ol class="cv-kroky">' + "".join(f"<li>{inline(x)}</li>" for x in kroky) + "</ol>")
    if c.get("prompt"):
        casti.append('<h4>Ukázkový prompt</h4><div class="kod" data-jazyk="prompt"><pre><code>'
                     f'{e(str(c["prompt"]))}</code></pre></div>')
    sledovat = _seznam_textu(c.get("co_sledovat"))
    if sledovat:
        casti.append('<h4>Co sledovat</h4><ul class="cv-sledovat">' + "".join(f"<li>{inline(x)}</li>" for x in sledovat) + "</ul>")
    vyklad = obsah_mod.odkaz_na_oddil(lo.replace("GenAI-", ""), mapa, web.dokumenty) if lo else {"href": ""}
    odkaz = f'<a href="{a(vyklad["href"])}">Výklad k {e(lo)} →</a>' if vyklad["href"] else ""
    return f"""<li class="karta cv-karta" id="{a(c['id'])}" data-kapitola="{c['kap']}">
  <p class="cv-hlava">{' '.join(hlava)}</p>
  <h3>{inline(str(c['nazev']))}</h3>
  {''.join(casti)}
  <p class="cv-pata"><label class="zk-volba cv-hotovo"><input type="checkbox" data-hotovo="{a(c['id'])}"> Hotovo</label>{odkaz}</p>
</li>"""


def stranka_cviceni(web: Web, cviceni: list[dict], mapa: dict) -> str:
    podle = defaultdict(list)
    for c in cviceni:
        podle[c["kap"]].append(c)
    sekce = []
    for k in sorted(podle):
        karty = "".join(karta_cviceni(web, c, mapa) for c in podle[k])
        sekce.append(f'<section class="sekce" id="kapitola-{k}" data-kapitola="{k}">'
                     f'<h2><span class="pr-kapitola-cislo">{k}</span> {e(KAPITOLY[k]["cz"])}</h2>'
                     f'<ul class="cv-seznam">{karty}</ul></section>')
    telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava">
  <p class="drobky">Hands-on objectives</p>
  <h1>Praktická cvičení</h1>
  <p class="perex">Cvičení podle hands-on objectives sylabu (HO) a vlastní navíc (CV). Prompt zkopíruj
  tlačítkem Kopírovat do chatbota a porovnej výsledek s tím, co máš sledovat.</p>
  <ul class="cv-legenda">
    <li><span class="cv-uroven cv-h0">H0</span> ukázka — stačí sledovat a rozumět</li>
    <li><span class="cv-uroven cv-h1">H1</span> řízené cvičení — podle kroků</li>
    <li><span class="cv-uroven cv-h2">H2</span> samostatné cvičení — vlastní řešení</li>
  </ul>
  <p class="poznamka"><strong>Do veřejných chatbotů nevkládej klientská ani firemní data.</strong>
  Cvičení používají vymyšlená data nebo vlastní projekty. Je to i téma kapitoly 3.</p>
  <p class="napoveda" id="cv-souhrn" aria-live="polite"></p>
</div>
{''.join(sekce) or '<p class="poznamka">Praktická cvičení se připravují.</p>'}
</main>
</div>"""
    return web.stranka(titulek=f"Praktická cvičení | {NAZEV_WEBU}",
                       popis="Praktická cvičení k ISTQB CT-GenAI: prompty pro testovací úlohy, kroky a co sledovat.",
                       telo=telo, aktivni="cviceni")


# --- studijní cíle ----------------------------------------------------------


def stranka_cilu(web: Web, mapa: dict, pocty_otazek: dict[str, int]) -> str:
    sekce = []
    for k in sorted(KAPITOLY):
        los = [x for x in LO_SEZNAM if kapitola_lo(x["lo"]) == k]
        bloky = []
        oddil_pred = None
        for x in los:
            lo = x["lo"]
            oddil = ".".join(lo.replace("GenAI-", "").split(".")[:2])
            if oddil != oddil_pred:
                if oddil_pred is not None:
                    bloky.append("</ul>")
                bloky.append(f'<h3 class="cile-oddil"><span>{oddil}</span> <span lang="en">{e(ODDILY_EN.get(oddil, ""))}</span></h3><ul class="cile">')
                oddil_pred = oddil
            cislo = lo.replace("GenAI-", "")
            odkaz = obsah_mod.odkaz_na_oddil(cislo, mapa, web.dokumenty)
            akce = []
            if odkaz["href"]:
                akce.append(f'<a href="{a(odkaz["href"])}">Výklad →</a>')
            n = pocty_otazek.get(lo, 0)
            if n:
                akce.append(f'<a href="procvicovani.html?lo={a(lo)}">Procvičit ({n} {cesky_pocet(n, "otázka", "otázky", "otázek")}) →</a>')
            body = x["otazek"] * body_lo(lo)
            bloky.append(
                f'<li class="cil {x["k"].lower()}" id="{kotva_lo(lo)}" data-lo="{lo}">'
                f'<div class="cil-hlava"><span class="lo-id">{e(lo)}</span> <span class="lo-k" data-k="{x["k"]}">{x["k"]}</span> '
                f'<span class="cil-zkouska">ve zkoušce {x["otazek"]} {cesky_pocet(x["otazek"], "otázka", "otázky", "otázek")} · '
                f'{body} {cesky_pocet(body, "bod", "body", "bodů")}</span></div>'
                f'<p class="cil-text" lang="en">{e(x["text"])}</p>'
                f'<div class="cil-pata"><div class="cil-hodnoceni" role="group" aria-label="Sebehodnocení {e(lo)}">'
                f'<button type="button" data-hodnoceni="0" aria-pressed="false">neumím</button>'
                f'<button type="button" data-hodnoceni="1" aria-pressed="false">trochu</button>'
                f'<button type="button" data-hodnoceni="2" aria-pressed="false">umím</button></div>'
                f'<span class="cil-stat" data-stat="{lo}"></span>'
                f'<span class="cil-akce">{" ".join(akce)}</span></div></li>')
        bloky.append("</ul>")
        sekce.append(f'<section class="sekce" id="kapitola-{k}" data-kapitola="{k}">'
                     f'<h2><span class="pr-kapitola-cislo">{k}</span> {e(KAPITOLY[k]["cz"])}</h2>{"".join(bloky)}</section>')
    telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava">
  <p class="drobky">Learning objectives</p>
  <h1>Studijní cíle</h1>
  <p class="perex">Všech {len(LO_SEZNAM)} studijních cílů sylabu s K-úrovní a počtem otázek ve zkoušce.
  U každého si poznač, jak ho umíš. Úspěšnost se počítá z odevzdaných zkoušek a z procvičování.</p>
  <ul class="cv-legenda">
    <li><span class="lo-k" data-k="K1">K1</span> zapamatovat (recall, recognize)</li>
    <li><span class="lo-k" data-k="K2">K2</span> pochopit (explain, compare, summarize)</li>
    <li><span class="lo-k" data-k="K3">K3</span> použít (apply) — 2 body</li>
  </ul>
  <div class="cile-souhrn" id="cile-souhrn" aria-live="polite"></div>
  <div class="zk-tlacitka"><button type="button" class="zk-btn" id="cile-reset">Smazat sebehodnocení</button></div>
</div>
{''.join(sekce)}
<p class="zk-zdroj">Texty studijních cílů: ISTQB® CT-GenAI Syllabus v1.1 (© ISTQB®), v anglickém originále.
Počty otázek: ISTQB Exam Structures and Rules Tables v1.19.</p>
</main>
</div>"""
    return web.stranka(titulek=f"Studijní cíle | {NAZEV_WEBU}",
                       popis="Studijní cíle (learning objectives) ISTQB CT-GenAI s K-úrovní, počtem otázek ve zkoušce a sebehodnocením.",
                       telo=telo, aktivni="cile", skripty=["assets/cile.js"])


# --- zdroje -----------------------------------------------------------------


def stranka_zdroju(web: Web) -> str:
    telo = """<div class="stranka">
<main>
<div class="zahlavi">
  <p class="drobky">Zdroje a autorská práva</p>
  <h1>Zdroje</h1>
  <p class="podtitul">Odkud jsou informace na tomto webu a jak se smí používat.</p>
</div>
<article class="md" id="text">
<h2 id="oficialni">Oficiální dokumenty ISTQB</h2>
<p>Jediná autorita pro zkoušku je sylabus. Ostatní zdroje slouží k porozumění a k praxi.</p>
<ul>
<li><strong>Certified Tester Testing with Generative AI (CT-GenAI) — Syllabus</strong>, verze 1.1, 27. 4. 2026. © ISTQB®.</li>
<li><strong>CT-GenAI Sample Exam A — Questions a Answers</strong>, verze 1.1, 27. 4. 2026. © ISTQB®.</li>
<li><strong>ISTQB Exam Structures and Rules Tables</strong>, verze 1.19 — rozpis zkoušky: 40 otázek, 46 bodů, hranice 30 bodů.</li>
<li><strong>ISTQB Glossary</strong> — <a href="https://glossary.istqb.org" target="_blank" rel="noopener noreferrer">glossary.istqb.org</a>.</li>
<li>Česká terminologie klasických testovacích pojmů: sylabus CTFL 4.0.1.1 v českém překladu a slovník CaSQB
(<a href="https://casqb.org/ke-stazeni" target="_blank" rel="noopener noreferrer">casqb.org/ke-stazeni</a>).</li>
</ul>
<p>Dokumenty ISTQB jsou zdarma ke stažení na <a href="https://istqb.org" target="_blank" rel="noopener noreferrer">istqb.org</a>.</p>

<h2 id="kurzy">Kurzy použité k přípravě</h2>
<p>Z kurzů na Udemy jsou na webu jen výpisky a výklad vlastními slovy. Otázky z kurzů se na veřejný web nedávají.</p>
<ul>
<li>Exam Preparation: ISTQB CT-GenAI — Rafał Podraza</li>
<li>ISTQB CT-GenAI Practice Tests 2026 — Rafał Podraza</li>
<li>ISTQB Testing with Generative AI (CT-GenAI) — Tarek Roshdy</li>
<li>ISTQB CT-GenAI Crash Course — Rahul Shetty Academy</li>
<li>Learn AI Tools &amp; Build AI Agents for Testing &amp; QA Automation — Rahul Shetty Academy</li>
</ul>

<h2 id="autorska-prava">Autorská práva</h2>
<p>Tento web je <strong>neoficiální studijní materiál</strong>. Není produktem ani publikací ISTQB®.
ISTQB® je registrovaná ochranná známka International Software Testing Qualifications Board. Web je nekomerční.</p>
<p>Výklad, zkrácené verze, slovník, přiřazovací a praktická cvičení a cvičné otázky jsou vlastní texty autora.
Krátké definice ze sylabu jsou uvedeny s odkazem na oddíl. Texty studijních cílů jsou citované v anglickém originále.</p>
<p>Simulace zkoušky Sample Exam A používá otázky a zdůvodnění z oficiální vzorové zkoušky CT-GenAI v1.1
(© ISTQB®) pro nekomerční procvičování s uvedením zdroje, jak to podmínky vzorové zkoušky dovolují.
Český překlad otázek je neoficiální překlad autora webu. Originál je ke stažení na istqb.org.</p>
<p>Kód generátoru ve složce <code>tools/</code> je pod licencí MIT. Na textový obsah webu se MIT nevztahuje.</p>

<h2 id="ucet">Přihlášení a uložená data</h2>
<p>Web funguje bez přihlášení. Postup (výsledky testů, kartičky, cvičení, označené kapitoly) se pak ukládá
jen v tomto prohlížeči, v jeho úložišti localStorage.</p>
<p>Kdo se přihlásí Google účtem, má postup uložený i ve službě Google Firebase (databáze Firestore, region EU).
Ukládá se jen postup na tomto webu pod náhodným identifikátorem účtu. E-mail a jméno zná přihlašovací služba
Firebase Authentication. Vidí je jen správce webu, ostatní uživatelé ani nikdo s přístupem ke kódu webu ne.</p>
<p>Postup z účtu smažeš v menu účtu vpravo nahoře (Smazat postup z účtu). O smazání celého účtu požádej
autora webu.</p>

<h2 id="ai">Použití AI</h2>
<p>Při zpracování materiálů pomáhaly nástroje generativní AI (přepis, překlad, návrh struktury a otázek).
Obsah prošel kontrolou proti sylabu v1.1. Přesto může obsahovat nepřesnosti — ke zkoušce vždy platí oficiální sylabus.</p>
</article>
</main>
</div>"""
    return web.stranka(titulek=f"Zdroje | {NAZEV_WEBU}",
                       popis="Zdroje studijních materiálů ISTQB CT-GenAI a poznámka o autorských právech.",
                       telo=telo, aktivni="zdroje")


# --- sestavení --------------------------------------------------------------


def sestav(argv: list[str] | None = None) -> int:
    c = cesty(argv)
    varovani: list[str] = []
    print(f"Zdroj: {c.zdroj}\nVýstup: {c.web}\n")

    dokumenty = obsah_mod.nacti_vse(c.obsah, varovani)
    udemy = otazky_mod.nacti_udemy(c.data, varovani)

    if c.web.exists():
        for stary in c.web.iterdir():
            if stary.is_dir():
                shutil.rmtree(stary)
            else:
                stary.unlink()
    c.web.mkdir(parents=True, exist_ok=True)
    (c.web / "assets" / "data").mkdir(parents=True, exist_ok=True)
    for soubor in ASSETS:
        zdroj = ASSETS_ZDROJ / soubor
        if zdroj.exists():
            shutil.copyfile(zdroj, c.web / "assets" / soubor)
        else:
            varovani.append(f"tools/assets/{soubor} chybí")

    web = Web(c.web, dokumenty, lokalni=bool(udemy))
    mapa = obsah_mod.mapa_oddilu(dokumenty)
    zapsano: list[str] = []

    for (k, v), d in sorted(dokumenty.items()):
        web.zapis(f"kapitola-{k}/{v}.html", stranka_kapitoly(web, d))
        zapsano.append(f"kapitola-{k}/{v}.html  ({d.slova_zdroje} slov)")

    web.zapis("kapitoly.html", stranka_kapitol(web))

    pojmy = nacti_slovnik(c, web, mapa, varovani)
    web.zapis("slovnik.html", stranka_slovniku(web, pojmy))
    web.zapis_js("assets/data/slovnik.js", "GENAI_SLOVNIK",
                 {"kapitoly": {str(k): v["cz"] for k, v in KAPITOLY.items()},
                  "pojmy": [{"id": z["id"], "en": z["en"], "cz": z["cz"], "def": z["def"], "kap": z["kap"],
                             "klicove": z["klicove"], "href": z["odkazy"][0]["href"] if z["odkazy"] else ""}
                            for z in pojmy]},
                 "data/slovnik/kapitola-*.json")
    web.zapis("karticky.html", stranka_karticek(web, pojmy))
    if not pojmy:
        varovani.append("slovník je prázdný — slovník a kartičky jsou bez obsahu")

    sady = nacti_prirazovani(c, varovani)
    web.zapis_js("assets/data/prirazovani.js", "PRIRAZOVANI",
                 {"kapitoly": {str(k): v["cz"] for k, v in KAPITOLY.items()}, "sady": sady,
                  "prefix": PREFIX}, "data/prirazovani/kapitola-*.json")
    web.zapis("prirazovani.html", stranka_prirazovani(web, sady))
    if not sady:
        varovani.append("žádná přiřazovací cvičení — stránka je bez obsahu")

    cviceni = nacti_cviceni(c, varovani)
    web.zapis("cviceni.html", stranka_cviceni(web, cviceni, mapa))
    if not cviceni:
        varovani.append("žádná praktická cvičení — stránka je bez obsahu")

    moduly = praxe_mod.nacti_vse(c.obsah / "praxe", varovani)
    for m in moduly:
        web.zapis(m.stranka, praxe_mod.stranka_modulu(web, m, moduly))
        zapsano.append(f"{m.stranka}  ({m.slova_zdroje} slov, {len(m.cviceni)} cvičení)")
    web.zapis("praxe.html", praxe_mod.stranka_praxe(web, moduly))

    vysledek_zkousek = zkousky.zapis(web, c, mapa, udemy, varovani)
    zapsano += vysledek_zkousek["zapsano"]

    web.zapis("cile.html", stranka_cilu(web, mapa, vysledek_zkousek["pocty_lo"]))
    web.zapis("zdroje.html", stranka_zdroju(web))
    souhrn = {"pojmu": len(pojmy), "sad": len(sady), "cviceni": len(cviceni),
              "otazek": vysledek_zkousek["verejnych"], "praxe": len(praxe_mod.cislovane(moduly))}
    postup = {"cviceni": [x["id"] for x in cviceni], "moduly": [f"modul-{m.stem}" for m in moduly],
              "praxe": [i for m in moduly for i, _ in m.cviceni], "sad": len(sady), "pojmu": len(pojmy),
              "cilu": len(LO_SEZNAM)}
    web.zapis("index.html", stranka_uvodu(web, c, varovani, souhrn, postup))
    (c.web / ".nojekyll").write_text("", encoding="utf-8")

    for z in zapsano:
        print(f"  {z}")
    print(f"  + index, kapitoly, slovník ({len(pojmy)} pojmů), kartičky, přiřazování ({len(sady)} sad), "
          f"cvičení ({len(cviceni)}), cíle, zdroje")
    if varovani:
        print(f"\nVarování ({len(varovani)}):")
        for v in varovani:
            print(f"  ! {v}")
    print(f"\nHotovo: {c.web}")
    return 0


if __name__ == "__main__":
    raise SystemExit(sestav())
