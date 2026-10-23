---
kapitola: 5
varianta: zkracena
nadpis: Zavedení a integrace generativní AI v testovací organizaci
podtitul: To nejnutnější ke zkoušce: stínová AI, strategie, výběr modelu, tři fáze, dovednosti, budování týmu a posun rolí.
---

Kapitola 5 má 80 minut, jediný klíčový pojem **shadow AI** (stínová AI) a u zkoušky 7 otázek, z každého LO jednu. Čtyři LO jsou K1 (5.1.1, 5.1.4, 5.2.2, 5.2.3). U nich se zkoušejí výčty, často skoro slovy sylabu.

## 5.1 Plán zavedení generativní AI v testování

:::lo
GenAI-5.1.1 (K1) Recall the risks of shadow AI
GenAI-5.1.2 (K2) Explain the key aspects to consider when defining a Generative AI strategy for software testing
GenAI-5.1.3 (K2) Summarize key criteria for selecting LLMs/SLMs for software test tasks in a given context
HO-5.1.3 (H1) Estimate the recurring costs of using Generative AI for a given test task
GenAI-5.1.4 (K1) Recall key phases in the adoption of Generative AI in a test organization
:::

Pořadí: nejdřív strategie, podle ní roadmapa, pak sledování postupu. Strategie podle úvodu oddílu zvažuje cíle testování, vhodný výběr LLM, problémy se vstupními daty pro prompty a soulad s AI normami a předpisy. Kdo začne nástrojem a strategii dopisuje zpětně, obvykle skončí u stínové AI.

### 5.1.1 Rizika stínové AI

:::pojem term="shadow AI"
Používání nástrojů nebo systémů GenAI v organizaci bez formálního schválení nebo dohledu.
:::

Tři rizika (S-C-IP):

1. **Information security and data privacy weaknesses**: osobní nástroje nemusí být dobře zabezpečené, hrozí únik dat.
2. **Compliance and regulatory issues**: neschválený nástroj může porušit normy a předpisy (3.4.1), hrozí právní následky.
3. **Vague intellectual property**: nejasné licence, spory o duševní vlastnictví, zvlášť při zpracování chráněných dat bez oprávnění.

Prevence: strategie a kroky pro integraci a nasazení GenAI, tedy schválená cesta místo zákazu.

:::zkouska
Licence patří k IP, ne k bezpečnosti. Stínová AI nikdy nic nezlepšuje: nevynucuje compliance, nesnižuje spory, neruší potřebu licencí.
:::

### 5.1.2 Klíčové aspekty strategie GenAI v testování

Šest oblastí (Cíl, Model, Data, Lidé, Měření, Pravidla):

1. **Měřitelné cíle testování**: vyšší produktivita, kratší testovací cykly, vyšší kvalita.
2. **Výběr LLM**: sladěný s cíli, kompatibilní se stávající testovací infrastrukturou, splňuje škálovatelnost.
3. **Kvalita dat**: přesná a relevantní vstupní data chráněná bezpečnostními postupy.
4. **Školení**: technické i etické dovednosti.
5. **Metriky**: měření účinnosti výsledků GenAI (2.3.1).
6. **Procesní pravidla**: pravidla pro citlivá data, povinnosti transparentnosti (co vzniklo s AI), **quality gates** s revizí vygenerovaného testwaru.

Body na sebe navazují. Cíl určuje model, model potřebuje kvalitní data, s nimi musí umět pracovat lidé, metriky ukazují splnění cíle a pravidla drží vše v mezích předpisů a etiky.

:::zkouska
Špatně je: „co nejvíc dat“, „nejsilnější veřejný model“, „zrušit revize kvůli rychlosti“, „cílem je zavést AI“.
:::

### 5.1.3 Výběr LLM/SLM pro testovací úlohy

Modely se liší funkčními schopnostmi (multimodalita, uvažování), technickými vlastnostmi (kontextové okno) a typem licence (komerční, open source). Benchmarků pro testovací úlohy je málo.

Čtyři kritéria (Výkon, Ladění, Peníze, Pomoc):

1. **Model performance**: výkon na cílových testovacích úlohách proti benchmarkům organizace, metriky z 2.3.1.
2. **Fine-tuning potential**: jde a vyplatí se model doladit na doménových datech?
3. **Recurring cost**: licenční poplatky a provozní náklady, musí se vejít do rozpočtu.
4. **Community and support**: aktivní komunita a podrobná dokumentace.

Organizace může vybrat jeden nebo více modelů. SLM se hodí spíš na úzké, časté úlohy a tam, kde data nesmí opustit vlastní prostředí. LLM spíš na široké a složité úlohy. Rozhoduje měření.

HO-5.1.3: odhad opakovaných nákladů z počtu vstupních a výstupních tokenů, promptů a četnosti úlohy. Porovnat alespoň jeden komerční a jeden open source model.

Výpočet má tři kroky. Spočítat tokeny jednoho volání (vstup a výstup zvlášť). Vynásobit cenou za tokeny a počtem volání za měsíc, s rezervou na opakování. U open source modelu na vlastním serveru místo ceny za tokeny započítat server a čas na správu. Při malém objemu obvykle vyjde levněji komerční služba, při velkém objemu nebo přísných pravidlech pro data se to může otočit.

:::zkouska
Veřejné benchmarky (třeba pro generování kódu) nejsou správné kritérium. Pilot nebo proof of concept není opakovaný náklad, výpočetní výkon a licence ano. „Výkon“ znamená kvalitu výsledků, ne rychlost.
:::

### 5.1.4 Fáze zavedení GenAI v testování

Tři fáze v pořadí (D-I-U):

1. **Discovery**: povědomí a budování schopností. Školení, přístup k LLM/SLM, první experimenty.
2. **Initiation and usage definition**: identifikace a prioritizace případů použití, posouzení infrastruktury s LLM, rozvoj odbornosti, sladění s potřebami organizace.
3. **Utilization and iteration**: plná integrace, průběžný monitoring, měření a řízení transformace, udržitelnost a škálovatelnost.

Fáze mohou běžet souběžně pro různé případy použití. Včas řešit strach ze ztráty práce.

:::zkouska
Názvy jako Pilot, Rollout, Scaling nebo Optimization v sylabu nejsou. Fáze nepatří celé organizaci najednou, ale konkrétnímu případu použití.
:::

## 5.2 Řízení změny při zavádění GenAI v testování

:::lo
GenAI-5.2.1 (K2) Explain the essential skills and knowledge areas required for testers to work effectively with generative AI in test processes
GenAI-5.2.2 (K1) Recall strategies for cultivating AI skills within test teams to support the adoption of Generative AI in test activities
GenAI-5.2.3 (K1) Recognize how test processes and responsibilities shift within a test organization when adopting Generative AI
:::

Řízení změny má dvě stránky: budování dovedností a vývoj rolí. Technickou i organizační. Oddíly jdou od jednotlivce přes tým k organizaci: 5.2.1 co umí tester, 5.2.2 jak to naučit tým, 5.2.3 jak se mění role a procesy.

### 5.2.1 Dovednosti a znalosti pro testování s GenAI

1. **Technické AI dovednosti**: prompt engineering, kontextové okno, metody revize testů.
2. **Doménová a testovací odbornost spojená s AI**: generování testovacích případů, analýza reportů o defektech, generování testovacích dat.
3. **Kompetence**: posouzení schopností LLM, zpřesňování promptů, hodnocení testwaru od AI.
4. **Rizika a ochrana dat**: znalost rizik a jejich zmírnění, dopady sdílení testwaru s LLM, **data sanitization**, prompty šetrné k soukromí.
5. **Environmentální hledisko**: modely přiměřené velikosti, méně výpočetní zátěže, rovnováha přínosu s náklady a energií.

:::zkouska
Špatně je: „zabránit halucinacím“ (lze jen zmírnit), „zajistit kvalitu trénovacích dat modelu“ (práce dodavatele), obecné testovací dovednosti bez vazby na AI.
:::

### 5.2.2 Budování schopností GenAI v testovacích týmech

Princip: **hands-on approach**. Prvky (Hands-on, Paths, Peers, Patterns, Communities):

- praxe s různými LLM/SLM,
- strukturované vzdělávací cesty,
- postupné budování know-how sdílením v organizaci,
- řízená cvičení a peer learning,
- postupné zapojení AI do každodenních úloh,
- posun od základních promptů k promptům specifickým pro testování,
- **prompt pattern**: znovupoužitelná šablona pro konzistentní a spolehlivé výstupy,
- interní **communities of practice**: pravidelná setkání, úspěchy, potíže, osvědčené postupy, knihovny vzorů promptů, poučení napříč projekty.

:::zkouska
Špatně je: jen teorie, vše najednou, experimenty bez struktury, jen externí experti, certifikace na jeden model.
:::

### 5.2.3 Vývoj testovacích procesů v organizaci podporované AI

**Tester**: ze specialisty na návrh a provádění testů na **AI-assisted test specialist**. Nové úlohy (tři R): revize celkového AI výstupu, zpřesňování promptů, údržba knihoven promptů pro testování.

**Test manažer**: AI-based test strategy, AI-based risk management, monitoring a řízení AI procesů. Zaměření: rovnováha lidí a AI, AI governance frameworks pro případy použití, tradiční kompetence plus **AI literacy**, koordinace GenAI testovacích agentů v hybridním týmu.

| | Tester | Test manažer |
|---|---|---|
| Kam se role posouvá | specialista na testování s podporou AI | vedoucí hybridního týmu lidí a AI agentů |
| Nové úlohy | revize AI výstupu, zpřesňování promptů, knihovny promptů | strategie s AI, rizika AI, monitoring a řízení AI procesů |

Žádná role nezaniká, obě se rozšiřují. Tester dál potřebuje testovací techniky, jinak nepozná špatný AI výstup. Test manažer dál řídí testování, jen do něj přibyla AI.

:::zkouska
Monitoring AI procesů a governance patří test manažerovi, ne testerovi. Odpovědi „spoléhat jen na AI“, „AI nahradí manažera“ nebo „manažer studuje vnitřní fungování modelů“ jsou špatně.
:::
