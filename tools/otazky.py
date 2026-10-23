# -*- coding: utf-8 -*-
"""Otázky (cvičné, Sample Exam A, Udemy): kontrola, převod pro web, skládání zkoušek.

Formát otázky: PRAVIDLA_ZPRACOVANI.md, kap. 7. Skládání cvičných zkoušek přebírá
logiku z cvicne_zkousky.py projektu CTFL, jen rozpis CT-GenAI je přímo po LO:
každý LO má pevný počet otázek (1.1.2, 2.1.1 a 3.2.2 po dvou, ostatní po jedné),
celkem 40 otázek a 46 bodů (K3 = 2 body).
"""

from __future__ import annotations

import random
import re
from collections import defaultdict
from pathlib import Path

from konfig import (LO_INFO, LO_SEZNAM, PISMENA, ROZPIS, body_lo, kapitola_lo, nacti_json)

SEMINKO = 2026  # pevné, aby se sady při každém sestavení nepřeskládaly

# Text odkazující na písmeno nebo pořadí možností — takové otázce nelze míchat pořadí.
ODKAZ_NA_PORADI = re.compile(
    r"(možnost[iíe]?\s+[a-f]\b|\b(?:options?|answers?|choices?)\s+[a-f]\b|(?<![\w(])[a-f]\)\s"
    r"|\(\s*[a-f]\s*\)|\b(?:all|none|both)\s+of\s+the\s+above\b|výše\s+uveden|\bvšechny\s+výše)",
    re.I,
)

ZDROJE_POPIS = {
    "vlastni": "vlastní cvičná otázka",
    "sample-a": "ISTQB® Sample Exam A v1.1",
    "podraza-prep": "Udemy: Podraza – Exam Prep",
    "podraza-practice": "Udemy: Podraza – Practice Tests",
    "roshdy": "Udemy: Roshdy – ISTQB GenAI",
    "shetty-crash": "Udemy: Shetty – Crash Course",
    "shetty-tools": "Udemy: Shetty – AI Tools for QA",
}


def _holy(t) -> str:
    return re.sub(r"<[^>]+>", " ", str(t or ""))


def chyby_otazky(q: dict, *, lo_povinne: bool = True) -> list[str]:
    """Seznam porušení datového kontraktu (prázdný = otázka je v pořádku)."""
    ch: list[str] = []
    if not isinstance(q, dict):
        return ["otázka není objekt"]
    if not q.get("id"):
        ch.append("chybí id")
    if lo_povinne and q.get("lo") not in ROZPIS:
        ch.append(f"lo „{q.get('lo')}“ není v rozpisu zkoušky")
    pocty = {}
    for jazyk in ("en", "cz"):
        t = q.get(jazyk)
        if not isinstance(t, dict) or not t.get("q"):
            ch.append(f"chybí text otázky {jazyk}")
            continue
        m = t.get("moznosti")
        if not isinstance(m, list) or not (2 <= len(m) <= len(PISMENA)):
            ch.append(f"{jazyk}.moznosti: má být 2–{len(PISMENA)} možností")
            continue
        pocty[jazyk] = len(m)
    if len(pocty) == 2 and pocty["en"] != pocty["cz"]:
        ch.append(f"en má {pocty['en']} možností, cz {pocty['cz']}")
    n = pocty.get("en") or pocty.get("cz") or 0
    spr = q.get("spravne")
    if not isinstance(spr, list) or not spr:
        ch.append("spravne: má být neprázdný seznam písmen")
    elif n and not all(isinstance(p, str) and p in PISMENA[:n] for p in spr):
        ch.append(f"spravne {spr} mimo rozsah možností a–{PISMENA[n - 1]}")
    elif len(set(spr)) != len(spr):
        ch.append("spravne obsahuje duplicitu")
    if isinstance(spr, list) and q.get("vyber") not in (None, len(spr)):
        ch.append(f"vyber={q.get('vyber')} nesedí s počtem správných ({len(spr)})")
    return ch


def chyby_dodatkove(q: dict) -> list[str]:
    """Dodatkové otázky Sample Exam A (navic: true): řazení nebo přiřazení do skupin."""
    ch: list[str] = []
    typ = q.get("typ")
    if typ not in ("razeni", "prirazeni"):
        return [f"neznámý typ „{typ}“ (čekáno razeni / prirazeni)"]
    n = None
    for jazyk in ("en", "cz"):
        t = q.get(jazyk) or {}
        if not t.get("q") or not isinstance(t.get("moznosti"), list):
            ch.append(f"chybí {jazyk}.q nebo {jazyk}.moznosti")
            continue
        if n is not None and len(t["moznosti"]) != n:
            ch.append("en a cz mají různý počet položek")
        n = len(t["moznosti"])
        if typ == "prirazeni" and not t.get("skupiny"):
            ch.append(f"chybí {jazyk}.skupiny")
    spr = q.get("spravne") or []
    if n is not None and len(spr) != n:
        ch.append(f"spravne má {len(spr)} prvků, položek je {n}")
    if typ == "razeni" and n and sorted(spr) != list(PISMENA[:n]):
        ch.append("spravne u řazení má být permutace písmen")
    if typ == "prirazeni" and n:
        skupin = len((q.get("en") or {}).get("skupiny") or [])
        if not all(str(x).isdigit() and 1 <= int(x) <= skupin for x in spr):
            ch.append("spravne u přiřazení má obsahovat čísla skupin 1–n")
    return ch


def dodatkova_pro_web(q: dict, odkaz) -> dict:
    def texty(t):
        return {"q": t.get("q", ""), "m": t.get("moznosti") or [], "skupiny": t.get("skupiny") or [],
                "obecne": t.get("vysvetleni_obecne") or ""}
    return {"id": q["id"], "typ": q["typ"], "lo": q.get("lo", ""), "k": q.get("k", ""),
            "spravne": [str(x) for x in q["spravne"]], "en": texty(q["en"]), "cz": texty(q["cz"]),
            "kap": odkaz(str(q.get("oddil") or (q.get("lo") or "").replace("GenAI-", "")))}


def lze_michat(q: dict) -> bool:
    if q.get("keep_order") or len(q.get("spravne") or []) != 1:
        return False
    texty = []
    for jazyk in ("en", "cz"):
        t = q.get(jazyk) or {}
        texty += [t.get("q", ""), t.get("vysvetleni_obecne", ""), *(t.get("moznosti") or []),
                  *((t.get("vysvetleni") or {}).values())]
    return not ODKAZ_NA_PORADI.search(" ".join(_holy(x) for x in texty))


def zamichej(q: dict, cil: int) -> dict:
    """Kopie otázky s možnostmi přeskládanými tak, aby správná byla na pozici `cil`."""
    if not lze_michat(q):
        return q
    n = len(q["en"]["moznosti"])
    puvodni = PISMENA.index(q["spravne"][0])
    cil = cil % n
    ostatni = [i for i in range(n) if i != puvodni]
    random.Random(f"{SEMINKO}-{q['id']}").shuffle(ostatni)
    poradi = ostatni[:cil] + [puvodni] + ostatni[cil:]
    nova = dict(q)
    for jazyk in ("en", "cz"):
        t = dict(q[jazyk])
        vys = t.get("vysvetleni") or {}
        t["moznosti"] = [t["moznosti"][i] for i in poradi]
        t["vysvetleni"] = {PISMENA[j]: vys[PISMENA[i]] for j, i in enumerate(poradi) if PISMENA[i] in vys}
        nova[jazyk] = t
    nova["spravne"] = [PISMENA[cil]]
    return nova


def _texty(t: dict | None) -> dict | None:
    if not t:
        return None
    return {
        "q": t.get("q", ""),
        "m": list(t.get("moznosti") or []),
        "vys": dict(t.get("vysvetleni") or {}),
        "obecne": t.get("vysvetleni_obecne") or "",
    }


def pro_web(q: dict, odkaz, *, n: int | None = None, oficialni: bool = False, navic: bool = False) -> dict:
    """Otázka ve tvaru, který čte assets/zkouska.js a assets/procvicovani.js."""
    lo = q.get("lo") or ""
    k = LO_INFO[lo]["k"] if lo in LO_INFO else q.get("k", "")
    body = body_lo(lo) if lo in LO_INFO else (q.get("body") or (2 if k == "K3" else 1))
    return {
        "id": q["id"],
        "n": n,
        "lo": lo,
        "k": k,
        "body": body,
        "vyber": len(q["spravne"]),
        "ok": [PISMENA.index(p) for p in q["spravne"]],
        "en": _texty(q.get("en")),
        "cz": _texty(q.get("cz")),
        "kap": odkaz(str(q.get("oddil") or lo.replace("GenAI-", ""))),
        "zdroj": ZDROJE_POPIS.get(q.get("zdroj", ""), q.get("zdroj", "")),
        "oficialni": oficialni,
        "navic": navic,
        "pozn": q.get("poznamka_webu") or "",
    }


# --- načtení --------------------------------------------------------------


def _otazky_souboru(data, nazev: str, varovani: list[str]) -> list[dict]:
    if isinstance(data, dict) and isinstance(data.get("otazky"), list):
        return data["otazky"]
    if isinstance(data, list):
        return data
    varovani.append(f"{nazev}: chybí pole „otazky“ — vynecháno")
    return []


def nacti_verejne(data_dir: Path, varovani: list[str]) -> tuple[list[dict], list[dict], dict]:
    """Vrátí (cvičné otázky, otázky Sample Exam A, metadata Sample A). Neplatné vynechá."""
    cvicne: list[dict] = []
    videna: set[str] = set()
    from konfig import soubory_kapitol
    for k, cesta in soubory_kapitol(data_dir / "cvicne-otazky"):
        data = nacti_json(cesta, varovani)
        for q in _otazky_souboru(data, f"cvicne-otazky/{cesta.name}", varovani) if data is not None else []:
            ch = chyby_otazky(q)
            if not ch and q["id"] in videna:
                ch = ["duplicitní id"]
            if ch:
                varovani.append(f"cvicne-otazky/{cesta.name} {q.get('id', '?')}: {'; '.join(ch)} — vynecháno")
                continue
            if kapitola_lo(q["lo"]) != k:
                varovani.append(f"cvicne-otazky/{cesta.name} {q['id']}: LO {q['lo']} je z jiné kapitoly")
            if q.get("k") and q["k"] != LO_INFO[q["lo"]]["k"]:
                varovani.append(f"{q['id']}: k={q['k']}, ale LO má {LO_INFO[q['lo']]['k']} (body podle LO)")
            videna.add(q["id"])
            cvicne.append(q)

    sample: list[dict] = []
    meta: dict = {}
    cesta = data_dir / "vzorova-zkouska-a.json"
    data = nacti_json(cesta, varovani)
    if data is None and not cesta.exists():
        varovani.append("data/vzorova-zkouska-a.json zatím neexistuje — Sample Exam A vynechána")
    elif data is not None:
        meta = {k: v for k, v in data.items() if k != "otazky"} if isinstance(data, dict) else {}
        meta["dodatkove"] = []
        for q in _otazky_souboru(data, cesta.name, varovani):
            if isinstance(q, dict) and q.get("navic"):
                ch = chyby_dodatkove(q)
                if ch:
                    varovani.append(f"vzorova-zkouska-a.json {q.get('id', '?')} (dodatková): {'; '.join(ch)} — vynecháno")
                else:
                    meta["dodatkove"].append(q)
                continue
            ch = chyby_otazky(q)
            if not ch and q["id"] in videna:
                ch = ["duplicitní id"]
            if ch:
                varovani.append(f"vzorova-zkouska-a.json {q.get('id', '?')}: {'; '.join(ch)} — vynecháno")
                continue
            videna.add(q["id"])
            sample.append(q)
    return cvicne, sample, meta


def nacti_udemy(data_dir: Path, varovani: list[str]) -> list[dict]:
    """Testy z data/udemy/*.json. Vrací [{id, nazev, otazky}] (jen platné otázky).

    Podporované tvary souboru:
      {"popis": …, "otazky": […]}             jeden test na soubor
      {"popis": …, "otazky": [{… "test": "3"}]} test podle pole „test“ u otázky
      {"popis": …, "testy": [{"nazev": …, "otazky": […]}]}
    """
    slozka = data_dir / "udemy"
    testy: list[dict] = []
    if not slozka.exists():
        return testy
    for cesta in sorted(slozka.glob("*.json")):
        data = nacti_json(cesta, varovani)
        if data is None:
            continue
        zdroj = data.get("zdroj") if isinstance(data, dict) else ""
        popis = ZDROJE_POPIS.get(zdroj or cesta.stem, "").replace("Udemy: ", "") or cesta.stem
        skupiny: list[tuple[str, list]] = []
        if isinstance(data, dict) and isinstance(data.get("testy"), list):
            for i, t in enumerate(data["testy"], 1):
                skupiny.append((str(t.get("nazev") or t.get("id") or f"Test {i}"), t.get("otazky") or []))
        else:
            podle: dict[str, list] = defaultdict(list)
            for q in _otazky_souboru(data, f"udemy/{cesta.name}", varovani):
                podle[str(q.get("test") or "")].append(q) if isinstance(q, dict) else None
            for t, seznam in podle.items():
                skupiny.append((f"Test {t}" if t else "", seznam))
        bez_lo: list[str] = []
        for nazev, seznam in skupiny:
            platne = []
            for q in seznam:
                ch = chyby_otazky(q, lo_povinne=False)
                if ch:
                    varovani.append(f"udemy/{cesta.name} {q.get('id', '?') if isinstance(q, dict) else '?'}: "
                                    f"{'; '.join(ch)} — vynecháno")
                    continue
                if q.get("lo") not in ROZPIS:
                    bez_lo.append(q["id"])
                platne.append(q)
            if platne:
                tid = re.sub(r"[^a-z0-9]+", "-", f"{cesta.stem}-{nazev}".lower()).strip("-")
                testy.append({"id": tid, "nazev": f"{popis} – {nazev}" if nazev else popis, "otazky": platne})
        if bez_lo:
            varovani.append(f"udemy/{cesta.name}: {len(bez_lo)} otázek bez LO z rozpisu ({bez_lo[0]}…) "
                            "— jsou jen ve svém testu, ne v mixu a procvičování")
    return testy


# --- skládání zkoušek podle rozpisu ---------------------------------------


def sestav_sady(otazky: list[dict]) -> tuple[list[list[dict]], list[dict]]:
    """Co nejvíc úplných zkoušek přesně podle rozpisu. Vrací (sady, zbylé otázky)."""
    rnd = random.Random(SEMINKO)
    podle_lo: dict[str, list[dict]] = defaultdict(list)
    for q in otazky:
        podle_lo[q["lo"]].append(q)
    for lo in sorted(podle_lo):
        podle_lo[lo].sort(key=lambda q: q["id"])
        rnd.shuffle(podle_lo[lo])
    pocet = min(len(podle_lo.get(lo, [])) // n for lo, n in ROZPIS.items())
    sady = []
    for s in range(pocet):
        sada = []
        for x in LO_SEZNAM:
            lo, n = x["lo"], x["otazek"]
            sada.extend(podle_lo[lo][s * n:(s + 1) * n])
        sady.append(sada)
    v_sadach = {q["id"] for s in sady for q in s}
    return sady, [q for q in otazky if q["id"] not in v_sadach]


def chybi_do_sady(otazky: list[dict], sad: int) -> dict[str, int]:
    """Kolik otázek kterému LO chybí do `sad` úplných zkoušek."""
    pocty = defaultdict(int)
    for q in otazky:
        pocty[q["lo"]] += 1
    return {lo: n * sad - pocty[lo] for lo, n in ROZPIS.items() if pocty[lo] < n * sad}


def sada_pro_web(sada: list[dict], cislo: int, odkaz, stitek: str = "") -> list[dict]:
    """Otázky sady se zamíchanými možnostmi (správné odpovědi rovnoměrně mezi a–d)."""
    start = random.Random(f"{SEMINKO}-{stitek}sada-{cislo}").randrange(4)
    return [pro_web(zamichej(q, start + i), odkaz, n=i + 1) for i, q in enumerate(sada)]
