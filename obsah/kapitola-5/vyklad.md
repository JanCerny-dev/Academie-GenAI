---
kapitola: 5
varianta: vyklad
nadpis: Zavedení a integrace generativní AI v testovací organizaci
podtitul: Jak dostat generativní AI do testování řízeně, bez stínové AI, s jasnou strategií, vhodným modelem a připraveným týmem.
---

Předchozí kapitoly ukázaly, co generativní AI umí, jak psát prompty, jaká nese rizika a z čeho se skládá testovací infrastruktura postavená na LLM. Pátá kapitola řeší otázku o úroveň výš. Jak to celé zavést do testovací organizace tak, aby to fungovalo dlouhodobě a nikomu to neublížilo.

Kapitola má dvě části. První, oddíl 5.1, je plán zavedení. Popisuje rizika neřízeného používání AI, obsah strategie, výběr modelu a fáze zavedení. Druhá, oddíl 5.2, je řízení změny. Popisuje, co se musí naučit testeři, jak schopnosti budovat v týmu a jak se mění role testera a test manažera.

Sylabus kapitole přiděluje 80 minut a jediný klíčový pojem: **shadow AI** (stínová AI). Kapitola je krátká, ale u zkoušky z ní padne sedm otázek.

:::zkouska
Z kapitoly 5 je u zkoušky 7 otázek za 7 bodů, z každého LO jedna. Čtyři z nich jsou na úrovni K1: 5.1.1, 5.1.4, 5.2.2 a 5.2.3. Otázka K1 ověřuje, jestli si pamatujete výčet ze sylabu. Správná odpověď často používá skoro stejná slova jako sylabus. Proto se u těchto čtyř LO vyplatí znát seznamy doslova, včetně anglických názvů. Zbylé tři LO (5.1.2, 5.1.3, 5.2.1) jsou K2. Tam musíte umět vysvětlit, proč něco platí, a poznat to v krátkém scénáři.
:::

## 5.1 Plán zavedení generativní AI v testování

:::lo
GenAI-5.1.1 (K1) Recall the risks of shadow AI
GenAI-5.1.2 (K2) Explain the key aspects to consider when defining a Generative AI strategy for software testing
GenAI-5.1.3 (K2) Summarize key criteria for selecting LLMs/SLMs for software test tasks in a given context
HO-5.1.3 (H1) Estimate the recurring costs of using Generative AI for a given test task
GenAI-5.1.4 (K1) Recall key phases in the adoption of Generative AI in a test organization
:::

Oddíl začíná myšlenkou, která drží celou kapitolu pohromadě. Organizace nejdřív potřebuje **GenAI strategy** (strategie generativní AI pro testování). Teprve podle ní sestaví **roadmap** (plán zavedení, cestovní mapu) a pak sleduje, jak integrace do testovacích procesů postupuje.

Sylabus v úvodu oddílu jmenuje čtyři věci, které strategie musí zvážit. Jsou to cíle testování, kterých chceme dosáhnout, vhodný výběr LLM, problémy se vstupními daty pro prompty a soulad s AI normami a předpisy. Podrobněji je rozvádí pododdíl 5.1.2.

Pořadí je důležité. Strategie je první, roadmapa druhá, monitoring třetí. Kdo začne nástrojem a strategii dopisuje zpětně, obvykle skončí u situace, kterou popisuje první pododdíl. Lidé používají AI po svém a organizace o tom neví.

### 5.1.1 Rizika stínové AI

Toto je studijní cíl GenAI-5.1.1 na úrovni K1. Máte si vybavit rizika stínové AI.

:::pojem term="shadow AI"
Stínová AI. Používání nástrojů nebo systémů generativní AI v organizaci bez formálního schválení nebo dohledu (slovník sylabu). Typicky jde o osobní účet ve veřejném chatbotu, do kterého zaměstnanec vkládá pracovní podklady.
:::

Název vychází ze staršího pojmu **shadow IT** (stínové IT). Tak se označují aplikace a služby, které si zaměstnanci zavedli sami, bez vědomí IT oddělení. U AI je princip stejný, jen jsou následky vážnější. Do chatbotu se totiž nevkládá jen text, ale často i data, která organizaci nepatří.

Proč stínová AI vzniká, je pochopitelné. Veřejné nástroje jsou dostupné za pár sekund. Schválení nového nástroje ve firmě trvá týdny. Tester má termín a chce si práci ulehčit. Do volného chatbotu vloží specifikaci a nechá si navrhnout testovací případy. Nikdo mu to nezakázal, ale nikdo to ani neschválil.

Sylabus uvádí tři rizika stínové AI. Tento výčet se zkouší na zapamatování.

1. **Information security and data privacy weaknesses** (slabiny v informační bezpečnosti a ochraně dat). Osobní AI nástroje nemusí mít dostatečné zabezpečení. Výsledkem může být **data breach** (únik dat).
2. **Compliance and regulatory issues** (problémy se souladem s předpisy a regulací). Neschválený nástroj může vést k porušení oborových norem a předpisů. Sylabus tu odkazuje na oddíl 3.4.1, tedy například na EU AI Act nebo ISO/IEC 42001. Důsledkem mohou být právní kroky.
3. **Vague intellectual property** (nejasné duševní vlastnictví). Nástroje s nejasnými licenčními podmínkami mohou uživatele vystavit sporům o duševní vlastnictví. Riziko roste, když se bez oprávnění zpracovávají data chráněná autorským právem.

Sylabus k tomu přidává jednu větu o řešení. Strategie a kroky pro integraci a nasazení GenAI pomáhají testovacím organizacím riziku stínové AI předejít. Řešením tedy není AI zakázat. Řešením je nabídnout schválenou cestu, která je pro lidi pohodlnější než ta neschválená.

Pomůcka na zapamatování: tři otázky, které si položí auditor po incidentu.

- Kam utekla data? To je bezpečnost a ochrana dat.
- Který předpis jsme porušili? To je compliance a regulace.
- Komu patří výsledek a z čeho vznikl? To je duševní vlastnictví.

Anglicky si lze zapamatovat zkratku **S-C-IP**: Security, Compliance, Intellectual Property.

:::zkouska
Hlídejte, ke kterému riziku patří licence. Nejasné licenční podmínky a zpracování chráněných dat bez oprávnění patří k riziku duševního vlastnictví, ne k bezpečnosti. Únik citlivých dat patří k bezpečnosti a ochraně dat. Porušení norem a právní následky patří ke compliance.

Druhý chyták jsou „pozitivní“ tvrzení. Stínová AI nikdy nezlepšuje dodržování předpisů, nesnižuje riziko sporů a neodstraňuje potřebu licencí. Pokud možnost tvrdí o stínové AI něco dobrého, je téměř jistě špatně.

Třetí drobnost: úvodní věta 5.1.1 mluví o rizicích pro „security, compliance, and data privacy“. Ve výčtu je ale třetí bod duševní vlastnictví a ochrana dat je spojená s bezpečností v bodě jedna. Při otázce na výčet se držte tří bodů ze seznamu.
:::

:::praxe
Představte si konzultační firmu, která dodává testery do banky a pojišťovny. Tester má na klientském notebooku přístup k produkčně podobným datům, protože testovací databáze je kopie produkce s neúplnou anonymizací. Jednoho večera si zkopíruje dvacet řádků z tabulky smluv do osobního účtu veřejného chatbotu. Chce zjistit, proč import padá na formátu data.

V jedné akci tak nastala všechna tři rizika. Osobní údaje klientů pojišťovny opustily prostředí, které je mělo chránit. Firma porušila smlouvu s klientem, který zpracování mimo své prostředí nepovolil, a porušila i GDPR. A pokud chatbot vrátí opravený skript, nikdo neví, za jakých licenčních podmínek vznikl a kdo k němu má práva.

Správná cesta existuje a je kratší, než se zdá. Tester popíše problém na vymyšlených datech se stejnou strukturou. Použije nástroj, který firma schválila pro daný typ dat. Nejasnosti řeší s vedoucím nebo s týmem, který ve firmě schvaluje AI nástroje. Ve větších firmách tuto roli plní AI board (rada pro AI) nebo podobný orgán.
:::

:::nad-ramec
V regulovaném prostředí, třeba v bankách, má stínová AI ještě jeden rozměr. Banky podléhají pravidlům pro outsourcing a pro řízení rizik ICT, v EU například nařízení DORA. Pokud dodavatel pošle data klienta do externí služby, kterou banka neprověřila, vzniká nehlášený subdodavatel. Sylabus tyto předpisy nejmenuje, u zkoušky se na ně neptá. V praxi jsou ale častým důvodem, proč klient povolí jen nástroje provozované ve vlastním prostředí.
:::

### 5.1.2 Klíčové aspekty strategie GenAI v testování

Toto je studijní cíl GenAI-5.1.2 na úrovni K2. Máte vysvětlit hlavní aspekty, které je třeba zvážit při definici strategie GenAI pro testování.

Sylabus popisuje šest oblastí. Jdou za sebou v logickém pořadí, od cíle po pravidla.

**1. Měřitelné cíle testování.** Strategie začíná definicí **measurable test objectives** (měřitelné cíle testování) pro GenAI. Sylabus uvádí tři příklady: zvýšit produktivitu testování, zkrátit testovací cykly a zlepšit kvalitu testování. Slovo „měřitelné“ je podstatné. Cíl „zmodernizovat testování pomocí AI“ nejde vyhodnotit. Cíl „zkrátit přípravu testovacích případů pro regresi o 30 % do konce čtvrtletí“ vyhodnotit jde.

**2. Výběr LLM.** Výběr modelu je podle sylabu kritický a musí odpovídat stanoveným cílům. Model navíc musí být kompatibilní se stávající **test infrastructure** (testovací infrastruktura) a musí splnit požadavky na **scalability** (škálovatelnost) systému. Výborný model, který nejde napojit na nástroj pro správu testů ani do CI pipeline, strategii nepomůže. Podrobná kritéria výběru jsou v 5.1.3.

**3. Kvalita dat.** Účinnost testování s LLM závisí na přesných a relevantních vstupních datech. Ta musí být chráněná spolehlivými bezpečnostními postupy. Sylabus to formuluje jasně: vysoká kvalita vstupních dat je podmínkou výsledků, kterým se dá věřit. Platí staré pravidlo „garbage in, garbage out“. Neúplná nebo rozporná specifikace dá neúplné nebo rozporné testy.

**4. Školení.** Organizace má zajistit **training programs** (vzdělávací programy), díky kterým tým získá technické i etické dovednosti. Technické znamená umět napsat prompt, posoudit výstup a zapojit AI do práce. Etické znamená rozumět zkreslení, transparentnosti a ochraně dat.

**5. Metriky.** Kromě školení se mají sbírat konkrétní metriky, které měří účinnost výsledků GenAI. Sylabus odkazuje na oddíl 2.3.1. Tam jsou metriky jako accuracy, precision, recall, relevance and contextual fit, diversity, execution success rate a time efficiency. Bez metrik nejde poznat, jestli strategie plní cíle z bodu 1.

**6. Procesní pravidla.** Pro soulad s regulací a etickými zásadami má organizace zavést **process guidelines** (procesní pravidla) pro používání GenAI. Sylabus jmenuje tři prvky:

- pravidla pro používání citlivých dat,
- **transparency obligations** (povinnosti transparentnosti), tedy například označit, co vzniklo pomocí GenAI,
- **quality gates** (kvalitativní brány) s revizí vygenerovaného testwaru.

Všimněte si, jak body na sebe navazují. Cíl určuje model. Model potřebuje kvalitní data. S modelem a daty musí umět pracovat lidé. Metriky ukazují, jestli to celé plní cíl. A pravidla drží všechno v mezích zákona a etiky.

Pomůcka: **„Cíl, Model, Data, Lidé, Měření, Pravidla.“** Anglicky Objectives, LLM, Data, Training, Metrics, Guidelines.

:::pojem term="quality gate"
Kvalitativní brána. Kontrolní bod v procesu, přes který výstup projde jen tehdy, když splní stanovená kritéria. V kontextu 5.1.2 jde hlavně o povinnou revizi testwaru vygenerovaného AI dříve, než se použije.
:::

:::pojem term="transparency obligation"
Povinnost transparentnosti. Pravidlo, že se u výstupu uvádí, jestli a jak vznikl pomocí generativní AI. Čtenář testovacího případu nebo reportu má vědět, že jde o AI výstup, a podle toho ho posuzovat.
:::

:::zkouska
U otázek K2 k 5.1.2 se často objevují distraktory, které zní rozumně, ale proti sylabu jdou.

- „Dát modelu co nejvíc dat.“ Sylabus chce data přesná a relevantní, ne co nejvíc. Víc dat znamená i víc osobních údajů a větší riziko úniku.
- „Vybrat nejvýkonnější veřejný model.“ Sylabus chce model sladěný s cíli a kompatibilní s infrastrukturou, ne nejsilnější.
- „Zrušit revize, protože AI je rychlá.“ Sylabus naopak chce quality gates s revizí vygenerovaného testwaru.
- „Cíl je zavést AI.“ Zavedení AI není cíl testování. Cílem je produktivita, kratší cykly nebo vyšší kvalita.
:::

:::praxe
Jak by strategie vypadala na projektu, kde dodavatel testuje pro banku nový modul plateb.

Cíl: zkrátit přípravu regresních testovacích případů o čtvrtinu a udržet podíl zamítnutých případů při revizi pod 10 %. Model: nástroj, který klient schválil a který běží v jeho cloudovém tenantu. Musí jít napojit na nástroj pro správu testů, který projekt používá. Data: požadavky a uživatelské scénáře bez osobních údajů, ukázková data jen syntetická. Školení: dvouhodinový workshop k promptům pro testovací případy a krátké školení k pravidlům pro data. Metriky: čas přípravy jednoho případu, podíl případů, které revize přijala bez úprav, a pokrytí požadavků. Pravidla: v nástroji pro správu testů se AI výstup označí štítkem, každý případ projde revizí seniorního testera a reálná klientská data do promptu nepatří nikdy.

Takový dokument má jednu až dvě strany. Na projektu pro regulovaného klienta ho obvykle odsouhlasí i bezpečnostní nebo compliance útvar klienta.
:::

### 5.1.3 Výběr LLM/SLM pro testovací úlohy

Toto je studijní cíl GenAI-5.1.3 na úrovni K2. Máte shrnout hlavní kritéria pro výběr LLM nebo SLM pro testovací úlohy v daném kontextu. Patří k němu praktické cvičení HO-5.1.3 na odhad opakovaných nákladů.

Nejdřív připomenutí z kapitoly 1. **Large language model (LLM)** (velký jazykový model) je natrénovaný na obrovském množství textů. **Small language model (SLM)** (malý jazykový model) má méně parametrů. Je navržený pro odlehčená a zaměřená řešení. Slovník sylabu dodává, že SLM nabízí rovnováhu mezi efektivitou a porozuměním jazyku pro konkrétní úlohu.

Sylabus pak popisuje, v čem se modely na trhu liší. Rozlišuje tři skupiny vlastností:

- **functional capabilities** (funkční schopnosti), například multimodální vstup nebo schopnost uvažování,
- **technical features** (technické vlastnosti), například velikost kontextového okna,
- **licensing types** (typy licencí), například komerční model proti open source.

Pak přichází důležité zjištění. Benchmarků pro zpracování jazyka, generování kódu nebo analýzu obrázků existuje hodně. Benchmarků zaměřených přímo na testovací úlohy je ale málo. Sylabus to dokládá odkazem na práci Wenhan 2024. Proto výběr modelu pro testování vyžaduje pečlivé posouzení podle čtyř kritérií.

**1. Model performance** (výkon modelu). Výkon modelu se hodnotí pro cílové testovací úlohy a proti benchmarkům organizace. K tomu slouží metriky z oddílu 2.3.1. Prakticky to znamená vzít vlastní vzorek úloh, třeba padesát uživatelských scénářů s hotovými testovacími případy od zkušených testerů. Na nich porovnat kandidáty. Veřejný žebříček modelů pro generování kódu tuto práci nenahradí.

**2. Fine-tuning potential** (potenciál pro doladění). Posuzuje se, jestli je možné a užitečné model doladit na doménových datech. Cílem je vyšší přesnost a relevance ve specializovaném kontextu. Fine-tuning jste poznali v oddílu 4.2.1. Některé modely doladit nejde, protože to licence nebo dodavatel neumožňuje. U jiných to jde, ale přínos nevyváží náklady a složitost.

**3. Recurring cost** (opakované náklady). Počítají se náklady, které se opakují po celou dobu používání. Patří sem licenční poplatky a provozní náklady. Model se musí vejít do rozpočtu organizace pro cílové testovací úlohy. Jednorázové náklady, třeba na pilotní ověření, sem nepatří.

**4. Community and support** (komunita a podpora). Přednost mají modely s aktivní komunitou a podrobnou dokumentací. Usnadňují nasazení a řešení problémů.

Pomůcka: **„Výkon, Ladění, Peníze, Pomoc.“** Anglicky si stačí pamatovat čtyři slova: Performance, Fine-tuning, Cost, Community.

Sylabus končí oddíl větou, že organizace může vybrat jeden nebo více modelů. Nemusí tedy existovat jeden model na všechno. Běžné je kombinovat silný model pro složité úlohy s menším modelem pro jednoduché a časté úlohy.

:::zkouska
Hlavní chyták 5.1.3 jsou veřejné benchmarky. Sylabus výslovně říká, že benchmarků pro testovací úlohy je málo. Správné kritérium je výkon na cílových testovacích úlohách měřený proti benchmarkům vlastní organizace. Možnost „vyhodnotit model podle veřejných benchmarků pro generování kódu“ je proto špatně.

Druhý chyták jsou opakované náklady. Licence, poplatky za tokeny, výpočetní výkon a provoz jsou opakované. Jednorázový pilot, proof of concept nebo počáteční instalace opakované nejsou.

Třetí: „výkon“ v sylabu znamená kvalitu výsledků na testovacích úlohách podle metrik z 2.3.1. Nejde primárně o rychlost odpovědi.
:::

### Kdy spíš SLM a kdy spíš LLM

Sylabus nedává tabulku „kdy SLM, kdy LLM“. Odpověď ale skládá z několika míst. Oddíl 1.1.2 popisuje SLM jako lehké a zaměřené. Oddíl 4.2.1 říká, že doladěný SLM může u konkrétní úlohy dosáhnout vysokého výkonu bez výpočetní zátěže velkého modelu. Oddíl 5.2.1 chce po testerech vybírat modely přiměřené velikosti úlohy. Z toho plyne praktické vodítko, které shrnuje tabulka.

| Situace | Spíš SLM | Spíš LLM |
|---|---|---|
| Úloha je úzká, opakovaná a dobře popsaná | ano | |
| Úloha vyžaduje široké znalosti nebo složité uvažování | | ano |
| Data nesmí opustit vlastní prostředí | ano, běží lokálně | jen pokud ho lze provozovat ve vlastním prostředí |
| Velký objem volání a omezený rozpočet | ano | |
| Dlouhé dokumenty, potřeba velkého kontextového okna | | ano |
| K dispozici jsou kvalitní doménová data na doladění | ano, doladění je levnější | možné, ale dražší |

Tabulka je vodítko, ne pravidlo. O výběru vždy rozhoduje měření na vlastních úlohách, tedy první kritérium.

:::praxe
Banka chce, aby AI třídila nové reporty o defektech do kategorií podle komponenty. Za den jich přijde kolem tří set. Data obsahují čísla účtů z logů, takže nesmí opustit prostředí banky. Úloha je úzká a opakovaná. Tým proto zkusí malý model provozovaný na serveru banky. Doladí ho na dvou tisících historických reportů, které už mají správnou kategorii.

Na stejném projektu chce test manažer z dvousetstránkové specifikace vytáhnout testovací podmínky pro nový produkt. Úloha je jednorázová, potřebuje velké kontextové okno a dobré porozumění souvislostem. Tady dává smysl velký model, pokud ho klient schválil pro tento typ dokumentů.

Výsledkem jsou dva modely pro dvě úlohy. Přesně to sylabus připouští.
:::

### Odhad opakovaných nákladů (HO-5.1.3)

Praktické cvičení HO-5.1.3 je na úrovni H1. Máte odhadnout opakované náklady na použití GenAI pro danou testovací úlohu. Sylabus jmenuje vstupní předpoklady: počet tokenů na vstupu a výstupu, použité prompty a četnost úlohy. Porovnat se mají cenové modely několika dodavatelů, alespoň jednoho komerčního a jednoho open source modelu.

Postup výpočtu je jednoduchý. Ukážeme ho na smyšlených cenách, aby šel sledovat. Skutečné ceny se mění a je třeba je ověřit u dodavatele.

Úloha: každou noc AI shrne výsledky regresního běhu do krátkého reportu pro tým.

1. Odhad vstupu: systémový prompt má 800 tokenů, výsledky běhu 12 000 tokenů. Celkem 12 800 tokenů.
2. Odhad výstupu: shrnutí má zhruba 1 000 tokenů.
3. Četnost: jednou za noc, 22 pracovních dní v měsíci. Kvůli opakování při chybách počítáme rezervu 20 %.
4. Komerční model se smyšlenou cenou 3 USD za milion vstupních a 15 USD za milion výstupních tokenů.
   Jeden běh stojí 12 800 × 3 / 1 000 000 + 1 000 × 15 / 1 000 000, tedy asi 0,038 + 0,015 = 0,053 USD.
   Měsíčně 0,053 × 22 × 1,2, tedy asi 1,40 USD.
5. Open source model na vlastním serveru. Licence je zdarma, ale server s GPU stojí smyšlených 600 USD měsíčně. K tomu správa, například čtyři hodiny práce měsíčně.

Závěr je pro jednu úlohu jasný. Komerční model vyjde levněji, protože úloha běží zřídka. Obraz se otočí, když na stejném serveru poběží desítky úloh s tisíci voláními denně. Nebo když data nesmějí opustit vlastní prostředí a komerční služba v něm není dostupná. Cvičení má ukázat právě tohle. Cena za token je jen jedna položka a o výsledku rozhoduje objem, četnost a provozní náklady.

:::nad-ramec
Do opakovaných nákladů se v praxi často zapomíná započítat čas lidí na revizi výstupů. Pokud revize jednoho AI testovacího případu trvá deset minut, je to opakovaný náklad stejně jako tokeny. Sylabus ho u 5.1.3 výslovně neuvádí. Pro rozhodnutí na projektu je ale často větší než účet za model.
:::

### 5.1.4 Fáze zavedení GenAI v testování

Toto je studijní cíl GenAI-5.1.4 na úrovni K1. Máte si vybavit hlavní fáze zavedení GenAI v testovací organizaci.

Sylabus uvádí tři fáze. Jejich přesné anglické názvy se zkoušejí.

1. **Discovery** (objevování). První fáze se zaměřuje na povědomí a budování schopností. Činnosti: školení testovacích týmů o konceptech GenAI, zpřístupnění LLM a SLM a experimenty s prvními případy použití. Cílem je, aby se testeři s GenAI seznámili a získali jistotu.
2. **Initiation and usage definition** (zahájení a definice použití). Ve druhé fázi už existuje základní porozumění. Fáze se zaměřuje na identifikaci a prioritizaci praktických případů použití GenAI v testování. Patří sem posouzení testovací infrastruktury postavené na LLM, rozvoj odbornosti a sladění s potřebami organizace. Sylabus tu odkazuje na kapitolu 6 sylabu CTFL, tedy na nástroje pro testování.
3. **Utilization and iteration** (využívání a iterace). Ve třetí, pokročilé fázi organizace GenAI plně integruje do testovacích procesů. Průběžně sleduje vývoj GenAI pro testování a souvisejících nástrojů. Měří a řídí transformaci, aby přínosy byly udržitelné a škálovatelné.

Sylabus k fázím přidává dvě poznámky. Obě se mohou objevit u zkoušky.

První poznámka: fáze mohou běžet souběžně pro různé případy použití. Analýza reportů z testování může být na roadmapě daleko, zatímco automatizace testů je teprve na začátku. Fáze tedy nepatří organizaci jako celku, ale konkrétnímu případu použití.

Druhá poznámka: je třeba včas rozpoznat a řešit obavy lidí, zejména **fear of job displacement** (strach ze ztráty práce). Ten může zpomalit zavádění a zhoršit náladu v týmu.

Pomůcka na pořadí: **D-I-U**, „Discover, Initiate, Utilize“. Česky „Objevit, Určit, Užívat“. Druhá a třetí fáze mají v názvu dvě části spojené slovem „and“: *Initiation and usage definition*, *Utilization and iteration*. První fáze je jen jedno slovo: *Discovery*.

Pro rozlišení fází pomáhá otázka, co je hlavním výstupem.

| Fáze | Hlavní otázka | Typický výstup |
|---|---|---|
| Discovery | Co to umí a jak se s tím pracuje? | proškolený tým, přístup k modelům, první pokusy |
| Initiation and usage definition | Kde nám to přinese nejvíc a s čím? | prioritizovaný seznam případů použití, posouzená infrastruktura |
| Utilization and iteration | Jak to udržet, měřit a rozšiřovat? | integrace do procesu, monitoring, měření přínosu, škálování |

:::zkouska
U otázky na fáze hledejte přesně tři názvy v pořadí Discovery, Initiation and usage definition, Utilization and iteration. Distraktory obvykle používají názvy, které znějí věrohodně, ale v sylabu nejsou: Pilot, Rollout, Scaling, Assessment, Optimization, Planning, Execution. Pozor i na prohozené pořadí nebo na čtyři fáze místo tří.

Častá je i otázka na zařazení činnosti. Školení a první experimenty patří do Discovery. Výběr a prioritizace případů použití a posouzení infrastruktury patří do Initiation and usage definition. Průběžný monitoring, měření transformace a škálování patří do Utilization and iteration.

Tvrzení „fáze musí proběhnout postupně pro celou organizaci“ je špatně. Sylabus říká, že mohou běžet souběžně pro různé případy použití.
:::

:::praxe
Jak mohou fáze vypadat u dodavatele testování, který pracuje pro několik bank a pojišťoven.

Discovery: firma zpřístupní schválený AI asistent v interním prostředí. Uspořádá školení k promptům a k pravidlům pro data. Testeři zkoušejí první úlohy na veřejných nebo vymyšlených podkladech, například návrh testovacích případů pro ukázkovou webovou aplikaci.

Initiation and usage definition: na jednom bankovním projektu tým vybere tři případy použití. Jsou to návrh testovacích případů z uživatelských scénářů, shrnutí výsledků regresního běhu a příprava syntetických testovacích dat. Seřadí je podle přínosu a rizika. Posoudí, jestli schválený nástroj jde napojit na nástroj pro správu testů. S klientem dohodne, jaká data smí do nástroje jít.

Utilization and iteration: shrnování regresních běhů funguje po třech měsících běžně. Tým měří, kolik času ušetří a kolik shrnutí musel opravit. Postup rozšíří na druhý projekt. Současně je generování testovacích dat stále ve fázi Discovery, protože klient zatím syntetická data neschválil. To je přesně souběh fází, který sylabus popisuje.

Strach ze ztráty práce se tu projeví konkrétně. Senioři se bojí, že klient bude chtít menší tým. Pomáhá otevřeně říct, co se mění. Méně času na přepisování, víc času na analýzu rizik a revizi. A ukázat, že revize AI výstupů vyžaduje právě zkušené lidi.
:::

## 5.2 Řízení změny při zavádění GenAI v testování

:::lo
GenAI-5.2.1 (K2) Explain the essential skills and knowledge areas required for testers to work effectively with generative AI in test processes
GenAI-5.2.2 (K1) Recall strategies for cultivating AI skills within test teams to support the adoption of Generative AI in test activities
GenAI-5.2.3 (K1) Recognize how test processes and responsibilities shift within a test organization when adopting Generative AI
:::

Úspěšné zavedení GenAI podle sylabu vyžaduje strukturovaný přístup k **change management** (řízení změny). Sylabus jmenuje dva hlavní aspekty. Prvním je budování potřebných dovedností. Druhým je vývoj tradičních testovacích rolí směrem k procesům podporovaným AI. Transformace má technickou i organizační stránku.

Tři pododdíly na sebe navazují jako jednotlivec, tým a organizace. Oddíl 5.2.1 říká, co musí umět jednotlivý tester. Oddíl 5.2.2 říká, jak to tým naučit. Oddíl 5.2.3 říká, jak se změní role a procesy.

### 5.2.1 Dovednosti a znalosti pro testování s GenAI

Toto je studijní cíl GenAI-5.2.1 na úrovni K2. Máte vysvětlit dovednosti a oblasti znalostí, které tester potřebuje k efektivní práci s generativní AI v testovacích procesech.

Sylabus obsah oddílu skládá z několika vrstev. Pro přehled je seřadíme do pěti oblastí.

**1. Technické AI dovednosti.** Tester má ovládat techniky **prompt engineering** (tvorba promptů) z kapitoly 2. Má rozumět **context window** (kontextové okno) modelu z kapitoly 1. A má si vytvořit metody revize testů, tedy postup, jak AI výstup zkontrolovat. Kontextové okno je praktická věc. Kdo vloží do konverzace sto stran a čeká, že model si pamatuje detail ze strany tři, dostane nespolehlivou odpověď.

**2. Doménová a testovací odbornost spojená s AI.** Testeři musí spojit znalost domény a testování s dovednostmi AI. Jen tak dokážou posoudit testování řízené LLM. Sylabus uvádí tři úlohy: generování testovacích případů, analýzu reportů o defektech a generování testovacích dat. Tester, který nezná pravidla pro výpočet úroků, nepozná, že AI vygenerovala testovací případ se špatně očekávaným výsledkem.

**3. Hlavní kompetence.** Sylabus je jmenuje výslovně:

- **assessing LLM capabilities** (posouzení schopností LLM), tedy co model zvládne a co ne, a jestli se dá pro úlohu přizpůsobit,
- **prompt refinement** (zpřesňování promptů), tedy postupné ladění zadání,
- **evaluation of AI-generated testware** (hodnocení testwaru vygenerovaného AI).

**4. Znalost rizik a ochrany dat.** Tester má rozumět rizikům, která jsou s GenAI neoddělitelně spojená, a běžným způsobům jejich zmírnění. To navazuje na kapitolu 3. Konkrétně má:

- rozumět dopadům sdílení testwaru s LLM na bezpečnost dat,
- provádět **data sanitization** (sanitizace dat), tedy odstranit nebo zamaskovat citlivé, osobní a důvěrné informace,
- dodržovat postupy **privacy-preserving prompt engineering** (tvorba promptů šetrná k soukromí).

**5. Environmentální hledisko.** Sylabus sem řadí optimalizaci výběru modelu a způsobu používání, aby se snížila výpočetní zátěž. Patří sem výběr **right-sized models** (modely přiměřené velikosti) pro testovací úlohy. A vyvažování přínosů automatizace s dopadem na náklady a spotřebu energie. Navazuje to na oddíl 3.3.1.

:::pojem term="data sanitization"
Sanitizace dat. Odstranění nebo zamaskování citlivých, osobních a důvěrných informací dříve, než se data předají modelu. Příklad: rodné číslo v logu se nahradí zástupným textem, jméno klienta vymyšleným jménem.
:::

:::pojem term="right-sized model"
Model přiměřené velikosti. Model, jehož schopnosti a výpočetní náročnost odpovídají úloze. Na jednoduchou klasifikaci nebo přeformulování textu stačí menší model. Velký model se nechá na složité úlohy.
:::

Proč je LO na úrovni K2 a ne K1? Sylabus nechce, abyste seznam jen odříkali. Chce, abyste poznali, proč daná dovednost k testování s AI patří. A abyste odlišili dovednosti s AI od obecných testovacích dovedností nebo od úloh, které testerovi nepatří.

Pro orientaci pomáhá otázka: týká se dovednost práce s modelem a jeho výstupy v testovacím procesu? Pokud ano, patří sem. Pokud jde o obecnou testovací techniku bez vazby na AI, nebo o práci vývojáře modelu, sem nepatří.

:::zkouska
Distraktory u 5.2.1 bývají tří druhů.

- Nesplnitelné cíle. „Ovládnout techniky, které zabrání halucinacím.“ Halucinace a chyby v uvažování jsou vlastností současných LLM. Lze je zmírnit, ne odstranit. Sylabus mluví o znalosti rizik a jejich zmírnění.
- Práce vývojáře modelu. „Zajistit kvalitu trénovacích a validačních dat modelu.“ Tester data, na kterých dodavatel model trénoval, obvykle nevidí a neovlivní. Jeho úlohou je posoudit schopnosti modelu a kvalitu výstupů.
- Obecné testovací dovednosti bez vazby na AI. Například výběr přístupu k automatizaci testů. Užitečné, ale nejde o dovednost pro práci s GenAI.

Správná odpověď obvykle zmiňuje posouzení schopností modelu pro úlohu, zpřesňování promptů, revizi AI výstupu, sanitizaci dat nebo výběr modelu přiměřené velikosti.
:::

:::praxe
Sebehodnocení testera na bankovním projektu může vypadat takto. Prompty pro testovací případy píše dobře, používá strukturu z kapitoly 2. Kontextové okno chápe, dlouhé specifikace dělí na části. Revizi AI výstupu dělá, ale bez kontrolního seznamu. Doménu plateb zná dobře. Sanitizaci dat dělá ručně a občas na něco zapomene. Na výběr modelu podle velikosti úlohy nemyslí vůbec, používá vždy nejsilnější dostupný.

Z toho plynou dva konkrétní kroky. Sepsat kontrolní seznam pro revizi AI testovacích případů. A připravit si skript nebo šablonu, která v datech nahradí čísla účtů a jména zástupnými hodnotami ještě před vložením do promptu. Cvičení CV-5-04 tento postup rozepisuje.
:::

### 5.2.2 Budování schopností GenAI v testovacích týmech

Toto je studijní cíl GenAI-5.2.2 na úrovni K1. Máte si vybavit strategie, jak v testovacích týmech pěstovat AI dovednosti a podpořit tím zavedení GenAI.

Sylabus staví na jednom principu. Pro strategické školení týmů je nezbytný **hands-on approach** (praktický přístup). Teorie z přednášek nestačí. Tento princip se rozpadá na několik konkrétních prvků. Výčet se zkouší na zapamatování.

1. **Practicing with various LLMs/SLMs** (praxe s různými LLM a SLM). Tým si zkouší víc modelů, aby viděl rozdíly. Učí se technikám, ne jednomu nástroji.
2. **Structured learning paths** (strukturované vzdělávací cesty). Učení má plán a postupuje od základů k pokročilému.
3. **Gradually developing know-how through sharing** (postupný rozvoj know-how sdílením v organizaci). Znalosti se nesoustředí u jednoho člověka.
4. **Guided exercises** (řízená cvičení). Cvičení s jasným zadáním a zpětnou vazbou.
5. **Peer learning** (učení od kolegů). Kolegové si ukazují, co funguje, a navzájem si kontrolují prompty.
6. **Gradual integration of AI into daily test tasks** (postupné zapojení AI do každodenních testovacích úloh). Ne všechno najednou, ale krok po kroku.

Sylabus dále popisuje, jak se členové týmu posouvají. Začínají u základní tvorby promptů. Postupně přecházejí k cílenějším technikám, jako jsou prompty specifické pro testování.

:::pojem term="prompt pattern"
Vzor promptu. Znovupoužitelná šablona pro tvorbu účinných promptů, která vede GenAI ke konzistentním a spolehlivým výstupům (sylabus 5.2.2). Příklad: šablona pro převod uživatelského scénáře na testovací případy v Gherkinu s pevně danými sekcemi role, kontext, instrukce, formát výstupu.
:::

Poslední prvek je **community of practice** (komunita praxe). Jde o interní skupinu lidí, kteří se pravidelně scházejí kvůli společnému tématu. Sylabus popisuje, co taková komunita dělá:

- podporuje průběžné sdílení znalostí,
- na pravidelných schůzkách ukazuje úspěšná použití GenAI,
- otevřeně probírá potíže,
- zpřesňuje osvědčené postupy,
- sdílí **prompt pattern libraries** (knihovny vzorů promptů),
- dokumentuje poučení z nasazení GenAI napříč projekty a doménami.

Pomůcka: **„Ruce, Cesta, Kolegové, Vzory, Komunita.“** Ruce znamenají praktický přístup a praxi s modely. Cesta je strukturovaná vzdělávací cesta s postupným zapojením. Kolegové jsou řízená cvičení a peer learning. Vzory jsou prompt patterns. Komunita je community of practice s knihovnami vzorů a poučeními. Anglicky: Hands-on, Paths, Peers, Patterns, Communities.

:::zkouska
Správná odpověď u 5.2.2 typicky obsahuje slova „hands-on“, „gradual“, „guided exercises“, „peer learning“, „prompt patterns“ nebo „communities of practice“.

Špatné odpovědi bývají postavené na opaku jednoho z prvků:

- jen teoretické kurzy bez praxe,
- zapojit AI do všech úloh najednou místo postupně,
- volné experimentování bez struktury,
- spoléhat hlavně na externí experty a nesdílet znalosti uvnitř,
- certifikace na jeden konkrétní model místo praxe s různými modely,
- nechat dobré prompty každému testerovi pro sebe.
:::

:::praxe
V konzultační firmě s několika desítkami testerů rozptýlených po klientských projektech může budování schopností vypadat takto.

Testeři dostanou přístup ke schválenému nástroji a krátkou vzdělávací cestu: základy promptů, prompty pro testovací případy, revize AI výstupu, pravidla pro data. Každý modul končí cvičením na veřejné ukázkové aplikaci, ne na klientském systému. Jednou za měsíc se koná hodinové setkání komunity praxe. Dva lidé ukážou, co jim na projektu fungovalo a co ne. Prompty, které se osvědčily, se po revizi uloží do sdílené knihovny vzorů s popisem, k čemu slouží a na jakých datech se nesmí použít. Poučení z projektů se zapisují bez klientských detailů, aby šla sdílet i mezi týmy, které pracují pro různé klienty.

Pro Janův projekt `uctenky` (Django, React, Playwright) jde podobná knihovna založit hned. Stačí složka `prompts/` se třemi šablonami: testovací případy z uživatelského scénáře, Playwright test z testovacího případu, shrnutí výsledku běhu.
:::

### 5.2.3 Vývoj testovacích procesů v organizaci podporované AI

Toto je studijní cíl GenAI-5.2.3 na úrovni K1. Máte poznat, jak se v testovací organizaci posouvají testovací procesy a odpovědnosti při zavádění GenAI.

Sylabus říká, že integrace GenAI mění tradiční testovací procesy testerů i test manažerů. Popisuje obě role zvlášť. Rozdělení mezi role je u zkoušky důležité.

**Tester.** Tester se mění ze specialisty na návrh a provádění testů na **AI-assisted test specialist** (specialista na testování s podporou AI). Kombinuje znalost testovacích technik s dovedností vést AI a ověřovat testware, který AI vytvořila. Jeho úlohy se rozšiřují o tři věci:

1. revizi celkového výstupu AI,
2. zpřesňování promptů,
3. údržbu knihoven promptů specifických pro testování.

Pomůcka pro testera: **tři R**, Review, Refine, Repository. Revize výstupu, zpřesnění promptu, údržba knihovny.

**Test manažer.** Odpovědnosti test manažera se rozšiřují o tři oblasti:

1. vytvoření **AI-based test strategy** (testovací strategie založená na AI),
2. **AI-based risk management** (řízení rizik spojených s AI),
3. monitoring a řízení testovacích procesů založených na AI.

Test manažer se navíc zaměřuje na čtyři věci:

- vyvažovat schopnosti lidí a AI,
- zavádět **AI governance frameworks** (rámce pro správu a řízení AI) pro jednotlivé případy použití,
- zajistit, aby tým měl tradiční testovací kompetence i **AI literacy** (AI gramotnost),
- koordinovat nejen lidi, ale i **GenAI-powered test agents** (testovací agenty poháněné GenAI).

Poslední bod sylabus zdůrazňuje. Test manažer bude řídit **hybrid team** (hybridní tým) lidí a nástrojů GenAI. To vyžaduje nové manažerské dovednosti.

Pomůcka pro test manažera: **„Strategie, Rizika, Řízení“** jako tři nové odpovědnosti. K tomu čtyři zaměření: **„Rovnováha, Pravidla, Gramotnost, Hybridní tým.“**

| | Tester | Test manažer |
|---|---|---|
| Odkud | specialista na návrh a provádění testů | řídí lidi a testovací projekty |
| Kam | specialista na testování s podporou AI | řídí hybridní tým lidí a AI agentů |
| Nové úlohy | revize AI výstupu, zpřesňování promptů, údržba knihoven promptů | strategie s AI, řízení rizik AI, monitoring a řízení AI procesů |
| Zaměření | testovací techniky plus vedení a ověřování AI | rovnováha lidé a AI, governance, AI gramotnost týmu |

Tabulka ukazuje, že žádná role nezaniká. Obě se rozšiřují. Tester dál potřebuje testovací techniky, protože bez nich nepozná špatný AI výstup. Test manažer dál řídí testování, jen do něj přibyla AI.

:::pojem term="AI literacy"
AI gramotnost. Schopnost rozumět, co AI umí a neumí, jak s ní bezpečně pracovat a jak kriticky posoudit její výstup. Podle 5.2.3 má test manažer zajistit, aby ji tým měl vedle tradičních testovacích kompetencí.
:::

:::pojem term="AI-assisted test specialist"
Specialista na testování s podporou AI. Cílová podoba role testera podle 5.2.3. Spojuje znalost testovacích technik s dovedností vést AI a ověřovat testware, který vytvořila.
:::

:::zkouska
U 5.2.3 se zkouší hlavně přiřazení odpovědnosti ke správné roli.

- Revize AI výstupu, zpřesňování promptů a údržba knihoven promptů patří testerovi.
- Strategie založená na AI, řízení rizik AI, monitoring a řízení AI procesů, governance a hybridní tým patří test manažerovi.

Chyták: „tester přechází k dohledu nad testovacími procesy založenými na AI.“ Monitoring a řízení AI procesů je v sylabu u test manažera.

Další chyták: odpovědi, které z člověka dělají zbytečnost. „Test manažer se spoléhá jen na AI“, „AI agent nahradí test manažera“, „tester už nepotřebuje testovací techniky“. Sylabus naopak chce rovnováhu lidí a AI a zachování tradičních kompetencí.

A ještě jeden: test manažer nemá studovat vnitřní fungování modelů ani je dolaďovat na úrovni architektury. Jeho úlohou je strategie, rizika, řízení a governance.
:::

:::praxe
Na projektu pro pojišťovnu po půl roce používání GenAI vypadá týden testera jinak než dřív. Méně času stráví psaním testovacích případů od nuly. Více času stráví revizí návrhů, které vygeneroval schválený nástroj. Hledá v nich chybějící okrajové případy, špatně očekávané výsledky a halucinované požadavky. Když najde opakující se chybu, upraví prompt v týmové knihovně a zapíše proč.

Test manažer na stejném projektu do testovací strategie doplnil, pro které úlohy se AI používá a pro které ne. Do registru rizik přidal rizika AI, například halucinace v očekávaných výsledcích a únik dat do promptu. V reportu o postupu testování sleduje podíl AI výstupů zamítnutých při revizi. S klientem dohodl, že AI agent smí spouštět regresní sadu v testovacím prostředí, ale defekty zakládá jen člověk. To je v malém AI governance framework pro jeden případ použití.
:::

:::nad-ramec
Shetty v kurzu AI Tools for QA shrnuje budoucnost role testera podobně jako sylabus. AI podle něj nenahradí testery, ale testery, kteří s AI pracovat neumějí, nahradí ti, kteří umějí. Rozhodující je kombinace odborné znalosti a práce s AI. Bez odborné znalosti nelze posoudit, jestli je výstup správný. Ukazuje také lokální modely, které běží offline na vlastním počítači, jako jednu z cest, když firma nepovolí cloudové služby. To je praktická podoba úvahy o SLM z 5.1.3. I lokální nástroj ale ve firmě musí schválit IT, jinak jde opět o stínovou AI.
:::

### Seznamy K1 k zapamatování

Na závěr čtyři výčty, které se v kapitole zkoušejí na zapamatování. Opakujte je anglicky, protože zkouška je jen v angličtině.

**5.1.1 Risks of shadow AI (tři rizika)**

1. Information security and data privacy weaknesses
2. Compliance and regulatory issues
3. Vague intellectual property

**5.1.4 Phases of GenAI adoption (tři fáze v pořadí)**

1. Discovery
2. Initiation and usage definition
3. Utilization and iteration

Fáze mohou běžet souběžně pro různé případy použití. Je třeba řešit strach ze ztráty práce.

**5.2.2 Building GenAI capabilities (strategie budování schopností)**

- hands-on approach, practicing with various LLMs/SLMs
- structured learning paths
- gradual know-how sharing within the organization
- guided exercises and peer learning
- gradual integration of AI into daily test tasks
- progression from basic prompts to test-specific prompts
- prompt patterns as reusable templates
- internal communities of practice, prompt pattern libraries, lessons learned

**5.2.3 Shift of roles (posun rolí)**

- Tester: from test design and execution specialist to AI-assisted test specialist. New tasks: review of AI output, prompt refinement, maintenance of test-specific prompt libraries.
- Test manager: AI-based test strategy, AI-based risk management, monitoring and control of AI-based test processes. Focus: balancing human and AI capabilities, AI governance frameworks, traditional competencies plus AI literacy, coordinating GenAI-powered test agents in hybrid teams.
