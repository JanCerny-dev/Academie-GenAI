---
modul: 2
nazev: Lokální modely a ochrana dat
podtitul: Rozběhneš jazykový model na vlastním počítači, necháš ho odpovídat z vlastních dokumentů a z Pythonu, a víš, kdy má lokální model v bance smysl a kdy ne.
cas: 3–4 h (plus stahování modelů)
uroven: středně pokročilý
nastroje: GPT4All, Python 3, volitelně Ollama nebo LM Studio, Hugging Face Transformers (jen ukázka)
kapitoly: 1, 3, 4, 5
zdroje: Shetty L13, L69, L72; Bruno L11–L13, L36–L37, L82–L83
---

Cloudový chatbot je pohodlný, ale každý prompt odchází na server poskytovatele. Pro testera v bance nebo pojišťovně to znamená jednoduché pravidlo. Do veřejného chatu nesmí nic, co patří klientovi nebo firmě. Lokální model je jedna z cest, jak s AI pracovat i nad citlivějšími podklady. Data neopustí počítač. Má to ale svou cenu: slabší výsledky, nároky na hardware a také lokální instalace je software, který musí schválit IT.

Modul má tři části. Nejdřív zprovozníš GPT4All, které ukazují oba kurzy. Pak ho necháš odpovídat z vlastních dokumentů (LocalDocs). Nakonec se k lokálnímu modelu připojíš z Pythonu a před odesláním promptu z něj odstraníš osobní údaje. Ukázka s GPT-Neo z Brunova kurzu vysvětlí, proč není každý stažený model k užitku.

## Co postavíš

- Funkční GPT4All s malým modelem, ověřené bez připojení k internetu.
- Kolekci LocalDocs nad veřejným dokumentem s požadavky. Model z ní odpovídá a uvádí zdroj.
- Python skript `local_testgen.py`, který přečte požadavky ze souboru, zamaskuje v nich e-maily, rodná čísla, čísla účtů a telefony a pošle je lokálnímu modelu přes rozhraní kompatibilní s OpenAI.
- Test `test_sanitize.py`, který ověří, že maskování funguje.
- Vlastní rozhodovací tabulku: kterou úlohu dělat v cloudu, kterou lokálně a kterou vůbec ne.

## Předpoklady

**Hardware.** Lokální model běží v operační paměti. Orientační pravidlo: volná RAM má být aspoň o pár GB větší než soubor modelu. Bruno v L12 stahuje Llama 3 8B o velikosti asi 4,3 GB, Shetty v L72 doporučuje na zkoušení menší Llama 3.2 a varuje, že větší model „zasekne“ počítač. Na běžném notebooku s 16 GB RAM bez dedikované grafické karty počítej s modelem 1–4 GB a s odpovědí v řádu desítek sekund. Čísla jsou orientační, ověřit na vlastním stroji.

**Software.** Stav k 23. 10. 2026, verze a názvy modelů ověřit:

| Nástroj | Co to je | Cena |
|---|---|---|
| GPT4All (nomic.ai/gpt4all) | desktopová aplikace s katalogem modelů a funkcí LocalDocs | zdarma, ověřit licenci |
| Ollama (ollama.com) | služba na pozadí s příkazovou řádkou a HTTP API | zdarma, nad rámec kurzu |
| LM Studio (lmstudio.ai) | desktopová aplikace s katalogem modelů a lokálním serverem | zdarma pro osobní použití, firemní podmínky ověřit, nad rámec kurzu |
| Python 3.10+ | pro krok 5 a 6 | zdarma |

Tabulka slouží k orientaci. Pro modul stačí GPT4All a Python. Ollama nebo LM Studio použiješ v kroku 5, pokud chceš pohodlnější API.

**Kde to dělat.** Na soukromém počítači. Na firemním notebooku nic z toho bez schválení neinstaluj, ani „jen na zkoušku“. I lokální model je software z internetu: instalátor, knihovny a soubor s vahami modelu. IT musí posoudit jeho původ, licenci a to, kam aplikace volá. Když lokální model chceš používat v práci, obrať se na IT nebo tým, který ve firmě spravuje AI platformu. Jinak jde o stínovou AI (kapitola 5, oddíl 5.1.1).

:::pozor
Lokální model neřeší ochranu dat sám od sebe. Pomáhá jen s jedním rizikem: data neodcházejí k poskytovateli modelu. Pořád platí, že klientská data na soukromém počítači nemají co dělat, a to ani v lokálním modelu. Celý modul proto pracuje s veřejnými a vlastními dokumenty.
:::

## Postup

### Krok 1: Rozhodni, jestli lokální model vůbec potřebuješ

Než něco stáhneš, ujasni si, k čemu lokální model je. Shetty v L13 popisuje tři cesty, kterými firmy řeší obavu z úniku dat do cloudových modelů:

1. **Podnikový model ve vlastním nebo smluvně chráněném prostředí.** Poskytovatel nabízí podnikovou verzi se smlouvou o zpracování dat a s nulovou retencí (zero data retention). Data se neukládají a nepoužívají k tréninku.
2. **Brána před modelem** (AI gateway). Každý prompt nejdřív projde filtrem, který zachytí citlivé údaje a požadavek zablokuje nebo zamaskuje.
3. **Lokální model.** Data neopustí stroj. Výkon omezuje hardware.

Shetty k tomu dodává, že bezpečnost modelů je věc infrastruktury a bezpečnostního týmu, ne testera. To je pravda jen napůl. Výběr a provoz nástroje opravdu řeší IT. Za to, co do nástroje vložíš, ale odpovídáš ty.

Zapiš si do poznámek tři úlohy ze své práce, kde bys AI rád použil, a ke každé jednu větu: jaká data by do modelu šla. Tabulku dokončíš v kroku 8.

Co má vyjít: krátký seznam. Typicky zjistíš, že pro polovinu úloh stačí cloudový chat bez citlivých dat. Například vysvětlení chybové hlášky frameworku nebo návrh struktury testovacího plánu. Lokální model má smysl tam, kde musíš pracovat s interním textem a schválený cloudový nástroj nemáš.

### Krok 2: Nainstaluj GPT4All a stáhni malý model

Bruno (L12) a Shetty (L72) postupují stejně:

1. Na stránce nomic.ai/gpt4all stáhni instalátor pro svůj systém a nainstaluj ho.
2. Spusť aplikaci a otevři **Models** a **Add Model**.
3. Vyber malý model z katalogu. Shetty doporučuje Llama 3.2 (asi 2 GB). Bruno používá Llama 3 8B Instruct (asi 4,3 GB). Názvy a velikosti v katalogu se mění, ověřit.
4. Počkej na stažení. Soubor se uloží do složky, kterou vidíš v **Settings**. Tam ji můžeš i změnit.
5. Otevři **Chats**, založ nový chat a nahoře vyber stažený model.

Pošli kontrolní dotaz:

```text
In three sentences: what is the difference between a test condition and a test case?
```

Co má vyjít: odpověď za několik sekund až desítek sekund. Pak **vypni Wi-Fi nebo odpoj kabel** a pošli další dotaz. Odpověď musí přijít i bez sítě. Tím ověříš, že model opravdu běží lokálně. Oba lektoři to v lekcích dělají stejně.

Všimni si kvality. Malý model odpoví obecně správně, ale u definic ISTQB se často splete nebo je smíchá. Porovnej odpověď s CTFL sylabem. Tohle je první praktická zkušenost s tím, co sylabus říká o malých jazykových modelech (SLM): jsou levnější a soukromé, ale méně přesné.

### Krok 3: Testovací případy z lokálního modelu

V tom samém chatu pošli prompt z Brunovy přílohy L13, jen přeložený do struktury z modulu 1:

```text
You are a test analyst. Create at most 8 functional test cases for a Contact Us form.
Facts:
- Fields First Name, Last Name, Email Address, Comments are all required.
- SUBMIT sends the form, RESET clears all fields.
- Valid submission shows "Thank You for your Message!"
- Invalid email shows "Error: Invalid email address"
- Any empty field shows "Error: all fields are required"
Use only these facts. Output a Markdown table: ID, Title, Steps, Expected result.
```

```text
Jsi test analytik. Vytvoř nejvýš 8 funkčních testovacích případů pro formulář Contact Us.
Fakta:
- Pole First Name, Last Name, Email Address, Comments jsou povinná.
- SUBMIT formulář odešle, RESET vymaže všechna pole.
- Platné odeslání zobrazí "Thank You for your Message!"
- Neplatný e-mail zobrazí "Error: Invalid email address"
- Prázdné pole zobrazí "Error: all fields are required"
Použij jen tato fakta. Výstup: Markdown tabulka ID, Název, Kroky, Očekávaný výsledek.
```

Co má vyjít: tabulka, často s menšími chybami. Malé modely porušují limit počtu, mění znění hlášek nebo nedodrží formát tabulky. V češtině bývají slabší než v angličtině. Spusť stejný prompt v libovolném cloudovém chatu a porovnej. Zapiš si tři konkrétní rozdíly. Bruno v L13 ukazuje i to, že lokální aplikace neumí vytvořit soubor Word. To ale není vlastnost modelu, jen aplikace.

### Krok 4: Model nad vlastními dokumenty (LocalDocs)

Shetty v L69 popisuje situaci, kterou zná každý nový tester v bance. Dostaneš desítky dokumentů a máš se v doméně rychle zorientovat. GPT4All na to má funkci **LocalDocs**. Aplikace dokumenty rozseká na kousky, z každého vytvoří **embedding** (vektorovou reprezentaci) a uloží je do lokálního indexu. Při dotazu nejdřív vyhledá kousky podobné otázce a vloží je modelu do promptu. To je princip **RAG** (generování rozšířené o vyhledávání), který sylabus popisuje v kapitole 4.

Jako dokumenty použij něco veřejného nebo vlastního. Dobře poslouží dokument s požadavky na demo aplikaci EventHub ze Shettyho kurzu (`EventHub-Product-Requirements-Document.pdf`, asi 1 700 slov), Brunův dokument ke Contact Us, nebo dokumentace tvého projektu Účtenky.

1. Dokumenty dej do samostatné složky, třeba `C:\ai-docs\eventhub`.
2. V GPT4All otevři **LocalDocs**, zvol **Add Collection**, pojmenuj ji a vyber složku.
3. Počkej, až aplikace dokončí **embedding**. U pár dokumentů jde o minuty.
4. V chatu vpravo zaškrtni kolekci a pošli otázku, na kterou je odpověď v dokumentu.

Příklad otázek pro EventHub:

```text
According to the documents, how many bookings can one user have at most, and what happens when the limit is reached?
Quote the sentence you used.
```

```text
Podle dokumentů: kolik rezervací může mít jeden uživatel nejvýš a co se stane při dosažení limitu?
Uveď větu, ze které vycházíš.
```

Co má vyjít: odpověď s odkazem na zdroj. GPT4All pod odpovědí ukazuje, ze kterého souboru čerpalo. Dokument EventHub uvádí v požadavku FR-B6 nejvýš 9 rezervací na uživatele. Desátá rezervace smaže nejstarší (FIFO). Stejné pravidlo je i v tabulce Business rules. Ověř, že model odpověděl stejně a že citovaná věta v dokumentu opravdu je.

Pak zkus tři kontrolní otázky. Každá ukazuje jinou slabinu RAG:

- **Otázka, na kterou dokument odpověď nemá.** Třeba „What is the refund policy?“, pokud v dokumentu není. Dobrá odpověď je „v dokumentech to není“. Malý model si často vymyslí obecné pravidlo.
- **Otázka mimo doménu.** Shetty se ptá na hlavní město Itálie. Model odpoví z vlastních znalostí, i když je kolekce zapnutá. Zdroj u odpovědi pak chybí. Vždy proto kontroluj, jestli odpověď vychází z dokumentu.
- **Otázka, jejíž odpověď je rozdělená do dvou míst dokumentu.** Vyhledání najde jen část a odpověď bude neúplná.

Výsledky si zapiš. Přesně tohle je cvičení HO-4.1.2 ze sylabu: vyzkoušet RAG a poznat jeho silné stránky i omezení.

:::pozor
Shetty v L69 tvrdí, že tím „trénuješ vlastní model“. To není přesné. LocalDocs model netrénuje ani nedolaďuje. Model zůstává stejný, jen dostává do promptu vyhledané kousky dokumentů. Rozdíl mezi RAG a fine-tuningem je zkouškové téma (kapitola 4, oddíly 4.1.2 a 4.2.1).
:::

### Krok 5: Lokální model jako API

Okno chatu stačí na zkoušení. Pro opakovanou práci, třeba generování testovacích dat pro každý nový požadavek, se hodí volat model z Pythonu. Všechny tři nástroje umí běžet jako lokální server s rozhraním kompatibilním s OpenAI. Výchozí adresy podle dokumentace nástrojů, ověřit:

| Nástroj | Jak zapnout server | Adresa |
|---|---|---|
| Ollama | běží automaticky po instalaci | `http://localhost:11434/v1` |
| LM Studio | záložka Developer, Start Server | `http://localhost:1234/v1` |
| GPT4All | Settings, Enable Local API Server | `http://localhost:4891/v1` |

Tabulka ukazuje, že skript níže funguje se všemi třemi. Liší se jen adresa a název modelu.

:::nad-ramec
Ollama a LM Studio kurzy nezmiňují. Dnes jsou to běžnější nástroje pro lokální modely než GPT4All. Ollama se ovládá z příkazové řádky. Model stáhneš a spustíš příkazem `ollama run llama3.2:3b` a stejný model je pak dostupný přes API. LM Studio má grafické rozhraní podobné GPT4All a navíc ukazuje, kolik paměti model zabere. Názvy modelů ověřit v katalogu nástroje.
:::

Pro Ollamu stáhni model a ověř, že server odpovídá:

```text
ollama pull llama3.2:3b
ollama list
```

Co má vyjít: model v seznamu s velikostí kolem 2 GB (ověřit).

### Krok 6: Python skript s maskováním osobních údajů

Bruno v L83 radí dvě věci, které platí pro cloudová i lokální API. Data před odesláním **anonymizuj** (nahraď citlivé hodnoty zástupnými) a API klíče nikdy nepiš do kódu. Lokální server klíč nepotřebuje, takže druhé pravidlo tu odpadá. První platí dál. Návyk maskovat data se ti vyplatí ve chvíli, kdy stejný skript přepneš na cloudové API.

Vytvoř složku projektu a v ní soubor `local_testgen.py`:

```python
# local_testgen.py – testovací případy z lokálního modelu přes OpenAI-kompatibilní API
import json
import os
import re
import sys
import urllib.request

BASE_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434/v1")  # Ollama
MODEL = os.getenv("LOCAL_LLM_MODEL", "llama3.2:3b")

PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "<EMAIL>"),
    (re.compile(r"\bCZ\d{2}(?: ?\d{4}){5}\b"), "<IBAN>"),
    (re.compile(r"\b\d{6}/\d{3,4}\b"), "<RC>"),
    (re.compile(r"\b(?:\d{1,6}-)?\d{2,10}/\d{4}\b"), "<UCET>"),
    (re.compile(r"\b\d{9,10}\b"), "<RC>"),
    (re.compile(r"(?:\+420 ?)?\b\d{3} ?\d{3} ?\d{3}\b"), "<TELEFON>"),
]


def sanitize(text: str) -> str:
    for pattern, placeholder in PATTERNS:
        text = pattern.sub(placeholder, text)
    return text


def ask(prompt: str) -> str:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a test analyst. Answer only from the given requirements."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.load(resp)
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    requirements = open(sys.argv[1], encoding="utf-8").read()
    clean = sanitize(requirements)
    prompt = (
        "Create at most 10 functional test cases as a Markdown table "
        "(ID, Title, Steps, Expected result) for these requirements. "
        "If something is unclear, list it under 'Open questions'.\n\n" + clean
    )
    print(ask(prompt))
```

Co v kódu stojí za vysvětlení:

- Skript používá jen standardní knihovnu Pythonu. Nic se neinstaluje přes `pip`, takže ho jde spustit i na stroji s omezeným přístupem k balíčkům.
- Adresa serveru a název modelu jsou v proměnných prostředí. Přepnutí na LM Studio je jen změna `LOCAL_LLM_URL`, ne úprava kódu.
- `sanitize()` prochází seznam regulárních výrazů a nahrazuje nálezy zástupným textem. Pořadí je důležité. Rodné číslo s lomítkem musí být nahrazeno dřív než číslo účtu, jinak by ho výraz pro účet označil jako účet. U šestimístného čísla účtu s kódem banky to nejde rozlišit, ale zamaskované je v obou případech.
- Systémový prompt drží model u dodaných požadavků. `temperature` 0.2 snižuje rozptyl odpovědí (kapitola 3, oddíl 3.1.4).
- `timeout=600`: lokální model na procesoru může odpovídat i minuty.

Vedle vytvoř test maskování `test_sanitize.py`. Údaje v něm jsou vymyšlené:

```python
from local_testgen import sanitize


def test_masks_personal_data():
    text = ("Klient jan.novak@banka.cz, RČ 850101/1234, účet 19-2000145399/0800, "
            "IBAN CZ65 0800 0000 1920 0014 5399, tel. +420 777 123 456.")
    out = sanitize(text)
    for leaked in ["jan.novak", "850101", "2000145399", "CZ65", "777 123"]:
        assert leaked not in out, out


def test_keeps_normal_text():
    assert sanitize("Pole Email Address je povinné.") == "Pole Email Address je povinné."
```

Spusť test a pak skript nad dokumentem s požadavky (třeba Brunovým Contact Us uloženým jako `contact_us.txt`):

```text
python -m pip install pytest
python -m pytest test_sanitize.py -v
python local_testgen.py contact_us.txt
```

Pro LM Studio před spuštěním nastav proměnné (PowerShell):

```text
$env:LOCAL_LLM_URL = "http://localhost:1234/v1"
$env:LOCAL_LLM_MODEL = "<název modelu z LM Studia>"
python local_testgen.py contact_us.txt
```

Co má vyjít: oba testy projdou. Skript vypíše tabulku testovacích případů. První volání může trvat déle, protože server model načítá do paměti. Maskování a test jsou ověřené spuštěním (Python 3.12, 10/2026). Volání API je ověřené jen proti zkušebnímu serveru, který vrací pevnou odpověď ve formátu OpenAI. Se skutečnou Ollamou, LM Studiem a GPT4All neověřeno.

Maskování přes regulární výrazy je pomůcka, ne záruka. Nepozná jména, adresy, čísla smluv ani interní názvy systémů. Proto je pravidlo opačné, než by se mohlo zdát. Maskování nedělá z citlivého dokumentu bezpečný. Je to pojistka pro případ, že ti do veřejného nebo vlastního dokumentu něco proklouzne. Rozdíl mezi anonymizací a pseudonymizací vysvětluje kapitola 3, oddíl 3.2.3. Výměna e-mailu za `<EMAIL>` je anonymizace jen tehdy, když z textu nejde osobu poznat jinak.

### Krok 7: Proč ne každý model – ukázka GPT-Neo

Bruno v L36 ukazuje opačnou cestu než GPT4All. Stáhne model **GPT-Neo 2.7B** z platformy **Hugging Face** a spustí ho přímo z Pythonu přes knihovnu `transformers`. Sám radí lekci jen sledovat a nepouštět. Model má kolem 10 GB, instalace knihoven narazí na verzi Pythonu a na Windows potřebuje i Rust a nástroje Visual Studio. Odpověď na procesoru trvá dlouho a výsledek podle Bruna není moc užitečný.

Podstatná část jeho kódu má tři řádky:

```python
from transformers import pipeline

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
response = generator(prompt, max_new_tokens=500)
```

`pipeline("text-generation")` načte model a při prvním spuštění ho stáhne do mezipaměti Hugging Face. `max_new_tokens` omezuje délku odpovědi. Zbytek Brunova souboru jen volí GPU nebo CPU a přesnost výpočtů.

Kurz nevysvětluje, proč je výsledek tak slabý. Hlavní důvod je v typu modelu. GPT-Neo z roku 2021 je **foundation LLM** (základní model). Neumí plnit instrukce, jen pokračuje v textu. Na prompt „Generate test cases…“ proto často napíše další podobné zadání nebo náhodný text. GPT4All i Ollama naopak nabízejí modely vyladěné na instrukce (instruction-tuned), obvykle s „Instruct“ nebo „chat“ v názvu. Rozdíl vysvětluje kapitola 1, oddíl 1.1.3.

Pokud si to chceš ověřit, vezmi místo 2.7B nejmenší variantu `EleutherAI/gpt-neo-125m` (zhruba 0,5 GB, ověřit). Stejný prompt jako v kroku 3 dá text, který s testovacími případy skoro nesouvisí. Instalace `transformers` a `torch` ale stáhne několik GB knihoven. Neověřeno.

Bruno v L37 shrnuje volbu modelu do tří možností. Cloudové API (OpenAI) je rychlé a jednoduché, ale platí se za použití a data odcházejí ven. Open-source model v kódu je zdarma a flexibilní, ale náročný na hardware a nastavení. GPT4All je kompromis: lokální model s optimalizovaným během a jednoduchým rozhraním. Dnes do stejné škatulky patří Ollama a LM Studio.

### Krok 8: Rozhodovací tabulka pro práci v bance

Vrať se k seznamu z kroku 1 a doplň ho do tabulky. Níže je vzor s typickými úlohami testera. Hodnoty jsou ilustrační. Co skutečně smíš, určuje interní pravidlo firmy, ne tahle tabulka.

| Úloha | Data, která by šla do modelu | Veřejný cloudový chat | Schválený podnikový nástroj | Lokální model na soukromém PC |
|---|---|---|---|---|
| Vysvětlit chybu v pytest nebo Playwright | obecný kód bez názvů systémů | ano | ano | ano |
| Testovací případy z požadavků klienta | interní dokument | ne | ano, podle pravidel | ne |
| Testovací data pro formulář | syntetická data | ano | ano | ano |
| Analýza logu z testovacího prostředí | technické a možná osobní údaje | ne | podle pravidel, po kontrole | ne |
| Rešerše domény z dokumentace projektu | interní dokumenty | ne | ano, podle pravidel | ne |
| Procvičování na veřejném demo projektu | veřejná data | ano | ano | ano |

Tabulka ukazuje hlavní poznatek modulu. Lokální model na soukromém počítači nepřidává žádné nové povolení pro firemní data. Smysl má pro učení, pro vlastní projekty a jako argument pro IT. Ve firmě odpovídá spíš sloupec „schválený podnikový nástroj“. Ten může být i lokálně provozovaný model na firemní infrastruktuře.

Bruno v L82 přidává tři etické zásady, které do tabulky nejdou, ale patří k ní:

- **Zkreslení (bias).** Model může v testovacích datech přednostně generovat jen některé typy jmen, adres nebo věkových skupin. Kontroluj rozložení vygenerovaných dat, hlavně u testů, které mají odhalit diskriminaci, třeba u scoringu.
- **Přílišné spoléhání na AI** (over-reliance). Výstup kontroluje člověk, který systému rozumí.
- **Transparentnost.** Zaznamenej, kde a jak jsi AI použil, s nástrojem a modelem. Bruno to doporučuje jako běžnou praxi. Ve firmě to často požadují i interní pravidla. Text vygenerovaný AI se nemá v dokumentaci vydávat za ručně psaný.

## Ověření

- Po odpojení od sítě GPT4All dál odpovídá (krok 2).
- Máš zapsané tři konkrétní rozdíly mezi výstupem lokálního a cloudového modelu na stejném promptu (krok 3).
- LocalDocs odpověděla na otázku z dokumentu se správným zdrojem a máš zapsané výsledky tří kontrolních otázek (krok 4).
- `python -m pytest test_sanitize.py` projde. Když do testu přidáš vlastní vymyšlené rodné číslo v jiném formátu a test selže, víš proč.
- `local_testgen.py` vrátí odpověď z lokálního serveru. Během běhu vidíš ve Správci úloh, že roste využití procesoru nebo GPU. To je důkaz, že výpočet běží u tebe.
- Rozhodovací tabulka z kroku 8 má aspoň tři tvoje úlohy.

## Časté chyby

**Příliš velký model.** Stáhneš model, který se do paměti nevejde. Počítač začne swapovat a odpověď nepřijde. Začni modelem do 4 GB a zvětšuj postupně.

**Základní model místo instrukčního.** Model jen pokračuje v textu a na zadání nereaguje. Hledej v názvu „Instruct“ nebo „chat“.

**Vypnutá kolekce LocalDocs.** Model odpovídá ze svých znalostí a ty si myslíš, že z dokumentů. Kontroluj, jestli je u odpovědi uvedený zdroj.

**Záměna RAG za trénink.** LocalDocs model nemění. Když dokumenty smažeš z kolekce, model o nich nic neví.

**Lokální instalace na firemním notebooku bez schválení.** I když data neodcházejí, jde o neschválený software. Řeší se s IT, ne obcházením.

**Víra v maskování.** Regulární výraz nepozná jméno ani interní identifikátor. Citlivý dokument maskováním bezpečný nebude.

**Neověřená licence modelu.** Modely mají různé licence. Některé omezují komerční použití. Pro firemní nasazení to musí posoudit IT nebo právní oddělení.

## Cvičení

:::cviceni nazev="Lokální versus cloud na jedné úloze"
Cíl: změřit rozdíl v kvalitě a čase. Spusť prompt z kroku 3 třikrát v lokálním modelu a třikrát v cloudovém chatu. U každého běhu zapiš čas odpovědi, počet testovacích případů a počet chyb (vymyšlená hláška, porušený formát, překročený limit).
Hotovo: tabulka šesti běhů a dvě věty závěru, pro kterou úlohu by ti lokální model stačil.
:::

:::cviceni nazev="RAG nad dokumentací vlastního projektu"
Cíl: vyzkoušet RAG na skutečném projektu. Vytvoř kolekci LocalDocs z README a dokumentace projektu Účtenky nebo BOS Harvester. Napiš pět otázek, na které znáš odpověď: tři s odpovědí v dokumentaci, jednu s odpovědí rozdělenou do dvou souborů a jednu, na kterou dokumentace odpověď nemá.
Hotovo: u každé otázky zapsaná odpověď, uvedený zdroj a hodnocení správná / částečná / vymyšlená. Aspoň jedna věta o tom, co bys v dokumentaci změnil, aby vyhledávání fungovalo lépe.
:::

:::cviceni nazev="Rozšíření maskování"
Cíl: procvičit, že maskování je pomůcka s mezerami. Přidej do `PATTERNS` výraz pro číslo pojistné smlouvy ve vymyšleném formátu `PS-2026-000123` a pro datum narození `1. 1. 1985`. Ke každému napiš test v `test_sanitize.py`. Pak napiš test, který ukáže, co maskování nezachytí (například jméno a příjmení), a označ ho `@pytest.mark.xfail` (na začátek souboru pak patří `import pytest`).
Hotovo: všechny testy projdou nebo jsou označené jako očekávané selhání. Komentář v kódu vysvětluje, proč jména regulárním výrazem maskovat nejdou.
:::

## Souvislost se sylabem CT-GenAI

Modul je praktickou podobou **kapitoly 3, oddílu 3.2**. Rizika posílání dat do cloudu a ztráta kontroly nad nimi jsou v **oddílu 3.2.1**. Opatření z kroku 6 a 8 (minimalizace dat, anonymizace, schválené prostředí) jsou v **oddílu 3.2.3**. Tam je i praktický příklad s GPT4All. Teplota v API volání souvisí s nedeterministickým chováním z **oddílu 3.1.4**. Etické zásady z Brunovy lekce L82 navazují na zkreslení (bias) v **oddílu 3.1.1** a na předpisy a rámce v **oddílu 3.4.1**. Spotřebě energie a nástrojům na její měření, včetně měření lokálně běžícího kódu, se věnuje **oddíl 3.3.1**.

LocalDocs v kroku 4 je RAG z **kapitoly 4, oddílu 4.1.2**. Odpovídá praktickému cíli HO-4.1.2. Rozdíl mezi RAG a doladěním modelu je v **oddílu 4.2.1**. Proč GPT-Neo nereaguje na instrukce, vysvětluje rozdíl mezi základním a instrukčním modelem v **kapitole 1, oddílu 1.1.3**.

Výběr mezi velkým cloudovým modelem a malým lokálním modelem je téma **kapitoly 5, oddílu 5.1.3** (výběr LLM/SLM). Instalace lokálního nástroje bez schválení je stínová AI z **oddílu 5.1.1**.
