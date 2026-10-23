---
modul: 5
nazev: Claude Code pro QA – skills a agenti nad EventHubem
podtitul: Nad kódem EventHubu postavíš řetězec skills, který vytvoří testovací scénáře, rozdělí je do vrstev pyramidy, napíše a spustí Playwright testy, zreviduje je a vydá report pokrytí.
cas: 6–8 h (rozděl do tří večerů)
uroven: pokročilý
nastroje: Claude Code, Playwright, Playwright MCP, Node.js, VS Code
kapitoly: 1, 2, 3, 4, 5
zdroje: Shetty L30–L43 (přílohy eventhub.zip, skills.zip, Claude-Code-Skills-System.pptx)
---

Agent z modulu [MCP a Playwright MCP](modul:mcp) uměl jednu věc: projít stránku a napsat test. Všechno ostatní mu musel tester říct v promptu. Jak vypadá doména, jaké jsou konvence projektu, kam uložit výsledek. Při další úloze znovu.

Shetty v sekci 6 ukazuje, jak tohle know-how uložit do souborů. **Claude Code** je agent, který běží v terminálu nad celým projektem. Čte kód, spouští příkazy a zapisuje soubory. Jeho **skills** jsou složky se souborem `SKILL.md`, ve kterých je popsané, co agent má vědět nebo jak má postupovat. Shetty jich nad demo aplikací EventHub napíše šest. Dvě uchovávají znalosti, čtyři řídí práci. Dohromady tvoří řetězec, ve kterém výstup jednoho kroku čte další krok.

```text
 eventhub-domain (znalosti)        playwright-best-practices (znalosti)
        |                                   |
        v                                   v
 /create-scenarios --> docs/test-scenarios.md
                              |
                              v
 /test-strategy  -----> docs/test-strategy.md
                              |
                              v
 /generate-tests ----> tests/*.spec.js  --(spustí, opraví)--> zelené testy
                              |
                              v
 /review-tests  -----> report v chatu  --> opravy zpět do /generate-tests
                              |
                              v
 cílený prompt (L43) -> report pokrytí: plánováno vs. implementováno
```

Modul vychází ze skutečných souborů z přílohy kurzu (`eventhub\.claude\skills\` a `skills.zip`, obsah je totožný). Ukážu jejich strukturu, vysvětlím, proč jsou napsané právě tak, upozorním na místa, kde si samy odporují, a ke každému typu napíšeš vlastní minimální variantu.

## Co postavíš

- Projekt EventHub s vlastním, zkráceným `CLAUDE.md` a se souborem `.claude/settings.json`, který říká, co agent smí bez ptaní a co nikdy.
- Šest skills z kurzu ve složce `.claude/skills/`, přečtené a pochopené, s opravenými rozpory.
- Vlastní znalostní skill s podsoubory a vlastní agentní skill `/coverage-report`.
- Dokumenty `docs/test-scenarios.md` a `docs/test-strategy.md` pro rezervace, které vytvoří agent a ty je zrevidíš.
- Tři Playwright testy, které agent napíše, spustí a opraví, a revizi těchto testů od dalšího skillu.
- Report pokrytí `docs/coverage-report.md`, který porovná plán se skutečně napsanými testy.

## Předpoklady

**Znalosti.** Modul předpokládá, že znáš Claude Code jako uživatel (prompt, schvalování akcí, `/clear`). Playwright a MCP z modulu 4. Testovací pyramidu a rozdíl mezi testem jednotky, integračním testem a end-to-end testem z CTFL.

**Software.** Stav k 23. 10. 2026, verze ověř:

| Nástroj | K čemu | Cena |
|---|---|---|
| Claude Code (CLI) | agent v terminálu | předplatné Claude Pro kolem 20 USD měsíčně (17 USD při ročním placení) nebo Max, případně platba za API. Shetty v L31 uvádí 10 USD, to už neplatí. |
| Git for Windows | na Windows ho Claude Code potřebuje (Git Bash) | zdarma |
| Node.js 20 LTS nebo novější | EventHub, Playwright, Playwright MCP | zdarma |
| `@playwright/test` 1.58.x | verze z `package.json` EventHubu | zdarma |
| Playwright MCP | ověření lokátorů v prohlížeči (modul 4) | zdarma |
| VS Code | čtení souborů, které agent vytvoří | zdarma |

**Aplikace.** EventHub z přílohy kurzu. Můžeš pracovat proti veřejné instanci `eventhub.rahulshettyacademy.com` (tak to dělá kurz) nebo proti lokální instanci. Lokální spuštění popisuje `README.md` v příloze: MySQL, `npm run setup`, `npm run db:push`, `npm run seed`, `npm run dev`. Spustíš ho sám. Na veřejné instanci si založ vlastní účet. Účty z kurzu (`rahulshetty1@gmail.com`) sdílí všichni studenti a test, který maže všechny rezervace, smaže i jejich data.

**Kde.** Na soukromém počítači, ve vlastní kopii projektu. Kód EventHubu je materiál placeného kurzu. Do veřejného repozitáře ho nedávej.

:::pozor
Claude Code čte soubory projektu a jejich obsah posílá do cloudu Anthropic. Spouští příkazy s tvými právy. Proto: žádný firemní ani klientský kód, žádná firemní data. Před prací si nastav oprávnění (krok 4). Co agent smí bez ptaní, patří do `.claude/settings.json` (sdílené, v gitu) nebo `.claude/settings.local.json` (osobní, mimo git). Do `deny` dej čtení souborů `.env`. Tokeny (GitHub, Jira, API klíče) patří do proměnných prostředí nebo do správce tajemství, nikdy do `CLAUDE.md`, do skills ani do povolených příkazů. Na firemním počítači Claude Code bez schválení nepoužívej. Schválený přístup řeší AI platform tým.
:::

## Postup

### Krok 1: Od jednoho agenta k řetězci (L30, L31)

Shetty začíná sekci kritikou vlastní ukázky z MCP. Jeden agent s pěti servery a dvaatřiceti nástroji funguje, ale špatně se udržuje. Instrukce pro databázi, prohlížeč a API se míchají. Změna pro jednu úlohu ovlivní ostatní. Ladí se těžko.

Řešení je stejné jako v návrhu kódu: rozdělit odpovědnosti. Každý specializovaný krok má svoji roli, svoje zdroje a svůj výstup. Shetty tomu říká **agentic AI** (agentní AI): víc specializovaných agentů, kteří spolupracují na cíli, který zadá člověk. Pojem odpovídá sylabu, kde agentní AI znamená systémy, které samostatně plánují a provádějí kroky k dosažení cíle.

V kurzu se „agentem“ myslí agentní skill, ne samostatný proces. Claude Code má i skutečné **subagents** (podagenty) s vlastním kontextovým oknem. Těm se věnuje krok 14. Řetězec v tomto modulu běží v jedné konverzaci a jednotlivé kroky si předávají práci přes soubory v `docs/`.

Shetty volí pro QA čtyři role: návrhář scénářů, testovací architekt, automatizační inženýr a recenzent. Každá role odpovídá jednomu kroku testovacího procesu z CTFL: návrh testů, plánování úrovní, implementace a revize.

### Krok 2: Instalace a první spuštění (L33, L34)

Instalace se mění častěji než zbytek modulu. Postupuj podle oficiální dokumentace (docs.claude.com, sekce Claude Code). V říjnu 2026 je na Windows doporučený nativní instalátor spuštěný z PowerShellu. Na macOS a Linuxu skript přes `curl`. Shetty v L33 radí nejdřív nainstalovat Git for Windows, protože Claude Code na Windows používá Git Bash. Ověření:

```powershell
claude --version
claude doctor
```

Druhý příkaz zkontroluje instalaci a vypíše problémy. Pak přejdi do kořene projektu a spusť `claude`. Agent pracuje nad složkou, ve které jsi ho spustil. Všechno, co v ní je, může číst. Konec sezení je `exit` nebo dvakrát Ctrl+C (L34).

Shetty ukazuje i alternativu: Claude Desktop, záložka *Code*, výběr složky projektu. Funkčně jde o totéž. V terminálu je ale vidět víc z toho, co agent dělá.

Kurz instaluje také rozšíření **Claude in Chrome**, přes které agent ovládá běžný prohlížeč. V L41 ho agent použije sám od sebe místo Playwright MCP. V tomto modulu ho nepoužíváme. Na firemních počítačích ho zakazuje firemní politika. Navíc pracuje v profilu prohlížeče s tvými přihlášeními a cookies. Pro ověřování lokátorů stačí Playwright MCP s izolovaným profilem.

### Krok 3: `/init` a `CLAUDE.md` (L33)

Každá práce v novém projektu začíná příkazem `/init`. Claude Code projde kód a vytvoří v kořeni soubor `CLAUDE.md`. V něm je přehled projektu, technologie, příkazy pro spuštění a testy a konvence kódu.

Podstatné je, jak se soubor používá. `CLAUDE.md` se načte **celý do každé konverzace**. Proto má být krátký. Shettyho slajd doporučuje kolem 50 řádků: přehled, konvence, odkazy. Podrobnosti patří do skills, které se načítají jen podle potřeby.

`CLAUDE.md` z přílohy EventHubu je dobrý příklad i odstrašující případ zároveň. Má rozumnou strukturu:

```text
# EventHub - Project Conventions for Claude Code
## Project Overview        2 věty o aplikaci
## Tech Stack              Next.js 14, Express, Prisma, MySQL, JWT, Playwright
## Project Structure       strom složek
## Architecture Pattern    Routes -> Controllers -> Services -> Repositories
## Commands to Run         npm run dev, seed, test, test:ui, jeden test
## Testing Conventions     umístění testů, priorita lokátorů, zákaz waitForTimeout
## Key Business Rules      7 pravidel jednou větou
## Custom Slash Commands   4 agenti
## Skill Documents         odkazy
## Code Style
```

Když ho ale porovnáš se skutečnou strukturou projektu, najdeš tři problémy:

1. Odkazuje na `.claude/commands/` a `.claude/docs/playwright-best-practices.md`. Takové složky v projektu nejsou. Skills jsou v `.claude/skills/`. Soubor vznikl dřív a s projektem se neaktualizoval. Agent pak hledá soubory, které neexistují.
2. Obsahuje testovací účet i s heslem. Soubor je v gitu a načítá se do každé konverzace.
3. Obchodní pravidla se opakují ve skillu `eventhub-domain`. Když se pravidlo změní, musíš ho opravit na dvou místech.

Udělej si vlastní verzi. Zkopíruj projekt do své pracovní složky, starý `CLAUDE.md` přejmenuj na `CLAUDE.kurz.md` a spusť `/init`. Pak výsledek uprav podle těchto zásad:

```markdown
# EventHub – konvence pro Claude Code

Demo aplikace pro rezervaci vstupenek (cvičná, z kurzu Shetty).
Frontend Next.js 14 (port 3000), backend Express + Prisma + MySQL (port 3001).

## Příkazy
- npm run dev – frontend i backend
- npm run seed – 10 statických akcí a testovací uživatelé
- npx playwright test tests/<soubor>.spec.js --reporter=line – jeden test

## Testy
- Playwright E2E v tests/<feature>.spec.js, jen Chromium.
- Adresa aplikace z proměnné BASE_URL, účet z EVENTHUB_USER a EVENTHUB_PASSWORD.
- Standardy: skill playwright-best-practices. Doména: skill eventhub-domain.

## Pravidla pro agenta
- Neměň kód v backend/ a frontend/ bez výslovného pokynu. Hledáš-li chybu aplikace, nahlas ji.
- Nikdy nečti .env soubory a nevypisuj tokeny ani hesla.
- Výstupy analýz ukládej do docs/.
```

Soubor má pod 25 řádků. Nic v něm není dvakrát a neobsahuje žádné tajemství.

### Krok 4: Co agent smí (oprávnění)

Než agentovi dáš první úkol, rozhodni, co smí. Claude Code se u každé akce, která něco mění nebo spouští, zeptá. Odpověď „ano, a už se neptej“ zapíše pravidlo do `.claude/settings.local.json`. Ten soubor je osobní a Claude Code ho při vytvoření nastaví jako ignorovaný gitem. Sdílená pravidla týmu patří do `.claude/settings.json`, který v gitu je.

Soubor `settings.local.json` z přílohy EventHubu je poučný. Ukazuje, co se v něm za pár týdnů práce nasbírá:

- Povolené `git push origin main`, `git commit:*`, `docker run:*`, `docker compose *` a `gh api *`. Agent tedy smí bez ptaní poslat kód do hlavní větve, spustit libovolný kontejner a volat libovolné GitHub API.
- Celý příkaz `curl` s e-mailem a heslem testovacího účtu.
- Celý **JWT token** v povoleném příkazu. Token je v čitelné podobě v souboru, který se dostal do zipu kurzu.
- Absolutní cesty z autorova počítače, které jinde nefungují.

Osobní soubor, který se dostal k tisícům studentů, je přesně ten typ úniku, kterému má rozdělení na `settings.json` a `settings.local.json` zabránit. Nestačí spoléhat na `.gitignore`. Soubor se dá zabalit do zipu, poslat e-mailem nebo zkopírovat.

Vlastní minimální `.claude/settings.json` pro tento modul:

```json
{
  "permissions": {
    "allow": [
      "Bash(npx playwright test *)",
      "Bash(npx playwright show-report)",
      "mcp__playwright__browser_navigate",
      "mcp__playwright__browser_snapshot"
    ],
    "ask": [
      "Bash(git commit *)",
      "Bash(git push *)",
      "mcp__playwright__browser_click",
      "mcp__playwright__browser_type"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./backend/.env)",
      "Read(./frontend/.env.local)",
      "Bash(rm -rf *)"
    ]
  }
}
```

Princip je jednoduchý. Bez ptaní jen čtení a spouštění testů. S dotazem všechno, co mění repozitář nebo stav aplikace. Nikdy čtení tajemství. Zápis vzorů se mezi verzemi Claude Code měnil (v souboru EventHubu najdeš `git add:*` i `gh api *`). Přesnou syntaxi ověř v dokumentaci, sekce *Permissions*. Aktuální pravidla vypíše v Claude Code příkaz `/permissions`.

:::praxe
Stejná logika platí pro Šmoulu. Agent, který běží bez dozoru (headless) a dostává úkoly přes Telegram, nemá nikoho, kdo by schválil akci. Jeho pravidla `allow` a `deny` jsou jediná brzda. Co by se nemělo stát ani jednou, patří do `deny`, ne do instrukce v promptu.
:::

### Krok 5: Knowledge skills a agent skills (L35, L38, L40)

Skill je složka v `.claude/skills/<název>/` se souborem `SKILL.md`. Soubor má na začátku **frontmatter** (hlavičku v YAML mezi dvěma řádky `---`) a pod ní text v Markdownu. Text je obyčejná instrukce v přirozeném jazyce. Žádná šablona tam není.

Shetty rozlišuje dva druhy skills. Pravidlo z jeho slajdu: když skill **něco ví**, je to knowledge skill. Když skill **něco dělá**, je to agent skill.

| | Knowledge skill (znalostní) | Agent skill (agentní) |
|---|---|---|
| Obsah | fakta, pravidla, API, lokátory, standardy | role, postup, formát výstupu, pravidla |
| Příklad z kurzu | `eventhub-domain`, `playwright-best-practices` | `create-scenarios`, `test-strategy`, `generate-tests`, `review-tests` |
| Frontmatter v kurzu | `user-invocable: false` | `disable-model-invocation: true` |
| Kdo ho spouští | Claude sám, když usoudí, že je relevantní | jen uživatel přes `/název` |
| Popis (`description`) | je v kontextu každé konverzace | v kontextu není, uživatel ho vidí v nabídce `/` |
| Analogie ze slajdu | příručka na polici | konzultant s vlastní metodikou |

Tabulka shrnuje, proč se oba druhy liší ve frontmatteru. Znalostní skill má být dostupný kdykoli, kdy ho úloha potřebuje. Proto ho model najde podle popisu. Agentní skill spouští akce, a ty má spouštět člověk. Proto ho model sám vyvolat nesmí.

Jak se skills načítají, popisuje dokumentace Claude Code takto (stav 10/2026, ověř):

- Bez obou přepínačů: skill může spustit uživatel i model. Popis je v kontextu.
- `disable-model-invocation: true`: skill spustí jen uživatel. Popis v kontextu není.
- `user-invocable: false`: skill nenajdeš v nabídce `/`, spouští ho jen model. Popis v kontextu je.
- Celý obsah `SKILL.md` se načte až ve chvíli, kdy se skill použije. Podsoubory se načtou, jen když na ně agent podle odkazu sáhne.

Pozor na rozpor v kurzu. Shetty v L40 říká, že skills s `user-invocable: false` se „načtou celé hned na začátku“. Jeho vlastní slajd (*The Description Field*) to říká správně: na začátku je v kontextu jen popis. Celý soubor se načte, až když ho model potřebuje. Pro návrh skills z toho plyne praktická věc. Popis znalostního skillu piš jako klíčová slova, podle kterých ho model najde. Popis agentního skillu piš jako popisek v menu, podle kterého ho najdeš ty.

Další pole frontmatteru, která se v kurzu objevují nebo se hodí:

- `name` je název skillu a zároveň příkaz `/name`.
- `description` je popis, viz výše. Bez dobrého popisu model znalostní skill nenajde.
- `argument-hint` je nápověda k argumentu v nabídce, například `[feature-name or blank for full suite]`.
- `$ARGUMENTS` v textu skillu se nahradí tím, co napíšeš za příkaz. `/create-scenarios booking management` dosadí `booking management`.
- `allowed-tools` povolí vybrané nástroje bez ptaní, dokud je skill aktivní. Používej opatrně (krok 13).

:::pojem term="skill (Claude Code)"
Složka `.claude/skills/<název>/` se souborem `SKILL.md`. Frontmatter určuje název, popis a kdo skill smí spustit. Text pod ním je instrukce nebo znalost v přirozeném jazyce. Claude Code načte celý obsah, až když se skill použije.
:::

### Krok 6: Znalostní skill `eventhub-domain` a chytré odkazy (L36, L37)

Struktura skillu z kurzu:

```text
.claude/skills/eventhub-domain/
├── SKILL.md            90 řádků: přehled, technologie, architektura, datové modely, rozcestník
├── business-rules.md   57 řádků: limity, sandbox, rezervační kód, refundace, cena
├── api-reference.md    39 řádků: endpointy, stavové kódy chyb
├── ui-selectors.md     48 řádků: lokátory po stránkách
└── user-flows.md       71 řádků: pět uživatelských toků, testovací data
```

Frontmatter hlavního souboru:

```yaml
---
name: eventhub-domain
description: EventHub application domain knowledge — business rules, API endpoints,
  data models, user flows, UI selectors, and error scenarios. Use when writing tests,
  reviewing code, creating scenarios, or answering questions about how EventHub works.
user-invocable: false
---
```

Popis obsahuje dvě části. Co skill obsahuje a kdy ho použít. Druhá část je pro model důležitější. Podle ní pozná, že úloha „napiš scénáře pro rezervace“ tento skill potřebuje.

Na konci `SKILL.md` je rozcestník:

```markdown
## Detailed Knowledge (Sub-Files)
Load these based on what the current task needs:
- **Business rules & validation logic** → read `./business-rules.md`
- **API endpoints & error codes** → read `./api-reference.md`
- **UI selectors for test automation** → read `./ui-selectors.md`
- **User flows, test scenarios & test data** → read `./user-flows.md`
```

Tomu Shetty v L37 říká chytré odkazy (smart references). Problém, který řeší, je **context bloat** (nafouknutí kontextu). Doménový dokument bankovní aplikace má snadno tisíce řádků. Kdyby byl v jednom souboru, agent by ho četl celý při každé úloze. Rychle by vyčerpal kontextové okno, platil by za zbytečné tokeny a s rostoucím kontextem by se zhoršovala kvalita odpovědí. S rozcestníkem si agent pro manuální scénáře přečte pravidla a toky. Lokátory a API vynechá. Automatizační agent si přečte lokátory. Slajd uvádí, který agent čte který podsoubor.

Stejný princip platí i pro agentní skills. Slajd *Keep Skills Lightweight* ukazuje agenta, který měl 71 řádků, protože obsahoval celý kontrolní seznam revize. Po úpravě má 30 řádků a jednu větu: „přečti skill best practices, ten je tvůj kontrolní seznam“. Pravidlo zní: co už je ve znalostním skillu, v agentovi neopakuj, jen na to odkaž.

#### Co v doménovém skillu nesedí

Když skill čteš jako tester, najdeš rozpory. Tohle je cenná dovednost, protože agent rozpor neohlásí. Vybere si jednu verzi a pokračuje.

| Pravidlo | `business-rules.md` | `user-flows.md` | kód |
|---|---|---|---|
| počet akcí na stránce | „max 9 events at a time“ | „12 events per page“ | frontend posílá `limit: 12`, backend má výchozí `10` |

Tabulka ukazuje tři různá čísla pro jedno pravidlo. ContextQA v sekci 11 se na totéž ptá a Shetty odpoví „devět“. Agent `create-scenarios` z něj udělá očekávaný výsledek podle toho, který soubor zrovna přečetl. Proto doménový skill revidují lidé, kteří doménu znají, stejně jako jakoukoli jinou testovací bázi.

Druhý nález je v konfiguraci. `backend/src/config/env.js` má záložní hodnotu `JWT_SECRET`, která se použije, když proměnná prostředí chybí. To není chyba skillu, ale dobrý podnět pro bezpečnostní scénář, který agent sám nenavrhl.

### Krok 7: Vlastní znalostní skill

Napiš si malý znalostní skill sám. Smyslem je projít celý cyklus: soubor, popis, ověření, že ho model najde. Téma: pravidla rezervací, zkrácená a v češtině.

Soubor `.claude/skills/eventhub-rezervace/SKILL.md`:

```markdown
---
name: eventhub-rezervace
description: Pravidla rezervací v EventHubu – limity, rezervační kód, refundace,
  izolace uživatelů. Použij při návrhu, psaní nebo revizi testů rezervací.
user-invocable: false
---

# Rezervace v EventHubu

- Jedna rezervace má 1 až 10 lístků. Cena = cena akce × počet lístků.
- Uživatel má nejvýš 9 rezervací. Desátá smaže nejstarší (FIFO).
- Rezervační kód má tvar <písmeno>-<6 znaků>. Písmeno je první písmeno názvu akce, velké.
- Zrušení rezervace vrátí místa akci.
- Cizí rezervace vrací 403 a text „Access Denied“.

Podrobnosti o refundaci: ./refundace.md
Rozpory s jinými soubory: ./otevrene-otazky.md – než z nich uděláš očekávaný výsledek, zeptej se.
```

Soubor `refundace.md` vedle něj:

```markdown
# Refundace
- 1 lístek: nárok na plnou refundaci.
- Víc lístků: bez nároku („Group bookings (N tickets) are non-refundable“).
- Výsledek se zobrazí po zhruba 4 s, mezitím běží spinner (#refund-spinner).
- Logika je jen ve frontendu, backend refundaci nemá.
```

A `otevrene-otazky.md` s rozporem z kroku 6. Poslední řádek `SKILL.md` je nejdůležitější část celého skillu. Agent dostane pravidlo, co dělat s nejistotou. Bez něj by rozpor potichu rozhodl sám.

Ověření: spusť nové sezení a napiš „kolik lístků může mít jedna rezervace a jak se pozná, ke které akci patří rezervační kód“. Agent by měl skill použít sám (v terminálu uvidíš, že ho načetl). Pak se zeptej na něco, co skill neobsahuje, třeba na formát telefonu. Agent by měl buď hledat v kódu, nebo říct, že to neví. Pokud si odpověď vymyslí, je to halucinace. Zapiš si ji.

### Krok 8: Agentní skill `create-scenarios` (L36, L38)

Agentní skill z kurzu má 50 řádků. Struktura je čitelná na první pohled:

```text
frontmatter     name, description, disable-model-invocation: true, argument-hint
role            "Senior Functional Test Designer – myslíš jako uživatel i jako útočník"
zdroje          1. skill eventhub-domain  2. jeho business-rules.md a user-flows.md
                3. frontend/app/  4. backend/src/services/
úloha           "Create test scenarios for: $ARGUMENTS", bez argumentu celá aplikace
myšlení         6 pohledů: Happy Path, Business Rules, Security, Negative/Error,
                Edge Cases, UI State
výstup          docs/test-scenarios.md, šablona TC s kategorií, prioritou P0–P3,
                předpoklady, kroky, očekávaným výsledkem, pravidlem a vrstvou
číslování       TC-001–099 Happy Path, 100–199 pravidla, 200–299 bezpečnost, ...
pravidla        každý scénář musí mít oporu v pravidle nebo v kódu
```

Shetty v L35 vysvětluje, proč skill vypadá takhle. Nový tester v týmu dostane od seniora tři věci: kde najde dokumentaci, jak má o testech přemýšlet a v jakém formátu je má odevzdat. Agent potřebuje totéž. Role nastaví úhel pohledu. Šest pohledů zabrání tomu, aby agent napsal jen šťastné cesty. Šablona a číslování dělají výstup strojově čitelný pro další krok.

Všimni si dvou detailů. Zdroje zahrnují kód frontendu a backendu, nejen dokumentaci. Agent tak může najít chování, které dokumentace nepopisuje. Pravidlo „každý scénář musí mít oporu“ je ochrana proti halucinaci. Scénář bez zdroje je vymyšlený.

Spuštění:

```text
/create-scenarios booking management
```

Shetty v L39 ukazuje, že skill jde spustit i větou („vytvoř scénáře pro správu rezervací“). U `disable-model-invocation: true` to ale podle dokumentace nefunguje. Model skill sám vyvolat nesmí a jeho popis nevidí. Agent pak úlohu udělá bez skillu, po svém. Spolehlivá cesta je lomítko a název. Ověř to sám: zadej úlohu větou a podívej se, jestli se v `docs/` objevil soubor v předepsané šabloně.

Během běhu uvidíš, že Claude Code spouští vestavěného podagenta **Explore**, který prochází kód. Běh trvá jednotky minut. Výsledek z kurzu je v příloze: `docs/test-scenarios.md`, 706 řádků, 53 scénářů pro správu rezervací. Shetty v L38 hlásí 45 scénářů. Stejný skill nad stejným kódem dal pokaždé jiný počet. To je nedeterministické chování, které popisuje sylabus. Počty z tvého běhu se budou lišit taky.

Revize scénářů je tvoje práce. Projdi aspoň tyto body:

1. Má každý scénář vyplněné pole *Business Rule*? Najdi pravidlo ve skillu nebo v kódu.
2. Jsou scénáře pro obě verze rozporu z kroku 6, nebo agent jednu vybral?
3. Opakují se scénáře pod jinými čísly?
4. Jsou bezpečnostní scénáře proveditelné (cizí rezervace, chybějící token), nebo jen obecné?
5. Odpovídají priority riziku? P0 by měl být tok, bez kterého aplikace nemá smysl.

:::praxe
Pro bankovní projekt je doménový skill testovací báze: pravidla platebního příkazu, limity, autorizace. Tam nesmí do cloudového modelu ani jeho kopie. Stejná struktura skillů jde ale použít s modelem, který klient schválil a provozuje ve svém prostředí. Know-how v souborech je přenositelné, model se dá vyměnit.
:::

### Krok 9: Agentní skill `test-strategy` (L39)

Druhý agent čte výstup prvního. Jeho role je testovací stratég, „napůl vývojář, napůl tester“. Shetty to zdůvodňuje tím, že bez znalosti kódu nejde rozhodnout, co je testovatelné testem jednotky.

Jádro skillu jsou rozhodovací pravidla:

```text
1. Čistá funkce bez vstupu a výstupu do okolí  -> Unit
2. Pravidlo v backendu nebo kontrakt API        -> API/Integration
3. Vykreslení jedné komponenty, stav UI         -> Component
4. Tok přes víc stránek, celý stack             -> E2E
5. Jde to otestovat na nižší vrstvě?            -> posuň dolů
6. Nevíš?                                       -> nejnižší vrstva, která stačí
```

K tomu seznam **anti-patterns** (protivzorů), které má hlásit. Validace vstupu testovaná přes E2E. Chybové kódy API testované přes prohlížeč. Žádný E2E test pro kritický tok. Všechno v E2E, tedy „kornout zmrzliny místo pyramidy“. A dvě pravidla pro výstup. Kritická pravidla se testují na víc vrstvách. Každé sporné zařazení musí mít zdůvodnění.

Spuštění:

```text
/test-strategy booking scenarios
```

Výsledek z kurzu (`docs/test-strategy.md`):

| Vrstva | Počet | Na co |
|---|---|---|
| Unit | 5 | `randomRef`, `generateUniqueRef`, výpočet ceny |
| API / integrace | 22 | kontrakt, autentizace, pravidla, stav databáze |
| Component | 14 | stavy UI, podmíněné zobrazení, refundace |
| E2E | 12 | kritické toky, víc stránek, bezpečnost mezi uživateli |

Tabulka ukazuje tvar pyramidy. Široký základ tvoří API testy, E2E je jen pětina. Dokument navíc obsahuje sekci *Decision Rationale*. Například refundace patří do komponentového testu, protože je to čistě frontendová logika se spinnerem. Bezpečnost mezi uživateli naopak zůstává i v E2E, protože jde o tok přes dvě přihlášení.

Na tomto výstupu se nejlépe ukazuje, kde agent pomáhá a kde rozhoduje člověk. Agent udělá první návrh za pár minut a odkáže na konkrétní funkce v kódu. Rozhodnutí, kdo které testy napíše, zůstává na týmu. Unit a komponentové testy patří vývojářům. Shetty v L39 doporučuje dokument s nimi projít. Tester si vezme API a E2E vrstvu.

Kontrolní otázky pro tvoji revizi: Odpovídají odkazy na soubory a funkce skutečnému kódu? Je E2E opravdu jen tam, kde nižší vrstva nestačí? Jsou všechna kritická pravidla (rezervační kód, izolace uživatelů) aspoň na dvou vrstvách?

### Krok 10: Znalostní skill `playwright-best-practices` (L40)

Než agent začne psát testy, potřebuje „zaškolení“ jako nový člen týmu. Shetty to v L40 přirovnává k předání znalostí (KT). Skill má 344 řádků a jedenáct oddílů:

```text
1  nastavení projektu (testDir, timeouty, Chromium, reportér, screenshoty)
2  priorita lokátorů: data-testid > role > label/placeholder > id > CSS, a co nikdy
3  filtrování a zúžení (filter hasText, has, scope na rodiče)
4  aserce (viditelnost, URL, obsah, čísla, vlastní timeout)
5  struktura testu (přihlášení -> akce -> aserce), page objects u větších sad
6  mockování API přes page.route
7  (číslo v souboru chybí)  testovací data a uživatelé
8  dynamická data (unikátní názvy)
9  čekání (auto-waiting, waitUntil; nikdy waitForTimeout)
10 ladění (console, jeden test, UI mód, report)
11 protivzory v tabulce
```

Je to znalostní skill (`user-invocable: false`). Čte ho `generate-tests`, který podle něj píše, i `review-tests`, který podle něj kontroluje. Jeden dokument tak slouží jako zadání i jako kritérium přijetí. To je dobrý vzor i pro lidský tým.

Při čtení najdeš rozpor, který stojí za zapsání. Skill v oddílu 1 uvádí základní adresu `http://localhost:3000`. `playwright.config.ts` má `https://eventhub.rahulshettyacademy.com`. Vygenerovaný test `tests/booking-management.spec.js` má adresu i přihlašovací údaje zapsané napevno jako konstanty v kódu. Skill v oddílu 11 přitom zakazuje „hardcoded“ data. Agent tedy pravidlo porušil a recenzent to v kurzu nezachytil. Testovací uživatelé i s heslem jsou navíc přímo v textu skillu. Pro veřejnou demo aplikaci to nevadí. Pro jakoukoli jinou je to vzor, který nechceš opakovat.

Oprav to ve své kopii. V oddílu 1 napiš, že adresa se bere z `process.env.BASE_URL`. Do oddílu s testovacími uživateli napiš jen názvy proměnných. Do `playwright.config.ts` dej `baseURL: process.env.BASE_URL ?? 'http://localhost:3000'`.

### Krok 11: Agentní skill `generate-tests`: napsat, spustit, opravit (L40, L41)

Tohle je nejcennější skill sekce. Shetty o něm v L40 říká, že je to „zlato“. Agent nekončí napsáním kódu. Pokračuje smyčkou:

```text
Krok 1  Napiš      přečti skills, existující testy a frontend, zapiš tests/<feature>.spec.js
Krok 2  Ověř       přes Playwright MCP otevři stránky a zkontroluj, že lokátory existují
Krok 3  Spusť      npx playwright test tests/<soubor>.spec.js --reporter=line
Krok 4  Rozhodni   když test padá, trojí kontrola:
                   - chybová hláška: timeout, prvek nenalezen, nesedí aserce?
                   - prohlížeč (MCP) a kód frontendu: změnil se lokátor? je prvek podmíněný?
                   - doménový skill: je očekávané chování skutečně požadavek?
                       doména chování potvrzuje      -> chyba testu, oprav test
                       kód odporuje doméně           -> možná chyba aplikace, nahlas ji,
                                                        test potichu nepřizpůsobuj
                   oprav a spusť znovu, dokud test neprojde
```

Skill končí větou, kterou Shetty v L41 vyzdvihuje: „Nekonči po napsání. Test je hotový, až když projde ve skutečném prohlížeči.“

Trojí kontrola je to, čím se skill liší od běžného **self-healing** (samoopravného) testu. Samooprava, která jen hledá nový lokátor, dokáže „opravit“ test tak, že projde přes chybu aplikace. Shetty to vysvětluje na příkladu: test čeká, že se okno nezobrazí, ale okno se zobrazí. Test nemá okno odkliknout, aby prošel. Má se podívat do domény. Když doména říká, že okno se zobrazit nemá, je to chyba aplikace. Test má selhat a agent ji má nahlásit.

Spuštění podle L41:

```text
/generate-tests booking flow – první 3 E2E testy z docs/test-strategy.md
```

Omezení na tři testy je rozumné. Celá sada E2E by běžela desítky minut a spotřebovala velkou část limitu předplatného. V kurzu trvá generování tří testů kolem 10 minut.

Co se v L41 stalo a na co si dát pozor:

- Skill říká „použij Playwright MCP“. Agent přesto použil Claude in Chrome, protože ho měl k dispozici. Agent si vybírá nástroj sám. Když chceš konkrétní nástroj, nedávej mu jiný. Pokud Playwright MCP nemáš připojený, agent ho podle L41 může zkusit doinstalovat a zeptá se na povolení. Neodsouhlasuj to automaticky.
- Výsledek byl šest testů v jednom souboru (`tests/booking-management.spec.js`, 221 řádků), všechny zelené. Zelené testy ale nic neříkají o jejich kvalitě. To ukáže až revize.
- Shetty nakonec nechal testy spustit v režimu s oknem prohlížeče (`--headed`), aby viděl, co dělají. To je dobrý zvyk. Podívej se aspoň jednou na každý nový test, než mu začneš věřit.

### Krok 12: Agentní skill `review-tests` (L41)

Čtvrtý agent je „přísný, ale konstruktivní“ recenzent. Kontrolním seznamem je skill best practices. Postup: přečíst standard, přečíst test a frontend, porovnat řádek po řádku, ověřit aserce proti doméně. Výstup pro každý soubor: co je dobře, nálezy označené `[CRITICAL]`, `[IMPORTANT]` a `[SUGGESTION]` s číslem řádku, kódem, opravou a porušeným pravidlem, skóre z deseti a seřazené opravy.

Dvě pravidla na konci skillu stojí za převzetí do jakéhokoli review promptu: „každý nález musí odkazovat na pravidlo“ a „nevymýšlej nálezy, když je test dobrý, řekni to“. První brání vágním připomínkám. Druhé brání tomu, aby model hledal chyby jen proto, že dostal roli recenzenta.

V kurzu dostaly testy skóre 7,5 z 10. Hlavní výtka byla kvalita lokátorů, například CSS selektor tam, kde existuje id. Shetty pak výstup recenze vložil zpět do `/generate-tests` s pokynem „oprav podle těchto nálezů“. Tak vzniká smyčka dvou agentů, kterou řídí člověk.

Skill nemá určené, kam výstup uložit. V kurzu skončil v chatu. Pro další práci je lepší soubor. Doplň do své kopie řádek „výstup zapiš do `docs/reviews/<soubor-testu>.md`“.

Zkus si také, co recenzent nenašel. Zadat mu můžeš přímo: „Porušuje test pravidlo o pevně zapsaných datech z oddílu 11?“ Recenzent by měl najít konstanty `BASE_URL`, `USER_EMAIL` a `USER_PASSWORD`. Proč je nenašel sám? Protože kontroluje řádky proti seznamu a tento protivzor v seznamu formulovaný je jen obecně („Hardcoded booking/event IDs“). Recenzent dělá to, co mu kontrolní seznam řekne.

### Krok 13: Cílená analýza pokrytí s reportem (L43)

V posledních lekcích Shetty spouští kroky ručně za sebou. V L43 ukazuje opak: zadá cíl a nechá agenta, ať si kroky naplánuje sám. Prompt zní zhruba takto (vlastní formulace):

```text
Analyzuj mezery v pokrytí testy.
1. Přečti docs/test-scenarios.md a docs/test-strategy.md, co je naplánováno.
2. Přečti všechny soubory v tests/, co je implementováno.
3. Spusť všechny Playwright testy a zjisti, které procházejí.
4. Vytvoř report: plánováno vs. implementováno po vrstvách, chybějící scénáře
   s prioritou, doporučení, co doplnit nejdřív.
```

Agent při tom sáhne po několika skills najednou a podagenti Explore čtou dokumenty souběžně. Výsledek v kurzu je očekávaný: E2E vrstva má 3 nebo 6 testů z dvanácti, ostatní vrstvy 0 %. Hodnota reportu není v tomto čísle. Je v tom, že každá mezera má číslo scénáře a prioritu, takže z reportu jde rovnou plánovat.

Během běhu se Shettymu objeví hláška o kompaktování konverzace a zbývajících 6 % kontextu. Celá sekce proběhla v jednom sezení a kontext se zaplnil. Shetty sezení ukončí, spustí nové a prompt zopakuje. Pro tebe z toho plynou dvě zásady. Velké úlohy začínej v čisté konverzaci (`/clear`). Zaplnění kontextu sleduj příkazem `/context`.

Opakovaný cílový prompt je kandidát na vlastní agentní skill. Napiš ho. Soubor `.claude/skills/coverage-report/SKILL.md`:

```markdown
---
name: coverage-report
description: Report pokrytí – porovná plánované scénáře a strategii s testy v tests/
disable-model-invocation: true
argument-hint: [oblast, např. booking; prázdné = vše]
---

# Analytik pokrytí

Jsi test analytik. Porovnáváš plán s realitou. Neopravuješ testy a nepíšeš nové.

## Vstupy
1. docs/test-scenarios.md – seznam scénářů (TC-xxx)
2. docs/test-strategy.md – přiřazení scénářů do vrstev
3. tests/*.spec.js – implementované E2E testy (TC číslo bývá v názvu testu)

## Úloha
Oblast: $ARGUMENTS
1. Sestav seznam plánovaných scénářů pro oblast, s vrstvou a prioritou.
2. Ke každému najdi implementovaný test. Shodu poznáš podle TC čísla v názvu
   nebo komentáři. Bez čísla shodu neodhaduj, zapiš „nejisté“.
3. Spusť E2E testy: npx playwright test --reporter=line
4. Zapiš docs/coverage-report.md:
   - tabulka po vrstvách: plánováno / implementováno / prochází
   - seznam chybějících P0 a P1 scénářů
   - testy, které neodpovídají žádnému scénáři
   - nejasnosti a rozpory, které jsi našel

## Pravidla
- Čísla počítej ze souborů, neodhaduj.
- Když test padá, zapiš to. Neopravuj ho.
- Na konci reportu uveď datum a že report vytvořil AI agent.
```

Tři věci jsou na skillu jinak než v kurzu. Skill má výslovně řečeno, co nedělá (neopravuje testy). Má pravidlo pro nejistou shodu, aby si ji nevymýšlel. A report nese informaci, že ho vytvořil agent. To je požadavek transparentnosti, který zná sylabus i interní pravidla firem.

Zkus ho spustit: `/coverage-report booking`. Pak report ověř ručně na třech náhodných řádcích.

Pole `allowed-tools` by šlo použít k tomu, aby skill spouštěl testy bez ptaní. Pro report to není potřeba. Jedno schválení příkazu je malá cena za to, že víš, co běží.

### Krok 14: Subagenti, rozsahy skills a co patří do gitu (L43)

**Subagents** (podagenti) jsou v Claude Code samostatná věc. Definují se v `.claude/agents/<název>.md`, mají vlastní systémový prompt, vlastní seznam nástrojů a hlavně vlastní kontextové okno. Hlavní konverzace jim předá úlohu a dostane zpět jen výsledek. Vestavěný Explore, kterého jsi viděl v krocích 8 a 9, je takový podagent. Skill lze spustit v podagentovi také přes pole `context: fork` ve frontmatteru (ověř v dokumentaci své verze). Přehled podagentů a jejich správu najdeš pod příkazem `/agents`.

Kdy co použít:

| Potřeba | Řešení |
|---|---|
| znalost, kterou model najde sám | znalostní skill |
| opakovaný postup spouštěný člověkem | agentní skill |
| úloha, která čte hodně souborů a vrací krátký výsledek | podagent (šetří hlavní kontext) |
| fakt, který musí znát každá konverzace | `CLAUDE.md`, krátce |

Tabulka nahrazuje Shettyho jednodušší dělení. Pro modul stačí skills. Podagent se vyplatí, když hlavní konverzace dochází kontext, typicky u analýzy pokrytí nad velkým projektem.

Skills mají tři rozsahy (slajd *Skill Scopes*):

- **Projekt**: `.claude/skills/` v repozitáři. Sdílí je tým přes git. Doménové skills a agenti projektu.
- **Osobní**: `~/.claude/skills/` (na Windows `C:\Users\<jméno>\.claude\skills\`). Platí ve všech tvých projektech, do gitu nejdou.
- **Podnik**: spravované nastavení, které nasazuje správce. Firemní standardy pro všechny.

Při shodě názvu má přednost podnik, pak osobní, pak projekt. Shetty v L43 doporučuje dobrý skill nabídnout jako firemní standard. Ve firmě to jde jen schválenou cestou přes správce nástroje.

Do gitu projektu patří `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/` a případně `.claude/agents/`. Nepatří tam `.claude/settings.local.json` a nic, co obsahuje tajemství.

### Krok 15: Kontrolní seznam pro vlastní skill a rozvržení práce

Shetty v L41 shrnuje sekci větou, že veškerá inteligence je v tom, jak napíšeš skills. Napsat je ale umí jen člověk, který danou práci umí sám. Strategii nenapíše někdo, kdo nezná testovací pyramidu. Standardy Playwrightu nenapíše někdo, kdo v něm nepsal. Skill je zapsaná odbornost, ne náhrada za ni.

Když píšeš nový skill nebo přebíráš cizí, projdi tyto otázky:

| Otázka | Znalostní skill | Agentní skill |
|---|---|---|
| Říká popis, kdy se má skill použít? | slovy ze zadání úloh | jako popisek v menu |
| Je správně frontmatter? | `user-invocable: false` | `disable-model-invocation: true` |
| Má hlavní soubor rozumnou délku? | do 100 řádků, zbytek v podsouborech | do 60 řádků, znalosti jen odkazem |
| Jsou zdroje konkrétní? | – | cesty k souborům a skillům, ne „projdi projekt“ |
| Je určený výstup? | – | soubor, šablona, číslování |
| Říká, co dělat s nejistotou? | odkaz na otevřené otázky | „zeptej se“ nebo „zapiš jako nejisté“ |
| Říká, co nedělat? | – | například „neměň kód aplikace“, „neopravuj, jen hlas“ |
| Obsahuje tajemství? | nikdy | nikdy |
| Sedí odkazy na soubory? | ověř po každém přesunu | ověř po každém přesunu |

Tabulka je stejná pro skills z kurzu i pro tvoje vlastní. Skills z kurzu ve většině bodů obstojí. Výjimky jsou výstup `review-tests` (není určený), pravidlo pro nejistotu (chybí všude) a hesla ve `playwright-best-practices`.

Rozvržení modulu do tří večerů:

1. **Večer 1** (kroky 1 až 7): instalace, `CLAUDE.md`, oprávnění, čtení skills, vlastní znalostní skill. Bez spouštění agentních skills. Výsledek: projekt připravený k práci a seznam rozporů v doméně.
2. **Večer 2** (kroky 8 až 10): scénáře a strategie pro rezervace, revize obou dokumentů, oprava `playwright-best-practices`. Každý agentní skill v nové konverzaci.
3. **Večer 3** (kroky 11 až 14): generování a revize testů, report pokrytí, cvičení.

Každý agentní běh spotřebuje znatelnou část limitu předplatného. Generování testů v kurzu běželo kolem deseti minut. Když limit dojde uprostřed běhu, zůstane rozpracovaný soubor. Proto po každém kroku commit ve své kopii projektu. Kdyby agent něco pokazil, vrátíš se o krok zpět.

## Ověření

- `claude doctor` nehlásí chyby. V projektu je tvůj `CLAUDE.md` pod 50 řádků bez hesel.
- `/permissions` ukazuje tvoje pravidla. Pokus přečíst `backend/.env` agent odmítne.
- V nabídce `/` vidíš `create-scenarios`, `test-strategy`, `generate-tests`, `review-tests` a `coverage-report`. Znalostní skills `eventhub-domain`, `playwright-best-practices` a `eventhub-rezervace` v nabídce nejsou.
- Na otázku o pravidlech rezervací agent sám načte `eventhub-rezervace`.
- `docs/test-scenarios.md` a `docs/test-strategy.md` existují a mají šablonu ze skillů. Máš poznámky z revize.
- Tři E2E testy projdou příkazem `npx playwright test`. V kódu nejsou adresa ani přihlašovací údaje.
- `docs/coverage-report.md` existuje. Tři řádky jsi ověřil ručně a sedí.

## Časté chyby

**`CLAUDE.md` jako odkladiště.** Soubor roste s každou úlohou a načítá se celý pokaždé. Podrobnosti patří do skills.

**Zastaralé odkazy.** `CLAUDE.md` nebo skill odkazuje na soubory, které už neexistují (v kurzu `.claude/commands/` a `.claude/docs/`). Agent je hledá a ztrácí čas. Po přesunu souborů projdi odkazy.

**Agentní skill spuštěný větou.** U `disable-model-invocation: true` ho model sám nevyvolá. Úlohu udělá bez skillu a výsledek nemá předepsaný formát. Používej `/název`.

**Znalostní skill, který model nenajde.** Obvykle kvůli obecnému popisu. Do `description` napiš, kdy se má skill použít, slovy, která se objeví v zadání.

**Duplicitní znalost.** Pravidlo ve skillu agenta i ve znalostním skillu. Po změně platí jen jedna verze. V agentovi jen odkaz.

**Rozpory v doménových souborech.** Agent je neohlásí a vybere si. Doménový skill je testovací báze a potřebuje revizi.

**Zelené testy = hotovo.** Test, který prošel, může testovat špatnou věc nebo porušovat standard. Revize a pohled na běh v prohlížeči jsou součást práce.

**Test „opravený“ přes chybu aplikace.** Bez trojí kontroly agent přizpůsobí test chování aplikace. Defekt pak zůstane skrytý.

**Plný kontext.** Dlouhé sezení přes celý řetězec skončí kompaktováním a zapomínáním. Každý velký krok v nové konverzaci, předávka přes soubory v `docs/`.

**Široká povolení.** „Povolit vždy“ u `git push` nebo `docker run` v osobním nastavení. Za pár týdnů nevíš, co všechno agent smí.

**Sdílený testovací účet.** Na veřejné instanci účty z kurzu sdílí všichni. Test „smaž všechny rezervace“ ovlivní cizí běhy a cizí běhy ovlivní tvoje testy.

## Cvičení

:::cviceni nazev="Skills pro vlastní projekt Účtenky"
Cíl: přenést strukturu na projekt, který znáš. Pro `uctenky` (Django + React + Playwright) napiš znalostní skill `uctenky-domena` s hlavním souborem do 60 řádků a dvěma podsoubory (pravidla a API). Pak upravenou kopii `create-scenarios` pro jednu oblast, například nahrání účtenky.
Hotovo: `/create-scenarios-uctenky nahrání` vytvoří soubor scénářů v šabloně. Aspoň 80 % scénářů má v poli pravidla odkaz, který v doménovém skillu nebo v kódu skutečně existuje. Máš zapsané, které scénáře byly vymyšlené a co jsi kvůli nim ve skillu upravil.
:::

:::cviceni nazev="Recenze a oprava jednoho testu"
Cíl: projít smyčku generování a revize. Spusť `/review-tests` na test z kroku 11. Doplň do skillu `review-tests` pravidlo o pevně zapsaných adresách a přihlašovacích údajích a spusť revizi znovu. Nálezy předej `/generate-tests` k opravě.
Hotovo: druhá revize najde pevně zapsané údaje. Po opravě je test zelený, čte adresu a účet z proměnných prostředí a skóre recenzenta je vyšší než na začátku. Rozdíl mezi první a druhou revizí máš zapsaný ve dvou větách.
:::

:::cviceni nazev="Report pokrytí a jeho kontrola"
Cíl: ověřit, jestli se reportu dá věřit. Spusť `/coverage-report booking` dvakrát v čistých konverzacích. Porovnej oba reporty.
Hotovo: tabulka, ve které jsou čísla z obou běhů vedle sebe a čísla, která jsi spočítal ručně. U každého rozdílu je vysvětlení (nejistá shoda, padající test, jiný výklad). Pokud se běhy liší, upravíš pravidla ve skillu tak, aby se rozdíl při třetím běhu zmenšil.
:::

## Souvislost se sylabem CT-GenAI

Celý modul ilustruje **kapitolu 4, oddíl 4.1.3** (agenti postavení na LLM v automatizaci testovacích procesů). Agent tu plánuje, volá nástroje (soubory, terminál, Playwright MCP), pozoruje výsledek a pokračuje. Řetězec čtyř agentních skills s předávkou přes soubory a cílový prompt z kroku 13 odpovídají víceagentnímu a autonomnímu použití z téhož oddílu. Schvalování příkazů a revize každého výstupu jsou **human-in-the-loop**. Znalostní skills s rozcestníkem jsou blízké principu RAG z **oddílu 4.1.2**: model dostane jen tu část znalostí, kterou úloha potřebuje. Architekturu nástroje (rozhraní, příprava kontextu, LLM) popisuje **oddíl 4.1.1**.

`CLAUDE.md` a text agentního skillu plní roli **systémového promptu** z **kapitoly 2, oddílu 2.1.3**. Role, pravidla a formát platí pro celou úlohu. Uživatelský prompt (`/create-scenarios booking`) jen upřesní cíl. Šest pohledů ve `create-scenarios` je strukturovaný prompt z **oddílu 2.1.1**. Scénáře, strategie a testy pokrývají **oddíl 2.2.2** (návrh a implementace testů) a **oddíl 2.2.3** (automatizované testování, samoopravné testy a jejich riziko). Report pokrytí z kroku 13 je analýza pokrytí z **oddílu 2.2.1** a podklad pro monitoring a řízení testování z **oddílu 2.2.4**. Opakovaný běh a porovnání v cvičení 3 jsou hodnocení výstupu z **oddílu 2.3**.

Rozpory v doménových souborech, vymyšlené scénáře a tvrzení agenta o vlastní práci jsou halucinace a chyby v uvažování z **kapitoly 3, oddílu 3.1.1**. Jiný počet scénářů při každém běhu je nedeterministické chování z **oddílu 3.1.4**. Oprávnění, zákaz čtení `.env` a únik tokenu v `settings.local.json` patří do **oddílů 3.2.1 a 3.2.3**.

Rozdíl mezi chatem a agentem, který pracuje nad celým projektem, je v **kapitole 1, oddílu 1.2.2**. Používání Claude Code na firemním kódu bez schválení je stínová AI z **kapitoly 5, oddílu 5.1.1**. Revize vygenerovaného testwaru a označení reportu jako výstupu AI odpovídají kvalitativním branám a povinnosti transparentnosti z **oddílu 5.1.2**.
