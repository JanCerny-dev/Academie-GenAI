---
modul: 12
nazev: Jenkins CI a Allure reporty
podtitul: Spustíš BDD framework z modulů 10 a 11 v Jenkinsu s výběrem tagu a s reportem Allure u každého buildu, a pro srovnání v GitHub Actions.
cas: 3–4 h
uroven: středně pokročilý
nastroje: Java JDK 21, Jenkins LTS, Allure Jenkins Plugin, GitHub Actions, Python 3.12
kapitoly: 2, 3, 4
zdroje: Bruno L75–L81
---

## Co postavíš

Framework z modulů 10 a 11 zatím spouštíš ručně ze svého terminálu. To stačí pro vývoj testů, ne pro tým. Kolega chce testy spustit bez znalosti příkazů, vedoucí chce vidět výsledky včerejšího běhu a regresní sada má běžet po každé změně aplikace. To řeší **CI** (continuous integration, průběžná integrace): server, který testy spouští automaticky nebo na kliknutí, uchovává výstupy a ukazuje historii.

Bruno v deváté sekci kurzu používá **Jenkins**, nejrozšířenější open-source CI server. Na konci modulu budeš mít:

- Jenkins běžící lokálně na `http://localhost:8080`,
- job, který spustí framework s tagem vybraným z rozbalovacího seznamu (`@regression`, `@smoke`, `@api`),
- report Allure u každého buildu, včetně screenshotů selhání z modulu 10,
- upravený `custom_runner.py`, který přijme tag z příkazové řádky i z Jenkinsu,
- pro srovnání minimální workflow v GitHub Actions, který dělá totéž bez vlastního serveru.

Bruno pracuje na Windows s Freestyle jobem nastaveným v prohlížeči. Postup sleduji stejně. Na konci ukazuji, jak stejný job vypadá jako kód (Jenkinsfile), protože tak se Jenkins v týmech používá častěji.

## Předpoklady

- Framework z modulu 10 (a ideálně 11), který lokálně projde příkazem `python custom_runner.py @regression`.
- **Java JDK.** Jenkins je program v Javě. Bruno v L76 instaluje OpenJDK 21, protože to byla v době natáčení nejnovější verze, kterou Jenkins podporoval. Jenkins podporu verzí Javy postupně posouvá. Aktuální stav ověř na stránce *Java Support Policy* v dokumentaci Jenkinsu.
- **Jenkins LTS** jako soubor `jenkins.war` z jenkins.io (sekce Download, varianta LTS, Generic Java package).
- Zhruba 1 GB místa na disku pro Jenkins, pluginy a historii buildů.
- Pro část s GitHub Actions účet na GitHubu a repozitář s frameworkem.

:::pozor
Jenkins je webový server se správou uživatelů a spouští libovolné příkazy na tvém počítači. Na firemním notebooku ho instaluj jen se souhlasem IT, protože se tím mění bezpečnostní profil stroje. Bruno v L77 musel kvůli Jenkinsu přidat výjimku do firewallu. Firewall ani jiná bezpečnostní nastavení firemního zařízení sám neměň. Na osobním počítači pusť Jenkins jen pro lokální přístup (krok 2) a zvol silné heslo správce.
:::

## Postup

### Krok 1: Java JDK a JAVA_HOME (L76)

Bruno stáhne OpenJDK 21 jako zip z archivu jdk.java.net, rozbalí ho do `C:\Program Files (x86)\Java JDK` a nastaví dvě proměnné prostředí:

- `JAVA_HOME` = cesta ke složce JDK (ta, ve které je podsložka `bin`),
- do `Path` přidá `%JAVA_HOME%\bin`.

Nastavení najdeš ve Windows pod *Upravit proměnné prostředí*. Bruno je zakládá jako systémové proměnné, což vyžaduje práva správce. Pro vlastní účet stačí uživatelské proměnné ve stejném dialogu. Pro Mac a Linux má příloha L76 návod s `tar` a `export JAVA_HOME=...`.

Ověření v novém okně terminálu (staré okno změnu proměnných nevidí):

```powershell
java -version
```

Má vypsat verzi 21. Pokud vypíše jinou verzi, máš v `Path` dřív jinou Javu. Pořadí v `Path` rozhoduje.

Rozbalovat JDK do `Program Files (x86)` je trochu neobvyklé, ta složka je určená pro 32bitové programy. Funguje to, jen se to později hůř hledá. Instalátory jako Eclipse Temurin nebo Microsoft Build of OpenJDK nastaví `JAVA_HOME` samy (nad rámec kurzu, neověřeno).

### Krok 2: Spuštění Jenkinsu (L77)

Jenkins se dá nainstalovat jako služba Windows, ale Bruno volí jednodušší cestu. Soubor `jenkins.war` spustí přímo Javou:

```powershell
java -jar jenkins.war
```

V logu hledej řádek `Jenkins is fully up and running`. Výjimky vypsané před ním při prvním startu obvykle nevadí. Potom otevři `http://localhost:8080`.

Pokud je port 8080 obsazený, Bruno doporučuje jiný port. V příloze L77 je ale příkaz `java -jar jenkins.war --httpsPort=9090`. Ten zapíná HTTPS, které potřebuje certifikát. Pro obyčejné HTTP na jiném portu je správná volba `--httpPort`:

```powershell
java -jar jenkins.war --httpPort=9090 --httpListenAddress=127.0.0.1
```

Volba `--httpListenAddress=127.0.0.1` je navíc oproti kurzu. Jenkins pak poslouchá jen na tvém počítači a z jiných strojů v síti není dostupný. Bez ní poslouchá na všech síťových rozhraních. Pro cvičení je lokální přístup přesně to, co chceš.

Při prvním otevření chce Jenkins jednorázové heslo. Najdeš ho v souboru `%USERPROFILE%\.jenkins\secrets\initialAdminPassword`, cestu ukazuje i úvodní stránka a log. Pak zvol *Install suggested plugins*, vytvoř účet správce a potvrď adresu Jenkinsu.

Veškerá data Jenkinsu (joby, buildy, pluginy) leží ve složce `%USERPROFILE%\.jenkins`. Soubor `jenkins.war` je jen program. Jenkins zastavíš klávesami Ctrl+C v okně terminálu a znovu spustíš stejným příkazem.

### Krok 3: První job (L78)

**Job** (úloha) je v Jenkinsu pojmenovaná sada kroků: odkud vzít kód, co spustit a co udělat s výsledky. Bruno nejdřív ověří, že Jenkins vidí Python:

1. *New Item*, název `validate python environment`, typ *Freestyle project*.
2. V sekci *Build Steps* přidej *Execute Windows batch command* (na Macu a Linuxu *Execute shell*).
3. Příkaz `python --version`, potom *Save*.
4. *Build Now*. V *Build History* se objeví build, po kliknutí na něj *Console Output* ukáže verzi Pythonu.

Zelená fajfka znamená, že příkaz skončil návratovým kódem 0. Jenkins pozná úspěch a neúspěch jen podle návratového kódu. Proto v modulu 10 runner končí `raise SystemExit(behave_main(...))`. Bez toho by build mohl být zelený, i když testy selhaly.

Pokud Jenkins Python nenajde, i když v terminálu funguje, běží Jenkins s jinými proměnnými prostředí. Typicky jsi Python přidal do `Path` až po spuštění Jenkinsu. Restartuj Jenkins v novém terminálu.

Testovací job pak Bruno smaže (*Delete Project*).

### Krok 4: Job pro framework (L79)

Druhý job spouští framework. Bruno ho nazve `ai-enhanced-test-automation-framework` a nastaví dvě věci:

- V sekci *General*, *Advanced*, zapne *Use custom workspace* a zadá cestu ke složce frameworku na disku.
- Jako *Execute Windows batch command* napíše `python -m behave --tags="@regression"`.

Po *Build Now* v *Console Output* uvidíš výpis Behave. Na konci 1 feature passed, 5 scenarios passed. Feature s testy API je skipped, protože nemá tag `@regression`.

**Custom workspace** znamená, že Jenkins pracuje přímo ve tvé pracovní složce. Pro výuku je to nejjednodušší. V praxi to má dvě nevýhody. Jenkins spouští testy nad tím, co máš zrovna rozpracované, ne nad verzí v gitu. A úklid v runneru maže složky `reports` a `screenshots` i tobě. Běžné nastavení je *Source Code Management: Git* s adresou repozitáře. Jenkins si pak kód sám stáhne do vlastní složky. Lokální adresář ale musí být gitový repozitář, který Jenkins umí naklonovat.

Jedno vylepšení stojí za to hned. Příkaz `python` spustí ten Python, který je v `Path` jako první, tedy globální instalaci. Ta nemá balíčky z tvého virtuálního prostředí. Brunovi to funguje, protože má balíčky nainstalované i globálně. Spolehlivější je zavolat Python z virtuálního prostředí přímo:

```bat
set HEADLESS=true
.venv\Scripts\python.exe custom_runner.py @regression
```

Proměnná `HEADLESS` přepne prohlížeč do režimu bez okna (modul 10, krok 5). Jenkins na Windows často běží bez přihlášeného uživatele u obrazovky, a pak okno prohlížeče stejně nikdo neuvidí.

### Krok 5: Výběr tagu jako parametr buildu (L80)

Job s napevno zapsaným `@regression` neumí spustit jen smoke testy nebo jen API. Bruno proto přidá parametr:

1. *Configure*, *This project is parameterized*, *Add Parameter*, *Choice Parameter*.
2. Název `BEHAVE_TAGS`, volby na samostatných řádcích: `@regression`, `@smoke`, `@api`.
3. Tlačítko *Build Now* se změní na *Build with Parameters*.

Jenkins předá každý parametr buildu jako proměnnou prostředí se stejným názvem. V příkazu pro Windows se na ni odkážeš `%BEHAVE_TAGS%`, v shellu `$BEHAVE_TAGS`:

```bat
.venv\Scripts\python.exe custom_runner.py --tags "%BEHAVE_TAGS%"
```

Runner musí tag přijmout. Bruno v L80 přidá do `custom_runner.py` modul `argparse` a čtení proměnné prostředí:

```python
parser = argparse.ArgumentParser(description="Run Behave tests with specific tags.")
parser.add_argument("--tags", help="Behave tags to filter scenarios", default="")
args = parser.parse_args()

tags = args.tags or os.getenv("BEHAVE_TAGS", "")

behave_main(["--tags", tags, "--format", "allure_behave.formatter:AllureFormatter",
             "--outfile", "reports/allure-results"])
```

Pořadí `args.tags or os.getenv(...)` znamená: tag z příkazové řádky má přednost, pak se použije proměnná z Jenkinsu. Runner tak funguje stejně lokálně i v CI.

Když ale tag nepřijde ani jednou cestou, předá runner Behave volbu `--tags ""`. Jak se na prázdný výraz Behave zachová, jsem neověřoval. Bezpečnější je volbu `--tags` vůbec nepřidat a spustit všechno. Vlastní varianta, ve které je logika sestavení argumentů oddělená do funkce, aby se dala otestovat bez spuštění Behave (funkce ověřená v `zdroje/_pracovni/bruno/over_offline.py`):

```python
import argparse, os, shutil
from behave.__main__ import main as behave_main

def behave_argumenty(tags_cli, env) -> list[str]:
    tags = tags_cli or env.get("BEHAVE_TAGS", "")
    args = ["--format", "allure_behave.formatter:AllureFormatter",
            "--outfile", "reports/allure-results",
            "--format", "pretty"]
    return (["--tags", tags] + args) if tags else args

def vycisti(slozka: str) -> None:
    shutil.rmtree(slozka, ignore_errors=True)
    os.makedirs(slozka, exist_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spuštění Behave podle tagů")
    parser.add_argument("--tags", default="")
    vycisti("reports")
    vycisti("screenshots")
    raise SystemExit(behave_main(behave_argumenty(parser.parse_args().tags, os.environ)))
```

Runner z modulu 10 bral tag jako první argument (`custom_runner.py @smoke`). Tato verze ho bere přes `--tags`, stejně jako Brunova. Uprav podle toho příkaz v jobu z kroku 4. Druhý formát `pretty` posílá čitelný průběh do konzole, takže ho uvidíš v *Console Output*. Bez něj je v Jenkinsu konzole skoro prázdná a všechny informace jsou jen v Allure.

V *Build History* u každého buildu ukazuje odkaz *Parameters*, s jakým tagem běžel. Když kolega hlásí, že „testy včera neprošly“, víš hned, kterou sadu spustil.

### Krok 6: Allure report v Jenkinsu (L81)

Ručně spouštěné `allure generate` z modulu 10 nahradí plugin. Bruno postupuje takto:

1. *Manage Jenkins*, *Plugins*. Nejdřív na záložce *Updates* aktualizuj nainstalované pluginy. Aktualizace často opravují bezpečnostní chyby. Některé vyžadují restart Jenkinsu.
2. Na záložce *Available plugins* vyhledej `Allure` a nainstaluj **Allure Jenkins Plugin**.
3. *Manage Jenkins*, *Tools*, sekce *Allure Commandline*: *Add Allure Commandline*, zadej název (třeba `allure`) a zapni automatickou instalaci nejnovější verze. Jenkins si nástroj stáhne sám, lokální instalace z modulu 10 tu není potřeba.
4. V jobu, sekce *Post-build Actions*, *Allure Report*. Do pole s cestou k výsledkům zadej `reports/allure-results`.

Pole s cestou je relativní k pracovní složce jobu. Bruno v L81 nastavuje i pole v *Advanced* a zapisuje cestu se zpětným lomítkem. Jenkins na Windows přijme obě lomítka. Rozhodující je, aby cesta vedla do složky se soubory JSON, ne do vygenerovaného HTML.

Po dalším buildu se u něj objeví ikona Allure. Report je uložený zvlášť pro každý build. Build s `@regression` ukáže pět prošlých testů a jeden přeskočený test API. Build s `@api` ukáže opak. Plugin navíc přenáší složku `history` mezi buildy, takže report ukazuje trend úspěšnosti. To lokální `allure generate --clean` z modulu 10 nedělá.

Bruno na závěr záměrně rozbije tři řádky v Examples (přidá do očekávané hlášky „555“). Build skončí jako neúspěšný a report ukazuje selhané scénáře se screenshoty z `after_scenario`. Jaký stav dostane build (*Failure* nebo *Unstable*), závisí na návratovém kódu runneru a nastavení pluginu (neověřeno).

### Krok 7: Tajemství v Jenkinsu

Testy z modulů 10 a 11 API klíč OpenAI nepotřebují. Volají ho jen generátory scénářů a `analyze_steps`, které se spouštějí ručně při psaní testů. Do CI je nedávej. Generovat testy při každém buildu znamená platit za každý build a dostávat pokaždé trochu jiné testy. To je opak toho, co od regresní sady chceš.

Když přesto job klíč potřebuje (třeba noční job, který generuje návrhy scénářů k revizi), nikdy ho nepiš do příkazu jobu ani do souboru v repozitáři. Jenkins má **Credentials** (úložiště přihlašovacích údajů):

1. *Manage Jenkins*, *Credentials*, přidej záznam typu *Secret text* s ID `openai-api-key`.
2. V jobu zapni *Use secret text(s) or file(s)* (plugin Credentials Binding je součástí doporučených pluginů) a namapuj ho na proměnnou `OPENAI_API_KEY`.

Jenkins pak klíč předá procesu jako proměnnou prostředí a v *Console Output* ho nahradí hvězdičkami. Knihovna `openai` si ho z proměnné vezme sama, jak ukazuje modul 9.

### Krok 8: Stejný job jako Jenkinsfile (nad rámec kurzu)

Freestyle job je nastavený klikáním a jeho konfigurace žije jen v Jenkinsu. Když Jenkins spadne nebo někdo nastavení změní, nikdo neví, co bylo předtím. **Pipeline** se zapisuje do souboru `Jenkinsfile` v repozitáři, verzuje se s kódem a prochází code review. Ekvivalent Brunova jobu (neověřeno spuštěním):

```groovy
pipeline {
    agent any
    parameters {
        choice(name: 'BEHAVE_TAGS', choices: ['@regression', '@smoke', '@api'], description: 'Které testy spustit')
    }
    environment {
        HEADLESS = 'true'
    }
    stages {
        stage('Příprava') {
            steps {
                bat 'python -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
                bat '.venv\\Scripts\\python.exe -m playwright install chromium'
            }
        }
        stage('Testy') {
            steps {
                bat '.venv\\Scripts\\python.exe custom_runner.py --tags "%BEHAVE_TAGS%"'
            }
        }
    }
    post {
        always {
            allure results: [[path: 'reports/allure-results']]
        }
    }
}
```

Job typu *Pipeline* s volbou *Pipeline script from SCM* si soubor načte z gitu. Sekce `post { always { ... } }` zajistí, že se report vytvoří i po neúspěšných testech. Zpětná lomítka jsou v Groovy řetězci zdvojená. Na Linuxu by místo `bat` byl `sh` a cesta `.venv/bin/python`.

### Krok 9: GitHub Actions (nad rámec kurzu)

Jenkins vyžaduje vlastní server, jeho údržbu a aktualizace pluginů. Pro projekty na GitHubu je dnes častější volbou **GitHub Actions**: CI přímo v GitHubu, bez vlastního serveru, s konfigurací v repozitáři. Pro GitLab existuje obdoba GitLab CI. Jenkins zůstává běžný ve firmách, které mají CI na vlastní infrastruktuře, například v bankách.

Minimální workflow `.github/workflows/bdd-testy.yml` pro stejný framework (neověřeno spuštěním, verze akcí ověř na GitHub Marketplace):

```yaml
name: BDD testy
on:
  workflow_dispatch:
    inputs:
      tags:
        description: Tag pro Behave
        type: choice
        options: ["@regression", "@smoke", "@api"]
        default: "@regression"
  push:
    branches: [main]

jobs:
  testy:
    runs-on: ubuntu-latest
    env:
      HEADLESS: "true"
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python -m playwright install --with-deps chromium
      - run: python custom_runner.py --tags "${{ inputs.tags || '@regression' }}"
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: allure-results
          path: reports/allure-results
```

Workflow se spustí po každém push do větve `main` s tagem `@regression`, nebo ručně na záložce *Actions* s výběrem tagu. Výraz `inputs.tags || '@regression'` dosadí výchozí tag, když workflow nespustil člověk. Volba `--with-deps` doinstaluje na Linuxu systémové knihovny, které Chromium potřebuje.

Výsledky Allure se uloží jako artifact buildu ke stažení. Na stažené výsledky pak lokálně spustíš `allure serve`. Publikovat HTML report přímo na web (například přes GitHub Pages) jde, ale vyžaduje další kroky a u soukromých projektů pozor na to, kdo report uvidí.

Klíč by se tu předal přes *Settings*, *Secrets and variables*, *Actions* a v kroku jako `env: OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}`. Platí stejné pravidlo jako u Jenkinsu: do běžného běhu testů nepatří.

U firemních repozitářů rozhoduje o CI firemní platforma. Kód klienta nepouštěj do veřejných runnerů ani do osobního účtu GitHub.

## Ověření

1. `java -version` v novém terminálu ukazuje verzi, kterou Jenkins podporuje.
2. Jenkins běží na `http://localhost:8080` (nebo na zvoleném portu). Z jiného počítače v síti dostupný není, pokud jsi použil `--httpListenAddress=127.0.0.1`.
3. Job *Build with Parameters* s volbou `@smoke` skončí zeleně. *Console Output* ukazuje 2 scenarios passed a zbytek skipped.
4. Build s `@api` neotevře prohlížeč a projde (pokud máš modul 11).
5. U každého buildu je ikona Allure a report obsahuje jen scénáře s vybraným tagem.
6. Po záměrném rozbití očekávané hlášky je build červený, v reportu je selhání se screenshotem. Po vrácení změny je další build zase zelený a graf trendu v Allure ukazuje oba stavy.
7. V konfiguraci jobu ani v repozitáři není žádný API klíč.

Funkce pro sestavení argumentů runneru je ověřená offline. Jenkins, plugin Allure, Jenkinsfile ani workflow GitHub Actions jsem nespouštěl.

## Časté chyby

**Jenkins nestartuje kvůli verzi Javy.** Novější Java, než Jenkins podporuje, nebo naopak příliš stará. Log na začátku vypíše chybu o nepodporované verzi. Zkontroluj `java -version` ve stejném terminálu, ze kterého Jenkins spouštíš.

**Port 8080 je obsazený.** Jiná aplikace (často jiný vývojový server) port používá. Spusť Jenkins s `--httpPort=9090`. Volba `--httpsPort` z přílohy kurzu je pro HTTPS a bez certifikátu nefunguje.

**`'python' is not recognized` v buildu.** Jenkins běží s proměnnými prostředí z doby svého spuštění. Restartuj ho po změně `Path`, nebo volej Python plnou cestou (`.venv\Scripts\python.exe`).

**`ModuleNotFoundError: No module named 'behave'` v buildu.** Jenkins spustil globální Python bez balíčků z virtuálního prostředí. Volej Python z `.venv`.

**Build je zelený, i když testy selhaly.** Runner nevrací návratový kód z Behave. Použij `raise SystemExit(behave_main(...))`.

**Parametr se nepropsal, běží všechny testy.** Na Windows je proměnná `%BEHAVE_TAGS%`, v shellu `$BEHAVE_TAGS`. Ve Windows batch příkazu `$BEHAVE_TAGS` nefunguje a předá se doslova.

**Allure report v Jenkinsu je prázdný.** Cesta v *Post-build Actions* nevede do složky se soubory JSON. Nebo runner složku `reports` smazal a Behave do ní nic nezapsal, protože spadl dřív. Podívej se do *Console Output* a do pracovní složky jobu.

**Testy v Jenkinsu padají na timeout, lokálně ne.** Headless prohlížeč na vytíženém stroji je pomalejší a bezplatné API se probouzí. Prodluž timeouty v asercích a u požadavků (moduly 10 a 11).

**Prohlížeč v Jenkinsu nejde spustit.** Jenkins běží jako služba bez grafického prostředí. Zapni `HEADLESS=true`.

## Cvičení

:::cviceni nazev="Noční regresní běh"
Cíl: spouštět regresní sadu automaticky. V jobu zapni *Build periodically* a nastav plán tak, aby běžel každý pracovní den v noci. Zápis používá syntaxi cron, symbol `H` rozloží zátěž v rámci hodiny.
Hotovo: druhý den ráno vidíš v *Build History* automaticky spuštěný build s tagem `@regression` a jeho report Allure. Do poznámky jsi zapsal, jaký výraz jsi použil a co přesně znamená.
:::

:::cviceni nazev="Freestyle job převedený na Jenkinsfile"
Cíl: mít konfiguraci CI verzovanou v gitu. Ulož Jenkinsfile z kroku 8 do repozitáře frameworku, založ job typu *Pipeline* s volbou *Pipeline script from SCM* a smaž Freestyle job.
Hotovo: build s parametrem `@smoke` projde, report Allure se vytvoří i při záměrně rozbitém testu (díky `post { always }`) a celá konfigurace je v souboru, který jde ukázat v code review.
:::

:::cviceni nazev="Srovnání Jenkins a GitHub Actions"
Cíl: rozhodnout se podle zkušenosti, ne podle článků. Nahraj framework do soukromého repozitáře na GitHubu (bez `.env`, zkontroluj `git status`) a přidej workflow z kroku 9.
Hotovo: workflow projde, artifact `allure-results` jde stáhnout a lokálně otevřít přes `allure serve`. Do krátké tabulky jsi zapsal pro obě varianty dobu běhu, počet kroků nastavení, kde jsou uložené reporty a kdo spravuje server.
:::

## Souvislost se sylabem CT-GenAI

Sylabus jenkinsovou konfiguraci nezkouší. Modul ale ukazuje, co se stane s testy vytvořenými pomocí GenAI, když se z nich stane regresní sada. Oddíl 2.2.3 (automatizované regresní testování s GenAI) mluví o udržování regresních testů a o vyhodnocování výsledků. Pravidelný běh v CI s reportem a historií je místo, kde se ukáže, jestli AI vygenerované testy jsou stabilní, nebo flaky. Report s trendem a screenshoty je také vstup pro monitoring testování z oddílu 2.2.4.

Rozhodnutí negenerovat testy při každém buildu souvisí s nedeterministickým chováním z oddílu 3.1.4. Regresní sada musí být stabilní, a proto se generuje jednou, reviduje člověkem a verzuje v gitu. Uložení API klíče v Credentials Jenkinsu nebo v Secrets na GitHubu je opatření z oddílu 3.2.3. Varování před osobním účtem a veřejnými runnery pro firemní kód odpovídá rizikům z oddílu 3.2.1.

Oddíl 4.2.2 o LLMOps popisuje průběžné nasazování a monitorování aplikací postavených na LLM. CI pipeline z tohoto modulu je jeho nejjednodušší stavební kámen: stejný mechanismus by spouštěl i automatické hodnocení kvality promptů, pokud by framework generoval testy pravidelně.
