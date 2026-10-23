---
kapitola: 3
varianta: zkracena
nadpis: Řízení rizik generativní AI v testování softwaru
podtitul: Co je nutné ke zkoušce: tři vady výstupu LLM, nedeterminismus, ochrana dat a útoky, energie a předpisy.
---

Kapitola 3 dává ve zkoušce 10 otázek za 11 bodů. Jedna otázka je K3 za 2 body: poznat v ukázce výstupu, o jakou vadu jde. Dvě otázky jsou k útokům z oddílu 3.2.2. Klíčová slova: **security** (bezpečnost), **vulnerability** (zranitelnost), **data privacy** (ochrana dat a soukromí), **hallucination** (halucinace), **temperature** (teplota), **reasoning error** (chyba v uvažování), **bias** (zkreslení), **context manipulation** (manipulace s kontextem).

## 3.1 Halucinace, chyby v uvažování a zkreslení

:::lo
GenAI-3.1.1 (K1) Recall the definitions of hallucinations, reasoning errors and biases in Generative AI systems
GenAI-3.1.2 (K3) Identify hallucinations, reasoning errors and biases in LLM output
GenAI-3.1.3 (K2) Summarize mitigation techniques for GenAI hallucinations, reasoning errors and biases in software test tasks
GenAI-3.1.4 (K1) Recall mitigation techniques for non-deterministic behavior of LLMs
:::

LLM vytváří statisticky věrohodný text. Věrohodný neznamená správný. Vady ve výstupu vedou k vadnému testwaru. Kvůli nedeterministickému chování se opravená vada může v další konverzaci vrátit.

### 3.1.1 Tři druhy vad

**Hallucination** (halucinace): výstup je fakticky nesprávný nebo nesouvisí s úlohou. V testování: smyšlené nebo nerelevantní testovací případy, nefunkční skripty, testy na akceptační kritéria, která v zadání nejsou.

**Reasoning error** (chyba v uvažování): model špatně vyloží logickou strukturu, tedy příčinu a následek, podmínku nebo postup po krocích, a dojde k chybnému závěru. LLM nemá skutečné logické uvažování, spoléhá na rozpoznávání vzorů. Typicky při plánování testování a prioritizaci testovacích případů.

**Bias** (zkreslení): pochází z trénovacích dat. Výstup systematicky upřednostňuje určité informace, postupy nebo předpoklady. Příklad: model trénovaný hlavně na angličtině upozaďuje jiné pohledy. V testování při generování testovacích dat a zpřesňování akceptačních kritérií.

Příčiny všech tří: povaha trénovacích dat a vnitřní omezení architektury transformer.

Halucinace je jednorázový výmysl, chyba v uvažování jednorázové selhání logiky. Zkreslení se opakuje a pozná se až z více výstupů nebo z celku. Vada, kterou model vytvoří kvůli limitu tokenů nebo kontextového okna, do žádné ze tří kategorií nepatří.

:::zkouska
Model něco přidal, co ve vstupu není? Halucinace. Fakta sedí, ale závěr z nich neplyne? Chyba v uvažování. Výstup je systematicky jednostranný? Zkreslení.
:::

### 3.1.2 Jak vady poznat

Halucinace: **cross-verification** (křížové ověření s dokumentací, požadavky a známým chováním systému), **domain expertise consultation** (konzultace s doménovým expertem), **consistency checks** (kontroly konzistence mezi výstupy a se známými fakty).

Chyby v uvažování: **logical validation** (logická validace toku úvahy v revizních cyklech) a **output testing** (spuštění vygenerovaných testů nebo skriptů proti testovanému objektu).

Zkreslení: revize, zda testware, například testovací kód nebo syntetická data, odpovídá testovací strategii a požadavkům na pokrytí. Kontrola zastoupení typů testů, typicky chybějící nefunkční testy.

Provádí se revizí nebo kombinací revize a automatizace. Hloubka kontroly odpovídá odhadnutému riziku úlohy. U platebních transakcí ověřujete každý výstup a spouštíte všechny skripty. U interního konceptu stačí rychlé přečtení.

Postup na ukázku výstupu: nejdřív hledejte prvky bez opory ve vstupu (halucinace). Pak přepočítejte závěry z údajů, které výstup sám uvádí (chyba v uvažování). Nakonec posuďte vyváženost celku vůči strategii a pokrytí (zkreslení).

```text
Zadání: AC1 částka 1–500 000 Kč, AC2 formát účtu, AC3 potvrzení kódem.
Výstup: "TC-06 Po odeslání přijde klientovi potvrzovací SMS (AC4)."
→ halucinace: AC4 v zadání není (odhalí křížové ověření)

Zadání: riziko = P × D, řadit sestupně.
Výstup: rizika 15, 8, 10, 12, 3 s prioritami 1, 3, 2, 4, 5
→ chyba v uvažování: čísla jsou správně, pořadí ne (odhalí logická validace)

Zadání: 20 testovacích klientů pro českou pojišťovnu.
Výstup: všichni John, Emily, Michael, +1 555…, datum MM/DD/RRRR
→ zkreslení: systematický sklon k anglickým vzorům (odhalí revize proti strategii)
```

:::zkouska
K3 otázka dává zadání a výstup. Porovnejte výstup se vstupem řádek po řádku. Hledejte prvek, který ve vstupu nemá oporu. Distraktory jsou obvykle prvky, které v zadání výslovně jsou.
:::

### 3.1.3 Jak vadám předcházet

Vady přicházejí hlavně při špatně navrženém promptu a chybějícím kontextu. Pět technik:

1. **Provide complete context**: všechny relevantní informace v promptu (oddíl 2.1.1).
2. **Divide prompts into manageable segments**: prompt chaining, ověření každého kroku před dalším (2.1.2). Chyby v uvažování se chytí brzy.
3. **Use clear, interpretable data formats**: strukturované, jednoznačné formáty.
4. **Select the appropriate GenAI model**: model vhodný pro úlohu (5.1.3).
5. **Compare results across models**: stejný prompt více modelům, porovnat výstupy.

Doplňkově kapitola 4: RAG a fine-tuning.

Úplný kontext míří hlavně na halucinace, protože model nemusí domýšlet. Rozdělení na kroky míří hlavně na chyby v uvažování, protože se chyba zachytí v mezivýsledku. Porovnání modelů ukáže nespolehlivá místa u všech tří vad. Toto přiřazení je pomůcka, sylabus ho výslovně nedělá.

:::zkouska
Jasný a strukturovaný formát snižuje nedorozumění. Nezvyšuje kreativitu a nemá vliv na náročnost fine-tuningu.
:::

### 3.1.4 Nedeterministické chování

Stejný vstup, různé výstupy. Příčina: pravděpodobnostní výběr tokenů při inferenci. Riziko roste s délkou výstupu. Úplnou reprodukovatelnost zaručit nelze.

Opatření:

- **Temperature** (teplota): snížení zúží rozdělení pravděpodobností, výstup je konzistentnější. Cena: méně kreativity a rozmanitosti.
- **Random seed** (semínko): některé implementace ho umožní nastavit. Stejná pseudonáhodná posloupnost zlepší opakovatelnost.
- Automatizovat část ověřování výstupu, aby hodnocení bylo strukturované a konzistentní.

V praxi: výstup ve strukturovaném formátu (JSON se schématem), validátor a kontrolní skripty, které běží pokaždé stejně. Nedeterminismus se dá změřit: stejný prompt pětkrát, výstupy porovnat, pak snížit teplotu a měření zopakovat.

:::zkouska
Rozdělení pravděpodobností zužuje jen nižší teplota. Semínko zlepšuje opakovatelnost, ale rozdělení nezužuje a na jeho hodnotě nezáleží. Learning rate je parametr tréninku, s variabilitou při inferenci nesouvisí.
:::

## 3.2 Rizika pro ochranu dat a bezpečnost při použití generativní AI v testování

:::lo
GenAI-3.2.1 (K2) Explain key data privacy and security risks associated with using generative AI in software testing
GenAI-3.2.2 (K2) Give examples of data privacy and vulnerabilities in using Generative AI in software testing
GenAI-3.2.3 (K2) Summarize mitigation strategies to protect data privacy and enhance security in Generative AI for software testing
:::

**Data privacy**: ochrana osobních a citlivých údajů před nežádoucím prozrazením. **Security**: ochrana dat a zdrojů před neoprávněným přístupem při zachování přístupu oprávněných. **Vulnerability**: slabina, kterou lze zneužít k útoku.

### 3.2.1 Rizika

Ochrana dat (i bez útočníka):

- **Unintentional data exposure**: výstup nechtěně odhalí citlivou informaci.
- **Lack of control over data usage**: nástroj data ukládá a zpracovává bez souhlasu nebo kontroly uživatele.
- **Compliance risks**: nesoulad s předpisy, jako je GDPR (nařízení (EU) 2016/679), vede k právním sporům.

Bezpečnost (počítá s útočníkem):

- Testovací infrastruktura s LLM je zranitelná vůči únikům dat a neoprávněnému přístupu.
- Útočníci zneužijí zranitelnosti LLM manipulativními útoky a mění chování modelu nebo získávají data.
- Útočníci vnášejí škodlivá vstupní data, aby model zmátli.

Příklad: tester vloží produkční log se jmény klientů do veřejného chatbota. Data opustí firmu (ztráta kontroly), pro zpracování chybí právní základ (nesoulad s GDPR) a jména se mohou objevit ve vygenerovaných testech (neúmyslné vyzrazení). Klientská data proto patří jen do schváleného nástroje, a i tam jen v nezbytném rozsahu.

:::zkouska
Hlavní riziko pro ochranu dat: citlivé informace v promptu budou vyzrazeny nebo zpracovány bez kontroly. Halucinace v syntetických datech nejsou vyzrazení skutečných dat.
:::

### 3.2.2 Útoky na generativní AI v testování

| Vektor | Podstata | Příklad ze sylabu |
|---|---|---|
| **context manipulation** | požadavky, které mají z modelu vytáhnout důvěrná trénovací data | překročení kontextového okna dlouhými prompty, model vypustí útržky trénovacích dat |
| **request manipulation** | vložení dat, která naruší výstup | obrázek zavede model do jiného kontextu, model halucinuje akceptační kritéria |
| **data poisoning** | manipulace s trénovacími daty | falešná hodnocení výsledků AI generovaného reportu o testování |
| **malicious code generation** | přimět model generovat zadní vrátka, např. volání externích příkazů | kód otevře komunikační kanál na škodlivou IP adresu |

:::zkouska
Data poisoning míří na to, z čeho se model učí. Ostatní tři vektory probíhají při používání. Ve verzi sylabu 1.0 se context manipulation jmenovala data exfiltration, některé kurzy používají starý název. Prompt injection a jailbreak sylabus v1.1 nejmenuje.
:::

### 3.2.3 Opatření

GDPR generativní AI výslovně nezakazuje. Jeho pojistky ale omezují zpracování, hlavně zákonnost a omezení účelu.

Opatření na ochranu dat:

- **Data minimization**: citlivá data jen tam, kde to zákon dovoluje, a jen nezbytné množství necitlivých dat.
- **Data anonymization and pseudonymization**: maskovat nebo nahradit citlivé údaje neidentifikujícími.
- **Secure data storage and transmission**: šifrování a řízení přístupu.
- **Resources training**: školení a pravidla pro odpovědné použití.

Doplňková opatření:

- **Systematic review of the generated output**: lidské hodnocení je nezbytné.
- **Evaluation by comparison with another LLM**.
- **Choice of a secure, operational environment**: komerční zabezpečená nabídka, zabezpečený cloud, nebo instalace ve vlastní infrastruktuře.
- **Regular security audits and vulnerability assessments**.
- **Staying updated with security best practices**.

Opatření se kombinují. Zapojit bezpečnostní inženýry, právníky, CTO nebo CISO.

Anonymizace vazbu na osobu nevratně ruší. Pseudonymizace nahradí údaj značkou a vazbu lze obnovit z odděleně uložené tabulky. Nejsilnější podobou minimalizace jsou syntetická testovací data vytvořená z datového modelu, bez skutečných záznamů.

:::zkouska
Proti riziku pro ochranu dat hledejte anonymizaci, pseudonymizaci nebo minimalizaci. Porovnání více modelů zlepšuje přesnost, ne ochranu dat. Neomezený přístup nebo vypnuté šifrování jsou zjevně špatně.
:::

## 3.3 Spotřeba energie a dopad generativní AI na životní prostředí

:::lo
GenAI-3.3.1 (K2) Explain the impact of task characteristics and model usage on the energy consumption of Generative AI in software testing
:::

### 3.3.1 Vliv na spotřebu energie a emise CO₂

Trénink i provoz LLM vyžadují velké výpočetní zdroje. Použití zatěžuje zařízení, sítě a datová centra. Spotřeba roste s používáním. Rozhoduje složitost úlohy a potřebné výpočetní zdroje.

Obrázek vygenerovaný výkonným modelem může spotřebovat tolik energie jako úplné nabití telefonu. Text jen malé procento nabití. Přesná data se získávají těžko, ale souhrnný dopad přes miliony uživatelů dává významné emise CO₂. Osvědčený postup: omezit zbytečné interakce s modelem.

Vlastnosti úlohy: druh výstupu (obrázek, video, text), délka vstupu a výstupu v tokenech, složitost. Větší kontextové okno zvyšuje výpočetní náročnost (oddíl 1.1.2). Způsob použití: velikost modelu, četnost volání, opakované běhy a porovnávání více modelů. Opakované běhy a porovnání modelů zlepšují spolehlivost, ale násobí spotřebu.

Praktické cvičení HO-3.3.1 (H1): v simulátoru spočítat energii a emise CO₂ pro zadané testovací úlohy a sledovat vliv vlastností úlohy a způsobu použití modelu.

:::zkouska
Obrázky jsou výrazně náročnější než text. Souhrnný dopad textových úloh zanedbatelný není. Vyhledávání s generativní AI spotřebuje víc než klasické vyhledávání.
:::

## 3.4 Předpisy, standardy a rámce osvědčených postupů pro AI

:::lo
GenAI-3.4.1 (K1) Recall examples of AI regulations, standards and best practice frameworks relevant to Generative AI in software testing
:::

### 3.4.1 Přehled

| Název | Typ | Obsah |
|---|---|---|
| ISO/IEC 42001:2023 | standard | požadavky na systém řízení AI v organizaci; konzistence a spolehlivost |
| ISO/IEC 23053:2022 | standard | rámec pro životní cyklus AI systémů se strojovým učením; bezpečnost, transparentnost, kvalita dat |
| EU AI Act | předpis | právní rámec, dělí AI aplikace podle úrovně rizika; transparentnost, odpovědnost, zmírnění zkreslení |
| NIST AI RMF | rámec (USA) | řízení rizik AI; férovost, transparentnost, bezpečnost; prevence zkreslených výsledků testů |

K tomu GDPR z oddílu 3.2. Organizace mají sledovat vývoj předpisů, standardů, národních zákonů a rámců.

Předpis (regulation) je právně závazný. Standard je dobrovolný, pokud ho nevyžaduje smlouva nebo zákon, a organizace se podle něj může certifikovat. Rámec (framework) je soubor doporučení bez závaznosti.

:::zkouska
ISO/IEC 25010 a ISO/IEC/IEEE 29119 jsou ze sylabu CTFL a generativní AI se netýkají. Jako normy pro AI v sylabu CT-GenAI platí 42001 a 23053.
:::
