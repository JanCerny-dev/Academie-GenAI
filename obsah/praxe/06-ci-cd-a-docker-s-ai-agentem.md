---
modul: 6
nazev: CI/CD a Docker s AI agentem
podtitul: Necháš agenta napsat GitHub Actions workflow pro Playwright testy a Docker kontejner pro jejich lokální běh, a pak oba výsledky zreviduješ a opravíš to, co agent udělal špatně.
cas: 3–4 h
uroven: středně pokročilý
nastroje: GitHub Actions, Docker Desktop, Claude Code, GitHub CLI, Playwright
kapitoly: 2, 3, 4, 5
zdroje: Shetty L47–L50 (příloha eventhub: .github/workflows, Dockerfile, docker-compose.yml)
---

Testy z modulu [Claude Code pro QA](modul:claude-code) běží na tvém počítači. Aby měly cenu pro tým, musí běžet samy po každé změně kódu a musí jít spustit i u kolegy, který nemá Node.js ani Playwright. První řeší **CI/CD** (continuous integration and delivery, průběžná integrace a dodávání), druhé **Docker**.

Shetty v sekci 8 ukazuje, že obojí zvládne Claude Code z jednoho promptu. Agent vytvoří workflow pro GitHub Actions, nahraje kód do repozitáře a testy se rozběhnou v cloudu. Pak na přání „manažera“ zabalí testy do kontejneru, který se spouští jedním příkazem. Shetty to nazývá QAOps: postupy DevOps použité na testy.

Hlavní poselství sekce ale Shetty opakuje několikrát. Agent udělá provedení. Nápad a kontrola zůstávají na tobě. Když nevíš, co je Docker, nenapadne tě ho chtít. Když nerozumíš workflow, nepoznáš, že agent udělal chybu. Tento modul proto ke každému výstupu agenta přidává revizi. Výsledky z kurzu jsou v příloze EventHubu a mají několik vad, na kterých se dá revize procvičit.

## Co postavíš

- Soukromý repozitář na GitHubu s testy EventHubu bez jediného hesla v kódu.
- Workflow `.github/workflows/e2e.yml`, které při každém push spustí Playwright testy a nahraje HTML report. Nejdřív v podobě od agenta, pak opravené.
- Tajemství (secrets) v GitHubu pro testovací účet, nastavená bez vložení hodnoty do chatu.
- `Dockerfile` a `docker-compose.yml`, které spustí testy v kontejneru jedním příkazem, proti veřejné nebo lokální instanci.
- Variantu workflow, ve které testy v GitHub Actions běží uvnitř kontejneru Playwrightu.
- Kontrolní seznam pro revizi workflow, které napsal agent.

## Předpoklady

**Znalosti.** Git na úrovni commit, push, větev. Projekt EventHub s testy z modulu 5. Základní představa o YAML. Shetty v kurzu YAML ani Docker nevykládá a odkazuje na své jiné kurzy. Tady vysvětlím jen to, co potřebuješ k revizi.

**Účty a software.** Stav k 23. 10. 2026, ověř:

| Nástroj | K čemu | Cena |
|---|---|---|
| GitHub účet | repozitář, Actions | zdarma. Soukromé repozitáře mají měsíční limit minut Actions zdarma. |
| GitHub CLI (`gh`) | přihlášení a nastavení secrets bez ručního kopírování tokenu | zdarma |
| Docker Desktop | kontejnery lokálně | zdarma pro osobní použití a malé firmy. Větší firmy potřebují placenou licenci, podmínky ověř na docker.com. |
| Claude Code | agent, který soubory napíše | předplatné z modulu 5 |
| Node.js 20 LTS | lokální běh | zdarma |

**Proč soukromý repozitář.** Kód EventHubu je materiál placeného kurzu. Shetty ho v L47 nahrává do veřejného repozitáře, protože je jeho. Ty ho do veřejného repozitáře nedávej. Stačí ti soukromý repozitář na osobním účtu, třeba pod `jancerny-dev`.

:::pozor
Agent v tomto modulu dostane právo pushovat do repozitáře a spouštět kontejnery. Povol mu to jen na dotaz (`ask` v `.claude/settings.json`), ne trvale. Přihlášení ke GitHubu udělej sám příkazem `gh auth login`. Token pak uloží `gh` do správce přihlašovacích údajů systému a agent ho nemusí vidět. Token ani heslo nikdy nevkládej do chatu, do workflow ani do `Dockerfile`. Hodnoty patří do GitHub Secrets a lokálně do proměnných prostředí. Firemní kód do osobního GitHubu nepatří, ani na zkoušku. Firemní CI řeší firemní platforma a její správci.
:::

## Postup

### Krok 1: Co přesně má vzniknout (L47)

Shetty začíná zadáním od manažera. Kód je zatím jen lokálně. Má se dostat do vzdáleného repozitáře. Po každém push do hlavní větve se mají automaticky spustit všechny testy. Report má být ke stažení.

Kdo pushne změnu, ať vývojář nebo tester, hned uvidí, jestli něco rozbil. To je jádro průběžné integrace. Testy z modulu 5 se tak stávají regresní sadou, která běží bez lidí.

V GitHubu to dělá **GitHub Actions**. Workflow je soubor YAML ve složce `.github/workflows/`. Popisuje, kdy se má spustit (**trigger**), na jakém stroji (**runner**) a jaké kroky (**steps**) má provést. GitHub pro každý běh připraví čistý virtuální stroj s Ubuntu, provede kroky a stroj zahodí.

### Krok 2: Příprava repozitáře, než se cokoli pushne

Tohle Shetty přeskakuje a je to nejdůležitější krok modulu. Co jednou pushneš, zůstane v historii gitu, i když to později smažeš. Automatické skenery prohledávají GitHub nepřetržitě.

Než agentovi zadáš push, zkontroluj čtyři věci:

1. **`.gitignore`** obsahuje `.env`, `.env.local`, `node_modules/`, `playwright-report/`, `test-results/` a `.claude/settings.local.json`. EventHub z kurzu má všechno kromě posledního řádku. Doplň ho.
2. **Žádná hesla v kódu.** Test z kurzu má e-mail a heslo jako konstanty. Pokud jsi je v modulu 5 nepřesunul do proměnných prostředí, udělej to teď.
3. **Žádné tokeny v nastavení.** `settings.local.json` z přílohy obsahuje celý JWT token. Ve tvé kopii ho smaž.
4. **Hledání tajemství.** Spusť jednoduché hledání:

```bash
git grep -n -i -E "password|secret|token|apikey|Bearer " -- . ":!package-lock.json"
```

Každý nález posuď. Slovo `password` v názvu pole formuláře je v pořádku. Skutečné heslo nebo token není. Před prvním push je ještě čas. Po něm už ne.

### Krok 3: Prompt pro agenta (L48)

Shetty v L48 dává Claude Code jeden prompt se třemi úkoly: vytvoř workflow pro Playwright, spouštěj ho při push do main, nahraj HTML report jako artefakt, a pak všechno pushni do daného repozitáře. Agent pracuje pár minut, ptá se na povolení a při prvním push otevře prohlížeč kvůli přihlášení.

Vlastní varianta promptu. Je rozdělená na dva kroky, aby se workflow dalo zkontrolovat dřív, než odejde:

```text
Krok 1, zatím nic nepushuj.
Vytvoř GitHub Actions workflow .github/workflows/e2e.yml pro Playwright testy v tests/.
- Spouštět při push a pull requestu do main a ručně (workflow_dispatch).
- Node 20 LTS, npm ci, jen Chromium s potřebnými systémovými balíčky.
- Adresa aplikace z proměnné BASE_URL, testovací účet ze secrets
  EVENTHUB_USER a EVENTHUB_PASSWORD. Hodnoty nikam nevypisuj.
- Když test selže, musí selhat celý běh. HTML report nahraj jako artefakt vždy,
  i při selhání, a nech ho 14 dní.
- Omez běh na 20 minut.
Pak mi ukaž soubor a vysvětli každý krok jednou větou.
```

Po revizi (krok 5) přijde druhý prompt:

```text
Krok 2. Commitni workflow se zprávou "ci: Playwright E2E v GitHub Actions"
a pushni do origin main. Před push mi ukaž git status a seznam souborů v commitu.
```

Proč dva kroky. Agent v L48 rovnou pushnul. Kdyby workflow obsahovalo chybu nebo tajemství, bylo by už v historii. Rozdělení dává místo pro **quality gate** (kvalitativní bránu): člověk projde výstup, než pokračuje.

Pro push musí být repozitář propojený (`git remote add origin <url>`). Pokud ještě nejsi přihlášený, spusť sám v terminálu `gh auth login` a `gh auth setup-git`. Nenech to dělat agenta.

### Krok 4: Rozbor workflow z kurzu

V příloze je workflow, které agent v kurzu vytvořil, `playwright.yml`. Má 83 řádků, z toho polovina komentáře. Podstatné části:

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:

concurrency:
  group: playwright-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '21.7.1'

jobs:
  playwright:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npx playwright install chromium --with-deps
      - name: Run Playwright tests
        run: npx playwright test --reporter=html,line
        continue-on-error: true
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ github.run_id }}
          path: playwright-report/
          retention-days: 30
```

Co je dobře:

- `concurrency` s `cancel-in-progress` zruší starší běh, když přijde nový push. Šetří minuty.
- `npm ci` instaluje přesně podle `package-lock.json`. Na CI je to správná volba místo `npm install`.
- `--with-deps` doinstaluje systémové knihovny, které prohlížeč na Ubuntu potřebuje.
- `if: always()` u nahrání reportu zajistí, že report je k dispozici i po selhání.

Co je špatně:

1. **`continue-on-error: true` u testů.** Když test selže, krok se označí jako úspěšný a celý běh je zelený. Pipeline, která nikdy nezčervená, nic nehlídá. Shetty v L48 ukazuje zelený běh a říká „teď je všechno certifikované“. S tímto nastavením by byl zelený i s padajícími testy. Agent to zdůvodnil tím, že report se má nahrát vždy. To ale řeší `if: always()` u dalšího kroku samo.
2. **Komentář neodpovídá kódu.** V souboru stojí „`|| true` ensures the artifact upload step always runs“. V kódu žádné `|| true` není. Agent změnil kód a komentář nechal. Komentáře od agenta je potřeba číst stejně kriticky jako kód.
3. **Node 21.7.1.** Lichá verze Node.js není **LTS** (s dlouhodobou podporou) a podpora jí skončila. Pro CI vol sudou LTS verzi.
4. **Testy běží proti produkci.** `playwright.config.ts` míří na veřejnou instanci. Každý push tak vytváří a maže rezervace na živém webu. U demo aplikace to Shetty dovolí. U skutečné aplikace testy patří proti testovacímu prostředí.
5. **Přihlašovací údaje v kódu testu.** Workflow žádné secrets nepoužívá, protože test má účet napevno. Problém je tedy v testu, ne ve workflow.

Tyto nálezy jsou typické pro kód od agenta. Nejde o syntaktické chyby. Workflow funguje. Chyby jsou v tom, co workflow dělá, když se něco pokazí.

### Krok 5: Opravené minimální workflow

Takhle má vypadat výsledek promptu z kroku 3 po revizi. Je to vlastní minimální varianta, ne kopie z kurzu:

```yaml
name: E2E testy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

concurrency:
  group: e2e-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    env:
      BASE_URL: ${{ vars.BASE_URL }}
      EVENTHUB_USER: ${{ secrets.EVENTHUB_USER }}
      EVENTHUB_PASSWORD: ${{ secrets.EVENTHUB_PASSWORD }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npx playwright install chromium --with-deps
      - run: npx playwright test --reporter=html,line
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ github.run_id }}
          path: playwright-report/
          retention-days: 14
```

Rozdíly proti kurzu: testy, které selžou, shodí běh. Report se nahraje vždy. Adresa je v proměnné repozitáře (`vars`), účet v tajemstvích (`secrets`). `permissions: contents: read` omezí, co smí token běhu v repozitáři dělat. Workflow nepotřebuje nic zapisovat, tak nic zapisovat nesmí.

Verze akcí (`checkout@v4`, `setup-node@v4`, `upload-artifact@v4`) odpovídají kurzu. Mezitím mohly vyjít novější, ověř je na GitHub Marketplace. Workflow jsem nespustil, je neověřené.

### Krok 6: Secrets bez kopírování do chatu

Hodnoty se do GitHubu dostanou dvěma způsoby. V prohlížeči: repozitář → *Settings → Secrets and variables → Actions*. Nebo přes `gh` v terminálu:

```bash
gh secret set EVENTHUB_USER
gh secret set EVENTHUB_PASSWORD
gh variable set BASE_URL --body "https://eventhub.rahulshettyacademy.com"
```

Bez parametru `--body` se `gh secret set` na hodnotu zeptá a nezapíše ji do historie příkazů. Tyto příkazy spusť sám, ne přes agenta. Agent by hodnotu musel vidět.

Jak se secrets chovají za běhu. GitHub je v logu nahradí hvězdičkami. Spuštění z pull requestu z cizího forku je nedostane. To je ochrana proti tomu, aby si cizí člověk upravil workflow a tajemství vypsal. Maskování v logu ale není absolutní. Hodnotu zakódovanou do jiného tvaru (třeba base64) GitHub nepozná. Proto workflow nikdy nemá tajemství vypisovat.

### Krok 7: Workflow, které nekopíruj (ci.yml a deploy.yml)

V příloze jsou ještě dvě workflow. Nejsou z kurzu, patří k produkčnímu provozu EventHubu. Stojí za přečtení, protože ukazují, kam se CI rozroste, a co agentovi nikdy nedávat bez revize.

`ci.yml` běží u každého pull requestu. Kontroluje syntaxi backendu, schéma Prisma a build frontendu. Úloha *schema-drift* se navíc přes SSH přihlásí na **produkční server**, nahraje tam schéma z pull requestu a porovná ho s produkční databází. K tomu potřebuje soukromý SSH klíč v secrets.

`deploy.yml` po každém push do main nasadí aplikaci na produkci. Zapíše `.env` na server, udělá `git reset --hard`, sestaví frontend a restartuje procesy.

Dobré vzory, které si vezmi:

- Tajemství se předává přes proměnnou prostředí kroku a `printf`, ne vložením do příkazu. Nezobrazí se tak v seznamu procesů.
- Nasazení má `cancel-in-progress: false`. Přerušené nasazení by nechalo server v rozbitém stavu.
- Úloha nasazení má `environment: production`. V GitHubu jde k prostředí nastavit povinné schválení člověkem.
- Migrace databáze se schválně nespouštějí automaticky.

A poučení. Workflow s SSH klíčem k produkci je nejcitlivější soubor v repozitáři. Kdo ho změní, dostane se na server. Pokud agentovi zadáš „nastav CI/CD“ v repozitáři, kde takové workflow je, může ho upravit. Změny v `.github/workflows/` vždy čti řádek po řádku. V týmu je chraň pravidlem, že je musí schválit konkrétní člověk (CODEOWNERS).

### Krok 8: Docker pro lokální běh (L49)

Shetty v L49 přehrává rozhovor s manažerem. Manažer chce testy spustit u sebe, ale nechce instalovat Node.js, npm, Playwright a prohlížeče. Chce jeden příkaz. Odpověď je **container** (kontejner): balík se vším potřebným, který běží na tvém počítači, ale nic do něj neinstaluje. Kontejner vzniká z **image** (obrazu), který popisuje `Dockerfile`.

Shetty zadá agentovi jednoduchý cíl: kontejnerizuj projekt tak, aby kdokoli po naklonování spustil testy jedním příkazem. Agent vytvoří tři soubory a sám ověří, že kontejner funguje.

`Dockerfile` z přílohy:

```dockerfile
FROM mcr.microsoft.com/playwright:v1.58.2-noble
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY playwright.config.ts ./
COPY tests/ ./tests/
CMD ["npx", "playwright", "test", "--reporter=line"]
```

Rozbor po řádcích:

- `FROM` vychází z oficiálního obrazu Playwrightu od Microsoftu. Obsahuje Node.js, prohlížeče a systémové knihovny. Proto není potřeba `playwright install`.
- Verze obrazu `v1.58.2` musí odpovídat verzi `@playwright/test` v `package-lock.json`. Když se rozejdou, testy spadnou s hláškou, že spustitelný soubor prohlížeče neexistuje. `package.json` má `^1.58.2`, takže při aktualizaci zámku může přijít novější verze. Při každé aktualizaci Playwrightu změň i řádek `FROM`.
- Nejdřív se kopírují jen `package.json` a zámek, pak `npm ci`, a teprve potom testy. Docker si mezivýsledky pamatuje. Když změníš jen test, instalace závislostí se nepouští znovu.
- `--ignore-scripts` zakáže instalační skripty balíčků. Je to jednoduchá ochrana proti škodlivému kódu v závislostech.
- Do obrazu se kopírují jen testy a konfigurace. `.dockerignore` vylučuje `frontend/`, `backend/`, `docs/`, `.claude/` a reporty. Obraz je malý a neobsahuje nic navíc.

`docker-compose.yml` přidává jen připojení složek s reporty, aby zůstaly po skončení kontejneru na disku:

```yaml
services:
  tests:
    build: .
    volumes:
      - ./playwright-report:/app/playwright-report
      - ./test-results:/app/test-results
```

Spuštění, Docker Desktop musí běžet:

```bash
docker compose run --rm tests
```

`--rm` kontejner po doběhnutí smaže. Shetty v L49 hlásí šest testů za 18 sekund. Report najdeš v `playwright-report/index.html` na svém disku.

### Krok 9: Kontejner proti lokální aplikaci

Testy z kurzu míří na veřejnou instanci. Když chceš testovat lokální EventHub, narazíš na zradu. `localhost` uvnitř kontejneru znamená kontejner, ne tvůj počítač. Aplikace na portu 3000 tam není.

Docker Desktop na Windows a macOS nabízí adresu `host.docker.internal`, která vede na hostitelský počítač. Na Linuxu je potřeba ji přidat. Úprava `docker-compose.yml`:

```yaml
services:
  tests:
    build: .
    environment:
      - BASE_URL=${BASE_URL:-http://host.docker.internal:3000}
      - EVENTHUB_USER
      - EVENTHUB_PASSWORD
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./playwright-report:/app/playwright-report
      - ./test-results:/app/test-results
```

Řádky `EVENTHUB_USER` a `EVENTHUB_PASSWORD` bez hodnoty převezmou hodnotu z prostředí, ve kterém `docker compose` spouštíš. Do souboru se tak heslo nezapíše. `BASE_URL` má výchozí hodnotu, kterou můžeš přepsat. Konfigurace Playwrightu musí adresu číst z `process.env.BASE_URL` (úprava z modulu 5).

Ještě jedna past. Frontend EventHubu volá backend na adrese z `NEXT_PUBLIC_API_URL`, výchozí `http://localhost:3001/api`. Tuto adresu volá prohlížeč uvnitř kontejneru, takže `localhost` opět ukazuje do kontejneru. Možnosti: nastavit frontend na `http://host.docker.internal:3001/api`, nebo spustit aplikaci i testy v jednom compose se společnou sítí. To druhé je cvičení 3. Celý krok 9 je neověřený.

### Krok 10: Docker v GitHub Actions (L50)

Článek L50 pokračuje rozhovorem. Runner v GitHubu má nějakou verzi Node.js. Testy potřebují jinou. Lokálně fungují, na CI ne. Řešení: spouštět testy na CI ve stejném kontejneru jako lokálně. Prostředí je pak jedno pro všechny.

Shetty dává prompt, ve kterém agent obraz sestaví a testy v něm spustí. Jednodušší je říct GitHubu, ať celou úlohu spustí v hotovém obraze Playwrightu. Úprava workflow z kroku 5:

```yaml
jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    container:
      image: mcr.microsoft.com/playwright:v1.58.2-noble
    env:
      BASE_URL: ${{ vars.BASE_URL }}
      EVENTHUB_USER: ${{ secrets.EVENTHUB_USER }}
      EVENTHUB_PASSWORD: ${{ secrets.EVENTHUB_PASSWORD }}
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright test --reporter=html,line
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ github.run_id }}
          path: playwright-report/
          retention-days: 14
```

Odpadly kroky `setup-node` a `playwright install`. Obojí je v obraze. Verze obrazu je na jednom místě vedle verze v `Dockerfile`, obě musíš měnit spolu. Dokumentace Playwrightu (sekce *Continuous Integration*) uvádí tuto variantu jako doporučenou. Ověř aktuální podobu, zvlášť pokud bys testoval i ve Firefoxu, který v kontejneru potřebuje úpravu proměnné `HOME`. Neověřeno.

### Krok 11: Kontrolní seznam pro workflow od agenta

Shetty v L49 říká: „AI nenahrazuje tvůj úsudek.“ Úsudek se dá zapsat do seznamu otázek. Projdi ho u každého workflow, které agent napíše nebo změní:

| Otázka | Na co se díváš |
|---|---|
| Selže běh, když selže test? | žádné `continue-on-error` ani `\|\| true` u testů |
| Je report k dispozici i po selhání? | `if: always()` u nahrání |
| Odkud se berou tajemství? | jen `secrets.*`, nic napevno, nic se nevypisuje |
| Co smí token běhu? | `permissions` co nejužší |
| Proti čemu testy běží? | testovací prostředí, ne produkce |
| Kdy se workflow spouští? | trigger odpovídá zadání, žádný `pull_request_target` bez důvodu |
| Jsou verze pevné? | Node LTS, obraz Playwrightu, akce s verzí |
| Sedí komentáře s kódem? | agent mění kód a komentáře nechává |
| Jak dlouho smí běžet? | `timeout-minutes` |

Tabulka je kvalitativní brána pro jeden typ výstupu. Stejný přístup platí pro jakýkoli testware od AI.

## Ověření

- `git grep` z kroku 2 nenajde v repozitáři žádné heslo ani token.
- Na GitHubu v záložce *Actions* proběhl běh `E2E testy` po push. V *Summary* je ke stažení artefakt s reportem.
- Když v testu schválně změníš očekávaný text, běh zčervená. Report je i tak ke stažení. Pak změnu vrať.
- V logu běhu nejsou vidět hodnoty `EVENTHUB_USER` a `EVENTHUB_PASSWORD`.
- `docker compose run --rm tests` doběhne a v `playwright-report/` je nový report.
- Po smazání kontejneru nezůstal v počítači nainstalovaný Playwright ani prohlížeče (kontrola: `npx playwright --version` mimo projekt hlásí, že balíček chybí, nebo jinou verzi).

## Časté chyby

**Zelená pipeline s padajícími testy.** `continue-on-error: true` nebo `|| true` u kroku s testy. Workflow tím ztratí smysl.

**Push dřív než revize.** Agent pushne workflow i s chybou nebo tajemstvím. Rozděl úlohu na „napiš“ a „pushni“.

**Heslo v historii gitu.** Smazání souboru heslo z historie neodstraní. Jediné spolehlivé řešení je heslo změnit. Proto kontrola v kroku 2 před prvním push.

**Nesoulad verzí Playwrightu.** Obraz `v1.58.2` a knihovna `1.59` v zámku. Chyba o chybějícím prohlížeči. Měň obě verze spolu.

**`localhost` v kontejneru.** Testy v kontejneru nevidí aplikaci na hostiteli. Použij `host.docker.internal`, nebo spusť aplikaci ve stejné síti compose.

**Docker Desktop neběží.** `docker compose` skončí chybou o připojení k démonovi. Spusť Docker Desktop a počkej, až hlásí, že běží.

**Testy proti produkci z CI.** Každý push mění data na živém webu. U skutečné aplikace testovací prostředí.

**Agent upraví citlivé workflow.** Zadání „nastav CI“ může skončit změnou nasazovacího workflow. Změny v `.github/workflows/` čti vždy celé.

**Lichá verze Node.js.** Verze bez dlouhodobé podpory přestanou dostávat opravy. Na CI používej LTS.

## Cvičení

:::cviceni nazev="Červená pipeline schválně"
Cíl: ověřit, že CI opravdu hlídá. Nahraj nejdřív workflow z kurzu s `continue-on-error: true`, rozbij jeden test a pushni. Pak workflow nahraď opravenou verzí z kroku 5 a pushni znovu se stejným rozbitým testem.
Hotovo: máš dva běhy, první zelený a druhý červený, oba s reportem, ve kterém je stejný padající test. Dvě věty o tom, co by se stalo na projektu, kdyby první varianta běžela půl roku.
:::

:::cviceni nazev="Kontejner proti lokálnímu EventHubu"
Cíl: spustit testy v Dockeru proti aplikaci na vlastním počítači. Spusť EventHub lokálně, uprav `docker-compose.yml` podle kroku 9 a vyřeš adresu backendu pro prohlížeč v kontejneru.
Hotovo: `docker compose run --rm tests` projde proti `host.docker.internal`. V žádném souboru v repozitáři není heslo. Máš zapsané, jak jsi vyřešil adresu backendu a proč.
:::

:::cviceni nazev="Celá aplikace v GitHub Actions"
Cíl: testy na CI bez závislosti na veřejné instanci. Nech agenta navrhnout workflow, které v Actions spustí MySQL jako službu (`services: mysql`), backend a frontend EventHubu a teprve proti nim testy. Workflow zreviduješ podle tabulky z kroku 11.
Hotovo: běh v Actions je zelený a nezávisí na `eventhub.rahulshettyacademy.com`. Heslo databáze pro CI je v secrets, ne v YAML. Vyplněná tabulka z kroku 11 s aspoň jedním nálezem, který jsi u agenta opravil.
:::

## Souvislost se sylabem CT-GenAI

Modul ukazuje agenta z **kapitoly 4, oddílu 4.1.3**, který automatizuje opakovanou úlohu kolem testování: vytvoří konfiguraci, ověří ji během a odešle do repozitáře. Rozdělení úlohy na „napiš“ a „pushni“ a revize mezi nimi jsou **human-in-the-loop** z téhož oddílu. Provoz testů v CI s pevnými verzemi a reporty je blízký myšlence opakovatelného provozu z **oddílu 4.2.2** (LLMOps), i když tady se provozují testy, ne model.

Regresní sada, která běží po každé změně, je automatizované regresní testování z **kapitoly 2, oddílu 2.2.3**. Report jako artefakt je podklad pro monitoring a řízení testování z **oddílu 2.2.4**. Prompt v kroku 3 používá strukturu a omezení z **oddílu 2.1.1**.

Vady workflow z kurzu (zelený běh při selhání, komentář, který neodpovídá kódu) jsou chyby v uvažování a halucinace z **kapitoly 3, oddílu 3.1.1**. Hledání tajemství před push, secrets místo hesel v kódu a úzká oprávnění tokenu jsou opatření z **oddílů 3.2.1 a 3.2.3**. Workflow s přístupem k produkci, které může agent změnit, je riziko, které sylabus řeší v **oddílu 3.2.2** u škodlivého generovaného kódu.

Kontrolní seznam z kroku 11 je kvalitativní brána z **kapitoly 5, oddílu 5.1.2**. Nahrání firemního kódu do osobního GitHubu by byla stínová AI a únik dat z **oddílu 5.1.1**.
