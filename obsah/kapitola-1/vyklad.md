---
kapitola: 1
varianta: vyklad
nadpis: Úvod do generativní AI pro testování softwaru
podtitul: Z čeho generativní AI vychází, jak velký jazykový model zpracovává text a obraz a jak ho tester může v praxi využít.
---

První kapitola sylabu CT-GenAI v1.1 má vyhrazeno 100 minut výuky. Je to nejkratší a nejvíc teoretická kapitola celého sylabu. Neučí ještě psát prompty ani řídit rizika. Vysvětluje, co se děje uvnitř modelu, a dává slovník, na kterém stojí zbytek kurzu. Kdo tuhle kapitolu pochopí, bude v dalších kapitolách rozumět, proč model halucinuje, proč „zapomíná“ začátek dlouhého logu a proč dvakrát stejný prompt nedává stejný výsledek.

Ve zkoušce na kapitolu 1 připadá 7 otázek za 7 bodů. Jedna otázka je na úrovni K1 (zapamatovat si), a to k typům AI v oddílu 1.1.1. Zbylých šest je na úrovni K2 (porozumět, porovnat, uvést příklad). Oddíl 1.1.2 o základech LLM má dvě otázky, ostatní oddíly po jedné. Otázky na úrovni K3 v této kapitole nejsou. Kapitola obsahuje také dvě praktická cvičení, **hands-on objectives** (HO). Ta se u zkoušky nezkoušejí, ale pomáhají pochopit tokeny a multimodální prompty.

Sylabus pro kapitolu uvádí šestnáct klíčových pojmů v oddílu **Generative AI Specific Keywords**. Jsou to AI chatbot, context window, deep learning, embedding, feature, foundation LLM, generative AI, generative pre-trained transformer, instruction-tuned LLM, large language model, machine learning, multimodal model, reasoning LLM, symbolic AI, tokenization a transformer. Klasická testovací klíčová slova (Keywords) kapitola nemá žádná. Všechny pojmy jsou vysvětlené v textu a najdete je také ve slovníku kapitoly.

## 1.1 Základy generativní AI a klíčové pojmy
:::lo
GenAI-1.1.1 (K1) Recall different types of AI: symbolic AI, classical machine learning, deep learning, and generative AI
GenAI-1.1.2 (K2) Explain the basics of generative AI and large language models
GenAI-1.1.3 (K2) Distinguish between foundation, instruction-tuned and reasoning LLMs
GenAI-1.1.4 (K2) Write and execute a given prompt addressing a test task using a multimodal LLM model
:::

**Generative AI** (generativní AI, zkráceně GenAI) je oblast umělé inteligence, která používá velké předem natrénované modely a vytváří z nich nový obsah. Výstup se podobá tomu, co by vytvořil člověk. Může to být text, obrázek, programový kód, ale i zvuk nebo video. Slovo „generativní“ je tu podstatné. Systém nic jen netřídí ani nevybírá ze seznamu, ale skládá nový výstup, který předtím v této podobě neexistoval.

:::pojem term="generative AI"
Typ AI, který pomocí modelů strojového učení vytváří nový obsah (text, obrázky, kód) podobný obsahu vytvořenému člověkem.
:::

**Large language model** (velký jazykový model, LLM) je model generativní AI, který byl předtrénován na obrovském množství textu. Díky tomu umí z promptu poznat kontext a odpovědět tak, aby odpověď k zadání dávala smysl. ChatGPT, Claude, Gemini nebo Copilot jsou aplikace, které nad takovými modely stojí. Samotný model a aplikace, přes kterou s ním mluvíte, jsou dvě různé věci. K tomuto rozdílu se kapitola vrátí v oddílu 1.2.2.

:::pojem term="large language model (LLM)"
Model generativní AI předtrénovaný na velmi velkém množství textových dat, který rozumí přirozenému jazyku a vytváří text podobný lidskému.
:::

Sylabus hned v úvodu jmenuje tři pojmy, které se pak vracejí celou kapitolou. Prvním je **tokenization** (tokenizace), tedy rozdělení textu na menší jednotky, se kterými model počítá. Druhým je **context window** (kontextové okno), tedy omezení, kolik informace model najednou bere v úvahu. Třetím je **multimodal model** (multimodální model), který zpracuje víc druhů dat než jen text, například obrázky nebo zvuk. Všechny tři pojmy jsou podrobně vysvětlené dál v oddílech 1.1.2 a 1.1.4.

V testování může LLM pomoct v celém testovacím procesu. Sylabus uvádí revizi a zlepšování akceptačních kritérií, generování testovacích případů a testovacích skriptů, hledání potenciálních defektů, analýzu vzorců v defektech, tvorbu syntetických testovacích dat a podporu při psaní dokumentace. Podrobný seznam schopností přijde v oddílu 1.2.1.

### 1.1.1 Spektrum AI: symbolická AI, klasické strojové učení, hluboké učení a generativní AI

Umělá inteligence není jedna technologie. Je to široký obor, ve kterém vedle sebe žijí různé přístupy. Každý řeší problémy jinak a každý má jiné silné a slabé stránky. Sylabus vybírá čtyři z nich: symbolickou AI, klasické strojové učení, hluboké učení a generativní AI. Další přístupy existují, ale do rozsahu sylabu nepatří.

### Symbolická AI

**Symbolic AI** (symbolická AI) napodobuje lidské rozhodování pomocí pravidel. Znalost je v ní zapsaná jako symboly a logická pravidla typu „když platí A a B, pak udělej C“. Pravidla píše člověk, typicky odborník na danou oblast. Systém se sám nic neučí. Jen pravidla vyhodnocuje.

Z testování znáte symbolickou AI lépe, než by se mohlo zdát. Rozhodovací tabulka pro schválení úvěru je přesně taková sada pravidel. Kdyby banka napsala program, který podle věku žadatele, výše příjmu a historie splácení rozhoduje „schválit, zamítnout, poslat ke schválení člověku“, šlo by o symbolickou AI. Stejně fungují starší chatboti, kteří reagují na klíčová slova předem připravenou odpovědí. Výhodou je, že rozhodnutí lze vysvětlit a otestovat klasickými technikami. Nevýhodou je, že systém nezvládne situaci, na kterou nikdo nenapsal pravidlo.

:::pojem term="symbolic AI"
Přístup k AI, který modeluje uvažování pomocí symbolů, pravidel a strukturované znalosti. Pravidla zapisuje člověk, systém se z dat neučí.
:::

### Klasické strojové učení

**Machine learning** (strojové učení, ML) obrací logiku. Pravidla nepíše člověk, ale systém je odvodí z dat. Sylabus mluví o **classical machine learning** (klasické strojové učení) a popisuje ho jako přístup řízený daty, který vyžaduje tři kroky. Prvním je příprava dat, tedy sběr, čištění a označení příkladů. Druhým je výběr příznaků. Třetím je trénování modelu.

Pojem **feature** (příznak) je jedním z klíčových pojmů kapitoly. Příznak je jedna měřitelná vlastnost vstupních dat. Model se z příznaků učí a podle nich pak předpovídá. U klasického ML vybírá příznaky člověk. Představte si model, který má předpovídat, ve kterém modulu aplikace se nejspíš objeví defekt. Člověk rozhodne, že vstupem budou příznaky jako počet řádků kódu, počet změn za poslední sprint, počet autorů a počet dřívějších defektů v modulu. Model se z historických dat naučí, které kombinace hodnot vedou k defektům.

Sylabus uvádí jako příklady použití v testování kategorizaci defektů a předpovídání softwarových problémů. Model může například automaticky zařadit nový report o defektu do kategorie „UI“, „výkon“ nebo „data“ podle toho, jak byly zařazené tisíce starších reportů.

:::pojem term="feature"
Příznak, tedy jedna měřitelná vlastnost vstupních dat, kterou algoritmus strojového učení používá při trénování i při předpovědi.
:::

:::pojem term="machine learning (ML)"
Proces, při kterém se systém pomocí výpočetních technik učí z dat nebo ze zkušenosti, místo aby dostal pevně napsaná pravidla.
:::

### Hluboké učení

**Deep learning** (hluboké učení) je podmnožina strojového učení. Používá **neural networks** (neuronové sítě) s mnoha vrstvami. Podstatný rozdíl proti klasickému ML je v příznacích. Hluboké učení se příznaky naučí z dat samo, člověk je nemusí ručně definovat. Proto zvládne velmi velké a složité datové sady, jako jsou obrázky, video, zvuk nebo text, kde by ruční výběr příznaků byl prakticky nemožný.

Sylabus přidává praktickou výhradu. I hluboké učení v praxi často potřebuje člověka. Někdo musí data anotovat (označit, co je na obrázku), někdo ladí model a někdo musí ověřit výsledky. Automatické učení příznaků tedy neznamená, že lidská práce úplně zmizí.

Příklad z testování: model, který na snímku obrazovky pozná tlačítko, textové pole nebo chybovou hlášku. Nikdo mu neřekl, že tlačítko má obdélníkový tvar a text uprostřed. Naučil se to z velkého množství označených snímků.

:::pojem term="deep learning"
Strojové učení, které používá neuronové sítě s více vrstvami a samo se z dat učí příznaky.
:::

### Generativní AI

Generativní AI staví na technikách hlubokého učení. Naučí se vzorce z trénovacích dat a podle nich vytváří nový obsah. LLM umí psát text, generovat kód a napodobovat uvažování nebo řešení problémů, ale jen v rozsahu toho, co se naučil.

Vztah mezi přístupy si lze představit jako vnořené množiny. Strojové učení je část AI. Hluboké učení je část strojového učení. Generativní AI používá techniky hlubokého učení. Symbolická AI stojí vedle, protože se z dat neučí.

```text
Umělá inteligence (AI)
├── Symbolická AI          pravidla a symboly, píše je člověk
└── Strojové učení (ML)    učí se z dat
    ├── Klasické ML        člověk vybírá příznaky (feature selection)
    └── Hluboké učení      neuronové sítě, příznaky se učí samy
        └── Generativní AI vytváří nový obsah (LLM, generátory obrázků)
```

Následující tabulka shrnuje, čím se přístupy liší a jak se mohou objevit v testování.

| Typ AI | Jak získá znalost | Typický příklad v testování |
|---|---|---|
| Symbolická AI | pravidla napíše člověk | pravidlový systém pro rozhodování o úvěru, chatbot na klíčová slova |
| Klasické ML | učí se z připravených dat, příznaky vybírá člověk | kategorizace defektů, předpověď rizikových modulů |
| Hluboké učení | neuronové sítě se příznaky učí samy | rozpoznání prvků GUI na snímku obrazovky |
| Generativní AI | předtrénovaný model vytváří nový obsah | návrh testovacích případů, testovacích dat, shrnutí logu |

Sylabus uzavírá oddíl důležitou myšlenkou. Hlavní výhoda generativní AI pro testování je v tom, že používá předtrénované modely. Ty lze nasadit přímo na testovací úlohu bez další fáze trénování. U klasického ML byste nejdřív museli nasbírat a označit data a model natrénovat. U LLM stačí napsat prompt. Tahle výhoda ale přináší rizika, jako jsou halucinace nebo únik dat, a těm se věnuje kapitola 3.

:::praxe
Banka chce automaticky třídit příchozí reporty o defektech podle komponenty. S klasickým ML by tým musel vzít několik tisíc historických reportů, označit je, vybrat příznaky (slova v názvu, modul, prostředí) a model natrénovat. S LLM může tým poslat report do modelu s instrukcí „zařaď do jedné z kategorií: platby, karty, klientská zóna, reporting“ a výsledek použít hned. Na interních datech banky to ale smí udělat jen přes model schválený pro firemní data, nikdy přes veřejný chatbot.
:::

:::zkouska
Otázka k 1.1.1 je na úrovni K1. Typicky přiřazujete popis k typu AI. Stačí znát jeden rozlišující znak každého typu. Symbolická AI pracuje s pravidly. Klasické ML vyžaduje přípravu dat a ruční výběr příznaků (feature selection). Hluboké učení používá neuronové sítě a příznaky se učí samo. Generativní AI používá hluboké učení a vytváří nový obsah. Nejčastější záměna je mezi klasickým ML a hlubokým učením: rozhoduje, kdo určuje příznaky.
:::

:::nad-ramec
Symbolická AI je nejstarší z těchto přístupů. Expertní systémy postavené na pravidlech byly rozšířené v 70. a 80. letech. Strojové učení se prosadilo s dostupností dat, hluboké učení s výkonem grafických karet po roce 2010. Generativní LLM v dnešní podobě se rozšířily po roce 2022. V praxi se přístupy kombinují. Aplikace na LLM často obsahuje i pevná pravidla, například kontrolu formátu výstupu.
:::

### 1.1.2 Základy generativní AI a LLM

Tento oddíl má ve zkoušce dvě otázky a je nejobsáhlejší v kapitole. Vysvětluje, jak LLM vzniká, jak převádí text na čísla, jak generuje odpověď a jaké z toho plynou vlastnosti, se kterými musí tester počítat.

### Generative pre-trained transformer a malé jazykové modely

LLM vycházejí z modelu hlubokého učení, který se jmenuje **generative pre-trained transformer** (GPT). Každé slovo názvu něco říká. „Generative“ znamená, že model vytváří nový text. „Pre-trained“ znamená, že byl předem natrénován na velké sadě dat, ještě než ho kdokoli použil. „Transformer“ je název architektury neuronové sítě, o které je řeč níže. Trénovací data tvoří knihy, články, webové stránky a další texty.

:::pojem term="generative pre-trained transformer (GPT)"
Model hlubokého učení postavený na architektuře transformer, předtrénovaný na velkém množství textu, aby rozuměl textu a vytvářel text podobný lidskému.
:::

Zkratka GPT je i v názvu produktu ChatGPT, ale pojem je obecný. Na stejném principu stojí i modely jiných firem.

Vedle velkých modelů existují **small language models** (malé jazykové modely, SLM). Mají výrazně méně **parameters** (parametrů), tedy vnitřních číselných vah, které se model naučil při trénování. Jsou navržené jako lehké a zaměřené řešení. Spustíte je na slabším hardwaru, často i lokálně na notebooku nebo na vlastním serveru. Odpovídají rychleji a provoz stojí méně. Za to obvykle zvládnou užší okruh úloh než velký model. Pro testera to může být důležité, když data nesmějí opustit firemní síť. SLM se podrobněji věnují kapitoly 4 a 5.

### Tokenizace

Neuronová síť pracuje jen s čísly. Text proto musí model nejdřív převést do číselné podoby. Sylabus k tomu uvádí dva pojmy: tokenizaci a embeddingy. Tokenizace je první krok.

**Tokenization** (tokenizace) rozdělí text na menší jednotky, kterým se říká **tokens** (tokeny). Token může být jeden znak, část slova nebo celé slovo. Častá krátká anglická slova bývají jeden token. Delší nebo méně častá slova se rozdělí na několik částí. Interpunkce, mezery na začátku slov, čísla a speciální znaky se také stávají tokeny. Model nejdřív tokenizuje celý vstup. Každý token pak zpracuje samostatně, ale tak, aby zůstal zachovaný kontext celé věty.

Jednoduchý příklad ukazuje, jak může tokenizace vypadat. Přesné dělení se liší podle modelu, protože každý model používá svůj tokenizér a svůj slovník tokenů.

```text
Vstup:   Verify that the login button is disabled.
Tokeny:  [Verify] [ that] [ the] [ login] [ button] [ is] [ disabled] [.]
Počet:   8 tokenů

Vstup:   Ověřte, že tlačítko Přihlásit je neaktivní.
Tokeny:  [Ov] [ěř] [te] [,] [ že] [ tla] [čít] [ko] [ Př] [ihl] [ásit] [ je] [ ne] [akt] [ivn] [í] [.]
Počet:   přibližně 17 tokenů (ilustrace, skutečné dělení závisí na tokenizéru)
```

Z příkladu jsou vidět tři věci, které tester potřebuje vědět. Zaprvé, počet tokenů není počet slov. U anglického textu vychází v průměru zhruba jeden token na čtyři znaky. Zadruhé, čeština se obvykle rozpadá na víc tokenů než stejně dlouhá angličtina. Tokenizéry vznikaly hlavně nad anglickými daty a česká slova s diakritikou a skloňováním v jejich slovníku tak často nejsou. Zatřetí, strukturovaná data jako JSON, XML, logy nebo kód obsahují hodně závorek, uvozovek a identifikátorů. Každý z nich zabere token, takže technický text bývá „dražší“, než by odpovídalo jeho délce.

Tokeny jsou měrnou jednotkou pro všechno podstatné. Počítá se v nich velikost kontextového okna. Účtuje se v nich cena za použití modelu přes API, zvlášť za vstupní a zvlášť za výstupní tokeny. A počet tokenů ovlivňuje i rychlost odpovědi.

:::pojem term="tokenization"
Rozdělení textu na menší jednotky (tokeny), se kterými jazykový model pracuje. Token může být znak, část slova nebo celé slovo.
:::

### Embeddingy

Tokenizace text rozdělí, ale samotné rozdělení ještě neříká nic o významu. Druhý krok proto tvoří **embeddings** (embeddingy, vektorové reprezentace). Každý token se převede na vektor, tedy řadu čísel v prostoru o mnoha rozměrech. Rozměrů bývají stovky až tisíce. Vektor zachycuje význam tokenu, jeho gramatickou roli (syntaxi) a vztahy k ostatním tokenům v kontextu.

Podstatná vlastnost embeddingů je blízkost. Tokeny s podobným významem nebo podobnou rolí v textu mají vektory blízko sebe. Slova „defect“, „bug“ a „fault“ budou v tomto prostoru u sebe. Slovo „banana“ bude daleko. Díky tomu model chápe vztahy mezi slovy, drží kontext a tvoří souvislé odpovědi, které k zadání sedí.

Inženýrovi pomůže analogie se souřadnicemi. Bod v trojrozměrném prostoru popisují tři čísla a vzdálenost dvou bodů lze spočítat. Embedding je totéž, jen rozměrů je mnohem víc a každý zachycuje nějaký aspekt významu. Žádný rozměr nemá lidsky čitelný název. Model si je vytvořil sám při trénování.

:::pojem term="embedding"
Číselná reprezentace tokenu v podobě vektoru ve vícerozměrném prostoru. Zachycuje význam, syntaxi a kontextové vztahy. Tokeny s podobným významem mají blízké vektory.
:::

:::zkouska
Tokenizaci a embeddingy zkouška ráda prohazuje. Tokenizace text *rozděluje* na stavební kameny (tokeny). Embedding token *převádí na vektor*, který nese význam. Když možnost mluví o „high-dimensional vectors“ nebo „semantic relationships“, popisuje embedding, ne tokenizaci. Když mluví o předpovědi dalšího tokenu, popisuje práci transformeru při inferenci, ne tokenizaci.
:::

:::nad-ramec
Embeddingy se nepoužívají jen uvnitř LLM. Stejný princip stojí za vyhledáváním podle významu. Dokumenty nebo jejich části se převedou na vektory a uloží do vektorové databáze. Dotaz se převede na vektor a hledají se nejbližší dokumenty. Na tom je postavené RAG, generování rozšířené o vyhledávání, kterému se věnuje kapitola 4.
:::

### Transformer a předpověď dalšího tokenu

LLM používají architekturu neuronové sítě, která se jmenuje **transformer**. Transformer je silný v jazykových úlohách, protože zpracovává kontext dlouhých úseků textu a učí se, jak spolu jednotlivé tokeny souvisejí. Mechanismus, který to umožňuje, se jmenuje **self-attention** (sebepozornost). Pro každý token model spočítá, jak moc má při jeho zpracování „dávat pozor“ na každý jiný token ve vstupu. Ve větě „Tlačítko Odeslat se po kliknutí nezaktivovalo, protože formulář nebyl validní“ tak model propojí slovo „nezaktivovalo“ se slovem „tlačítko“, i když mezi nimi stojí jiná slova.

:::pojem term="transformer"
Architektura modelu hlubokého učení, která pomocí mechanismu self-attention zachycuje vztahy mezi tokeny i ve vzdálených částech vstupu.
:::

Při **inference** (inferenci), tedy při použití natrénovaného modelu, LLM předpovídá další token v posloupnosti. Odpověď nevzniká najednou. Model vezme prompt, spočítá pravděpodobnosti pro všechny možné další tokeny, jeden vybere a připojí ho na konec. Pak celý postup opakuje s prodlouženým textem, dokud odpověď nedokončí. Proto vidíte, jak odpověď v chatu „naskakuje“ postupně.

Z toho plyne věta, kterou sylabus zdůrazňuje a která se vrací v kapitole 3. Transformer generuje text, který je statisticky pravděpodobný vzhledem k trénovacím datům a promptu. Pravděpodobný ale neznamená správný. Model nemá vestavěnou kontrolu pravdivosti. Když se v trénovacích datech často objevuje určitá kombinace slov, model ji nabídne i tam, kde neplatí.

:::praxe
Tester požádá LLM o automatizovaný test pro REST API aplikace uctenky a do promptu nevloží specifikaci API. Model vygeneruje test, který volá endpoint `/api/v1/receipts/upload` s hlavičkou `X-Api-Key`. Kód vypadá profesionálně a dává smysl. Aplikace ale žádný takový endpoint nemá a autentizuje se jinak. Model jen poskládal nejpravděpodobnější podobu API podle tisíců podobných projektů, které viděl při trénování. Test je plauzibilní, ale nepoužitelný. Řešení je dát modelu skutečnou specifikaci, třeba schéma OpenAPI, a výsledek vždy zkontrolovat.
:::

### Nedeterministické chování

LLM se chovají **non-deterministic** (nedeterministicky). Stejný vstup zadaný několikrát může vést k různým výstupům. Sylabus uvádí dvě hlavní příčiny. První je pravděpodobnostní povaha inference. Model nevybírá vždy nejpravděpodobnější token, ale vzorkuje z rozdělení pravděpodobností. Druhou příčinou je nastavení **hyperparameters** (hyperparametrů), které vzorkování ovlivňují. Nejznámější z nich je teplota (temperature), které se podrobněji věnuje kapitola 3.

Pro testera má nedeterminismus dva důsledky. Když LLM používáte jako pomocníka, třeba pro návrh testovacích případů, dvakrát spuštěný stejný prompt dá dvě různé sady. Ani jedna nemusí být chybná, ale nejsou stejné. Když testujete aplikaci, která LLM obsahuje, nemůžete očekávaný výsledek porovnávat znak po znaku. Musíte ověřovat vlastnosti odpovědi, například jestli obsahuje požadovanou informaci, jestli má správný formát a jestli neobsahuje zakázaný obsah.

:::praxe
Šmoula odpovídá přes Telegram a na pozadí volá Claude Code. Kdyby jeho automatický test kontroloval, že odpověď na zprávu „Jaké je počasí?“ zní přesně „Dnes bude slunečno.“, padal by náhodně. Rozumnější test ověří, že odpověď přišla do určité doby, není prázdná, je v češtině a neobsahuje text chybové výjimky.
:::

### Kontextové okno

**Context window** (kontextové okno) je množství předchozího textu, které model může vzít v úvahu, když generuje odpověď. Měří se v tokenech. Do okna se počítá všechno, co model v daném okamžiku „vidí“: systémový prompt, celá dosavadní konverzace, vložené dokumenty a také odpověď, kterou právě generuje.

Velké kontextové okno umožňuje modelu držet souvislosti v dlouhém textu. Sylabus uvádí jako příklad analýzu velkých testovacích logů. Když se celý log do okna vejde, model může spojit chybu na řádku 200 s varováním na řádku 15. Větší okno má ale cenu. S počtem tokenů roste výpočetní náročnost a doba zpracování. Delší vstup je pomalejší a přes API i dražší.

Když vstup okno přesáhne, model jeho část nevidí. Podle aplikace to může znamenat, že se nejstarší část konverzace zahodí, že se text ořízne, nebo že aplikace vrátí chybu. Chatovací aplikace staré zprávy často potichu zkrátí nebo shrnou. Uživatel pak má dojem, že model „zapomněl“ pokyn ze začátku rozhovoru. Ve skutečnosti ten pokyn už nebyl v okně.

```text
Kontextové okno (pevná velikost v tokenech)
                 ┌────────────────────────────────────────┐
[pokyn: formát ] │ [požadavek 1] [odpověď 1] ... [dotaz N]│ → odpověď
  už mimo okno   └────────────────────────────────────────┘
```

:::pojem term="context window"
Rozsah textu měřený v tokenech, který model bere v úvahu při generování odpovědi. Co se do okna nevejde, model nevidí.
:::

:::praxe
Tester vloží do chatbota výstup z nočního běhu Playwright testů aplikace uctenky, celkem 40 000 řádků. Požádá o seznam všech selhání a jejich pravděpodobných příčin. Model vrátí shrnutí, ve kterém chybí tři selhání z prvních minut běhu. Příčinou je kontextové okno. Lepší postup je log nejdřív zkrátit (vybrat jen řádky s FAIL a ERROR a jejich okolí), nebo ho rozdělit na části a každou analyzovat zvlášť. Obecně platí, že do okna má jít jen to, co model k úloze potřebuje.
:::

:::zkouska
Kontextové okno omezuje, kolik textu model najednou bere v úvahu. Neřídí pořadí zpracování, rychlost tokenizace ani to, jestli model umí pracovat s více dokumenty. Typický scénář v otázce: model při práci s dlouhým dokumentem ignoruje informace ze začátku. Správné vysvětlení je, že starší tokeny vypadly z kontextového okna. Nedeterminismus by vysvětloval rozdílné odpovědi na stejný vstup, ne ztrátu informace z dlouhého textu.
:::

### HO-1.1.2: Tokenizace a počet tokenů

První praktické cvičení kapitoly (úroveň H1, řízené cvičení) má dvě části. V první části vezmete tokenizér a rozdělíte jím ukázkový text. Sledujete, jak se rozdělí slova, interpunkce a fráze, a hledáte pravidelnosti. Ve druhé části měříte počet tokenů u různých vstupů a uvažujete, jak počet ovlivňuje práci s modelem, hlavně vzhledem k limitu kontextového okna a k nákladům. Cílem je umět odhadnout, jak struktura a délka vstupu ovlivní interakci s LLM. Podrobné zadání je v sadě cvičení ke kapitole.

Pro tokenizaci lze použít webový tokenizér OpenAI, který ukazuje tokeny barevně. V Pythonu stejnou práci udělá knihovna `tiktoken`. Anthropic nabízí počítání tokenů přes své API. Výsledky se mezi modely liší, protože každý dodavatel používá jiný tokenizér.

```python
import tiktoken

enc = tiktoken.get_encoding("o200k_base")
for text in ["Verify that the login button is disabled.",
             "Ověřte, že tlačítko Přihlásit je neaktivní."]:
    tokens = enc.encode(text)
    print(len(tokens), [enc.decode([t]) for t in tokens])
```

### 1.1.3 Základní, instrukční a uvažující LLM

LLM nevznikají v jednom kroku. Procházejí několika fázemi trénování a každá je specializovanější než předchozí. Podle toho sylabus rozlišuje tři kategorie: základní (foundation) LLM, LLM vyladěné na instrukce a uvažující (reasoning) LLM.

### Základní (foundation) LLM

**Foundation LLM** (základní LLM, synonymum **base LLM**) je univerzální model natrénovaný na obrovské a pestré sadě dat. Sylabus v oddílu 1.1.3 uvádí text, kód, obrázky a další modality. Díky rozsáhlému předtrénování se dá použít v mnoha oblastech, například ve zpracování přirozeného jazyka (natural language processing, NLP), v počítačovém vidění nebo v rozpoznávání řeči. Je silný a flexibilní, ale pro konkrétní úlohu ho obvykle musíte dál přizpůsobit.

Základní model se naučil hlavně jedno: pokračovat v textu. Když mu napíšete „Napiš pět testovacích případů pro přihlášení“, nemusí je napsat. Může v textu pokračovat třeba dalšími podobnými zadáními, protože tak podobný text vypadal v trénovacích datech. Rozumí jazyku, ale nebyl naučen plnit pokyny.

:::pojem term="foundation LLM"
Univerzální model předtrénovaný na velkém a pestrém množství dat, který umí předpovídat další token. Pro konkrétní úlohy ho je obvykle nutné dál přizpůsobit. Synonymum: base LLM.
:::

### LLM vyladěné na instrukce

**Instruction-tuned LLM** (LLM vyladěný na instrukce) vzniká ze základního modelu doladěním. Dolaďuje se na datové sadě, ve které je každý prompt spárovaný s očekávanou odpovědí. Model se tak naučí, že na pokyn má reagovat splněním pokynu. Trénink optimalizuje tři věci: dodržení zadané úlohy, plnění instrukcí a souvislost odpovědi. Výsledkem je model, který lépe chápe záměr uživatele a jedná podle něj. Slovník sylabu dodává, že trénink bývá posílený zpětnou vazbou, která odměňuje správné odpovědi.

Takové modely jsou dobré tam, kde potřebujete přesně dodržet zadání: formát, šablonu, délku, strukturu. Typicky převod uživatelského scénáře do testovacích případů v syntaxi Gherkin, vyplnění šablony reportu o defektu nebo vygenerování testovacích dat jako JSON podle daného schématu. Sylabus o nich říká, že se jim někdy říká také „non-reasoning“ modely.

:::pojem term="instruction-tuned LLM"
Základní LLM doladěný na dvojicích prompt a očekávaná odpověď, aby spolehlivě plnil instrukce uživatele. Často posílený zpětnou vazbou.
:::

### Uvažující (reasoning) LLM

**Reasoning LLM** (uvažující LLM) navazuje na model vyladěný na instrukce a dál posiluje strukturované myšlení: logické vyvozování, řešení problémů o více krocích a uvažování v řetězci kroků (**chain-of-thought reasoning**). Dotrénovává se na pečlivě vybraných úlohách, které vyžadují porozumění kontextu, mezikroky a syntézu složitých informací. Hodí se proto na úlohy s vysokou kognitivní zátěží, včetně technických oblastí.

V praxi poznáte uvažující model podle toho, že před odpovědí „přemýšlí“. Vytváří si mezikroky, ověřuje je a teprve potom odpoví. Je to pomalejší a spotřebuje to víc tokenů, a proto i víc peněz. Na jednoduché úlohy se tedy nevyplatí.

:::pojem term="reasoning LLM"
LLM, který staví na modelu vyladěném na instrukce a je dál trénován na logické vyvozování a řešení problémů o více krocích. Hodí se na kognitivně náročné úlohy.
:::

Následující tabulka porovnává všechny tři kategorie.

| Kategorie | Jak vzniká | Silná stránka | Omezení |
|---|---|---|---|
| Foundation LLM | předtrénování na obrovských pestrých datech | univerzálnost, široké znalosti | neplní spolehlivě pokyny, potřebuje přizpůsobení |
| Instruction-tuned LLM | doladění na dvojicích prompt a odpověď | plní instrukce, drží formát a šablonu | slabší u vícekrokových úvah |
| Reasoning LLM | další trénink na úlohách s mezikroky | logika, vícekroková analýza, syntéza | pomalejší, dražší, na rutinu zbytečný |

V testování se podle sylabu používají modely vyladěné na instrukce i uvažující modely. Volba závisí na složitosti úlohy a na tom, kolik uvažování vyžaduje. Rutinní úlohy s jasným zadáním zvládne model vyladěný na instrukce rychle a levně. Úlohy, kde je potřeba propojit víc zdrojů, najít rozpor nebo zvážit varianty, patří uvažujícímu modelu.

:::praxe
Dvě úlohy ze stejného projektu pojišťovny ukazují rozdíl. První: „Převeď těchto 12 akceptačních kritérií na scénáře v Gherkinu podle naší šablony.“ Zadání je jasné, jde hlavně o dodržení formátu. Stačí model vyladěný na instrukce. Druhá: „Tady je 150 reportů o defektech z posledních tří vydání a seznam změn v kódu. Najdi, které oblasti aplikace jsou nejrizikovější, a navrhni, kam soustředit regresní testy.“ Model musí data propojit, hledat trendy a vyvodit doporučení. Tady se vyplatí uvažující model.
:::

:::zkouska
Otázky k 1.1.3 obvykle dávají testovací úlohu a ptají se, která kategorie se na ni hodí nejlépe. Přesné dodržení šablony nebo syntaxe (Gherkin, JSON schéma) vede na instruction-tuned LLM. Syntéza více zdrojů, hledání trendů a vícekroková analýza vedou na reasoning LLM. Foundation LLM je odpověď jen tam, kde jde o obecný, nepřizpůsobený model. Pozor na past „uvažující model je vždy nejlepší“: na formátovací úlohy není potřeba a je dražší.

Některé kurzy podávají ladění na instrukce jako něco, co si dělá tým u sebe nad vlastními pravidly projektu, nebo tvrdí, že uvažující model sám prohledává interní databáze. Podle sylabu je ladění na instrukce obecný krok vývoje modelu (dvojice prompt a odpověď) a uvažující model se vyznačuje vícekrokovým logickým uvažováním, ne přístupem k datům.
:::

:::nad-ramec
Hranice mezi kategoriemi se v produktech stírají. Řada současných modelů má přepínatelný režim přemýšlení (thinking), takže stejný model pracuje jednou jako „non-reasoning“ a jednou jako uvažující. Čisté základní modely běžný uživatel v chatu skoro nepotká. Dodavatelé je zveřejňují hlavně pro výzkum a pro firmy, které si model dolaďují samy. Doladění modelu (fine-tuning) se věnuje kapitola 4.
:::

### 1.1.4 Multimodální LLM a modely pro obraz a jazyk

**Multimodal model** (multimodální model) zpracovává a vytváří obsah ve více druzích dat, kterým se říká **modalities** (modality). Modalitou je text, obraz, zvuk nebo video. Multimodální LLM rozšiřují klasický transformer tak, aby kromě textu přijaly i další modality. Trénují se na velkých a pestrých datových sadách, ze kterých se naučí vztahy mezi různými druhy dat. Například že obrázek s červeným rámečkem kolem pole odpovídá textu „pole je povinné a nebylo vyplněno“.

Tokenizace se přizpůsobí každé modalitě. Text se dělí na tokeny jako v oddílu 1.1.2. Obrázek se pomocí modelu pro obraz a jazyk převede na embeddingy. Ty pak zpracuje transformer společně s embeddingy textu. Transformer tak pracuje s jedním společným proudem vektorů, ať pocházejí z čehokoli.

:::pojem term="multimodal model"
Model generativní AI, který zpracovává a vytváří obsah ve více druzích dat, například v textu, obrazech a zvuku.
:::

**Vision-language model** (model pro obraz a jazyk, VLM) je podmnožina multimodálních LLM. Konkrétně propojuje vizuální a textovou informaci. Sylabus uvádí tři typické úlohy. **Image captioning** (popis obrázku) znamená vytvořit textový popis toho, co je na obrázku. **Visual question answering** (odpovídání na otázky k obrázku) znamená odpovědět na dotaz, například „Je na snímku vidět chybová hláška?“. Třetí úlohou je analýza souladu mezi textovým a vizuálním vstupem, například jestli snímek obrazovky odpovídá popisu v uživatelském scénáři.

:::pojem term="vision-language model (VLM)"
Podmnožina multimodálních modelů, která společně zpracovává obraz a text a propojuje je, například při popisu obrázku nebo odpovídání na otázky k obrázku.
:::

```text
Multimodální LLM (text, obraz, zvuk, video ...)
└── Model pro obraz a jazyk (VLM)   jen obraz + text
```

Pro testování přinášejí multimodální modely, hlavně ty doplněné o VLM, velké možnosti. Umí analyzovat vizuální prvky aplikace, jako jsou snímky obrazovky a drátěné modely GUI (wireframy). Zároveň čtou k nim patřící text, například report o defektu nebo uživatelský scénář. Tester tak může hledat rozdíly mezi očekávaným výsledkem a tím, co je skutečně vidět na snímku. Modely také umí vytvořit testovací případy, které kombinují textová data a vizuální podněty, a tím zvýšit pokrytí.

:::praxe
V aplikaci uctenky existuje uživatelský scénář: „Jako uživatel chci po nahrání účtenky vidět rozpoznanou částku, datum a obchod, abych je mohl před uložením opravit.“ Tester pořídí snímek obrazovky po nahrání účtenky a vloží ho do multimodálního modelu spolu se scénářem. Model upozorní, že na snímku chybí pole pro obchod a datum se zobrazuje jen jako text bez možnosti úpravy. Obojí je rozpor se scénářem. Tester nález ověří ručně a teprve potom založí report o defektu.
:::

### HO-1.1.4: Multimodální prompt s textem a obrázkem

Druhé praktické cvičení kapitoly (úroveň H1) má dva kroky. V prvním si projdete zadaný prompt a vstupní data, tedy text a obrázek. Ve druhém prompt spustíte v multimodálním LLM, vložíte obrázek i text a zkontrolujete odpověď modelu. Cvičení má ukázat přínosy i úskalí multimodálního přístupu. Ukázkový prompt může vypadat takto:

```text
Role: Jsi zkušený tester webových aplikací.
Kontext: Přikládám snímek obrazovky přihlašovací stránky a akceptační kritéria.
Akceptační kritéria:
1. Stránka obsahuje pole E-mail a Heslo a tlačítko Přihlásit.
2. Tlačítko Přihlásit je neaktivní, dokud nejsou obě pole vyplněná.
3. Pod formulářem je odkaz Zapomenuté heslo.
4. Chybová hláška se zobrazuje červeně pod polem, kterého se týká.
Úkol: Porovnej snímek s každým kritériem. U každého napiš SPLNĚNO, NESPLNĚNO
nebo NELZE Z OBRÁZKU OVĚŘIT a jednou větou zdůvodni.
Formát: tabulka se sloupci Kritérium | Stav | Zdůvodnění.
```

Úskalí se ukážou rychle. Model může přehlédnout drobný text nebo špatně přečíst text v nízkém rozlišení. Může si „domyslet“ prvek, který na snímku není. Ze statického obrázku nepozná chování, třeba jestli je tlačítko neaktivní, pokud to nepozná z barvy. Proto je v promptu stav NELZE Z OBRÁZKU OVĚŘIT. Dalším úskalím je ochrana dat. Snímek obrazovky z testovacího prostředí banky může obsahovat skutečná klientská data a do veřejného modelu nepatří.

:::zkouska
Vztah je jednosměrný: modely pro obraz a jazyk (VLM) jsou podmnožinou multimodálních LLM, ne naopak. Pojmy nejsou synonyma. Multimodální LLM je širší kategorie, která může zahrnovat i zvuk a video. Otázka k 1.1.4 se může ptát i na použití v testování: porovnání snímku obrazovky nebo wireframu s textem (uživatelský scénář, report o defektu, očekávaný výsledek).
:::

:::nad-ramec
Znění studijního cíle GenAI-1.1.4 je neobvyklé. Je zařazený jako K2 (porozumět), ale formulovaný slovesy „write and execute“, která odpovídají spíš praktickému cvičení. Ve zkoušce lze proto čekat otázku na porozumění, tedy co multimodální model a VLM umí a k čemu se v testování hodí, ne na samotné psaní promptu.
:::

## 1.2 Využití generativní AI v testování: základní principy
:::lo
GenAI-1.2.1 (K2) Give examples of key LLM capabilities for test tasks
GenAI-1.2.2 (K2) Compare interaction models when using GenAI for software testing
:::

Druhá polovina kapitoly přechází od toho, jak LLM funguje, k tomu, k čemu ho tester použije. Sylabus shrnuje silné stránky LLM do šesti činností. Modely dobře zpracovávají přirozený jazyk i kód. Generují souvislý text a kód. Odpovídají na otázky. Shrnují informace. Překládají mezi jazyky. A v multimodálním režimu analyzují obrázky.

Testeři ve všech rolích mohou GenAI využít dvěma způsoby, které se navzájem doplňují. Prvním je AI chatbot, který okamžitě odpovídá na dotazy. Druhým jsou aplikace postavené na LLM, které jsou integrované do testovacích nástrojů. Oba způsoby rozebírá oddíl 1.2.2.

### 1.2.1 Hlavní schopnosti LLM pro testovací úlohy

LLM umí interpretovat požadavky, specifikace, snímky obrazovky, kód, testovací případy a reporty o defektech. Pomáhají proto pochopit a vyjasnit informace, které tester v testovacím procesu potřebuje, a vytvářet části testwaru. Sylabus jmenuje sedm schopností. Projdeme je jednu po druhé, u každé s příkladem.

### Analýza a zlepšování požadavků

LLM pomáhá analyzovat požadavky a další části testovací báze. Hledá nejednoznačnosti, nekonzistence a chybějící informace. Umí také navrhnout otázky, které tester položí stakeholderům, aby se požadavek vyjasnil. Je to forma statického testování s pomocníkem, který nikdy není unavený, ale také nezná souvislosti projektu, pokud mu je nedáte.

```text
Jsi test analytik. Přečti následující požadavek a vypiš:
1) nejednoznačné formulace,
2) chybějící informace potřebné pro návrh testů,
3) otázky pro product ownera.
Požadavek: "Klient může v internetovém bankovnictví zadat jednorázový
příkaz až do výše svého denního limitu. Při překročení limitu systém
zobrazí upozornění."
```

Model nejspíš upozorní, že není jasné, jestli limit platí pro jeden příkaz nebo pro součet za den, co přesně je „upozornění“ a jestli příkaz projde, a jak se limit chová u příkazů se splatností v budoucnu.

### Podpora tvorby testovacích případů

LLM pomáhá generovat testovací případy a navrhovat cíle testování podle systémových požadavků, uživatelských scénářů nebo jiných částí testovací báze. Tester přitom zůstává tím, kdo rozhoduje. Model navrhne, člověk vybere, opraví a doplní.

### Generování testovacího orákula

**Test oracle** (testovací orákulum) je zdroj, ze kterého tester určí očekávaný výsledek. LLM může očekávané výsledky navrhnout, například spočítat, jaká má být výsledná částka pojistného pro danou kombinaci vstupů podle popsaných pravidel. Právě tady platí věta z oddílu 1.1.2 nejvíc. Navržený očekávaný výsledek je plauzibilní, ne nutně správný. Pokud je chybný, test bude potvrzovat chybu. Orákulum od modelu je proto nutné ověřit proti specifikaci.

### Generování testovacích dat

LLM generuje datové sady, navrhuje hraniční hodnoty a vytváří různé kombinace testovacích dat. Hodí se to hlavně na syntetická data, která vypadají realisticky, ale nepatří žádné skutečné osobě.

```text
Vygeneruj 10 testovacích záznamů účtenek ve formátu JSON s poli:
obchod (text), datum (YYYY-MM-DD), castka (číslo se 2 desetinnými místy), mena.
Zahrň hraniční hodnoty: částka 0,00 a 0,01, datum 29. 2. v přestupném roce,
název obchodu s diakritikou a s 255 znaky. Data musí být smyšlená.
```

### Podpora automatizace testů

LLM pomáhá generovat testovací skripty z popisu testovacího případu. Umí také navrhnout úpravy stávajících skriptů, třeba odstranit duplicity nebo nahradit křehké lokátory stabilnějšími, a doporučit vhodné testovací techniky. Výsledný skript je potřeba spustit a zkontrolovat, protože model kód sám nespouští.

### Analýza výsledků testů

LLM pomáhá analyzovat výsledky testů. Vytváří jejich shrnutí a třídí anomálie podle závažnosti a priority. Když noční běh skončí s 60 selháními, model je může seskupit podle společné příčiny, třeba „45 selhání má stejnou chybu připojení k databázi“.

### Tvorba testwaru

LLM pomáhá vytvářet dokumenty, jako jsou plány testů, reporty o testování a reporty o defektech. Umí je také udržovat aktuální, jak se projekt vyvíjí. Například upraví plán testů podle nového rozsahu vydání.

Těchto sedm schopností pokrývá celý testovací proces, od analýzy přes návrh a implementaci až po vyhodnocení a reporting. Následující tabulka je přiřazuje k činnostem testovacího procesu podle CTFL.

| Schopnost LLM | Činnost testovacího procesu |
|---|---|
| Analýza a zlepšování požadavků | testovací analýza |
| Podpora tvorby testovacích případů | testovací analýza, návrh testů |
| Generování testovacího orákula | návrh testů |
| Generování testovacích dat | návrh testů, implementace testů |
| Podpora automatizace testů | implementace testů |
| Analýza výsledků testů | provedení testů, dokončení testování |
| Tvorba testwaru | plánování, monitoring a řízení, dokončení testování |

:::praxe
Při testování Šmouly lze použít několik schopností najednou. Model z popisu příkazů bota navrhne testovací případy pro neplatné vstupy, vygeneruje sadu zpráv s emoji, dlouhými texty a vloženým kódem jako testovací data a nakonec shrne log z běhu testů. Žádný z výstupů ale nejde rovnou do repozitáře. Tester je čte a opravuje.
:::

:::zkouska
Otázky k 1.2.1 často nabízejí pět možností a chtějí vybrat dvě schopnosti, které podle sylabu LLM mají. Správné možnosti odpovídají seznamu výše (nejednoznačnosti v požadavcích, testovací data s hraničními hodnotami, očekávané výsledky, shrnutí výsledků a podobně). Špatné možnosti obvykle slibují víc, než sylabus říká: samostatné spouštění všech testů bez člověka, vývoj kompletní aplikace k nasazení, nebo provádění průzkumného testování místo testera. LLM ve všech schopnostech *pomáhá* a člověk výstup kontroluje.
:::

### 1.2.2 AI chatboti a testovací aplikace postavené na LLM

Oba způsoby práce s LLM testerovi pomáhají. Liší se ale funkcemi, pružností a tím, jak se zapojují do práce.

### AI chatbot

**AI chatbot** nabízí uživatelsky přívětivé konverzační rozhraní, přes které tester komunikuje přímo s LLM. Tester píše otázky, příkazy nebo prompty v přirozeném jazyce a dostává okamžité odpovědi, které berou ohled na kontext konverzace. Pomocí řetězení promptů (**prompt chaining**) může výstup postupně zpřesňovat. Nejdřív si nechá vypsat testovací podmínky, pak z vybraných podmínek testovací případy a nakonec k nim testovací data.

Sylabus uvádí, kde jsou chatboti zvlášť užiteční. Hodí se na rutinní úlohy, na průzkumné testování a na zaškolení nových testerů, protože dávají rychlý přístup ke znalostem a postupům. Pomáhají tam, kde je potřeba rychlá zpětná vazba, vysvětlení testovacího pojmu nebo průběžné zkoumání požadavků a možných testovacích případů. Ovládání je intuitivní, takže je zvládnou i netechničtí stakeholdeři. Tím se rozšiřuje okruh uživatelů a usnadňuje se zavedení.

:::pojem term="AI chatbot"
Konverzační aplikace, která pomocí LLM zpracovává dotazy uživatele a odpovídá textem podobným lidskému. Umožňuje interaktivní komunikaci v přirozeném jazyce.
:::

### Testovací aplikace postavená na LLM

**LLM-powered testing application** (testovací nástroj postavený na LLM) integruje schopnosti LLM přes **API** (aplikační programové rozhraní). Plní přesně vymezené a často automatizované testovací úlohy. Uživatel s modelem obvykle nepíše volně. Aplikace připraví prompt sama, doplní do něj data z testovacího nástroje, odešle ho modelu a výsledek zpracuje.

Takové aplikace nabízejí víc přizpůsobení a lepší škálovatelnost. Organizace i dodavatelé nástrojů díky nim mohou vložit generativní AI do stávajících testovacích frameworků. Automatizují se tak opakující se nebo složité úlohy, jako je generování testovacích případů, analýza defektů nebo tvorba testovacích dat. Ve vyspělejších řešeních organizace vytvářejí AI agenty, kteří zastávají určité testovací role. Agentům se věnuje kapitola 4.

Příkladem je plugin do nástroje pro správu testů, který z nového uživatelského scénáře automaticky navrhne testovací případy. Jiným příkladem je krok v CI/CD pipeline, který po každém nočním běhu pošle selhání do modelu a do týmového kanálu zapíše jejich roztřídění.

### Srovnání

| Hledisko | AI chatbot | Testovací aplikace na LLM |
|---|---|---|
| Rozhraní | konverzace v přirozeném jazyce | integrace přes API do nástroje nebo frameworku |
| Typ úloh | ad hoc dotazy, rutinní úlohy, průzkum požadavků | přesně vymezené, často automatizované úlohy |
| Zpětná vazba | okamžitá, interaktivní | podle procesu, často bez obsluhy |
| Přizpůsobení a škálování | omezené, závisí na uživateli | vysoké, nastavuje organizace nebo dodavatel |
| Uživatelé | kdokoli, i netechnický stakeholder | testeři a týmy v rámci nástroje |
| Typické využití | vysvětlení pojmu, zaškolení, rychlý návrh | generování testů, analýza defektů, syntéza dat, agenti |

Tabulka ukazuje, že nejde o soupeře. Chatbot je nástroj pro člověka, který přemýšlí a ptá se. Aplikace na LLM je nástroj pro proces, který se opakuje.

Sylabus končí oddíl větou, která platí pro oba způsoby. Úspěšné nasazení generativní AI v testování vyžaduje dobrý prompt engineering. Pečlivě navržené prompty s jasnými a konkrétními instrukcemi zvyšují šanci, že výstup bude přesný, relevantní a v souladu s cíli testování. U chatbota prompt píše tester při každém dotazu. U aplikace ho napsal někdo jednou a aplikace ho používá opakovaně, takže špatný prompt se tam projeví v každém běhu. Prompt engineeringu se věnuje kapitola 2.

:::praxe
Šmoula je ve skutečnosti aplikace postavená na LLM, i když s ním Jan mluví přes Telegram jako s chatbotem. Zpráva z Telegramu nejde do modelu tak, jak je. Server na Oracle Cloud ji doplní o instrukce a kontext, spustí Claude Code v režimu bez obsluhy a odpověď vrátí. Rozhraní je konverzační, ale za ním stojí předem připravená integrace přes API. Na takovém příkladu je dobře vidět, že rozhoduje způsob integrace a míra přizpůsobení, ne vzhled rozhraní.
:::

:::zkouska
Správná odpověď na srovnání obvykle zní: chatbot nabízí konverzační rozhraní pro ad hoc úlohy, aplikace na LLM nabízí přizpůsobené řešení pro konkrétní testovací úlohy integrované přes API. Distraktory role prohazují (chatbot vyžaduje integraci, aplikace stojí na konverzaci) nebo tvrdí, že oba způsoby jsou totožné. Pozor také na tvrzení, že u integrované aplikace na kvalitě promptu nezáleží. Některé kurzy to naznačují, ale podle sylabu potřebují dobrý prompt engineering oba způsoby.
:::

:::nad-ramec
Mezi chatbotem a aplikací existují mezistupně. Asistent v IDE, jako je GitHub Copilot, má chatovací okno, ale zároveň vidí otevřený kód a umí měnit soubory. Nástroje jako Claude Code jdou dál a samy spouštějí příkazy. Pro zkoušku stačí dvě kategorie ze sylabu. V praxi je dobré se u každého nástroje zeptat, jaká data do modelu odcházejí, kdo prompt připravuje a kdo kontroluje výstup.
:::
