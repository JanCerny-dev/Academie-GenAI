---
modul: 99
nazev: Závěrečný projekt
podtitul: AI asistent pro test design. Ze specifikace vzniknou testovací podmínky, testovací případy, scénáře v Gherkin a spustitelné testy. Kvalitu výstupu měří metriky ze sylabu a celé to běží v CI.
cas: 40–50 h (4–5 týdnů po 10 h)
uroven: pokročilý
nastroje: Python 3.12, OpenAI API nebo Anthropic API (volitelně Ollama), Behave, Playwright, requests, pytest, GitHub Actions
kapitoly: 2, 3, 4, 5
zdroje: vlastní návrh; Bruno L32–L74 (API, Behave, Playwright); Shetty L9–L12 (test design v chatu), L38–L43 (agent nad doménovým dokumentem), L47–L48 (CI)
---

## Co postavíš

Postavíš nástroj v Pythonu, který převede textovou specifikaci na testy a sám změří, jak dobře to udělal.
Vstupem je specifikace s očíslovanými požadavky. Výstupem jsou testovací podmínky, testovací případy,
soubory `.feature` v jazyce **Gherkin** a testy, které Behave spustí proti skutečné aplikaci.
Na konci každého běhu vznikne report s metrikami kvality.

Asistent nepoužívá jeden velký prompt. Používá **prompt chaining** (řetězení promptů, sylabus 2.1.2).
Každý krok má vlastní prompt, vlastní formát výstupu a vlastní kontrolu. Chyba se tak pozná u kroku,
kde vznikla, a nepropíše se do dalších.

Projekt spojuje moduly Praxe do jednoho celku: [volání LLM z Pythonu](modul:openai),
[Behave a Playwright](modul:behave) a [GitHub Actions](modul:github-actions).
Přehled nástrojů je v [taháku](modul:tahak).

## Cílová aplikace

Projekt stojí na veřejných demo aplikacích, aby šel ukázat komukoli a nepotřeboval žádná firemní data.

Hlavní cíl je **webdriveruniversity.com**: formulář Contact Us a stránka Login Portal. Formulář má čtyři
povinná pole, kontrolu e-mailu, tlačítka SUBMIT a RESET a dvě chybové hlášky. Na takové specifikaci
se dobře ukazuje rozdělení do tříd ekvivalence i hraniční hodnoty. Kurz Gianni Bruno pracuje se stejným
formulářem, takže máš s čím porovnávat.

Rozšíření pro API je **goal-tracker API** z téhož kurzu (`https://goal-tracker-api.onrender.com/api/v1/`).
Kurz používá jen endpoint `status`. Jaké další endpointy API nabízí, si ověř sám, než pro ně napíšeš
specifikaci. Aplikace běží na bezplatném hostingu, první požadavek po pauze proto může trvat déle (neověřeno).

Druhá, soukromá datová sada je **EventHub** z kurzu Rahul Shetty. Jeho dokument požadavků má požadavky
s ID (FR-A1, FR-B4…) a tabulku obchodních pravidel. To je ideální referenční sada pro měření recall.
Aplikace se spouští lokálně z balíčku kurzu. Dokument požadavků ani kód z kurzu do veřejného repozitáře
nedávej, jsou chráněné autorským právem. Do README napiš jen souhrnná čísla z evaluace.

:::pozor nazev="Data a klíče"
Specifikaci píšeš sám a popisuje veřejnou aplikaci, do modelu tedy nejde nic citlivého.
API klíč patří do proměnné prostředí (`OPENAI_API_KEY` nebo `ANTHROPIC_API_KEY`), lokálně třeba přes
Windows Credential Manager, v CI do GitHub Actions secrets. Do repozitáře dej jen `.env.example`
s názvy proměnných bez hodnot. U poskytovatele API si nastav měsíční limit útraty.
:::

## Architektura

Diagram ukazuje tok dat. Každá šipka dolů je jeden prompt nebo jeden krok bez LLM.
Kontroly v hranatých závorkách běží bez modelu a zastaví řetězec, když výstup nesplní pravidla.

```text
 specs/contact-us.md        vlastní specifikace, požadavky REQ-CU-01 … REQ-CU-nn
          |
          |  prompt 1: testovací analýza (role, kontext, specifikace, výstup JSON)
          v
 out/conditions.json        testovací podmínky s vazbou na REQ
          |  [schéma JSON, každý REQ má aspoň jednu podmínku]
          |
          |  prompt 2: testovací návrh (třídy ekvivalence, hraniční hodnoty, few-shot příklad)
          v
 out/cases.json             testovací případy: vstupy, kroky, očekávaný výsledek
          |  [schéma JSON, vazba na podmínku, očekávaný výsledek cituje specifikaci]
          |
          |  prompt 3: implementace (katalog povolených kroků Gherkin)
          v
 features/*.feature         scénáře v Gherkin
          |  [parser Gherkin, žádný krok mimo katalog]
          |
          |  Behave + Playwright (UI), Behave + requests (API)
          v
 out/junit/*.xml            výsledky běhu testů
          |
          |  evaluace bez LLM: porovnání s reference/*.golden.json
          v
 eval/report.md             metriky, průměr a rozptyl z více běhů, porovnání verzí promptu

 CI (GitHub Actions)
   push:      lint -> unit testy s falešným LLM (bez klíče, bez nákladů)
   ručně / 1× týdně: celý řetězec s reálným modelem -> report jako artefakt
```

Kód má pět částí. Modul `llm.py` je jediné místo, které volá model. Má jednotné rozhraní pro OpenAI,
Anthropic i lokální Ollamu a ukládá odpovědi do cache podle otisku promptu. Díky cache jsou opakované
běhy zdarma a testy asistenta deterministické. Modul `pipeline.py` skládá kroky řetězce a `schema.py`
kontroluje výstupy. Modul `gherkin.py` hlídá katalog kroků. Modul `eval.py` počítá metriky.

Prompty jsou samostatné soubory ve složce `prompts/` s číslem verze v hlavičce. Každý report zapíše,
s jakou verzí promptu a s jakým modelem vznikl. To je základ **LLMOps** (sylabus 4.2.2) v malém měřítku.

## Metriky kvality

Metriky vycházejí z tabulky v oddílu 2.3.1 sylabu. Měří se proti referenční sadě, kterou napíšeš ručně
dřív, než asistenta poprvé spustíš. Jinak by ses nechal ovlivnit tím, co model vygeneroval.

| Metrika ze sylabu | Jak ji v projektu měříš |
|---|---|
| Accuracy | Podíl požadavků REQ, které vygenerované testovací případy pokrývají. |
| Precision | Podíl vygenerovaných případů, které jsou správné: odkazují na existující požadavek a očekávaný výsledek odpovídá specifikaci. Sporné případy posoudíš ručně. |
| Recall | Podíl tříd ekvivalence a hraničních hodnot z referenční sady, které vygenerované případy pokrývají. |
| Relevance a contextual fit | Podíl případů, které používají jen pole, tlačítka a hlášky ze specifikace. Vymyšlená hláška je **hallucination** (halucinace). |
| Diversity | Počet různých tříd a technik, podíl negativních a hraničních případů, počet téměř stejných případů. |
| Execution success rate | Podíl scénářů, které Behave načte a spustí bez syntaktické chyby a bez nedefinovaného kroku. |
| Time efficiency | Čas generování a revize proti času ruční tvorby referenční sady. |

Tabulka ukazuje, že většinu metrik jde spočítat automaticky. Ruční zůstává jen posouzení sporných případů
u precision a změření ruční práce u time efficiency.

Výstup LLM je **non-deterministic** (nedeterministický, sylabus 3.1.4). Jeden běh proto nic nedokazuje.
Každou konfiguraci pusť aspoň pětkrát a do reportu zapiš průměr, minimum a maximum. Teplotu nastav nízko
a u modelů, které to umí, zafixuj seed.

## Etapy

Etapy jdou po sobě. Každá končí kritériem hotovo, které jde ověřit příkazem nebo pohledem do souboru.
Zaškrtnutí se ukládá jen v tomto prohlížeči a postup uvidíš na stránce Praxe.

### Etapa 0: Repozitář a prostředí (2–3 h)

Založ repozitář, virtuální prostředí, `requirements.txt` nebo `pyproject.toml` a strukturu složek podle
oddílu Co dát na GitHub. Do `.gitignore` přidej `.env`, `out/` a `.venv/`.
Klíč načítej jen z proměnné prostředí, chybějící klíč ať skončí srozumitelnou chybou.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install behave playwright requests pytest jsonschema
python -m playwright install chromium
```

:::cviceni nazev="Etapa 0 hotová"
Příkaz `python -m asistent --help` vypíše nápovědu, `pytest` projde a v historii gitu není žádný klíč.
Ověříš to hledáním řetězce `sk-` v repozitáři.
:::

### Etapa 1: Specifikace a referenční sada (5–7 h)

Napiš vlastními slovy specifikaci formuláře Contact Us a stránky Login Portal. Každý požadavek dostane ID,
třeba `REQ-CU-03 E-mail musí obsahovat znak @`. Chování ověř ručně v prohlížeči, ne podle paměti.
Potom ručně navrhni referenční sadu: testovací podmínky a testovací případy s třídami ekvivalence
a hraničními hodnotami. Změř, jak dlouho ti to trvalo. To je základ pro time efficiency.

:::cviceni nazev="Etapa 1 hotová"
Specifikace má aspoň 12 požadavků s ID. Soubor `reference/contact-us.golden.json` má aspoň 25 případů,
každý s vazbou na požadavek. Čas ruční práce je zapsaný v `reference/README.md`.
:::

### Etapa 2: Řetězec promptů pro analýzu a návrh (6–8 h)

Napiš prompt 1 pro testovací podmínky a prompt 2 pro testovací případy. Oba mají strukturu ze sylabu 2.1.1:
roli, kontext, instrukce, vstupní data, omezení a formát výstupu. Výstup chtěj jako JSON a hned ho zkontroluj
schématem. Když JSON neprojde, pošli modelu chybu a nech ho výstup opravit, nejvýš dvakrát.

```python
import json
from jsonschema import validate

def krok(llm, prompt: str, vstup: dict, schema: dict, pokusu: int = 3) -> dict:
    zprava = prompt.format(vstup=json.dumps(vstup, ensure_ascii=False))
    for _ in range(pokusu):
        odpoved = llm.complete(zprava, temperature=0.2)
        try:
            data = json.loads(odpoved)
            validate(data, schema)
            return data
        except Exception as chyba:  # JSON nebo schéma neprošlo: model dostane chybu zpět
            zprava += f"\n\nPředchozí výstup byl neplatný: {chyba}. Vrať jen opravený JSON."
    raise RuntimeError("Model nevrátil platný výstup ani po opravách")
```

Ukázka je kostra, ne hotový kód. Rozhraní `llm.complete` si navrhni sám tak, aby šlo v testech nahradit
falešným objektem, který vrací připravené odpovědi.

:::cviceni nazev="Etapa 2 hotová"
Jeden příkaz vytvoří `out/conditions.json` a `out/cases.json`. Oba projdou schématem a každý požadavek
ze specifikace má aspoň jednu testovací podmínku. Unit testy s falešným LLM pokrývají opravu neplatného JSON.
:::

### Etapa 3: Gherkin a spustitelné testy (8–10 h)

Prompt 3 převede testovací případy na scénáře v Gherkin. Model smí použít jen kroky z katalogu, který
mu dáš v promptu, třeba `When I fill in "{pole}" with "{hodnota}"`. Step definitions k těmto krokům napíšeš
jednou ručně v Pythonu s Playwright. Katalog zvedá execution success rate: model nevymýšlí nové kroky,
které nikdo neimplementoval. Kontrola po kroku 3 odmítne scénář s krokem mimo katalog.

:::cviceni nazev="Etapa 3 hotová"
Příkaz `behave --dry-run` nehlásí žádný nedefinovaný krok. Běh proti webdriveruniversity.com projde,
nebo každé selhání máš v `eval/selhani.md` vysvětlené: chyba testu, nebo skutečná odchylka aplikace
od specifikace.
:::

### Etapa 4: Evaluace a porovnání promptů (6–8 h)

Modul `eval.py` porovná výstupy s referenční sadou a spočítá metriky z tabulky výše. Celý řetězec pusť
pětkrát. Potom vytvoř druhou verzi promptu 2, třeba s few-shot příkladem místo samotného popisu techniky,
a porovnej obě verze. To je **A/B testing** promptů ze sylabu 2.3.2. Do reportu zapiš i chyby,
které jsi ve výstupu našel ručně, a jak jsi podle nich upravil prompt (output analysis).

:::cviceni nazev="Etapa 4 hotová"
Příkaz `python -m asistent eval` vytvoří `eval/report.md` s tabulkou metrik pro verze A a B,
s průměrem, minimem a maximem z pěti běhů. Report uvádí model, teplotu a verzi promptů.
:::

### Etapa 5: CI v GitHub Actions (3–4 h)

První workflow běží při každém push: kontrola stylu a unit testy s falešným LLM. Nepotřebuje klíč a nic nestojí.
Druhé workflow spustíš ručně nebo jednou týdně. Pustí celý řetězec s reálným modelem, spustí Behave
a report nahraje jako artefakt. Klíč čte ze secrets. Počet běhů omez, ať nepřekvapí účet.

:::cviceni nazev="Etapa 5 hotová"
README má odznak zeleného buildu. Ruční spuštění evaluace vytvoří artefakt s reportem.
Klíč je jen v GitHub Actions secrets a v logu se nezobrazí.
:::

### Etapa 6: Rozšíření o API a druhou datovou sadu (volitelně, 4–6 h)

Napiš krátkou specifikaci pro goal-tracker API a nech stejný řetězec vytvořit API scénáře.
Step definitions pro API používají `requests`. Pokud máš EventHub z kurzu, spusť evaluaci i nad jeho
dokumentem požadavků lokálně a do README zapiš jen výsledná čísla.

:::cviceni nazev="Etapa 6 hotová"
Aspoň jeden soubor `.feature` pro API vznikl stejným řetězcem a projde. README porovnává metriky
pro UI a API, případně i pro EventHub.
:::

### Etapa 7: README a portfolio (3–4 h)

Dopiš README podle osnovy v další části. Nech projekt spustit kolegu jen podle README a zapiš,
kde se zasekl.

:::cviceni nazev="Etapa 7 hotová"
Kolega spustí asistenta podle README do 15 minut bez tvé pomoci. README obsahuje výsledky evaluace
a sekci Omezení.
:::

Součet etap je 37–50 hodin. Při deseti hodinách týdně to jsou čtyři až pět týdnů.
Etapy 0 až 5 tvoří ucelený projekt. Etapa 6 je bonus.

## Co dát na GitHub

Repozitář má být čitelný i pro člověka, který ho otevře na dvě minuty. Struktura:

```text
ai-test-design-assistant/
  README.md               cíl, architektura, spuštění, výsledky, omezení
  requirements.txt
  .env.example            jen názvy proměnných, žádné hodnoty
  specs/                  vlastní specifikace (contact-us.md, login.md, goal-tracker-api.md)
  reference/              ručně napsaná referenční sada + čas ruční práce
  prompts/                01-podminky.md, 02-pripady-a.md, 02-pripady-b.md, 03-gherkin.md
  asistent/               llm.py, pipeline.py, schema.py, gherkin.py, eval.py, cli.py
  features/               vygenerované scénáře (ukázka jednoho běhu)
    steps/                ručně psané step definitions (Playwright, requests)
  eval/                   report.md, selhani.md, results/*.json z jednotlivých běhů
  tests/                  unit testy s falešným LLM
  .github/workflows/      ci.yml (push), eval.yml (ručně, 1× týdně)
```

Do repozitáře nepatří API klíče, soubor `.env`, materiály z kurzů (dokument EventHub, kód z lekcí)
ani nic z práce.

README má tuto osnovu: jaký problém nástroj řeší, diagram architektury, spuštění v pěti příkazech,
tabulka výsledků evaluace, ukázka jednoho vstupu a výstupu, omezení a rizika, souvislost s ISTQB CT-GenAI.
Sekce omezení je důležitá. Ukazuje, že víš, kde nástroj selhává.

## Jak to vypadá v portfoliu

V životopise stačí jedna věta: nástroj v Pythonu, který ze specifikace generuje testy přes řetězení promptů,
spouští je v Behave a Playwright a měří kvalitu výstupu metrikami z ISTQB CT-GenAI. K tomu odkaz na repozitář.

Na pohovoru se ptají na rozhodnutí, ne na seznam technologií. Připrav si tři příběhy s vlastními čísly z reportu.
Jak se změnil recall po přidání few-shot příkladu. Jakou halucinaci metrika relevance zachytila a jak jsi
upravil prompt. Proč katalog kroků zvedl execution success rate. Čísla neodhaduj, vezmi je z `eval/report.md`.

Na LinkedIn se hodí krátký příspěvek s diagramem a jednou tabulkou výsledků. Napiš v něm i to, co nefungovalo.

## Rizika a omezení

Model občas vymyslí pole nebo hlášku, která ve specifikaci není. Proti tomu stojí kontrola relevance
a citace specifikace v očekávaném výsledku. Výstupy se mezi běhy liší, proto cache, nízká teplota a více běhů.
Referenční sada je jen tak dobrá, jak pečlivě ji napíšeš: chyby v ní zkreslí všechny metriky.
Webová demo aplikace se může změnit bez ohlášení. Když testy začnou padat všechny najednou, ověř nejdřív aplikaci.

## Souvislost se sylabem CT-GenAI

Projekt pokrývá většinu kapitoly 2. Struktura promptů a řetězení promptů jsou v
[oddílu 2.1](../kapitola-2/vyklad.html#oddil-2-1). Testovací analýza, návrh a implementace s GenAI jsou v
[oddílu 2.2](../kapitola-2/vyklad.html#oddil-2-2). Metriky a A/B testování promptů popisuje
[oddíl 2.3](../kapitola-2/vyklad.html#oddil-2-3).

Halucinace, nedeterminismus a ochrana dat jsou v [kapitole 3](../kapitola-3/vyklad.html#oddil-3-1).
Řetězec s kontrolami mezi kroky je jednoduchá testovací infrastruktura postavená na LLM
([oddíl 4.1](../kapitola-4/vyklad.html#oddil-4-1)). Verze promptů a modelů v reportu patří k LLMOps
([oddíl 4.2](../kapitola-4/vyklad.html#oddil-4-2)). Volba mezi cloudovým a lokálním modelem odpovídá
výběru LLM a SLM v [oddílu 5.1](../kapitola-5/vyklad.html#oddil-5-1).
