---
kapitola: 1
varianta: zkracena
nadpis: Úvod do generativní AI pro testování softwaru
podtitul: To nejnutnější ke zkoušce: typy AI, jak LLM zpracovává text, kategorie LLM, multimodalita, schopnosti LLM a dva způsoby práce s nimi.
---

Kapitola má v sylabu 100 minut. Ve zkoušce na ni připadá 7 otázek za 7 bodů: jedna K1 k oddílu 1.1.1, dvě K2 k oddílu 1.1.2 a po jedné K2 k oddílům 1.1.3, 1.1.4, 1.2.1 a 1.2.2. Praktická cvičení HO-1.1.2 a HO-1.1.4 se nezkoušejí.

## 1.1 Základy generativní AI a klíčové pojmy
:::lo
GenAI-1.1.1 (K1) Recall different types of AI: symbolic AI, classical machine learning, deep learning, and generative AI
GenAI-1.1.2 (K2) Explain the basics of generative AI and large language models
GenAI-1.1.3 (K2) Distinguish between foundation, instruction-tuned and reasoning LLMs
GenAI-1.1.4 (K2) Write and execute a given prompt addressing a test task using a multimodal LLM model
:::

**Generative AI** (generativní AI) používá velké předtrénované modely a vytváří nový obsah podobný lidskému: text, obrázky, kód. **Large language model** (LLM) je model GenAI předtrénovaný na velkém množství textu. Z promptu pozná kontext a vytvoří relevantní odpověď. V testování pomáhá v celém procesu: revize akceptačních kritérií, testovací případy a skripty, hledání defektů, analýza vzorců defektů, syntetická testovací data, dokumentace.

### 1.1.1 Spektrum AI

Sylabus rozlišuje čtyři přístupy. Každý má jeden rozlišující znak.

| Typ | Rozlišující znak |
|---|---|
| **Symbolic AI** (symbolická AI) | pravidla a symboly napsané člověkem, napodobuje lidské rozhodování |
| **Classical machine learning** (klasické ML) | řízené daty: příprava dat, ruční výběr příznaků (**feature selection**), trénování modelu; např. kategorizace defektů, předpověď problémů |
| **Deep learning** (hluboké učení) | neuronové sítě s více vrstvami, příznaky se učí samy z velkých a složitých dat (obraz, zvuk, text); člověk pořád anotuje, ladí, ověřuje |
| **Generative AI** | používá hluboké učení a vytváří nový obsah podle vzorců z trénovacích dat |

**Feature** (příznak) je jedna měřitelná vlastnost vstupních dat, ze které se model učí a podle které předpovídá. Hlavní výhoda GenAI pro testování: předtrénovaný model lze použít přímo, bez další fáze trénování. Přináší to ale rizika (kapitola 3).

:::zkouska
K1 otázka: přiřaď popis k typu AI. Klasické ML proti hlubokému učení rozlišuje to, kdo určuje příznaky. U klasického ML člověk, u hlubokého učení síť sama.
:::

### 1.1.2 Základy GenAI a LLM

LLM stojí na modelu **generative pre-trained transformer** (GPT), trénovaném na knihách, článcích a webu. **Small language models** (SLM) mají méně parametrů a jsou to lehká, zaměřená řešení.

Text se pro model převádí na čísla ve dvou krocích. **Tokenization** (tokenizace) rozdělí text na tokeny. Token je znak, část slova nebo slovo. **Embedding** převede každý token na vektor ve vícerozměrném prostoru, který nese význam, syntaxi a kontext. Tokeny s podobným významem mají blízké vektory.

V tokenech se měří velikost kontextového okna, cena za použití modelu přes API (vstup i výstup zvlášť) i doba zpracování. Počet tokenů není počet slov. Anglický text má v průměru zhruba jeden token na čtyři znaky, čeština a strukturovaná data (JSON, logy, kód) obvykle víc tokenů na stejnou délku.

**Transformer** je architektura neuronové sítě, která pomocí self-attention zachycuje vztahy mezi tokeny i v dlouhém textu. Při inferenci LLM předpovídá další token. Výsledek je statisticky pravděpodobný, ale ne nutně správný.

LLM jsou **non-deterministic** (nedeterministické): stejný vstup může dát různé výstupy. Příčinou je pravděpodobnostní inference a nastavení hyperparametrů.

**Context window** (kontextové okno) je množství předchozího textu v tokenech, které model při generování bere v úvahu. Větší okno udrží souvislosti v dlouhém textu (např. velké testovací logy), ale zvyšuje výpočetní náročnost a dobu zpracování. Co se do okna nevejde, model nevidí. Do okna se počítá systémový prompt, celá konverzace, vložené dokumenty i generovaná odpověď. Proto chatbot v dlouhé konverzaci „zapomene“ pokyn ze začátku a proto se dlouhé logy mají před analýzou zkrátit nebo rozdělit.

Pro testera z toho plynou dva praktické důsledky. Výstup LLM je potřeba ověřit, protože pravděpodobný text může být chybný. A u aplikace, která LLM obsahuje, nelze očekávaný výsledek porovnávat znak po znaku. Ověřují se vlastnosti odpovědi, například obsah, formát a délka.

:::zkouska
Tokenizace text dělí na stavební kameny. Embedding je vektor s významem. Předpověď dalšího tokenu dělá transformer. Kontextové okno omezuje rozsah textu, který model najednou bere v úvahu. Neřídí pořadí ani rychlost zpracování. Scénář „model ignoruje začátek dlouhého dokumentu“ vysvětluje kontextové okno, ne nedeterminismus.
:::

### 1.1.3 Základní, instrukční a uvažující LLM

| Kategorie | Vznik | Hodí se na |
|---|---|---|
| **Foundation LLM** (base LLM) | předtrénování na obrovských pestrých datech | univerzální použití; pro konkrétní úlohu potřebuje přizpůsobení |
| **Instruction-tuned LLM** | doladění základního modelu na dvojicích prompt a očekávaná odpověď | plnění instrukcí, dodržení formátu a šablony (Gherkin, JSON) |
| **Reasoning LLM** | další trénink na úlohách s mezikroky (chain-of-thought) | logické vyvozování, vícekroková analýza, syntéza složitých informací |

V testování se používají instruction-tuned (někdy „non-reasoning“) i reasoning modely. Volba závisí na složitosti úlohy a potřebě uvažování.

:::zkouska
Přesné dodržení šablony nebo syntaxe vede na instruction-tuned LLM. Syntéza dat z více zdrojů, trendy a priority vedou na reasoning LLM. Uvažující model není automaticky nejlepší volba. Ladění na instrukce je krok vývoje modelu, ne ladění na pravidla konkrétního projektu.
:::

### 1.1.4 Multimodální LLM a modely pro obraz a jazyk

**Multimodal model** zpracovává více modalit: text, obraz, zvuk, video. Rozšiřuje transformer a učí se vztahy mezi druhy dat. Tokenizace se přizpůsobí modalitě. Obrázek se pomocí modelu pro obraz a jazyk převede na embeddingy a ty zpracuje transformer.

**Vision-language model** (VLM) je podmnožina multimodálních LLM pro obraz a text. Úlohy: popis obrázku, odpovídání na otázky k obrázku, kontrola souladu textu a obrazu. V testování porovná snímek obrazovky nebo wireframe s uživatelským scénářem, reportem o defektu nebo očekávaným výsledkem a pomůže navrhnout testovací případy z textu i obrazu, čímž zvyšuje pokrytí.

Úskalí: model může přehlédnout drobný nebo nečitelný text, domyslet si prvek, který na snímku není, a ze statického obrázku nepozná chování aplikace. Snímky obrazovky mohou obsahovat citlivá data, která do veřejného modelu nepatří.

:::zkouska
VLM je podmnožina multimodálních LLM, ne naopak, a pojmy nejsou zaměnitelné.
:::

## 1.2 Využití generativní AI v testování: základní principy
:::lo
GenAI-1.2.1 (K2) Give examples of key LLM capabilities for test tasks
GenAI-1.2.2 (K2) Compare interaction models when using GenAI for software testing
:::

LLM dobře zpracovávají přirozený jazyk a kód, generují text a kód, odpovídají na otázky, shrnují, překládají a v multimodálním režimu analyzují obrázky. Tester je může využít dvěma doplňujícími se způsoby: přes AI chatboty a přes aplikace na LLM integrované do testovacích nástrojů.

### 1.2.1 Hlavní schopnosti LLM pro testovací úlohy

Sylabus uvádí sedm schopností:

1. **Analýza a zlepšování požadavků:** nejednoznačnosti, nekonzistence, chybějící informace, otázky pro stakeholdery.
2. **Podpora tvorby testovacích případů:** testovací případy a cíle testování z testovací báze.
3. **Generování testovacího orákula:** očekávané výsledky.
4. **Generování testovacích dat:** datové sady, hraniční hodnoty, kombinace.
5. **Podpora automatizace testů:** skripty z popisu testovacího případu, návrhy úprav skriptů, vhodné testovací techniky.
6. **Analýza výsledků testů:** shrnutí, třídění anomálií podle závažnosti a priority.
7. **Tvorba testwaru:** plány testů, reporty o testování a o defektech a jejich aktualizace.

:::zkouska
Distraktory slibují víc než sylabus: spouštění všech testů bez člověka, vývoj celé aplikace k nasazení, samostatné průzkumné testování. LLM ve všech úlohách pomáhá, výstup kontroluje člověk.
:::

### 1.2.2 AI chatboti a testovací aplikace postavené na LLM

**AI chatbot** je konverzační rozhraní k LLM. Tester píše v přirozeném jazyce a dostává okamžité odpovědi. Řetězením promptů výstup zpřesňuje. Hodí se na rutinní úlohy, průzkumné testování, zaškolení, rychlou zpětnou vazbu a vysvětlení pojmů. Zvládnou ho i netechničtí stakeholdeři.

**LLM-powered testing application** integruje LLM přes API a plní přesně vymezené, často automatizované úlohy: generování testovacích případů, analýzu defektů, tvorbu testovacích dat. Nabízí víc přizpůsobení a škálovatelnost. Organizace a dodavatelé ji vkládají do testovacích frameworků. Ve vyspělé podobě jde o AI agenty (kapitola 4).

| Hledisko | AI chatbot | Aplikace na LLM |
|---|---|---|
| Rozhraní | konverzace | integrace přes API |
| Úlohy | ad hoc, rutinní, průzkum | přesně vymezené, automatizované |
| Přizpůsobení | omezené | vysoké, škálovatelné |
| Uživatelé | kdokoli, i netechnický | testeři v rámci nástroje |

Oba způsoby potřebují dobrý prompt engineering (kapitola 2). Jasné a konkrétní instrukce zvyšují šanci, že výstup bude přesný, relevantní a v souladu s cíli testování.

:::zkouska
Chatbot = konverzace, ad hoc úlohy. Aplikace na LLM = integrace přes API, přizpůsobené řešení konkrétních úloh. Distraktory role prohazují nebo tvrdí, že u integrované aplikace na promptu nezáleží.
:::
