---
modul: 10
nazev: BDD framework – Behave, Playwright a AI
podtitul: Krok za krokem postavíš testovací framework nad formulářem Contact Us, ve kterém AI píše scénáře a navrhuje kód kroků a ty ho kontroluješ.
cas: 8–10 h
uroven: pokročilý
nastroje: Python 3.12, Behave, Playwright, openai, allure-behave, Allure CLI, VS Code
kapitoly: 2, 3
zdroje: Bruno L38–L68
---

## Co postavíš

Sedmá sekce Brunova kurzu je největší. V jednatřiceti lekcích staví od prázdné složky testovací framework, který spojuje čtyři věci. **BDD** (behavior-driven development, vývoj řízený chováním) dává testům čitelnou podobu ve větách. **Playwright** ovládá prohlížeč. **Behave** propojuje věty s kódem v Pythonu. OpenAI API pomáhá s psaním scénářů a kódu.

Tento modul prochází stejnou cestu v sedmnácti krocích. Každý krok končí něčím, co jde spustit a ověřit. Na konci máš framework, který:

- vygeneruje soubor `.feature` se scénáři pro formulář Contact Us na webdriveruniversity.com,
- má kroky napsané jednou a znovu použité v mnoha scénářích,
- otevírá a zavírá prohlížeč centrálně v `environment.py`,
- nechá AI navrhnout kód pro dosud neimplementované kroky,
- používá Scenario Outline, Background a tagy,
- spouští se vlastním runnerem, vytváří report v Allure a při selhání přiloží screenshot,
- před každým během uklidí staré výsledky.

Výsledná struktura projektu:

```text
ai_bdd_test_framework/
├── .env                         OPENAI_API_KEY (není v gitu)
├── .gitignore
├── requirements.txt
├── config/
│   ├── env.json                 base_url, prohlížeč, headless
│   └── prompts.py               prompty pro generování scénářů
├── features/
│   ├── environment.py           hooky: setup a teardown
│   ├── contact_form.feature     scénáře v Gherkinu
│   └── steps/
│       └── contact_us_form_steps.py
├── utils/
│   ├── openai_utils.py          volání OpenAI API
│   ├── analyze_steps.py         AI návrhy kódu pro kroky
│   └── types.py                 typové nápovědy pro context
├── run_tests.py                 generátor .feature (název z kurzu)
├── custom_runner.py             spouštění podle tagů + Allure
├── reports/                     výsledky Allure (generuje se)
└── screenshots/                 screenshoty selhání (generuje se)
```

Modul 11 do stejného frameworku přidá testy API a modul 12 ho spustí v Jenkinsu. Názvy souborů držím podle kurzu, aby se daly dohledat v přílohách lekcí. Kód ukazuji ve dvou podobách. Nejdřív podstatnou část z kurzu s vysvětlením, potom vlastní minimální variantu, která opravuje chyby nebo bezpečnostní slabiny originálu.

## Předpoklady

Hotový modul 9 nebo stejné znalosti: virtuální prostředí, API klíč v proměnné prostředí, první volání OpenAI API. Dál potřebuješ:

- **Python 3.12** a VS Code. Kurz natáčel na Pythonu 3.13.
- **Balíčky.** Kurz má v `requirements.txt` z L40 tyto verze: `behave==1.2.6`, `playwright==1.49.0`, `openai==1.57.0`. V L66 přidává `allure-behave` bez uvedené verze. Lokálně mám Playwright 1.61.0, Behave jsem nespouštěl. Novější řada Behave 1.3 mění syntaxi tagů (viz krok 13). Pokud chceš postupovat přesně podle kurzu, nainstaluj verze z kurzu.
- **Prohlížeče pro Playwright:** stáhne je příkaz `python -m playwright install chromium` (zhruba stovky MB).
- **Java a Allure CLI** pro HTML reporty (krok 15). Allure je program v Javě. Bruno používá JDK 21 kvůli Jenkinsu v modulu 12.
- **Rozšíření VS Code** „Cucumber (Gherkin) Full Support“ pro zvýraznění a proklik z kroku na kód. Kurz mu v L47 nastavuje cesty v `settings.json`.
- **Kredit na OpenAI.** Celý modul spotřebuje desítky volání, v řádu desítek centů.

:::pozor
Framework testuje veřejnou cvičnou stránku webdriveruniversity.com. Do promptů posíláš jen popis jejího formuláře a kód kroků. U firemní aplikace by stejný postup znamenal posílat do cloudu požadavky, zdrojový kód a selektory klienta. To bez schváleného nástroje nedělej.
:::

## Postup

### Krok 1: BDD a Gherkin za pět minut (L38–L39)

BDD popisuje chování systému příklady, kterým rozumí analytik, tester i vývojář. Příklady se píšou jazykem **Gherkin**. Soubor s příponou `.feature` obsahuje jednu funkci (Feature) a pod ní scénáře (Scenario). Každý scénář má kroky začínající klíčovými slovy:

- `Given` popisuje výchozí stav (jsem na formuláři),
- `When` popisuje akci (vyplním pole, kliknu),
- `Then` popisuje očekávaný výsledek (vidím hlášku),
- `And` a `But` pokračují předchozím druhem kroku.

```gherkin
Feature: Contact Us form functionality

  Scenario: Valid form submission
    Given I am on the Contact Us form
    When I fill in the "first_name" field with "Joe"
    And I click on the "SUBMIT" button
    Then I should see the message "Thank You for your Message!"
```

Behave ke každé větě hledá **step definition** (definice kroku). Je to funkce v Pythonu označená dekorátorem `@given`, `@when` nebo `@then` s textem, který na větu pasuje. Text může obsahovat parametry ve složených závorkách. Krok `When I fill in the "first_name" field with "Joe"` tak obslouží funkce s dekorátorem `@when('I fill in the "{field}" field with "{value}"')`.

Scénáře v kurzu píšou anglicky, protože Behave i AI s anglickými klíčovými slovy pracují nejspolehlivěji. Gherkin umí i češtinu (`# language: cs`, klíčová slova Pokud, Když, Pak), ale v týmech se používá výjimečně.

### Krok 2: Kostra projektu a první test v Playwrightu (L40)

Vytvoř složku a virtuální prostředí stejně jako v modulu 9 a nainstaluj balíčky:

```powershell
mkdir ai_bdd_test_framework
cd ai_bdd_test_framework
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install behave==1.2.6 playwright==1.49.0 openai python-dotenv allure-behave
python -m playwright install chromium
pip freeze > requirements.txt
mkdir config, features\steps, utils, reports, screenshots
```

Kurz instaluje všechny tři prohlížeče (Chromium, Firefox, WebKit). Pro tento modul stačí Chromium.

Do `config/env.json` patří nastavení prostředí. Kurz ho založí hned, ale používá ho až od L44:

```json
{
    "base_url": "https://www.webdriveruniversity.com",
    "browser": "chromium",
    "headless": true
}
```

**Headless** znamená, že prohlížeč běží bez okna. Lokálně při ladění chceš `false`, abys viděl, co test dělá. V CI chceš `true`.

Pak Bruno ověří, že Playwright funguje, krátkým skriptem `run_tests.py`:

```python
from playwright.sync_api import sync_playwright

def test_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        page = browser.new_page(no_viewport=True)
        page.goto("https://webdriveruniversity.com/Contact-Us/contactus.html")
        print("Page Title: ", page.title())
        browser.close()
```

`sync_playwright()` spustí řídicí proces Playwrightu. `launch()` otevře prohlížeč, `new_page()` v něm novou záložku. Kombinace `--start-maximized` a `no_viewport=True` zvětší okno na celou obrazovku. Bez `no_viewport` by Playwright nastavil pevnou velikost stránky 1280 × 720 bodů.

Spusť `python run_tests.py`. Otevře se Chromium, načte formulář a v terminálu se objeví titulek stránky. Tím víš, že instalace prohlížeče proběhla.

### Krok 3: Napojení na OpenAI (L41)

Bruno vytvoří tři soubory. Do `config/openai_key.json` uloží klíč. Do `config/prompts.py` slovník promptů. Do `utils/openai_utils.py` funkce pro volání API:

```python
def initialize_client():
    with open("config/openai_key.json", "r") as f:
        api_key = json.load(f)["api_key"]
    return OpenAI(api_key=api_key)

client = initialize_client()          # spustí se už při importu modulu

def load_prompt(key):
    return prompts.get(key, "")        # neznámý klíč = prázdný prompt

def generate_text(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=700)
    return response.choices[0].message.content.strip()
```

Kód má tři slabá místa. Klíč leží v souboru uvnitř projektu, takže se snadno dostane do gitu. Klient vzniká už při importu, takže každý skript, který modul jen naimportuje, spadne, když klíč chybí. A `load_prompt` při překlepu v klíči vrátí prázdný řetězec. Prázdný prompt se pak pošle modelu a zaplatíš za odpověď na nic.

Vlastní varianta `utils/openai_utils.py` řeší všechny tři (neověřeno spuštěním):

```python
import os
from functools import lru_cache
from dotenv import load_dotenv
from openai import OpenAI
from config.prompts import prompts

load_dotenv()                                  # OPENAI_API_KEY a OPENAI_MODEL z .env

@lru_cache(maxsize=1)
def _client() -> OpenAI:
    return OpenAI()                            # klient vznikne až při prvním volání

def load_prompt(key: str) -> str:
    if key not in prompts:
        raise KeyError(f"Prompt {key!r} v config/prompts.py není")
    return prompts[key]

def generate_text(prompt: str, max_tokens: int = 1500) -> str:
    odpoved = _client().chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.1,                       # Bruno přidává až v L52
    )
    return odpoved.choices[0].message.content.strip()
```

Do `.gitignore` dej hned teď `.env`, `.venv/`, `reports/`, `screenshots/` a `__pycache__/`. Proč klíč nepatří do souboru v projektu, rozebírá modul 9 v kroku 2.

Bruno integraci ověří funkcí, která požádá o jednoduchý scénář pro přihlašovací formulář a vypíše ho. Udělej totéž v interaktivním Pythonu z kořene projektu: `python -c "from utils.openai_utils import generate_text; print(generate_text('Write a simple Gherkin scenario for a login form.'))"`. Má vyjít krátký scénář s Given, When a Then.

### Krok 4: AI vygeneruje soubor .feature (L42–L43)

Do `config/prompts.py` patří prompt pro formulář. Bruno ho v L42 rozšiřuje o dvě důležité věty: každý scénář má začínat stejným krokem a výstup nemá být obalený značkami kódu. Zkrácená podoba:

```python
prompts = {
    "contact_us_form": """
    Feature: Contact Us form functionality

    Write Gherkin scenarios for testing a Contact Us form with the following details:
    - The form contains input fields: 'First Name', 'Last Name', 'Email Address', and 'Comments'.
    - All fields are mandatory. The 'SUBMIT' button submits the form. The 'RESET' button clears all fields.
    - A success message is displayed for valid submissions: 'Thank You for your Message'.
    ...
    For each scenario:
    1. Start with 'Given I am on the Contact Us form.'
    2. Include explicit steps for filling fields, clicking buttons, and validating messages.

    Generate scenarios for: valid submission, missing fields, invalid email, RESET button.
    Do not use code formatting tags. Output plain Gherkin syntax only.
    """
}
```

Kurz má na konci souboru ještě `print(json.dumps(prompts, indent=2))`. Ten řádek se provede při každém importu, takže se celý prompt vypisuje do terminálu i při generování API testů v modulu 11. Bruno to v L70 sám zmiňuje. Řádek smaž.

V L43 Bruno ukazuje, že slovník může mít víc promptů (`contact_us_form`, `login_form`). Generátor pak vybírá podle klíče. Tak se dá z jednoho skriptu generovat víc feature souborů.

Generátor v `run_tests.py` (kurz tak soubor pojmenoval, i když testy nespouští) načte prompt, zavolá model a výsledek uloží:

```python
def generate_scenarios():
    prompt = load_prompt("contact_us_form")
    scenarios = generate_text(prompt)
    feature_file_path = "features/contact_form.feature"
    try:
        with open(feature_file_path, "x") as f:     # "x" = vytvoř, jen když soubor neexistuje
            f.write(scenarios)
    except FileExistsError:
        print(f"{feature_file_path} already exists. Skipping overwrite...")
```

Režim `"x"` je dobrý nápad. Vygenerovaný soubor budeš v dalších krocích ručně upravovat. Druhé spuštění generátoru by tvou práci přepsalo novou, jinou verzí od modelu. Doplň ještě `encoding="utf-8"`, jinak Windows zapíše soubor v kódování cp1250.

Výsledek z kurzu (příloha L42) má čtyři scénáře. První vypadá takto:

```gherkin
Scenario: Valid form submission
    Given I am on the Contact Us form
    When I fill in 'First Name' with 'John'
    And I fill in 'Last Name' with 'Doe'
    And I fill in 'Email Address' with 'john.doe@example.com'
    And I fill in 'Comments' with 'This is a test message'
    And I click on the 'SUBMIT' button
    Then I should see the success message 'Thank You for your Message'
```

Při revizi si všimni tří věcí. Kroky jsou čitelné, ale každý má hodnotu napevno, takže by potřeboval vlastní kód. Názvy polí jsou popisky z obrazovky, ne identifikátory, podle kterých je najde automatizace. A očekávaná hláška chybí vykřičník, protože chyběl už v promptu. Model vyrobil přesně to, co dostal. Revize vygenerovaného výstupu člověkem je tady povinná, ne volitelná.

### Krok 5: Setup a teardown v environment.py (L44–L45)

Behave hledá soubor `features/environment.py` a volá v něm funkce zvané **hooks** (háčky) v pevně daných okamžicích. Kurz používá čtyři:

| Hook | Kdy se volá | Co v něm frameworku dělá |
|---|---|---|
| `before_all` | jednou před všemi testy | načte `env.json`, spustí Playwright a prohlížeč |
| `before_scenario` | před každým scénářem | otevře novou stránku |
| `after_scenario` | po každém scénáři | zavře stránku (později screenshot) |
| `after_all` | jednou po všech testech | zavře prohlížeč, zastaví Playwright |

Rozdělení má důvod. Spuštění prohlížeče trvá sekundy, takže se dělá jednou. Nová stránka pro každý scénář zajistí, že si scénáře nepředávají cookies ani vyplněná pole. Metoda `browser.new_page()` navíc pro každou stránku vytvoří samostatný kontext prohlížeče, takže je izolace úplná.

Všechno, co hooky vytvoří, ukládají do objektu `context`. Behave ho předává každému kroku. Krok pak sáhne na `context.page` a nemusí vědět, odkud stránka přišla. To je hlavní myšlenka celé architektury. Kroky popisují jen práci se stránkou, správa prohlížeče je na jednom místě.

Bruno v L45 přidává modul `logging` místo `print`. Výhoda je časové razítko a úroveň zprávy (INFO, ERROR). Výpis se pak dá filtrovat a v Jenkinsu je čitelnější.

Vlastní minimální `features/environment.py` pro tento krok (neověřeno spuštěním):

```python
import json, logging, os
from pathlib import Path
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("framework")

def before_all(context):
    env = json.loads(Path("config/env.json").read_text(encoding="utf-8"))
    context.base_url = env.get("base_url", "https://www.webdriveruniversity.com")
    headless = os.environ.get("HEADLESS", str(env.get("headless", True))).lower() == "true"
    context.playwright = sync_playwright().start()
    context.browser = context.playwright[env.get("browser", "chromium")].launch(headless=headless)
    log.info("Prohlížeč spuštěn (headless=%s)", headless)

def before_scenario(context, scenario):
    log.info("Scénář: %s", scenario.name)
    context.page = context.browser.new_page()

def after_scenario(context, scenario):
    context.page.close()

def after_all(context):
    context.browser.close()
    context.playwright.stop()
```

Oproti kurzu jsou tu dvě změny. Ukládám `base_url` do kontextu, protože kurz ho sice má v `env.json`, ale v krocích pak píše celou adresu napevno. A proměnná prostředí `HEADLESS` umí přepsat hodnotu z `env.json`. V Jenkinsu tak spustíš testy bez okna a nemusíš měnit soubor v repozitáři.

`context.playwright["chromium"]` funguje, protože objekt Playwright zpřístupňuje prohlížeče i přes hranaté závorky. Hodnotu `browser` v `env.json` tak můžeš přepnout na `firefox` nebo `webkit` bez změny kódu, pokud jsi ty prohlížeče nainstaloval.

### Krok 6: Šablony kroků přes dry run (L46–L47)

Teď má Behave soubor `.feature`, ale žádné definice kroků. Bruno nechá v souboru jen první scénář (ostatní zakomentuje) a spustí:

```powershell
python -m behave --dry-run
```

Volba `--dry-run` nic nespouští, jen zkontroluje, ke kterým krokům chybí definice. Pro chybějící kroky vypíše hotové šablony:

```python
@given(u'I am on the Contact Us form')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I am on the Contact Us form')
```

Šablony zkopíruj do `features/steps/contact_us_form_steps.py` a nahoru přidej `from behave import given, when, then`. Předponu `u` u řetězců můžeš smazat, v Pythonu 3 nic nedělá. Behave načítá všechny soubory `.py` ve složce `features/steps` automaticky.

Opakované `python -m behave --dry-run` teď ukáže nulu nedefinovaných kroků. Když spustíš `python -m behave` bez `--dry-run`, otevře se a zavře prohlížeč a první krok spadne na `NotImplementedError`. Bruno ho v L47 nahradí `print("TO DO 1!!!!")`, aby viděl, že se krok opravdu volá.

V L47 také nastavuje rozšíření pro VS Code, aby ve feature souboru poznalo definované kroky a umělo na ně prokliknout. Do uživatelského `settings.json` přidá:

```json
"cucumberautocomplete.strictGherkinCompletion": true,
"cucumberautocomplete.steps": ["features/steps/*.py"],
"cucumberautocomplete.syncfeatures": "features/*feature"
```

Po změně je potřeba okno znovu načíst (*Developer: Reload Window*). Rozšíření občas kroky nerozpozná hned. Rozhodující je výstup `--dry-run`, ne podtržení v editoru.

### Krok 7: Parametrizace kroků podle DRY (L48)

Když odkomentuješ zbylé scénáře, `--dry-run` nahlásí spoustu nových nedefinovaných kroků. Věta `When I fill in 'First Name' with 'Jane'` se od `... with 'John'` liší jen jménem. Behave je ale bere jako dva různé kroky. S napevno zapsanými hodnotami bys potřeboval funkci pro každou kombinaci pole a hodnoty.

Princip **DRY** (don't repeat yourself, neopakuj se) to řeší parametry. Bruno přepíše věty ve feature souboru tak, aby se proměnná část dala vyjmout:

```gherkin
When I fill in the "first_name" field with "Joe"
And I click on the "SUBMIT" button
Then I should see the success message saying "Thank You for your Message!"
```

Dvě změny stojí za pozornost. Hodnoty jsou v dvojitých uvozovkách, se kterými se ve vzorech kroků lépe pracuje. A místo popisku „First Name“ je v kroku hodnota atributu `name` ze stránky (`first_name`, `last_name`, `email`, `message`). Bruno k tomu dojde až v L57, kdy zjistí, že podle popisků pole na stránce nenajde. Je to kompromis. Krok je o něco technickější, ale selektor se dá sestavit přímo z parametru.

Pak smaže celý soubor kroků, znovu spustí `--dry-run` a z nových šablon vznikne šest definic, které pokryjí všechny čtyři scénáře:

```python
@given('I am on the Contact Us form')
def navigate_to_contact_us_form(context): ...

@when('I fill in the "{field}" field with "{value}"')
def fill_in_field(context, field, value): ...

@when('I click on the "{button}" button')
def click_button(context, button): ...

@then('I should see the success message saying "{message}"')
def verify_success_message(context, message): ...

@then('I should see an error message saying "{message}"')
def verify_error_message(context, message): ...

@then('all fields should be cleared')
def verify_all_fields_cleared(context): ...
```

Bruno také přejmenuje funkce z generického `step_impl` na popisné názvy. Behave na názvu nezáleží, ale ve výpisu chyb a v editoru se popisné názvy čtou mnohem lépe.

### Krok 8: Vlastní kontext pro nápovědu v editoru (L49–L50)

Objekt `context` je v Behave obecný. Editor neví, že `context.page` je stránka Playwrightu, a nenabízí její metody. Bruno proto v L49 definuje třídu jen pro **type hints** (typové nápovědy) a v L50 ji podle DRY přesune do samostatného souboru `utils/types.py`, aby ji nemusel opakovat v každém souboru:

```python
from playwright.sync_api import Playwright, Browser, Page

class CustomContext:
    page: Page            # záložka, se kterou test pracuje
    browser: Browser      # spuštěný prohlížeč
    playwright: Playwright
```

V krocích pak píše `def fill_in_field(context: CustomContext, field, value)`. Za běhu se nic nemění, Behave dál předává svůj vlastní objekt. Třída jen říká editoru a čtenáři, co v kontextu najde. Editor pak po napsání `context.page.` nabídne `fill`, `click` a další metody.

První skutečně implementované kroky z L49:

```python
@given('I am on the Contact Us form')
def navigate_to_contact_us_form(context: CustomContext):
    context.page.goto("https://webdriveruniversity.com/Contact-Us/contactus.html")

@when('I fill in the "{field}" field with "{value}"')
def fill_in_field(context: CustomContext, field, value):
    field_selector = f'[name="{field}"]'
    context.page.wait_for_selector(field_selector)
    context.page.fill(field_selector, value)
```

Selektor `[name="first_name"]` je **CSS selector**, který najde prvek podle atributu `name`. Volání `wait_for_selector` počká, až se prvek objeví. Playwright ale u `fill` čeká automaticky, takže tento řádek je navíc. Nevadí, jen zbytečně prodlužuje kód.

### Krok 9: AI navrhne kód pro neimplementované kroky (L51–L52)

Zbývají čtyři kroky s `print("TO DO!")`. Místo ručního psaní nechá Bruno model analyzovat soubor kroků a navrhnout implementaci. Skript `utils/analyze_steps.py` načte soubor kroků, přidá k němu popis prostředí a pošle to modelu:

```python
environment_context = """
The automation framework is already set up to initialize Playwright in environment.py.
This includes setting up the browser, creating a new page, and managing teardown processes.
Avoid reinitializing Playwright in step definitions as it is redundant.
You can access the current page using 'context.page'.
"""

prompt = f"""
{environment_context}

Analyze the following Behave step definitions.
For each unimplemented step, provide example Python code to implement it,
using Playwright for browser automation.

Behave steps:
{steps}
"""
```

Proměnná `environment_context` je nejcennější část celé lekce. Bez ní model nezná architekturu frameworku. Typicky by v každém kroku znovu spouštěl `sync_playwright()` a otevíral vlastní prohlížeč. Kontext mu řekne, co už existuje a kde to najde. Sylabus tomu v oddílu 2.1.1 říká komponenta Context a v oddílu 2.2.3 zdůrazňuje, že model musí znát konvence existujícího frameworku.

V L52 Bruno v `generate_text` přidá `temperature=0.1` a `top_p=1.0`, aby opakovaná spuštění dávala podobné návrhy. Skript spouští z kořene projektu jako modul:

```powershell
python -m utils.analyze_steps
```

Spuštění přes `-m` je důležité. Python pak bere kořen projektu jako výchozí místo pro importy a `from utils.openai_utils import generate_text` funguje. Spuštění `python utils\analyze_steps.py` by skončilo chybou `ModuleNotFoundError: No module named 'utils'`.

V kódu z kurzu je drobná chyba. Načtení souboru chytá výjimku `FileExistsError`, ale chybějící soubor vyvolá `FileNotFoundError`. Při špatné cestě tedy skript spadne s výpisem výjimky místo srozumitelné hlášky. Model ten kód psal s Brunem a nikdo si toho nevšiml, protože soubor vždycky existoval.

Vlastní varianta posílá i feature soubor (model pak vidí, jak se kroky používají) a do promptu přidává konkrétní pravidla. Návrhy ukládá do souboru, aby se daly porovnat mezi běhy (neověřeno spuštěním):

```python
from pathlib import Path
from utils.openai_utils import generate_text

KONTEXT = """Framework: Behave + Playwright sync API for Python.
Playwright is started in features/environment.py. Use only context.page, never start a browser.
Use only real Playwright sync API methods (page.fill, page.click, page.locator(...).input_value(),
expect from playwright.sync_api). If unsure that a method exists, say so instead of guessing.
Steps starting with 'Then' must contain an assertion."""

def analyzuj(steps_soubor: str, feature_soubor: str, vystup: str = "ai_suggestions.md") -> None:
    kroky = Path(steps_soubor).read_text(encoding="utf-8")
    feature = Path(feature_soubor).read_text(encoding="utf-8")
    prompt = (f"{KONTEXT}\n\nFeature file:\n{feature}\n\nStep definitions:\n{kroky}\n\n"
              "For each step that only prints TO DO or raises NotImplementedError, propose an implementation.")
    Path(vystup).write_text(generate_text(prompt, max_tokens=2000), encoding="utf-8")
    print(f"Návrhy uloženy do {vystup}. Nic se nezapsalo do kódu, převzetí je na tobě.")

if __name__ == "__main__":
    analyzuj("features/steps/contact_us_form_steps.py", "features/contact_form.feature")
```

Skript návrhy jen ukládá. Do souboru kroků je nikdy nepíše sám. O převzetí kódu rozhoduje člověk po kontrole.

### Krok 10: Kontrola AI návrhů a dokončení kroků (L53–L57)

Lekce L53 až L57 ukazují, jak s návrhy z modelu pracovat. Bruno nic nepřebírá naslepo. Návrh zkopíruje, spustí test a podle výsledku ho opraví. Soubor `ai-suggestions.txt` v přílohách zachycuje tři typy problémů, které potkáš u každého generovaného testovacího kódu.

**Více variant, jedna správná.** Pro klik na tlačítko dostal Bruno tři selektory: `[name="SUBMIT"]`, `button:has-text("SUBMIT")` a `button=SUBMIT`. Žádný nefungoval. Tlačítka na stránce nejsou prvky `<button>`, ale `<input type="submit" value="SUBMIT">`. Správný selektor `[value="SUBMIT"]` našel Bruno sám v nástrojích pro vývojáře v prohlížeči. Model stránku neviděl, takže hádal podle nejčastějšího vzoru.

**Neexistující metoda.** Pro kontrolu vymazaných polí model navrhl `context.page.locator(field_selector).value()`. Locator v Playwrightu metodu `value()` nemá. Správně je `input_value()`. Kód vypadá věrohodně a projde kontrolou syntaxe, spadne až za běhu. To je typická **halucinace** v generovaném kódu.

**Neexistující výjimka.** Návrh pro kontrolu hlášky obsahoval `except Error.TimeoutError:`. Objekt `Error` tam neexistuje. Bruno místo toho importuje `from playwright.sync_api import TimeoutError`. Pozor, tento import zastíní vestavěnou výjimku `TimeoutError` z Pythonu. V tomto souboru to nevadí, ve větším kódu je čitelnější `from playwright.sync_api import TimeoutError as PlaywrightTimeout`.

Bruno v L54 ještě rozšíří prompt o větu, aby kroky s `Then I should see` vždy obsahovaly aserci. První návrhy totiž jen čekaly na prvek a nic neověřovaly. Test bez aserce nikdy neselže, a tedy nic netestuje.

Pro chybové hlášky použije v L57 jiný selektor než pro úspěch. Chybová stránka nemá hlášku v samostatném prvku, je to prostý text v `<body>`. Proto `//body[contains(., "{message}")]`. Hledá text kdekoli v těle stránky.

Výsledný soubor kroků z kurzu má kolem sedmdesáti řádků, hlavně kvůli logování a ručnímu `try/except`. Playwright má pro aserce vlastní funkci `expect`, která sama čeká a sama hlásí srozumitelnou chybu. Vlastní minimální varianta celého souboru `features/steps/contact_us_form_steps.py` (neověřeno spuštěním):

```python
from behave import given, when, then
from playwright.sync_api import expect
from utils.types import CustomContext

POLE = ("first_name", "last_name", "email", "message")

@given("I am on the Contact Us form")
def otevri_formular(context: CustomContext):
    context.page.goto(f"{context.base_url}/Contact-Us/contactus.html")

@when('I fill in the "{field}" field with "{value}"')
def vypln_pole(context: CustomContext, field, value):
    if value == "\\n":                       # dohoda z tabulky Examples: pole nechat prázdné (krok 11)
        return
    context.page.fill(f'[name="{field}"]', value)

@when('I click on the "{button}" button')
def klikni(context: CustomContext, button):
    context.page.click(f'input[value="{button}"]')

@then('I should see the message "{expected_message}"')
def over_zpravu(context: CustomContext, expected_message):
    expect(context.page.locator("body")).to_contain_text(expected_message, timeout=5000)

@then("all fields should be cleared")
def over_prazdna_pole(context: CustomContext):
    for name in POLE:
        expect(context.page.locator(f'[name="{name}"]')).to_have_value("")
```

Krok `I should see the message` nahrazuje oba původní kroky pro úspěch i chybu. Bruno k němu dojde v L60. Kontrola textu v `body` funguje pro stránku s poděkováním i pro chybovou stránku. Timeout 5 sekund je delší než Brunovy 2 sekundy. Veřejná stránka občas odpovídá pomalu a krátký timeout pak dělá **flaky** testy (nestabilní, jednou projdou a jednou ne).

V tomto bodě by měly projít všechny čtyři scénáře: `python -m behave`.

### Krok 11: Scenario Outline (L58–L60)

Scénáře pro úspěšné odeslání a pro neplatný e-mail mají stejné kroky, liší se jen daty. **Scenario Outline** (šablona scénáře) je zapíše jednou a data dá do tabulky **Examples**. Behave pak spustí scénář jednou pro každý řádek tabulky a do míst `<nazev_sloupce>` dosadí hodnoty:

```gherkin
Scenario Outline: Form submission scenarios
    When I fill in the "first_name" field with "<first_name>"
    And I fill in the "last_name" field with "<last_name>"
    And I fill in the "email" field with "<email>"
    And I fill in the "message" field with "<message>"
    And I click on the "<button>" button
    Then I should see the message "<expected_message>"

    Examples:
        | first_name | last_name | email                  | message                    | button | expected_message               |
        | Joe        | Blogs     | joe_blogs@example.com  | Please can you contact me? | SUBMIT | Thank You for your Message!    |
        | Sarah      | Woods     | sarah_woodsexample.com | Hello World                | SUBMIT | Error: Invalid email address   |
        | \n         | \n        | \n                     | \n                         | SUBMIT | Error: all fields are required |
```

Třetí řádek řeší prázdná pole. Prázdnou hodnotu by krok `fill` zapsal jako prázdný řetězec, což je u prázdného pole totéž. Bruno ale chce pole úplně přeskočit, a proto zvolil dohodnutou značku `\n`. Krok ji v kódu porovnává s `"\\n"`, protože z tabulky přijde jako dva znaky: zpětné lomítko a písmeno n, ne jako nový řádek. Je to funkční, ale nečitelné. Srozumitelnější značka by byla třeba `<prázdné>` nebo `-`. Ať zvolíš cokoli, napiš to do komentáře nad tabulku.

Tabulka Examples je místo, kde se uplatní techniky návrhu testů. Každý řádek je jeden testovací případ. Doplnit řádky pro hraniční hodnoty a třídy ekvivalence (e-mail bez domény, e-mail s mezerou, velmi dlouhý komentář) je přesně úloha, kterou můžeš zadat modelu. Výsledek ale stejně jako u kroků zkontroluj. Model nezná skutečnou validaci stránky a očekávané hlášky si může domyslet.

Bruno v L59 ještě ukazuje, že Scenario Outline se dá přehnat. Když se do jedné šablony nacpou scénáře s různou logikou, tabulka je široká a scénář ztrácí srozumitelnost. Proto scénář pro RESET a pro chybějící pole zůstávají samostatné.

### Krok 12: Background (L61–L62)

Každý scénář začíná krokem `Given I am on the Contact Us form`. Klíčové slovo **Background** (pozadí) zapíše společné kroky jednou na začátek feature souboru. Behave je spustí před každým scénářem, včetně každého řádku Scenario Outline:

```gherkin
Feature: Contact Us form functionality

    Background: Pre-conditions
        Given I am on the Contact Us form

    Scenario Outline: Form submission scenarios
        When I fill in the "first_name" field with "<first_name>"
        ...
```

Background patří jen pro předpoklady, které opravdu platí pro všechny scénáře v souboru. Jakmile by jeden scénář potřeboval začít jinde, Background už nesedí a krok musí zpět do scénářů. Background se také nemá rozrůst do dlouhé sekvence kroků. Čtenář scénáře pak nevidí, v jakém stavu test začíná.

### Krok 13: Tagy (L63–L64)

**Tag** (štítek) je slovo se zavináčem nad Feature nebo Scenario. Umožní spustit jen část testů. Bruno označí celý soubor `@regression` a dva rychlé scénáře `@smoke`:

```gherkin
@regression
Feature: Contact Us form functionality
    ...
    @smoke
    Scenario: Missing fields
    ...
    @smoke
    Scenario: Using the 'RESET' button
```

Tag nad Feature dědí všechny scénáře v souboru. Spuštění podle tagu:

```powershell
python -m behave --tags=@smoke          # jen dva smoke scénáře
python -m behave --tags=@regression     # všech pět (3 řádky Outline + 2 scénáře)
```

Kombinace tagů se zapisují podle verze Behave různě. Kurz používá Behave 1.2.6 se starou syntaxí. Čárka znamená „nebo“, opakovaná volba `--tags` znamená „a zároveň“ a vlnovka znamená „ne“: `--tags=@smoke,@api` nebo `--tags=@regression --tags=~@slow`. Novější řada Behave 1.3 přijímá čitelné výrazy jako `--tags="@regression and not @slow"` (neověřeno). Pokud se ti kombinace tagů chová divně, nejdřív zkontroluj `pip show behave`.

### Krok 14: Vlastní runner (L65)

Psát dlouhé příkazy s volbami je otravné a v CI se snadno udělá překlep. Bruno proto vytvoří `custom_runner.py`, který zavolá Behave přímo z Pythonu:

```python
from behave.__main__ import main as behave_main

if __name__ == "__main__":
    behave_main(["--tags", "@regression"])
```

Funkce `behave_main` dostane stejný seznam voleb, jaký bys napsal do příkazové řádky. Výhoda je, že do runneru můžeš přidat logiku. V dalších krocích přibude formát pro Allure a úklid složek. V modulu 12 přibude výběr tagu z Jenkinsu. Runner zatím vrací návratový kód z Behave jen implicitně. Pro CI je lepší napsat `raise SystemExit(behave_main([...]))`, aby neúspěšné testy vrátily nenulový kód.

### Krok 15: Reporty v Allure (L66)

Textový výstup Behave se dobře čte v terminálu, ale špatně se sdílí. **Allure Report** vytvoří z výsledků HTML stránku s přehledem, historií a přílohami. Má dvě části: formátovač pro Behave, který při běhu zapisuje výsledky jako soubory JSON, a nástroj příkazové řádky, který z nich sestaví web.

Formátovač je balíček `allure-behave` (už nainstalovaný v kroku 2). V runneru se zapne dvěma volbami:

```python
import os
from behave.__main__ import main as behave_main

if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)
    behave_main([
        "--tags", "@regression",
        "--format", "allure_behave.formatter:AllureFormatter",
        "--outfile", "reports/allure-results",
    ])
```

Kurz tím nahradí výchozí výstup do terminálu. Pokud chceš vidět průběh i v terminálu, přidej ještě `"--format", "pretty"`. Behave umí více formátů najednou.

Nástroj Allure na Windows Bruno instaluje ručně. Stáhne zip z GitHubu (allure-framework/allure2, sekce Releases), rozbalí ho a složku `bin` přidá do proměnné prostředí `PATH`. Allure potřebuje Javu, `java -version` musí fungovat. Pro Mac a Linux je v přílohách L66 návod s Homebrew a `wget`. Kontrola instalace: `allure --version`.

Report vznikne a otevře se dvěma příkazy:

```powershell
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

První příkaz sestaví statický web do `reports/allure-report`, volba `--clean` smaže předchozí verzi. Druhý spustí lokální web server a otevře prohlížeč. Server ukončíš klávesami Ctrl+C. Pro rychlé prohlížení stačí jeden příkaz `allure serve reports/allure-results`, který report sestaví do dočasné složky a rovnou ho otevře.

Report HTML neotevírej dvojklikem ze souboru. Prohlížeč pak kvůli bezpečnostním pravidlům nenačte data a stránka zůstane prázdná nebo ukazuje „Loading“.

### Krok 16: Screenshot při selhání (L67)

Když UI test selže, první otázka zní: co bylo v tu chvíli na obrazovce? Bruno v `after_scenario` zjistí, zda scénář selhal, uloží screenshot do složky `screenshots` a přiloží ho k reportu v Allure:

```python
if scenario.status == "failed":
    screenshot_path = f"screenshots/{scenario.name.replace(' ', '_')}.png"
    context.page.screenshot(path=screenshot_path)
    with open(screenshot_path, "rb") as image_file:
        allure.attach(image_file.read(), name=scenario.name, attachment_type=AttachmentType.PNG)
```

Potřebné importy jsou `import allure` a `from allure_commons.types import AttachmentType`. Porovnání `scenario.status == "failed"` funguje, protože stav v Behave se umí porovnat s řetězcem. Přesnější zápis je `from behave.model_core import Status` a `scenario.status == Status.failed`.

Metoda `screenshot()` bez parametru `path` vrátí obrázek rovnou jako bajty. Nemusíš ho tedy zapisovat na disk a pak znovu číst. Vlastní varianta `after_scenario`:

```python
import re
import allure
from allure_commons.types import AttachmentType
from pathlib import Path

def after_scenario(context, scenario):
    if scenario.status == "failed":
        png = context.page.screenshot(full_page=True)
        allure.attach(png, name=scenario.name, attachment_type=AttachmentType.PNG)
        jmeno = re.sub(r"[^\w.-]+", "_", scenario.name)[:100]      # bezpečný název souboru
        Path("screenshots").mkdir(exist_ok=True)
        (Path("screenshots") / f"{jmeno}.png").write_bytes(png)
    context.page.close()
```

Nahrazení všech zvláštních znaků je důležité. Název scénáře z Outline obsahuje dvojtečky, zavináče nebo uvozovky. Některé z těchto znaků Windows v názvu souboru nepovolí. Kurzové `replace(' ', '_')` řeší jen mezery a navíc předpokládá, že složka `screenshots` existuje. Bez ní `page.screenshot(path=...)` skončí chybou.

Ověření: Bruno záměrně pokazí dva řádky v Examples (přidá do očekávané hlášky „555“). Dva scénáře selžou a v reportu Allure mají u kroku přiložený screenshot. Udělej totéž a pak změnu vrať.

### Krok 17: Úklid před během (L68)

Každý běh přidává do `reports/allure-results` nové soubory JSON a do `screenshots` nové obrázky. Staré výsledky by se v reportu míchaly s novými. Bruno proto do runneru přidá funkci, která složky před během smaže a znovu vytvoří:

```python
import shutil

def clean_and_create_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

clean_and_create_folder("reports")
clean_and_create_folder("screenshots")
```

Funkce maže celou složku `reports`, tedy i dříve vygenerovaný HTML report. To je záměr, report se po každém běhu vytváří znovu. Pokud chceš v Allure vidět trend mezi běhy, musíš před smazáním zkopírovat složku `history` z posledního reportu do nových výsledků. Jenkins to v modulu 12 dělá za tebe.

Funkce `shutil.rmtree` maže bez potvrzení a bez koše. Proto do ní nikdy nedávej cestu z proměnné, kterou může někdo přepsat zvenku. Názvy složek nech napevno v kódu.

Celý runner po tomto kroku (vlastní varianta, neověřeno spuštěním):

```python
import os, shutil, sys
from behave.__main__ import main as behave_main

def vycisti(slozka: str) -> None:
    shutil.rmtree(slozka, ignore_errors=True)
    os.makedirs(slozka, exist_ok=True)

if __name__ == "__main__":
    vycisti("reports")
    vycisti("screenshots")
    tags = sys.argv[1] if len(sys.argv) > 1 else "@regression"
    raise SystemExit(behave_main([
        "--tags", tags,
        "--format", "allure_behave.formatter:AllureFormatter", "--outfile", "reports/allure-results",
        "--format", "pretty",
    ]))
```

Spuštění: `python custom_runner.py @smoke`. Modul 12 tento runner rozšíří o čtení tagu z Jenkinsu.

### Kde AI v tomto frameworku pomohla a kde ne

Po sedmnácti krocích stojí za to se ohlédnout. AI ve frameworku dělala tři věci. Vygenerovala první verzi scénářů z popisu požadavků. Navrhla šablony implementace pro kroky. A v kurzu ještě radila s nastavením nástrojů, například s instalací Allure.

Všechny tři výstupy potřebovaly opravu. Scénáře měly hodnoty napevno a chybnou hlášku převzatou z promptu. Kód kroků obsahoval neexistující metody a selektory pro prvky, které na stránce nejsou. Bez spuštění testu a bez pohledu do nástrojů pro vývojáře by framework nefungoval.

Užitek je přesto reálný. Model ušetřil psaní kostry a Bruno se mohl soustředit na kontrolu. Klíčem je, že framework má jasnou strukturu. Kroky jsou krátké a parametrizované a správa prohlížeče je na jednom místě. Model dostal tuto strukturu v kontextu a jeho návrhy do ní zapadly. Čím chaotičtější framework, tím horší návrhy.

## Ověření

Framework je hotový, když z kořene projektu platí všechno níže:

1. `python -m behave --dry-run` ukazuje `0 undefined` u kroků.
2. `python custom_runner.py @regression` skončí s výsledkem 1 feature passed a 5 scenarios passed. Kurz uvádí stejný výsledek po L68: tři řádky Scenario Outline a dva samostatné scénáře.
3. `python custom_runner.py @smoke` spustí jen dva scénáře, zbytek je skipped.
4. Po `allure serve reports/allure-results` vidíš v reportu pět zelených testů.
5. Po záměrném pokažení jednoho řádku v Examples selže právě jeden scénář, v reportu má screenshot a ve složce `screenshots` je jeden soubor PNG.
6. Druhé spuštění runneru začne s prázdnou složkou `screenshots`.
7. `python run_tests.py` nepřepíše existující `features/contact_form.feature`.
8. `git status` neukazuje `.env`, `reports/` ani `screenshots/`.

Nic z tohoto modulu jsem nespouštěl. Kód kroků, hooků a runneru vychází z příloh kurzu a z dokumentace Playwrightu a Behave. Před prvním během počítej s drobnými opravami, hlavně kolem verzí balíčků.

## Časté chyby

**`ModuleNotFoundError: No module named 'utils'` nebo `'config'`.** Skript běží z jiné složky, nebo byl spuštěn jako soubor místo modulu. Spouštěj z kořene projektu: `python -m utils.analyze_steps`. Totéž platí pro Behave. Spuštění `python -m behave` z kořene přidá aktuální složku do cesty importů, a proto kroky a `environment.py` najdou `utils`. Samotný příkaz `behave` z jiné složky to zaručit nemusí.

**Behave nenajde `environment.py`.** Soubor musí ležet přímo ve složce `features`, ne v kořeni projektu ani v `features/steps`.

**`AmbiguousStep`.** Dva vzory kroků pasují na stejnou větu, například `I fill in "{field}"` a `I fill in "{field}" field with "{value}"`. Behave bere první shodu a ohlásí konflikt. Vzory piš tak, aby se nepřekrývaly.

**Krok je ve VS Code podtržený, ale test projde.** Rozšíření nemá správně nastavené cesty nebo potřebuje znovu načíst okno. Rozhodující je `--dry-run`.

**`TimeoutError` u kontroly hlášky.** Text na stránce se liší od očekávaného, typicky velikostí písmen nebo interpunkcí („All“ proti „all“, chybějící vykřičník). Hláška v Examples musí sedět znak po znaku. Zkopíruj ji ze stránky, ne z promptu.

**AI navrhla metodu, která neexistuje.** `AttributeError: 'Locator' object has no attribute 'value'`. Ověř metodu v dokumentaci Playwrightu (Locator API). Do promptu přidej větu, ať model používá jen existující metody a nejistotu přizná.

**Prázdný report v Allure.** Ve složce `reports/allure-results` nejsou soubory JSON, protože formátovač nebyl zapnutý nebo běh skončil chybou dřív, než začal. Zkontroluj volby `--format` a `--outfile` v runneru. Prázdnou stránku způsobí i otevření `index.html` dvojklikem.

**`allure` není rozpoznaný příkaz.** Složka `bin` z rozbaleného Allure chybí v `PATH`, nebo je potřeba otevřít nový terminál. Po změně `PATH` se starý terminál nedozví nic.

**Screenshot se neuloží.** Složka `screenshots` neexistuje, nebo název scénáře obsahuje znak, který Windows v názvu souboru nedovolí.

**Generátor přepsal ručně upravený feature soubor.** Kód zapisuje v režimu `"w"` místo `"x"`. Generované soubory nech v gitu, rozdíl pak vždy uvidíš v `git diff`.

## Cvičení

:::cviceni nazev="Rozšiř Examples o techniky návrhu testů"
Cíl: použít AI na test design a výsledek ověřit spuštěním. Požádej model o nové řádky tabulky Examples pro pole Email: třídy ekvivalence a hraniční případy (chybí @, chybí doména, dvě zavináče, mezera, velmi dlouhá adresa). Do promptu dej stávající tabulku jako vzor (few-shot).
Hotovo: tabulka má aspoň pět nových řádků, každý jsi spustil a u řádků, kde se skutečné chování stránky liší od návrhu modelu, jsi opravil očekávaný výsledek podle stránky a zapsal, kde se model mýlil.
:::

:::cviceni nazev="Druhý feature soubor pro Login Portal"
Cíl: ověřit, že framework je opravdu znovupoužitelný. Přidej do `config/prompts.py` prompt `login_form` (Bruno ho má v L43), vygeneruj `features/login.feature` a doplň kroky. Využij existující kroky, kde to jde.
Hotovo: `python -m behave --dry-run` hlásí 0 undefined, nové kroky jsou nejvýš tři, scénáře projdou a jsou označené tagem `@login`. Stránka zobrazuje výsledek přihlášení v dialogovém okně prohlížeče, takže budeš potřebovat `page.on("dialog", ...)`. Zjisti to z dokumentace Playwrightu, ne od modelu, a porovnej to s tím, co navrhne `analyze_steps`.
:::

:::cviceni nazev="Změř, kolik návrhů z AI bylo použitelných"
Cíl: mít vlastní data o kvalitě generovaného kódu. Smaž implementaci čtyř kroků (nech `print("TO DO!")`) a spusť svou variantu `analyze_steps` třikrát.
Hotovo: tabulka pro každý krok a běh se sloupci „funguje beze změny“, „funguje po drobné opravě“, „nefunguje“ a „typ chyby“ (selektor, neexistující metoda, chybějící aserce). Jedna věta závěru, která úprava promptu by pomohla nejvíc.
:::

## Souvislost se sylabem CT-GenAI

Celý modul je praktickou ukázkou oddílu 2.2.2 (návrh testů a implementace testování s GenAI). AI v něm převádí požadavky na scénáře v Gherkinu a scénáře na kód kroků. Sylabus výslovně uvádí generování BDD scénářů a testovacích skriptů jako příklad. Oddíl 2.2.3 (automatizované regresní testování s GenAI) odpovídá krokům 9 a 10. Model navrhuje kód pro existující framework, a proto potřebuje znát jeho konvence: kde vzniká prohlížeč, jak se jmenuje stránka v kontextu, jak vypadají aserce. Proměnná `environment_context` je přesně ta komponenta Context, kterou oddíl 2.1.1 popisuje v struktuře promptu. Vzorová tabulka Examples ve cvičení 1 je few-shot prompting z oddílu 2.1.2.

Revize návrhů v kroku 10 je kapitola 3 v praxi. Neexistující metoda `value()` a výjimka `Error.TimeoutError` jsou halucinace z oddílu 3.1.1. Selektory pro prvky `<button>`, které na stránce nejsou, jsou chyba v uvažování: model z běžného vzoru odvodil nesprávný závěr o konkrétní stránce. Spuštění testu a pohled do nástrojů pro vývojáře jsou techniky odhalení z oddílu 3.1.2. Doplnění pravidel do promptu (používej jen existující metody, Then musí mít aserci) jsou opatření z oddílu 3.1.3. Nastavení nízké teploty v L52 souvisí s nedeterministickým chováním z oddílu 3.1.4.

Cvičení 3 je jednoduché měření kvality výstupu podle oddílu 2.3.1 a následné ladění promptu podle oddílu 2.3.2. Upozornění na kód a selektory klienta v cloudových modelech odpovídá rizikům z oddílu 3.2.1.
