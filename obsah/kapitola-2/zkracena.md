---
kapitola: 2
varianta: zkracena
nadpis: Prompt engineering pro efektivní testování
podtitul: Co je nutné ke zkoušce: šest komponent promptu, tři základní techniky, systémový a uživatelský prompt, GenAI v testovacích činnostech, metriky a ladění promptů.
---

Kapitola 2 dává ve zkoušce 11 otázek za 16 bodů. Pět otázek je K3 (oddíl 2.2), každá za 2 body. LO 2.1.1 má dvě otázky, ostatní LO po jedné. Klíčová slova: **acceptance criteria** (akceptační kritéria), **test script** (testovací skript), **test case** (testovací případ), **test condition** (testovací podmínka), **test data** (testovací data), **test design** (návrh testů), **test report** (report z testování), **few-shot prompting**, **meta prompting**, **natural language processing** (zpracování přirozeného jazyka, NLP), **one-shot prompting**, **prompt**, **prompt chaining** (řetězení promptů), **prompt engineering**, **system prompt** (systémový prompt), **user prompt** (uživatelský prompt), **zero-shot prompting**.

## 2.1 Tvorba účinných promptů

:::lo
GenAI-2.1.1 (K2) Give examples of the structure of prompts used in generative AI for software testing
GenAI-2.1.2 (K2) Differentiate core prompting techniques for software testing
GenAI-2.1.3 (K2) Distinguish between system prompts and user prompts
:::

**Prompt** je vstup, kterým zadáváme LLM úlohu. **Prompt engineering** je návrh, zkoušení a vylepšování promptů, aby výstupy byly přesné a použitelné. **NLP** je schopnost modelu rozumět běžnému jazyku. Díky ní model rozkládá požadavky na testovatelná tvrzení a z požadavků vytváří návrhy testovacích případů.

Dobré výsledky dává kombinace tří věcí: strukturovaného promptu, techniky promptování a správného rozdělení na systémový a uživatelský prompt.

### 2.1.1 Šest komponent strukturovaného promptu

| Komponenta | Co obsahuje |
|---|---|
| **Role** | perspektiva nebo persona: tester, test manažer, inženýr automatizace; určuje odpovědnost, tón a přístup |
| **Context** (kontext) | pozadí: testovaný objekt, testovaná funkce, okolnosti |
| **Instruction** (instrukce) | úloha; jasně, v rozkazovacím způsobu, stručně, s podstatnými požadavky |
| **Input data** (vstupní data) | materiál k práci: uživatelské scénáře, akceptační kritéria, snímky, kód, existující testy, ukázky výstupu |
| **Constraints** (omezení) | pravidla a omezení; určují, jak se instrukce použije na vstupní data |
| **Output format** (formát výstupu) | podoba, struktura a vlastnosti odpovědi |

Pořadí v sylabu je vždy stejné. Struktura se kombinuje s technikami promptování podle úlohy a modelu.

Příklad celého strukturovaného promptu:

```text
Role: Jsi test analytik platebních systémů v bance.
Context: Mobilní bankovnictví přidává okamžité platby do 400 000 Kč.
Instruction: Navrhni testovací podmínky pro okamžitou platbu.
Input data: <uživatelský scénář a akceptační kritéria AC1–AC3>
Constraints: Jen funkční chování. Pro limit částky použij hraniční hodnoty.
Chybějící informace nevymýšlej, uveď je jako otevřené otázky.
Output format: Tabulka: ID, testovací podmínka, vazba na AC, priorita.
```

Role má popsat potřebnou odbornost, ne superlativy. Instrukce začíná slovesem (navrhni, najdi, seřaď). Vstupní data je dobré od pokynu oddělit, aby model poznal, co je materiál. Omezení často určuje rozsah, techniku, terminologii, zákazy a prioritu zdrojů. Popisky komponent v promptu nejsou povinné. Pomáhají ale kontrole, že žádná část nechybí, a ve zkoušce bývají prompty s popisky.

Rozlišení častých záměn. Kontext popisuje systém a situaci, vstupní data jsou konkrétní materiál (to, co jde přiložit jako soubor). Omezení je pravidlo pro práci, formát výstupu je podoba výsledku. Instrukce říká co, omezení jak a v jakých mezích. Teplota, seed ani velikost modelu nejsou komponenty promptu.

:::zkouska
Typická otázka: jeden řádek promptu a čtyři komponenty. „Použij přiložené logy a reporty z nástroje“ = input data. „Výstup jako tabulka se sloupci…“ = output format. „Ber v úvahu jen schválené požadavky“ = constraints. U K3 otázek hledejte slabou komponentu: vágní instrukci, omezení typu „drž se osvědčených postupů“, omezení proti cíli („nejvýše dva případy“, když se chce úplnost), formát nevhodný pro čtenáře, chybějící vstupní data.
:::

### 2.1.2 Základní techniky promptování

Tři základní techniky podle sylabu jsou **prompt chaining**, **few-shot prompting** a **meta prompting**. Kombinují se se šestisložkovou strukturou.

**Zero-shot**: prompt bez příkladu, model se opírá o znalosti z tréninku. **One-shot**: právě jeden příklad. **Few-shot**: několik příkladů, které ukotví požadované chování. Few-shot je zvlášť účinný, když příklady umí ukázat požadovaný výstup, a dává konzistentní výsledky.

```text
Příklad 1: <scénář> → <Gherkin>
Příklad 2: <scénář> → <Gherkin>
Nový scénář: <scénář> → ?
```

**Prompt chaining** rozkládá úlohu na řadu promptů. Výsledek každého kroku se ručně nebo automaticky zkontroluje a upraví, než se pokračuje. Každá odpověď ovlivňuje další prompt, a proto je výsledek přesnější. Hodí se pro složité úlohy, které potřebují rozklad a kontrolu mezivýsledků, a umožňuje dynamickou interakci.

```text
Krok 1: Najdi v požadavcích nejednoznačnosti. → tester ověří a vyjasní
Krok 2: Z opravených požadavků odvoď testovací podmínky. → tester zkontroluje
Krok 3: Ověř pokrytí všech požadavků podmínkami a vypiš mezery.
```

Bez ověření mezi kroky jde jen o dlouhý rozhovor, ne o řetězení ve smyslu sylabu.

**Meta prompting** využívá model k vytvoření nebo vylepšení promptu. V opakovaném cyklu model prompt navrhne, tester ho posoudí a upraví. Šetří ruční práci s návrhem promptu a pomáhá testerovi, který neví, jak prompt napsat. Sylabus to popisuje jako párovou práci (pairing) testera s AI, přínosnou pro produktivitu i učení.

```text
Potřebuji prompt pro analýzu exportu výsledků regresních testů (CSV). Chci
seskupit podobná selhání a porovnat je se seznamem známých anomálií. Navrhni
strukturovaný prompt se šesti částmi a nejdřív se mě zeptej na chybějící údaje.
```

Techniky lze kombinovat.

:::zkouska
Zero/one/few-shot se liší jen počtem příkladů. Distraktory prohazují definice: few-shot „rozkládá úlohu“, chaining „dává příklady“, meta prompting „ladí prompty ručně bez modelu“. Meta prompting není chain-of-thought (instrukce „přemýšlej krok za krokem“).
:::

### 2.1.3 Systémový a uživatelský prompt

**System prompt** obvykle definuje vývojář nebo tester nástroje. Uživatel ho ve většině rozhraní nevidí ani nemění. Je to předem daná sada pokynů pro chování, „osobnost“ a provozní parametry modelu (formální tón, stručnost, pravidla domény, zakázané chování). Platí po celou konverzaci a nemění se. Může obsahovat roli, kontext a omezení, případně obecné pokyny k výstupu. Má být jasný a konkrétní, pokud jde o roli a omezení.

**User prompt** je skutečný vstup uživatele. Mění se s každou interakcí, je viditelný a tvoří bezprostřední kontext odpovědi. Má být zaměřený a dobře strukturovaný: explicitní instrukce, relevantní kontext, formát výstupu.

Systémový prompt se nastaví jednou na začátku, uživatelské prompty přicházejí postupně. Model bere v úvahu oba zároveň.

```text
System: Jsi asistent testerů v bance. Odpovídej formálně a podle terminologie
ISTQB. Nevymýšlej chování systému. Testovací případy vracej ve formátu ID,
předpoklady, kroky, očekávaný výsledek.

User: Navrhni testovací případy pro změnu limitu platební karty 0–200 000 Kč.
```

| | System prompt | User prompt |
|---|---|---|
| Kdo píše | vývojář nebo tester nástroje | uživatel |
| Platnost | celá konverzace | jedna interakce |
| Viditelnost | obvykle skrytý | viditelný |
| Obsah | role, kontext, omezení, obecná pravidla | konkrétní úloha, data, upřesnění formátu |

Co platí pořád, patří do systémového promptu. Co se mění s úlohou, patří do uživatelského.

:::zkouska
Hlavní funkce systémového promptu: rámec chování modelu pro celou konverzaci. Nemění se s každou interakcí, nenese konkrétní dotaz uživatele a uživatel ho obvykle nevidí.
:::

## 2.2 Použití technik prompt engineeringu v testovacích úlohách

:::lo
GenAI-2.2.1 (K3) Apply generative AI to test analysis tasks
GenAI-2.2.2 (K3) Apply generative AI to test design and test implementation tasks
GenAI-2.2.3 (K3) Apply generative AI to automated regression testing
GenAI-2.2.4 (K3) Apply generative AI to test monitoring and control task
GenAI-2.2.5 (K3) Select and apply appropriate prompting techniques for a given context and test task
:::

GenAI podporuje testovací analýzu, návrh testů, automatizaci, prioritizaci testovacích případů, detekci defektů, analýzu pokrytí a monitoring a řízení testování. Kvalitní vstup je pro smysluplné výsledky nezbytný.

Postup u K3 otázek: najít cíl v zadání, určit testovací činnost, projít šest komponent, vyřadit obecné a proti cíli jdoucí možnosti, vybrat úpravu, která konkrétně řeší slabé místo. Úprava, která jen opakuje existující text jinými slovy, správná nebývá.

Typické tvary K3 otázek: vybrat nejlepší ze čtyř promptů, vybrat nejlepší úpravu návrhu promptu, vybrat správné pořadí kroků řetězení, nebo vybrat techniku pro popsanou úlohu. Úprava v instrukci nebo ve formátu výstupu, která přesně popisuje požadovaný výsledek, bývá silnější než úprava role.

### 2.2.1 Testovací analýza

Vstup: požadavky, uživatelské scénáře, technické specifikace, wireframy GUI. Výstup: prioritizované testovací podmínky, například akceptační kritéria. Pět úloh:

1. **Hledání potenciálních defektů v testovací bázi**: nekonzistence, nejednoznačnosti, neúplnost; porovnání vzorů požadavků, znalost dřívějších reportů o defektech.
2. **Generování testovacích podmínek** z požadavků a scénářů pomocí NLP.
3. **Prioritizace testovacích podmínek podle rizika**: s informací o pravděpodobnosti a dopadu, s ohledem na regulaci, uživatelské funkce (přihlášení, platby) a historii defektů.
4. **Podpora analýzy pokrytí**: mapování požadavků na testovací podmínky, hledání mezer.
5. **Návrh technik testování** podle typu požadavku (hraniční hodnoty, třídy ekvivalence).

Kvalita a relevance vstupu přímo ovlivňuje správnost výstupu.

Příklad: model, který nedostane údaje o pravděpodobnosti a dopadu, prioritu jen odhaduje. Model, který nevidí wireframe, neodhalí rozpor mezi wireframem a textem požadavku. Užitečné omezení u multimodálního promptu je priorita zdrojů: „při rozporu mezi wireframem a pravidly platí pravidla a rozpor vypiš“.

Pozor na hranici činností: analýza určuje, *co* testovat, návrh testů *jak*. U prioritizace musí prompt dodat pravidlo výpočtu rizika (např. pravděpodobnost × dopad), aby šel výsledek ověřit.

Cvičení: HO-2.2.1a multimodální prompt (text + wireframe) pro akceptační kritéria; HO-2.2.1b řetězení s lidským ověřením v pořadí nejednoznačnosti → testovatelnost → úplnost.

:::zkouska
Testovací analýza = testovací podmínky, priority, defekty v bázi, pokrytí. Testovací případy s kroky už jsou návrh testů. Pokud zadání říká, že krok už proběhl (revize), neopakuje se. Pokud báze obsahuje nejasnosti, řetězení začíná jejich nalezením a ověřením.
:::

### 2.2.2 Návrh testů a implementace testování

Návrh testů rozpracuje testovací podmínky do testovacích případů a dalšího testwaru. Implementace testování vytvoří nebo získá testware potřebný k provedení. Čtyři úlohy:

1. **Generování testovacích případů** (návrhy): předpoklady, vstupy, očekávané výsledky, kritéria pokrytí; od základního ověření po end-to-end.
2. **Syntéza testovacích dat**: reprezentativní, syntetická, chránící soukromí, včetně extrémních situací; pro funkční i nefunkční testy.
3. **Generování automatizovaných testovacích skriptů** a manuálních procedur ze strukturovaných testovacích případů, pro různé frameworky; lze je aktualizovat.
4. **Plánování a prioritizace provedení testů** podle závislostí, priority, rizik, dostupnosti zdrojů a cílů.

Výstupy jsou návrhy. Tester je kontroluje, vygenerovaný kód spustí a projde revizí. Do promptu se nikdy nevkládají skutečná data klientů, syntetická data se generují podle pravidel, ne podle kopie produkce.

Cvičení: HO-2.2.2a testovací případy z AC (strukturovaný prompt) → tabulka pokrytí AC → meta prompt pro E2E procedury; HO-2.2.2b few-shot pro Gherkin (příklady se scénářem, podmínkami a given-when-then); HO-2.2.2c řetězení pro prioritizaci sady s riziky a závislostmi, s ručním ověřením chyb v uvažování.

:::zkouska
Existující vzory a jednotný formát → few-shot. Kontrola po krocích → řetězení. Nejistota, jak prompt napsat → meta prompting. Omezení „nejvýše dva“, „jen hraniční případy“ ohrožuje pokrytí. „Rely on best practices“ je vágní omezení.
:::

### 2.2.3 Automatizované regresní testování

Regresních testů s každým vydáním přibývá, proto se automatizují, hlavně v CI/CD. GenAI pomáhá je vytvářet, udržovat a optimalizovat a analýzou dopadu cílí na oblasti ovlivněné změnami. Pět činností:

1. **Skripty pro testování řízené klíčovými slovy** (keyword-driven): mapování klíčových slov na testovací případy, generování skriptů.
2. **Analýza dopadu a optimalizace testů** podle změn v kódu.
3. **Samoopravné a adaptivní testy** (self-healing) pro drobné změny UI a API.
4. **Automatizované reportování a přehledy**: metriky, selhání, trendy, předpověď míst selhání.
5. **Lepší reporty o defektech a analýza kořenové příčiny**: logy, snímky, údaje o prostředí.

GUI testy trápí měnící se rozhraní (dynamické lokátory), API testy měnící se formáty, endpointy a autentizace. GenAI dělá chyby, výstup se kontroluje podle rizika.

U skriptů řízených klíčovými slovy je typický few-shot: popis knihovny klíčových slov, dva až tři hotové skripty jako vzor a omezení „používej jen klíčová slova z knihovny, chybějící nevymýšlej“. Samooprava testu musí být viditelná a schválená člověkem. Jinak může test „opravit“ i skutečný defekt a projít.

Cvičení: HO-2.2.3a few-shot pro skripty řízené klíčovými slovy, plus systémový prompt pro asistenta, který skripty kontroluje a opravuje; HO-2.2.3b strukturované prompty pro analýzu regresního reportu v jedné konverzaci: porovnání výsledků se specifikací → seskupení podobných defektů → seznam známých anomálií → křížová kontrola.

:::zkouska
Nejlepší úprava promptu pro analýzu reportu konkretizuje instrukci (oddělit očekávané a skutečné výsledky, seskupit, porovnat se známými anomáliemi). Pouhá změna role nebo přidání nesouvisejících pojmů (Gherkin) nepomůže. U výběru regresních testů je nejčastější slabinou chybějící vstup (mapa test → modul).
:::

### 2.2.4 Monitoring testování a řízení testování

Monitoring pracuje s velkým množstvím často nestrukturovaných dat z nástrojů pro správu testů. Čtyři úlohy:

1. **Monitoring a analýza metrik**: trendy, předpověď rizik, upozornění na odchylky od plánu.
2. **Řízení testování**: podklady pro změnu priorit, harmonogramu a zdrojů.
3. **Přehledy z dokončení a průběžné učení**: souhrnné reporty s úspěchy a poučením.
4. **Lepší vizualizace a reportování**: dynamické dashboardy a souhrny v přirozeném jazyce pro všechny zainteresované strany.

Příklad: plán na týden 300 provedených testů, k pátku provedeno 212 (70,7 %), z toho prošlo 177 (83,5 %), 35 nových a 19 uzavřených defektů (+16 otevřených). Model má z takových dat popsat trend (mezera proti plánu roste) a navrhnout opatření řízení testování (vyjasnit blokované testy, přesunout kapacitu na rizikové oblasti, probrat rozsah nebo termín).

HO-2.2.4: ukázka, jak LLM z dat testovacích nástrojů vytvoří metriky postupu, trendů defektů a pokrytí. Čísla od modelu je třeba ověřit, nejlépe požádat o ukázání výpočtu.

:::zkouska
Rozhoduje čtenář a cíl. Srozumitelnost pro vedení → formát výstupu se souhrnem v běžném jazyce a dalšími kroky. Odhalit odchylky → dodat plán a požádat o porovnání. Víc technických detailů může cíl „snadno pochopitelné“ zhoršit.
:::

### 2.2.5 Výběr techniky promptování

| Technika | Kdy | Příklady |
|---|---|---|
| Prompt chaining | složité úlohy s přesností a lidským ověřením po krocích | testovací analýza, návrh testů, automatizace |
| Few-shot | opakující se úlohy, konkrétní nebo omezený formát | Gherkin, keyword-driven, reporty s pevným formátem |
| Meta prompting | pružné, dynamické úlohy, tvorba promptu pro novou úlohu | analýza reportů, detekce anomálií |

Techniky lze kombinovat: meta prompting vytvoří první prompt, ten se doplní příklady (few-shot) a úloha se rozdělí na ověřitelné kroky (chaining). HO-2.2.5 se ptá: vyžaduje úloha přesnost, nebo opakující se strukturu?

Rychlé procvičení:

- Sto reportů o defektech za sprint má mít stejnou strukturu jako tři vzory od vedoucí testů → few-shot.
- Tester poprvé analyzuje logy nového modulu a neví, jak úlohu modelu popsat → meta prompting.
- Specifikace úvěrového procesu: nejasnosti, pak testovací podmínky, pak pokrytí, po každém kroku schválení analytikem → prompt chaining.
- Převod 300 manuálních testů do frameworku klíčových slov, kde už je 50 hotových skriptů → few-shot.
- Jednorázové vysvětlení metriky hustota defektů → zero-shot stačí.
- Nový interní nástroj: s modelem připravit prompt, doplnit firemní vzory, rozdělit na generování a kontrolu → kombinace meta prompting, few-shot a chaining.

:::zkouska
Hotové příklady k napodobení → few-shot. Kroky s ověřením → chaining. Model má pomoci napsat nebo zlepšit prompt → meta prompting. Když model z dodaných příkladů a jasných pravidel přímo generuje další položky stejného druhu, je to few-shot. Zero-shot bývá distraktor.
:::

## 2.3 Hodnocení výsledků GenAI a ladění promptů

:::lo
GenAI-2.3.1 (K2) Understand the metrics for evaluating the results of generative AI on test tasks
GenAI-2.3.2 (K2) Give examples of techniques for evaluating and iteratively refining prompts
:::

### 2.3.1 Metriky

| Metrika | Co měří | Příklad ze sylabu |
|---|---|---|
| Accuracy | celková správnost vůči standardu (testy od odborníka, požadavky) | pokrytí všech specifikovaných požadavků |
| Precision | správnost vzhledem ke konkrétnímu cíli | testovací případy správně identifikují anomálie |
| Recall | zachycení všech relevantních případů | pokrytí platných i neplatných tříd ekvivalence |
| Relevance and contextual fit | vhodnost pro kontext | soulad s testovací bází a doménovými požadavky |
| Diversity | šíře vstupů a situací bez opakování | různé chování uživatelů, okrajové případy |
| Execution success rate | podíl artefaktů spustitelných tak, jak jsou | skripty bez syntaktických chyb a problémů s formátem |
| Time efficiency | ušetřený čas proti ruční práci | čas AI vs. čas člověka na stejné testy |

Příklad výpočtu: 10 z 12 požadavků pokryto → accuracy 83 %. Ze 16 „negativních“ testů 12 skutečně cílí na anomálii → precision 75 %. 5 z 8 tříd ekvivalence → recall 62,5 %. 31 ze 40 skriptů se spustí bez úprav → execution success rate 77,5 %.

Kromě obecných metrik lze použít metriky specifické pro úlohu. Hodnotí se ručně revizí nebo automaticky porovnáním s referencí. Kvůli nedeterminismu musí metriky vycházet ze statisticky relevantních dat (víc běhů).

Precision a recall se doplňují: model může mít vysokou precision (co vrátil, je správně) a nízký recall (většinu relevantních případů nenašel). Test, který se spustí a selže kvůli defektu, se počítá jako úspěšně spuštěný. Do time efficiency patří i čas kontroly výstupu.

:::zkouska
Accuracy = vůči standardu, relevance = vůči kontextu, diversity = šíře bez opakování. Execution success rate = spustitelnost, ne výsledek testu. Time efficiency sama nestačí. U kombinace testovacích případů, skriptů a dat bývá správná kombinace metriky pro šíři pokrytí a metriky spustitelnosti.
:::

### 2.3.2 Techniky hodnocení a ladění promptů

1. **Iterative prompt modification**: začít základním promptem a podle výsledků postupně přidávat kontext a upravovat formulace a terminologii.
2. **A/B testing of prompts**: víc verzí promptu porovnat podle předem daných metrik.
3. **Output analysis**: hledat ve výstupu nepřesnosti a nekonzistence (např. vůči testovací bázi), pochopit typ chyby a upravit prompt.
4. **Integrate user feedback**: sbírat od testerů názory na užitečnost, srozumitelnost a podrobnost.
5. **Adjust prompt length and specificity**: víc kontextu někdy pomůže, kratší prompt jindy lépe zobecní.

Týmy mají pořádat session pro hodnocení a optimalizaci promptů a sdílet postupy, například knihovny promptů (prompt libraries). Pomáhá to standardizovat techniky a neopakovat chyby.

Iterativní ladění v praxi: verze 1 je zero-shot bez struktury a dává obecné testy s vymyšlenými prvky. Analýza výstupu ukáže chybějící kontext a pravidla, a tak verze 2 doplní kontext, vstupní data a omezení (třídy ekvivalence, hranice včetně). Zpětná vazba testerů ukáže nejednotný formát, a tak verze 3 přidá dva příklady (few-shot) a přesný formát. Každá verze se vyhodnotí stejnými metrikami na několika bězích. HO-2.3.2: několik iterací promptu s A/B testováním a lidským ověřením, každá vyhodnocená metrikami.

:::zkouska
Soustavně chybné očekávané výsledky a hledání příčiny → output analysis. Dvě verze promptu k porovnání → A/B testing. Čtenáři říkají, že výstup je příliš podrobný → user feedback. Příliš úzké nebo obecné výsledky → délka a konkrétnost. Jiné formulace se stejným obsahem mezi běhy jsou normální nedeterminismus, ne důvod k úpravě.
:::
