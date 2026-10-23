---
kapitola: 4
varianta: zkracena
nadpis: Testovací infrastruktura postavená na LLM
podtitul: Co ke zkoušce stačí vědět o architektuře nástrojů s LLM, RAG, agentech, fine-tuningu a LLMOps.
---

Kapitola má 110 minut výuky, pět studijních cílů na úrovni K2 a na zkoušce z ní přijde pět otázek, z každého cíle jedna. Klíčová slova: **test infrastructure** (infrastruktura testování), **fine-tuning**, **LLM-powered agent**, **Large Language Model Operations** (LLMOps), **retrieval-augmented generation** (RAG) a **vector database** (vektorová databáze).

## 4.1 Architektonické přístupy k testovací infrastruktuře s LLM

:::lo
GenAI-4.1.1 (K2) Explain key architectural components and concepts of LLM-powered test infrastructure
GenAI-4.1.2 (K2) Summarize Retrieval-Augmented Generation
GenAI-4.1.3 (K2) Explain the role and application of LLM-powered agents in automating test processes
:::

Generativní AI se do testování dostává přes AI chatboty a přes testovací nástroje postavené na LLM. RAG a agenti jsou dvě rozšíření základní architektury.

### 4.1.1 Architektonické komponenty a koncepty

Infrastruktura testování s LLM zapojuje LLM do testovacího procesu kvůli automatizaci, uvažování a rozhodování. Na rozdíl od chatbotu zpracovává testovací dotazy, analyzuje požadavky, generuje testovací případy a vyhodnocuje výstupy.

Má tři části. **Front-end** je rozhraní, kam tester zadává dotazy. **Back-end** ověřuje uživatele (authentication), vyhledává data, připravuje prompt, řídí komunikaci s LLM a upravuje výstup modelu (post-processing). **LLM** generuje odpovědi ze strukturovaných promptů a běží buď jako služba třetí strany přes API, nebo jako vlastní model.

Oproti klientovi a serveru platí čtyři rozdíly. LLM je chytrá komponenta, která uvažuje nad testwarem. Odpovědi vznikají dynamicky z kontextu, ne podle pravidel. Back-end čerpá z relační databáze (strukturovaná data, například testovací případy) a z vektorové databáze (sémantické vyhledávání pomocí embeddingů). Back-end surový výstup upraví tak, aby odpovídal testovacím podmínkám.

Tok dat v kostce: tester zadá dotaz ve front-endu, back-end ověří, kdo se ptá, vyhledá podklady v relační a vektorové databázi a složí z nich prompt. Model vrátí odpověď a back-end ji převede do šablony, zkontroluje a teprve pak ji front-end zobrazí. Model sám do žádného systému nesahá. Všechno, co o projektu ví, mu dodá back-end. Proto se na back-endu řeší bezpečnost, oprávnění a kvalita vstupu.

:::zkouska
Prompt z dotazu a dat z databází skládá back-end. Front-end jen přijímá vstup a zobrazuje výsledek. LLM data samo nevyhledává. Post-processing je také práce back-endu.
:::

### 4.1.2 Retrieval-Augmented Generation (RAG)

:::pojem term="retrieval-augmented generation (RAG)"
Technika, která spojuje LLM s vyhledávačem. Vyhledávač najde relevantní data a model z nich vytvoří přesnější odpověď odpovídající kontextu.
:::

RAG zvyšuje relevanci a přesnost odpovědí tím, že do generování zapojí další zdroje dat. Model se nic nového nenaučí, jen dostane podklady v promptu.

Předzpracování proběhne předem. Dokumenty se rozdělí na části (chunks), například po 256 až 512 tokenech, kvůli cílenému vyhledání a kontextovému oknu. Části se vyčistí, převedou na embeddingy předtrénovaným modelem a uloží do vektorové databáze.

Zpracování dotazu má dva kroky. Při vyhledání (retrieval) se dotaz převede na embedding a najdou se části s největší sémantickou podobností. Při generování (generation) dostane LLM nalezené části jako kontext a spojí je se svými znalostmi. Výsledkem je podložená odpověď (grounded response).

Proti halucinacím RAG pomáhá tím, že model nemusí hádat. Potřebnou informaci má přímo v kontextovém okně a lze ho promptem omezit na odpovědi jen z dodaných podkladů s uvedením zdroje. Halucinace to snižuje, ale neodstraňuje. RAG selže, když vyhledávání najde špatnou nebo zastaralou pasáž, když je index neaktuální, nebo když otázka potřebuje přehled přes celý dokument. Praktický cíl HO-4.1.2 chce právě tyto silné a slabé stránky poznat porovnáním odpovědí s RAG a bez něj.

V testování RAG zpřístupní firemní databáze, dokumentaci a repozitáře v reálném čase. Testovací analýza a návrh testů pak odpovídají nejnovějším specifikacím a existujícím testovacím datům.

:::pojem term="vector database"
Databáze optimalizovaná pro ukládání a dotazování vektorových reprezentací dat o mnoha rozměrech.
:::

:::zkouska
Pořadí: rozdělit, vyčistit, převést na embeddingy, uložit. Při dotazu: zakódovat dotaz, vyhledat, předat modelu, generovat. RAG nemění váhy modelu, dodává data za běhu. Vyhledávání je podle významu, ne podle klíčových slov. Podle oficiální vzorové zkoušky je ruční procházení vyhledaných podkladů před dotazem zbytečný krok proti smyslu RAG, i když jeden z kurzů tvrdí opak. Jednotný formát výstupu není znak RAG.
:::

### 4.1.3 Agenti postavení na LLM v automatizaci testovacích procesů

:::pojem term="LLM-powered agent"
Aplikace, která spojuje uvažování, rozhodování a paměť LLM a pomocí nástrojů provádí úlohy, poloautonomně nebo autonomně.
:::

Agent na rozdíl od chatbotu jedná. Volá předem definované funkce, takzvané nástroje (tools), a pracuje s externími systémy.

Autonomní agent pracuje s minimálním zásahem člověka a opírá se o předem daná pravidla, učení posilováním a adaptivní zpětnou vazbu. Poloautonomní agent pracuje s pravidelným lidským dohledem, aby výstup odpovídal cílům uživatele.

Multiagentní architektura spojuje více agentů se specializovanými rolemi. Jejich koordinaci se říká orchestrace (orchestration).

Příklad orchestrace: jeden agent analyzuje požadavky, druhý navrhuje testovací případy, třetí píše automatizované testy, čtvrtý je spouští a pátý píše report. Orchestrátor předává výstupy mezi nimi.

V testovacích nástrojích jsou agenti schovaní v AI asistentech. Ti poloautonomně převádějí uživatelské scénáře a požadavky na testware v celém procesu: analýza, návrh, implementace, provedení, reportování. Automatizace se tím posouvá od skriptů k automatizaci řízené cílem a postavené na agentech.

Agenti mají stejná rizika jako LLM: halucinace, chyby v uvažování a zkreslení. Sylabus doporučuje automatickou verifikaci výsledků agenta a poloautonomní agenty pro kritické úlohy.

U agenta je chyba dražší než u chatbotu, protože ji agent rovnou provede. Může založit falešné defekty nebo upravit test tak, aby prošel. Autonomie se proto nastavuje podle rizika úlohy: u interní aplikace může agent zakládat defekty sám, u platebního systému je jen navrhuje a tester je schvaluje.

:::zkouska
Agent jedná přes nástroje, chatbot jen odpovídá. Autonomie se liší mírou zapojení člověka a díky ní lze zlepšit efektivitu i kvalitu zároveň. Agenti nikdy neruší potřebu verifikace. Orchestrace znamená koordinaci více agentů.
:::

## 4.2 Fine-tuning a LLMOps: provozování generativní AI v testování

:::lo
GenAI-4.2.1 (K2) Explain the fine-tuning of language models for specific test tasks
GenAI-4.2.2 (K2) Explain LLMOps and its role in deploying and managing LLMs for test tasks
:::

Dvě praktiky pro provoz: fine-tuning přizpůsobí model a LLMOps řídí provozní řetězec.

### 4.2.1 Fine-tuning LLM pro testovací úlohy

:::pojem term="fine-tuning"
Učení s učitelem na označených příkladech, které upraví váhy modelu a přizpůsobí ho úloze nebo doméně.
:::

Fine-tuning dál trénuje předtrénovaný LLM nebo SLM na cílené datové sadě. Model získá specializované uvažování v doméně a její slovník. Doladěný SLM může u úzké úlohy dosáhnout vysokého výkonu s menšími výpočetními nároky. Příklad ze sylabu: model doladěný na uživatelských scénářích a testovacích případech organizace generuje testy v jejím formátu a terminologii.

Prompt engineering a RAG mění jen vstup, fine-tuning mění model. RAG se hodí na aktuální fakta, fine-tuning na stálý formát, styl a úzkou opakovanou úlohu. Fine-tuning se nehodí na fakta, která se často mění, protože každá změna by znamenala nový trénink a model by neuměl říct, odkud informaci má. Techniky se dají kombinovat: doladěný model může dostávat podklady přes RAG.

Ukázka postupu (HO-4.2.1): výběr LLM nebo SLM, datová sada pro úlohu, doladění v knihovně pro strojové učení, prompt doladěnému modelu a rozbor kvality výstupu. Důraz je na kvalitě dat.

Čtyři výzvy: zkreslené nebo nepřesné výsledky (řeší kvalitní data), **overfitting** (přeučení: model je příliš přizpůsobený trénovacím datům a hůř zvládá nová data), **opacity** (neprůhlednost rozhodování, ztěžuje ladění a validaci) a velké výpočetní nároky u LLM.

:::zkouska
Fine-tuning mění váhy, prompt a RAG ne. Nenahrazuje obecné znalosti modelu a nezaručuje, že nedojde k přeučení. Doladit jde LLM i SLM.
:::

### 4.2.2 LLMOps při nasazení a správě LLM pro testování

:::pojem term="Large Language Model Operations (LLMOps)"
Praktiky, nástroje a procesy pro vývoj, nasazení, monitoring a údržbu LLM v produkčním prostředí.
:::

Rozhodnutí LLMOps závisí na způsobu použití. AI chatbot: ochrana dat, bezpečnost a náklady, volba mezi LLM jako službou s dostatečnými zárukami a vlastním open-source modelem, posouzení záruk dodavatele nebo vlastních schopností. Testovací nástroj s GenAI: totéž a navíc posouzení záruk poskytovatele k bezpečnosti dat a výkonu, analýza nákladů a přínosů a posouzení rizik. Vlastní vývoj: plná kontrola nad ochranou dat a bezpečností, plánování výpočetního výkonu, úložiště a školení, procesy validace a údržby a potřebná odbornost.

Přístupy se nevylučují a dají se rozšířit o RAG a fine-tuning.

Příklad: banka používá schválený chatbot na obecné otázky, AI funkce v nástroji pro správu testů po prověření dodavatele a pro citlivá data vlastní nástroj s open-source modelem ve vlastním datovém centru. Všechny tři přístupy běží současně.

Slovník sylabu řadí do LLMOps nasazení, monitoring a údržbu. V praxi to znamená verzovat prompty a modely, před změnou spustit evaluační sadu dotazů, sledovat odezvu, chybovost, cenu a kvalitu a průběžně aktualizovat index RAG. Nástroj s LLM je software, který se musí testovat stejně jako jiný.

:::zkouska
LLMOps řídí LLM po celý životní cyklus včetně ochrany dat, bezpečnosti a nákladů. Neomezuje používání GenAI, nezužuje ji na chatboty a neruší lidský dohled. Posouzení záruk poskytovatele nástroje patří k druhému přístupu, plánování výpočetního výkonu a školení k vlastnímu vývoji. Přístupy lze kombinovat.
:::
