---
modul: 3
nazev: GitHub Copilot pro testera
podtitul: S Copilotem ve VS Code postavíš a rozšíříš malý testovací projekt v Pythonu s Playwrightem a pytestem, napíšeš vlastního agenta na návrh scénářů a vyzkoušíš cloudového agenta na GitHubu.
cas: 4–5 h
uroven: středně pokročilý
nastroje: VS Code, GitHub Copilot, Python 3, pytest, Playwright (pytest-playwright), Git, GitHub; volitelně PyCharm
kapitoly: 2, 3, 4, 5
zdroje: Shetty L14–L19, L44–L46 (přílohy create-scenarios.agent.md, eventhub-domain.md)
---

GitHub Copilot je AI asistent zabudovaný přímo do vývojového prostředí. Na rozdíl od chatu v prohlížeči vidí soubory projektu, umí je upravovat a spouštět příkazy v terminálu. Pro testera to znamená, že nemusí kopírovat kód tam a zpátky. Zároveň to znamená, že nástroj sahá na soubory a příkazy a jeho práci je potřeba kontrolovat stejně pečlivě jako práci kolegy.

Shetty v kurzu ukazuje Copilot na Playwrightu v TypeScriptu (L15, L16) a na Selenium frameworku v Javě v IntelliJ (L19). Tady je stejný postup přenesený do Pythonu: Playwright s pytestem a stránka Contact Us na webdriveruniversity.com.

## Co postavíš

Na konci modulu budeš mít vlastní repozitář `copilot-qa-lab`:

```text
copilot-qa-lab/
├── .github/
│   ├── copilot-instructions.md      pravidla projektu pro Copilot
│   └── agents/
│       └── create-scenarios.agent.md vlastní agent na návrh scénářů
├── docs/
│   ├── contact-us-domain.md          popis domény (vstup pro agenta)
│   └── test-scenarios.md             výstup agenta
├── pages/
│   ├── __init__.py
│   └── contact_page.py               Page Object pro Contact Us
├── tests/
│   └── test_contact.py               testy v pytestu
├── pytest.ini
└── requirements.txt
```

Část kódu napíše Copilot v režimu agent. Část vysvětlí v režimu ask. Strukturu dalších testů navrhne v režimu plan. Dokumentace scénářů vznikne vlastním agentem. Na konci necháš cloudového agenta na GitHubu připravit pull request.

## Předpoklady

**Účty a ceny.** Stav k 23. 10. 2026, ověřit na github.com/features/copilot:

| Co | Potřebuješ | Poznámka |
|---|---|---|
| Copilot ve VS Code (ask, agent, plan) | účet GitHub, tarif Copilot Free stačí | Free má měsíční limit požadavků. Shetty v L14 ukazuje procento spotřebovaných kreditů přímo v okně chatu. |
| Vlastní agenti (`.agent.md`) | totéž | soubor v repozitáři, funguje lokálně |
| Cloudový agent (Copilot coding agent) | placený tarif, ověřit | Shetty v L46 zmiňuje zkušební verzi Pro s platební kartou. Podmínky se mění, ověřit. |

Tabulka ukazuje, že kroky 1 až 8 zvládneš zdarma. Placený tarif potřebuješ jen na krok 9.

**Software.** VS Code v aktuální verzi. Shetty v L14 zdůrazňuje aktualizaci, protože rozhraní Copilotu se mění s každou verzí. Python 3.10 nebo novější, Git a účet na GitHubu.

**Kde to dělat.** Na soukromém počítači a v soukromém repozitáři. Pro práci platí jiná pravidla. Copilot v práci používej jen s licencí, kterou přidělila firma (Copilot Business nebo Enterprise), a s nastavením, které určilo IT. Firemní repozitáře neotvírej s Copilotem přihlášeným pod osobním účtem. Kód by pak odcházel mimo firemní smlouvu. Shetty to v L19 popisuje podobně: zjisti u DevOps nebo bezpečnostního týmu, jaké pluginy a modely jsou povolené.

:::pozor
Copilot v režimu agent může vytvářet a mazat soubory a spouštět příkazy v terminálu. Nech zapnuté výchozí schvalování akcí (Default Approvals), jak radí Shetty v L14. Každý příkaz si před schválením přečti. Do repozitáře nikdy nepatří hesla, tokeny ani soubor `.env`. Agent je přečte stejně snadno jako zbytek kódu.
:::

## Postup

### Krok 1: Zapni Copilot ve VS Code a poznej režimy

1. Otevři VS Code. Copilot Chat je ve VS Code zabudovaný, ikona je v horní liště nebo v postranním panelu. Rozšíření není nutné instalovat zvlášť (Shetty L14, ověřit u tvé verze).
2. Klikni na ikonu, zvol přihlášení a přihlas se účtem GitHub v prohlížeči.
3. V dolní části okna chatu najdeš tři přepínače. Výběr režimu, výběr modelu a nastavení schvalování.

Shetty v L14 až L16 popisuje režimy takto:

| Režim | Co dělá | Kdy ho použít |
|---|---|---|
| Ask | odpovídá textem, nic nemění | vysvětlení kódu, konfigurace, chybové hlášky |
| Agent | čte, vytváří, upravuje a maže soubory, spouští příkazy | psaní testů, opravy, refaktoring |
| Plan | prozkoumá projekt, položí doplňující otázky a navrhne postup | rozhodnutí o struktuře, než se začne psát kód |

Tabulka shrnuje hlavní pravidlo z kurzu. Když nechceš, aby AI sahala na kód, zůstaň v ask. V agent dostane nástroj oprávnění jednat.

Výběr modelu nech na **Auto**. Copilot podle složitosti úlohy zvolí model sám. Shetty v L15 ukazuje, že pro dotaz na konfiguraci zvolil kódovací model z řady GPT. Dražší modely spotřebují víc z měsíčního limitu.

:::nad-ramec
**PyCharm a IntelliJ.** Shetty to ukazuje v L17 a L19. V nastavení otevři **Plugins**, záložku **Marketplace**, vyhledej **GitHub Copilot**, nainstaluj a restartuj IDE. Vpravo se objeví panel **GitHub Copilot Chat** se stejnými režimy Ask, Agent a Plan. Přihlášení probíhá přes prohlížeč. V Eclipse (L18) se plugin instaluje přes Eclipse Marketplace a přihlašuje se kódem zařízení (device code). Postup v modulu funguje ve všech IDE stejně. Liší se jen umístění tlačítek a způsob přidání kontextu. V JetBrains IDE Shetty pro dotaz nad celým projektem používá `@project`, ve VS Code slouží k tomu `#codebase` (ověřit u tvé verze).
:::

### Krok 2: Připrav kostru projektu ručně

Kostru vytvoř sám. Je to pár příkazů a víš pak přesně, co v projektu je. V PowerShellu:

```text
mkdir copilot-qa-lab
cd copilot-qa-lab
git init
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest-playwright
python -m playwright install chromium
mkdir pages, tests, docs
New-Item pages\__init__.py
```

Vytvoř `pytest.ini`:

```text
[pytest]
testpaths = tests
pythonpath = .
markers =
    submit: test odesílá formulář na demo stránku
```

A `.gitignore` s řádky `.venv/`, `__pycache__/`, `.env`, `test-results/`.

Co má vyjít: příkaz `python -m pytest` doběhne s hlášením „no tests ran“. Prostředí je připravené.

Ověřeno s Playwright 1.61, pytest-playwright 0.10 a pytest 9 (10/2026). Pokud `pip` nainstaluje novější Playwright, příkaz `playwright install chromium` stáhne k němu odpovídající prohlížeč. Bez něj test skončí hláškou „Executable doesn't exist“.

### Krok 3: Ask – nech si vysvětlit, co nástroj dělá

Shetty v L15 otevře konfiguraci Playwrightu a ptá se na rozdíl mezi časovými limity. V Pythonu je ekvivalent fixture `page` z pluginu pytest-playwright. Otevři `pytest.ini`, přepni na **Ask** a přidej soubor do kontextu. Ve VS Code přes tlačítko **Add Context** nebo napsáním `#file:pytest.ini` do promptu.

```text
I use pytest with the pytest-playwright plugin. Explain:
1. Where does the "page" fixture come from and what is its scope?
2. Which command-line options control browser, headed mode and slow motion?
3. What does "pythonpath = ." in #file:pytest.ini do?
Answer briefly, with one example command per point.
```

```text
Používám pytest s pluginem pytest-playwright. Vysvětli:
1. Odkud se bere fixture "page" a jaký má scope?
2. Které volby příkazové řádky určují prohlížeč, zobrazení okna a zpomalení?
3. Co dělá "pythonpath = ." v #file:pytest.ini?
Odpovídej stručně, u každého bodu jeden příklad příkazu.
```

Co má vyjít: fixture `page` poskytuje plugin a má scope `function`, tedy nová stránka pro každý test. Volby `--browser`, `--headed` a `--slowmo`. `pythonpath = .` přidá kořen projektu do cesty importů, takže testy najdou balíček `pages`. Ověř aspoň jednu odpověď v dokumentaci pytest-playwright. Model u voleb pluginů někdy uvede volbu, která existuje jen v JavaScriptové verzi Playwrightu.

Kontext je důležitý. Shetty v L15 vysvětluje, že s přiloženým souborem Copilot hledá nejdřív v něm. Odpověď je přesnější a spotřebuje méně tokenů, než když prochází celý projekt.

### Krok 4: Agent – Page Object a první testy

Teď necháš Copilot napsat kód. Model stránku nevidí, stejně jako v modulu 1. Lokátory mu proto dodej sám. V prohlížeči otevři https://webdriveruniversity.com/Contact-Us/contactus.html, klikni pravým tlačítkem na formulář, zvol **Prozkoumat** a zkopíruj atributy `name` polí. Shetty v L19 kopíruje celé outer HTML. U veřejné demo stránky to nevadí. U firemní aplikace je lepší popsat jen to, co je potřeba.

Přepni na **Agent** a pošli:

```text
Create a Page Object for the Contact Us page in pages/contact_page.py and tests in tests/test_contact.py.

Facts:
- URL: https://webdriveruniversity.com/Contact-Us/contactus.html
- Fields: input[name='first_name'], input[name='last_name'], input[name='email'], textarea[name='message']
- Buttons: input[type='reset'] (RESET), input[type='submit'] (SUBMIT)
- Valid submission shows the text "Thank You for your Message!"
- Invalid email shows "Error: Invalid email address"; an empty field shows "Error: all fields are required"

Rules:
- Python, pytest-playwright sync API, use the built-in "page" fixture.
- Locators as attributes in __init__, methods open(), fill(), submit(), reset().
- Assertions with playwright.sync_api.expect, no time.sleep.
- Mark tests that click SUBMIT with @pytest.mark.submit.
- Use only fictitious data with the domain example.com.
- Do not run any command except: python -m pytest
```

Česky stačí přeložit úvod a pravidla. Fakta nech v původní podobě, jsou to selektory a texty ze stránky.

Co má vyjít: Copilot ukáže plán, vytvoří dva soubory a zobrazí změny jako diff. Zelené řádky jsou přidané, červené odebrané. Než klikneš **Keep**, projdi diff. Pokud agent navrhne spustit `pytest`, schval to. Jiné příkazy, třeba instalaci dalších balíčků, posuď zvlášť.

Pro srovnání tady je minimální verze, kterou jsem napsal ručně. Copilot nemusí vytvořit totéž. Má ale obsahovat stejné části.

```python
# pages/contact_page.py
from playwright.sync_api import Page, expect

URL = "https://webdriveruniversity.com/Contact-Us/contactus.html"


class ContactPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("input[name='first_name']")
        self.last_name = page.locator("input[name='last_name']")
        self.email = page.locator("input[name='email']")
        self.comments = page.locator("textarea[name='message']")
        self.reset_button = page.locator("input[type='reset']")
        self.submit_button = page.locator("input[type='submit']")

    def open(self) -> None:
        self.page.goto(URL)

    def fill(self, first: str, last: str, email: str, comments: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.email.fill(email)
        self.comments.fill(comments)

    def submit(self) -> None:
        self.submit_button.click()

    def reset(self) -> None:
        self.reset_button.click()

    def expect_message(self, text: str) -> None:
        expect(self.page.locator("body")).to_contain_text(text)
```

```python
# tests/test_contact.py
import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage


@pytest.fixture
def contact(page):
    cp = ContactPage(page)
    cp.open()
    return cp


def test_reset_clears_all_fields(contact):
    contact.fill("Jana", "Testova", "jana@example.com", "Ahoj")
    contact.reset()
    for field in (contact.first_name, contact.last_name, contact.email, contact.comments):
        expect(field).to_have_value("")


@pytest.mark.submit
def test_valid_submission_shows_thank_you(contact):
    contact.fill("Jana", "Testova", "jana@example.com", "Testovaci zprava")
    contact.submit()
    contact.expect_message("Thank You for your Message!")


@pytest.mark.submit
@pytest.mark.parametrize(
    "first,last,email,comments,message",
    [
        ("Jana", "Testova", "jana.example.com", "x", "Error: Invalid email address"),
        ("", "Testova", "jana@example.com", "x", "Error: all fields are required"),
    ],
)
def test_invalid_input_shows_error(contact, first, last, email, comments, message):
    contact.fill(first, last, email, comments)
    contact.submit()
    contact.expect_message(message)
```

Spusť testy:

```text
python -m pytest -v
python -m pytest -m "not submit" --headed --slowmo 500
```

Co má vyjít: čtyři testy. Druhý příkaz spustí jen test tlačítka RESET a ukáže okno prohlížeče, abys viděl, co test dělá. Test RESET je ověřený proti živé stránce (10/2026, spuštěný přes `--browser-channel msedge`). Testy s odesláním formuláře neověřeno. Texty hlášek jsou převzaté z kurzu a stránka je může zobrazovat jinak. Pokud test selže na textu, oprav očekávání podle toho, co stránka skutečně ukáže, ne podle toho, co tvrdí model.

Na čem v diffu od Copilotu záleží:

- **Vymyšlené lokátory.** Když model napíše `#first-name` místo `input[name='first_name']`, nedržel se zadání. Test pak selže na čekání na prvek.
- **`time.sleep` nebo `wait_for_timeout`.** Playwright čeká na prvky sám. Pevné čekání dělá testy pomalé a nestabilní.
- **Kontrola přes `page.content()` a `in`.** Funguje, ale při selhání neukáže rozumnou chybu. `expect(...).to_contain_text` čeká a hlásí rozdíl.
- **Skutečné e-maily** nebo jména v testovacích datech.

### Krok 5: Plan – kam s testy pro Login Portal

Shetty v L16 se v režimu plan ptá, jestli nový test patří do existujícího souboru, nebo do nového. Copilot prozkoumá projekt a doporučí jeden soubor na funkci nebo stránku. Zkus totéž s druhou stránkou. Přepni na **Plan**:

```text
I want to add tests for https://webdriveruniversity.com/Login-Portal/index.html
(fields #text and #password, button #login-button, result is shown in a JavaScript alert).
Look at the existing project structure and propose:
- which files to create or change,
- how to handle the JavaScript alert in pytest-playwright,
- how to keep the valid credentials out of the code.
Do not write code yet. Ask me if something is unclear.
```

```text
Chci přidat testy pro https://webdriveruniversity.com/Login-Portal/index.html
(pole #text a #password, tlačítko #login-button, výsledek se zobrazí v JavaScript alertu).
Prohlédni si strukturu projektu a navrhni:
- které soubory vytvořit nebo změnit,
- jak v pytest-playwright zpracovat JavaScript alert,
- jak nemít platné přihlašovací údaje v kódu.
Kód zatím nepiš. Když ti něco není jasné, zeptej se.
```

Co má vyjít: plán s novým souborem `pages/login_page.py` a `tests/test_login.py`, podle vzoru z kroku 4. Pro alert by měl navrhnout `page.on("dialog", ...)` nebo `page.expect_event("dialog")`. Pro údaje proměnné prostředí, třeba `WDU_USER` a `WDU_PASS`, čtené přes `os.environ` ve fixture. Pokud plán navrhne údaje rovnou do kódu nebo do `pytest.ini`, plán odmítni a napiš proč. I u demo stránky jde o návyk.

Pak přepni na **Agent** a nech plán provést. Ve VS Code k tomu bývá u plánu tlačítko pro předání agentovi (ověřit). Jinak napiš „Implement the plan above“.

### Krok 6: Další úlohy z praxe

Shetty v L19 ukazuje na Selenium frameworku v Javě řadu běžných úloh. Všechny fungují i v Pythonu. Každý prompt pošli v uvedeném režimu a výsledek zkontroluj:

| Úloha | Režim | Prompt |
|---|---|---|
| Nový Page Object podle stávajících | Agent | `Create pages/checkbox_page.py in the same style as #file:pages/contact_page.py for <URL>. Locators: ...` |
| Oprava chyb | Agent | `Fix the errors in #file:tests/test_login.py and explain each fix in one line.` |
| Najít použití metody | Ask | `#codebase Where is ContactPage.expect_message used?` |
| Docstringy a komentáře | Agent | `Add docstrings to public methods in #file:pages/contact_page.py. Do not change behaviour.` |
| Test jako ruční testovací případ | Ask | `Describe #file:tests/test_contact.py as manual test cases: ID, preconditions, steps, expected result.` |
| Kroky pro BDD | Agent | `Create pytest-bdd step definitions for #file:features/contact.feature using ContactPage.` |
| Úprava podle připomínky z review | Agent | `Reviewer comment: "<vlož komentář>". Change only the code the comment refers to.` |

Tabulka je tahák. Shetty v L19 opakuje jedno pravidlo: výsledek je tak dobrý, jak dobrý je kontext. Přidej správné soubory a popiš úlohu konkrétně. Převod testu na ruční testovací případ se hodí, když potřebuješ automatické testy evidovat v Jira nebo jiném nástroji pro správu testů.

U úpravy podle review dej pozor na rozsah změn. Agent rád „vylepší“ i kód, na který se připomínka nevztahovala. Pokyn „change only…“ to omezí, diff to potvrdí.

### Krok 7: Pravidla projektu pro Copilot

:::nad-ramec
Kurz tuto funkci nezmiňuje. Copilot čte soubor `.github/copilot-instructions.md` a jeho obsah přidá ke každému dotazu v repozitáři (ověřit v dokumentaci GitHubu). Je to obdoba systémového promptu z kapitoly 2. Pravidla, která jsi v kroku 4 psal do promptu, tak stačí napsat jednou.
:::

Vytvoř `.github/copilot-instructions.md`:

```text
# Project rules
- Python 3.10+, pytest, pytest-playwright (sync API).
- Page Objects live in pages/, tests in tests/. One Page Object per page.
- Locators are attributes set in __init__. Prefer name, id or role locators.
- Assertions only with playwright.sync_api.expect. Never use time.sleep or wait_for_timeout.
- Test data must be fictitious; emails use the domain example.com.
- Credentials come from environment variables, never from code or config files.
- Tests that submit a form are marked @pytest.mark.submit.
```

Co má vyjít: když v novém chatu napíšeš krátký prompt „Add a test that RESET works after a failed submit“, Copilot dodrží pravidla bez dalšího vysvětlování. Ověř to v diffu: žádný `sleep`, správný marker, data na `example.com`.

### Krok 8: Vlastní agent na návrh scénářů

Shetty v L45 vytváří vlastního agenta (custom agent). Je to soubor Markdown s hlavičkou, který popisuje roli, vstupy, postup a formát výstupu. Copilot ho pak nabízí ve výběru agentů vedle Ask, Agent a Plan. Shettyho agent `create-scenarios` čte popis domény EventHub (`eventhub-domain.md`) a vytváří scénáře podle šesti pohledů: happy path, obchodní pravidla, bezpečnost, negativní případy, hraniční případy a stavy UI. Výstup zapisuje do `docs/test-scenarios.md`.

Agent je jen tak dobrý jako popis domény. Nejdřív proto napiš `docs/contact-us-domain.md`. Stačí to, co víš ze stránky a z dokumentu s požadavky z modulu 1:

```text
# Contact Us – domain

## Fields
| Field | Selector | Rule |
|---|---|---|
| First Name | input[name='first_name'] | required |
| Last Name | input[name='last_name'] | required |
| Email Address | input[name='email'] | required, valid email format |
| Comments | textarea[name='message'] | required |

## Behaviour
- SUBMIT with all fields valid shows "Thank You for your Message!" (verify exact text on the page)
- Invalid email shows "Error: Invalid email address"
- Any empty field shows "Error: all fields are required"
- RESET clears all fields

## Unknown (do not assume)
- Maximum field lengths
- Which error wins when a field is empty AND the email is invalid
- Whether submitted data is stored anywhere
```

Oddíl „Unknown“ je důležitý. Říká agentovi, kde nemá hádat.

Pak ve VS Code v rozbalovacím seznamu agentů zvol **Configure Custom Agents** a **Create new custom agent**. Umístění zvol ve workspace, tedy `.github/agents/`. Soubor musí končit na `.agent.md`. Obsah:

```text
---
name: create-scenarios
description: Designs functional test scenarios for one feature from docs/*-domain.md files.
tools: ['read', 'edit', 'search']
---

# Functional test designer

You are a senior functional test designer. You think like a real user and like a malicious user.

## Before you start
Read the domain file for the feature the user names, e.g. docs/contact-us-domain.md.
If there is no domain file for that feature, stop and say so.

## Thinking lenses
Apply all six to the feature:
| Lens | Question |
|---|---|
| Happy path | What is the expected successful journey? |
| Business rules | Which documented rules must be validated? |
| Security | Can input be abused (injection, very long input, scripts)? |
| Negative | What happens with invalid input or wrong order of actions? |
| Edge cases | Which boundaries and limits apply? |
| UI state | What is shown before, during and after an action? |

## Output
Append to docs/test-scenarios.md using this template:

### TC-<NNN>: <title>
**Lens**: <one of the six>
**Priority**: <P0 | P1 | P2>
**Preconditions**: ...
**Steps**: numbered
**Expected result**: ...
**Source**: <section of the domain file, or "UNKNOWN – needs clarification">
**Suggested layer**: <Unit | API | UI end-to-end>

## Rules
- Every scenario must have a Source. Never invent behaviour that is not in the domain file.
- Items listed under "Unknown" become questions, not expected results.
- Do not modify any file other than docs/test-scenarios.md.
```

Proti Shettyho příloze `create-scenarios.agent.md` jsem udělal čtyři změny a stojí za to vědět proč:

1. **Omezené nástroje.** Shettyho soubor má řádek `tools` zakomentovaný, takže agent smí všechno, co je zapnuté, včetně spouštění příkazů a webu. Agent, který jen píše dokumentaci, potřebuje číst, hledat a upravovat soubory. Méně oprávnění znamená menší škodu, když se něco pokazí. Jde o řízení přístupu, které kapitola 3, oddíl 3.2.3 uvádí mezi opatřeními. V bezpečnosti se tomu obecně říká princip nejnižších oprávnění (least privilege). Názvy nástrojů ověř v dokumentaci, Shettyho šablona je uvádí v podobě `'read'`, `'edit'`, `'search'`.
2. **Žádné `$ARGUMENTS`.** Shettyho soubor vznikl převodem ze skillu pro Claude Code (sekce 6 kurzu) a proměnnou `$ARGUMENTS` si nese odtamtud. Copilot vstup bere ze zprávy uživatele (ověřit, jestli proměnnou podporuje). Formulace „the feature the user names“ funguje v obou případech.
3. **Pole Source.** Shettyho pravidlo „every scenario must trace back to a documented rule“ je v textu, ale ne v šabloně. Když je pole v šabloně, agent ho vyplní u každého scénáře a ty hned vidíš, co nemá oporu.
4. **Pozůstatky šablony.** V příloze zůstal řádek „Define what this custom agent does…“ z výchozí šablony a v poli `name` přípona souboru. Model takový text bere jako součást instrukcí. Patří smazat.

Spusť agenta. V chatu ho vyber v seznamu agentů a napiš:

```text
Contact Us form
```

Co má vyjít: soubor `docs/test-scenarios.md` s desítkou až dvěma desítkami scénářů ve stanovené šabloně. Shetty v L46 dostal pro rezervace v EventHubu 32 scénářů. Contact Us je menší, takže čekej méně. Zkontroluj:

- Má každý scénář vyplněný Source?
- Žádný očekávaný výsledek nepochází z oddílu „Unknown“? Ty položky mají být otázky.
- Bezpečnostní scénáře jsou rozumné pro formulář? Například velmi dlouhý text nebo `<script>` v komentáři, ne „penetrační test serveru“.
- Agent neupravil jiný soubor než `docs/test-scenarios.md`?

Vlastní agent je v podstatě uložený systémový prompt s pravidly a omezeným přístupem k nástrojům. Proto ho dávej do repozitáře. Celý tým pak pracuje se stejnými pravidly a jejich změny jsou vidět v historii Gitu.

### Krok 9: Cloudový agent na GitHubu

Shetty v L46 pushne repozitář na GitHub. Vlastní agenti z `.github/agents/` se pak objeví i v záložce **Agents** na github.com. Úlohu tam zadáš z prohlížeče. Agent ji zpracuje v cloudu ve vlastní větvi a nabídne pull request. Nepotřebuješ k tomu otevřený projekt ani VS Code.

Postup podle kurzu (rozhraní ověřit, mění se):

1. Vytvoř na GitHubu **soukromý** repozitář a pushni do něj projekt. Shetty to v L46 nechá udělat agenta v chatu. Bezpečnější je pushnout sám a vědět, co odchází. Před pushem zkontroluj `git status`, že v repozitáři není `.env` ani jiný soubor s údaji.
2. Na github.com otevři repozitář a záložku **Agents**. Bez placeného tarifu tě GitHub vyzve k upgradu.
3. Vyber agenta `create-scenarios` a zadej úlohu, třeba „Login Portal“. Agent nemá doménový soubor, takže by měl podle pravidel skončit s hlášením, že soubor chybí. To je dobrý test, že pravidla fungují.
4. Přidej `docs/login-portal-domain.md`, pushni a úlohu zopakuj.
5. Až agent skončí, otevři jeho větev a pull request. Projdi změny v záložce **Files changed** stejně jako u kolegy.

Co má vyjít: pull request se změnou jediného souboru `docs/test-scenarios.md`. Pokud agent změnil i jiné soubory, pravidla v `.agent.md` nefungují a je potřeba je zpřesnit.

Cloudový agent běží na infrastruktuře GitHubu a má přístup k celému repozitáři. Do repozitáře s cloudovým agentem proto nepatří nic, co by nesmělo opustit firmu. U firemních repozitářů o zapnutí rozhoduje správce organizace na GitHubu, ne jednotlivec.

## Ověření

- `python -m pytest -m "not submit"` projde. `python -m pytest -v` projde, nebo víš, proč který test selhal, a máš to zapsané.
- V `git log` vidíš, které změny udělal Copilot a které ty. Nauč se commitovat po každém kroku zvlášť, třeba se zprávou „Copilot agent: Page Object for Contact Us“.
- V kódu není žádný `time.sleep`, skutečný e-mail ani přihlašovací údaj. Rychlá kontrola: `git grep -n -i -E "sleep|password|@gmail"`.
- Test pro Login Portal čte údaje z proměnných prostředí. Bez nich se přeskočí (`pytest.skip`), ne selže s nesrozumitelnou chybou.
- `docs/test-scenarios.md` má u každého scénáře pole Source.
- Agent `create-scenarios` bez doménového souboru úlohu odmítne.

## Časté chyby

**Agent bez kontroly diffu.** Klikneš Keep a necháš v projektu změny, které jsi nečetl. Agent často upraví víc, než bylo potřeba.

**Schválení všech příkazů.** Nastavení, které schvaluje automaticky, ušetří kliknutí, ale agent pak spustí i instalaci balíčků nebo `git push`. Pro učení nech výchozí schvalování.

**Chybějící kontext.** Bez přiloženého souboru Copilot hádá strukturu projektu a píše kód „obecně“, ne podle tvého vzoru.

**Lokátory z hlavy modelu.** Model stránku nevidí. Lokátory dodej nebo je zkontroluj v prohlížeči.

**Údaje v kódu nebo v `pytest.ini`.** I u demo stránky. Pro testy patří do proměnných prostředí, v CI do úložiště tajemství (secrets).

**Prohlížeč neodpovídá verzi Playwrightu.** Po aktualizaci `playwright` spusť `python -m playwright install chromium`. Jinak test skončí na hlášce „Executable doesn't exist“.

**Copilot s osobním účtem ve firemním repozitáři.** Kód odchází mimo firemní smlouvu. Používej jen licenci a nastavení od firmy.

**Agent s příliš širokými oprávněními.** Vlastní agent na dokumentaci nepotřebuje terminál ani web. Omez `tools`.

## Cvičení

:::cviceni nazev="Login Portal s Copilotem"
Cíl: projít ask, plan a agent na nové stránce. Podle kroku 5 nech navrhnout a implementovat testy pro Login Portal. Údaje čti z proměnných `WDU_USER` a `WDU_PASS`. Přidej test platného přihlášení, neplatného hesla a prázdných polí. Alert zachyť přes událost `dialog`.
Hotovo: tři testy projdou s nastavenými proměnnými a bez nich se přeskočí. V kódu ani v historii Gitu nejsou údaje. Commit od Copilotu je oddělený od tvých oprav.
:::

:::cviceni nazev="Druhý vlastní agent: recenzent testů"
Cíl: napsat agenta, který jen čte a hodnotí. Vytvoř `.github/agents/review-tests.agent.md` s nástroji jen pro čtení a vyhledávání. Agent projde `tests/` a `pages/` podle pravidel z `.github/copilot-instructions.md` a vypíše nálezy do chatu: soubor, řádek, porušené pravidlo. Nic nemění.
Hotovo: agent najde aspoň jeden nález, který jsi do kódu schválně vložil (třeba `time.sleep(1)`), a nezmění žádný soubor.
:::

:::cviceni nazev="Agent nad vlastním projektem"
Cíl: použít vlastního agenta mimo demo. Napiš doménový soubor pro jednu funkci projektu Účtenky (například nahrání účtenky) a nech agenta `create-scenarios` navrhnout scénáře. Porovnej je s testy, které v projektu už máš v Playwrightu.
Hotovo: tabulka tří sloupců (scénář od agenta, existující test, poznámka). Aspoň dva scénáře, které v projektu chybějí a dávají smysl, a aspoň jeden, který je nesmyslný, s vysvětlením proč.
:::

## Souvislost se sylabem CT-GenAI

Copilot je testovací nástroj postavený na LLM v podobě, kterou popisuje **kapitola 1, oddíl 1.2.2**. Na rozdíl od chatbota z modulu 1 je zabudovaný v IDE a pracuje s kontextem projektu. Režimy ask a agent odpovídají rozdílu mezi asistentem a agentem z **kapitoly 4, oddílu 4.1.3**. Agent si úlohu sám rozdělí na kroky, používá nástroje (soubory, terminál) a člověk schvaluje jeho akce. To je člověk ve smyčce (human-in-the-loop) z téhož oddílu. Cloudový agent v kroku 9 je stejný princip s větší autonomií. Architekturu nástroje, tedy model, kontext a nástroje, popisuje **oddíl 4.1.1**.

Generování a údržba testovacích skriptů v krocích 4 a 6 je automatizované regresní testování s GenAI z **kapitoly 2, oddílu 2.2.3**. Převod testu na ruční testovací případ a návrh scénářů agentem v kroku 8 patří k návrhu testů z **oddílu 2.2.2**. Pravidla v `.github/copilot-instructions.md` a v souboru `.agent.md` jsou systémový prompt z **oddílu 2.1.3**. Šablona výstupu a pole Source jsou komponenty Constraints a Output format z **oddílu 2.1.1**.

Vymyšlené lokátory a hlášky jsou halucinace z **kapitoly 3, oddílu 3.1.1**. Omezení nástrojů agenta, údaje v proměnných prostředí a kontrola diffu jsou opatření z **oddílu 3.2.3**. Rizika agenta s širokými oprávněními (spuštění škodlivého kódu, únik dat) popisuje **oddíl 3.2.2**. Používání Copilotu s osobním účtem na firemním kódu je stínová AI z **kapitoly 5, oddílu 5.1.1**.
