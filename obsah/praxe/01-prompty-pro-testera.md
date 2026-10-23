---
modul: 1
nazev: Prompty pro testera v chatu
podtitul: Z dokumentu s požadavky vytvoříš v běžném AI chatu testovací případy, testovací plán, rozdělení testů do pyramidy a kombinace testovacích dat a výsledek zkontroluješ.
cas: 3–4 h
uroven: začátečník
nastroje: ChatGPT, Microsoft Copilot, Google Gemini nebo NotebookLM, webový prohlížeč, Python 3 (jen krok 10)
kapitoly: 1, 2, 3
zdroje: Shetty L3–L12; Bruno L4–L10 (prompty L08, L09, L13, dokument L10)
---

Tento modul nepotřebuje žádné programování. Pracuješ v okně AI chatu a v prohlížeči. Cílem je naučit se psát prompty, které vrátí použitelný testware napoprvé nebo napodruhé, a naučit se ten testware kontrolovat. Obě lekce, ze kterých modul vychází, dělají totéž. Shetty pracuje s Gemini nad e-shopem, Bruno s ChatGPT nad dvěma stránkami webu WebDriver University. Tady je obojí spojené do jednoho postupu na veřejné demo aplikaci.

Prompty jsou v modulu anglicky i česky. Modely fungují v obou jazycích. Anglická verze se hodí, když výstup půjde do anglické dokumentace nebo do automatizace, česká verze, když s výstupem pracuje český tým.

## Co postavíš

Na konci modulu budeš mít v jednom textovém souboru vlastní malou knihovnu promptů (prompt library) a k ní výstupy pro stránku Contact Us na webu webdriveruniversity.com:

- sadu testovacích případů z dokumentu s požadavky, ve formátu tabulky, který si určíš,
- zkrácený testovací plán pro malý projekt s danými omezeními (lidé, dny, prohlížeče),
- přiřazení testovacích případů k vrstvám testovací pyramidy (shift left),
- tabulku kombinací testovacích dat pro validaci e-mailu, uloženou jako CSV,
- seznam nálezů z kontroly výstupu: co si model vymyslel, co chybí, co je duplicitní.

Knihovnu promptů pak můžeš použít v práci. Stačí v ní vyměnit popis systému a podklady.

## Předpoklady

Stačí jeden z těchto nástrojů. Stav k 23. 10. 2026, podmínky se často mění, ověřit:

| Nástroj | Bez přihlášení | Nahrání souboru | Poznámka |
|---|---|---|---|
| ChatGPT (chatgpt.com) | omezeně | podle tarifu, ověřit | Bruno v kurzu uvádí, že free verze tehdy nahrávání neuměla. Dnes to bývá jinak, ověřit. |
| Microsoft Copilot (copilot.microsoft.com) | ano | po přihlášení, ověřit | Firemní varianta M365 Copilot má jiné podmínky než spotřebitelská. |
| Google Gemini | ne | ano, ověřit | Shetty ho v kurzu používá, umí export do Google Sheets. |
| NotebookLM (notebooklm.google) | ne | ano, je na to stavěný | Odpovídá jen z nahraných zdrojů a odkazuje na ně. |

Tabulka ukazuje hlavně to, že na výběru nástroje pro tento modul skoro nezáleží. Postup a principy jsou stejné.

Dál budeš potřebovat:

- prohlížeč se stránkami https://webdriveruniversity.com/Contact-Us/contactus.html a https://webdriveruniversity.com/Login-Portal/index.html,
- dokument s požadavky na Contact Us. Bruno ho má v kurzu jako přílohu lekce L10. Pokud ho nemáš, napiš si podle kroku 1 vlastní, stačí půl strany,
- textový editor na knihovnu promptů (stačí `prompty.md` v libovolné složce),
- pro krok 10 Python 3 s knihovnou `pytest`.

:::pozor
Do veřejného AI chatu nevkládej nic z práce: žádné požadavky klienta, kód, logy, jména, čísla účtů ani přihlašovací údaje. Patří to i k pravidlům firmy. Celý modul proto běží na veřejné demo stránce. Když chceš to samé dělat nad pracovním zadáním, použij jen nástroj, který schválilo IT, a pracovní účet. Kapitola 3, oddíl 3.2 vysvětluje proč.
:::

## Postup

### Krok 1: Poznej testovanou stránku dřív, než se zeptáš modelu

Otevři stránku Contact Us a vyzkoušej ji ručně. Bruno na tom v lekci L6 trvá a má pravdu. Model stránku nevidí. Když mu dáš jen URL, nebude znát pole, hlášky ani chování a doplní je odhadem.

Vyzkoušej aspoň tyto situace a zapiš si, co se stalo:

1. Vyplň všechna čtyři pole, e-mail ve tvaru `test@example.com`, a klikni na SUBMIT.
2. Vyplň vše, ale v e-mailu vynech zavináč.
3. Nech prázdné Last Name a Email Address.
4. Vyplň pole a klikni na RESET.

Výsledek si zapiš do knihovny promptů jako krátký popis chování. Podle kurzu se zobrazí hlášky „Thank You for your Message!“, „Error: Invalid email address“ a „Error: all fields are required“. Přesné znění a velká písmena si ověř na stránce, mohly se změnit. Všimni si i toho, jak se chyba zobrazí. Podle kurzu nejde o hlášku pod polem, ale o samostatnou stránku s textem. Právě to model z URL nikdy neodhadne.

Stejně si projdi Login Portal. Podle kurzu (L7) stránka přijímá jediný pár údajů a výsledek ukáže v JavaScript alertu s textem „validation succeeded“ nebo „validation failed“. Ověřit na stránce.

Co má vyjít: krátký seznam pozorovaného chování obou stránek. Z něj v dalších krocích vyrobíš kontext do promptu.

### Krok 2: Začni slabým promptem a podívej se, co se pokazí

Otevři nový chat a pošli záměrně slabý prompt. Je to **zero-shot prompting**: model nedostane žádný příklad a skoro žádný kontext.

```text
Generate test cases for the Contact Us page at https://webdriveruniversity.com/Contact-Us/contactus.html.
```

```text
Vytvoř testovací případy pro stránku Contact Us na https://webdriveruniversity.com/Contact-Us/contactus.html.
```

Co má vyjít: dlouhý seznam obecných testů. Obvykle tam najdeš testy, které s touto stránkou nesouvisí, a hlášky, které stránka nemá. Typicky „Error message is displayed indicating the First Name field is required“. Bruno na tom v L6 ukazuje, že model takovou hlášku vymyslel, protože stránku neviděl. Některé chatboty dnes umí stránku stáhnout přes vyhledávání. I tak nevidí, jak se stránka chová po kliknutí, takže výsledek stejně neodpovídá skutečnosti.

Zeptej se modelu přímo:

```text
Can you access the HTML and JavaScript of a web page if I only give you its URL? Answer in two sentences.
```

Odpověď se bude lišit podle nástroje. Důležité je to, co z ní plyne: test nemůže stát na tom, co si model o stránce domyslel.

Zapiš si do knihovny tři konkrétní chyby, které jsi ve výstupu našel. V kroku 11 je budeš porovnávat s lepší verzí.

:::pozor
Bruno v L6 ukazuje i vložení celého zdrojového kódu stránky do chatu a sám hned dodává, že to není dobrý postup. U vlastní demo stránky to nevadí. U pracovní aplikace by šlo o únik zdrojového kódu. Dobrý tester umí systém popsat sám, a to je bezpečnější i přesnější.
:::

### Krok 3: Přepiš prompt podle pravidla 3 C

Shetty v lekcích L3 a L4 shrnuje dobrý prompt do pravidla **3 C**:

- **context** (kontext): kdo model je a o jakou situaci jde,
- **constraints** (omezení): jaká pravidla a hranice platí,
- **clarity** (jasnost výstupu): jak má výsledek vypadat.

Sylabus CT-GenAI v oddílu 2.1.1 popisuje strukturu promptu podrobněji, šesti komponentami. 3 C je zjednodušení stejné myšlenky. Pro zkoušku platí šest komponent, a proto je v knihovně promptů používej jako kontrolní seznam.

| 3 C (Shetty) | Komponenty podle sylabu 2.1.1 |
|---|---|
| Context | Role, Context |
| Constraints | Constraints, částečně Instruction |
| Clarity | Output format |
| (chybí) | Input data |

Tabulka ukazuje, co 3 C nepokrývá: vstupní data. Ty je musíš do promptu dát zvlášť. Tady jsou to tvoje poznámky z kroku 1.

Nový prompt má všechny části. Vychází z Brunova promptu v příloze L09, ale je přestavěný podle komponent sylabu:

```text
Role: You are a test analyst who designs functional test cases for web forms.

Context: I am testing a public demo "Contact Us" page. You cannot see the page,
so rely only on the facts below.

Input data (observed behaviour):
- Fields: First Name, Last Name, Email Address, Comments. All are required.
- Buttons: SUBMIT and RESET. RESET clears all fields.
- Valid submission shows: "Thank You for your Message!"
- Invalid email shows: "Error: Invalid email address"
- Any empty field shows: "Error: all fields are required"
- Errors are shown on a separate page, not under the fields.

Instruction: Design functional test cases for field validation, required fields,
error messages and the RESET button.

Constraints:
- Use only the behaviour listed above. If something is unknown, list it under
  "Open questions" instead of guessing.
- Cover positive and negative cases. Use equivalence partitioning for the email field.
- At most 12 test cases. No performance, security or usability tests.

Output format: A Markdown table with columns ID, Title, Preconditions, Steps,
Test data, Expected result, Priority (High/Medium/Low). Then a short list "Open questions".
```

Česká verze má stejnou stavbu. Stačí přeložit popisky a pokyny, citace hlášek nech v původním znění, protože tak je stránka zobrazuje:

```text
Role: Jsi test analytik, který navrhuje funkční testovací případy pro webové formuláře.

Kontext: Testuji veřejnou demo stránku "Contact Us". Stránku nevidíš, vycházej jen z faktů níže.

Vstupní data (pozorované chování):
- Pole: First Name, Last Name, Email Address, Comments. Všechna jsou povinná.
- Tlačítka SUBMIT a RESET. RESET vymaže všechna pole.
- Platné odeslání zobrazí: "Thank You for your Message!"
- Neplatný e-mail zobrazí: "Error: Invalid email address"
- Prázdné pole zobrazí: "Error: all fields are required"
- Chyba se zobrazí na samostatné stránce, ne pod polem.

Instrukce: Navrhni funkční testovací případy pro validaci polí, povinná pole, chybové hlášky a tlačítko RESET.

Omezení:
- Použij jen chování uvedené výše. Co nevíš, dej do seznamu "Otevřené otázky", nehádej.
- Pokryj pozitivní i negativní případy. U e-mailu použij rozdělení do tříd ekvivalence.
- Nejvýš 12 testovacích případů. Žádné výkonnostní, bezpečnostní ani usability testy.

Formát výstupu: Markdown tabulka se sloupci ID, Název, Předpoklady, Kroky, Testovací data,
Očekávaný výsledek, Priorita (High/Medium/Low). Pod ní krátký seznam "Otevřené otázky".
```

Co má vyjít: tabulka s nejvýš dvanácti řádky. Očekávané výsledky citují skutečné hlášky. Vymyšlené hlášky typu „First Name is required“ zmizí. V otevřených otázkách se objeví věci, které model neví, třeba maximální délka komentáře nebo jestli se po odeslání vymaže formulář. Tyhle otázky jsou cenné. U skutečného projektu je pošleš analytikovi.

Pokyn „co nevíš, nehádej“ je nejlevnější ochrana proti **hallucination** (halucinace). Neodstraní ji úplně, ale model pak častěji přizná neznalost.

Shetty v L7 a L8 přidává praktický důvod pro přesný prompt: tokeny a **context window** (kontextové okno). Vágní prompt je krátký, ale vede k dlouhé odpovědi a několika doplňujícím dotazům. Každá výměna stojí tokeny a plní kontextové okno. Při dlouhé konverzaci model zapomíná, co bylo na začátku. Přesný prompt bývá ve výsledku levnější i spolehlivější.

### Krok 4: Zužuj výsledek doplňujícími prompty

V tom samém chatu pošli doplňující prompt. Model má předchozí odpověď v kontextu, takže nemusíš nic opakovat:

```text
From the table above, keep only the test cases that must pass before release.
Explain in one sentence per case why it is critical.
```

```text
Z tabulky výše nech jen testovací případy, které musí projít před vydáním.
U každého jednou větou vysvětli, proč je kritický.
```

Co má vyjít: tři až šest případů. Bruno v L6 a L9 dělá totéž pokynem „only critical test cases“. Druhá věta promptu ti dá zdůvodnění, které můžeš porovnat s vlastním úsudkem. Pokud model označí jako kritický test RESET a vynechá platné odeslání, je to chyba v jeho úsudku, ne v tvém.

Shetty v L6 radí doplňující otázky používat, ale nenatahovat. Když potřebuješ víc než tři opravy, je lepší vrátit se ke kroku 3, prompt opravit a spustit v novém chatu.

### Krok 5: Few-shot – ukaž modelu formát, který používáš

Tabulka z kroku 3 má sloupce, které jsi popsal slovy. V práci máš ale obvykle konkrétní šablonu, třeba z Jira Xray nebo TestRailu. Místo popisu ji stačí ukázat. To je **few-shot prompting**: v promptu jsou jeden nebo více vzorů výstupu. Shetty to ukazuje v L5.

Otevři nový chat a pošli tento prompt. Vzor obsahuje jeden testovací případ pro Login Portal. Údaje v něm jsou záměrně vymyšlené, stejně jako v Brunově promptu v L08. Pravé údaje do chatu nepatří ani u demo stránky. Zvykni si na to.

```text
You are a test analyst. Write test cases for a login page in exactly the same format
and level of detail as the example below.

Facts about the page:
- Fields: Username, Password. Button: Login.
- Only one credential pair is valid. Use the placeholder VALID_USER / VALID_PASS.
- Success shows a JavaScript alert "validation succeeded".
- Any failure shows a JavaScript alert "validation failed".

Example:
ID: LOGIN-01
Title: Successful login with valid credentials
Priority: High
Preconditions: Login page is open.
Steps:
1. Enter VALID_USER into Username.
2. Enter VALID_PASS into Password.
3. Click Login.
Expected result: Alert with text "validation succeeded" is displayed.

Now write LOGIN-02 to LOGIN-08. Cover invalid username, invalid password,
empty fields, case sensitivity and leading or trailing spaces.
```

Česky stačí přeložit úvodní pokyn a seznam faktů. Vzor nech tak, jak ho skutečně používáš, jazyk vzoru model obvykle převezme.

Co má vyjít: sedm případů ve stejném tvaru jako vzor, se stejnými popisky a stejnou úrovní detailu. Všimni si, že prompt nemusel popisovat sloupce. Vzor je popsal sám. Ověř, že model u prázdných polí nečeká jinou hlášku než „validation failed“. Pokud ano, nedržel se faktů a je potřeba to v promptu zdůraznit.

Jeden vzor je přesněji **one-shot prompting**. Dva až tři vzory s různými typy případů (pozitivní a negativní) dávají stabilnější výsledek. Sylabus rozdíl popisuje v oddílu 2.1.2.

### Krok 6: Chain of thought – nech model ukázat postup

Třetí technika ze Shettyho L6 je **chain-of-thought prompting** (řetězec úvah). Model požádáš, aby postupoval krok za krokem a postup ukázal. Hodí se tam, kde potřebuješ zkontrolovat úvahu, ne jen výsledek. U testování je to typicky návrh testů z pravidel, která se navzájem ovlivňují.

```text
Let's reason step by step. The email field on a contact form must contain exactly one "@",
a non-empty local part, and a domain with at least one dot. 
1. List the validation rules you derive from this.
2. For each rule, list valid and invalid equivalence partitions.
3. Pick one representative value per partition and add boundary values where relevant.
4. Only then output a table: Value, Partition, Expected (valid/invalid), Rule.
```

```text
Postupuj krok za krokem. Pole e-mail v kontaktním formuláři musí obsahovat právě jeden "@",
neprázdnou část před ním a doménu s aspoň jednou tečkou.
1. Vypiš validační pravidla, která z toho plynou.
2. Ke každému pravidlu vypiš platné a neplatné třídy ekvivalence.
3. Z každé třídy vyber jednu reprezentativní hodnotu a tam, kde to dává smysl, přidej hraniční hodnoty.
4. Teprve potom vypiš tabulku: Hodnota, Třída, Očekávání (platná/neplatná), Pravidlo.
```

Co má vyjít: nejdřív seznam pravidel a tříd, pak tabulka. V mezikrocích uvidíš, kde se model splete. Častá chyba je, že hodnotu `a@b.c` označí za neplatnou, protože ji považuje za „nerealistickou“, přestože pravidlům vyhovuje. Taková chyba v uvažování by se bez mezikroků v tabulce schovala.

Pravidla v promptu jsou tvoje zjednodušení. Skutečná stránka může validovat jinak. Výsledná tabulka proto není orákulo. Říká, co testovat, ale co je správně, ověříš na stránce.

:::nad-ramec
Uvažující modely (reasoning LLM) dnes postupují krok za krokem samy a postup často ukazují v rozbalovacím panelu. Shetty to v L6 předvádí na Gemini a DeepSeek. U nich pokyn „krok za krokem“ výsledek mění méně. Má ale smysl, když chceš mezikroky v přesně daném pořadí, jako v promptu výše. Chain-of-thought sylabus CT-GenAI mezi technikami neuvádí (viz kapitola 2, oddíl 2.1.2).
:::

### Krok 7: Nahraj dokument s požadavky

Zatím jsi popisoval chování stránky sám. Na projektu ale máš obvykle dokument s požadavky. Bruno v L10 ho do chatu nahrává jako soubor.

Než soubor nahraješ, otevři ho a zkontroluj. Bruno to opakuje několikrát: žádná hesla, přístupové klíče, osobní údaje ani interní informace. Jeho dokument má v zápatí poznámku, že jde o testovací dokument. U pracovního dokumentu by kontrola nestačila. Ten do veřejného chatu nepatří vůbec.

V ChatGPT, Copilotu nebo Gemini nahraj soubor přes ikonu sponky a pošli:

```text
Using only the attached requirements document, create functional test cases for the
Contact Us form. Focus on form validation, successful submission and error messages.
For each test case add the requirement section it covers (e.g. "2.3 Error Messages").
If the document is ambiguous or contradicts itself, list the issue under "Requirement issues".
Output: Markdown table ID, Requirement, Title, Steps, Expected result.
```

```text
Vycházej jen z přiloženého dokumentu s požadavky a vytvoř funkční testovací případy pro
formulář Contact Us. Zaměř se na validaci formuláře, úspěšné odeslání a chybové hlášky.
U každého testovacího případu uveď oddíl požadavků, který pokrývá (např. "2.3 Error Messages").
Pokud je dokument nejednoznačný nebo si odporuje, uveď problém v seznamu "Problémy v požadavcích".
Výstup: Markdown tabulka ID, Požadavek, Název, Kroky, Očekávaný výsledek.
```

Co má vyjít: tabulka se sloupcem Požadavek. Tím získáš jednoduchou **traceability** (sledovatelnost) mezi testovací bází a testy. Seznam problémů je druhý užitečný výstup. Brunův dokument má například úspěšnou hlášku dvakrát a pokaždé jinak („Thank you for your message.“ a „Thank You for your Message.“). Formulář se podle jednoho místa má po odeslání vymazat, podle stránky to ověřené nemáš. Pokud model tyhle rozpory nenajde, zeptej se na ně přímo. To je mimochodem analýza požadavků, kterou sylabus uvádí v oddílu 1.2.1.

NotebookLM se chová jinak než běžný chat. Nahraný dokument vloží jako zdroj (source) a odpovídá jen z něj. U každého tvrzení ukáže odkaz na místo ve zdroji. Pro testera je to praktické: tvrzení si ověříš kliknutím. V NotebookLM založ nový notebook, přidej dokument jako zdroj a pošli stejný prompt. Porovnej výsledek s ChatGPT nebo Copilotem. NotebookLM obvykle přidá méně vlastních nápadů a víc se drží textu. Pro hledání chybějících testů, které dokument nezmiňuje, je naopak slabší.

Shetty v L8 přidává pravidlo pro práci s nahranými soubory: dokument nahraj do konverzace jednou a dál se na něj odkazuj („refer to the attached document“). Opakované nahrávání plní kontextové okno a stojí tokeny.

### Krok 8: Testovací plán z požadavků

Shetty v L9 nechá Gemini napsat testovací plán pro e-shop „Style Haven“ z přílohy kurzu `requirements-ai.docx`. Stejný postup zkus na Contact Us, nebo na Shettyho dokumentu, pokud ho máš. Hlavní myšlenka lekce: plán bez omezení je k ničemu. Model si jinak vymyslí tým i termín.

```text
You are a test manager. Based on the attached requirements, write a test plan.

Constraints:
- Team: 2 testers, part-time (50 %).
- Time: 10 working days including regression.
- Environments: Windows 11 and macOS; browsers Chrome and Safari; one mobile viewport.
- Out of scope: load testing.

Structure: Scope (in/out), Test approach per test level, Schedule with effort in person-days,
Entry and exit criteria, Risks with mitigation, Deliverables.
Mark every number that is your assumption with [ASSUMPTION].
```

```text
Jsi test manažer. Podle přiložených požadavků napiš testovací plán.

Omezení:
- Tým: 2 testeři na poloviční úvazek.
- Čas: 10 pracovních dní včetně regrese.
- Prostředí: Windows 11 a macOS, prohlížeče Chrome a Safari, jedno mobilní rozlišení.
- Mimo rozsah: zátěžové testy.

Struktura: Rozsah (co ano, co ne), Přístup k testování podle úrovní testů, Harmonogram s pracností
v člověkodnech, Vstupní a výstupní kritéria, Rizika a jejich zmírnění, Výstupy.
Každé číslo, které je tvůj předpoklad, označ [PŘEDPOKLAD].
```

Co má vyjít: plán v zadané struktuře. Součet člověkodnů v harmonogramu nesmí přesáhnout kapacitu. Dva testeři na poloviční úvazek po deset dní mají dohromady deset člověkodnů. Spočítej to. Model se v součtech plete častěji, než by člověk čekal.

Pozor na jednu věc z kurzu. Shetty v L9 tvrdí, že model odhad pracnosti „porovnal s podobnými projekty z internetu“ a že čísla jsou přesná. To neplatí. Model žádnou databázi projektů neprohledává, čísla odhaduje z obecných vzorců v trénovacích datech. Značka [ASSUMPTION] v promptu ti ukáže, kde přesně odhaduje. Odhady patří k tomu, co musí schválit člověk, který tým zná.

### Krok 9: Strategie shift left – které testy do které vrstvy

Shetty v L11 dává modelu testovací případy z L10 a ptá se, které patří do unit testů, které do integračních (API) a které do end-to-end testů přes UI. Myšlenka je **shift left** (posun testování dopředu): co jde otestovat dřív a levněji, nemá čekat na hotové UI. Shetty ukazuje i chybu v promptu. První verze dotazu vrátí obecný výklad o pyramidě. Teprve když napíše „for the test cases you created above“, dostane přiřazení.

V chatu z kroku 3 nebo 7 pošli:

```text
For each test case in your table above, add a column "Test level" with one of:
Unit, Integration/API, UI end-to-end. Add a column "Reason" with one short sentence.
Rule: choose the lowest level where the behaviour can be verified.
Keep at most 3 cases in UI end-to-end.
```

```text
Ke každému testovacímu případu z tvé tabulky výše přidej sloupec "Úroveň testu" s jednou z hodnot:
Unit, Integrace/API, UI end-to-end. Přidej sloupec "Důvod" s jednou krátkou větou.
Pravidlo: vyber nejnižší úroveň, na které jde chování ověřit.
Do UI end-to-end dej nejvýš 3 případy.
```

Co má vyjít: tabulka rozšířená o dva sloupce. Validace formátu e-mailu by měla skončit v unit testech, odeslání formuláře a zobrazení děkovné hlášky v UI. Pravidlo „nejnižší úroveň“ a limit tří případů v UI jsou omezení, bez kterých model rád dá skoro všechno do UI.

Výsledek ber jako návrh do diskuse s vývojáři. Shetty to v L11 říká správně: neříkej vývojáři „AI říká, že to patří do unit testů“. Musíš umět vysvětlit proč. U Contact Us je navíc háček. Validace je podle požadavků na straně klienta v JavaScriptu. Unit test by pak byl test JavaScriptové funkce, ne backendu. Model to obvykle nerozliší, ty ano.

### Krok 10: Kombinace testovacích dat a jejich kontrola v Pythonu

Shetty v L12 chce po modelu kombinace vstupů a výstupů pro jeden unit test. Bruno v L4 upozorňuje, že testovací data mají být zjevně fiktivní, třeba e-maily na doméně `example.com`. Ta doména je pro dokumentaci a testy rezervovaná, takže nikomu skutečnému nepatří.

Pošli prompt:

```text
Generate test data for the Contact Us form as CSV with header:
case_id,first_name,last_name,email,comments,expected
"expected" is one of: success, invalid_email, all_fields_required.
Rules:
- 15 rows. Every row must differ in at least one partition.
- Use only fictitious data. Emails must use the domain example.com or be deliberately invalid.
- Include: empty values, whitespace-only values, unicode names (e.g. Czech diacritics),
  very long comment (describe it as LONG_2000 instead of writing it out).
Output only the CSV in a code block.
```

```text
Vygeneruj testovací data pro formulář Contact Us jako CSV s hlavičkou:
case_id,first_name,last_name,email,comments,expected
"expected" je jedna z hodnot: success, invalid_email, all_fields_required.
Pravidla:
- 15 řádků. Každý řádek se liší aspoň v jedné třídě ekvivalence.
- Jen fiktivní data. E-maily na doméně example.com nebo záměrně neplatné.
- Zahrň: prázdné hodnoty, hodnoty jen z mezer, jména s diakritikou,
  velmi dlouhý komentář (napiš místo něj LONG_2000, nevypisuj ho).
Vypiš jen CSV v bloku kódu.
```

Ulož výstup jako `contact_data.csv`. Pak data zkontroluj vlastním skriptem. Model se v takových tabulkách plete hlavně v poli `expected`. Řádek s prázdným jménem a neplatným e-mailem může označit jako `invalid_email`, i když stránka podle pozorování z kroku 1 hlásí nejdřív chybějící pole. Skript níže kontroluje strukturu a nejjednodušší pravidlo: prázdné pole znamená `all_fields_required`.

```python
# check_contact_data.py
import csv
from pathlib import Path

import pytest

ROWS = list(csv.DictReader(Path("contact_data.csv").open(encoding="utf-8")))
FIELDS = ["first_name", "last_name", "email", "comments"]
ALLOWED = {"success", "invalid_email", "all_fields_required"}


def test_header_and_count():
    assert ROWS, "CSV je prázdné"
    assert set(ROWS[0]) == {"case_id", *FIELDS, "expected"}
    assert len(ROWS) == 15


def test_unique_ids():
    ids = [r["case_id"] for r in ROWS]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("row", ROWS, ids=lambda r: r["case_id"])
def test_expected_is_consistent(row):
    assert row["expected"] in ALLOWED
    if any(not row[f].strip() for f in FIELDS):
        assert row["expected"] == "all_fields_required"


@pytest.mark.parametrize("row", ROWS, ids=lambda r: r["case_id"])
def test_no_real_looking_emails(row):
    email = row["email"].strip()
    if "@" in email and email.count("@") == 1:
        assert email.lower().endswith("example.com"), f"podezřelá doména: {email}"
```

Spusť ve složce s CSV:

```text
python -m pytest check_contact_data.py -v
```

Co má vyjít: seznam testů, u každého řádku CSV dva. Selhání znamenají, že model porušil vlastní zadání. Typicky nesedí počet řádků nebo pole `expected` u řádku s prázdnou hodnotou. Nesrovnalosti oprav ručně, nebo je pošli modelu zpět s výpisem selhání. Skript je ověřený na ručně vytvořeném vzorovém CSV (Python 3.12, pytest, 10/2026). Na skutečném výstupu modelu neověřeno.

Pravidlo „prázdné pole má přednost před neplatným e-mailem“ je tvůj předpoklad z kroku 1. Ověř ho na stránce. Pokud stránka hlásí jinak, oprav skript, ne data.

### Krok 11: Kontrola a zlepšení výstupu

Oba lektoři opakují totéž: výstup nikdy nepoužívej, jak je. Kontrola ale potřebuje postup, jinak se omezí na to, že tabulka „vypadá dobře“. Projdi výstup z kroku 3 nebo 7 podle tohoto seznamu a nálezy zapiš:

1. **Sledovatelnost.** Má každý testovací případ oporu v požadavku nebo v pozorování? Případ bez opory je buď užitečný nápad navíc, nebo halucinace. Rozhodni, co z toho.
2. **Vymyšlené chování.** Cituje očekávaný výsledek skutečnou hlášku? Hledej hlášky, které stránka nemá.
3. **Pokrytí.** Má každý požadavek aspoň jeden test? Chybí negativní případy?
4. **Duplicity.** Testují dva případy stejnou třídu ekvivalence?
5. **Ověřitelnost.** Dá se očekávaný výsledek jednoznačně vyhodnotit? „Form works correctly“ se vyhodnotit nedá.
6. **Data.** Jsou testovací data fiktivní a odpovídají krokům?

Pak si nech pomoct modelem, ale s jasnou rolí. V novém chatu, bez předchozí historie:

```text
You are a reviewer of test cases. Below are (A) the requirements and (B) test cases written by someone else.
1. List requirements from (A) that have no test case in (B).
2. List test cases in (B) whose expected result is not supported by (A). Quote the unsupported part.
3. List duplicate test cases.
Do not rewrite the test cases. Only report findings.

(A) <vlož požadavky nebo pozorování z kroku 1>
(B) <vlož tabulku testovacích případů>
```

```text
Jsi recenzent testovacích případů. Níže jsou (A) požadavky a (B) testovací případy, které napsal někdo jiný.
1. Vypiš požadavky z (A), ke kterým v (B) není žádný testovací případ.
2. Vypiš testovací případy z (B), jejichž očekávaný výsledek nemá oporu v (A). Citovanou část uveď.
3. Vypiš duplicitní testovací případy.
Testovací případy nepřepisuj. Jen vypiš nálezy.

(A) <vlož požadavky nebo pozorování z kroku 1>
(B) <vlož tabulku testovacích případů>
```

Nový chat je důležitý. V původním chatu model hájí, co sám napsal. Formulace „napsal někdo jiný“ a pokyn „nepřepisuj“ ho drží v roli recenzenta.

Co má vyjít: tři seznamy. Porovnej je se svými nálezy. Co model našel a ty ne, prověř. Co jsi našel ty a model ne, je důkaz, že recenze modelem nenahradí tvou. Nakonec oprav prompt z kroku 3 tak, aby se nalezené chyby neopakovaly, a ulož novou verzi do knihovny s datem. Tohle je iterativní ladění promptu, které sylabus popisuje v oddílu 2.3.2.

## Ověření

Modul máš hotový, když platí:

- Knihovna promptů obsahuje aspoň pět promptů (kroky 3, 5, 6, 7 nebo 8, 11). U každého je datum, nástroj a model, se kterým jsi ho zkoušel, a jedna věta o výsledku.
- Tabulka z kroku 3 nebo 7 neobsahuje žádnou hlášku, kterou stránka nezobrazuje. Ověřil jsi to ručně aspoň u tří testů.
- U každého testovacího případu z kroku 7 je uvedený oddíl požadavků.
- Součet pracnosti v testovacím plánu z kroku 8 nepřesahuje kapacitu z omezení.
- `pytest` z kroku 10 projde, nebo víš, proč neprojde, a máš to zapsané.
- Seznam nálezů z kroku 11 má aspoň tři položky z tvé vlastní kontroly.

Prakticky nejlepší test celého modulu: spusť prompt z kroku 3 ve dvou různých nástrojích, třeba v ChatGPT a Copilotu. Výsledky nebudou stejné, protože modely jsou nedeterministické. Pokud se ale liší v podstatě, třeba v hláškách nebo v počtu povinných polí, prompt ještě nechává moc prostoru pro domýšlení.

## Časté chyby

**Jen URL místo popisu.** Model stránku nevidí, nebo vidí jen statický kód bez chování. Výsledek vypadá profesionálně a je částečně vymyšlený. Popiš chování sám (krok 1 a 3).

**Pravé přihlašovací údaje v promptu.** I u demo stránky. Bruno v L8 nahrazuje skutečné údaje vymyšlenými a vysvětluje, že je to návyk. V práci by šlo o únik.

**Nahrání dokumentu bez kontroly.** Dokument může mít v revizích, komentářích nebo zápatí interní informace. Zkontroluj ho celý. Pracovní dokumenty do veřejného chatu nedávej vůbec.

**Nekonečná konverzace.** Po desítkách výměn model zapomíná začátek a míchá verze tabulek. Shetty v L8 radí raději začít nový chat s opraveným promptem.

**Důvěra v čísla.** Odhady pracnosti, počty testů a součty v plánu jsou odhad, ne výpočet. Přepočítej je.

**Recenze ve stejném chatu.** Když model kontroluje svůj vlastní výstup v téže konverzaci, často jen potvrdí, co napsal. Recenzi dělej v novém chatu a s rolí recenzenta.

**Přebírání tvrzení z kurzu.** Shetty v L10 říká, že tester se psaním testovacích případů už nemusí zabývat. Pro práci v bance to neplatí. Za testovací případy odpovídá tester a musí umět vysvětlit, proč tam jsou.

## Cvičení

:::cviceni nazev="Login Portal od nuly"
Cíl: projít celý postup na druhé stránce bez návodu. Na stránce Login Portal si zapiš chování, napiš strukturovaný prompt se všemi šesti komponentami ze sylabu a nech vytvořit testovací případy. Pravé údaje v promptu nahraď zástupnými hodnotami. Pak výstup zkontroluj podle kroku 11.
Hotovo: tabulka s nejvýš deseti případy, žádná vymyšlená hláška, aspoň jeden test na prázdná pole a jeden na velikost písmen. Seznam nálezů z kontroly má aspoň dvě položky.
:::

:::cviceni nazev="Tři techniky, jedna úloha"
Cíl: porovnat zero-shot, few-shot a chain-of-thought na stejné úloze. Úloha: testovací případy pro pole Comments (povinné, text). Napiš tři prompty, každý jednou technikou, a spusť je v nových chatech stejného nástroje.
Hotovo: tabulka o třech řádcích (technika, počet případů, počet vymyšlených pravidel, tvoje hodnocení použitelnosti 1–5) a dvě věty o tom, kterou techniku bys použil v práci a proč.
:::

:::cviceni nazev="Rozpory v požadavcích"
Cíl: použít AI k analýze požadavků, ne jen ke generování testů. Nahraj Brunův dokument k Contact Us (nebo vlastní půlstránkový dokument) do NotebookLM a do jednoho dalšího chatu. Požádej o seznam nejednoznačností a rozporů s odkazem na místo v dokumentu.
Hotovo: aspoň tři nalezené problémy, u každého citace z dokumentu a jedna otázka, kterou bys poslal analytikovi. Poznámka, který nástroj odkazoval na zdroj přesněji.
:::

## Souvislost se sylabem CT-GenAI

Modul je praktickou podobou kapitoly 2. Struktura promptu v kroku 3 odpovídá šesti komponentám z **kapitoly 2, oddílu 2.1.1**. Pravidlo 3 C ze Shettyho kurzu je jejich zjednodušení a ve zkoušce se neobjeví. Zero-shot a few-shot (kroky 2 a 5) jsou techniky z **oddílu 2.1.2**. Chain-of-thought z kroku 6 sylabus mezi techniky neřadí, zmiňuje ho jen u uvažujících modelů v **kapitole 1, oddílu 1.1.3**.

Kroky 3, 5 a 7 jsou návrh testů podle **oddílu 2.2.2**, krok 7 s hledáním rozporů zároveň testovací analýza podle **oddílu 2.2.1**. Testovací plán v kroku 8 a rozdělení do vrstev v kroku 9 jsou podpora plánování a řízení testování, kterou sylabus rozebírá v **oddílu 2.2.4**. Kontrolu odhadů pracnosti z kroku 8 procvičuje i HO-3.1.2b v **kapitole 3, oddílu 3.1.2**. Výběr techniky podle úlohy shrnuje **oddíl 2.2.5**. Kontrola výstupu a úprava promptu v kroku 11 jsou hodnocení výsledků a iterativní ladění promptu z **oddílů 2.3.1 a 2.3.2**.

Bezpečnostní pravidla modulu (žádná firemní data, zástupné údaje místo hesel, kontrola dokumentu před nahráním) vycházejí z **kapitoly 3, oddílů 3.2.1 a 3.2.3**. Vymyšlené hlášky z kroku 2 a chybné součty z kroku 8 jsou příklady halucinací a chyb v uvažování z **kapitoly 3, oddílu 3.1.1**. Rozdílné výsledky ve dvou nástrojích v části Ověření ukazují nedeterministické chování z **oddílu 3.1.4**. Přehled schopností LLM pro testování, včetně analýzy požadavků a generování testovacích dat, je v **kapitole 1, oddílu 1.2.1**.
