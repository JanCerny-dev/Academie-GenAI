---
kapitola: 2
varianta: vyklad
nadpis: Prompt engineering pro efektivní testování
podtitul: Jak sestavit prompt, kterou techniku zvolit pro kterou testovací činnost a jak výsledek změřit a prompt vylepšit.
---

Druhá kapitola je jádrem celého sylabu CT-GenAI. Sylabus jí přiděluje 365 minut výuky, víc než kterékoli jiné kapitole. Ve zkoušce z ní je 11 otázek za 16 bodů ze 46. Pět z těch otázek je na úrovni K3 a každá má dva body. Jsou to jediné K3 otázky kapitoly a dohromady dávají deset bodů. Kdo zvládne oddíl 2.2, má skoro třetinu bodů potřebných k úspěchu.

Kapitola má tři části. Oddíl 2.1 vysvětluje, z čeho se skládá dobrý prompt, jaké jsou základní techniky promptování a čím se liší systémový prompt od uživatelského. Oddíl 2.2 ukazuje, jak se tyto znalosti použijí v konkrétních testovacích činnostech: v testovací analýze, v návrhu a implementaci testů, v automatizovaném regresním testování a v monitoringu a řízení testování. Na konci oddílu 2.2 je návod, jak vybrat vhodnou techniku. Oddíl 2.3 se věnuje tomu, jak výsledky generativní AI měřit a jak prompt postupně vylepšovat.

Sylabus uvádí dvě skupiny klíčových slov. Obecné testovací pojmy jsou **acceptance criteria** (akceptační kritéria), **test script** (testovací skript), **test case** (testovací případ), **test condition** (testovací podmínka), **test data** (testovací data), **test design** (návrh testů) a **test report** (report z testování). Pojmy specifické pro GenAI jsou **few-shot prompting**, **meta prompting**, **natural language processing** (zpracování přirozeného jazyka), **one-shot prompting**, **prompt**, **prompt chaining** (řetězení promptů), **prompt engineering**, **system prompt** (systémový prompt), **user prompt** (uživatelský prompt) a **zero-shot prompting**. Všechny je třeba umět poznat v anglickém textu otázky.

Kapitola obsahuje i čtrnáct praktických cílů (hands-on objectives, HO). Ve zkoušce se přímo nezkoušejí, ale K3 otázky jsou z nich odvozené. Typická K3 otázka popíše situaci z některého cvičení a chce, abyste vybrali nejlepší prompt, nejlepší úpravu promptu nebo nejlepší pořadí kroků. Proto výklad u každého cvičení ukazuje, jak by prompt mohl vypadat.

Ukázkové prompty jsou většinou česky, aby se daly rovnou vyzkoušet. Názvy komponent promptu (Role, Context, Instruction…) nechávám anglicky, protože přesně tak je uvidíte ve zkoušce. Zkouška ukazuje prompty jen anglicky.

## 2.1 Tvorba účinných promptů

:::lo
GenAI-2.1.1 (K2) Give examples of the structure of prompts used in generative AI for software testing
GenAI-2.1.2 (K2) Differentiate core prompting techniques for software testing
GenAI-2.1.3 (K2) Distinguish between system prompts and user prompts
:::

Oddíl 2.1 odpovídá anglickému názvu **Effective Prompt Development**. Sylabus v něm skládá dohromady tři věci. Strukturovaný prompt dává požadavku jasný tvar. Techniky promptování určují, jak s modelem pracovat (s příklady, po krocích, nebo tak, že model pomáhá prompt napsat). A rozdělení na systémový a uživatelský prompt říká, co platí pro celou konverzaci a co jen pro jeden dotaz. Teprve kombinace všech tří dává dobré výsledky.

### Prompt a prompt engineering

**Prompt** je vstup, kterým uživatel nebo aplikace zadává velkému jazykovému modelu (LLM) úlohu. Může to být otázka, pokyn, text k analýze, obrázek nebo kombinace těchto prvků. Model z promptu odvodí, co má udělat, a vygeneruje odpověď.

:::pojem term="prompt"
Vstup pro LLM, kterým zadáváme úlohu. Obsahuje pokyn a podle potřeby kontext, data, příklady a požadavky na tvar odpovědi.
:::

**Prompt engineering** (tvorba promptů) je disciplína, která se zabývá tím, jak prompty navrhovat, zkoušet a vylepšovat, aby model vracel přesné a použitelné výsledky. Pro testera to není nová profese. Je to dovednost podobná psaní dobrého testovacího případu. Nejasný testovací případ provede každý jinak. Nejasný prompt dá pokaždé jiný a často nepoužitelný výsledek.

:::pojem term="prompt engineering"
Návrh, zkoušení a postupné vylepšování promptů tak, aby LLM vracel přesné, relevantní a konzistentní výstupy pro danou úlohu.
:::

Model rozumí textu díky **natural language processing** (NLP, zpracování přirozeného jazyka). Je to obor AI, který se zabývá porozuměním lidskému jazyku a jeho generováním. Sylabus pojem zmiňuje u dvou úloh. V testovací analýze model díky NLP interpretuje význam požadavků a rozkládá je na testovatelná tvrzení. V návrhu testů díky NLP vytváří z požadavků návrhy testovacích případů. Ve zkoušce stačí vědět, že NLP je schopnost, která modelu umožňuje pracovat s požadavky psanými běžným jazykem.

:::pojem term="natural language processing (NLP)"
Zpracování přirozeného jazyka. Obor AI, díky kterému model rozumí textu psanému běžným jazykem a umí jej vytvářet. V testování umožňuje převést slovní požadavky na testovací podmínky a testovací případy.
:::

Rozdíl mezi slabým a dobrým promptem je vidět na jednoduchém příkladu. Slabý prompt zní takto:

```text
Napiš testy na převod peněz.
```

Model neví, o jakou aplikaci jde, jaká pravidla platí, kolik testů chcete ani v jakém tvaru. Vrátí obecný seznam, který by se hodil na jakoukoli banku na světě. Lepší prompt říká, kdo má odpovídat, o jaký systém jde, co přesně udělat, z jakých podkladů vyjít, čeho se držet a jak má výsledek vypadat. Přesně to popisuje struktura promptu v oddílu 2.1.1.

### 2.1.1 Struktura promptu pro testování

Sylabus popisuje strukturovaný prompt pro testování jako skladbu šesti komponent. Pořadí je v sylabu vždy stejné a vyplatí se ho naučit: **role**, **context**, **instruction**, **input data**, **constraints**, **output format**. Každá komponenta odpovídá na jinou otázku.

| Komponenta | Česky | Na jakou otázku odpovídá |
|---|---|---|
| Role | role | Z jakého pohledu má model odpovídat? |
| Context | kontext | O jaký systém, funkci a situaci jde? |
| Instruction | instrukce, pokyn | Co přesně má model udělat? |
| Input data | vstupní data | S jakými podklady má pracovat? |
| Constraints | omezení | Jakých pravidel a hranic se má držet? |
| Output format | formát výstupu | Jak má výsledek vypadat? |

Tabulka slouží jako tahák. Následuje rozbor každé komponenty.

#### Role

**Role** určuje perspektivu nebo personu, kterou má model zaujmout. Typicky je to tester, test analytik, test manažer nebo inženýr automatizace testů. Role pomáhá modelu odhadnout, za co odpovídá a jakým tónem a přístupem má psát. Test manažer bude psát o rizicích, termínech a zdrojích. Inženýr automatizace bude psát o lokátorech, frameworku a stabilitě skriptů.

```text
Jsi zkušený test analytik se zaměřením na platební systémy v bankovnictví.
```

Role nemá být přehnaně úzká ani nesmyslně obecná. „Jsi tester“ je slabé, ale použitelné. „Jsi nejlepší tester na světě s 30 lety praxe“ nepřidává žádnou informaci. Dobrá role popisuje odbornost, která je pro úlohu potřeba.

#### Context

**Context** (kontext) dává modelu informace o pozadí, které potřebuje, aby určil testovací podmínky. Patří sem popis testovaného objektu, konkrétní testované funkce a dalších okolností: typ aplikace, uživatelé, prostředí, fáze projektu, regulatorní rámec.

```text
Testujeme mobilní bankovnictví pro fyzické osoby. Nová verze přidává okamžité
platby do 400 000 Kč. Aplikace běží na Androidu a iOS, platby se autorizují
biometrií nebo PINem.
```

Kontext odpovídá na otázku „o čem to je“. Nejde o data, se kterými má model přímo pracovat. To je nejčastější záměna, ke které se ještě vrátíme.

#### Instruction

**Instruction** (instrukce) je samotný pokyn. Říká, jakou úlohu má model provést. Sylabus chce, aby instrukce byla jasná, v rozkazovacím způsobu a stručná. Obsahuje popis úlohy a podstatné požadavky na ni.

```text
Navrhni testovací podmínky pro okamžitou platbu podle níže uvedeného
uživatelského scénáře a akceptačních kritérií.
```

Instrukce začíná slovesem: navrhni, analyzuj, porovnej, seřaď, najdi, převeď. „Mohl bys se podívat na…“ je slabší, protože nedává jasný úkol.

#### Input data

**Input data** (vstupní data) jsou všechny informace, které model potřebuje k provedení úlohy. Sylabus jmenuje uživatelské scénáře, akceptační kritéria, snímky obrazovky, kód, existující testovací případy a ukázky výstupu. Čím podrobnější a lépe strukturovaná vstupní data, tím přesnější a lépe zasazený výsledek.

```text
Uživatelský scénář:
Jako klient banky chci odeslat okamžitou platbu, aby peníze dorazily příjemci
do několika sekund.

Akceptační kritéria:
AC1: Okamžitou platbu lze odeslat jen na účet banky zapojené do systému
     okamžitých plateb.
AC2: Maximální částka jedné platby je 400 000 Kč.
AC3: Pokud banka příjemce platbu nepřijme do 10 sekund, klient uvidí chybové
     hlášení a peníze se mu vrátí na účet.
```

Vstupní data je dobré v promptu jasně oddělit, třeba nadpisem, odrážkou nebo oddělovačem. Model pak ví, co je pokyn a co materiál k zpracování.

#### Constraints

**Constraints** (omezení) popisují omezení nebo zvláštní pravidla, která má model dodržet. Sylabus říká, že omezení určují, *jak* se mají instrukce použít na vstupní data. Typická omezení v testování jsou rozsah (jen funkční testy, jen negativní případy), použitá technika (analýza hraničních hodnot), terminologie (podle ISTQB), zakázané věci (nevymýšlej chování, které není v podkladech) a priorita zdrojů (při rozporu mezi wireframem a požadavkem platí požadavek).

```text
Zaměř se jen na funkční chování, ne na vzhled obrazovky. Pro AC2 použij analýzu
hraničních hodnot. Pokud v podkladech něco chybí, nevymýšlej to, ale uveď to
jako otevřenou otázku.
```

#### Output format

**Output format** (formát výstupu) říká, jakou podobu, strukturu nebo vlastnosti má mít odpověď: tabulka, seznam, JSON, Gherkin, Markdown, počet položek, sloupce, jazyk, délka.

```text
Výstup vrať jako tabulku Markdown se sloupci: ID, testovací podmínka,
vazba na AC, priorita (vysoká/střední/nízká). Pod tabulku napiš seznam
otevřených otázek.
```

#### Celý strukturovaný prompt

Když komponenty složíme, vznikne prompt, se kterým model nemusí nic hádat. Popisky komponent v promptu psát nemusíte. Pomáhají ale čitelnosti a usnadňují kontrolu, jestli nic nechybí. Ve zkoušce bývají prompty s popisky, aby šlo o jednotlivých částech mluvit.

```text
Role: Jsi zkušený test analytik se zaměřením na platební systémy v bankovnictví.

Context: Testujeme mobilní bankovnictví pro fyzické osoby. Nová verze přidává
okamžité platby do 400 000 Kč. Platby se autorizují biometrií nebo PINem.

Instruction: Navrhni testovací podmínky pro okamžitou platbu podle uživatelského
scénáře a akceptačních kritérií níže.

Input data:
<uživatelský scénář a AC1 až AC3 z předchozí ukázky>

Constraints: Jen funkční chování. Pro AC2 použij analýzu hraničních hodnot.
Nevymýšlej chování, které v podkladech není; chybějící informace uveď jako
otevřené otázky.

Output format: Tabulka Markdown se sloupci ID, testovací podmínka, vazba na AC,
priorita. Pod tabulkou seznam otevřených otázek.
```

Sylabus dodává, že struktura je jen základ. Kombinuje se s technikami promptování z oddílu 2.1.2 podle toho, o jakou úlohu jde a jaký model se používá.

:::praxe
Stejná struktura funguje i nad projektem `uctenky` (fakturační systém v Djangu a Reactu). Prompt pro test analýzu filtru faktur by mohl vypadat takto:

```text
Role: Jsi test analytik webových aplikací.
Context: Aplikace eviduje osoby a faktury. Stránka Faktury má filtr podle
odběratele, dodavatele, produktu, minimální a maximální ceny a limitu počtu
záznamů. API endpoint je GET /api/invoices/filter.
Instruction: Navrhni testovací podmínky pro filtr faktur.
Input data: Popis parametrů filtru (viz níže) a model Invoice: price je
DecimalField(max_digits=10, decimal_places=2).
Constraints: Jen funkční testy filtru, ne vzhled. Pro cenu a limit použij
hraniční hodnoty. Kombinace filtrů omez na páry.
Output format: Tabulka: ID, podmínka, parametry, typ (pozitivní/negativní).
```

Model díky informaci o `DecimalField` sám navrhne hranici dvou desetinných míst a maximální hodnotu 99 999 999,99. Bez té informace by ji neměl odkud vzít.
:::

#### Jak komponenty rozlišit

Ve zkoušce dostanete jeden řádek promptu a máte určit, do které komponenty patří. Nejčastěji se pletou tři dvojice.

**Context × Input data.** Kontext popisuje svět kolem úlohy: systém, funkci, uživatele, prostředí. Vstupní data jsou konkrétní materiál, se kterým model pracuje: text požadavku, log, report z nástroje, snímek obrazovky, existující testy. Pomůcka: kdyby šlo materiál přiložit jako soubor, jsou to vstupní data. Věta „testujeme pojišťovací portál pro zprostředkovatele“ je kontext. Věta „použij přiložený export 120 testovacích případů z Jira“ jsou vstupní data.

**Constraints × Output format.** Omezení říkají, jakých pravidel se držet při práci. Formát výstupu říká, jak má vypadat výsledek. „Vrať tabulku se sloupci ID, popis, závažnost“ je formát. „Ber v úvahu jen požadavky označené jako schválené“ je omezení. Pozor na hraniční případ: „použij syntaxi Given-When-Then“ může být v různých promptech uvedeno jako omezení i jako formát. Rozhoduje, jestli věta mluví o pravidle pro tvorbu (omezení), nebo o podobě odevzdaného výsledku (formát).

**Instruction × Constraints.** Instrukce říká *co* dělat, omezení *jak* nebo *v jakých mezích*. „Najdi nejednoznačnosti v požadavcích“ je instrukce. „Posuzuj jen požadavky v kapitole 3“ je omezení.

:::zkouska
LO 2.1.1 má ve zkoušce dvě otázky, víc než ostatní K2 cíle v kapitole. Typicky dostanete popis jedné části promptu a čtyři komponenty na výběr. Hledejte sloveso a předmět věty. Rozkaz s úlohou je instrukce. Popis systému je kontext. Konkrétní soubory, texty a data jsou vstupní data. Pravidla a zákazy jsou omezení. Tvar výsledku je formát výstupu. Pamatujte také, že komponent je šest. Teplota (temperature), velikost modelu nebo seed nejsou komponenty promptu, jsou to parametry modelu.
:::

#### Jak poznat slabou komponentu

K3 otázky v oddílu 2.2 často ukazují rozepsaný prompt, ve kterém je jedna komponenta slabá. Prompt má všech šest částí, ale jedna z nich nic neříká. Typické slabiny:

- Role je tak obecná, že nic neurčuje, nebo tak úzká, že model odvádí od cíle.
- Instrukce je vágní („analyzuj výsledky“), takže model neví, jaký výstup má vzniknout.
- Omezení odkazuje na nic neříkající „osvědčené postupy“ (best practices) místo konkrétního pravidla.
- Omezení je v rozporu s cílem, například „vygeneruj nejvýš dva testovací případy“, když se chce pokrytí všech akceptačních kritérií.
- Formát výstupu neodpovídá čtenáři, například technická tabulka pro vedení firmy.
- Vstupní data chybí nebo nejsou ta, která úloha potřebuje.

Při řešení takové otázky se ptejte: která změna nejvíc přiblíží výsledek k cíli popsanému v zadání? Nejlepší úprava bývá konkrétní a míří přesně na slabé místo. Úprava, která jen přidává slova bez nové informace, bývá distraktor.

Praktický cíl **HO-2.1.1 (H0)** je pozorovací. Ve výuce se ukáže několik strukturovaných promptů pro různé testovací úlohy a účastníci v nich hledají šest komponent a sledují, jak každá ovlivní výsledek. Cvičení najdete v datech kapitoly.

### 2.1.2 Základní techniky promptování

Sylabus odkazuje na přehledovou práci Schulhoff (2024), která popisuje desítky technik promptování. Pro testování z nich vybírá tři **core prompting techniques** (základní techniky promptování): **prompt chaining**, **few-shot prompting** a **meta prompting**. Všechny tři se kombinují se šestisložkovou strukturou z oddílu 2.1.1. Do výkladu few-shot promptingu sylabus zahrnuje i **zero-shot** a **one-shot prompting**. Ve zkoušce se tedy počítá s pěti názvy, ale za „tři základní techniky“ se považují chaining, few-shot a meta prompting.

#### Zero-shot prompting

**Zero-shot prompting** znamená, že prompt neobsahuje žádný příklad požadovaného výstupu. Model se opírá jen o znalosti, které získal při tréninku. Hodí se pro jednoduché a běžné úlohy, kde je jasné, co se chce, a na přesném tvaru výsledku tolik nezáleží.

```text
Vysvětli rozdíl mezi konfirmačním a regresním testováním. Uveď ke každému
jeden příklad z webového e-shopu.
```

Zero-shot neznamená špatný prompt. Může být plně strukturovaný, se všemi šesti komponentami. Jen v něm není ukázka. Když je výsledek nekonzistentní v tvaru nebo stylu, je to signál přejít na one-shot nebo few-shot.

:::pojem term="zero-shot prompting"
Prompt bez jakéhokoli příkladu výstupu. Model se opírá jen o znalosti z tréninku.
:::

#### One-shot prompting

**One-shot prompting** přidává do promptu právě jeden příklad. Příklad ukazuje, jaký výsledek se očekává pro daný vstup.

```text
Převeď akceptační kritérium na testovací případ ve stejném tvaru jako v příkladu.

Příklad:
Kritérium: Slevový kód SLEVA10 sníží cenu košíku o 10 %.
Testovací případ:
  ID: TC-01
  Předpoklad: Košík obsahuje zboží za 1 000 Kč.
  Kroky: Zadej kód SLEVA10 a potvrď.
  Očekávaný výsledek: Cena košíku je 900 Kč.

Kritérium: Doprava je zdarma pro objednávky od 1 500 Kč.
Testovací případ:
```

:::pojem term="one-shot prompting"
Prompt s právě jedním příkladem, který ukazuje očekávaný výstup pro daný vstup.
:::

#### Few-shot prompting

**Few-shot prompting** obsahuje víc než jeden příklad, tedy „několik“. Víc příkladů pevněji ukotví požadované chování modelu. Model z nich odvodí vzor a použije ho na nový vstup. Sylabus říká, že technika je zvlášť účinná u úloh, kde příklady umí ukázat požadované chování. Model pak dobře zobecňuje a výsledky jsou konzistentní.

```text
Role: Jsi test analytik pojišťovny.
Instruction: Pro nový uživatelský scénář napiš testovací scénáře v Gherkinu
stejně jako v příkladech.

Příklad 1
Scénář: Jako klient chci vidět výši pojistného před uzavřením smlouvy.
Gherkin:
  Scenario: Zobrazení pojistného pro standardní vozidlo
    Given klient zadal vozidlo s objemem motoru 1 400 cm3
    When klient přejde na shrnutí nabídky
    Then vidí roční pojistné a měsíční splátku

Příklad 2
Scénář: Jako klient chci nahlásit škodu online.
Gherkin:
  Scenario: Nahlášení škody s fotografií
    Given klient je přihlášen a má aktivní smlouvu
    When klient vyplní popis škody a přiloží fotografii
    Then systém založí škodní událost a zobrazí její číslo

Nový scénář: Jako klient chci změnit frekvenci placení z ročního na čtvrtletní.
Gherkin:
```

Kolik příkladů použít, sylabus neurčuje. V praxi se začíná dvěma až pěti. Příklady mají být rozmanité, aby model nepřevzal náhodnou vlastnost jednoho z nich. Když budou všechny tři příklady o přihlášeném klientovi, model začne každý scénář přihlášením, i když to nový scénář nepotřebuje.

:::pojem term="few-shot prompting"
Prompt s několika (víc než jedním) příklady vstupu a očekávaného výstupu. Příklady ukotví tvar a styl výsledku a model je zobecní na nový vstup.
:::

:::zkouska
Zero-shot, one-shot a few-shot se liší jen počtem příkladů v promptu: žádný, jeden, několik. Nezáleží na tom, kolikrát s modelem mluvíte. Pět zpráv bez příkladu není few-shot, ale nejspíš prompt chaining. Jeden prompt se třemi ukázkami je few-shot. Pozor i na to, že „shot“ znamená příklad, ne pokus.
:::

#### Prompt chaining

**Prompt chaining** (řetězení promptů) rozkládá úlohu na řadu mezikroků. Každý krok má vlastní prompt. Výsledek každého kroku se ručně nebo automaticky zkontroluje a případně opraví, než se pokračuje dalším krokem. Protože každá odpověď ovlivňuje další prompt, je výsledek přesnější. Sylabus doporučuje řetězení pro testovací úlohy, které jsou složité, potřebují rozklad na dílčí úlohy a systematickou kontrolu mezivýsledků. Řetězení navíc umožňuje dynamickou interakci: podle výsledku kroku se můžete rozhodnout, co dál.

Příklad: analýza požadavků na kalkulačku pojistného ve třech krocích.

```text
Krok 1
Role: Jsi test analytik pojišťovny.
Instruction: Projdi požadavky na kalkulačku pojistného níže a vypiš všechna
místa, která jsou nejednoznačná, neúplná nebo si odporují.
Input data: <požadavky REQ-01 až REQ-14>
Output format: Tabulka: ID požadavku, problém, návrh otázky pro analytika.
```

Tester výsledek projde. Dvě nalezené „nejednoznačnosti“ jsou ve skutečnosti v pořádku, a tak je vyškrtne. Ke třem dalším doplní odpověď od business analytika. Teprve potom pokračuje.

```text
Krok 2
Instruction: Zde jsou požadavky doplněné o odpovědi analytika. Navrhni
z nich testovací podmínky.
Input data: <opravené požadavky a odpovědi>
Output format: Tabulka: ID podmínky, popis, vazba na požadavek.
```

```text
Krok 3
Instruction: Zkontroluj, zda testovací podmínky pokrývají všechny požadavky
REQ-01 až REQ-14. Vypiš požadavky bez pokrytí a navrhni pro ně chybějící
podmínky.
Input data: <podmínky z kroku 2 po kontrole testerem>
```

Řetězení má dvě podstatné vlastnosti. Úloha je rozdělená na kroky, a mezi kroky je ověření. Bez ověření jde jen o dlouhý rozhovor. Sylabus výslovně mluví o kontrole výsledku před dalším krokem, buď ruční, nebo automatické (například skript, který zkontroluje, že JSON z kroku 1 má všechna povinná pole).

:::pojem term="prompt chaining"
Řetězení promptů. Úloha se rozloží na posloupnost dílčích promptů. Výstup každého kroku se zkontroluje a upraví a teprve pak slouží jako vstup dalšího kroku.
:::

#### Meta prompting

**Meta prompting** využívá schopnost modelu vytvořit nebo vylepšit vlastní prompty. V opakovaném cyklu model navrhne prompt, tester ho posoudí a upraví a model ho podle toho dál zpřesní. Technika těží z toho, že model „ví“, jak vypadají dobře optimalizované prompty. Sylabus uvádí dvě výhody. Šetří ruční práci při návrhu promptů, takže se hodí, když záleží na efektivitě a optimalizaci promptu. A pomáhá testerovi, který si neví rady, jak účinný prompt napsat, protože ho může s modelem vytvořit společně.

```text
Potřebuji prompt pro analýzu reportu z regresního testování. Report je export
z nástroje pro správu testů (CSV, asi 800 řádků). Chci z něj získat seskupení
podobných selhání, porovnání se seznamem známých anomálií a návrh, co reportovat
jako nový defekt.

Napiš mi pro to strukturovaný prompt se šesti částmi: role, kontext, instrukce,
vstupní data, omezení, formát výstupu. Než ho napíšeš, polož mi otázky na
informace, které ti chybí.
```

Model se zeptá třeba na sloupce CSV, na formát seznamu známých anomálií a na to, kdo bude výstup číst. Po odpovědích navrhne prompt. Tester ho vyzkouší, výsledek posoudí a vrátí modelu připomínky. Cyklus se opakuje, dokud prompt nedává dobré výsledky.

Sylabus tuto spolupráci popisuje jako formu **pairing** (párové práce) s nástrojem GenAI. Tester a AI interaktivně pracují na společném cíli, podobně jako dva lidé při párovém programování nebo párovém testování. Přínosem je nejen produktivita, ale i učení: tester vidí, jak model prompt staví, a příště ho napíše lépe sám.

:::pojem term="meta prompting"
Technika, při které LLM navrhuje nebo vylepšuje prompt a tester ho posuzuje a upravuje. Probíhá v opakovaném cyklu. Je to forma párové práce testera s AI.
:::

:::nad-ramec
Kurz Podraza v jedné lekci popisuje meta prompting jako „instrukce, jak má model přemýšlet, než odpoví“. To je jiná technika, blízká **chain-of-thought** (řetězec úvah), kdy model požádáte, aby postupoval krok za krokem. Pro zkoušku platí definice ze sylabu: meta prompting je tvorba nebo vylepšení promptu pomocí modelu. Chain-of-thought sylabus nezmiňuje a kurz Shetty AI Tools ji ukazuje jako samostatnou techniku. Pokud ji ve zkoušce uvidíte jako možnost, nebude to správná odpověď na otázku o meta promptingu.
:::

#### Kombinace technik

Techniky se nevylučují. Sylabus uvádí, že je lze s výhodou kombinovat, a v oddílu 2.2.5 dává příklad. Meta promptingem vznikne první verze promptu. Ta obsahuje příklady, které tester upraví a doplní, takže se prompt mění ve few-shot. Úlohu nakonec rozdělí na menší kroky, aby mohl mezivýsledky ověřit, a tím použije prompt chaining.

#### Jak techniky rozpoznat

Praktický cíl **HO-2.1.2b (H1)** chce, abyste v daném promptu poznali použitou techniku. Stačí hledat několik znaků.

| Co v zadání vidíte | Technika |
|---|---|
| Prompt bez ukázky výstupu | zero-shot |
| Právě jedna ukázka vstupu a výstupu | one-shot |
| Dvě a víc ukázek, nový vstup na konci | few-shot |
| Řada promptů, výstup jednoho je vstupem dalšího, mezi nimi kontrola | prompt chaining |
| Model píše nebo vylepšuje prompt, tester ho posuzuje | meta prompting |

Tabulka shrnuje jen rozpoznávací znaky. Kdy kterou techniku použít, řeší oddíl 2.2.5.

Praktický cíl **HO-2.1.2a (H0)** je ukázka všech tří základních technik na testovacích úlohách a diskuse o tom, jak každá přispívá k přesnosti a úplnosti výstupu.

:::zkouska
Distraktory v otázkách k 2.1.2 obvykle prohodí definice. „Few-shot rozkládá úlohu na kroky“ patří k řetězení. „Prompt chaining poskytuje příklady“ patří k few-shot. „Meta prompting ladí prompty ručně bez modelu“ je špatně, podstatou je, že prompt navrhuje nebo vylepšuje model. „Meta prompting spoléhá jen na prompty napsané testerem“ je také špatně. Správná možnost bývá ta, kde sedí všechny tři definice zároveň.
:::

### 2.1.3 Systémový prompt a uživatelský prompt

Při práci s LLM se uplatňují dva druhy promptů. Každý má jiný účel a jinak tvaruje konverzaci.

**System prompt** (systémový prompt) obvykle definuje vývojář nebo tester, který nástroj staví. Určuje celkové chování modelu. Ve většině rozhraní ho uživatel chatbota nevidí a nemůže ho měnit. Sylabus ho popisuje jako předem definovanou sadu pokynů, která určuje chování modelu, jeho „osobnost“ a **operational parameters** (provozní parametry). Provozní parametry říkají, jak má model odpovídat: formálním tónem, stručně, podle pravidel dané domény, nebo bez určitého chování. Systémový prompt platí pro celou konverzaci a během ní se nemění. Může obsahovat části strukturovaného promptu, nejčastěji roli, kontext a omezení.

:::pojem term="system prompt"
Systémový prompt. Pokyny, které nastavuje vývojář nebo tester nástroje. Platí po celou konverzaci, určují roli, tón, pravidla a omezení modelu a uživatel je obvykle nevidí.
:::

Příklad systémového promptu pro interního asistenta testerů v bance:

```text
Jsi asistent testerů v bance. Odpovídej česky, věcně a formálně.
Používej terminologii ISTQB (testovací podmínka, testovací případ, defekt,
selhání). Když si nejsi jistý, řekni to a nic nedomýšlej.
Nepracuj s osobními údaji klientů. Pokud je uživatel vloží, upozorni ho
a dál s nimi nepracuj.
Testovací případy vždy vracej ve formátu: ID, předpoklady, kroky,
očekávaný výsledek.
```

**User prompt** (uživatelský prompt) je skutečný vstup nebo otázka uživatele chatbota. Mění se s každou interakcí. Obsahuje konkrétní instrukce, otázky nebo úlohy, které má model právě vyřešit. Na rozdíl od systémového promptu ho uživatel vidí a tvoří bezprostřední kontext každé odpovědi.

:::pojem term="user prompt"
Uživatelský prompt. Konkrétní dotaz nebo úloha, kterou uživatel zadává v dané interakci. Mění se s každou zprávou a je viditelný.
:::

Uživatelské prompty ve stejné konverzaci mohou vypadat takto:

```text
Navrhni testovací případy pro změnu limitu platební karty. Limit lze nastavit
od 0 do 200 000 Kč po tisících.
```

```text
Teď ke stejné funkci přidej negativní testovací případy pro nečíselné vstupy.
```

Model při každé odpovědi bere v úvahu oba prompty zároveň: neměnný systémový a aktuální uživatelský. Proto asistent výše vrátí testovací případy ve formátu ID, předpoklady, kroky, očekávaný výsledek, i když o to uživatel v dotazu nežádá.

Typický postup je tento: systémový prompt se nastaví jednou na začátku konverzace a pak přicházejí jednotlivé uživatelské prompty. Sylabus k tomu dává dvě doporučení. Systémový prompt má být jasný a konkrétní, pokud jde o roli modelu a omezení. Může obsahovat i kontext a obecné pokyny, například k očekávanému výstupu. Uživatelské prompty mají být zaměřené a dobře strukturované, s explicitní instrukcí, dalším relevantním kontextem a pokyny k formátu výstupu.

| Vlastnost | System prompt | User prompt |
|---|---|---|
| Kdo ho píše | vývojář nebo tester nástroje | uživatel chatbota |
| Platnost | celá konverzace, nemění se | jedna interakce, mění se |
| Viditelnost pro uživatele | obvykle skrytý | viditelný |
| Typický obsah | role, kontext, omezení, tón, obecná pravidla výstupu | konkrétní úloha, vstupní data, upřesnění formátu |
| Funkce | rámec pro celou konverzaci | bezprostřední zadání odpovědi |

Tabulka ukazuje, že komponenty strukturovaného promptu se mezi oba druhy dělí. Co platí pořád, patří do systémového promptu. Co se mění s úlohou, patří do uživatelského.

:::praxe
Šmoula, Janův agent nad Claude Code, je dobrý příklad rozdělení. Pravidla, která platí pro každou zprávu z Telegramu (kdo je uživatel, v jakém jazyce odpovídat, co agent nesmí dělat), patří do systémového promptu, případně do konfiguračního souboru, který nástroj přidává k systémovému promptu. Text zprávy z Telegramu je uživatelský prompt. Když se agent chová v každé konverzaci stejně špatně, je chyba nejspíš v systémovém promptu. Když selže jen u jednoho dotazu, je chyba spíš v tom dotazu.
:::

:::nad-ramec
V API se systémový prompt předává odděleně od zpráv uživatele. V Anthropic API je to parametr `system`, v OpenAI API zpráva s rolí `system` nebo `developer`. Zjednodušená ukázka v Pythonu:

```python
from anthropic import Anthropic

client = Anthropic()  # klíč se čte z proměnné prostředí ANTHROPIC_API_KEY
odpoved = client.messages.create(
    model="<název modelu>",
    max_tokens=1500,
    system="Jsi asistent testerů. Odpovídej česky a používej terminologii ISTQB.",
    messages=[{"role": "user", "content": "Navrhni testovací podmínky pro filtr faktur podle ceny."}],
)
print(odpoved.content[0].text)
```

Klíč patří do proměnné prostředí nebo do trezoru, nikdy přímo do kódu.
:::

:::zkouska
Hlavní funkcí systémového promptu je dát rámec chování modelu pro celou konverzaci. Distraktory mu přisuzují vlastnosti uživatelského promptu: že se mění s každou interakcí, že nese konkrétní otázku uživatele nebo že je pro uživatele viditelný. Pozor na slovo „obvykle“: sylabus říká, že uživatel systémový prompt *ve většině rozhraní* nevidí. Vývojář, který nástroj staví, ho samozřejmě vidí a píše.
:::

## 2.2 Použití technik prompt engineeringu v testovacích úlohách

:::lo
GenAI-2.2.1 (K3) Apply generative AI to test analysis tasks
GenAI-2.2.2 (K3) Apply generative AI to test design and test implementation tasks
GenAI-2.2.3 (K3) Apply generative AI to automated regression testing
GenAI-2.2.4 (K3) Apply generative AI to test monitoring and control task
GenAI-2.2.5 (K3) Select and apply appropriate prompting techniques for a given context and test task
:::

Sylabus jmenuje testovací úlohy, se kterými může GenAI pomoci: testovací analýza, návrh testů, automatizace testů, prioritizace testovacích případů, detekce defektů, analýza pokrytí a monitoring a řízení testování. Kombinací technik z oddílu 2.1.2 lze prompty přizpůsobit konkrétním cílům testování, takže výstupy jsou přesnější, relevantnější a účinnější. Sylabus k tomu přidává větu, která se v oddílu 2.2 opakuje v různých podobách: kvalitní vstup je pro smysluplné výsledky GenAI nezbytný.

Oddíl 2.2 má pět pododdílů a každý má jeden K3 cíl. První čtyři odpovídají testovacím činnostem, které znáte z CTFL. Pátý učí vybrat techniku promptování.

### Jak řešit K3 otázky v oddílu 2.2

K3 znamená aplikovat. Otázka nechce definici, ale rozhodnutí v konkrétní situaci. V CT-GenAI mají K3 otázky několik opakujících se tvarů:

1. **Vyber nejlepší prompt.** Čtyři varianty strukturovaného promptu se liší v jedné nebo dvou komponentách. Hledáte tu, kde je každá komponenta konkrétní a slouží cíli ze zadání.
2. **Vyber nejlepší úpravu promptu.** Dostanete návrh promptu a čtyři možné úpravy. Hledáte úpravu, která míří na skutečnou slabinu a přímo podporuje cíl.
3. **Vyber správné pořadí kroků.** Dostanete seznam kroků řetězení a varianty jejich pořadí nebo výběru. Hledáte posloupnost, kde každý krok staví na ověřeném výsledku předchozího a kde nechybí ani nepřebývá žádný krok podle zadání.
4. **Vyber techniku.** Popis úlohy a výběr z technik promptování. Hledáte znaky úlohy z tabulky v oddílu 2.2.5.

Postup řešení je ve všech případech podobný.

1. Přečtěte si cíl. Je obvykle v první nebo poslední větě zadání („cílem je, aby metriky byly srozumitelné pro vedení“, „cílem je zajistit pokrytí všech akceptačních kritérií“).
2. Určete testovací činnost. Analýza hledá *co testovat*, návrh testů *jak testovat*, implementace připravuje testware ke spuštění, monitoring a řízení sleduje postup a reaguje na odchylky.
3. Projděte šest komponent. U každé se zeptejte, jestli je konkrétní a jestli slouží cíli.
4. Vyřaďte možnosti, které jsou obecné („použij osvědčené postupy“), které cíl rozšiřují nebo zužují („zaměř se jen na hraniční případy“, když se chce úplnost), nebo které přidávají něco, co s úlohou nesouvisí.
5. Ze zbylých vyberte tu, která přidává nejvíc konkrétní informace přesně tam, kde prompt selhává.

Dvě obecné zásady pomáhají skoro vždy. Úprava v instrukci nebo formátu výstupu, která přesně popisuje požadovaný výsledek, bývá silnější než úprava role. A úprava, která jen opakuje to, co už v promptu je, jinými slovy, správná nebývá.

### 2.2.1 Testovací analýza s GenAI

Testovací analýza (test analysis) odpovídá na otázku *co testovat*. Tester v ní analyzuje testovací bázi, identifikuje testovací podmínky a určuje jejich prioritu. GenAI může testovací analýzu podpořit tím, že generuje a prioritizuje testovací podmínky, hledá defekty v testovací bázi a pomáhá s analýzou pokrytí.

Vstupní data pro tyto úlohy jsou požadavky, uživatelské scénáře, technické specifikace, wireframy uživatelského rozhraní a další relevantní informace. Výstupem jsou typické pracovní produkty testovací analýzy, například prioritizované testovací podmínky. Sylabus jako příklad testovacích podmínek uvádí akceptační kritéria.

:::pojem term="test condition"
Testovací podmínka. Testovatelný aspekt komponenty nebo systému, který je cílem testování. Vzniká v testovací analýze z testovací báze.
:::

:::pojem term="acceptance criteria"
Akceptační kritéria. Podmínky, které musí výsledek implementace uživatelského scénáře splnit, aby jej zainteresované strany přijaly. V CT-GenAI je sylabus uvádí jako příklad testovacích podmínek, které GenAI pomáhá vytvořit.
:::

Sylabus popisuje pět typických úloh. Ke každé následuje ukázkový prompt.

#### Hledání potenciálních defektů v testovací bázi

GenAI umí analyzovat testovací bázi a hledat nekonzistence, nejednoznačnosti a neúplné informace, které by mohly vést k defektům. Porovnává podobné vzory požadavků nebo využívá znalosti z dřívějších reportů o defektech. Na tomto základě označí možné anomálie a navrhne zlepšení. Je to obdoba revize, kterou znáte ze statického testování v CTFL.

```text
Role: Jsi test analytik pojišťovny se zkušeností s revizemi požadavků.
Context: Pojišťovna připravuje online kalkulačku povinného ručení. Požadavky
napsal produktový tým a projdou revizí před začátkem vývoje.
Instruction: Najdi v požadavcích nejednoznačnosti, rozpory a chybějící
informace, které by mohly vést k defektům.
Input data:
REQ-01 Pojistné se počítá z objemu motoru a věku řidiče.
REQ-02 Řidiči do 25 let mají přirážku.
REQ-03 Řidiči nad 25 let mají základní sazbu.
REQ-04 Výsledek se zobrazí rychle.
Constraints: U každého nálezu uveď, proč může vést k defektu. Nehodnoť styl
textu, jen obsah.
Output format: Tabulka: ID požadavku, typ problému (nejednoznačnost /
rozpor / neúplnost), popis, otázka pro autora.
```

Dobrý model najde aspoň tyto věci. Řidič přesně 25letý nespadá ani pod REQ-02, ani pod REQ-03. REQ-02 neříká, jak velká je přirážka. REQ-04 nemá měřitelné kritérium („rychle“). REQ-01 neříká nic o elektromobilech, které objem motoru nemají. Tester každý nález posoudí. Model může označit i věc, která problémem není, a výsledek proto nesmí jít autorovi požadavků bez kontroly.

#### Generování testovacích podmínek z testovací báze

LLM umí analyzovat požadavky a uživatelské scénáře a generovat z nich testovací podmínky. Díky zpracování přirozeného jazyka interpretuje význam požadavku a rozloží ho na měřitelná, testovatelná tvrzení.

```text
Role: Jsi test analytik e-shopu.
Context: E-shop s elektronikou zavádí doručení na výdejní místo.
Instruction: Z uživatelského scénáře a akceptačních kritérií odvoď testovací
podmínky. Každá podmínka musí být samostatně ověřitelná.
Input data:
Jako zákazník chci vybrat výdejní místo na mapě, abych si zásilku vyzvedl
v blízkosti domova.
AC1: Zákazník vidí výdejní místa do 10 km od zadané adresy.
AC2: Výdejní místo nelze vybrat pro zásilku těžší než 15 kg.
AC3: Vybrané místo se zobrazí v rekapitulaci objednávky.
Constraints: Ke každému AC aspoň jedna pozitivní a jedna negativní podmínka.
Output format: Seznam: TP-xx, popis, vazba na AC.
```

#### Prioritizace testovacích podmínek podle rizika

Když má model informaci o pravděpodobnosti a dopadu selhání u každé testovací podmínky, pomůže prioritizovat testovací úsilí. Sylabus zdůrazňuje, že model má vzít v úvahu regulatorní požadavky, funkce, se kterými přichází do styku uživatel (přihlášení, platby), a historická data o defektech. Bez těchto informací model prioritu jen odhaduje podle obecných zkušeností.

```text
Role: Jsi test manažer v bance.
Context: Release mobilního bankovnictví za 3 týdny. Regulátor vyžaduje silné
ověření klienta u plateb.
Instruction: Seřaď testovací podmínky podle úrovně rizika a navrhni prioritu.
Input data: Tabulka 18 testovacích podmínek se sloupci ID, popis,
pravděpodobnost selhání (1–5), dopad (1–5), počet defektů v posledních
třech releasech.
Constraints: Úroveň rizika = pravděpodobnost × dopad. Podmínky související
s regulatorními požadavky dostanou nejméně prioritu „vysoká“ bez ohledu
na výpočet. U každé priority uveď jednu větu zdůvodnění.
Output format: Tabulka: pořadí, ID, úroveň rizika, priorita, zdůvodnění.
```

Prompt dává modelu přesné pravidlo výpočtu. Model tedy nemusí hádat, co je riziko, a tester může každý řádek přepočítat. To je důležité, protože modely se při počítání mohou splést (chyby v uvažování řeší kapitola 3).

#### Podpora analýzy pokrytí

Mapováním požadavků a uživatelských scénářů na testovací podmínky může LLM provést analýzu pokrytí (coverage analysis) a zjistit, zda jsou pokryty všechny aspekty testovací báze. Sylabus to doporučuje hlavně u projektů se složitými požadavky, kde mezery v pokrytí vedou k defektům, které uniknou do produkce.

```text
Instruction: Porovnej seznam požadavků a seznam testovacích podmínek.
Pro každý požadavek uveď, které podmínky ho pokrývají. Vypiš požadavky
bez pokrytí a části požadavků, které pokryté nejsou.
Input data: <42 požadavků na modul pojistných událostí> <96 testovacích podmínek>
Constraints: Za pokrytí považuj jen přímou vazbu na obsah požadavku, ne
podobnost slov. Když si nejsi jistý, označ vazbu jako „k ověření“.
Output format: Matice trasovatelnosti: požadavek × podmínky, poslední sloupec
stav (pokryto / částečně / nepokryto / k ověření).
```

#### Návrh technik testování

GenAI může podle typu požadavku navrhnout vhodné techniky testování, například analýzu hraničních hodnot nebo rozdělení tříd ekvivalence. Testerovi to pomáhá použít pro konkrétní testovací podmínky nejúčinnější techniku.

```text
Instruction: Pro každý z následujících požadavků navrhni nejvhodnější techniku
testování černé skříňky a krátce zdůvodni proč.
Input data:
R1 Splatnost faktury je 7 až 90 dní od data vystavení.
R2 Sazba DPH je 0 %, 12 % nebo 21 %.
R3 Sleva závisí na kombinaci věrnostního programu, výše objednávky
   a typu zákazníka.
R4 Objednávka prochází stavy nová, zaplacená, odeslaná, doručená, stornovaná.
Output format: Tabulka: požadavek, technika, zdůvodnění.
```

Očekávaná odpověď: R1 analýza hraničních hodnot, R2 rozdělení tříd ekvivalence, R3 rozhodovací tabulka, R4 testování přechodů stavů. Pokud model navrhne něco jiného, je to dobrá příležitost zkontrolovat, jestli se nemýlí model, nebo jestli není požadavek napsaný nejasně.

#### Kvalita vstupu rozhoduje

Sylabus uzavírá výčet větou, kterou se vyplatí znát: kvalita a relevance vstupů, které model dostane, přímo ovlivňuje správnost a přesnost výstupu. Model, který nedostane informaci o riziku, nemůže dobře prioritizovat. Model, který nevidí wireframe, neodhalí rozpor mezi wireframem a textem požadavku.

:::praxe
V projektu `uctenky` platí pravidlo, že se osoby nemažou: `DELETE` osobu jen skryje a `PUT` skryje původní záznam a založí nový. Kdo dá modelu jen text uživatelského scénáře „jako uživatel chci upravit údaje osoby“, dostane podmínky pro obyčejnou editaci. Kdo do vstupních dat přidá i toto pravidlo, dostane podmínky, které skutečně testují riziko: stará faktura dál ukazuje původní údaje, upravená osoba má nové ID a v seznamu se přesune na konec, skrytá osoba se ve výpisu neobjeví. Tady je přímo vidět, jak kvalita vstupu mění výstup.
:::

#### HO-2.2.1a: multimodální prompt s wireframem

Praktický cíl **HO-2.2.1a (H2)** je cvičení, ve kterém se píše strukturovaný **multimodal prompt** (multimodální prompt), tedy prompt s textem i obrázkem. Cílem je vygenerovat kvalitní akceptační kritéria, tedy dobře formulovaná, jasná a úplná, z uživatelského scénáře a wireframu obrazovky. Do promptu lze přidat další text, například omezení vstupních polí nebo obchodní pravidla pro zpracování dat. Výsledky se porovnávají, aby bylo vidět, jak různé formulace komponent ovlivní výsledek.

```text
Role: Jsi test analytik internetového bankovnictví.
Context: Banka přidává obrazovku pro nastavení trvalého příkazu.
Instruction: Napiš akceptační kritéria pro uživatelský scénář. Využij
přiložený wireframe obrazovky a obchodní pravidla.
Input data:
- Uživatelský scénář: Jako klient chci založit trvalý příkaz, abych
  nemusel každý měsíc ručně platit nájem.
- Obrázek: wireframe-trvaly-prikaz.png (pole účet příjemce, částka,
  frekvence, den splatnosti, datum první a poslední platby, tlačítko Uložit)
- Pravidla: částka 1 až 1 000 000 Kč; den splatnosti 1 až 28; datum první
  platby nejdříve zítra.
Constraints: Kritéria piš jen pro prvky, které jsou na wireframu nebo
v pravidlech. Pokud wireframe a pravidla nesouhlasí, platí pravidla
a rozpor vypiš zvlášť.
Output format: Akceptační kritéria ve tvaru Given-When-Then, číslovaná AC1,
AC2…; pod nimi seznam rozporů a nejasností.
```

Na wireframu může být například pole „datum poslední platby“, o kterém pravidla nic neříkají. Dobrý výsledek ho vypíše jako nejasnost a nevymyslí pro něj pravidlo. Omezení o prioritě zdrojů je přesně ten typ informace, který model sám nezná.

#### HO-2.2.1b: řetězení a lidské ověření při zpřesňování akceptačních kritérií

Praktický cíl **HO-2.2.1b (H2)** procvičuje řetězení promptů při analýze uživatelského scénáře a zpřesňování akceptačních kritérií. Sylabus určuje tři kroky v pevném pořadí: nejprve identifikovat nejednoznačnosti, pak posoudit testovatelnost a nakonec posoudit úplnost. Po každém kroku tester výsledek ručně ověří a podle potřeby opraví, buď přímo, nebo dalším promptem. Další krok tak pracuje s „čistým“ výsledkem předchozího.

```text
Krok 1 (nejednoznačnosti)
Role: Jsi test analytik e-shopu.
Instruction: Najdi v uživatelském scénáři a akceptačních kritériích
nejednoznačné formulace. U každé navrhni jednoznačnou variantu.
Input data:
Jako registrovaný zákazník chci uložit košík na později, abych mohl nákup
dokončit jindy.
AC1: Uložený košík se zákazníkovi zobrazí po přihlášení.
AC2: Uložený košík vyprší po nějaké době.
AC3: Ceny v uloženém košíku jsou aktuální.
Output format: Tabulka: AC, problém, návrh nové formulace.
```

Tester z výsledku převezme formulace, se kterými souhlasí („košík vyprší po 30 dnech“ potvrdí product owner), a zbytek opraví.

```text
Krok 2 (testovatelnost)
Instruction: Zde jsou upravená akceptační kritéria. U každého posuď, zda je
testovatelné: má jasný předpoklad, akci a ověřitelný výsledek? Netestovatelná
kritéria přepiš.
Input data: <kritéria po kontrole z kroku 1>
Output format: Tabulka: AC, testovatelné ano/ne, důvod, přepis.
```

```text
Krok 3 (úplnost)
Instruction: Posuď, zda upravená kritéria pokrývají scénář úplně. Navrhni
chybějící kritéria, například pro zboží, které mezitím zmizelo ze skladu,
nebo pro zákazníka s více zařízeními.
Input data: <kritéria po kontrole z kroku 2>
Output format: Seznam nových AC s krátkým zdůvodněním.
```

Cvičení ukazuje hlavní výhodu řetězení: složitá úloha se rozdělí na menší, a člověk ověří každý mezivýsledek. Kdyby všechny tři kroky byly v jediném promptu, chyba z prvního kroku by se tiše přenesla do dalších.

#### Řešený příklad K3: testovací analýza

Zadání (vlastní, ve stylu zkoušky): Tým e-shopu dostal nové požadavky na věrnostní program. Požadavky zatím nikdo nerevidoval a product owner sám říká, že v nich jsou nejasnosti. Úkolem je s pomocí GenAI a řetězení promptů připravit prioritizované testovací podmínky. Která posloupnost je nejvhodnější?

- A: Prompt 1 odvodí testovací podmínky z požadavků. Prompt 2 podmínky seřadí podle rizika. Výsledek se předá týmu.
- B: Prompt 1 najde v požadavcích nejednoznačnosti a rozpory. Tester nálezy ověří a vyjasní s product ownerem. Prompt 2 odvodí testovací podmínky z opravených požadavků. Tester je zkontroluje. Prompt 3 je seřadí podle rizika s využitím dodaných údajů o pravděpodobnosti a dopadu.
- C: Jeden prompt požádá o nalezení nejasností, odvození testovacích podmínek a jejich seřazení podle rizika najednou.
- D: Prompt 1 najde nejednoznačnosti. Prompt 2 z původních, neopravených požadavků vygeneruje testovací případy s kroky. Prompt 3 je seřadí podle rizika.

Správná je B. Začíná krokem, který situace vyžaduje (požadavky obsahují nejasnosti), a mezi kroky je lidské ověření. A vynechá hledání defektů v testovací bázi, takže nejasnosti se přenesou do podmínek. C není řetězení, všechno je v jednom promptu bez kontroly mezivýsledků. D sice nejasnosti najde, ale nepoužije je a navíc přeskočí od analýzy rovnou k testovacím případům, což je návrh testů. Kdyby zadání naopak říkalo, že požadavky už revizí prošly, první krok by byl zbytečný.

:::zkouska
U otázek k 2.2.1 si hlídejte hranici mezi testovací analýzou a návrhem testů. Testovací analýza vytváří testovací podmínky, prioritizuje je, hledá defekty v testovací bázi a kontroluje pokrytí. Testovací případy s kroky a očekávanými výsledky už jsou návrh testů. Pokud zadání říká, že něco už bylo uděláno (revize požadavků, prioritizace), správná odpověď tento krok neopakuje.
:::

### 2.2.2 Návrh testů a implementace testování s GenAI

Sylabus odkazuje na definice z CTFL. Návrh testů (test design) zahrnuje rozpracování a zpřesnění testovacích podmínek do testovacích případů a dalšího testwaru. Implementace testování (test implementation) zahrnuje vytvoření nebo získání testwaru potřebného pro provedení testů.

:::pojem term="test design"
Návrh testů. Činnost, ve které se testovací podmínky rozpracují do testovacích případů a dalšího testwaru. Odpovídá na otázku „jak testovat“.
:::

:::pojem term="test case"
Testovací případ. Sada předpokladů, vstupů, akcí, očekávaných výsledků a následných podmínek vytvořená na základě testovacích podmínek.
:::

S podporou GenAI lze vytvářet, prioritizovat a řadit do harmonogramu provedení testů manuální testy i automatizované testovací skripty. GenAI může tuto velkou skupinu činností výrazně podpořit, protože pomáhá vytvářet a hodnotit různý testware: testovací případy, testovací data, testovací skripty a testovací prostředí. Sylabus uvádí čtyři typické úlohy.

#### Generování testovacích případů

Díky zpracování přirozeného jazyka vytváří GenAI návrhy testovacích případů z funkčních i nefunkčních požadavků. Když model dostane vhodné informace, navrhne předpoklady, vstupy, očekávané výsledky a kritéria pokrytí. Vzniknou testovací případy pro různé cíle testování, od základního ověření funkce po složité end-to-end testy. Sylabus mluví o „draft test cases“, tedy o návrzích. Tester je musí projít.

```text
Role: Jsi test analytik webových aplikací.
Context: Aplikace uctenky eviduje osoby a faktury. Faktura má pole
invoiceNumber (unikátní), seller, buyer, issued, dueDate, product,
price (max 10 číslic, 2 desetinná místa) a vat.
Instruction: Navrhni testovací případy pro založení faktury přes formulář.
Input data:
TP-01 Fakturu s vyplněnými povinnými poli lze uložit.
TP-02 Duplicitní číslo faktury se odmítne.
TP-03 Cena se ukládá na dvě desetinná místa.
TP-04 Odběratel a dodavatel se vybírají z existujících osob.
Constraints: Ke každé testovací podmínce aspoň jeden pozitivní a jeden
negativní testovací případ. Nevymýšlej validace, které nejsou v podkladech;
pokud by validace dávala smysl a chybí, uveď ji jako otázku.
Output format: Tabulka: ID, vazba na TP, předpoklady, kroky, vstupní data,
očekávaný výsledek.
```

#### Syntéza testovacích dat

GenAI umí vytvořit reprezentativní syntetická testovací data, která chrání soukromí a podobají se produkčním datům. Pokrývají i extrémní situace a různé testovací podmínky. Hodí se pro funkční i nefunkční testování. Data lze přizpůsobit požadavkům aplikace a simulovat realistické situace bez odhalení citlivých informací.

:::pojem term="test data"
Testovací data. Data potřebná k provedení testů. GenAI je umí syntetizovat tak, aby připomínala produkční data, ale neobsahovala skutečné osobní údaje.
:::

```text
Role: Jsi specialista na testovací data v bance.
Instruction: Vygeneruj 30 syntetických záznamů klientů pro testování
registrace do internetového bankovnictví.
Constraints:
- Žádné skutečné osoby. Jména kombinuj náhodně. Rodná čísla nepoužívej,
  místo nich vygeneruj fiktivní identifikátor klienta ve tvaru TST-000001.
- 20 platných záznamů, 10 neplatných: prázdné povinné pole, e-mail bez
  zavináče, telefon s písmeny, jméno o délce 101 znaků, věk 17 let.
- U neplatných záznamů uveď, kterou validaci mají spustit.
Output format: CSV se sloupci: id, jmeno, prijmeni, datum_narozeni, id_klienta, email,
telefon, ocekavany_vysledek.
```

Do promptu nikdy nevkládejte skutečná data klientů, ani „jen jako vzor“. Ochranou dat se podrobně zabývá kapitola 3.

#### Generování automatizovaných testovacích skriptů

GenAI umí ze strukturovaných testovacích případů vytvořit manuální testovací procedury i automatizované testovací skripty. Interpretuje kroky testu a převede je do kódu pro různé frameworky automatizace testů. Skripty lze později aktualizovat nebo rozšířit podle nových požadavků.

:::pojem term="test script"
Testovací skript. Posloupnost instrukcí pro provedení testu, obvykle automatizovaná. GenAI ji umí vytvořit ze strukturovaného testovacího případu.
:::

```text
Role: Jsi inženýr automatizace testů, pracuješ s Playwrightem v TypeScriptu.
Context: E2E testy aplikace uctenky používají Page Object Model. Existují
stránkové objekty InvoicesPage a StatisticsPage. Lokátory jsou jen
ve stránkových objektech, testy volají pojmenované metody.
Instruction: Převeď testovací případ níže na test v Playwrightu.
Input data:
TC-07 Filtr minimální ceny
Předpoklad: databáze obsahuje faktury s cenou 500, 1 500 a 3 000 Kč.
Kroky: otevři Faktury, zadej minimální cenu 1 000, potvrď filtr.
Očekávaný výsledek: zobrazí se jen faktury s cenou 1 500 a 3 000 Kč.
Ukázka existujícího testu: <obsah tests/invoices.spec.ts>
Constraints: Nepoužívej lokátory přímo v testu. Pokud metoda ve stránkovém
objektu chybí, napiš ji zvlášť a označ ji. Nepoužívej pevné čekání
(waitForTimeout).
Output format: Kód testu v jednom bloku, pod ním seznam nových metod
stránkového objektu.
```

Tento prompt je mimochodem malý few-shot: ukázka existujícího testu slouží jako příklad stylu. Vygenerovaný kód se musí spustit a projít revizí jako kód od kolegy.

#### Plánování a prioritizace provedení testů

GenAI umí analyzovat testovací případy a jejich vzájemné závislosti a optimalizovat harmonogram provedení testů podle priority, souvisejících rizik, dostupnosti zdrojů a cílů testování.

```text
Instruction: Sestav pořadí provedení testovacích případů pro dnešní den.
Input data: Tabulka 40 testovacích případů: ID, priorita, riziko,
závislost na jiném TC, potřebné prostředí, odhad času.
Constraints: TC se nesmí spustit dřív než TC, na kterém závisí. Prostředí
UAT je dostupné jen 9:00–13:00. Kapacita dva testeři po 6 hodinách.
Output format: Harmonogram: pořadí, ID, tester, čas začátku. Pod ním seznam
TC, které se nevešly, s důvodem.
```

Výstup je návrh. Tester ho zkontroluje, protože model se při kombinaci závislostí, časů a kapacity snadno splete.

#### HO-2.2.2a: testovací případy řetězením, strukturovaným promptem a meta promptingem

Praktický cíl **HO-2.2.2a (H2)** kombinuje tři postupy ve třech krocích. Nejprve strukturovaný prompt vytvoří funkční testovací případy z akceptačních kritérií v zadaném formátu. Ve druhém kroku se ověří úplnost: model vytvoří tabulku, která ukáže, které akceptační kritérium je kterým testovacím případem pokryto. Ve třetím kroku vznikne meta prompt, který pomůže vytvořit end-to-end testovací procedury a postupně se zlepšuje.

```text
Krok 1 (strukturovaný prompt)
Role: Jsi test analytik e-shopu.
Context: Funkce „uložit košík na později“.
Instruction: Vytvoř funkční testovací případy pro akceptační kritéria AC1–AC5.
Input data: <AC1–AC5 z HO-2.2.1b po úpravách>
Output format: ID, název, předpoklady, kroky, očekávaný výsledek, vazba na AC.
```

```text
Krok 2 (kontrola pokrytí)
Instruction: Vytvoř tabulku pokrytí: řádky jsou AC1–AC5, sloupce testovací
případy z předchozí odpovědi. Označ, které AC není pokryto, nebo je pokryto
jen pozitivním případem.
```

```text
Krok 3 (meta prompt)
Chci vytvořit end-to-end testovací procedury, které spojí uložení košíku,
přihlášení z jiného zařízení a dokončení objednávky. Navrhni mi prompt, který
z testovacích případů výše sestaví takové procedury. Prompt by měl obsahovat
všech šest částí struktury. Po mém hodnocení ho uprav.
```

#### HO-2.2.2b: few-shot pro testovací případy v Gherkinu

Praktický cíl **HO-2.2.2b (H2)** používá few-shot prompting pro testovací podmínky a testovací případy ve stylu Gherkin. Postup je tento. Nejprve si projdete připravené příklady a syntaxi Gherkinu. Pak vyberete *n* příkladů, které vložíte do promptu. Každý příklad obsahuje uživatelský scénář, testovací podmínky a očekávané testovací případy ve tvaru given-when-then. Prompt se použije na nový uživatelský scénář. Pokud výsledky nejsou přesné, upraví se prompt nebo příklady.

**Gherkin** je jednoduchý strukturovaný jazyk pro popis scénářů chování. Používá klíčová slova `Feature`, `Scenario`, `Given` (výchozí stav), `When` (akce), `Then` (očekávaný výsledek), případně `And` a `But`.

```text
Role: Jsi test analytik ve finančním týmu.
Instruction: Pro nový uživatelský scénář napiš testovací podmínky a scénáře
v Gherkinu přesně ve stylu příkladů.
Constraints: Jedna testovací podmínka = jeden Scenario. Kroky piš z pohledu
uživatele, ne implementace. Konkrétní hodnoty uváděj v uvozovkách.

Příklad 1
Uživatelský scénář: Jako účetní chci filtrovat faktury podle odběratele.
Testovací podmínky:
  TP1 Filtr vrátí jen faktury vybraného odběratele.
  TP2 Odběratel bez faktur vrátí prázdný seznam.
Gherkin:
  Feature: Filtr faktur podle odběratele
    Scenario: Filtr vrátí faktury vybraného odběratele
      Given existují faktury pro odběratele "Alfa s.r.o." a "Beta a.s."
      When filtruji faktury podle odběratele "Alfa s.r.o."
      Then vidím jen faktury odběratele "Alfa s.r.o."
    Scenario: Odběratel bez faktur
      Given odběratel "Gama s.r.o." nemá žádnou fakturu
      When filtruji faktury podle odběratele "Gama s.r.o."
      Then vidím hlášení "Žádné faktury"

Příklad 2
Uživatelský scénář: Jako účetní chci omezit počet zobrazených faktur.
Testovací podmínky:
  TP1 Limit zobrazí nejvýš zadaný počet faktur.
  TP2 Limit 0 se odmítne.
Gherkin:
  Feature: Limit počtu faktur
    Scenario: Limit omezí počet řádků
      Given existuje 25 faktur
      When nastavím limit "10"
      Then vidím 10 faktur
    Scenario: Nulový limit
      When nastavím limit "0"
      Then vidím chybu "Limit musí být alespoň 1"

Nový uživatelský scénář: Jako účetní chci filtrovat faktury podle rozsahu ceny.
```

Z praxe: pokud model v odpovědi vynechává negativní scénáře, nestačí ho o ně požádat v instrukci. Je lepší přidat negativní scénář do každého příkladu. Few-shot model napodobuje hlavně to, co vidí v příkladech.

:::nad-ramec
Hodnoty v příkladu (hlášení „Žádné faktury“, chyba „Limit musí být alespoň 1“) jsou vymyšlené pro ilustraci. Skutečné texty v aplikaci `uctenky` mohou být jiné. Přesně tohle je riziko few-shot promptu: model převezme i vymyšlené detaily z příkladů a vydává je za fakta. Příklady proto berte ze skutečných, ověřených testů.
:::

#### HO-2.2.2c: řetězení pro prioritizaci testovací sady

Praktický cíl **HO-2.2.2c (H2)** se týká prioritizace testovacích případů v dané testovací sadě s ohledem na analýzu rizik a závislosti mezi testovacími případy. Cvičení začíná krátkým přehledem přístupů k testování: založeného na rizicích, na pokrytí a na požadavcích. Pak účastníci píší prompty, které z dané sady vytvoří proveditelné plány prioritizace podle různých strategií. Výsledek modelu je třeba ručně ověřit, aby se odhalily chyby v jeho uvažování. Jde o úlohu, která vyžaduje uvažování nad více kritérii současně.

```text
Krok 1
Instruction: Z testovací sady vypiš všechny závislosti mezi testovacími
případy jako seznam „TC-A musí proběhnout před TC-B“.
Input data: <testovací sada 30 TC s popisem předpokladů>
```

Tester ověří, že model nevynechal žádnou závislost a žádnou si nevymyslel.

```text
Krok 2
Instruction: Seřaď testovací případy podle rizika (pravděpodobnost × dopad)
od nejvyššího. Dodrž ověřené závislosti z kroku 1.
Input data: <ověřený seznam závislostí> <rizika ke každému TC>
Output format: pořadí, ID, riziko, poznámka, pokud závislost posunula TC
dopředu nebo dozadu.
```

```text
Krok 3
Instruction: Vytvoř alternativní pořadí podle pokrytí požadavků: nejdřív TC,
které pokrývají nejvíc dosud nepokrytých požadavků. Porovnej obě pořadí
a popiš rozdíly.
```

Typická chyba modelu v tomto cvičení: seřadí sadu podle rizika a závislost poruší, protože vysoce rizikový test postaví před test, který pro něj připravuje data. Proto je ověření po kroku 1 a po kroku 2 nutné.

#### Řešený příklad K3: výběr promptu pro návrh testů

Zadání (vlastní): Tester chce pro uživatelský scénář „Jako klient chci změnit PIN k platební kartě“ a jeho čtyři akceptační kritéria vygenerovat testovací případy. Firma má jednotný formát testovacích případů a tester má k dispozici tři schválené testovací případy z jiného projektu v tomto formátu. Cílem je, aby každé akceptační kritérium bylo pokryté a aby výstup šel rovnou importovat do nástroje pro správu testů. Který prompt je nejvhodnější?

- A: Role tester. Instrukce: vygeneruj testovací případy pro scénář. Vstupní data: scénář a kritéria. Omezení: drž se osvědčených postupů. Formát: tabulka.
- B: Role test analytik platebních karet. Instrukce: vygeneruj testovací případy pro scénář tak, aby každé AC pokrýval aspoň jeden pozitivní a jeden negativní případ. Vstupní data: scénář, kritéria a tři schválené testovací případy jako vzor. Omezení: formát přesně podle vzorů, nevymýšlej pravidla mimo kritéria. Formát: CSV se sloupci podle vzorů a sloupec s vazbou na AC.
- C: Role test analytik platebních karet. Instrukce: vygeneruj tři testovací případy zaměřené na hraniční hodnoty PINu. Vstupní data: scénář a tři vzory. Formát: CSV.
- D: Role test analytik platebních karet. Instrukce: navrhni prompt, který by vygeneroval testovací případy. Vstupní data: scénář a kritéria.

Správná je B. Používá few-shot (tři schválené vzory), vyžaduje pokrytí každého kritéria a formát odpovídá importu. A má vágní omezení a nevyužívá vzory. C omezí počet a zaměření tak, že pokrytí všech kritérií nezajistí. D je meta prompting, který by se hodil, kdyby tester nevěděl, jak prompt sestavit. Tady to ví a má vzory.

:::zkouska
U 2.2.2 hledejte, jestli zadání zmiňuje existující příklady (pak few-shot), požadavek na kontrolu po krocích (pak řetězení) nebo nejistotu, jak prompt napsat (pak meta prompting). Hlídejte také slova, která pokrytí nenápadně omezují: „nejvýše dva“, „jen hraniční případy“, „zaměř se na okrajové situace“. Pokud je cílem úplnost, takové omezení dělá z možnosti distraktor.
:::

### 2.2.3 Automatizované regresní testování s GenAI

S každou novou iterací nebo vydáním obvykle roste počet regresních testů. Proto jsou vhodným kandidátem na automatizaci, hlavně v CI/CD pipeline, kde se testy spouštějí velmi často. GenAI může tento proces zjednodušit tím, že pomáhá vytvářet, udržovat a optimalizovat sady automatizovaných regresních testů. Dokáže se přizpůsobit změnám v kódu a provést **impact analysis** (analýzu dopadu), tedy určit, které části softwaru nejspíš ovlivnily poslední změny. Regresní testování se pak soustředí tam, kde je nejvíc potřeba.

:::pojem term="regression testing"
Regresní testování. Testování, které ověřuje, že změna (oprava, nová funkce, změna prostředí) nezpůsobila nežádoucí dopady v dříve fungujících částech systému.
:::

Sylabus uvádí pět činností, které lze podpořit promptováním.

#### Implementace skriptů pro testování řízené klíčovými slovy

V **keyword-driven testing** (testování řízeném klíčovými slovy) představují předem definovaná klíčová slova běžné kroky testu, například `Přihlas uživatele` nebo `Ověř text na stránce`. Testovací skript se skládá z klíčových slov a jejich parametrů. Implementace každého klíčového slova je v knihovně. LLM může klíčová slova namapovat na konkrétní testovací případy, vygenerovat testovací skripty a pomáhat testerům a inženýrům automatizace.

:::pojem term="keyword-driven testing"
Testování řízené klíčovými slovy. Skriptovací technika, při které testovací skripty obsahují klíčová slova vyšší úrovně a jejich implementace je v samostatné knihovně.
:::

Úloha je typicky few-shot: model dostane popis knihovny klíčových slov a dva nebo tři hotové skripty a podle nich napíše další.

```text
Role: Jsi inženýr automatizace testů, pracuješ s Robot Frameworkem.
Context: Regresní sada pro internetové bankovnictví. Používáme jen klíčová
slova z naší knihovny.
Instruction: Napiš testovací skript pro nový testovací případ podle vzorů.
Input data:
Knihovna klíčových slov:
  Přihlas Klienta    ${uživatel}    ${heslo}
  Otevři Sekci    ${název}
  Zadej Platbu    ${účet}    ${částka}    ${zpráva}
  Potvrď Platbu PINem    ${pin}
  Ověř Hlášení    ${text}
  Odhlas Klienta

Vzor 1:
*** Test Cases ***
Platba Na Vlastní Účet
    Přihlas Klienta    test_klient_01    ${HESLO}
    Otevři Sekci    Platby
    Zadej Platbu    2001234567/2010    500    test vlastní
    Potvrď Platbu PINem    ${PIN}
    Ověř Hlášení    Platba byla odeslána
    Odhlas Klienta

Vzor 2:
*** Test Cases ***
Platba Nad Limit
    Přihlas Klienta    test_klient_01    ${HESLO}
    Otevři Sekci    Platby
    Zadej Platbu    2001234567/2010    500001    nad limit
    Ověř Hlášení    Částka překračuje denní limit
    Odhlas Klienta

Nový testovací případ: Platba s prázdným číslem účtu se nesmí odeslat.
Constraints: Používej jen klíčová slova z knihovny. Pokud žádné nevyhovuje,
nevymýšlej ho a napiš, jaké klíčové slovo chybí. Hesla a PIN jen jako proměnné.
Output format: Jeden blok Robot Framework.
```

#### Analýza dopadu a optimalizace testů

GenAI může analyzovat změny v kódu a určit oblasti s vysokým rizikem. Regresní testy pak cílí tam, kde jsou nejvíc potřeba.

```text
Role: Jsi test analytik regresního testování.
Context: Aplikace uctenky, backend Django REST Framework. Plná regresní sada
trvá 40 minut, po každém commitu chceme pustit jen relevantní část.
Instruction: Podle změn v kódu urči ovlivněné oblasti a vyber regresní testy,
které je třeba spustit.
Input data:
- git diff posledního commitu (soubor invoices/views/invoice_views.py,
  funkce monthly_summary)
- Mapa testů: tabulka test → endpoint → soubor
Constraints: Vyber testy jen podle mapy. Pokud změna zasahuje soubor, který
v mapě není, uveď to jako riziko. Vždy přidej smoke testy.
Output format: Seznam vybraných testů se zdůvodněním, pod ním seznam rizik.
```

Mapa testů je podstatná část vstupu. Bez ní model jen hádá podle názvů testů.

#### Samoopravné a adaptivní testy

GenAI lze použít k automatické úpravě testovacích skriptů tak, aby zvládly drobné změny uživatelského rozhraní nebo API. Testy pak nepadají zbytečně kvůli malým úpravám a testovací sady zůstávají dlouhodobě stabilní. Tomuto přístupu se říká **self-healing tests** (samoopravné testy).

:::pojem term="self-healing test"
Samoopravný test. Automatizovaný test, jehož skript se při drobné změně UI nebo API (jiný lokátor, přejmenované pole) automaticky přizpůsobí, aby test zbytečně nepadal.
:::

Samooprava má i rizikovou stránku. Pokud se tlačítko „Odeslat platbu“ změnilo na „Smazat účet“ a test se „opraví“ tak, že klikne na nové tlačítko, test projde a skutečný defekt zůstane skrytý. Každá automatická úprava skriptu proto musí být viditelná a schválená člověkem.

#### Automatizované reportování a přehledy

GenAI umožňuje generovat podrobné a včas dostupné reporty z testování s metrikami úspěšnosti, selháními a hlavními zjištěními. Zainteresované strany dostanou dashboardy, které ukazují trendy testování a nabízejí předpověď míst, kde může dojít k selhání.

:::pojem term="test report"
Report z testování. Dokument nebo přehled s výsledky a hodnocením testování. Patří sem report o postupu prací při testování i souhrnný report z testování.
:::

#### Lepší reporty o defektech a analýza kořenové příčiny

GenAI může automaticky sestavit úplný report o defektu s testovacími logy, snímky obrazovky a údaji o testovacím prostředí. Sylabus v nadpisu zmiňuje i analýzu kořenové příčiny (root cause analysis). Model z logů a stack trace navrhne pravděpodobnou příčinu, kterou pak ověří vývojář.

```text
Instruction: Z logu selhaného testu a snímku obrazovky sestav report
o defektu podle naší šablony a navrhni pravděpodobnou kořenovou příčinu.
Input data: <log z Playwrightu> <stack trace serveru> <snímek>
<šablona reportu o defektu>
Constraints: Odděl fakta z logu od domněnek. Domněnky označ slovem
„hypotéza“.
Output format: Pole šablony: název, prostředí, kroky, očekávaný výsledek,
skutečný výsledek, závažnost, hypotéza kořenové příčiny.
```

:::praxe
V projektu `uctenky` se graf tržeb nikdy nevykreslil. Klient volal adresu `/api/invoices/monthly-summary?year=2025` a funkce `apiGet` k ní připojila další otazník. Server dostal rok `"2025?"` a vracel chybu 500. Kdyby model dostal jen hlášku z klienta („Nepodařilo se načíst data pro graf“), mohl by hádat donekonečna. S logem serveru, kde je vidět hodnota `"2025?"`, najde příčinu během chvíle. Regresní test, který hlídá, že se graf vykreslí, je pak přesně ten typ testu, který patří do automatizované regresní sady.
:::

#### GUI a API regresní testy

Tyto činnosti se uplatní u funkčních i nefunkčních regresních testů. Sylabus ale připomíná, že GenAI dělá chyby. Vygenerovaný výstup je třeba pečlivě kontrolovat, a to tím důkladněji, čím vyšší je související riziko (podrobně kapitola 3).

GenAI pomáhá i u automatizovaných end-to-end regresních testů přes GUI a přes API. Každý typ má jiné potíže. GUI testy bývají nestabilní, protože se uživatelské rozhraní často mění. GenAI umí skripty přizpůsobit dynamickým lokátorům a změněným interakcím a omezit ruční zásahy. API regresní testy řeší měnící se formáty požadavků a odpovědí, endpointy a autentizaci. GenAI umí skripty přizpůsobit vyvíjející se specifikaci API a vygenerovat různorodá testovací data, takže pokrytí zůstává úplné a ruční aktualizace ubývají.

#### HO-2.2.3a: few-shot pro skripty řízené klíčovými slovy

Praktický cíl **HO-2.2.3a (H2)** procvičuje few-shot prompting při tvorbě a správě testovacích skriptů řízených klíčovými slovy pro webovou aplikaci s frameworkem pro automatizaci GUI testů. Cvičení má dvě části. První se věnuje automatizaci: vytvoření dokumentace knihovny klíčových slov, generování prvních skriptů, jejich validaci pomocí AI a rozšíření pokrytí o další skripty. Druhá část se věnuje ladění: pomocí systémového promptu se vytvoří AI asistent, který kontroluje a opravuje testovací skripty.

Systémový prompt takového asistenta může vypadat takto:

```text
Jsi asistent pro kontrolu testovacích skriptů v Robot Frameworku.
Znáš knihovnu klíčových slov uvedenou níže a nic jiného nepoužíváš.
U každého skriptu, který dostaneš:
1. Ověř, že používá jen klíčová slova z knihovny a správný počet argumentů.
2. Ověř, že hesla a PIN jsou jen v proměnných.
3. Najdi kroky bez ověření výsledku.
Vrať seznam nálezů (řádek, problém, oprava) a pod ním opravený skript.
Pokud je skript v pořádku, napiš jen „Bez nálezů“.

Knihovna klíčových slov:
<dokumentace knihovny>
```

Uživatelský prompt pak obsahuje jen skript ke kontrole. Systémový prompt se nemění, dokud se nezmění knihovna.

#### HO-2.2.3b: strukturované prompty pro analýzu reportu z regresního testování

Praktický cíl **HO-2.2.3b (H2)** ukazuje metodický postup analýzy reportů z regresního testování pomocí strukturovaných promptů. Postup začíná analýzou výsledků testů a jejich porovnáním se specifikací testů. Pokračuje seskupením (clustering) podobných defektů, údržbou seznamu známých anomálií (known anomalies list) a křížovou kontrolou zjištění. Všechny kroky jsou propojené v jedné konverzaci s LLM.

```text
Krok 1
Role: Jsi test analytik regresního testování v pojišťovně.
Context: Noční regresní běh modulu pojistných smluv, 640 automatizovaných testů.
Instruction: Projdi výsledky běhu a porovnej je se specifikací testů. Pro každý
neúspěšný test odděl očekávaný a skutečný výsledek a urči, zda jde o selhání
aplikace, chybu testu, nebo problém prostředí.
Input data: <export výsledků CSV> <specifikace testů>
Output format: Tabulka: test, očekávaný výsledek, skutečný výsledek,
kategorie, krátké zdůvodnění.
```

```text
Krok 2
Instruction: Seskup neúspěšné testy z kroku 1 podle pravděpodobné společné
příčiny (stejná chybová hláška, stejný endpoint, stejný krok). U každé skupiny
uveď počet testů a jednu větu, co mají společného.
```

```text
Krok 3
Instruction: Porovnej skupiny se seznamem známých anomálií. Označ, které
skupiny odpovídají známé anomálii, které jsou nové a které známé anomálie
se v tomto běhu neobjevily (mohly být opraveny).
Input data: <seznam známých anomálií s ID a popisem>
```

```text
Krok 4
Instruction: Pro nové skupiny navrhni text reportu o defektu. Aktualizuj
seznam známých anomálií: nové položky přidej, opravené označ k uzavření.
Nakonec křížově zkontroluj, že každý neúspěšný test z kroku 1 je přiřazen
k právě jedné skupině.
Output format: 1) návrhy reportů, 2) aktualizovaný seznam anomálií,
3) výsledek křížové kontroly.
```

Krok 4 končí křížovou kontrolou. Ta odhalí, jestli model nějaký test „ztratil“, což se u dlouhých vstupů stává.

#### Řešený příklad K3: výběr regresních testů

Zadání (vlastní): Regresní sada aplikace pro správu pojistných smluv má 1 200 automatizovaných testů a běží čtyři hodiny. Tým chce, aby GenAI po každém merge requestu vybral jen testy relevantní pro změnu. První verze promptu:

```text
Role: Jsi test analytik.
Context: Regresní sada aplikace pro správu pojistných smluv.
Instruction: Vyber regresní testy, které je třeba spustit po této změně.
Input data: git diff merge requestu.
Constraints: Vyber jen relevantní testy.
Output format: Seznam ID testů.
```

Výsledky jsou nespolehlivé, model vybírá testy podle podobnosti názvů. Která úprava nejlépe zlepší schopnost modelu vybrat správné testy?

- A: Změnit roli na „senior test analytik se zkušeností s pojišťovnictvím“.
- B: Přidat do vstupních dat mapu, která ke každému testu uvádí pokryté moduly a soubory, a do instrukce požadavek vybrat testy podle průniku změněných souborů s mapou.
- C: Doplnit do omezení „vyber nejvýše 100 testů, aby běh netrval déle než 20 minut“.
- D: Změnit formát výstupu na tabulku s ID testu, názvem a odhadovanou dobou běhu.

Správná je B. Problém je v chybějícím vstupu: model nemá z čeho analýzu dopadu udělat. A mění perspektivu, ale nedodá informaci. C omezí počet, ale výběr zůstane stejně náhodný a může vypustit potřebné testy. D změní jen vzhled výsledku.

:::zkouska
K 2.2.3 si pamatujte pět činností: skripty řízené klíčovými slovy, analýza dopadu a optimalizace, samoopravné testy, automatizované reportování a lepší reporty o defektech s analýzou kořenové příčiny. Few-shot je typická technika pro skripty řízené klíčovými slovy, protože jde o opakující se vzor. U otázek na vylepšení promptu pro analýzu reportu hledejte úpravu, která konkretizuje instrukci (co přesně s výsledky udělat), ne úpravu, která jen přejmenuje roli nebo přidá nesouvisející pojmy, třeba Gherkin do analýzy reportu.
:::

### 2.2.4 Monitoring testování a řízení testování s GenAI

Monitoring testování vyžaduje získat velké množství dat, často nestrukturovaných. Data už obvykle leží v nástrojích pro správu testů a GenAI je pomůže analyzovat a syntetizovat. Sylabus uvádí čtyři skupiny úloh.

:::pojem term="test monitoring"
Monitoring testování. Průběžné sledování testovacích činností a porovnávání skutečného postupu s plánem pomocí metrik.
:::

:::pojem term="test control"
Řízení testování. Opatření, která se přijímají na základě monitoringu, aby testování dosáhlo cílů, například změna priorit, harmonogramu nebo zdrojů.
:::

**Monitoring testování a analýza metrik.** GenAI usnadňuje automatizaci monitoringu a analýzu trendů. Umí předpovídat možná rizika a upozornit tým na odchylky od plánu. Tým tak má aktuální informace a může jednat dřív.

**Řízení testování.** GenAI pomáhá s řízením testování tím, že dává podklady pro změnu priorit testů, úpravu harmonogramu a přerozdělení zdrojů. Testování tak zůstává pružné a soustředí se na oblasti s vysokou prioritou.

**Přehledy z dokončení testování a průběžné učení.** GenAI pomáhá vytvářet souhrnné reporty z testování, které zdůrazní úspěchy a poučení. Tým podle nich upraví strategii testování a zlepší další testovací procesy.

**Lepší vizualizace metrik a reportování.** GenAI pomáhá vytvářet dynamické dashboardy a souhrny v přirozeném jazyce. Všechny zainteresované strany tak mají přístup k metrikám, které potřebují, mohou se rychle rozhodnout a vidí jasně postup testování.

#### Příklad: metriky z exportu

Tester má export z nástroje pro správu testů za druhý týden systémového testování bankovní aplikace. Plán na tento týden je 300 testovacích případů, tedy 60 denně. Sloupce s příponou `_kumul` jsou součty od pondělí, sloupce s příponou `_den` jsou denní hodnoty.

```text
den,plán_kumul,provedeno_kumul,prošlo_kumul,selhalo_kumul,blokováno_kumul,nové_defekty_den,uzavřené_defekty_den
po,60,58,50,6,2,5,1
út,120,110,93,12,5,7,3
st,180,151,128,16,7,9,4
čt,240,183,154,19,10,8,6
pá,300,212,177,23,12,6,5
```

Prompt pro monitoring:

```text
Role: Jsi test manažer.
Context: Systémové testování mobilního bankovnictví, druhý týden ze tří.
Plán na tento týden je 300 provedených testovacích případů (60 denně).
Instruction: Spočítej z dat metriky postupu a trend defektů. Porovnej
skutečný postup s plánem, popiš odchylky a navrhni opatření pro řízení
testování.
Input data: <CSV výše>
Constraints: U každého čísla ukaž výpočet. Opatření navrhuj jen na základě
dat; co z dat nevyplývá, označ jako předpoklad.
Output format:
1) tabulka metrik,
2) tři věty pro vedení bez odborného žargonu,
3) seznam navržených opatření s prioritou.
```

Správné výpočty, které by měl model vrátit a tester ověřit:

| Metrika | Výpočet | Výsledek |
|---|---|---|
| Plnění plánu provedení k pátku | 212 / 300 | 70,7 % |
| Podíl prošlých z provedených | 177 / 212 | 83,5 % |
| Podíl blokovaných z provedených | 12 / 212 | 5,7 % |
| Nové defekty za týden | 5 + 7 + 9 + 8 + 6 | 35 |
| Uzavřené defekty za týden | 1 + 3 + 4 + 6 + 5 | 19 |
| Přírůstek otevřených defektů | 35 − 19 | +16 |

Trend je čitelný. Provádění zaostává za plánem a mezera se každý den zvětšuje (−2, −10, −29, −57, −88). Blokovaných testů přibývá. Defekty se otevírají rychleji, než se zavírají. Rozumná opatření pro řízení testování jsou například vyjasnit příčinu blokovaných testů, přesunout kapacitu na oblasti s vysokým rizikem a s vedením projektu probrat posun termínu nebo zúžení rozsahu.

Tabulka slouží ke kontrole. Jazykové modely se při aritmetice umí splést, proto má prompt požadavek „ukaž výpočet“. Ve výuce k tomu slouží praktický cíl **HO-2.2.4 (H0)**: ukázka, jak LLM z dat z testovacích nástrojů vytvoří metriky postupu, trendy defektů a pokrytí, upozorní na rizika a shrne je přirozeným jazykem pro všechny zainteresované strany.

:::nad-ramec
U větších exportů je spolehlivější nechat model napsat skript (například v Pythonu s knihovnou pandas), který metriky spočítá, než ho nechat počítat přímo v textu. Model pak dělá to, v čem je dobrý (napsat kód a interpretovat výsledek), a čísla počítá program.
:::

#### Řešený příklad K3: monitoring

Zadání (vlastní): Test manažerka e-shopu chce, aby LLM každé ráno z exportu výsledků upozornil na odchylky od plánu testování dřív, než se z nich stane problém. Návrh promptu:

```text
Role: Jsi test manažer.
Context: Akceptační testování nové verze e-shopu, 4 týdny.
Instruction: Shrň výsledky testování za včerejšek.
Input data: Export výsledků testů za včerejšek.
Constraints: Stručně a srozumitelně.
Output format: Odstavec textu.
```

Která úprava nejlépe pomůže dosáhnout cíle?

- A: Přidat do vstupních dat plán testování (plánovaný počet provedených testů a vyřešených defektů po dnech) a do instrukce porovnání skutečnosti s plánem a označení odchylek nad 10 %.
- B: Změnit roli na „zkušený test manažer s 15 lety praxe“.
- C: Přidat do formátu výstupu graf s počtem prošlých testů.
- D: Rozšířit omezení na „piš stručně, srozumitelně a profesionálně“.

Správná je A. Odchylku od plánu nelze zjistit bez plánu. Jde o chybějící vstupní data a o instrukci, která neodpovídá cíli (shrnutí ≠ porovnání s plánem). B nepřidává informaci. C zlepší vizualizaci, ale bez plánu stále neukáže odchylku. D jen opakuje existující omezení jinými slovy.

:::zkouska
U 2.2.4 se ptejte, kdo výstup čte a co s ním má udělat. Když je cílem srozumitelnost pro vedení, pomůže úprava formátu výstupu, například souhrn v běžném jazyce s doporučeným dalším postupem. Když je cílem odhalit odchylky, pomůže dodat plán a požádat o porovnání. Úprava, která přidá hodně technických podrobností, může cíl „snadno pochopitelné pro vedení“ naopak zhoršit.
:::

### 2.2.5 Výběr techniky promptování

Sylabus shrnuje, kdy se která ze tří základních technik hodí. Tabulka je převyprávěná vlastními slovy.

| Technika | Doporučené použití | Typické testovací úlohy |
|---|---|---|
| Prompt chaining | složité úlohy, které vyžadují přesnost a lidské ověření po každém kroku | testovací analýza, návrh testů a automatizace, kde se kontroluje funkční správnost každého kroku |
| Few-shot prompting | opakující se úlohy nebo úlohy s konkrétním, omezeným formátem výstupu | testovací případy v Gherkinu, testování řízené klíčovými slovy, reporty z testování s pevným formátem |
| Meta prompting | pružné a dynamické úlohy, tvorba promptů pro nové úlohy | obecný popis cíle a úlohy, podle kterého LLM vytvoří prompt; složité úlohy jako analýza reportů z testování a detekce anomálií |

Tabulka říká, že rozhoduje povaha úlohy. Praktický cíl **HO-2.2.5 (H1)** to formuluje jako otázku: vyžaduje úloha přesnost, nebo opakující se strukturu?

Z tabulky plynou rozpoznávací znaky pro zkoušku:

- **Prompt chaining** poznáte podle slov jako „po krocích“, „ověřit mezivýsledek“, „každý krok zkontrolovat“, „složitá úloha“, „rozdělit na dílčí úlohy“, „výsledek jednoho kroku použít v dalším“.
- **Few-shot** poznáte podle slov „máme vzory“, „existující testovací případy“, „jednotný formát“, „stejný styl“, „opakovaně“, „šablona“, „Gherkin“, „klíčová slova“.
- **Meta prompting** poznáte podle slov „nová úloha“, „nevíme, jak prompt napsat“, „optimalizovat prompt“, „ušetřit čas při návrhu promptu“, „nechat model navrhnout prompt“.
- **Zero-shot** se hodí, když je úloha jednoduchá a běžná a na přesném tvaru nezáleží. Ve výběrových otázkách bývá spíš distraktorem, protože scénáře obvykle obsahují příklady, kroky nebo nejistotu.

Sylabus výslovně uvádí, že pro jeden případ užití lze použít více technik. Meta promptingem vznikne první prompt. Ten může obsahovat příklady, které je třeba upravit a doplnit (few-shot). Nakonec je užitečné rozdělit úlohu na menší dílčí úlohy, aby šlo ověřit mezikroky (prompt chaining).

#### Procvičení: osm situací

Následující situace jsou krátké. U každé je nejvhodnější technika a zdůvodnění.

1. Tým píše každý sprint přes sto reportů o defektech a chce, aby všechny měly stejnou strukturu jako tři vzorové reporty od vedoucí testů. **Few-shot.** Opakující se úloha s pevným formátem a hotové vzory.
2. Tester má poprvé analyzovat logy z nového platebního modulu, neví, jak úlohu modelu popsat, a chce, aby mu model pomohl prompt sestavit. **Meta prompting.** Nová úloha a nejistota, jak prompt napsat.
3. Analýza rozsáhlé specifikace úvěrového procesu: nejdřív najít nejasnosti, pak po vyjasnění odvodit testovací podmínky, pak zkontrolovat pokrytí. Po každém kroku musí výsledek schválit analytik. **Prompt chaining.** Složitá úloha s lidským ověřením mezi kroky.
4. Převod 300 manuálních testovacích případů do skriptů v existujícím frameworku klíčových slov, ve kterém už je 50 hotových skriptů. **Few-shot.** Opakující se vzor, vzory existují.
5. Test manažer chce jednorázově vysvětlit, co znamená metrika hustota defektů. **Zero-shot.** Jednoduchý dotaz, model to zná, tvar nehraje roli.
6. Detekce anomálií v nočních výsledcích výkonnostních testů. Tým zatím neví, jaké anomálie hledat a jak úlohu nejlépe zadat. **Meta prompting.** Pružná úloha, nový typ, prompt teprve vzniká.
7. Vytvoření end-to-end testovacích procedur pro pojistnou událost, kde se nejdřív vygenerují testovací případy pro jednotlivé kroky procesu, tester je ověří a pak se z nich sestaví procedury. **Prompt chaining.** Výsledek jednoho kroku slouží jako ověřený vstup dalšího.
8. Nový interní nástroj má generovat testovací případy pro desítky týmů. Vedoucí chce nejdřív s modelem připravit dobrý prompt, doplnit do něj firemní vzory testovacích případů a pak úlohu rozdělit na generování a kontrolu pokrytí. **Kombinace: meta prompting, few-shot a prompt chaining.** Přesně podle vzoru kombinace ze sylabu.

:::praxe
Pro `uctenky` se kombinace hodí třeba při rozšíření E2E testů. Meta promptingem vznikne prompt pro generování Playwright testů. Do promptu se jako příklady vloží dva existující testy z `tests/invoices.spec.ts` (few-shot), aby model dodržel Page Object Model. Úloha se rozdělí: nejdřív testovací případy v textu, kontrola, pak teprve kód, spuštění a oprava (prompt chaining).
:::

:::zkouska
Otázka k 2.2.5 je K3 za dva body. Vypadá jako scénář s popisem úlohy a čtyřmi technikami na výběr. Rozhodují tři otázky. Jsou v zadání hotové příklady, které se mají napodobit? Pak few-shot. Je úloha rozdělená na kroky s ověřováním? Pak řetězení. Má model pomoci vytvořit nebo vylepšit prompt? Pak meta prompting. Pokud zadání obsahuje víc znaků najednou, hledejte ten, který je pro úspěch úlohy rozhodující. Když scénář popisuje, že model z dodaných příkladů a jasných pravidel přímo vygeneruje další položky stejného druhu, jde o few-shot, i když se v zadání objeví slovo „analýza“.
:::

## 2.3 Hodnocení výsledků GenAI a ladění promptů

:::lo
GenAI-2.3.1 (K2) Understand the metrics for evaluating the results of generative AI on test tasks
GenAI-2.3.2 (K2) Give examples of techniques for evaluating and iteratively refining prompts
:::

Výstup GenAI nelze přebírat bez kontroly. Sylabus proto chce, aby hodnocení probíhalo podle jasné sady metrik, které posoudí kvalitu, relevanci a účinnost vygenerovaných výstupů. Sylabus odkazuje na práci Li (2024). Metriky mohou být obecné nebo specifické pro úlohu a pomáhají prompty optimalizovat. Oddíl 2.3.1 popisuje metriky, oddíl 2.3.2 techniky, jak prompt na jejich základě vylepšit.

### 2.3.1 Metriky pro hodnocení výsledků GenAI v testovacích úlohách

Sylabus uvádí sedm metrik. Všechny vysvětlím na jednom příkladu, aby bylo vidět, jak se liší.

**Příklad pro celý oddíl.** Tester nechal LLM vygenerovat testovací případy pro filtr faktur v projektu `uctenky`. Testovací báze má 12 požadavků (R1 až R12). Pro filtr ceny určil tester předem 8 tříd ekvivalence: čtyři platné (jen minimum, jen maximum, minimum i maximum, minimum rovné maximu) a čtyři neplatné (záporná cena, nečíselný vstup, minimum větší než maximum, víc než dvě desetinná místa). Model vrátil 40 testovacích případů. Tester je zkontroloval a z testovacích případů nechal vygenerovat Playwright testy.

#### Accuracy (správnost)

**Accuracy** měří celkovou správnost výstupu vůči testovacím případům napsaným odborníkem, vůči požadavkům nebo jinému standardu. Příklad ze sylabu: do jaké míry vygenerované testovací případy pokrývají všechny specifikované požadavky.

V příkladu pokrývají vygenerované testovací případy 10 z 12 požadavků. Accuracy z pohledu pokrytí požadavků je 10 / 12 = 83 %. Tester může accuracy měřit i jinak, například porovnáním s referenční sadou od zkušeného kolegy, nebo podílem testovacích případů se správným očekávaným výsledkem. Vždy jde o srovnání s nějakým standardem.

:::pojem term="accuracy"
Správnost. Celková korektnost výstupu GenAI vůči standardu: testovacím případům od odborníka, požadavkům nebo jiné referenci. Například podíl požadavků, které vygenerované testy pokrývají.
:::

#### Precision (přesnost)

**Precision** hodnotí správnost výstupu vzhledem ke konkrétnímu cíli. Příklad ze sylabu: do jaké míry vygenerované testovací případy správně identifikují anomálie.

V příkladu model označil 16 testovacích případů jako „negativní, odhalí neplatné chování“. Tester zjistil, že skutečně neplatné chování testuje 12 z nich. Zbylé čtyři jsou ve skutečnosti pozitivní testy s jiným popisem. Precision vůči cíli „odhalit anomálie“ je 12 / 16 = 75 %.

:::pojem term="precision"
Přesnost. Správnost výstupu vzhledem ke konkrétnímu cíli. Například jaký podíl testovacích případů, které mají odhalit anomálii, ji opravdu cílí.
:::

#### Recall (úplnost)

**Recall** měří schopnost modelu najít všechny relevantní případy v daném souboru. Příklad ze sylabu: do jaké míry vygenerované testovací případy pokrývají platné a neplatné třídy ekvivalence datové třídy.

V příkladu pokrývají testovací případy 5 z 8 tříd ekvivalence: všechny čtyři platné a jen jednu neplatnou (zápornou cenu). Recall je 5 / 8 = 62,5 %. Chybí nečíselný vstup, minimum větší než maximum a víc než dvě desetinná místa.

:::pojem term="recall"
Úplnost. Schopnost modelu zachytit všechny relevantní případy. Například podíl tříd ekvivalence, které vygenerované testy pokrývají.
:::

Precision a recall se doplňují. Model může mít vysokou precision (co označil jako negativní test, opravdu je negativní test) a nízký recall (většinu neplatných tříd vůbec nenašel). Proto se hodnotí obě.

:::nad-ramec
Kdo zná strojové učení, zná precision a recall jako vzorce nad maticí záměn: precision = TP / (TP + FP), recall = TP / (TP + FN). Výpočty v příkladu jsou s tím v souladu. Sylabus CT-GenAI ale metriky definuje slovně a šířeji. Accuracy tu například neznamená podíl správných klasifikací, ale celkovou správnost vůči standardu. Kurz Roshdy na tento rozdíl výslovně upozorňuje. Ve zkoušce platí definice ze sylabu.
:::

#### Relevance and contextual fit (relevance a soulad s kontextem)

**Relevance and contextual fit** určuje, zda je výstup použitelný a vhodný pro daný kontext. Příklad ze sylabu: do jaké míry jsou vygenerované testovací případy v souladu s testovací bází a zahrnují požadavky specifické pro doménu.

V příkladu tři testovací případy testují filtrování podle měny EUR a export do PDF. Nic z toho aplikace nemá ani to není v testovací bázi. Dva další testovací případy ignorují pravidlo, že skryté osoby se ve výpisu nezobrazují. Relevance je tedy narušená u 5 ze 40 případů. Testovací případy mimo testovací bázi mohou vypadat věrohodně, ale jsou signálem halucinace, ne bonusem.

:::pojem term="relevance and contextual fit"
Relevance a soulad s kontextem. Zda je výstup použitelný v daném projektu: odpovídá testovací bázi, doméně a potřebám čtenáře.
:::

#### Diversity (rozmanitost)

**Diversity** hodnotí, zda výstup pokrývá širokou škálu vstupů a situací a vyhýbá se opakování. Příklad ze sylabu: do jaké míry vygenerované testovací případy pokrývají různé chování uživatelů a zkoumají okrajové případy.

V příkladu je 9 ze 40 testovacích případů téměř stejných: liší se jen hodnotou ceny ve stejné třídě ekvivalence. Unikátních testovacích případů je 31. Hraniční hodnoty (například cena přesně na minimu) testují jen dva případy. Rozmanitost je nízká, i když počet testů vypadá velkoryse.

:::pojem term="diversity"
Rozmanitost. Míra, do jaké výstup pokrývá různé vstupy, chování uživatelů a okrajové případy bez zbytečného opakování.
:::

#### Execution success rate (míra úspěšného spuštění)

**Execution success rate** měří podíl vygenerovaných testovacích artefaktů, které lze v testovacím prostředí úspěšně spustit tak, jak jsou. Příklad ze sylabu: kolik vygenerovaných testovacích skriptů lze spustit bez syntaktických chyb a bez problémů s formátem výstupu.

V příkladu vzniklo ze 40 testovacích případů 40 Playwright testů. 31 z nich šlo spustit bez úprav. Devět mělo chybu: neexistující metodu stránkového objektu, překlep v importu, nebo pevné čekání, které neprošlo lintem. Execution success rate je 31 / 40 = 77,5 %.

Pozor na rozdíl mezi „spustit“ a „projít“. Test, který se spustí a selže, protože našel defekt, se počítá jako úspěšně spuštěný. Metrika hodnotí použitelnost artefaktu, ne kvalitu testovaného systému.

:::pojem term="execution success rate"
Míra úspěšného spuštění. Podíl vygenerovaných artefaktů (skriptů, testů), které lze spustit v testovacím prostředí bez úprav, tedy bez syntaktických chyb a problémů s formátem.
:::

#### Time efficiency (časová efektivita)

**Time efficiency** hodnotí ušetřený čas ve srovnání s ruční prací. Příklad ze sylabu: čas, který AI potřebuje k vygenerování testovacích případů, oproti času, který by člověk potřeboval na ruční vytvoření ekvivalentních testů.

V příkladu by tester psal testovací případy i skripty ručně asi 6 hodin. Generování trvalo 5 minut, kontrola a opravy 1 hodinu 30 minut. Celkem 1 hodina 35 minut. Úspora je 4 hodiny 25 minut, tedy asi 74 %. Doporučuji do výpočtu vždy zahrnout čas kontroly. Bez něj by úspora vyšla skoro 99 % a nebyla by pravdivá.

:::pojem term="time efficiency"
Časová efektivita. Ušetřený čas při použití GenAI ve srovnání s ruční prací na stejném výsledku.
:::

#### Souhrn metrik a jak je měřit

| Metrika | Otázka, na kterou odpovídá | Hodnota v příkladu |
|---|---|---|
| Accuracy | Je výstup správný vůči standardu? | 10 / 12 požadavků = 83 % |
| Precision | Je správný vzhledem ke konkrétnímu cíli? | 12 / 16 = 75 % |
| Recall | Našel všechno relevantní? | 5 / 8 tříd = 62,5 % |
| Relevance and contextual fit | Hodí se do kontextu projektu? | 5 ze 40 mimo testovací bázi nebo pravidla |
| Diversity | Je výstup rozmanitý a bez opakování? | 31 unikátních ze 40, 2 hraniční |
| Execution success rate | Dá se spustit, jak je? | 31 / 40 = 77,5 % |
| Time efficiency | Kolik času to ušetřilo? | asi 74 % |

Tabulka ukazuje, že jedno číslo nestačí. Výstup s vysokou time efficiency a nízkým recallem šetří čas tím, že vynechává testy.

Sylabus doplňuje tři věci. Kromě obecných metrik lze definovat **task-specific metrics** (metriky specifické pro úlohu), například u reportů o defektech podíl reportů, které vývojáři vrátí kvůli chybějícím informacím. Metriky lze vyhodnocovat ručně revizí, nebo automaticky, například porovnáním výstupu LLM s předem připravenou referencí. A protože je GenAI nedeterministická, musí metriky vycházet ze statisticky relevantních dat.

V praxi to znamená spustit stejný prompt vícekrát a hodnotit průměr a rozptyl, ne jeden výsledek. Pokud deset běhů dá recall mezi 50 a 75 % s průměrem 64 %, je to užitečnější informace než jeden běh se 75 %.

Praktický cíl **HO-2.3.1 (H0)** ukazuje na konkrétní testovací úloze, jak se metriky přizpůsobí úloze a jak se použijí na výsledky z LLM.

:::zkouska
Nejčastěji se pletou accuracy, relevance a diversity. Accuracy je správnost vůči standardu. Relevance je vhodnost pro kontext a doménu. Diversity je šíře bez opakování. Precision se ptá „je správně to, co model vrátil vzhledem k cíli“, recall „vrátil model všechno, co měl“. Execution success rate se týká spustitelnosti, ne výsledku testu. Time efficiency sama nestačí: rychle vygenerované nepoužitelné skripty nejsou úspěch. Pokud otázka popisuje kombinaci výstupů (testovací případy, skripty a testovací data), správná odpověď obvykle kombinuje metriku pro šíři pokrytí s metrikou pro spustitelnost skriptů.
:::

### 2.3.2 Techniky hodnocení a iterativního ladění promptů

Na metriky navazuje pět technik, které sylabus uvádí pro hodnocení a vylepšování promptů.

#### Iterative prompt modification (iterativní úprava promptu)

Začnete základním promptem a podle skutečných výsledků ho postupně upravujete. Přidáváte kontext nebo měníte formulace, například terminologii, aby byl prompt konkrétnější a výsledek relevantnější. Je to výchozí technika, ostatní ji doplňují.

#### A/B testing of prompts (A/B testování promptů)

Vytvoříte několik verzí promptu a podle předem stanovených metrik vyhodnotíte, která dává lepší výsledky. Technika pomáhá zjistit, která formulace nebo struktura promptu vede k nejpřesnějším a nejrelevantnějším výsledkům. Podmínkou jsou metriky stanovené předem a dost běhů na každou verzi.

#### Output analysis (analýza výstupu)

Zkoumáte výstup AI a hledáte nepřesnosti a nekonzistence, například vůči testovací bázi. Když pochopíte, jaké typy chyb model dělá, upravíte prompt tak, aby se podobné chyby v dalších iteracích neopakovaly. Hodí se tam, kde výstup soustavně obsahuje stejný druh chyby a potřebujete zjistit proč.

#### Integrate user feedback (zapracování zpětné vazby uživatelů)

Sbíráte od testerů názory na užitečnost a srozumitelnost výstupu, například na úroveň podrobnosti vygenerovaných testů. Jejich postřehy analyzujete a podle nich prompt upravíte, aby lépe odpovídal skutečným potřebám. Uživateli výstupu mohou být i vývojáři, kteří čtou reporty o defektech, nebo vedení, které čte souhrny.

#### Adjust prompt length and specificity (úprava délky a konkrétnosti promptu)

Zkoušíte různou délku promptu a různou úroveň podrobnosti. Někdy víc kontextu zlepší kvalitu odpovědi. Jindy kratší prompt lépe zobecňuje. Dlouhý prompt plný nesouvisejících informací může odvést pozornost modelu od podstaty úlohy.

#### Řešený příklad: verze 1 → verze 2 → verze 3

Úloha: testovací případy pro filtr ceny faktur v `uctenky`. Každou verzi tester spustil pětkrát a metriky zprůměroval.

**Verze 1** je zero-shot bez struktury.

```text
Napiš testovací případy pro filtr faktur podle ceny.
```

Výsledek: obecné testovací případy, kroky popisují neexistující tlačítka, polovina testů je o řazení, ne o filtru. Žádné neplatné třídy kromě záporné ceny.

Tester provedl **output analysis**. Zjistil tři typy chyb. Model nezná rozhraní aplikace, a tak vymýšlí prvky. Model neví, jaké hodnoty jsou neplatné. A model neví, zda je hranice minima včetně, nebo bez, takže očekávané výsledky si odporují.

**Verze 2** přidává kontext, vstupní data a omezení.

```text
Role: Jsi test analytik webových aplikací.
Context: Aplikace uctenky, stránka Faktury, filtr podle minimální a maximální
ceny. Cena je kladné číslo s nejvýše dvěma desetinnými místy, max 99 999 999,99.
Instruction: Navrhni testovací případy pro filtr ceny.
Input data: Popis filtru: pole „Min. cena“ a „Max. cena“, tlačítko „Filtrovat“.
Hranice jsou včetně (faktura s cenou rovnou minimu se zobrazí).
Constraints: Pokryj všechny platné a neplatné třídy ekvivalence a hraniční
hodnoty. Nevymýšlej prvky rozhraní, které nejsou v popisu.
Output format: Tabulka: ID, třída/hranice, vstup, očekávaný výsledek.
```

Výsledek: kroky odpovídají aplikaci, recall vzrostl, očekávané výsledky už si neodporují. Testeři ale v **zpětné vazbě** uvedli, že tabulka nejde přímo převést na Playwright testy, protože chybí předpoklady (jaká data jsou v databázi). A testovací případy se mezi běhy výrazně liší v podrobnosti.

**Verze 3** přidává dva příklady (few-shot) a přesný formát.

```text
<vše z verze 2>

Output format: Pro každý testovací případ blok přesně podle příkladů:

Příklad 1
ID: TC-F01
Třída: platná, minimum i maximum
Předpoklad: faktury s cenou 500, 1 500 a 3 000 Kč
Kroky: Min. cena = 1 000; Max. cena = 2 000; Filtrovat
Očekávaný výsledek: zobrazí se jen faktura s cenou 1 500 Kč

Příklad 2
ID: TC-F02
Třída: neplatná, minimum větší než maximum
Předpoklad: faktury s cenou 500, 1 500 a 3 000 Kč
Kroky: Min. cena = 2 000; Max. cena = 1 000; Filtrovat
Očekávaný výsledek: <doplní tester podle skutečného chování aplikace>
```

V příkladu 2 tester záměrně nenechal očekávaný výsledek vymyslet. Chování aplikace pro minimum větší než maximum nezná, a tak ho nejdřív ověří. Kdyby do příkladu napsal smyšlenou chybovou hlášku, model by ji opakoval ve všech podobných testech.

Výsledky pěti běhů každé verze:

| Metrika | Verze 1 | Verze 2 | Verze 3 |
|---|---|---|---|
| Recall (8 tříd) | 2,4 / 8 = 30 % | 6,6 / 8 = 83 % | 7,6 / 8 = 95 % |
| Relevance (případy v souladu s testovací bází) | 55 % | 92 % | 97 % |
| Execution success rate skriptů | 20 % | 61 % | 88 % |
| Rozdíl v počtu testů mezi běhy | 6 až 21 | 11 až 17 | 13 až 15 |

Tabulka ukazuje, že každá iterace řešila jiný problém. Verze 2 řešila chybějící kontext, verze 3 chybějící vzor formátu. Čísla jsou ilustrační, ne naměřená. Postup je ale přesně ten, který sylabus popisuje: základní prompt, výsledky, analýza, úprava, nové vyhodnocení.

#### Řešený příklad: A/B test

Tým váhá mezi dvěma formulacemi instrukce ve verzi 3.

- **A:** „Navrhni testovací případy pro filtr ceny.“
- **B:** „Nejdřív vypiš všechny třídy ekvivalence a hraniční hodnoty filtru ceny. Pak ke každé napiš jeden testovací případ.“

Každou verzi spustí desetkrát a porovná předem dané metriky: recall tříd a execution success rate. Pokud B dává recall 96 % proti 88 % u A a execution success rate je u obou stejný, vybere B a uloží ji do sdílené knihovny promptů. Pokud se výsledky liší jen o jednotky procent a rozptyl je velký, rozdíl může být jen náhoda. Pak je potřeba víc běhů, nebo verze považovat za rovnocenné.

#### Jak techniku vybrat podle situace

| Situace | Vhodná technika |
|---|---|
| Model opakovaně generuje testy s chybným očekávaným výsledkem, který odporuje požadavkům, a chcete zjistit proč | output analysis |
| Máte dvě formulace promptu a chcete objektivně vybrat lepší | A/B testing of prompts |
| Testeři říkají, že vygenerované testy jsou příliš podrobné a nečitelné | integrate user feedback |
| První prompt dává obecné výsledky a chcete ho postupně zpřesňovat | iterative prompt modification |
| Dlouhý prompt s mnoha detaily dává úzké výsledky, které nepokrývají nové situace | adjust prompt length and specificity |

Tabulka je pomůcka pro zkoušku. V praxi se techniky prolínají a jedna ladicí session obvykle použije několik z nich.

:::praxe
Ne každá změna výstupu znamená, že je prompt špatný. Když stejný prompt dá jednou „Ověř, že se zobrazí faktura“ a podruhé „Zkontroluj zobrazení faktury“, je to běžné nedeterministické chování. Prompt je potřeba upravit, když se mění *obsah*: chybí požadované detaily, objevují se funkce mimo testovací bázi nebo si odporují očekávané výsledky.
:::

#### Sdílení v týmu

Sylabus doporučuje, aby týmy pořádaly session pro hodnocení a optimalizaci promptů a sdílely postupy v rámci týmu nebo celé testovací organizace. Sdílení pomáhá standardizovat techniky a udržet stejnou kvalitu. Podporuje kulturu učení a postupného zlepšování. Tým staví na společných zkušenostech, neopakuje stejné chyby a postupně používá GenAI nástroje účinněji. Sylabus jako příklad uvádí sdílení **prompt libraries** (knihoven promptů).

:::pojem term="prompt library"
Knihovna promptů. Sdílená sbírka ověřených promptů pro opakované testovací úlohy, často s výsledky hodnocení a poznámkami, kdy prompt použít.
:::

Praktický cíl **HO-2.3.2 (H1)** je cvičení optimalizace promptu pro danou testovací úlohu. Účastníci začnou počátečním promptem, iterativně ho upravují a každou iteraci vyhodnotí metrikami z oddílu 2.3.1. Používají A/B testování a lidské ověření. Na konci mají za sebou několik iterací a vidí, jak ladění vede k účinnějšímu a kontextu lépe odpovídajícímu generování testovacích případů.

:::zkouska
Otázky k 2.3.2 obvykle popíšou problém a ptají se, která technika se na něj hodí nejlépe. Když model soustavně dělá stejný typ chyby a jde o pochopení příčiny, je to output analysis. A/B testing předpokládá, že máte víc verzí promptu a srovnáváte je metrikami. Zpětná vazba uživatelů se hodí, když problém vidí čtenáři výstupu a vy ho zatím neznáte. Úprava délky a konkrétnosti se hodí, když prompt vede k příliš úzkým nebo příliš obecným výsledkům. Variabilita formulací mezi běhy sama o sobě není důvod prompt měnit.
:::
