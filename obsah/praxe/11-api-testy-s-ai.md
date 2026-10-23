---
modul: 11
nazev: Testy API s AI
podtitul: Přidáš do BDD frameworku testy API, necháš AI navrhnout scénáře z dokumentace a kontraktu a ověříš odpovědi i data v databázi.
cas: 4–5 h
uroven: pokročilý
nastroje: Python 3.12, Behave, requests, Playwright (APIRequestContext), openai, SQLite
kapitoly: 2, 3
zdroje: Bruno L69–L74; Shetty L57–L60
---

## Co postavíš

Testy přes uživatelské rozhraní jsou pomalé a křehké. Každá změna rozložení stránky může rozbít selektor. Většina logiky aplikace ale leží za **API** (application programming interface, aplikační rozhraní). Test, který pošle požadavek přímo na server a zkontroluje odpověď, je rychlejší a spolehlivější. Proto se v testovací pyramidě testů API píše víc než testů UI.

V tomto modulu rozšíříš framework z modulu 10 o čtyři věci:

1. Generátor scénářů pro API, který z popisu endpointu vytvoří soubor `.feature` (Bruno L70).
2. Kroky v Behave, které posílají požadavky knihovnou `requests` a kontrolují odpovědi (Bruno L71–L72).
3. Úpravu `environment.py`, aby testy API neotevíraly prohlížeč (Bruno L73–L74).
4. Pomocné funkce a prompty pro práci s JSON, testy z kontraktu API a SQL dotazy pro kontrolu dat v databázi (Shetty L57–L60).

Jako cvičné API slouží Brunovo veřejné Goal Tracker API na `goal-tracker-api.onrender.com`. Endpoint `/api/v1/status` vrací stav služby. Pro SQL část použiješ ukázkové tabulky ze Shettyho kurzu (`DBTables.xlsx`) nahrané do lokální databáze SQLite.

Nové soubory ve frameworku:

```text
ai_bdd_test_framework/
├── features/
│   ├── environment.py              upraveno: prohlížeč jen pro UI scénáře
│   ├── goal_tracker_api.feature    nový, tag @api
│   └── steps/
│       └── goal_tracker_api_steps.py
└── utils/
    ├── api_test_generator.py       AI generuje scénáře pro API
    └── json_utils.py               hledání v JSON, porovnání s ignorovanými klíči
```

## Předpoklady

- Hotový framework z modulu 10 (stačí kroky 1 až 14, Allure není nutný).
- Balíček `requests`: `pip install requests` a znovu `pip freeze > requirements.txt`. Kurz verzi neuvádí. Playwright už máš, jeho `APIRequestContext` použiješ v kroku 7.
- Základní představa o HTTP: metody GET, POST, PUT, DELETE, stavové kódy (200 OK, 201 Created, 400, 401, 404, 500), formát JSON. Bruno to v L69 vysvětluje přirovnáním k číšníkovi, který odnese objednávku do kuchyně a přinese jídlo.
- Volitelně Postman nebo jiný klient pro ruční průzkum API. Stačí i prohlížeč nebo PowerShell.

:::pozor
Odpovědi skutečných API a schémata databází obsahují osobní údaje, čísla účtů a interní názvy. Do cloudového modelu z nich neposílej nic. Shetty v L60 ukazuje bezpečnější postup: modelu dáš jen schéma s pozměněnými názvy a vymyšlená data. To je minimum. U klientských systémů (banka, pojišťovna) se nesmí ven dostat ani schéma bez schváleného nástroje.
:::

## Postup

### Krok 1: Prozkoumej endpoint ručně (L69–L70)

Než napíšeš první test, podívej se, co API skutečně vrací. Bruno otevře adresu v prohlížeči a v Postmanu. Stejně dobře poslouží PowerShell:

```powershell
Invoke-RestMethod https://goal-tracker-api.onrender.com/api/v1/status
```

Podle kurzu vrací endpoint stav 200 a JSON se stavem `OPERATIONAL`. Přesnou podobu odpovědi si zapiš, budeš ji potřebovat do promptu i do asercí. Dokumentace dalších endpointů je podle Bruna na úvodní stránce API (`goal-tracker-api.onrender.com`).

Služby na Render.com v bezplatném režimu se po nečinnosti uspávají. První požadavek po delší pauze pak může trvat desítky sekund. Pro toto API jsem to neověřoval, ale počítej s tím při nastavení timeoutu.

Tento krok je **test analysis** (testovací analýza) v malém. Zjišťuješ, co je testovací báze (dokumentace a skutečné chování), jaké jsou testovací podmínky (služba odpovídá, odpověď má správný tvar a hodnotu) a co nevíš (chování při výpadku, hlavičky, rychlost).

### Krok 2: AI vygeneruje scénář pro API (L70)

Bruno vytvoří `utils/api_test_generator.py`. Znovu používá funkci `generate_text` z modulu 10, jen s novým promptem:

```python
def generate_api_tests(api_name):
    prompt = f"""
    Generate a Gherkin scenario for testing the {api_name} API. The scenarios should:
    - Be concise and focus only on the API status
    - Include minimal steps.
    - Base URL is: https://goal-tracker-api.onrender.com/
    - The end point is /status

    Example cases to consider:
    - Successful request; reponse will contain 'OPERATIONAL'
    """
    return generate_text(prompt)
```

Spuštění `python -m utils.api_test_generator` vypíše scénář. Bruno ho zkopíruje do `features/goal_tracker_api.feature` a ručně opraví adresu:

```gherkin
Feature: Check API status

Scenario: Check API status
    Given the base URL is "https://goal-tracker-api.onrender.com/api/v1/"
    When I send a GET request to "status" endpoint
    Then the response should contain "OPERATIONAL"
```

Oprava byla nutná, protože prompt uváděl základní adresu bez `/api/v1/` a endpoint s lomítkem na začátku. Model nemůže vědět, jak API skutečně vypadá. Pracuje jen s tím, co dostane. Chyba v zadání se tak propsala do testu.

Vlastní varianta promptu dává modelu úplné informace a pravidla pro kroky. Přidává i ukázku odpovědi z kroku 1 a seznam kroků, které už ve frameworku existují. Model je pak použije místo vymýšlení nových formulací (neověřeno spuštěním):

```python
PROMPT_API = """You write Gherkin scenarios for a Behave framework.

API under test: {nazev}
Full URL of the endpoint: {url}   (method GET, no authentication)
Example of a real response (status 200):
{ukazka}

Existing step phrases. Reuse them exactly, do not invent new wording for the same action:
- Given the base URL is "<url>"
- When I send a GET request to "<endpoint>" endpoint
- Then the response status code should be <code>
- Then the JSON field "<path>" should be "<value>"

Write 1 to 3 scenarios. Tag every scenario with @api.
If something cannot be tested from the information above, add it as a Gherkin comment starting with "# OPEN:".
Output plain Gherkin only."""
```

Tag `@api` už musí být u každého scénáře, protože ho v kroku 5 bude číst `environment.py`. Komentáře `# OPEN:` zachytí otázky, na které dokumentace neodpovídá. Je to stejný princip jako pole `otazky` v modulu 9.

Komentář v Gherkinu musí stát na samostatném řádku. Pokud ho model napíše za krok na stejný řádek, Behave ho vezme jako součást textu kroku a krok pak nenajde definici.

### Krok 3: Kroky pro API v Behave a requests (L71–L72)

Bruno vygeneruje šablony kroků přes `python -m behave --dry-run` (stejně jako v modulu 10) a implementuje je v `features/steps/goal_tracker_api_steps.py`:

```python
import requests

@given('the base URL is "{base_url}"')
def step_impl(context, base_url):
    context.base_url = base_url

@when('I send a GET request to "{end_point}" endpoint')
def step_impl(context, end_point):
    endpoint = f"{context.base_url}{end_point}"
    response = requests.get(endpoint)
    context.reponse = response              # L71: překlep, L72 opraveno na context.response

@then('the response should contain "{expected_text}"')
def step_impl(context, expected_text):
    assert context.response.status_code == 200, f"Expected status code 200 but got {context.response.status_code}"
    assert expected_text in context.response.text, f"Response text does not contain {expected_text}"
```

Princip je stejný jako u UI. Krok `When` provede akci a výsledek uloží do `context`. Krok `Then` ho odtud vezme a ověří. Kroky si tak předávají data jen přes kontext, ne přes globální proměnné.

V příloze L71 je překlep `context.reponse`. Krok `Then` pak hledá `context.response` a spadne na `AttributeError`. Bruno to opravuje v L72. Takový překlep neodhalí ani editor, protože `context` přijme jakýkoli atribut. Proto je užitečná třída `CustomContext` z modulu 10. Když do ní doplníš `response: requests.Response`, editor na neznámý atribut upozorní.

Kód z kurzu má ještě dvě slabiny, které v testech API potkáš často.

**Chybí timeout.** Funkce `requests.get` bez parametru `timeout` čeká na odpověď neomezeně dlouho. Když server neodpoví, test visí a v Jenkinsu blokuje celý build. Vždy uváděj `timeout=` v sekundách.

**Kontrola podřetězcem.** Aserce `"OPERATIONAL" in response.text` projde i pro odpověď `{"status": "NOT OPERATIONAL"}`. Ověřil jsem to v `zdroje/_pracovni/bruno/over_offline.py`. Text odpovědi je JSON, tak ho jako JSON rozparsuj a porovnej konkrétní pole.

Vlastní varianta kroků (neověřeno spuštěním, název pole `status` v odpovědi ověř v kroku 1):

```python
import requests
from behave import given, when, then
from utils.json_utils import najdi

TIMEOUT_S = 60          # bezplatný hosting se po nečinnosti probouzí pomalu

@given('the base URL is "{base_url}"')
def nastav_url(context, base_url):
    context.api_url = base_url.rstrip("/") + "/"

@when('I send a GET request to "{end_point}" endpoint')
def posli_get(context, end_point):
    context.response = requests.get(context.api_url + end_point.lstrip("/"), timeout=TIMEOUT_S)

@then("the response status code should be {code:d}")
def over_kod(context, code):
    assert context.response.status_code == code, (
        f"Čekal jsem {code}, přišlo {context.response.status_code}: {context.response.text[:300]}")

@then('the JSON field "{cesta}" should be "{hodnota}"')
def over_pole(context, cesta, hodnota):
    skutecna = najdi(context.response.json(), cesta)
    assert str(skutecna) == hodnota, f"{cesta}: čekal jsem {hodnota!r}, přišlo {skutecna!r}"
```

Vzor `{code:d}` řekne Behave, že parametr je celé číslo. Hodnota pak přijde jako `int` a porovnání se `status_code` funguje bez převodu. V aserci vypisuji začátek odpovědi. Když test v CI selže, hned vidíš, co server poslal, a nemusíš ho spouštět znovu.

Nepojmenoval jsem atribut `context.base_url`. Ten už používají UI kroky z modulu 10 pro adresu webu. Kdyby scénář API přepsal stejný atribut, mohl by tím rozbít UI scénář, který poběží po něm.

### Krok 4: Pomocné funkce pro JSON (Shetty L57, L59)

Shetty ukazuje na složité vnořené odpovědi, jak s JSON pomáhá AI. Postup má tři kroky. Nejdřív požádá model, ať ze vzorové odpovědi vytvoří **JSON Schema** (popis struktury: jaká pole, jakého typu, která povinná). Pak nechá ze schématu vygenerovat testovací případy: chybějící povinná pole, špatné datové typy, neplatný formát URL, prázdné seznamy. Nakonec chce kód, který odpověď projde a spočítá něco napříč vnořenými poli, například součet cen všech kurzů.

Schéma je užitečné i bez AI. Pokud vývojáři API teprve připravují, schéma existuje dřív než skutečná odpověď. Testovací případy pak můžeš navrhnout předem. Odpověď se dá proti schématu validovat knihovnou `jsonschema` (neověřeno, `pip install jsonschema`, funkce `jsonschema.validate(instance, schema)`).

Shetty generuje kód v Javě a v L58 pro odpovědi vytváří třídy POJO. To je postup typický pro Javu, kde se JSON převádí na objekty s pevnými typy. V Pythonu stačí slovníky a seznamy z `response.json()`, případně `dataclasses` nebo knihovna Pydantic, pokud chceš typovou kontrolu. Lekci L58 proto vynechávám.

Shettyho poznámka k tomu stojí za zapamatování. Model napoprvé použil jinou knihovnu na čtení JSON, než má projekt. Kód fungoval, ale v code review by neprošel. Do promptu proto patří i to, jaké knihovny a konvence projekt používá.

Do `utils/json_utils.py` dej tři malé funkce. Kód je ověřený spuštěním na ukázkových datech v `zdroje/_pracovni/bruno/over_offline.py`:

```python
def najdi(data, cesta: str):
    """Hodnota podle cesty s tečkami, čísla jsou indexy seznamu: 'goals.0.title'."""
    for kus in cesta.split("."):
        data = data[int(kus)] if isinstance(data, list) else data[kus]
    return data

def hodnoty_klice(data, klic: str):
    """Všechny hodnoty daného klíče v libovolně vnořeném JSON (např. všechny ceny)."""
    if isinstance(data, dict):
        for k, v in data.items():
            if k == klic:
                yield v
            else:
                yield from hodnoty_klice(v, klic)
    elif isinstance(data, list):
        for v in data:
            yield from hodnoty_klice(v, klic)

def porovnej(ocekavane, skutecne, ignoruj=frozenset(), cesta=""):
    """Seznam rozdílů mezi dvěma JSON strukturami. Klíče z `ignoruj` se přeskočí."""
    rozdily = []
    if isinstance(ocekavane, dict) and isinstance(skutecne, dict):
        for k in (ocekavane.keys() | skutecne.keys()) - ignoruj:
            if k not in skutecne:
                rozdily.append(f"{cesta}{k}: chybí ve skutečné odpovědi")
            elif k not in ocekavane:
                rozdily.append(f"{cesta}{k}: navíc ve skutečné odpovědi")
            else:
                rozdily += porovnej(ocekavane[k], skutecne[k], ignoruj, f"{cesta}{k}.")
    elif isinstance(ocekavane, list) and isinstance(skutecne, list):
        if len(ocekavane) != len(skutecne):
            rozdily.append(f"{cesta}: délka {len(ocekavane)} != {len(skutecne)}")
        for i, (a, b) in enumerate(zip(ocekavane, skutecne)):
            rozdily += porovnej(a, b, ignoruj, f"{cesta}{i}.")
    elif ocekavane != skutecne:
        rozdily.append(f"{cesta.rstrip('.')}: {ocekavane!r} != {skutecne!r}")
    return rozdily
```

Funkce `porovnej` řeší úlohu ze Shettyho L59. Test má uloženou očekávanou odpověď a porovnává ji se skutečnou. Některá pole se ale mění při každém volání, typicky `id`, `createdAt` nebo token. Bez jejich vynechání by test selhal pokaždé. Shetty nechá model funkci nejdřív napsat a pak ji v dalším promptu rozšíří o seznam ignorovaných klíčů. Vrací jen `true` nebo `false`. Moje varianta vrací seznam rozdílů, takže chybová hláška rovnou řekne, které pole nesedí:

```python
porovnej({"id": 1, "goal": {"title": "Run", "tags": ["a", "b"]}},
         {"id": 99, "goal": {"title": "Run", "tags": ["a", "c"]}},
         ignoruj={"id"})
# ['goal.tags.1: 'b' != 'c'']
```

Pozor na jednu věc. Funkce ignoruje klíč na všech úrovních. Pokud se pole `id` vyskytuje i ve vnořených objektech a tam se měnit nemá, potřebuješ ignorovat podle celé cesty. Takové rozšíření je dobrý úkol pro model. Dej mu tuto funkci, popiš požadavek a výsledek ověř na dvou nebo třech příkladech, které si připravíš sám.

### Krok 5: Jeden framework pro UI i API (L73–L74)

Po přidání testů API má framework problém. `before_all` spouští prohlížeč i pro běh, ve kterém jsou jen testy API. To stojí několik sekund a v CI zbytečně zatěžuje stroj. Bruno to v L73 řeší tagem `@api`. V `before_scenario` zkontroluje, jestli scénář tag má. Pokud ano, prohlížeč nespouští, jinak ho spustí:

```python
def before_scenario(context, scenario):
    if "api" in scenario.tags:
        context.is_api_test = True
    else:
        context.is_api_test = False
        context.browser = context.playwright[context.browser_type].launch(headless=context.headless_mode)
        context.page = context.browser.new_page(no_viewport=True)

def after_all(context):
    if hasattr(context, 'browser') and not context.is_api_test:
        context.browser.close()
        context.playwright.stop()
```

Myšlenka je správná, provedení má tři chyby. Zkontroluj je sám v příloze L74, než budeš číst dál.

**Prohlížeč pro každý scénář a únik procesů.** Prohlížeč se spouští v `before_scenario`, tedy pro každý UI scénář znovu. Zavírá se ale jen jednou v `after_all`. Při pěti UI scénářích zůstanou čtyři prohlížeče otevřené až do konce běhu, protože se na ně ztratí odkaz. Navíc spuštění prohlížeče pro každý scénář zpomalí přesně to, co měl refaktoring zrychlit.

**Úklid závisí na posledním scénáři.** Příznak `is_api_test` se přepisuje u každého scénáře. V `after_all` tedy platí hodnota posledního scénáře. Když běh skončí testem API, `after_all` nezavře prohlížeč ani nezastaví Playwright.

**Tag nad Feature nefunguje.** `scenario.tags` obsahuje jen tagy napsané přímo nad scénářem. Bruno to v L74 obchází pokynem, že tag `@api` se musí psát nad každý scénář a nikdy nad Feature. Behave přitom má atribut `scenario.effective_tags`, který obsahuje i zděděné tagy z Feature.

Vlastní varianta řeší všechny tři. Prohlížeč se spustí líně, tedy až u prvního UI scénáře, a pak se znovu používá. Úklid kontroluje, co skutečně existuje, ne příznak (neověřeno spuštěním):

```python
# importy a logging jako v modulu 10 (json, os, Path, sync_playwright, allure, AttachmentType)

def before_all(context):
    env = json.loads(Path("config/env.json").read_text(encoding="utf-8"))
    context.env = env
    context.base_url = env.get("base_url", "https://www.webdriveruniversity.com")
    context.playwright = None
    context.browser = None

def _prohlizec(context):
    if context.browser is None:
        context.playwright = sync_playwright().start()
        headless = os.environ.get("HEADLESS", str(context.env.get("headless", True))).lower() == "true"
        context.browser = context.playwright[context.env.get("browser", "chromium")].launch(headless=headless)
    return context.browser

def before_scenario(context, scenario):
    context.is_api_test = "api" in scenario.effective_tags
    context.page = None if context.is_api_test else _prohlizec(context).new_page()

def after_scenario(context, scenario):
    if context.page is not None:
        if scenario.status == "failed":
            allure.attach(context.page.screenshot(full_page=True), name=scenario.name,
                          attachment_type=AttachmentType.PNG)
        context.page.close()

def after_all(context):
    if context.browser is not None:
        context.browser.close()
    if context.playwright is not None:
        context.playwright.stop()
```

Ověř to spuštěním s tagem `@api`. Ve výpisu nesmí být žádná zmínka o spuštění prohlížeče a ve Správci úloh se nesmí objevit proces Chromium. Pak spusť všechno dohromady (`python custom_runner.py "@regression,@api"` pro Behave 1.2.6). Po skončení běhu nesmí zůstat žádný proces Chromium.

Pro testy API v Behave bez tagu existuje i druhé řešení. Prohlížeč spouštět jen u scénářů s tagem `@ui`. Výchozí stav je pak „bez prohlížeče“, což je pro velkou sadu testů API výhodnější. Kurz volí opačnou logiku, protože framework začínal jako čistě UI.

### Krok 6: Test API z kontraktu (Shetty L59)

**API contract** (kontrakt API) je formální popis rozhraní: endpointy, metody, parametry, tvar požadavků a odpovědí, stavové kódy. Nejčastěji má podobu specifikace OpenAPI (dříve Swagger) ve formátu YAML nebo JSON. Shetty modelu vloží kontrakt knihovní služby (přidání, načtení a smazání knihy) a nechá vygenerovat testy postupně v Javě, v Cypressu a v Pythonu s knihovnou `requests`.

Na lekci je vidět, jak dobře model pracuje s formální specifikací. Kontrakt je přesný, a tak je přesný i vygenerovaný test. Model tu nemusí hádat jako u selektorů na webové stránce. Shetty také ukazuje, že se vyplatí doptat: „Dá se to udělat lépe?“ Model pak u Cypressu sám navrhne fixtures (data v samostatném souboru) a custom commands (znovupoužitelné příkazy).

Typický test z kontraktu je **end-to-end** scénář nad jedním zdrojem: vytvoř záznam, načti ho, ověř data, smaž ho a ověř, že už neexistuje. Smazání na konci je úklid testovacích dat. Bez něj by se databáze testovacího prostředí plnila záznamy z každého běhu.

Prompt pro generování z kontraktu (vlastní šablona):

```text
Role: Jsi test analytik pro REST API.
Kontext: Níže je výňatek ze specifikace OpenAPI. Testy poběží v Behave s knihovnou requests.
Existující kroky ve frameworku: (vlož seznam kroků z goal_tracker_api_steps.py)
Úkol:
1. Vypiš testovací podmínky pro každý endpoint: úspěch, chybějící povinné pole, špatný typ, neexistující ID, chybějící autentizace.
2. Pro každou podmínku napiš scénář v Gherkinu s tagem @api.
3. Scénáře, které zakládají data, musí data na konci smazat.
Omezení: Používej jen endpointy, pole a stavové kódy uvedené ve specifikaci. Co ve specifikaci chybí, zapiš jako otázku.
Specifikace:
(vlož YAML)
```

První bod je testovací analýza, druhý návrh testů. Rozdělení do dvou kroků v jednom promptu ti umožní nejdřív zkontrolovat seznam podmínek a teprve pak číst scénáře. Pokud seznam podmínek není úplný, nemá smysl kontrolovat scénáře.

Shetty v závěru lekce zmiňuje, že stejný test jde napsat i v Playwrightu. Playwright pro Python má na požadavky bez prohlížeče objekt **APIRequestContext**. Hodí se, když chceš v jednom testu kombinovat UI a API. Například přes API připravíš data a přes UI ověříš, že se zobrazují. Krátká ukázka (neověřeno spuštěním):

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    api = p.request.new_context(base_url="https://goal-tracker-api.onrender.com/api/v1/", timeout=60_000)
    odpoved = api.get("status")
    assert odpoved.ok, odpoved.status
    print(odpoved.json())
    api.dispose()
```

Relativní adresa `status` se připojí k `base_url`. Pokud `base_url` nekončí lomítkem, poslední část cesty se nahradí, stejně jako v prohlížeči. Timeout je tu v milisekundách, na rozdíl od `requests`, kde je v sekundách.

### Krok 7: SQL dotazy s pomocí AI (Shetty L60)

Testy API a UI ověří, co aplikace ukazuje. Občas ale musíš ověřit i to, odkud čísla pocházejí. Shetty uvádí příklad z e-shopu. Web tvrdí, že nejvíc tržeb udělalo město New York. Tester to ověří dotazem do databáze. Když neumíš dobře SQL, může dotaz napsat model.

Postup ze Shettyho lekce má čtyři kroky:

1. Dej modelu **schéma** tabulek (názvy tabulek, sloupců a vazeb), ne skutečná data. Model potřebuje znát strukturu, ne obsah.
2. Pokud je i schéma citlivé, přejmenuj sloupce (`city` na `town`, `country` na `coun`). Ve výsledném dotazu je pak vrátíš zpět.
3. Uveď databázový systém (MySQL, SQL Server, PostgreSQL, Oracle). Dialekty se liší, například omezení počtu řádků je `LIMIT 1` v MySQL, ale `TOP 1` nebo `FETCH FIRST 1 ROWS ONLY` jinde.
4. Ptej se na dotaz, ne na výsledek. Výsledek musí spočítat databáze, ne model.

Shettyho příloha `DBTables.xlsx` obsahuje čtyři malé tabulky: `customers`, `orders`, `products` a `order_items`. Nahrál jsem je do SQLite a dotazy spustil (ověřeno, viz `zdroje/_pracovni/bruno/over_offline.py`). Dotaz na město s nejvyššími tržbami:

```sql
SELECT c.city, ROUND(SUM(o.total_amount), 2) AS trzby
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY trzby DESC
LIMIT 1;
-- výsledek: Mumbai | 420.99
```

Výsledek není New York. V ukázkových datech má nejvyšší součet objednávek Mumbai (420,99) a New York je druhý (385,75). Shettyho New York byl jen příklad tvrzení z webu. V reálném testu by takový rozdíl znamenal defekt: web ukazuje jiné město, než říkají data.

Data skrývají ještě jednu past. Částka `total_amount` v tabulce `orders` nesedí se součtem položek (`quantity × price`) u žádné z šesti objednávek. U objednávky 1 je `total_amount` 250,50, ale položky dávají 255,99. Kontrolní dotaz:

```sql
SELECT o.order_id, o.total_amount, ROUND(SUM(oi.quantity * p.price), 2) AS soucet_polozek
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY o.order_id
HAVING ABS(o.total_amount - SUM(oi.quantity * p.price)) > 0.01;
-- výsledek: všech 6 objednávek
```

U vymyšlených dat to nevadí. Ukazuje to ale, proč nestačí mít od modelu syntakticky správný dotaz. Otázka „které město má nejvyšší tržby“ má dvě možné odpovědi podle toho, který sloupec je zdroj pravdy. Model si jeden vybere a obvykle neřekne, že existuje i druhý. V těchto datech vyjde Mumbai oběma cestami (podle položek 750,00). Na skutečných datech se výsledky rozejít mohou. Rozhodnutí, co je zdroj pravdy, patří k testovací analýze a dělá ho člověk, ideálně s analytikem nebo vývojářem.

Shetty k tomu zmiňuje i generování velkého množství testovacích dat, třeba tisíc unikátních jmen a e-mailů pro zátěžový test. To model zvládne, ale pro tisíc řádků je levnější a opakovatelnější nechat ho napsat skript, který data vygeneruje (například knihovnou Faker se seedem), než si nechat data vypsat do chatu.

## Ověření

1. `python -m behave --tags=@api` spustí scénáře pro Goal Tracker API, projdou a ve výpisu není spuštění prohlížeče.
2. `python -m behave` (všechno) projde. Po skončení neběží v systému žádný proces Chromium spuštěný testy.
3. Tag `@api` přesunutý nad Feature (místo nad scénáře) dál funguje. To ověřuje opravu se `effective_tags`.
4. Když v souboru `.feature` změníš očekávanou hodnotu na `NOT OPERATIONAL`, test selže se srozumitelnou hláškou, která obsahuje skutečnou hodnotu pole.
5. Když dočasně změníš adresu na neexistující doménu, test selže do 60 sekund a nezasekne se.
6. `python -I zdroje/_pracovni/bruno/over_offline.py` vypíše výsledky SQL dotazů a „porovnání JSON OK“.

Kroky 1 až 5 jsem nespouštěl, protože vyžadují síť. Pomocné funkce pro JSON a SQL dotazy jsou ověřené offline na Pythonu 3.12.10 a SQLite 3.49.1.

## Časté chyby

**`AttributeError: 'Context' object has no attribute 'response'`.** Překlep v názvu atributu (v kurzu `reponse`), nebo krok `When` selhal dřív, než odpověď uložil. Podívej se na první chybu ve výpisu, ne na poslední.

**Test API spustil prohlížeč.** Tag je nad Feature a `environment.py` čte `scenario.tags`. Použij `scenario.effective_tags`.

**Test visí.** Chybí `timeout` u `requests.get`. Bezplatný hosting se navíc po nečinnosti probouzí pomalu, první požadavek dej s delším timeoutem.

**Adresa se špatně složí.** Dvě lomítka (`v1//status`) nebo žádné (`v1status`). Normalizuj lomítka na jednom místě, jako `nastav_url` v kroku 3.

**`requests.exceptions.JSONDecodeError`.** Server nevrátil JSON, typicky stránku s chybou 502 nebo 503 při probouzení služby. V aserci vypisuj `response.status_code` a začátek `response.text`, ať víš, co přišlo.

**Aserce na podřetězec projde, i když nemá.** `"OPERATIONAL" in text` platí i pro `NOT OPERATIONAL`. Porovnávej hodnotu konkrétního pole.

**Model vygeneroval endpoint nebo pole, které API nemá.** Prompt neobsahoval dokumentaci, nebo ji model doplnil podle podobných API. V promptu uveď, že smí používat jen to, co je ve specifikaci.

**SQL dotaz funguje v SQLite, ale ne v cílové databázi.** Dialekt. Uveď v promptu přesný databázový systém a verzi.

**Porovnání JSON selže na pořadí prvků v seznamu.** Funkce `porovnej` bere pořadí jako významné. Pokud API pořadí nezaručuje, seřaď seznamy před porovnáním podle stabilního klíče.

## Cvičení

:::cviceni nazev="Scénáře z dokumentace Goal Trackeru"
Cíl: projít celý cyklus od dokumentace k testu. Otevři dokumentaci na úvodní stránce Goal Tracker API, vyber dva endpointy kromě `/status` a vlož jejich popis do promptu z kroku 6. Nech model vypsat testovací podmínky a scénáře.
Hotovo: máš soubor `.feature` se scénáři pro oba endpointy, každý scénář jsi spustil a u každého, který selhal, víš, zda je chyba v testu (model si něco domyslel), nebo v API. Seznam otázek `# OPEN:` má aspoň jednu položku.
:::

:::cviceni nazev="Porovnání odpovědi se snapshotem"
Cíl: použít `porovnej` v Behave kroku. Napiš krok `Then the response should match the snapshot "<soubor>" ignoring "<klice>"`, který načte očekávaný JSON ze složky `features/snapshots/` a porovná ho s odpovědí. Klíče k ignorování se zadají čárkami.
Hotovo: scénář projde pro skutečnou odpověď a selže se srozumitelným seznamem rozdílů, když ve snapshotu změníš jednu hodnotu. Rozšíření funkce o ignorování podle celé cesty jsi nechal napsat model a ověřil ho na třech vlastních příkladech.
:::

:::cviceni nazev="SQL dotazy se změněným schématem"
Cíl: procvičit bezpečný postup ze Shettyho L60. Přejmenuj v popisu schématu `DBTables` všechny sloupce na neutrální názvy (`c1`, `c2` nebo synonyma) a požádej model o dotazy pro zbývající otázky z listu: nejprodávanější kategorie, zákazníci bez nedávné objednávky, průměrná hodnota objednávky u zákazníků s vysokou útratou.
Hotovo: dotazy po zpětném přejmenování běží v SQLite (vzor v `over_offline.py`), výsledky jsi ověřil ručně v Excelu na malých datech a u otázky „bez nedávné objednávky“ jsi rozhodl a zapsal, od jakého data se počítá „nedávno“. Model to sám určit nemůže.
:::

## Souvislost se sylabem CT-GenAI

Krok 1 a první polovina promptu v kroku 6 jsou testovací analýza podle oddílu 2.2.1 (testovací analýza s GenAI). Model z dokumentace nebo kontraktu odvozuje testovací podmínky a hlásí mezery v testovací bázi. Generování scénářů a kódu kroků z kontraktu je návrh testů a implementace testování podle oddílu 2.2.2. Úprava `environment.py` tak, aby jeden framework obsloužil UI i API, a doplnění testů API do existující sady odpovídají oddílu 2.2.3 (automatizované regresní testování s GenAI).

Opravy v krocích 2, 3 a 5 jsou hodnocení výstupu podle oddílu 2.3. Výstup modelu i kód z kurzu jsou věrohodné, ale obsahují konkrétní chyby: špatnou adresu, aserci na podřetězec, únik procesů prohlížeče. Endpointy nebo pole, která ve specifikaci nejsou, jsou halucinace z oddílu 3.1.1. Výběr zdroje pravdy u SQL dotazu je typ chyby v uvažování, kterou oddíl 3.1.2 doporučuje odhalovat nezávislou kontrolou výsledku.

Postup se schématem místo dat a s přejmenovanými sloupci je praktické opatření z oddílu 3.2.3 (jak chránit data a posílit bezpečnost). Upozornění na odpovědi API a schémata klientských systémů odpovídá rizikům úniku dat z oddílu 3.2.1.
