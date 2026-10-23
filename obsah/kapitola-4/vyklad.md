---
kapitola: 4
varianta: vyklad
nadpis: Testovací infrastruktura postavená na LLM
podtitul: Z jakých částí se skládá nástroj s LLM, jak funguje RAG a agenti, kdy model doladit a jak ho provozovat.
---

Čtvrtá kapitola sylabu CT-GenAI se jmenuje **LLM-Powered Test Infrastructure for Software Testing** (testovací infrastruktura postavená na LLM). Sylabus jí dává 110 minut výuky. Předchozí kapitoly se dívaly na LLM zvenku: jak psát prompty a jaká rizika hlídat. Tahle kapitola se dívá dovnitř. Ukazuje, z jakých částí se skládá nástroj, který LLM používá, a jak se takový nástroj rozšiřuje a provozuje.

Kapitola má dva oddíly a pět studijních cílů. Všechny jsou na úrovni K2, takže máte umět vysvětlit, porovnat a zdůvodnit. Na zkoušce z kapitoly přijde pět otázek, z každého studijního cíle jedna, každá za jeden bod. Výpočty ani K3 úlohy tu nejsou.

Klíčová slova kapitoly jsou dvě skupiny. Z obecné testovací terminologie je to **test infrastructure** (infrastruktura testování). Z terminologie generativní AI je to **fine-tuning** (doladění modelu), **LLM-powered agent** (agent postavený na LLM), **Large Language Model Operations** (LLMOps), **retrieval-augmented generation** (RAG, generování rozšířené o vyhledávání) a **vector database** (vektorová databáze). Všechny tyto pojmy v textu vysvětlím a u každého je samostatný rámeček s definicí.

Sylabus ke kapitole uvádí i tři praktické cíle, takzvané **hands-on objectives**. HO-4.1.2 na úrovni H1 chce, abyste si RAG sami vyzkoušeli. HO-4.1.3 a HO-4.2.1 jsou na úrovni H0, tedy jen ukázka: jak agent automatizuje opakovanou testovací úlohu a jak probíhá doladění modelu. Zadání najdete v cvičeních ke kapitole.

:::nad-ramec
Úrovně praktických cílů jsou v sylabu tři. H0 znamená sledovat ukázku, H1 znamená vyzkoušet si úlohu s vedením a H2 znamená provést úlohu samostatně. Na zkoušce se praktické cíle nezkouší. Pomáhají ale pochopit látku, ze které jsou K2 otázky.
:::

## 4.1 Architektonické přístupy k testovací infrastruktuře s LLM

:::lo
GenAI-4.1.1 (K2) Explain key architectural components and concepts of LLM-powered test infrastructure
GenAI-4.1.2 (K2) Summarize Retrieval-Augmented Generation
GenAI-4.1.3 (K2) Explain the role and application of LLM-powered agents in automating test processes
:::

Sylabus začíná připomínkou z první kapitoly. Generativní AI se do testování dostává dvěma typy infrastruktury. Prvním typem je **AI chatbot**, tedy konverzační rozhraní, kde tester píše prompty a čte odpovědi. Druhým typem jsou **LLM-powered test tools** (testovací nástroje postavené na LLM). Ty volají LLM přes API a dělají předem dané, často automatizované úlohy. Rozdíl mezi nimi vysvětluje oddíl 1.2.2.

Oddíl 4.1 pak popisuje tři věci. Nejdřív základní architekturu testovacího nástroje s LLM. Potom dvě rozšíření, která z něj dělají užitečnější nástroj: RAG a agenty. Obě rozšíření stojí na základní architektuře, takže ji probereme první.

### 4.1.1 Architektonické komponenty a koncepty

:::pojem term="test infrastructure"
Infrastruktura testování. Podle slovníku ISTQB testovací prostředí, testovací nástroje, vybavení pracoviště a procedury, které jsou potřeba k provádění testování. V kapitole 4 jde o tu část, která do testování zapojuje LLM.
:::

Sylabus definuje **LLM-powered test infrastructure** (infrastrukturu testování postavenou na LLM) jako systém, který zapojuje LLM do testovacího procesu. Cílem je lepší automatizace, uvažování a rozhodování. Takový nástroj zpracovává dotazy k testování, analyzuje požadavky, generuje testovací případy a vyhodnocuje výstupy.

Sylabus ji staví do protikladu k tradičnímu AI chatbotu. Chatbot se soustředí na konverzaci: otázka, odpověď, další otázka. Testovací nástroj s LLM je postavený kolem testovacích úloh. Má přístup k datům projektu, ví, v jakém formátu chcete výsledek, a výsledek umí zařadit do dalších kroků.

#### Tři hlavní části

Typická architektura má tři části. Sylabus mluví o vícekomponentovém návrhu, který zajišťuje bezpečnou a efektivní komunikaci s LLM.

**Front-end** (uživatelské rozhraní) je místo, kde tester zadává dotazy nebo příkazy. Může to být webová stránka, plugin v nástroji pro správu testů, příkazová řádka nebo chatovací okno.

**Back-end** (serverová část) zpracovává vstup od uživatele. Sylabus u něj vyjmenovává čtyři funkce: **authentication** (autentizace, tedy ověření, kdo se ptá a co smí vidět), **data retrieval** (vyhledání dat), **prompt preparation** (příprava promptu) a řízení komunikace s LLM. K tomu přidává ještě páté: úpravu odpovědi modelu, než ji uvidí uživatel.

**LLM** je samotný model, který generuje odpovědi na základě strukturovaných promptů. Může běžet dvěma způsoby. Buď jako služba třetí strany, ke které se back-end připojuje přes API. Nebo jako vlastní model provozovaný uvnitř organizace (in-house).

#### V čem je to víc než klient a server

Na první pohled jde o obyčejnou aplikaci: rozhraní, server a nějaká služba za ním. Sylabus ale zdůrazňuje čtyři rozdíly. Ty se na zkoušce objevují nejčastěji.

Zaprvé, LLM není jen server, který vrací uložená data. Je to chytrá zpracovávající komponenta, která interpretuje testware a uvažuje nad ním. **Testware** jsou pracovní produkty testování, například testovací případy, testovací data nebo reporty.

Zadruhé, nástroj nefunguje podle pravidel. Starší chatboty založené na pravidlech (**rule-based chatbots**) odpovídají předem napsanými větami. Nástroj s LLM vytváří odpověď dynamicky z kontextu, třeba z požadavků, kódu nebo výsledků testů.

Zatřetí, back-end čerpá z více zdrojů dat. Sylabus uvádí dva typy. **Relational databases** (relační databáze) drží strukturovaná data, například existující testovací případy, defekty nebo výsledky běhů. **Vector databases** (vektorové databáze) slouží k sémantickému vyhledávání podle významu. Pracují s embeddingy a jsou základem RAG z oddílu 4.1.2.

Začtvrté, back-end odpověď modelu dál zpracovává. Tomu se říká **post-processing** (následné zpracování). Sylabus říká, že back-end vylepšuje surový výstup LLM tak, aby odpovídal testovacím podmínkám testovacího procesu. Teprve potom jde výsledek na front-end. V praxi to znamená převést volný text do šablony testovacího případu, zkontrolovat povinná pole, odstranit duplicity nebo ověřit, že odkazy na požadavky skutečně existují.

:::zkouska
Hlídejte si, která část dělá co. Front-end jen přijímá vstup a zobrazuje výsledek. Back-end ověřuje uživatele, vyhledává data v relační i vektorové databázi, skládá prompt, volá LLM a upravuje jeho odpověď. LLM generuje odpověď a sám data z databází nevyhledává. Otázka typu „která komponenta spojí vstup uživatele s daty z databází a připraví prompt“ má odpověď back-end. Stejně tak post-processing patří back-endu, ne modelu ani front-endu.
:::

#### Diagram a tok dat

Následující schéma ukazuje, jak spolu části mluví. Čísla odpovídají krokům popsaným pod ním.

```text
 Tester
   |
   | (1) dotaz: "Navrhni testy pro změnu limitu karty"
   v
+-------------------+
|    FRONT-END      |  webové rozhraní, plugin, CLI
+-------------------+
   |  (2) požadavek + identita uživatele
   v
+--------------------------------------------------------------+
|                         BACK-END                             |
|                                                              |
|  (3) autentizace a oprávnění                                 |
|  (4) vyhledání dat ----------+-----------------+             |
|                              |                 |             |
|                     +----------------+  +----------------+   |
|                     | relační DB     |  | vektorová DB   |   |
|                     | testy, defekty |  | chunky specif. |   |
|                     +----------------+  +----------------+   |
|  (5) příprava promptu (instrukce + dotaz + nalezená data)    |
|  (6) volání LLM -------------------------------+             |
|  (8) post-processing <-------------------------+             |
+--------------------------------------------------------------+
   |                                   |  ^
   | (9) upravený výsledek             |  | (7) odpověď modelu
   v                                   v  |
+-------------------+          +----------------------+
|    FRONT-END      |          |  LLM                 |
|  zobrazí testy    |          |  API třetí strany    |
+-------------------+          |  nebo in-house model |
                               +----------------------+
```

Tok dat jde v devíti krocích. (1) Tester napíše do front-endu, co potřebuje. (2) Front-end pošle dotaz back-endu spolu s informací, kdo se ptá. (3) Back-end ověří identitu a zjistí, k jakým projektům a dokumentům má uživatel přístup. (4) Back-end vyhledá podklady. Z relační databáze vytáhne třeba existující testovací případy k modulu karet a otevřené defekty. Z vektorové databáze vytáhne pasáže specifikace, které se k dotazu významově hodí. (5) Back-end složí prompt. Obvykle obsahuje systémový prompt s rolí a pravidly, nalezené podklady, požadovaný formát a nakonec dotaz uživatele. (6) Back-end pošle prompt modelu. (7) Model vrátí odpověď. (8) Back-end odpověď zpracuje: převede ji do šablony, zkontroluje, že každý test odkazuje na existující požadavek, a vyřadí duplicity se stávajícími testy. (9) Výsledek se zobrazí testerovi.

Všimněte si, že model v tomto schématu nikam sám nesahá. Všechno, co ví o projektu, mu do promptu vloží back-end. To je důvod, proč je back-end místem, kde se řeší bezpečnost, ochrana dat a kvalita vstupu. Když back-end pošle modelu špatné nebo zastaralé podklady, dostanete přesvědčivě napsané, ale chybné testy.

:::praxe
Šmoula jako testovací infrastruktura s LLM. Jan provozuje vlastního AI agenta Šmoulu. Jeho architekturu lze popsat přesně pojmy z oddílu 4.1.1.

Front-end je Telegram. Jan píše zprávy do chatu s botem a tam také čte odpovědi.

Back-end je služba na virtuálním stroji v Oracle Cloud. Přijímá zprávy z Telegramu a plní stejné funkce, jaké vyjmenovává sylabus. Autentizace znamená, že bot musí odpovídat jen Janovi. Typicky se to řeší kontrolou identifikátoru chatu nebo uživatele. Vyhledání dat znamená načíst z privátního GitHub repozitáře relevantní poznámky z paměti. Příprava promptu znamená složit zadání pro model z instrukcí, paměti a zprávy. Řízení komunikace s LLM znamená spustit Claude Code v takzvaném headless režimu, tedy bez interaktivního okna. Post-processing znamená výstup zkrátit nebo rozdělit tak, aby se vešel do zprávy v Telegramu, a případně zapsat novou poznámku do paměti.

LLM je model Claude, ke kterému se Claude Code připojuje jako ke službě třetí strany přes API.

Datové zdroje se od sylabu liší. Šmoula nemá relační ani vektorovou databázi. Paměť má jako soubory v markdownu v gitu. To je jednoduchý a dohledatelný zdroj, ale vyhledává se v něm podle názvů souborů a textu, ne podle významu. Kdyby paměť narostla na stovky poznámek, dává smysl přidat vektorové vyhledávání, tedy RAG.
:::

### 4.1.2 Retrieval-Augmented Generation (RAG)

:::pojem term="retrieval-augmented generation (RAG)"
Generování rozšířené o vyhledávání. Technika, která spojuje LLM s vyhledávačem (retrieverem). Vyhledávač najde k dotazu relevantní data a model z nich vytvoří přesnější odpověď, která odpovídá kontextu.
:::

LLM ví jen to, co se naučil při trénování. Jeho znalosti končí k určitému datu a nikdy neobsahovaly vaše interní dokumenty. Specifikaci platebního API, kterou analytik upravil minulý týden, model nezná. Když se na ni zeptáte, buď přizná, že neví, nebo si odpověď vymyslí. Druhá možnost je **hallucination** (halucinace), tedy nepravdivá informace vytvořená modelem, o které mluví kapitola 3.

RAG tento problém řeší tak, že modelu potřebné informace dodá v promptu. Sylabus říká, že RAG vylepšuje LLM tím, že do generování odpovědi zapojuje další zdroje dat. Tím roste relevance a přesnost výstupu. Model se tedy nic nového nenaučí. Jen dostane k dotazu správné podklady a odpovídá z nich.

Celý proces má dvě fáze. První fáze proběhne předem, jednou pro každý dokument. Sylabus jí říká **preprocessing** (předzpracování). Druhá fáze proběhne při každém dotazu. Sylabus jí říká **user prompt processing** (zpracování promptu uživatele) a odehrává se při **inference** (inferenci), tedy když model generuje odpověď.

#### Fáze 1: předzpracování dokumentů

Předzpracování připraví dokumenty tak, aby v nich šlo rychle hledat podle významu. Má čtyři kroky.

Prvním krokem je **chunking** (rozdělení na části). Velký dokument se rozdělí na menší kusy, kterým se říká **chunks**. Sylabus jako příklad uvádí velikost 256 až 512 tokenů. Důvody jsou dva a sylabus je jmenuje výslovně. Malé části umožňují cílené vyhledání, protože se najde konkrétní pasáž, a ne celý sto stránkový dokument. A malé části se vejdou do kontextového okna modelu, i když jich pošlete několik najednou.

Druhým krokem je vyčištění a zpracování každé části. Odstraní se zbytečné prvky, jako jsou záhlaví stránek, čísla stránek, opakované copyrighty nebo rozbité znaky z převodu PDF. Text se sjednotí.

Třetím krokem je převod na **embedding** (vektorovou reprezentaci). Každá část se pomocí předtrénovaného modelu převede na vektor o mnoha rozměrech. Embeddingy znáte z oddílu 1.1. Texty s podobným významem mají vektory blízko u sebe. Model pro embeddingy bývá jiný a menší než LLM, které pak generuje odpověď.

Čtvrtým krokem je uložení. Vektory se uloží do vektorové databáze, obvykle spolu s původním textem části a s metadaty, například názvem dokumentu, verzí a číslem kapitoly.

:::pojem term="vector database"
Vektorová databáze. Databáze optimalizovaná pro ukládání a dotazování vektorových reprezentací dat o mnoha rozměrech. V RAG v ní leží embeddingy částí dokumentů a umí rychle najít ty, které jsou nejpodobnější vektoru dotazu.
:::

#### Fáze 2: zpracování dotazu

Sylabus popisuje zpracování dotazu jako dva kroky: vyhledání a generování.

**Retrieval** (vyhledání) začíná tím, že systém dotaz uživatele zakóduje na embedding. Musí k tomu použít stejný model jako při předzpracování, jinak by vektory nebyly srovnatelné. Pak ve vektorové databázi najde části, jejichž embeddingy jsou vektoru dotazu nejpodobnější. Sylabus tomu říká **semantic similarity** (sémantická podobnost). Výsledkem je několik nejrelevantnějších pasáží.

**Generation** (generování) znamená, že nalezené pasáže se vloží do promptu jako kontext a pošlou se modelu. Model vytvoří odpověď, která kombinuje jeho vlastní znalosti s nově dodanými daty. Této vložené části promptu se v praxi říká rozšíření (augmentation), odtud prostřední slovo názvu RAG.

Celé dohromady to vypadá takto.

```text
FÁZE 1: PŘEDZPRACOVÁNÍ (jednou, předem)

  dokumenty         chunking           čištění          embedding         uložení
 +----------+     +----------+      +----------+     +-----------+     +------------+
 | sylabus  | --> | části po | -->  | bez      | --> | vektor    | --> | vektorová  |
 | specif.  |     | 256-512  |      | záhlaví, |     | pro každou|     | databáze   |
 | testy    |     | tokenech |      | sjednoc. |     | část      |     | + text +   |
 +----------+     +----------+      +----------+     +-----------+     | metadata   |
                                                                       +------------+
                                                                             ^
FÁZE 2: ZPRACOVÁNÍ DOTAZU (při každém dotazu)                                |
                                                                             |
  dotaz             embedding dotazu     vyhledání (retrieval)               |
 +----------+     +-------------+      +--------------------------+          |
 | "Jaké    | --> | vektor      | -->  | najdi k nejpodobnějších  | ---------+
 | rizika   |     | dotazu      |      | částí                    |
 | má RAG?" |     +-------------+      +--------------------------+
 +----------+                                     |
                                                  v
                        +----------------------------------------------+
                        | prompt = instrukce + nalezené části + dotaz  |
                        +----------------------------------------------+
                                                  |
                                                  v
                                 +--------------------------------+
                                 | LLM: generování (generation)   |
                                 | odpověď podložená podklady     |
                                 +--------------------------------+
```

#### Proč podle významu a ne podle slov

Klasické fulltextové vyhledávání hledá shodná slova. Sémantické vyhledávání hledá shodný význam. Rozdíl je vidět na příkladu z bankovní aplikace. Tester se zeptá: „Co se má stát, když někdo zkouší hesla hrubou silou?“ Ve specifikaci ale stojí: „Po třech neúspěšných pokusech o přihlášení se účet na 15 minut zablokuje.“ Slova „hrubá síla“ ani „heslo“ v požadavku nejsou. Fulltext ho proto nenajde. Embedding dotazu i embedding požadavku ale leží blízko u sebe, protože oba texty mluví o opakovaném neúspěšném přihlášení. Vektorové vyhledávání požadavek najde.

#### Podložená odpověď

Sylabus používá pojem **grounded response** (podložená odpověď). Je to výstup, který vychází z relevantních, přesných a kontextově vhodných informací získaných při vyhledávání. Odpověď se tak neopírá jen o to, co se model naučil při trénování, ale i o konkrétní data k danému promptu. Sylabus to popisuje jako souhru vyhledání a generování, která zvyšuje přesnost, relevanci a spolehlivost odpovědí.

#### Proč RAG pomáhá proti halucinacím

Halucinace často vzniká tam, kde model nemá potřebnou informaci, a přesto musí vygenerovat pravděpodobně znějící text. RAG mu tu informaci dodá přímo do kontextového okna. Model pak nemusí hádat, protože má odpověď před sebou.

Účinek se dá ještě zesílit promptem. Do systémového promptu se napíše, že model smí odpovídat jen z dodaných podkladů a u každého tvrzení má uvést, ze které části čerpal. Když podklady odpověď neobsahují, má to říct. Tester pak může každou odpověď ověřit proti zdroji. To je velký rozdíl proti čistému LLM, kde nemáte s čím porovnávat.

#### Kde RAG selhává

Sylabus v praktickém cíli HO-4.1.2 chce, abyste poznali silné stránky i omezení RAG. Omezení plynou z toho, že RAG je jen tak dobrý, jak dobré jsou podklady a vyhledávání.

:::nad-ramec
Typická selhání RAG v praxi. Sylabus je nevyjmenovává, ale při cvičení HO-4.1.2 na ně narazíte.

Vyhledávání nenajde správnou pasáž. Stává se to, když je dotaz formulovaný jinak než dokumentace, nebo když chunking rozdělí požadavek či tabulku napůl. Model pak dostane jen polovinu informace.

Vyhledávání najde špatnou pasáž. Dvě verze specifikace se liší jen v jednom čísle, ale embeddingy mají téměř stejné. Model dostane starou verzi a odpoví přesvědčivě a chybně. Proto se do metadat ukládá verze a staré verze se z indexu mažou.

Index je zastaralý. Když se dokumenty změní a nikdo je znovu nezpracuje, RAG odpovídá podle stavu z minulého měsíce. Sylabus slibuje sladění s nejnovějšími specifikacemi. To platí jen tehdy, když se index průběžně aktualizuje.

Otázka vyžaduje přehled přes celý dokument. „Kolik požadavků nemá žádný test?“ nebo „Shrň celý sylabus“ jsou úlohy, na které nestačí pět nalezených částí. RAG je dobrý na dohledání konkrétní informace, ne na agregaci přes všechno.

Přesné identifikátory. Embeddingy zachycují význam, ale hůř rozlišují kódy jako REQ-1043 a REQ-1034. Proto se v praxi kombinuje vektorové a fulltextové vyhledávání (hybrid search).

Model kontext ignoruje nebo ho míchá s vlastními znalostmi. RAG halucinace snižuje, ale neodstraňuje. Výstup je pořád potřeba kontrolovat, jak popisuje oddíl 3.1.

Škodlivý obsah v dokumentech. Když někdo do indexovaného dokumentu vloží text s instrukcí pro model, model ho může vykonat. Jde o nepřímou formu prompt injection a souvisí s útoky z oddílu 3.2.2.

Oprávnění. Když back-end při vyhledávání nehlídá, k jakým dokumentům má uživatel přístup, RAG mu může ukázat obsah, který vidět nesmí.
:::

#### RAG v testování

Sylabus shrnuje přínos RAG pro testování jednou myšlenkou. RAG umožňuje testovacímu nástroji s LLM sáhnout do firemních zdrojů dat, jako jsou databáze, dokumentace a repozitáře, a získat kontext v reálném čase. Testovací úlohy, například testovací analýza nebo návrh testů, pak odpovídají nejnovějším specifikacím, požadavkům a existujícím testovacím datům.

Příklad z pojišťovny. Testovací tým má k produktu havarijního pojištění dvě stě stran podmínek, stovky uživatelských scénářů a tisíce existujících testovacích případů. Tester chce navrhnout testy pro novou slevu za bezeškodní průběh. Bez RAG by musel podklady najít a vložit do promptu sám. S RAG zadá jen dotaz. Nástroj najde pasáže podmínek o bonusu a malusu, scénáře k výpočtu pojistného a existující testy výpočtu. Model z toho navrhne nové testy, které navazují na terminologii a strukturu týmu.

:::praxe
Malý RAG nad sylabem CT-GenAI v Pythonu. Sylabus je veřejný dokument, takže se hodí na první pokus bez rizika úniku dat. Celé to jde postavit na notebooku.

Postup má šest kroků. Načíst text sylabu. Rozdělit ho na části zhruba po 300 slovech s malým překryvem, aby se věty na hranicích neztratily. Každou část převést na embedding lokálním modelem z knihovny sentence-transformers. Uložit vektory do paměti jako pole numpy. Při dotazu spočítat embedding dotazu a vybrat čtyři nejpodobnější části podle kosinové podobnosti. Složit prompt a poslat ho modelu.

```python
# rag_sylabus.py – minimální RAG nad sylabem CT-GenAI (jen veřejná data)
import numpy as np
from sentence_transformers import SentenceTransformer

text = open("CT-GenAI_Syllabus_v1.1.txt", encoding="utf-8").read()

def rozdel(text, velikost=300, prekryv=50):
    slova = text.split()
    krok = velikost - prekryv
    return [" ".join(slova[i:i + velikost]) for i in range(0, len(slova), krok)]

casti = rozdel(text)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
vektory = model.encode(casti, normalize_embeddings=True)   # předzpracování

def najdi(dotaz, k=4):
    v = model.encode([dotaz], normalize_embeddings=True)[0]
    skore = vektory @ v                    # kosinová podobnost (vektory jsou normované)
    nej = np.argsort(skore)[::-1][:k]
    return [(float(skore[i]), casti[i]) for i in nej]

def prompt(dotaz):
    kontext = "\n---\n".join(c for _, c in najdi(dotaz))
    return ("Odpovídej jen z podkladů níže. Když v nich odpověď není, napiš to.\n"
            f"PODKLADY:\n{kontext}\n\nOTÁZKA: {dotaz}")

print(prompt("Which challenges of fine-tuning does the syllabus list?"))
# Výsledný prompt pošlete modelu, který máte schválený (klíč v proměnné prostředí).
```

Jak výsledek otestovat. Připravte si deset otázek, na které znáte odpověď ze sylabu, a k nim čísla oddílů. U každé otázky zkontrolujte dvě věci zvlášť. Nejdřív vyhledání: je mezi nalezenými částmi ta správná? Potom generování: odpověděl model správně a jen z podkladů? Stejné otázky pak položte modelu bez RAG a výsledky porovnejte. Přesně to chce praktický cíl HO-4.1.2.

Na co si dát pozor. Sylabus je anglicky, takže anglický model pro embeddingy stačí. Pro české dotazy nad anglickým textem použijte vícejazyčný model, jinak vyhledávání selže. Textový převod PDF obsahuje záhlaví „© International Software Testing Qualifications Board“ na každé straně. Před chunkingem je dobré je odstranit, jinak ruší podobnost.
:::

:::zkouska
Pořadí kroků předzpracování: rozdělit na části, vyčistit a zpracovat, převést na embeddingy, uložit do vektorové databáze. Při dotazu: zakódovat dotaz, vyhledat podobné části, předat je modelu jako kontext, vygenerovat odpověď. Vyhledání je vždy před generováním.

RAG nemění váhy modelu. Data dodává za běhu, při inferenci. To ho odlišuje od fine-tuningu. Otázka, která tvrdí, že RAG model „přeučí“ nebo že si model dokumenty „zapamatuje“, je chybná.

Důvod chunkingu je cílené vyhledání a vejití se do kontextového okna. Úspora místa v databázi to není.

Vyhledávání je sémantické, podle podobnosti embeddingů. Není to vyhledávání podle klíčových slov.

Pozor na rozpor s kurzy. Jeden z kurzů tvrdí, že u kritické aplikace je nejlepší ručně projít vyhledané podklady a teprve pak dotaz doladit. Oficiální vzorová zkouška ISTQB bere takový ruční mezikrok jako zbytečnou práci, která jde proti smyslu RAG. Smyslem RAG je, že vyhledání a předání kontextu proběhne automaticky. Jiný kurz zase tvrdí, že když nástroj generuje testy vždy ve stejném formátu, je to RAG. Není. Jednotný formát zajišťuje prompt, šablona nebo post-processing.
:::

### 4.1.3 Agenti postavení na LLM v automatizaci testovacích procesů

:::pojem term="LLM-powered agent"
Agent postavený na LLM. Aplikace, která spojuje uvažování a rozhodování LLM s pamětí a pomocí nástrojů provádí úlohy. Podle sylabu je určená k poloautonomnímu nebo autonomnímu zpracování definovaných úloh.
:::

Sylabus popisuje agenty postavené na LLM jako specializované aplikace generativní AI. Jejich jádrem je LLM, které rozumí přirozenému jazyku a umí ho generovat. K tomu agent umí zpracovat instrukce, získat kontext a provést rozumné akce.

Rozdíl proti chatbotu je jeden a sylabus ho pojmenovává přesně. Chatbot jen odpovídá na otázky. Agent umí jednat. Dělá to tak, že volá předem definovanou sadu funkcí, kterým se říká **tools** (nástroje). Nástrojem může být čtení souboru, dotaz do databáze, volání REST API, spuštění testů, vytvoření záznamu v Jiře nebo odeslání zprávy. Díky nástrojům agent pracuje s externími systémy a mění je.

Příklad rozdílu. Chatbotu napíšete: „Navrhni testy pro tento uživatelský scénář.“ Dostanete text, který zkopírujete do nástroje pro správu testů. Agentovi napíšete totéž. Agent si scénář sám načte z backlogu, navrhne testy, zapíše je jako testovací případy a připojí k nim odkaz na scénář.

#### Smyčka agenta: plánování, nástroje, paměť

Slovníková definice v sylabu jmenuje čtyři schopnosti: uvažování, rozhodování, paměť a nástroje. V praxi se skládají do smyčky, kterou agent opakuje, dokud úlohu nesplní.

```text
                 +-------------------------------+
   cíl --------> | 1. PLÁNOVÁNÍ (LLM)            |
   od člověka    |    rozlož cíl na kroky,       |
                 |    vyber další krok a nástroj |
                 +-------------------------------+
                        |                ^
                        v                |
                 +----------------+      |       +------------------+
                 | 2. AKCE        |      |       | PAMĚŤ            |
                 |    volání      |      +-------| krátkodobá:      |
                 |    nástroje    |              | kontext běhu     |
                 +----------------+              | dlouhodobá:      |
                        |                        | soubory, DB      |
                        v                        +------------------+
                 +----------------+                      ^
                 | 3. POZOROVÁNÍ  |                      |
                 |    výsledek    | ---------------------+
                 |    nástroje    |   4. zápis do paměti
                 +----------------+
                        |
                        v
              hotovo? -- ne --> zpět na 1
                 |
                ano
                 v
     +-------------------------+       +---------------------------+
     | kontrolní bod: člověk   | ----> | výsledek, report, záznam  |
     | nebo automatická        |       +---------------------------+
     | verifikace              |
     +-------------------------+
```

Plánování dělá LLM. Dostane cíl, třeba „zjisti, proč v nočním běhu spadlo dvanáct testů“. Rozloží ho na kroky: načíst report, seskupit chyby, podívat se na poslední změny v kódu, navrhnout příčinu. Pak vybere první krok a nástroj, kterým ho provede.

Akce je volání nástroje. Model sám nic nespouští. Vygeneruje strukturovaný požadavek, například název funkce a parametry, a aplikace kolem modelu ho provede.

Pozorování je výsledek nástroje. Vrátí se modelu jako další kontext. Model z něj zjistí, jestli krok vyšel, a naplánuje další.

Paměť má dvě úrovně. Krátkodobá paměť je to, co se vejde do kontextového okna během jednoho běhu: zadání, dosavadní kroky a jejich výsledky. Dlouhodobá paměť přežije konec běhu. Může to být soubor s poznámkami, databáze nebo vektorový index. Agent si do ní uloží, co se naučil, a při dalším běhu to načte.

:::nad-ramec
Rozklad na plánování, akci, pozorování a paměť je obecný model, se kterým pracuje většina agentních nástrojů. Sylabus ho takto nekreslí. Ke zkoušce stačí vědět, co sylabus říká: agent využívá LLM k porozumění a generování, zpracovává instrukce, získává kontext, volá nástroje a slovníková definice k tomu přidává paměť a rozhodování.
:::

#### Úrovně autonomie

Sylabus rozlišuje dvě úrovně autonomie. Rozdíl je v tom, jak často do práce agenta vstupuje člověk.

**Autonomous agents** (autonomní agenti) pracují samostatně s minimálním zásahem člověka. Řídí se předem danými pravidly, učením posilováním (**reinforcement learning**) a adaptivními zpětnovazebními smyčkami.

**Semi-autonomous agents** (poloautonomní agenti) pracují s pravidelným dohledem člověka. Člověk kontroluje, že výstup odpovídá cílům, které uživatel stanovil.

V praxi se pro druhý případ používá pojem **human-in-the-loop** (člověk ve smyčce). Agent v určitém bodě zastaví a čeká na schválení. Typicky před akcí, která něco mění mimo agenta: zapsání defektu, odeslání zprávy, smazání dat nebo nasazení.

Následující tabulka obě úrovně porovnává na stejné úloze.

| | Autonomní agent | Poloautonomní agent |
|---|---|---|
| Úloha | noční běh regresních testů a hlášení chyb | totéž |
| Zásah člověka | minimální, člověk čte až souhrn | člověk schvaluje vybrané kroky |
| Co agent udělá sám | spustí testy, roztřídí chyby, založí defekty v Jiře | spustí testy, roztřídí chyby, připraví návrhy defektů |
| Kontrolní bod | automatická verifikace, například kontrola duplicit | tester potvrdí, že jde o defekt, a teprve pak se založí |
| Vhodné pro | úlohy s nízkým rizikem a jasnými pravidly | kritické úlohy, kde chyba agenta něco stojí |

Z tabulky plyne, že autonomie není vlastnost, kterou agent buď má, nebo nemá. Nastavuje se podle rizika úlohy. Stejný agent může u interní webové aplikace zakládat defekty sám a u platebního systému banky jen navrhovat.

#### Více agentů a orchestrace

**Multi-agent architectures** (multiagentní architektury) jsou systémy, kde spolupracuje několik agentů. Každý má specializovanou roli. Agenti spolu komunikují a koordinují se. Složité problémy tak řeší efektivněji než jeden agent. Této koordinaci se říká **orchestration** (orchestrace).

Příklad z testování. První agent analyzuje požadavky a hledá v nich nejasnosti. Druhý z nich navrhuje testovací podmínky a testovací případy. Třetí píše automatizované testy v Playwrightu. Čtvrtý je spouští a pátý vyhodnocuje výsledky a píše report. Orchestrátor rozhoduje, kdo je na řadě, a předává výstupy dál. Sylabus k tomu dodává, že agenti takto napodobují lidské uvažování a rozhodování.

:::pojem term="orchestration"
Orchestrace. Koordinovaná spolupráce více agentů se specializovanými rolemi, kteří společně řeší složitou úlohu.
:::

#### Agenti v testovacích nástrojích

Sylabus popisuje, jak se agenti dostávají k testerům. Bývají schovaní v AI asistentech, které jsou zabudované přímo do testovacích nástrojů. Asistent převádí uživatelské scénáře nebo požadavky na testware. Pokrývá přitom celý testovací proces: testovací analýzu, návrh testů, implementaci testů, provedení testů a reportování. Dělá to poloautonomně.

Výsledkem je souvislý automatizovaný tok práce od požadavku po report. Ubývá ruční práce a zkracuje se doba, za kterou tým dostane zpětnou vazbu. Sylabus to shrnuje jako posun automatizace testování od provádění skriptů k automatizaci řízené cílem a postavené na agentech (**goal-driven, agent-based test automation**). Klasický automatizovaný test je skript, který přesně říká, co udělat. Agent dostane cíl, třeba „ověř, že se uživatel může odhlásit z newsletteru“, a kroky si odvodí sám.

#### Rizika agentů

Agenti stojí na LLM, takže mají stejné problémy. Sylabus jmenuje halucinace, chyby v uvažování (**reasoning errors**) a zkreslení (**bias**) z oddílu 3.1. Agent může dát nesprávné nebo zavádějící výsledky, a tím oslabit spolehlivost automatizovaných testovacích procesů.

U agenta je dopad chyby větší než u chatbotu. Chatbot chybu napíše a člověk ji může přehlédnout nebo opravit. Agent chybu rovnou provede. Založí dvacet falešných defektů, „opraví“ test tak, aby prošel, i když aplikace je rozbitá, nebo smaže testovací data jiného týmu.

Sylabus uvádí dvě opatření. Prvním je automatická verifikace výsledků agenta. Například kontrola, že každý navržený test odkazuje na existující požadavek, že vygenerovaný kód jde přeložit a že defekt není duplicitou existujícího. Druhým je použití poloautonomních agentů pro kritické úlohy, tedy člověk ve smyčce.

:::nad-ramec
Další opatření z praxe. Agent má mít jen ty nástroje a oprávnění, které k úloze potřebuje (princip nejmenších oprávnění). Má běžet v izolovaném prostředí, ne s přístupem k produkci. Každé volání nástroje se má logovat, aby šlo zpětně dohledat, co agent udělal. A má mít limity: maximální počet kroků, čas a cenu za běh.

Ve firemním prostředí platí ještě jedno pravidlo. Agent se k firemním systémům, jako je M365, Jira nebo GitLab, připojuje jen přes oficiální a auditovatelné rozhraní. Typicky je to registrovaná aplikace nebo servisní účet se schválenými oprávněními. Když přístup chybí, řeší se s týmem, který schvaluje AI nástroje, a ne obcházením.
:::

#### Ukázka: agent na opakovanou úlohu

Praktický cíl HO-4.1.3 chce ukázat, jak agent pomáhá s opakovanou testovací úlohou. Sylabus chce vidět tři věci: vstupní data, chování agenta a výsledky jeho akcí.

Vezměme webovou aplikaci a každodenní triáž nočního běhu. Vstupem je report z běhu ve formátu JUnit XML, seznam změn v gitu od posledního běhu a přístup k Jiře. Agent report načte a zjistí, že padlo dvanáct testů. Seskupí je podle chybové hlášky. Osm padá na stejném lokátoru tlačítka „Odeslat“, tři na vypršení času na API a jeden na kontrole textu. U skupiny s lokátorem najde v gitu commit, který přejmenoval CSS třídu. U API se podívá do logů a zjistí, že testovací prostředí bylo v noci restartované. Výsledkem je souhrn se třemi skupinami a návrhem: jeden defekt na změněný lokátor, opakování testů API a ruční kontrola posledního testu. Tester souhrn zkontroluje a schválí založení defektu. Ráno tak tester čte hotovou analýzu místo dvanácti stack trace.

:::praxe
Šmoula jako agent postavený na LLM. V oddílu 4.1.1 jsme Šmoulu popsali jako infrastrukturu. Teď ho popíšeme jako agenta.

LLM a plánování zajišťuje Claude Code s modelem Claude. Claude Code sám rozloží zadání na kroky a vybírá, který nástroj použije.

Nástroje jsou to, co Claude Code umí volat: číst a zapisovat soubory, spouštět příkazy v shellu a pracovat s gitem. Každý přidaný nástroj zvětšuje, co Šmoula dokáže, a zároveň co může pokazit.

Paměť má dvě úrovně přesně podle modelu výše. Krátkodobá paměť je kontext jednoho běhu Claude Code. Dlouhodobá paměť jsou markdownové soubory v privátním GitHub repozitáři. Díky gitu má každá změna paměti historii a dá se vrátit.

Autonomie se u Šmouly liší podle typu úlohy. Plánované úlohy běží bez člověka, takže jsou autonomní. Konverzace přes Telegram jsou poloautonomní, protože Jan výsledek čte a reaguje na něj. Rozumné pravidlo je, aby akce s vedlejším efektem mimo repozitář, například odeslání zprávy někomu jinému nebo zápis do cizího systému, vyžadovala potvrzení v Telegramu. To je člověk ve smyčce.

Rizika ze sylabu platí i tady. Šmoula může halucinovat fakta do paměti, a ta se pak vrací v dalších bězích. Automatická verifikace může být jednoduchá: plánovaná úloha jednou týdně projde nové poznámky a označí tvrzení bez zdroje.
:::

:::nad-ramec
MCP, Claude Code a n8n. Sylabus tyto nástroje nezmiňuje, ale v praxi jsou to nejčastější způsoby, jak dnes agenta postavit.

**Model Context Protocol** (MCP) je otevřený protokol, který sjednocuje, jak se k aplikaci s LLM připojují nástroje a zdroje dat. Místo psaní vlastní integrace pro každý systém se připojí MCP server. V kurzu Rahula Shettyho jsou ukázky MCP serverů pro Playwright (ovládání prohlížeče), databázi, souborový systém a REST API. Agent z jednoho zadání v angličtině vyplní registrační formulář daty z databáze, přes API ověří přihlášení a výsledek zapíše do Excelu. Pojmy ze sylabu: MCP servery jsou nástroje, aplikace s LLM je agent.

**Claude Code** je agent pro práci s kódem v terminálu. Čte projekt, spouští příkazy a mění soubory. Umí pracovat s takzvanými skills, tedy soubory s instrukcemi a znalostmi, které načte jen tehdy, když jsou k úloze potřeba. V kurzu jsou ukázky agentů, kteří z doménové dokumentace navrhují testovací scénáře, rozdělují je do úrovní testovací pyramidy, píšou testy v Playwrightu a opravují ty, které padají. Spojení několika takových agentů s různou rolí odpovídá multiagentní architektuře ze sylabu.

**n8n** je nástroj pro automatizaci pracovních postupů. Jeho uzel AI Agent má tři části, které odpovídají smyčce výše: model jako „mozek“, paměť na posledních několik zpráv a nástroje, například Google Sheets, e-mail, Telegram nebo Jira.

U všech tří platí totéž co v sylabu. Agent může halucinovat a chybovat, a čím víc nástrojů má, tím větší škodu může udělat.
:::

:::zkouska
Agent se od chatbotu liší tím, že jedná: volá nástroje a mění externí systémy. Chatbot jen odpovídá.

Autonomní a poloautonomní agent se liší mírou zapojení člověka. Autonomní pracuje s minimálním zásahem, poloautonomní s pravidelným dohledem. Jejich kombinace umožňuje zlepšit efektivitu i kvalitu zároveň. Nejde o volbu „buď rychle, nebo kvalitně“.

Orchestrace je koordinace více agentů se specializovanými rolemi. Neznamená ovládání jednoho agenta člověkem.

Agenti nemají méně rizik než LLM. Mají stejná rizika: halucinace, chyby v uvažování a zkreslení. Odpověď, že agenti odstraňují potřebu verifikace nebo lidského dohledu, je vždy špatně. Sylabus doporučuje automatickou verifikaci výsledků a poloautonomní agenty pro kritické úlohy.

Posun, který sylabus popisuje, je od automatizace založené na skriptech k automatizaci řízené cílem a postavené na agentech.
:::

## 4.2 Fine-tuning a LLMOps: provozování generativní AI v testování

:::lo
GenAI-4.2.1 (K2) Explain the fine-tuning of language models for specific test tasks
GenAI-4.2.2 (K2) Explain LLMOps and its role in deploying and managing LLMs for test tasks
:::

Oddíl 4.1 popsal, jak testovací nástroj s LLM postavit. Oddíl 4.2 popisuje, jak ho dostat do skutečného provozu. Sylabus k tomu jmenuje dvě praktiky. Fine-tuning přizpůsobí samotný model úloze. LLMOps řídí celý provozní řetězec kolem modelu.

### 4.2.1 Fine-tuning LLM pro testovací úlohy

:::pojem term="fine-tuning"
Doladění modelu. Učení s učitelem na datové sadě označených příkladů, které upraví váhy LLM a přizpůsobí model konkrétním úlohám nebo doméně.
:::

Sylabus definuje fine-tuning jako přizpůsobení předtrénovaného jazykového modelu konkrétním úlohám nebo doméně. Jazykovým modelem může být velký model (LLM) nebo malý model (**small language model**, SLM) z oddílu 1.1.2. Model se dál trénuje na cílené datové sadě. Naučí se z ní znalosti a jemné rozdíly dané domény. Výsledkem je model, který je pro danou úlohu přesnější a relevantnější.

S fine-tuningem jste se už potkali. V oddílu 1.1 sylabus popisuje, že modely vyladěné na instrukce (**instruction-tuned LLMs**) vznikají z foundation modelů doladěním na dvojicích prompt a očekávaná odpověď. Je to stejný princip. Rozdíl je jen v tom, že tady model dolaďuje organizace pro svou úlohu.

Podstatné je, co se při fine-tuningu mění. Při promptování ani při RAG se model nemění, mění se jen vstup. Při fine-tuningu se mění parametry modelu, tedy jeho váhy. Model si nové chování odnese do každého dalšího dotazu, aniž byste mu ho museli vysvětlovat.

#### Kdy se fine-tuning hodí

Sylabus uvádí dva hlavní důvody. Fine-tuning dává obecným modelům specializované schopnosti uvažovat v konkrétní doméně. A naučí je slovník, který je pro daný obor typický.

Sylabus k tomu zdůrazňuje malé modely. SLM potřebuje méně výpočetních zdrojů. Doladěný SLM může u konkrétní úlohy dosáhnout vysokého výkonu bez nákladů, které by vyžadovalo doladění LLM. Volba mezi LLM a SLM se tedy řídí požadavky úlohy.

Příklad ze sylabu: model generuje testovací případy z uživatelských scénářů ve výstupním formátu, který používá konkrétní organizace. Model se dotrénuje na uživatelských scénářích organizace a k nim napsaných testovacích případech. Tím se přizpůsobí testovacímu procesu a terminologii organizace.

Pro představu, jak taková trénovací data vypadají. Každý řádek je jeden příklad: vstup a očekávaný výstup. Následující ukázka je smyšlená.

```json
{"vstup": "Jako klient chci změnit denní limit platební karty v mobilní aplikaci, abych mohl zaplatit vyšší nákup.",
 "vystup": "TC-KAR-001 | Změna limitu v povoleném rozsahu | Předpoklad: přihlášený klient, aktivní karta | Kroky: 1. Otevřít detail karty 2. Zadat limit 50 000 Kč 3. Potvrdit SMS kódem | Očekávaný výsledek: limit 50 000 Kč platí okamžitě, klient dostane notifikaci | Ref: US-412"}
{"vstup": "Jako klient chci dočasně zablokovat kartu, když ji nemůžu najít.",
 "vystup": "TC-KAR-014 | Dočasná blokace karty | Předpoklad: přihlášený klient, aktivní karta | Kroky: 1. Otevřít detail karty 2. Zvolit Dočasně blokovat 3. Potvrdit | Očekávaný výsledek: karta je ve stavu Blokovaná, platby jsou zamítnuté, odblokování je dostupné | Ref: US-415"}
```

Model po doladění na stovkách takových dvojic generuje testy ve stejném formátu, se stejnou strukturou identifikátorů a se stejnými obraty. Promptem by šlo dosáhnout podobného výsledku, ale prompt by musel formát popisovat a obsahovat příklady pokaždé znovu.

#### Prompt engineering, RAG nebo fine-tuning

Sylabus v oddílu 3.1.3 říká, že RAG a fine-tuning jsou dvě doplňující se techniky pro lepší výsledky LLM. Když je pochopíte spolu s prompt engineeringem, rozhodování je jednodušší. Tabulka shrnuje rozdíly.

| | Prompt engineering | RAG | Fine-tuning |
|---|---|---|---|
| Co se mění | jen prompt | prompt se doplní o vyhledaná data | váhy modelu |
| Kdy působí | při každém dotazu | při každém dotazu | trvale, po doladění |
| Na co se hodí | rychlé a různorodé úlohy | aktuální fakta z dokumentů | stálý formát, styl, slovník, úzká opakovaná úloha |
| Změna podkladů | přepsat prompt | znovu zpracovat dokument | znovu trénovat |
| Náklady na začátek | nízké | střední | vysoké: data, výpočet, odborníci |
| Dohledatelnost zdroje | podle toho, co je v promptu | dobrá, odpověď lze vázat na nalezené části | špatná, znalost je rozpuštěná ve vahách |

Z tabulky plyne praktické pravidlo. Začíná se promptem. Když model potřebuje fakta, která se mění nebo která nezná, přidá se RAG. Fine-tuning přichází na řadu, když úloha je úzká a stále stejná, když chcete jednotné chování bez dlouhých promptů, nebo když potřebujete malý model, který poběží uvnitř organizace.

Fine-tuning naopak není vhodný na doplnění faktů, které se často mění. Každá změna specifikace by znamenala nový trénink. A model by po doladění pořád neuměl říct, odkud informaci má. Techniky se dají kombinovat. Doladěný model může dostávat podklady přes RAG.

:::nad-ramec
Rozhodovací pravidlo i tabulka jsou shrnutí z praxe, sylabus je takto nepodává. Sylabus říká jen to, že obě techniky se doplňují, že RAG dodává data za běhu a že fine-tuning model trvale přizpůsobuje úloze, doméně a slovníku. Na zkoušce stačí poznat, která technika mění model a která ne, a k čemu se která hodí.
:::

#### Postup fine-tuningu

Praktický cíl HO-4.2.1 popisuje ukázku procesu ve čtyřech krocích. Výběr vhodného LLM nebo SLM. Představení datové sady připravené pro danou testovací úlohu. Ukázka řešení samotného doladění, například v knihovně pro strojové učení. A nakonec poslání promptu doladěnému modelu a rozbor kvality výstupu. Sylabus přitom zdůrazňuje hlavně kvalitu trénovacích dat.

V praxi se mezi tyto kroky vkládá ještě několik dalších. Úplný postup vypadá takto.

1. Definovat úlohu a kritéria úspěchu. Například: z uživatelského scénáře vygenerovat testovací případy ve formátu týmu, aspoň devět z deseti bez ruční opravy formátu.
2. Vybrat model. Menší model je levnější na trénink i provoz a může běžet uvnitř organizace. Větší model zvládne složitější uvažování.
3. Připravit datovou sadu. Dvojice vstup a očekávaný výstup, které jsou správné, jednotné a pokrývají různé typy případů. Data se zbaví osobních a citlivých údajů. Rozdělí se na trénovací, validační a testovací část.
4. Doladit model. Používá se knihovna pro strojové učení a výpočetní výkon, obvykle grafické karty.
5. Vyhodnotit. Doladěný model dostane příklady, které při tréninku neviděl, a výsledek se porovná s původním modelem a s kritérii z prvního kroku.
6. Nasadit a sledovat. To už je oblast LLMOps z oddílu 4.2.2.

:::nad-ramec
Dnes se nejčastěji nedolaďují všechny váhy modelu. Používají se úsporné metody (parameter-efficient fine-tuning, PEFT), například LoRA. Ty trénují jen malou přidanou část parametrů. Doladění malého modelu se tak vejde na jednu grafickou kartu. Typické nástroje jsou knihovny Hugging Face Transformers a PEFT. Na zkoušce se tyto názvy neobjevují.
:::

#### Výzvy fine-tuningu

Sylabus jmenuje čtyři výzvy. Na zkoušce se objevují jako seznam, ze kterého je potřeba poznat, co do něj nepatří.

První výzvou jsou zkreslené nebo nepřesné výsledky. Model se naučí přesně to, co je v datech. Když jsou v trénovacích testech chyby, model je bude opakovat. Když data pokrývají jen pozitivní scénáře, model bude negativní testy vynechávat. Jedinou obranou je kvalitní datová sada zaměřená na danou úlohu.

Druhou výzvou je **overfitting** (přeučení). Model se příliš přizpůsobí trénovacím datům a na nových, neviděných datech funguje hůř. Ztrácí schopnost zobecnit na jiné situace. Příklad: model doladěný jen na scénářích z modulu karet bude i u úvěrů psát kroky o kartě.

Třetí výzvou je **opacity** (neprůhlednost). Není vidět, jak LLM dospívá ke svým rozhodnutím a výstupům. To komplikuje ladění i validaci. Když doladěný model generuje špatné testy, nedá se snadno zjistit, který trénovací příklad za to může.

Čtvrtou výzvou jsou výpočetní zdroje. Doladění LLM vyžaduje značný výpočetní výkon. Sylabus to vztahuje výslovně k velkým modelům. U SLM jsou nároky nižší.

:::pojem term="overfitting"
Přeučení. Model je příliš přizpůsobený trénovacím datům a na nových, dosud neviděných datech dává horší výsledky.
:::

:::praxe
Šmoula fine-tuning nepotřebuje. Šmoula pracuje s hotovým modelem přes Claude Code. Jeho znalosti o Janovi a projektech se mění každý den a leží v markdownu v gitu. To je přesně případ, kdy se data dodávají za běhu, ne trénují do vah. Doladění by znamenalo jiný model, vlastní trénink a vlastní provoz, a s každou novou poznámkou by bylo zastaralé.

Fine-tuning by smysl dával u jiné úlohy. Malý model běžící přímo na serveru v Oracle Cloud by mohl třídit příchozí zprávy do pěti kategorií: úkol, poznámka, dotaz, připomínka, ostatní. Úloha je úzká, stále stejná a dá se na ní připravit několik stovek příkladů z vlastní historie zpráv. Doladěný SLM by ji zvládl levně a bez posílání zpráv třetí straně.
:::

:::zkouska
Fine-tuning mění váhy modelu. Promptování a RAG je nemění. To je nejčastější rozlišovací otázka.

Fine-tuning nenahrazuje obecné znalosti modelu úlohovými znalostmi. Přidává specializaci k tomu, co model už umí.

Fine-tuning nezaručuje, že nedojde k přeučení. Přeučení je jedna ze čtyř výzev, které je potřeba aktivně hlídat.

Doladit lze LLM i SLM. Doladěný SLM může u úzké úlohy dosáhnout vysokého výkonu s menšími nároky.

Čtyři výzvy ze sylabu: zkreslené nebo nepřesné výsledky kvůli špatným datům, přeučení, neprůhlednost a výpočetní nároky. Když je v nabídce jiná „výzva“, například „model po doladění neumí přirozený jazyk“, do seznamu nepatří.
:::

### 4.2.2 LLMOps při nasazení a správě LLM pro testování

:::pojem term="Large Language Model Operations (LLMOps)"
LLMOps. Soubor praktik, nástrojů a procesů, které zjednodušují vývoj, nasazení a údržbu LLM v produkčním prostředí. Slovník sylabu to shrnuje jako nasazení, monitoring a údržbu LLM v provozu.
:::

LLMOps je pro velké jazykové modely totéž, co DevOps pro software a MLOps pro modely strojového učení. Řeší, jak model a aplikaci kolem něj dostat do provozu, udržet je v chodu a měnit je bez nehod.

Sylabus k LLMOps přistupuje přes to, jak organizace generativní AI v testování používá. Podle způsobu použití se mění rozhodnutí, která LLMOps musí udělat. Sylabus popisuje tři přístupy.

#### Přístup 1: AI chatbot

Testeři používají chatbot. Hlavní otázkou je ochrana dat a bezpečnost a k tomu optimalizace nákladů. Organizace má dvě cesty. Může použít platformu typu **LLM-as-a-Service** (LLM jako služba), pokud poskytovatel dá potřebné záruky. Nebo si postaví vlastní infrastrukturu s LLM pod open-source licencí a získá větší kontrolu. Sylabus požaduje důkladné posouzení záruk dodavatele, případně vlastních schopností. Cílem je zmírnit rizika pro ochranu dat a bezpečnost z oddílu 3.2 a zajistit efektivní provoz.

#### Přístup 2: testovací nástroj se schopnostmi generativní AI

Organizace používá hotový testovací nástroj, který má AI funkce zabudované. Platí stejné otázky jako u chatbotu: ochrana dat, bezpečnost a provozní náklady. Navíc musí organizace posoudit záruky, které k bezpečnosti dat a výkonu dává poskytovatel nástroje. Takové nástroje obvykle doplňují existující testovací procesy. Proto sylabus požaduje důkladnou analýzu nákladů a přínosů a posouzení rizik.

#### Přístup 3: vlastní vývoj testovacího nástroje s generativní AI

Organizace si nástroj postaví sama. Tento přístup dává nejvíc kontroly nad riziky ochrany dat a bezpečnosti. Vyžaduje ale pečlivé plánování zdrojů pro AI: výpočetní výkon, úložiště dat a školení lidí. Organizace musí zavést strukturované procesy pro validaci a údržbu toho, co vyvine. A potřebuje odborníky, kteří umí infrastrukturu testování s LLM implementovat a nasadit.

Tabulka shrnuje, co je u kterého přístupu navíc.

| Přístup | Hlavní otázky LLMOps | Co je typické jen pro tento přístup |
|---|---|---|
| AI chatbot | ochrana dat, bezpečnost, náklady | volba mezi LLM jako službou a vlastním open-source modelem, posouzení záruk dodavatele |
| Testovací nástroj s GenAI | ochrana dat, bezpečnost, provozní náklady | posouzení záruk poskytovatele nástroje k bezpečnosti a výkonu, analýza nákladů a přínosů |
| Vlastní vývoj | plná kontrola nad ochranou dat a bezpečností | plánování výpočetního výkonu, úložiště a školení, procesy validace a údržby, vlastní odbornost |

Sylabus dodává dvě věci, na které se zkouška ráda ptá. Přístupy se navzájem nevylučují. Organizace může pro některé úlohy používat chatbot a pro jiné si vyvíjet vlastní nástroje, a to současně. A všechny přístupy lze rozšířit o RAG a o fine-tuning LLM nebo SLM.

Příklad z banky. Testeři používají firemně schválený chatbot na obecné otázky, třeba na vysvětlení techniky testování nebo návrh struktury testovacího plánu. V nástroji pro správu testů mají zapnuté AI funkce dodavatele, které generují návrhy testů z požadavků. Před zapnutím banka prověřila, kde dodavatel data zpracovává a jestli je nepoužívá k tréninku. A pro práci s produkčně podobnými daty si banka vyvíjí vlastní nástroj s open-source modelem ve vlastním datovém centru, doplněný o RAG nad interní dokumentací. Všechny tři přístupy běží vedle sebe.

#### Co LLMOps dělá v provozu

Sylabus u LLMOps mluví o vývoji, nasazení a údržbě a slovník přidává monitoring. Konkrétní činnosti nevyjmenovává. Pro pochopení je dobré vědět, co se pod těmi slovy v praxi skrývá.

:::nad-ramec
Typické činnosti LLMOps rozdělené podle fází. Sylabus je takto nerozepisuje.

Vývoj. Prompty a systémové prompty se ukládají do gitu stejně jako kód. Každá změna promptu má verzi, autora a důvod. Spolu s nimi se verzuje konfigurace: název a verze modelu, teplota, maximální délka odpovědi a nastavení RAG.

Evaluace. Před každou změnou promptu, modelu nebo indexu RAG se spustí sada testovacích dotazů s očekávanými vlastnostmi odpovědi. Kontroluje se formát, přítomnost povinných informací, odkazy na zdroje a zakázaný obsah. Část se hodnotí automaticky, část člověk. Výstup lze porovnat i s jiným LLM, jak popisuje oddíl 3.2.3. Kvůli nedeterministickému chování z oddílu 3.1.4 se každý dotaz pouští víckrát.

Nasazení. Volí se hostování: služba třetí strany, zabezpečený cloud nebo vlastní infrastruktura. Nastavuje se řízení přístupu. Tajné klíče patří do trezoru nebo proměnných prostředí, nikdy do kódu. Nová verze promptu nebo modelu se pouští nejdřív na malou část uživatelů.

Monitoring. Sleduje se doba odezvy, chybovost, počet tokenů a cena, počet odmítnutých odpovědí a kvalita na náhodném vzorku. Hlídá se změna chování, když poskytovatel model aktualizuje. Logy se sbírají tak, aby v nich nebyla citlivá data.

Údržba. Aktualizuje se index RAG, když se změní dokumenty. Model se znovu dolaďuje, když se změní formát nebo proces. Staré verze modelů se vyřazují dřív, než je poskytovatel přestane podporovat.

Pro testera je z toho podstatné, že nástroj s LLM je také software, který se musí testovat. Evaluační sada promptů je jeho regresní test.
:::

:::praxe
LLMOps pro Šmoulu. Šmoula je malý vlastní vývoj, tedy třetí přístup ze sylabu. Jan nese plnou kontrolu i plnou odpovědnost.

Verzování. Instrukce pro Claude Code a šablony promptů jsou v gitu. Každá změna má commit se zdůvodněním. Když se chování Šmouly zhorší, jde dohledat, která změna to způsobila.

Monitoring. Každý běh se zapíše do logu: čas, typ úlohy (zpráva z Telegramu nebo plánovaná úloha), doba trvání, výsledek a spotřeba, pokud ji nástroj vykazuje. Selhaná plánovaná úloha pošle upozornění do Telegramu. Jednou týdně stačí projít souhrn: kolik běhů selhalo, které úlohy trvaly nejdéle a jestli roste spotřeba.

Evaluace. Deset typických zadání s popsaným očekávaným výsledkem, třeba „najdi v paměti poznámku o kurzu X“ nebo „shrň včerejší zprávy“. Sada se pustí po každé větší změně instrukcí nebo po aktualizaci Claude Code.

Bezpečnost. Přístupové údaje k Telegramu, GitHubu a API jsou v proměnných prostředí na serveru, ne v repozitáři. Do paměti v gitu nepatří hesla, tokeny ani firemní a klientská data.
:::

:::zkouska
Hlavním zaměřením LLMOps je řídit LLM po celý jejich životní cyklus, včetně ochrany dat, bezpečnosti a nákladů. LLMOps neslouží k omezení používání generativní AI, nezužuje ji na chatboty a neodstraňuje lidský dohled.

U otázky na přístupy si všímejte, co je pro který přístup jedinečné. Posouzení záruk poskytovatele testovacího nástroje k bezpečnosti dat a výkonu patří k druhému přístupu. Plánování výpočetního výkonu, úložiště a školení a vlastní procesy validace patří k vlastnímu vývoji. Volba mezi LLM jako službou a vlastním open-source modelem je uvedená u chatbotu.

Přístupy se nevylučují a lze je kombinovat s RAG i fine-tuningem. Odpověď „organizace si musí vybrat jeden přístup“ je špatně.
:::

:::zkouska
Rychlý přehled celé kapitoly. Infrastruktura testování s LLM má front-end, back-end a LLM. Back-end ověřuje uživatele, vyhledává v relační a vektorové databázi, připravuje prompt, volá LLM a upravuje výstup. RAG přidává vyhledávání: předem rozdělí dokumenty na části, převede je na embeddingy a uloží do vektorové databáze, při dotazu najde podobné části a předá je modelu. Agent jedná přes nástroje, může být autonomní nebo poloautonomní, více agentů spolupracuje v orchestraci a všichni potřebují verifikaci. Fine-tuning mění váhy modelu a má čtyři výzvy. LLMOps řídí model v provozu a rozhodnutí závisí na tom, jestli organizace používá chatbot, hotový nástroj, nebo vlastní vývoj.
:::
