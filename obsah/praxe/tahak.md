---
modul: 0
nazev: Tahák nástrojů
podtitul: Všechny nástroje ze sekce Praxe na jedné stránce: k čemu jsou, kdy je nepoužít, kolik stojí a kam tečou data.
cas: 15–20 min
uroven: začátečník
nastroje: ChatGPT, Microsoft Copilot, NotebookLM, GPT4All, Ollama, GitHub Copilot, MCP, Playwright MCP, Claude Code, n8n, ContextQA, OpenAI API, Anthropic API, Behave, Playwright, Jenkins, GitHub Actions
kapitoly: 1, 2, 3, 4, 5
zdroje: Shetty L3–L76; Bruno L6–L83; ceny a podmínky podle stavu 10/2026 (ověřit)
---

## Jak tahák číst

Každá tabulka pokrývá jednu skupinu modulů. Sloupec **Na co se hodí** říká, kde nástroj ušetří nejvíc práce.
Sloupec **Kdy ho nepoužít** je stejně důležitý: popisuje situace, kdy nástroj zdržuje nebo kdy je riskantní.
Ceny jsou orientační podle stavu v říjnu 2026 a mění se často. Před nákupem je vždy ověř na webu výrobce.
Sloupec **Data** popisuje, kam odchází to, co do nástroje vložíš. Tohle je téma kapitoly 3 sylabu.
Poslední sloupec odkazuje na modul, kde nástroj nastavíš krok za krokem.

:::pozor nazev="Firemní a klientská data"
Do cloudového nástroje nevkládej data klientů, interní dokumenty ani kód z firemních projektů,
pokud ho zaměstnavatel výslovně neschválil. Nástroj, který si tester zapne sám bez schválení, je
**shadow AI** (stínová AI, sylabus 5.1.1). Na cvičení používej veřejné demo aplikace a vlastní projekty.
API klíče patří do proměnné prostředí nebo do Windows Credential Manageru, nikdy do kódu ani do repozitáře.
:::

## Nástroje v chatu

Sem patří nástroje, se kterými pracuješ v okně prohlížeče nebo v desktopové aplikaci bez programování.
Sylabus je řadí mezi **AI chatbots** a **LLM-powered testing applications** (oddíl 1.2.2).

| Nástroj | Na co se hodí | Kdy ho nepoužít | Cena (orientačně, ověřit) | Data | Modul |
|---|---|---|---|---|---|
| ChatGPT, Microsoft Copilot (chat) | Testovací podmínky a případy z textu požadavku, testovací data, revize testů, vysvětlení chybové hlášky. | Když potřebuješ opakovatelný výsledek ve stejném formátu. Když vstup obsahuje citlivá data. | Základní verze zdarma, ChatGPT Plus kolem 20 USD měsíčně. Copilot Chat s pracovním účtem bývá součástí firemní licence. | Text odchází do cloudu výrobce. U osobních účtů se konverzace může použít k tréninku, dokud to v nastavení nevypneš. Pracovní účet s ochranou dat se k tréninku nepoužívá. | [Prompty pro testování v chatu](modul:chatgpt) |
| NotebookLM | Otázky nad nahranými dokumenty: specifikace, uživatelské příručky, sylabus. Odpověď cituje zdroj. | Když dokument není veřejný. Když potřebuješ výstup zpracovat dál strojově. | Zdarma s účtem Google, vyšší limity v placeném tarifu. | Dokumenty jsou uložené v cloudu Google. Podle Google se u osobních účtů k tréninku nepoužívají (ověřit v podmínkách). | [NotebookLM nad dokumenty](modul:notebooklm) |
| GPT4All | Offline chat na vlastním počítači, funkce LocalDocs pro dotazy nad složkou dokumentů. | Na slabém notebooku bez dost paměti. Když potřebuješ kvalitu velkých cloudových modelů. | Zdarma, open source. Platíš výkonem počítače. | Zůstávají na počítači. Volitelné sdílení anonymních dat vývojářům nech vypnuté. | [Lokální modely](modul:gpt4all) |
| Ollama | Lokální model jako služba na `localhost`. Volá se z Pythonu stejně jako cloudové API. | Když tým nemá stroj s dost pamětí. Když model nestačí na delší kontext. | Zdarma, open source. | Lokální modely běží jen na počítači. Pozor na cloudové modely, pokud je Ollama nabízí: ty už data posílají ven. | [Lokální modely](modul:ollama) |
| ContextQA a další testovací nástroje postavené na LLM | Testovací případy z nahraných požadavků, převod manuálního testu na automatizovaný, záznam kroků v prohlížeči. | Bez smlouvy o zpracování dat pro firemní použití. Když potřebuješ mít testy jako kód ve vlastním repozitáři. | Komerční platforma, na vyzkoušení zkušební kredity (ověřit). | Požadavky i adresa testované aplikace jdou do cloudu dodavatele. | [Testovací nástroje postavené na LLM](modul:contextqa) |

Chat je nejrychlejší start. Jakmile ale stejný prompt pouštíš podesáté, vyplatí se ho přenést do Pythonu a volat přes API.

## AI v IDE a agenti

Tyto nástroje pracují přímo nad repozitářem. Čtou soubory, navrhují změny a umí spouštět příkazy.
Sylabus je popisuje jako **LLM-powered agents** (agenti postavení na LLM, oddíl 4.1.3).

| Nástroj | Na co se hodí | Kdy ho nepoužít | Cena (orientačně, ověřit) | Data | Modul |
|---|---|---|---|---|---|
| GitHub Copilot v IDE (VS Code, IntelliJ, PyCharm) | Doplňování kódu testů, režimy Ask, Agent a Plan, vysvětlení cizího kódu, refaktoring step definitions. | Když nerozumíš výsledku a nedokážeš ho zkontrolovat. Na kód, který firma nesmí posílat do cloudu. | Free plán s měsíčním limitem, Pro kolem 10 USD měsíčně, firemní plány dražší. | Kód z otevřených souborů a prompt jdou do cloudu GitHubu. Firemní plány se k tréninku nepoužívají, u osobních je volba v nastavení. | [GitHub Copilot v IDE](modul:github-copilot) |
| Copilot custom agents a cloud agent | Opakovaný úkol popsaný v souboru `.agent.md` (třeba tvorba scénářů z doménového dokumentu). Cloud agent pracuje na úkolu sám a výsledek pošle jako pull request. | Bez revize pull requestu. Na repozitáři, kde agent může zasáhnout do produkčního kódu. | Cloud agent vyžaduje placený plán Copilot (ověřit). | Agent běží v cloudovém prostředí GitHubu nad kopií repozitáře a má právo zapisovat do větve. | [Copilot agenti](modul:github-copilot) |
| MCP a Playwright MCP | **Model Context Protocol** připojí k LLM nástroje: prohlížeč, databázi, soubory, API. Playwright MCP ovládá prohlížeč a z průzkumu stránky navrhne test. | Když MCP server pochází z neověřeného zdroje. Na databázi s reálnými daty. | Protokol i Playwright MCP jsou zdarma. Platí se model, který servery používá. | MCP server běží s tvými právy. Co server přečte (stránku, tabulku, soubor), odchází do modelu. | [MCP a Playwright MCP](modul:mcp) |
| Claude Code a skills | Agent v terminálu nad celým projektem: testovací scénáře z doménových dokumentů, testy v Playwright, spuštění a oprava padajících testů, report pokrytí. Skills uloží know-how do souborů. | Bez kontroly příkazů, které agent spouští. Na velkém úkolu bez rozdělení na menší kroky. | Předplatné Claude Pro nebo Max (Pro kolem 20 USD měsíčně), nebo platba za tokeny přes API. | Obsah souborů, které agent čte, jde do cloudu Anthropic. U komerčních účtů a API se k tréninku nepoužívá, u osobních je volba v nastavení (ověřit). | [Claude Code pro QA](modul:claude-code) |
| n8n | Workflow mezi systémy bez programování: tabulka s defekty, Jira, e-mail, AI agent jako jeden uzel, webhook s chatem. | Na logiku, kterou je lepší mít v kódu a testovat. Když nikdo workflow nebude udržovat. | Community verze pro vlastní server zdarma, cloud placený se zkušební dobou 14 dní. | U vlastního serveru zůstávají data u tebe, uzel s LLM je ale posílá poskytovateli modelu. Cloud běží na serverech n8n. | [Agenti v n8n](modul:n8n) |

Agent ušetří nejvíc času u úkolů s jasným cílem a ověřitelným výsledkem, třeba „všechny testy projdou“.
U nejasného zadání spotřebuje hodně tokenů a výsledek je potřeba stejně přepsat.

## Automatizace v Pythonu

Tady LLM voláš z vlastního kódu. Výstup je opakovatelný, dá se měřit a dá se spustit bez člověka.

| Nástroj | Na co se hodí | Kdy ho nepoužít | Cena (orientačně, ověřit) | Data | Modul |
|---|---|---|---|---|---|
| OpenAI API a Anthropic API z Pythonu | Generování scénářů v Gherkin, řetězení promptů, hodnocení výstupů, analýza step definitions. Stejný prompt pokaždé se stejnými parametry. | Na jednorázový dotaz, ten je rychlejší v chatu. Bez limitu útraty na účtu. | Platba za tokeny. Cvičení z kurzů vyjdou na jednotky dolarů. Nastav si měsíční limit. | Data jdou do cloudu poskytovatele. Podle podmínek API se k tréninku standardně nepoužívají, krátce se uchovávají kvůli kontrole zneužití (ověřit). | [LLM z Pythonu přes API](modul:openai) |
| Behave a Playwright pro Python | BDD framework: scénáře v Gherkin, step definitions v Pythonu, Playwright ovládá prohlížeč, API testy přes `requests`. Report v Allure. | Na jednoduchý test bez potřeby čitelných scénářů, tam stačí pytest. | Zdarma, open source. | Běží lokálně. Ven jde jen to, co pošleš do LLM. | [Behave a Playwright](modul:behave) |

:::pozor nazev="API klíč"
Kurz Gianni Bruno ukládá klíč do souboru `openai-key.json` v projektu. Takový soubor snadno skončí v gitu.
Bezpečnější je proměnná prostředí `OPENAI_API_KEY` nebo `ANTHROPIC_API_KEY`, nastavená mimo repozitář.
V CI patří klíč do správce tajemství (Jenkins Credentials, GitHub Actions secrets).
:::

## CI/CD

Testy a evaluace promptů mají běžet samy po každé změně. Bez toho se zhoršení výstupu modelu pozná pozdě.

| Nástroj | Na co se hodí | Kdy ho nepoužít | Cena (orientačně, ověřit) | Data | Modul |
|---|---|---|---|---|---|
| Jenkins | CI na vlastním serveru: spouštění testů podle tagů, Allure report, plánované běhy. Běžný ve firmách s vlastní infrastrukturou. | Na osobní projekt na GitHubu, tam je jednodušší GitHub Actions. | Zdarma, open source. Platíš server a jeho údržbu. | Zůstávají na serveru. Tajemství patří do Jenkins Credentials. Pozor na prompty a odpovědi v logu. | [Jenkins](modul:jenkins) |
| GitHub Actions | CI přímo v repozitáři: testy při každém push, evaluace promptů, publikace reportu. Agent workflow umí napsat podle zadání. | Když firma nepovoluje kód na GitHubu. Na dlouhé běhy v soukromém repozitáři bez kontroly minut. | U veřejných repozitářů zdarma, u soukromých měsíční limit minut zdarma. | Běží na serverech GitHubu. Tajemství v Actions secrets, v logu se maskují. Logy veřejného repozitáře vidí každý. | [GitHub Actions](modul:github-actions) |

## Jak vybrat nástroj

Začni otázkou, jaká data do nástroje půjdou. Citlivá data patří jen do nástroje schváleného zaměstnavatelem,
nebo do lokálního modelu (GPT4All, Ollama). Teprve potom řeš pohodlí a cenu.

Pro jednorázový úkol, třeba návrh testů z jedné uživatelské story, stačí chat.
Pro otázky nad několika dokumenty se hodí NotebookLM, pokud jsou dokumenty veřejné, jinak LocalDocs v GPT4All.
Když pracuješ v repozitáři s testy, použij GitHub Copilot nebo Claude Code. Agent má smysl u úkolu,
jehož výsledek jde ověřit spuštěním.

Opakovaný proces, který má běžet bez člověka, patří do Pythonu s voláním API a do CI.
Proces, který spojuje víc systémů (tabulka, Jira, e-mail), je rychlejší postavit v n8n.

## Souvislost se sylabem CT-GenAI

Chatboti a testovací aplikace postavené na LLM jsou v [oddílu 1.2.2](../kapitola-1/vyklad.html#oddil-1-2-2).
Rizika ve sloupci Data rozebírá [kapitola 3](../kapitola-3/vyklad.html#oddil-3-2), hlavně ochranu dat a únik dat.
Agenti, MCP a RAG nad dokumenty (NotebookLM, LocalDocs) patří do [oddílu 4.1](../kapitola-4/vyklad.html#oddil-4-1).
Výběr modelu a riziko stínové AI popisuje [oddíl 5.1](../kapitola-5/vyklad.html#oddil-5-1).
