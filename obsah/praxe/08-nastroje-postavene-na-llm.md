---
modul: 8
nazev: Testovací nástroje postavené na LLM
podtitul: Vyzkoušíš komerční testovací platformu s LLM na EventHubu od nahrání požadavků po plán vydání a podle vlastních kritérií posoudíš, jestli by obstála na projektu pro banku.
cas: 2–3 h
uroven: začátečník
nastroje: ContextQA, TestMu AI (KaneAI), testRigor, rozšíření prohlížeče Chrome
kapitoly: 1, 2, 3, 4, 5
zdroje: Shetty L61–L68 (příloha EventHub-Product-Requirements-Document)
---

V předchozích modulech jsi skládal nástroje sám: model, MCP servery, skills, CI. Na trhu jsou i hotové platformy, které tohle všechno nabízejí v jednom produktu. Nahraješ požadavky, platforma vygeneruje testovací případy, sama je automatizuje, spustí v cloudu a uchová historii. Shetty v sekci 11 ukazuje jednu z nich, ContextQA, na stejné aplikaci EventHub. Další, TestMu AI, odkazuje na své video.

Modul je kratší a má jiný cíl než ostatní. Nestaví se v něm nic, co by ti zůstalo. Jde o to platformu poznat a umět ji posoudit. Taková rozhodnutí na projektech přicházejí často: dodavatel nástroje předvede demo a tým má říct, jestli ho chce. Demo vždy vypadá dobře. Otázky, které demo neukazuje, jsou na konci modulu.

## Co postavíš

- Zkušební účet na ContextQA s projektem pro EventHub.
- Testovací případy vygenerované z dokumentu požadavků EventHubu, zrevidované a částečně schválené.
- Jeden automaticky provedený end-to-end test s videem a Playwright trace.
- Testovací sadu, plán vydání a jeden test vytvořený z akceptačních kritérií.
- Hodnoticí tabulku platformy podle deseti kritérií.

## Předpoklady

**Znalosti.** Pojmy testovací případ, testovací sada, plán testování a regresní testy z CTFL. Zkušenost z modulu [Prompty pro testera](modul:chatgpt) pomůže při srovnání s chatem.

**Účty.** Stav k 23. 10. 2026, ověř:

| Platforma | Co nabízí | Cena |
|---|---|---|
| ContextQA (contextqa.com) | testy z požadavků, automatizace v přirozeném jazyce, plány vydání, cloudové spuštění, rozšíření pro záznam | komerční, na vyzkoušení zkušební kredity přes odkaz z L63 |
| TestMu AI, produkt KaneAI (v L61 Shetty uvádí KaneAI jako produkt LambdaTestu, vztah značek ověř) | agent pro tvorbu a údržbu testů, HyperExecute pro spouštění | komerční, zkušební verze. Shetty k ní dává jen tříhodinové video (L68). |
| testRigor | testy psané v angličtině, spouštění v cloudu | komerční |

Tabulka slouží jen k orientaci. Shetty v L61 tyto tři platformy jmenuje jako ty, o kterých slyší nejčastěji. Trh se rychle mění a názvy produktů také.

**Podklady.** Dokument požadavků EventHubu z přílohy kurzu (`EventHub-Product-Requirements-Document.pdf`). Veřejná instance `eventhub.rahulshettyacademy.com` a tvůj vlastní testovací účet na ní.

:::pozor
Všechno, co do platformy nahraješ, odchází na servery dodavatele: dokument požadavků, adresa aplikace, přihlašovací údaje k testovacímu účtu, snímky obrazovky a videa z běhů. Proto jen veřejná demo aplikace, vymyšlená data a testovací účet s heslem, které nikde jinde nepoužíváš. Registruj se soukromým e-mailem, ne firemním. Firemní požadavky, kód ani přístup k testovacím prostředím klienta do zkušební verze nepatří. Takový krok by vyžadoval smlouvu, posouzení dodavatele a schválení. Rozšíření prohlížeče z kroku 6 instaluj jen do samostatného profilu Chrome, ve kterém nejsi nikam přihlášený.
:::

## Postup

### Krok 1: Chat, nebo nástroj postavený na LLM (L61)

Shetty začíná rozdílem, který je i v sylabu. Generativní AI v chatu (ChatGPT, Claude, Gemini) je asistent. Z požadavků napíše testovací případy, data i kód. Nic ale nespustí, neuchová historii běhů, nespravuje sady ani plány a neukáže trend selhání. To všechno musíš dělat jinde.

**LLM-powered test tool** (testovací nástroj postavený na LLM) je platforma pro testování, do které je model zabudovaný. Uživatel s modelem nemluví přímo. Pracuje v nástroji a model běží na pozadí. Shetty to popisuje jako nástroj pro správu testů (Jira s Xray, Quality Center), do kterého přibyla AI a automatizace.

| | AI chatbot | Testovací nástroj postavený na LLM |
|---|---|---|
| Výstup | text, kód | testovací případy, automatizované kroky, výsledky běhů |
| Spuštění testů | ne | ano, v cloudu nebo na vlastních strojích |
| Historie a trendy | ne | ano |
| Sady, plány, vydání | ne | ano |
| Kde jsou data | u poskytovatele modelu | u dodavatele platformy a jeho poskytovatele modelu |
| Cena | předplatné nebo tokeny | licence nebo kredity za běhy |

Tabulka shrnuje rozdíl, na který se ptá sylabus v kapitole 1. Shetty k ceně dodává, že s licencí „nemusíš řešit tokeny“. To platí jen napůl. Zkušební verze i placené plány mívají kredity za generování nebo za běhy. Tokeny jsou jen schované v ceníku.

### Krok 2: Požadavky a vyjasňující otázky (L62)

Po přihlášení vytvoř projekt, typ webová aplikace. V části požadavků zvol import ze souboru a nahraj PDF s požadavky EventHubu. ContextQA umí požadavky převzít i z Jiry nebo Azure DevOps. Shetty v L62 zmiňuje ještě dvě možnosti: snímky obrazovky jednotlivých stránek a video z ručního průchodu aplikací. Z nich platforma odvodí uživatelské toky. Shetty sám upozorňuje na omezení. Pravidlo, které na obrazovce není vidět (například limit devíti rezervací), z obrázku nevyčte. Taková sada pokryje toky, ne obchodní pravidla.

Před generováním nastav:

- **Publikování:** *require approval*. Každý vygenerovaný případ projde tvou revizí, než se stane platným. Shetty to volí záměrně. Automatické publikování by do sady pustilo i chybné případy.
- **Typy případů:** pozitivní, negativní, hraniční.

Po spuštění analýzy platforma shrne, co v dokumentu pochopila, a položí **vyjasňující otázky**. V kurzu jsou čtyři. Jaká je výchozí stránka po přihlášení. Jak se uživatel dostane do administrace. Kolik karet akcí je na stránce. Jestli zahrnout bezpečnostní testy mezi uživateli. K tomu chce skutečnou adresu (dokument uvádí `localhost`) a přihlašovací údaje.

Na vyjasňujících otázkách je vidět, že nástroj pracuje s nejistotou lépe než prostý chat. Otázka na počet karet je přesně rozpor, který najdeš v doménových souborech EventHubu (modul [Claude Code pro QA](modul:claude-code), krok 6). Dokument říká devět, frontend posílá dvanáct. Shetty odpoví devět. Odpověď na takovou otázku je rozhodnutí o očekávaném výsledku. Patří analytikovi nebo vlastníkovi produktu, ne tomu, kdo zrovna kliká.

Heslo, které zadáš, platforma uloží jako proměnnou prostředí projektu. Proto testovací účet s jedinečným heslem.

### Krok 3: Revize vygenerovaných případů (L62)

Shetty dostane za pár minut 55 testovacích případů. Pak říká větu, na které stojí celý modul: tvoje role se mění z autora na soudce. Platforma podle něj udělá 90 % správně, zbytek doplní člověk. To číslo je jeho odhad, ne měření. Změř si vlastní.

Projdi aspoň patnáct případů a ke každému zapiš:

1. Odpovídá požadavku v dokumentu? Ke kterému oddílu?
2. Obsahuje očekávaný výsledek, který jde ověřit? „Rezervace proběhne správně“ ověřit nejde.
3. Neopakuje jiný případ?
4. Nevymýšlí pravidlo, které v dokumentu není?
5. Má předpoklad (přihlášení) jako samostatný případ, nebo ho opakuje v krocích?

Shetty v L62 ukazuje, že platforma přihlášení vyčlenila jako předpoklad (prerequisite) a jiné případy na něj odkazují. To je dobrý návrh. Odpovídá principu nezávislých kroků, který znáš z page objects.

Schval jen případy, které revizí prošly. Z tvých poznámek spočítej podíl případů, které by šly použít bez úprav. To je metrika **accuracy** z kapitoly 2 sylabu, změřená na tvém vzorku.

### Krok 4: Z ručního případu automatizovaný test (L64, L65)

Schválený případ otevři a spusť (*Run*). Platforma nemá žádný skript. Každý krok popsaný přirozeným jazykem předá svému agentovi a ten ho v prohlížeči provede. Shetty v L64 sleduje běh přes jednotlivé kroky: přihlášení, katalog, filtr kategorie, výběr akce, rezervace, kontrola v seznamu rezervací, zrušení, kontrola vrácených míst. Celý tok trvá kolem pěti minut.

Po běhu jsou k dispozici video, snímky po krocích a **Playwright trace**. Platforma pod povrchem používá Playwright. Úspěšný případ změní stav z *Review* na *Ready*.

Shetty v L64 říká, že první běh je pomalejší, protože platforma teprve hledá prvky. Další běhy jsou rychlejší, protože si postup „pamatuje“. Stojí za to zjistit, co přesně si pamatuje. Pokud ukládá nalezené lokátory, chová se při dalším běhu jako běžný skript. Pokud kroky pokaždé znovu vykládá model, může se běh od běhu lišit. Na to se zeptej dodavatele. Pro regresní testy je to podstatný rozdíl.

V L65 Shetty ukazuje, jak se test udržuje. Kroky nejsou kód, ale věty. Když se v aplikaci změní popisek pole z „Full Name“ na „Given Name“, opravíš větu v kroku. Když chceš přidat kontrolu, že je vidět rezervační kód, dopíšeš ji do textu kroku. Hodnoty jako adresa, jméno zákazníka nebo heslo jsou v **proměnných prostředí** (*Environment and data*). Pro testovací prostředí UAT si založíš druhou sadu proměnných a test spustíš proti ní.

Vyzkoušej to. Změň v jednom kroku očekávaný text na nesmyslný a spusť test znovu. Má selhat. Pokud projde, platforma krok „opravila“ za tebe a ty o tom víš jen z logu. To by byl nebezpečný druh samoopravy.

### Krok 5: Sady, plán vydání a spouštění (L65, L66)

Schválené případy dej do testovací sady (*Test Suites*). Shetty založí sadu „EventHub“. Pak v L66 vytvoří **plán vydání** („December release“). Plán obsahuje sady a ke každé určuje prostředí:

- prohlížeč a platformu, třeba Safari pro sadu, jejíž uživatelé jsou hlavně na Macu,
- kde testy běží: v cloudu dodavatele (*ContextQA Lab*), nebo na **vlastních zařízeních** (*local devices*),
- kolik testů běží souběžně,
- časový plán: jednorázově k datu, nebo opakovaně (každé úterý).

Plán lze napojit na CI (Jenkins, GitLab) a výsledky jsou v historii plánu. Shetty upozorňuje, že plánované spouštění v jeho instanci zapnuté nebylo. Některé funkce mohou být jen v placených plánech.

Možnost spouštět na vlastních strojích je pro regulované klienty důležitá. Testovaná aplikace v interní síti banky není z cloudu dodavatele dostupná a klient často nechce, aby k ní přístup měl. Zjisti, co v tomto režimu i tak odchází do cloudu. Typicky kroky testu, výsledky, snímky a video.

### Krok 6: Test z akceptačních kritérií a záznam v prohlížeči (L67)

Dvě další cesty, jak test vznikne.

**AI Assistance.** Vložíš akceptační kritéria uživatelského scénáře v běžné řeči a cílovou adresu. Platforma z nich vytvoří testovací případ a rovnou ho provede. Shetty to ukazuje na přihlášení do EventHubu s kontrolou, že se zobrazí tlačítko „Browse Events“. Vyzkoušej vlastní kritéria:

```text
Přihlášený uživatel otevře seznam akcí a vybere první akci s tlačítkem Book Now.
Zvolí 2 lístky, vyplní jméno, e-mail a telefon a potvrdí rezervaci.
Ověř, že se zobrazí rezervační kód a že jeho první písmeno je
první písmeno názvu akce. Ověř, že celková cena je dvojnásobek ceny lístku.
```

**Record and Play.** Nainstaluješ rozšíření ContextQA pro Chrome, zadáš adresu a zapneš nahrávání. Pak aplikaci projdeš ručně. Rozšíření zaznamená kroky a vytvoří z nich testovací případ. Shetty to v L67 dělá na `loginpagePractise`. Upozorňuje, že záznam zachytí i omylem provedené akce (dvojklik místo kliknutí). Kroky je potřeba projít a zbytečné smazat.

Rozšíření pro záznam potřebuje právo číst a měnit obsah stránek, na kterých běží. Podívej se při instalaci, jaká oprávnění žádá. Proto samostatný profil Chrome. Na firemním počítači neinstaluj rozšíření, které firma neschválila.

Shetty zmiňuje i mobilní aplikace (nahraje se instalační balíček a běží v emulátoru dodavatele) a API. Tyto části neukazuje, takže jsou neověřené.

### Krok 7: Hodnoticí tabulka

Teď to hlavní. Vyplň pro platformu tabulku. U každého kritéria napiš, co jsi zjistil a odkud (vyzkoušel, dokumentace, ceník, neznámo).

| Kritérium | Otázka |
|---|---|
| Kvalita generování | Jaký podíl případů prošel revizí bez úprav (krok 3)? |
| Stabilita běhu | Projde stejný test pětkrát po sobě? Liší se kroky mezi běhy? |
| Zachycení chyby | Selže test, když aplikace nebo očekávaný výsledek nesedí (krok 4)? |
| Export | Jdou testy vyexportovat jako kód (Playwright), nebo jen jako text, nebo vůbec? |
| Závislost na dodavateli | Co zbude, když licence skončí? Kolik práce by stálo testy převést jinam? |
| Data | Kam jdou požadavky, hesla, snímky a videa? V jaké zemi? Jak dlouho se uchovávají? Používají se k tréninku modelů? |
| Model | Který model platforma používá a u koho běží? Jde zvolit jiný? |
| Spouštění | Funguje běh na vlastních strojích a co přitom odchází ven? |
| Cena | Licence za uživatele, kredity za běhy, nebo obojí? Kolik by stála sada 300 testů denně? |
| Audit | Je vidět, co AI vygenerovala a co člověk schválil a kdy? |

Tabulka spojuje technické a obchodní otázky. Tři z nich demo v kurzu nezodpoví a jsou pro rozhodnutí nejdůležitější.

**Vendor lock-in** (závislost na dodavateli). Testy v platformě jsou věty v databázi dodavatele. Pokud je nejde vyexportovat jako kód, roky práce na regresní sadě patří s licencí dodavateli. Playwright trace z běhu není totéž co udržovatelný test. Proti tomu stojí vlastní Playwright testy v repozitáři z modulu 5. Ty patří týmu, ale musí je někdo psát a udržovat.

**Data.** Pro projekt pro banku nebo pojišťovnu je nová cloudová platforma pro testování služba třetí strany, která zpracovává informace klienta. Ve finančním sektoru EU se na takové služby vztahuje nařízení **DORA** (Digital Operational Resilience Act), účinné od 17. 1. 2025. Klient musí poskytovatele ICT služeb evidovat a řídit jejich rizika. Výběr takového nástroje proto nedělá tester sám, ani tým sám. Jde přes nákup, bezpečnost a schválení klientem.

**Cena.** Shetty platformu staví do kontrastu s placením za tokeny. Ve skutečnosti platíš obojí, jen jinou formou. Porovnej cenu za měsíc s tím, kolik by stála vlastní sada v Playwright s CI z modulu 6. Do vlastní sady započítej i čas lidí na údržbu. Bez toho srovnání nedává smysl.

:::praxe
Jak by vypadalo rozumné rozhodnutí na projektu pro banku. Tým chce zrychlit přípravu regresních testů. Platforma s LLM na demu zaujme. Rozumný postup je pilot na veřejné nebo syntetické aplikaci, změřená kritéria z tabulky a výsledek předložený s otázkami na data a export. Pokud dodavatel nedá smlouvu o zpracování dat, provoz v EU a export testů, pilot na klientských datech nezačne. To není byrokracie. Je to stejné hodnocení, jaké by tým dělal u jakéhokoli jiného nástroje třetí strany.
:::

## Ověření

- V projektu ContextQA máš vygenerované testovací případy a poznámky z revize aspoň patnácti z nich.
- Jeden end-to-end případ prošel automatizovaným během a máš k němu video nebo trace.
- Test s úmyslně špatným očekávaným výsledkem selhal.
- Máš testovací sadu a plán vydání se dvěma konfiguracemi prohlížeče.
- Hodnoticí tabulka má vyplněné všechny řádky, u každého se zdrojem informace.
- Po skončení zkušební verze jsi smazal projekt a změnil heslo testovacího účtu, nebo účet zrušil.

## Časté chyby

**Automatické publikování.** Vygenerované případy jdou rovnou do sady bez revize. Tým pak udržuje případy, které nikdo nečetl.

**Odpověď na vyjasňující otázku od kohokoli.** Odpověď určí očekávaný výsledek. Patří tomu, kdo zná požadavky.

**Snímky místo požadavků.** Ze snímků vzniknou toky, ne pravidla. Sada vypadá úplně, ale obchodní pravidla netestuje.

**Zelený běh bez kontroly.** Agent platformy může krok vyložit jinak, než jsi chtěl, a test projde. Podívej se na video aspoň u prvních běhů.

**Hodnocení podle dema.** Demo ukazuje šťastnou cestu na jednoduché aplikaci. Kritéria z kroku 7 je potřeba ověřit na vlastním pilotu.

**Firemní e-mail při registraci.** Zkušební účet na firemní adresu vypadá jako firemní rozhodnutí a dodavatel tě bude kontaktovat jako zákazníka. Na zkoušení soukromý e-mail.

**Rozšíření v hlavním profilu prohlížeče.** Rozšíření pro záznam vidí stránky, na kterých jsi přihlášený. Samostatný profil.

## Cvičení

:::cviceni nazev="Platforma proti vlastnímu agentovi"
Cíl: porovnat platformu s řetězcem skills z modulu 5 na stejné úloze. Vezmi oblast správy rezervací. Porovnej scénáře z ContextQA se scénáři z `/create-scenarios`.
Hotovo: tabulka s počtem případů, počtem schválených bez úprav, počtem duplicit a počtem vymyšlených pravidel u obou nástrojů. Jeden odstavec o tom, který výstup bys raději udržoval a proč.
:::

:::cviceni nazev="Hodnocení druhé platformy"
Cíl: procvičit krok 7 na jiném produktu. Projdi Shettyho video k TestMu AI (L68) nebo zkušební verzi testRigoru a vyplň stejnou hodnoticí tabulku.
Hotovo: dvě vyplněné tabulky vedle sebe. U každého kritéria je vyznačené, kde se platformy liší. Tři otázky, které bys dodavateli poslal před pilotem.
:::

:::cviceni nazev="Doporučení pro tým"
Cíl: převést hodnocení do podoby, kterou přečte vedoucí. Napiš doporučení na jednu stranu pro vymyšlený projekt pro pojišťovnu: použít platformu, nepoužít, nebo pilot s podmínkami.
Hotovo: doporučení má cíl měřitelný podle sylabu (o kolik zrychlit, jak to měřit), tři rizika s opatřením a seznam toho, co musí schválit někdo jiný než tým. Text neobsahuje žádná skutečná data klienta.
:::

## Souvislost se sylabem CT-GenAI

Krok 1 je přímo **kapitola 1, oddíl 1.2.2**: rozdíl mezi AI chatbotem a testovací aplikací postavenou na LLM. Platforma z modulu je učebnicový příklad druhé skupiny. Má vlastní rozhraní, z dokumentů připravuje kontext pro model, výstup zařazuje do sad a plánů. To odpovídá architektuře s front-endem, back-endem a LLM z **kapitoly 4, oddílu 4.1.1**. Agent, který kroky v přirozeném jazyce provádí v prohlížeči, je agent z **oddílu 4.1.3**. Otázka, jestli platforma při běhu znovu volá model, nebo spouští uložený skript, souvisí s provozem a monitoringem z **oddílu 4.2.2**.

Generování případů z požadavků a z akceptačních kritérií patří do **kapitoly 2, oddílu 2.2.2**. Opravy kroků přirozeným jazykem a samooprava při změně UI jsou v **oddílu 2.2.3** včetně rizika, že samooprava zakryje defekt. Podíl případů schválených bez úprav a stabilita běhů jsou metriky z **oddílu 2.3.1** (accuracy, execution success rate, time efficiency).

Vymyšlená pravidla v generovaných případech jsou halucinace z **kapitoly 3, oddílu 3.1.1**. Data, která odcházejí dodavateli, a jejich ochrana jsou v **oddílech 3.2.1 a 3.2.3**. Předpisy a rámce pro AI (EU AI Act, NIST AI RMF, ISO/IEC 42001) jsou v **oddílu 3.4.1**. DORA mezi nimi není, je to oborový předpis nad rámec sylabu.

Hodnoticí tabulka z kroku 7 je prakticky provedená **kapitola 5, oddíl 5.1.2** (strategie: cíle, výběr nástroje a modelu, kvalita dat, metriky, pravidla a kvalitativní brány) a **oddíl 5.1.3** (výběr modelu podle úlohy, ceny a provozu). Zkušební účet platformy použitý na firemních datech bez schválení by byla stínová AI z **oddílu 5.1.1**. Pilot místo okamžitého nasazení odpovídá fázím zavedení z **oddílu 5.1.4**.
