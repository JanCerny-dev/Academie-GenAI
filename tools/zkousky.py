# -*- coding: utf-8 -*-
"""Stránky a data simulace zkoušky: Sample Exam A, cvičné zkoušky, náhodná zkouška,
procvičování a lokální část s otázkami z Udemy (web/lokalni/, jen na disku).

Průběh testu řídí assets/zkouska.js, procvičování assets/procvicovani.js (převzato z webu CTFL).

Výstup:
  zkouska.html                  rozcestník
  zkouska-a.html                Sample Exam A (assets/data/zkouska-a.js)
  cvicna-zkouska-N.html         cvičné zkoušky podle rozpisu (assets/data/cvicna-N.js)
  nahodna-zkouska.html          losování v prohlížeči podle rozpisu (assets/data/otazky-vse.js)
  procvicovani.html             procvičování po kapitolách a LO (assets/data/otazky-vse.js)
  lokalni/…                     totéž pro otázky z data/udemy/ (jen když data existují)
"""

from __future__ import annotations

from collections import Counter

import obsah as obsah_mod
import otazky as Q
from konfig import (CELKEM_BODU, CELKEM_OTAZEK, HRANICE_BODU, KAPITOLY, LO_INFO, LO_SEZNAM, MINUT,
                    MINUT_PRODLOUZENO, NAZEV_WEBU, PREFIX, ROZPIS, body_lo)
from rozvrzeni import Web, a, e

UPOZORNENI_LOKALNI = (
    '<p class="lokalni-varovani" role="note"><strong>Jen pro osobní studium, nepublikovat.</strong> '
    "Otázky na těchto stránkách pocházejí z placených kurzů Udemy a jsou chráněné autorským právem. "
    "Složka <code>web/lokalni/</code> je v .gitignore a nesmí se nahrát na GitHub ani nikam sdílet.</p>"
)

POZNAMKA_SAMPLE = (
    '<p class="zk-zdroj">Otázky a zdůvodnění: <em>ISTQB® Certified Tester Testing with Generative AI — '
    "Sample Exam set A</em>, verze {verze}. © International Software Testing Qualifications Board (ISTQB®). "
    "Anglické znění převzato beze změn pro nekomerční procvičování; český překlad je neoficiální překlad autora webu. "
    'Originál ke stažení na <a href="https://istqb.org" target="_blank" rel="noopener noreferrer">istqb.org</a>.</p>'
)

POZNAMKA_CVICNE = (
    '<p class="zk-zdroj"><strong>Vlastní cvičné otázky.</strong> Nejsou z oficiální vzorové zkoušky ISTQB® '
    "ani z placených kurzů. Jsou napsané nově podle studijních cílů sylabu CT-GenAI v1.1 (s pomocí AI) "
    "a zkontrolované proti sylabu. Přesto mohou obsahovat nepřesnosti — ke zkoušce vždy platí znění sylabu.</p>"
)

JAZYKY = [("en", "English", "jako u zkoušky"), ("cz", "Česky", "pochopit otázky"),
          ("encz", "English + skrytý český překlad", "nácvik")]


def _koren_zkousky(sada: str, koren: str, prefix: str, extra: str = "") -> str:
    return (f'<div id="zkouska" data-sada="{a(sada)}" data-koren="{koren}" data-prefix="{prefix}"{extra}>\n'
            '  <noscript><p>Simulace zkoušky potřebuje zapnutý JavaScript.</p></noscript>\n</div>')


def stranka_testu(web: Web, *, sada: str, nadpis: str, drobky: str, perex: str, poznamka: str,
                  data_js: str, koren: str = "", prefix: str = PREFIX, aktivni: str = "zkouska",
                  popis: str = "", horni: str = "") -> str:
    zpet = "index.html" if aktivni == "lokalni" else "zkouska.html"
    telo = f"""<div class="stranka uvod">
<main id="text">
{horni}
<div class="uvod-hlava">
  <p class="drobky"><a href="{zpet}">{'Lokální testy' if aktivni == 'lokalni' else 'Zkouška'}</a> · {e(drobky)}</p>
  <h1>{e(nadpis)}</h1>
  <p class="perex">{perex}</p>
</div>
{_koren_zkousky(sada, koren, prefix)}
{poznamka}
</main>
</div>"""
    return web.stranka(titulek=f"{nadpis} | {NAZEV_WEBU}", popis=popis or perex, telo=telo, koren=koren,
                       aktivni=aktivni, skripty=[data_js, "assets/zkouska.js"],
                       atributy_body=f' data-vysledky="{prefix}zkousky-vysledky"')


def stranka_procvicovani(web: Web, *, koren: str = "", prefix: str = PREFIX, aktivni: str = "zkouska",
                         data_js: str, perex: str, poznamka: str, horni: str = "") -> str:
    zpet = "index.html" if aktivni == "lokalni" else "zkouska.html"
    telo = f"""<div class="stranka uvod">
<main id="text">
{horni}
<div class="uvod-hlava">
  <p class="drobky"><a href="{zpet}">{'Lokální testy' if aktivni == 'lokalni' else 'Zkouška'}</a> · procvičování</p>
  <h1>Procvičování</h1>
  <p class="perex">{perex}</p>
</div>
<div id="procvicovani" data-koren="{koren}" data-prefix="{prefix}">
  <noscript><p>Procvičování potřebuje zapnutý JavaScript.</p></noscript>
</div>
{poznamka}
</main>
</div>"""
    return web.stranka(titulek=f"Procvičování | {NAZEV_WEBU}", popis=perex, telo=telo, koren=koren,
                       aktivni=aktivni, skripty=[data_js, "assets/procvicovani.js"])


def karta(cil: str, *, cislo: str, nadpis: str, meta: str, vysledek: str, jazyky: bool = True) -> str:
    if jazyky:
        hlavni = ' class="hlavni"'
        odkazy = "".join(
            f'<li><a href="{cil}?jazyk={j}"{hlavni if j == "en" else ""}>{e(n)}<span>{e(p)}</span></a></li>'
            for j, n, p in JAZYKY)
    else:
        odkazy = f'<li><a href="{cil}" class="hlavni">Otevřít<span>→</span></a></li>'
    return f"""<li class="karta" data-vysledek="{a(vysledek)}">
  <p class="karta-cislo">{e(cislo)}</p>
  <h3>{e(nadpis)}</h3>
  <p class="karta-meta">{meta}</p>
  <ul>{odkazy}</ul>
</li>"""


def data_vse(otazky: list[dict], *, lokalni: bool = False) -> dict:
    return {
        "rozpis": ROZPIS,
        "kapitoly": {str(k): v["cz"] for k, v in KAPITOLY.items()},
        "lo": {x["lo"]: {"k": x["k"], "text": x["text"]} for x in LO_SEZNAM},
        "lokalni": lokalni,
        "otazky": otazky,
    }


def _lze_nahodnou(otazky: list[dict]) -> bool:
    pocty = Counter(q["lo"] for q in otazky)
    return all(pocty[lo] >= n for lo, n in ROZPIS.items())


def zapis(web: Web, c, mapa: dict, udemy: list[dict], varovani: list[str]) -> dict:
    cvicne, sample, meta = Q.nacti_verejne(c.data, varovani)

    def odkaz(oddil: str) -> dict:
        return obsah_mod.odkaz_na_oddil(oddil, mapa, web.dokumenty)

    zapsano: list[str] = []
    karty_oficialni, karty_cvicne, karty_dalsi = [], [], []

    # Sample Exam A — pořadí otázek i možností beze změny
    if sample:
        verze = str(meta.get("verze") or "1.1 (27. 4. 2026)")
        otazky_a = [Q.pro_web(q, odkaz, n=i + 1, oficialni=True) for i, q in enumerate(sample)]
        bodu = sum(q["body"] for q in otazky_a)
        web.zapis_js("assets/data/zkouska-a.js", "VZOROVA_ZKOUSKA",
                     {"sada": "a", "nazev": "Sample Exam A", "oficialni": True, "otazky": otazky_a},
                     "data/vzorova-zkouska-a.json")
        web.zapis("zkouska-a.html", stranka_testu(
            web, sada="a", nadpis="Sample Exam A", drobky="oficiální vzorová zkouška",
            perex=f"{len(otazky_a)} otázek ({bodu} bodů) z oficiální vzorové zkoušky ISTQB CT-GenAI v1.1. "
                  "Stejný formát, čas i hranice úspěchu jako u skutečné zkoušky.",
            poznamka=POZNAMKA_SAMPLE.format(verze=e(verze)), data_js="assets/data/zkouska-a.js"))
        zapsano.append(f"zkouska-a.html  ({len(otazky_a)} otázek, {bodu} bodů)")
        if len(otazky_a) != CELKEM_OTAZEK or bodu != CELKEM_BODU:
            varovani.append(f"Sample Exam A má {len(otazky_a)} otázek / {bodu} bodů (čekáno 40 / 46)")
        karty_oficialni.append(karta("zkouska-a.html", cislo="Oficiální", nadpis="Sample Exam A",
                                     meta=f"{len(otazky_a)} otázek · {bodu} bodů · verze {e(verze)}", vysledek="a"))

    # Dodatkové otázky Sample Exam A (drag & drop) — mimo zkoušku 40/46
    dodatkove = [Q.dodatkova_pro_web(q, odkaz) for q in meta.get("dodatkove", [])]
    if dodatkove:
        verze = str(meta.get("verze") or "1.1")
        web.zapis_js("assets/data/zkouska-a-dodatkove.js", "DODATKOVE_OTAZKY", {"otazky": dodatkove},
                     "data/vzorova-zkouska-a.json (navic: true)")
        telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava">
  <p class="drobky"><a href="zkouska.html">Zkouška</a> · Sample Exam A</p>
  <h1>Dodatkové otázky Sample Exam A</h1>
  <p class="perex">{len(dodatkove)} otázky typu „drag &amp; drop“ (seřazení kroků, přiřazení do skupin). Do zkoušky
  40 otázek / 46 bodů se nepočítají. Místo přetahování vybíráš pořadí nebo skupinu ze seznamu.</p>
</div>
<div id="dodatkove" data-koren="">
  <noscript><p>Dodatkové otázky potřebují zapnutý JavaScript.</p></noscript>
</div>
{POZNAMKA_SAMPLE.format(verze=e(verze))}
</main>
</div>"""
        web.zapis("zkouska-a-dodatkove.html", web.stranka(
            titulek=f"Dodatkové otázky Sample Exam A | {NAZEV_WEBU}",
            popis="Dodatkové otázky ISTQB CT-GenAI Sample Exam A: řazení a přiřazení.", telo=telo,
            aktivni="zkouska", skripty=["assets/data/zkouska-a-dodatkove.js", "assets/dodatkove.js"]))
        zapsano.append(f"zkouska-a-dodatkove.html  ({len(dodatkove)} otázky)")
        karty_oficialni.append(karta("zkouska-a-dodatkove.html", cislo="Oficiální · navíc",
                                     nadpis="Dodatkové otázky A1–A3",
                                     meta=f"{len(dodatkove)} otázky řazení a přiřazení, mimo bodování",
                                     vysledek="a-dodatkove", jazyky=False))

    # Cvičné zkoušky přesně podle rozpisu
    sady, _navic = Q.sestav_sady(cvicne)
    for i, sada in enumerate(sady, start=1):
        otazky_s = Q.sada_pro_web(sada, i, odkaz)
        web.zapis_js(f"assets/data/cvicna-{i}.js", "VZOROVA_ZKOUSKA",
                     {"sada": f"cvicna-{i}", "nazev": f"Cvičná zkouška {i}", "oficialni": False, "otazky": otazky_s},
                     "data/cvicne-otazky/kapitola-*.json")
        web.zapis(f"cvicna-zkouska-{i}.html", stranka_testu(
            web, sada=f"cvicna-{i}", nadpis=f"Cvičná zkouška {i}", drobky="cvičná zkouška",
            perex="40 vlastních otázek sestavených přesně podle rozpisu ostré zkoušky: stejné studijní cíle, "
                  "stejné K-úrovně, 46 bodů. Možnosti jsou zamíchané tak, aby správné odpovědi byly rovnoměrně mezi a–d.",
            poznamka=POZNAMKA_CVICNE, data_js=f"assets/data/cvicna-{i}.js"))
        zapsano.append(f"cvicna-zkouska-{i}.html")
        karty_cvicne.append(karta(f"cvicna-zkouska-{i}.html", cislo=f"Cvičná {i}", nadpis=f"Cvičná zkouška {i}",
                                  meta="40 otázek · 46 bodů · rozpis jako ostrá zkouška", vysledek=f"cvicna-{i}"))
    if cvicne and not sady:
        chybi = Q.chybi_do_sady(cvicne, 1)
        varovani.append(f"cvičné otázky ({len(cvicne)}) zatím nestačí na úplnou zkoušku; chybí: "
                        + ", ".join(f"{lo.replace('GenAI-', '')}×{n}" for lo, n in chybi.items()))
    elif sady:
        chybi = Q.chybi_do_sady(cvicne, len(sady) + 1)
        varovani.append(f"do další ({len(sady) + 1}.) cvičné zkoušky chybí {sum(chybi.values())} otázek "
                        f"v {len(chybi)} LO")

    # Společná zásoba pro náhodnou zkoušku a procvičování
    vse = [Q.pro_web(Q.zamichej(q, i), odkaz) for i, q in enumerate(cvicne)]
    vse += [Q.pro_web(q, odkaz, n=i + 1, oficialni=True) for i, q in enumerate(sample)]
    pocty_lo = dict(Counter(q["lo"] for q in vse))
    if vse:
        web.zapis_js("assets/data/otazky-vse.js", "CVICNE_OTAZKY", data_vse(vse),
                     "data/cvicne-otazky/*.json a data/vzorova-zkouska-a.json")
        web.zapis("procvicovani.html", stranka_procvicovani(
            web, data_js="assets/data/otazky-vse.js",
            perex=f"{len(vse)} otázek (vlastní cvičné a Sample Exam A) po kapitolách nebo po studijních cílech, "
                  "bez časového limitu. Vyhodnocení a zdůvodnění uvidíš hned po každé odpovědi.",
            poznamka=POZNAMKA_CVICNE))
        zapsano.append("procvicovani.html")
        karty_dalsi.append(karta("procvicovani.html", cislo="Bez limitu", nadpis="Procvičování",
                                 meta=f"{len(vse)} otázek po kapitolách a po LO, okamžité vyhodnocení",
                                 vysledek="procvicovani", jazyky=False))
        if _lze_nahodnou(vse):
            web.zapis("nahodna-zkouska.html", stranka_testu(
                web, sada="nahodna", nadpis="Náhodná zkouška", drobky="náhodná zkouška",
                perex="Při každém spuštění se vylosuje nových 40 otázek přesně podle rozpisu ostré zkoušky "
                      "(počty po studijních cílech, 46 bodů), volitelně i z otázek Sample Exam A.",
                poznamka=POZNAMKA_CVICNE, data_js="assets/data/otazky-vse.js"))
            zapsano.append("nahodna-zkouska.html")
            karty_dalsi.insert(0, karta("nahodna-zkouska.html", cislo="Pokaždé jiná", nadpis="Náhodná zkouška",
                                        meta=f"40 otázek losovaných z {len(vse)} podle rozpisu", vysledek="nahodna"))
        else:
            varovani.append("veřejné otázky zatím nepokrývají celý rozpis — náhodná zkouška vynechána")

    web.zapis("zkouska.html", rozcestnik(web, karty_oficialni, karty_cvicne, karty_dalsi))

    if udemy:
        zapsano += zapis_lokalni(web, udemy, odkaz, varovani)
    return {"zapsano": zapsano, "pocty_lo": pocty_lo, "verejnych": len(vse)}


def rozcestnik(web: Web, oficialni: list[str], cvicne: list[str], dalsi: list[str]) -> str:
    def sekce(id_: str, nadpis: str, uvod: str, karty: list[str]) -> str:
        if not karty:
            return ""
        return (f'<section class="sekce" id="{id_}"><h2>{nadpis}</h2>{uvod}'
                f'<ul class="mrizka">{"".join(karty)}</ul></section>')

    obsah = (
        sekce("oficialni", "Oficiální vzorová zkouška", "", oficialni)
        + sekce("cvicne", "Cvičné zkoušky",
                "<p>Vlastní otázky, které nejsou z oficiální vzorové zkoušky ani z placených kurzů. "
                "Každá zkouška má přesně rozpis ostré zkoušky.</p>", cvicne)
        + sekce("dalsi", "Náhodná zkouška a procvičování", "", dalsi)
    ) or '<p class="poznamka">Otázky se připravují. Až budou data, objeví se tady zkoušky.</p>'
    telo = f"""<div class="stranka uvod">
<main id="text">
<div class="uvod-hlava">
  <p class="drobky">Simulace zkoušky</p>
  <h1>Zkouška</h1>
  <p class="perex">U každé zkoušky si vyber jazyk. Ostrá zkouška je jen anglicky: začni česky, pak přejdi
  na angličtinu se skrytým českým překladem, který odkryješ tlačítkem u otázky.</p>
</div>
{obsah}
<section class="sekce">
  <h2>Jak to probíhá</h2>
  <ul>
    <li><strong>40 otázek, 46 bodů, {MINUT} minut</strong> ({MINUT_PRODLOUZENO} minut, pokud zkoušku skládáš v jiném
    než rodném jazyce). Otázka K3 má 2 body. K úspěchu je potřeba <strong>{HRANICE_BODU} bodů</strong> (65 %).</li>
    <li>Otázky jde označit k revizi a vracet se k nim přes mřížku čísel.</li>
    <li>Po odevzdání se ukáže jen počet bodů. Kdo nesplní, může si dát 10 minut na opravu bez nápovědy.</li>
    <li>Ve vyhodnocení je zdůvodnění u každé možnosti, úspěšnost po kapitolách a po studijních cílech
    a odkaz do výkladu.</li>
    <li>Výsledky a historie pokusů se ukládají jen v tomto prohlížeči. Úspěšnost po LO uvidíš na stránce
    <a href="cile.html">Cíle</a>.</li>
  </ul>
</section>
</main>
</div>"""
    return web.stranka(titulek=f"Zkouška | {NAZEV_WEBU}",
                       popis="Simulace zkoušky ISTQB CT-GenAI: Sample Exam A, cvičné zkoušky podle rozpisu, "
                             "náhodná zkouška a procvičování, anglicky i česky.",
                       telo=telo, aktivni="zkouska", atributy_body=f' data-vysledky="{PREFIX}zkousky-vysledky"')


# --- lokální část (Udemy) ---------------------------------------------------


def zapis_lokalni(web: Web, testy: list[dict], odkaz, varovani: list[str]) -> list[str]:
    prefix = PREFIX + "lokalni-"
    koren = "../"
    zapsano = []
    karty = []
    vse = []
    for i, t in enumerate(testy, start=1):
        sada = f"udemy-{t['id']}"
        otazky_t = []
        for j, q in enumerate(t["otazky"]):
            otazky_t.append(Q.pro_web(q, odkaz, n=j + 1))
            if q.get("lo") in ROZPIS:
                vse.append(Q.pro_web(Q.zamichej(q, j), odkaz))
        bodu = sum(q["body"] for q in otazky_t)
        web.zapis_js(f"lokalni/data/test-{i}.js", "VZOROVA_ZKOUSKA",
                     {"sada": sada, "nazev": t["nazev"], "oficialni": False, "otazky": otazky_t},
                     "data/udemy/*.json (JEN LOKÁLNĚ)")
        web.zapis(f"lokalni/test-{i}.html", stranka_testu(
            web, sada=sada, nadpis=t["nazev"], drobky="test z Udemy",
            perex=f"{len(otazky_t)} otázek ({bodu} bodů) v pořadí z kurzu.", poznamka="", horni=UPOZORNENI_LOKALNI,
            data_js=f"lokalni/data/test-{i}.js", koren=koren, prefix=prefix, aktivni="lokalni"))
        zapsano.append(f"lokalni/test-{i}.html  ({len(otazky_t)} otázek)")
        karty.append(karta(f"test-{i}.html", cislo=f"Test {i}", nadpis=t["nazev"],
                           meta=f"{len(otazky_t)} otázek · {bodu} bodů", vysledek=sada))
    dalsi = []
    if vse:
        web.zapis_js("lokalni/data/vse.js", "CVICNE_OTAZKY", data_vse(vse, lokalni=True),
                     "data/udemy/*.json (JEN LOKÁLNĚ)")
        web.zapis("lokalni/procvicovani.html", stranka_procvicovani(
            web, koren=koren, prefix=prefix, aktivni="lokalni", data_js="lokalni/data/vse.js",
            perex=f"{len(vse)} otázek z kurzů Udemy po kapitolách a po studijních cílech.",
            poznamka="", horni=UPOZORNENI_LOKALNI))
        zapsano.append("lokalni/procvicovani.html")
        dalsi.append(karta("procvicovani.html", cislo="Bez limitu", nadpis="Procvičování",
                           meta=f"{len(vse)} otázek po kapitolách a LO", vysledek="procvicovani", jazyky=False))
        if _lze_nahodnou(vse):
            web.zapis("lokalni/mix.html", stranka_testu(
                web, sada="mix", nadpis="Mix všech testů", drobky="mix podle rozpisu",
                perex="40 otázek losovaných ze všech testů z Udemy přesně podle rozpisu ostré zkoušky.",
                poznamka="", horni=UPOZORNENI_LOKALNI, data_js="lokalni/data/vse.js",
                koren=koren, prefix=prefix, aktivni="lokalni"))
            zapsano.append("lokalni/mix.html")
            dalsi.insert(0, karta("mix.html", cislo="Mix", nadpis="Mix všech testů",
                                  meta="40 otázek podle rozpisu", vysledek="mix"))
        else:
            varovani.append("otázky z Udemy nepokrývají celý rozpis — lokální mix vynechán")
    telo = f"""<div class="stranka uvod">
<main id="text">
{UPOZORNENI_LOKALNI}
<div class="uvod-hlava">
  <p class="drobky">Jen na tomto počítači</p>
  <h1>Lokální testy z Udemy</h1>
  <p class="perex">{len(testy)} testů, {sum(len(t['otazky']) for t in testy)} otázek. Stejný engine jako veřejné zkoušky:
  volba jazyka, časomíra, body, vyhodnocení po kapitolách a LO.</p>
</div>
<section class="sekce"><h2>Testy</h2><ul class="mrizka">{''.join(karty)}</ul></section>
{f'<section class="sekce"><h2>Mix a procvičování</h2><ul class="mrizka">{"".join(dalsi)}</ul></section>' if dalsi else ''}
</main>
</div>"""
    web.zapis("lokalni/index.html", web.stranka(
        titulek=f"Lokální testy | {NAZEV_WEBU}", popis="Lokální testy z kurzů Udemy — jen pro osobní studium.",
        telo=telo, koren=koren, aktivni="lokalni", atributy_body=f' data-vysledky="{prefix}zkousky-vysledky"'))
    zapsano.insert(0, "lokalni/index.html")
    return zapsano
