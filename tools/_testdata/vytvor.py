# -*- coding: utf-8 -*-
"""Vytvoří malá ukázková data pro `build_site.py --testdata` (stejné formáty jako PRAVIDLA, kap. 5–7).

Texty jsou vymyšlené výplně, nejde o obsah sylabu ani kurzů.
Spuštění: python tools/_testdata/vytvor.py   (přepíše obsah/, data/ a README.md v této složce)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ZDE = Path(__file__).resolve().parent
sys.path.insert(0, str(ZDE.parent))
from konfig import LO_SEZNAM  # noqa: E402

VYKLAD_1 = """---
kapitola: 1
varianta: vyklad
nadpis: Úvod do generativní AI (testovací data)
podtitul: Ukázkový text, který prověří všechny konstrukce převodníku.
---

## 1.1 Základy generativní AI
:::lo
GenAI-1.1.1 (K1) Recall different types of AI
GenAI-1.1.2 (K2) Explain the basics of generative AI and large language models
:::

### 1.1.1 Druhy AI
Odstavec s **tučným textem**, *kurzívou*, `kódem` a [odkazem](https://istqb.org).
Pokračování odstavce na dalším řádku, s čárkou za **tučně**, a hvězdička 5 * 3 zůstane.

- první odrážka
- druhá odrážka s **tučně**
  - vnořená odrážka
  - druhá vnořená
- třetí odrážka

1. první krok
2. druhý krok
   1. podkrok

| Typ | Popis | Počet |
|---|:---:|---:|
| **symbolic AI** | pravidla | 1 |
| machine learning | data `x` | 2 |

Tabulku doplňuje věta pod ní.

```text
You are a test analyst. Write three test cases
for the login form <input type="password">.
```

:::praxe
Příklad z praxe: přihlášení do bankovní aplikace.

- odrážka uvnitř bloku
:::

:::nad-ramec
Doplněk nad rámec sylabu.
:::

:::zkouska
Pozor na záměnu **hallucination** a reasoning error.
:::

:::pojem term="hallucination"
Výstup, který vypadá věrohodně, ale není pravdivý.
:::

### Vlastní podnadpis bez čísla
> Citace na jednom řádku.

---

## 1.2 Schopnosti LLM
:::lo
GenAI-1.2.1 (K2) Give examples of key LLM capabilities for test tasks
:::

Text oddílu 1.2 & znaky < > se musí escapovat.

### 1.2.1 Schopnosti
```json
{"test": "case", "priority": 1}
```
"""

ZKRACENA_1 = """---
kapitola: 1
varianta: zkracena
nadpis: Úvod do generativní AI — zkráceně
podtitul: Jen to nutné ke zkoušce.
---

## 1.1 Základy generativní AI
:::lo
GenAI-1.1.1 (K1) Recall different types of AI
:::

Krátký odstavec.

:::zkouska
Chyták u zkoušky.
:::

## 1.2 Schopnosti LLM
Druhý odstavec.
"""

VYKLAD_2 = """---
kapitola: 2
varianta: vyklad
nadpis: Prompt engineering (testovací data)
podtitul: Druhá kapitola jen s výkladem.
---

## 2.1 Struktura promptu
:::lo
GenAI-2.1.1 (K2) Give examples of the structure of prompts
:::

Odstavec.

## 2.2 Použití technik
Odstavec 2.2.
"""

PRAXE_01 = """---
modul: 1
nazev: Ukázkový modul v chatu (testovací data)
podtitul: Prověří bloky Praxe, odkazy na kapitoly a sousední moduly.
cas: 1–2 h
uroven: začátečník
nastroje: ChatGPT, NotebookLM
kapitoly: 1, 2
zdroje: Shetty L3–L13; Bruno L6–L13
---

## Co postavíš
Odstavec s **tučným** textem a odkazem na [Python modul](modul:ukazka-python) i na [tahák](modul:tahak).
Odkaz na [neexistující modul](modul:neexistuje) se vykreslí jen jako text.

## Předpoklady
:::pozor nazev="Žádná firemní data"
Do veřejného chatbota nevkládej klientská data. API klíč patří do proměnné prostředí.
:::

## Postup
### 1. Otevři chatbot
:::krok
Přihlas se a otevři nový chat.
:::

:::krok nazev="Vlož prompt"
Zkopíruj prompt tlačítkem Kopírovat.

```text
You are a test analyst. Derive test conditions for the Contact Us form.
```
:::

### 2. Zkontroluj výstup
| Metrika | Co měří |
|---|---|
| recall | pokrytí požadavků |

## Cvičení
:::cviceni nazev="Testovací podmínky pro formulář"
Cíl: deset podmínek. **Hotovo**, když každá odkazuje na požadavek.
:::

:::cviceni nazev="Porovnání dvou promptů"
Porovnej zero-shot a few-shot.
:::

## Souvislost se sylabem CT-GenAI
Kapitola 2, oddíl 2.3.1.
"""

PRAXE_05 = """---
modul: 5
nazev: Ukázkový modul v Pythonu
podtitul: Druhý modul pro test sousedů a skupin.
cas: 3 h
uroven: středně pokročilý
nastroje: Python, Behave, Playwright
kapitoly: 4
zdroje: Bruno L38–L68
---

## Co postavíš
Framework v Pythonu.

## Cvičení
:::cviceni nazev="Spusť Behave"
`behave` projde bez chyby.
:::
"""

PRAXE_TAHAK = """---
modul: 0
nazev: Tahák nástrojů
podtitul: Testovací tahák.
cas: 15 min
uroven: začátečník
nastroje: všechny
kapitoly: 1, 2, 3, 4, 5
zdroje: Shetty, Bruno
---

## Nástroje v chatu
| Nástroj | Na co | Modul |
|---|---|---|
| ChatGPT | návrh testů | [Ukázkový modul](modul:ukazka-chat) |
"""

PRAXE_PROJEKT = """---
modul: 99
nazev: Závěrečný projekt
podtitul: Testovací projekt.
cas: 30–40 h
uroven: pokročilý
nastroje: Python, OpenAI API
kapitoly: 2, 4
zdroje: vlastní návrh
---

## Cíl
Asistent pro test design.

```text
specifikace -> podmínky -> případy -> Gherkin
```
"""

README = """# Testovací README

## Studijní plán CT-GenAI (testovací)

### Týden 1 – orientace
- Přečíst sylabus.
- Tahle odrážka zmiňuje pohovor a nesmí se na web dostat.

### Týden 2 – kapitola 1
- Učit se podle **learning objectives**.

## Jiná sekce
Nepatří do plánu.
"""


def otazka(id_, lo, k, i, *, n=4, spravne=None, keep_order=False, zdroj="vlastni"):
    spravne = spravne or [["a", "b", "c", "d"][i % n]]
    pis = "abcdef"[:n]
    return {
        "id": id_, "zdroj": zdroj, "lo": lo, "k": k, "body": 2 if k == "K3" else 1,
        "vyber": len(spravne), "keep_order": keep_order,
        "en": {"q": f"<p>Test question {id_} for {lo}?</p>",
               "moznosti": [f"Answer text {j + 1} of {id_}" for j, p in enumerate(pis)],
               "vysvetleni": {p: ("Correct." if p in spravne else "Incorrect.") for p in pis},
               "vysvetleni_obecne": "<p>General explanation.</p>"},
        "cz": {"q": f"<p>Testovací otázka {id_} k {lo}?</p>",
               "moznosti": [f"Text odpovědi {j + 1} otázky {id_}" for j, p in enumerate(pis)],
               "vysvetleni": {p: ("Správně." if p in spravne else "Špatně.") for p in pis},
               "vysvetleni_obecne": "<p>Obecné vysvětlení.</p>"},
        "spravne": spravne, "oddil": lo.replace("GenAI-", ""), "poznamka": "",
    }


def main() -> None:
    for slozka in ("obsah", "data"):
        cesta = ZDE / slozka
        if cesta.exists():
            import shutil
            shutil.rmtree(cesta)

    def pis(rel: str, obsah) -> None:
        p = ZDE / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(obsah if isinstance(obsah, str) else json.dumps(obsah, ensure_ascii=False, indent=1),
                     encoding="utf-8")

    pis("README.md", README)
    pis("obsah/kapitola-1/vyklad.md", VYKLAD_1)
    pis("obsah/kapitola-1/zkracena.md", ZKRACENA_1)
    pis("obsah/kapitola-2/vyklad.md", VYKLAD_2)
    pis("obsah/praxe/01-ukazka-chat.md", PRAXE_01)
    pis("obsah/praxe/05-ukazka-python.md", PRAXE_05)
    pis("obsah/praxe/tahak.md", PRAXE_TAHAK)
    pis("obsah/praxe/projekt.md", PRAXE_PROJEKT)

    pis("data/slovnik/kapitola-1.json", [
        {"en": "hallucination", "cz": "halucinace", "def": "Věrohodný, ale nepravdivý výstup.", "kap": 1,
         "oddil": "1.1.1", "klicove": True, "poznamka": "záměna s reasoning error"},
        {"en": "Token", "cz": "token", "def": "Jednotka textu pro model.", "kap": 1, "oddil": "1.1", "klicove": True},
        {"en": "chatbot", "cz": "chatbot", "def": "Konverzační aplikace.", "kap": 1, "oddil": "1.2", "klicove": False},
    ])
    pis("data/slovnik/kapitola-2.json", [
        {"en": "token", "cz": "token", "def": "Jednotka textu, počítá se do kontextového okna.", "kap": 2,
         "oddil": "2.1", "klicove": False},
        {"en": "few-shot prompting", "cz": "few-shot prompting", "def": "Prompt s několika příklady.", "kap": 2,
         "oddil": "2.9.9", "klicove": True},
    ])
    sada = {"id": "typy", "sek": "1.1.1", "nazev": "Který typ AI to je?", "zdroj": "Sylabus 1.1.1.",
            "otazka": "Zařaď příklad.", "kat": [["sym", "Symbolická AI", "symbolic AI", "Pravidla."],
                                                ["ml", "Strojové učení", "machine learning", "Data."]],
            "pol": [["Pravidla napsaná expertem", "sym", "Pravidla zapsal člověk."],
                    ["Model naučený z historie", "ml", "Učí se z dat."]]}
    pis("data/prirazovani/kapitola-1.json", [sada])
    pis("data/prirazovani/kapitola-2.json", [dict(sada, sek="2.1")])  # stejné id v jiné kapitole je v pořádku
    pis("data/cviceni/kapitola-1.json", [
        {"id": "HO-1.1.2", "uroven": "H1", "lo": "GenAI-1.1.2", "nazev": "Tokenizace", "cil": "Spočítat tokeny.",
         "zadani": "Vezmi **pět** textů.\n\n- jeden\n- dva", "kroky": ["Otevři tokenizér.", "Vlož text."],
         "prompt": "Count the tokens in:\n<text>", "co_sledovat": ["čeština má víc tokenů"],
         "projekt": "uctenky", "cas_min": 15},
        {"id": "CV-1-01", "uroven": "H2", "lo": "GenAI-1.2.1", "nazev": "Vlastní cvičení", "cil": "Cíl.",
         "zadani": "Zadání.", "kroky": [], "prompt": "", "co_sledovat": [], "projekt": "obecné", "cas_min": 10},
    ])

    # Cvičné otázky: dvě úplné zkoušky + rezerva, včetně otázky se 3 možnostmi, keep_order a výběru dvou.
    podle_kap: dict[int, list] = {}
    for x in LO_SEZNAM:
        lo, k, n = x["lo"], x["k"], x["otazek"]
        cislo = lo.replace("GenAI-", "")
        for i in range(2 * n + (1 if cislo in ("1.1.1", "2.2.1") else 0)):
            q = otazka(f"CG-{cislo}-{i + 1:02d}", lo, k, i)
            podle_kap.setdefault(int(cislo[0]), []).append(q)
    podle_kap[1][0] = otazka("CG-1.1.1-01", "GenAI-1.1.1", "K1", 0, n=3)
    podle_kap[1][1] = otazka("CG-1.1.1-02", "GenAI-1.1.1", "K1", 1, keep_order=True)
    podle_kap[1][1]["en"]["moznosti"][3] = "All of the above"
    podle_kap[3][0] = otazka("CG-3.1.1-01", "GenAI-3.1.1", "K1", 0, spravne=["a", "c"])
    for k, seznam in podle_kap.items():
        pis(f"data/cvicne-otazky/kapitola-{k}.json", {"popis": f"Testovací otázky ke kapitole {k}", "otazky": seznam})

    sample = []
    for x in LO_SEZNAM:
        for i in range(x["otazek"]):
            cislo = x["lo"].replace("GenAI-", "")
            sample.append(otazka(f"A-{len(sample) + 1:02d}", x["lo"], x["k"], i, zdroj="sample-a"))
    razeni = otazka("A-A1", "GenAI-4.1.2", "K2", 0, n=3, keep_order=True, zdroj="sample-a")
    razeni.update(typ="razeni", navic=True, vyber=3, spravne=["c", "a", "b"])
    prirazeni = otazka("A-A2", "GenAI-2.1.2", "K2", 0, n=3, keep_order=True, zdroj="sample-a")
    for j in ("en", "cz"):
        prirazeni[j]["skupiny"] = ["Skupina jedna", "Skupina dvě"]
    prirazeni.update(typ="prirazeni", navic=True, vyber=3, spravne=["1", "2", "1"])
    pis("data/vzorova-zkouska-a.json", {"popis": "Testovací Sample Exam A", "sada": "A", "verze": "1.1",
                                        "otazky": sample + [razeni, prirazeni]})

    udemy = [otazka(f"UD-TEST-{i + 1:03d}", x["lo"], x["k"], i, zdroj="podraza-practice")
             for i, x in enumerate(LO_SEZNAM) for _ in range(x["otazek"])]
    for i, q in enumerate(udemy):
        q["id"] = f"UD-TEST-{i + 1:03d}"
        q["en"]["q"] = f"<p>Udemy-only question number {i + 1} that must never leave the local folder?</p>"
    udemy.append(otazka("UD-TEST-BEZLO", "GenAI-1.1.1", "K1", 0, zdroj="shetty-tools"))
    udemy[-1]["lo"] = None
    pis("data/udemy/podraza-practice.json", {"popis": "Testovací Udemy", "zdroj": "podraza-practice",
                                             "testy": [{"nazev": "Practice Test 1", "otazky": udemy}]})
    print(f"Testovací data zapsána do {ZDE}")


if __name__ == "__main__":
    main()
