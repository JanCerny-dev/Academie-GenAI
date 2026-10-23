---
modul: 9
nazev: Generování testovacích případů z Pythonu přes API LLM
podtitul: Napíšeš skript, který z požadavků vygeneruje testovací případy ve formátu JSON, zkontroluje je a řekne, kolik volání stálo.
cas: 3–4 h
uroven: středně pokročilý
nastroje: Python 3.12, openai (Python SDK), python-dotenv, VS Code
kapitoly: 2, 3, 5
zdroje: Bruno L15–L16, L30–L37
---

## Co postavíš

V chatu ChatGPT nebo Copilot se testovací případy generují ručně: vložíš požadavek, zkopíruješ odpověď. To funguje pro jeden formulář. Když chceš totéž opakovat pro desítky požadavků, porovnávat výsledky mezi verzemi promptu nebo výstup rovnou předat dalšímu nástroji, potřebuješ volat model z kódu. K tomu slouží **API** (application programming interface, aplikační rozhraní) poskytovatele modelu.

Na konci modulu budeš mít malý projekt `genai-tc` s jedním hlavním skriptem. Skript načte textový popis požadavků, pošle ho modelu přes OpenAI API, dostane zpět testovací případy jako JSON, zkontroluje jejich strukturu a uloží je do souboru. K tomu vypíše, kolik **tokenů** (token, nejmenší jednotka textu, kterou model zpracovává) volání spotřebovalo a kolik to zhruba stálo.

Jako testovací bázi použijeme stránku Contact Us na webdriveruniversity.com. Je to veřejná cvičná aplikace, kterou Bruno používá v celém kurzu. Stejná stránka se objeví i v modulu 10, kde nad ní postavíš BDD framework.

```text
genai-tc/
├── .venv/                  virtuální prostředí (není v gitu)
├── .env                    API klíč (není v gitu)
├── .gitignore
├── requirements.txt
├── pozadavky/
│   └── contact_us.md       testovací báze: popis formuláře
├── generuj_tc.py           hlavní skript
├── porovnej_behy.py        kontrola opakovatelnosti
└── vystup/                 vygenerované testovací případy (JSON)
```

Kurz má k tomu tři části. Lekce L15 a L16 ukazují, jak AI rozšíří testovací data v jednoduchém Python programu. Lekce L33 až L35 zakládají účet u OpenAI a posílají první dotaz z kódu. Lekce L36 a L37 srovnávají placené API s lokálními modely. Tento modul jde dál než kurz: přidává strukturovaný výstup, kontrolu výsledku, měření opakovatelnosti a bezpečné uložení klíče.

## Předpoklady

Python a jeho základy (proměnné, funkce, slovníky, práce se soubory, `pip`) kurz probírá v sekcích 4 a 5. Tady je nevykládám. Potřebuješ:

- **Python 3.12** nebo novější (ověřeno na 3.12.10). Kurz natáčel na 3.13.
- **VS Code** s rozšířením Python. Kurz ještě používá Code Runner, ten není nutný.
- **Účet na platform.openai.com s kreditem.** API je placené odděleně od předplatného ChatGPT. Bruno v L33 uvádí minimální dobití 5 USD a případný zkušební kredit. Podmínky se mění, ověř je na stránce s ceníkem (openai.com/api/pricing).
- **Knihovny:** `openai` a `python-dotenv`. Kurz má v `requirements.txt` verzi `openai==1.57.0` (prosinec 2024). Novější verze existují. Kód v tomto modulu používá rozhraní Chat Completions, které má knihovna od verze 1.0.

:::pozor
Do API nikdy neposílej firemní ani klientská data. Účet na OpenAI je tvůj osobní, data jdou mimo firmu a mimo smluvní ochranu Trasku. Cvičení dělej jen na veřejných demo aplikacích a na vlastních projektech. Pokud chceš LLM používat v práci, schválený přístup zajišťuje AI platform tým. Obcházet ho osobním klíčem je přesně ta **shadow AI** (stínová AI), o které mluví sylabus v oddílu 5.1.1.
:::

Cena za celé cvičení je v řádu centů. Generování desítky testovacích případů má typicky jednotky tisíc tokenů. Přesné ceny za milion tokenů se liší podle modelu a mění se, proto je v kódu nepíšu napevno.

## Postup

### Krok 1: Projekt a virtuální prostředí

**Virtual environment** (virtuální prostředí) je samostatná instalace balíčků jen pro jeden projekt. Když v jednom projektu potřebuješ `openai` 1.57 a v jiném novější verzi, každý má svou kopii a navzájem se neovlivní. Bruno to v L34 ukazuje přes Command Palette ve VS Code (*Python: Create Environment*). Stejný výsledek dá příkazová řádka:

```powershell
mkdir genai-tc
cd genai-tc
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install openai python-dotenv
pip freeze > requirements.txt
```

Po aktivaci vidíš na začátku řádku `(.venv)`. Příkaz `pip freeze` zapíše přesné verze všech nainstalovaných balíčků. Kolega pak projekt obnoví příkazem `pip install -r requirements.txt` a dostane stejné verze.

Pokud PowerShell aktivaci odmítne kvůli zásadám spouštění skriptů, nespouštěj nic se zvýšenými právy. Stačí spouštět Python přímo z prostředí: `.\.venv\Scripts\python.exe generuj_tc.py`. Výsledek je stejný.

Bruno v L34 narazil na chybu při `pip install openai` a vyřešil ji smazáním a novým vytvořením prostředí. To je rozumný postup. Prostředí je jednorázové a dá se kdykoli znovu vytvořit z `requirements.txt`.

### Krok 2: API klíč a proč nepatří do kódu

API klíč získáš na platform.openai.com v sekci API keys tlačítkem *Create new secret key*. Klíč se zobrazí jen jednou. Kdo ho má, může tvým jménem volat API a utrácet tvůj kredit.

Bruno v L35 vkládá klíč přímo do zdrojového kódu jako `api_key='...'`. V modulu 10 ho pak ukládá do souboru `config/openai_key.json`. Obojí je pro výuku pohodlné a v praxi nebezpečné. Soubor se zdrojákem nebo konfigurací skončí v gitu, v e-mailu, ve sdíleném adresáři nebo ve screenshotu. Odtud ho najdou automatické skenery, které GitHub prochází nepřetržitě. Klíč v historii gitu nezmizí ani po smazání souboru.

Bezpečnější varianta: klíč patří do **proměnné prostředí** (environment variable). Knihovna `openai` ji umí přečíst sama. Pokud v konstruktoru `OpenAI()` neuvedeš `api_key`, hledá proměnnou `OPENAI_API_KEY`.

Pro lokální vývoj je praktický soubor `.env`, který se načte při startu skriptu a nikdy se necommituje. Nejdřív vytvoř `.gitignore`, teprve potom `.env`:

```text
# .gitignore
.venv/
.env
__pycache__/
vystup/
```

```text
# .env  (jen lokálně, nikdy do gitu ani do chatu)
OPENAI_API_KEY=sem-vloz-svuj-klic
OPENAI_MODEL=gpt-4o-mini
```

Do repozitáře místo toho patří `.env.example` se stejnými názvy proměnných a prázdnými hodnotami. Kolega z něj pozná, co má nastavit, a žádné tajemství neuvidí.

Ještě o stupeň lepší je **Windows Credential Manager** (Správce přihlašovacích údajů). Klíč je pak uložený šifrovaně pod tvým uživatelským účtem a není v žádném souboru projektu. Z Pythonu se k němu dostaneš knihovnou `keyring` (neověřeno):

```python
# jednorázově: uložení klíče, zadáš ho do skrytého vstupu
import getpass, keyring
keyring.set_password("openai", "api_key", getpass.getpass("OpenAI klíč: "))
```

```python
# ve skriptu: načtení klíče
import keyring
from openai import OpenAI
client = OpenAI(api_key=keyring.get_password("openai", "api_key"))
```

Ve zbytku modulu používám `.env`, protože ho uvidíš i v cizích projektech a v CI (modul 12 ukazuje, jak klíč předat Jenkinsu).

:::pozor
Klíč nevkládej do chatu s AI asistentem, do Teams ani do ticketu. Pokud se klíč někam dostal, okamžitě ho na platform.openai.com zruš a vytvoř nový. Zrušení je jediná spolehlivá náprava. V nastavení projektu na OpenAI si navíc nastav limit útraty (usage limit), aby chyba v cyklu nevyčerpala celý kredit.
:::

### Krok 3: První volání API

Kód z L35 dělá čtyři věci. Vytvoří klienta, sestaví zprávu, pošle požadavek a vypíše odpověď. Podstatná část vypadá takto (klíč v kódu je převzatý z kurzu a je to přesně to, co děláme jinak):

```python
from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')      # kurz: klíč přímo v kódu

messages = [{"role": "user", "content": "Generate test cases for a Contact Us Page, based on: ..."}]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=1500,
)
print(response.choices[0].message.content.strip())
```

Projdi si jednotlivé části:

- `messages` je seznam zpráv konverzace. Každá zpráva má `role` (kdo mluví) a `content` (text). Role `user` je uživatelský prompt. Později přidáme roli `system`.
- `client.chat.completions.create` je jedno HTTP volání na endpoint Chat Completions. Model nemá paměť mezi voláními. Co chceš, aby věděl, musí být v `messages`.
- `model` určuje, který model odpoví. Kurz používá `gpt-3.5-turbo`, starý a dnes nedoporučovaný model. Aktuální názvy a ceny najdeš na stránce Models v dokumentaci OpenAI.
- `max_tokens` je strop délky odpovědi. Když ho model dosáhne, odpověď se uřízne uprostřed. Bruno v L35 zkouší 500, 1500 a 2500 tokenů. Výsledek je pokaždé pět nebo šest podobných testovacích případů. Delší limit tedy neznamená lepší výstup, jen dovoluje delší odpověď.
- `response.choices[0].message.content` je text odpovědi. Seznam `choices` má víc prvků jen tehdy, když si vyžádáš víc variant odpovědi najednou.

Vlastní minimální verze s klíčem z `.env` (soubor `prvni_volani.py`):

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()                                  # načte .env do proměnných prostředí
client = OpenAI()                              # klíč si vezme z OPENAI_API_KEY
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

odpoved = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Napiš tři testovací podmínky pro pole E-mail ve formuláři."}],
    max_tokens=300,
)
print(odpoved.choices[0].message.content)
print("tokeny:", odpoved.usage.prompt_tokens, "+", odpoved.usage.completion_tokens)
```

Spusť `python prvni_volani.py`. Má vyjít krátký seznam podmínek a řádek s počtem tokenů. Pokud dostaneš chybu 401, klíč se nenačetl nebo je neplatný. Chyba 429 znamená vyčerpaný kredit nebo limit požadavků. Výchozí model `gpt-4o-mini` je jen příklad (neověřeno, zda je v době čtení stále nabízen). Model měň v `.env`, ne v kódu.

### Krok 4: Požadavky do souboru, prompt do struktury

Bruno má požadavky na formulář napsané přímo v řetězci v kódu. Když je přesuneš do samostatného souboru, oddělíš testovací bázi od logiky. Soubor můžeš verzovat, revidovat a měnit bez zásahu do Pythonu. Vytvoř `pozadavky/contact_us.md` vlastními slovy podle stránky:

```text
Formulář Contact Us (https://webdriveruniversity.com/Contact-Us/contactus.html)
- Pole: First Name, Last Name, Email Address, Comments. Všechna jsou povinná.
- Tlačítko SUBMIT odešle formulář.
- Tlačítko RESET vymaže všechna pole.
- E-mail musí být ve platném formátu (obsahuje @ a doménu).
- Po úspěšném odeslání se zobrazí stránka s textem "Thank You for your Message!".
- Při chybě se zobrazí "Error: all fields are required" nebo "Error: Invalid email address".
```

Pozor na drobnost, kterou Bruno odhalí až při automatizaci v modulu 10. Jeho prompt uvádí "Thank You for your Message" a "Error: All fields are required". Skutečná stránka ukazuje "Thank You for your Message!" s vykřičníkem a "all" malým písmenem. Model přesné texty zná jen z promptu. Když je v požadavku překlep, model ho věrně zopakuje do každého testovacího případu.

Teď prompt. Oddíl 2.1.1 sylabu skládá prompt z komponent **Role**, **Context**, **Instruction**, **Input Data**, **Constraints** a **Output Format**. V API se to přirozeně rozdělí do dvou zpráv. **System prompt** (systémový prompt) nese to, co platí pro každé volání: roli, pravidla a tvar výstupu. **User prompt** (uživatelský prompt) nese konkrétní vstup, tedy požadavky jednoho formuláře.

```python
SYSTEM = """Jsi zkušený test analytik. Navrhuješ testovací případy pro webové formuláře.
Pravidla:
- Vycházej jen z požadavků v uživatelské zprávě. Nic si nedomýšlej.
- Pokud je požadavek nejasný, zapiš to do pole "otazky", nevymýšlej chování.
- Použij rozdělení do tříd ekvivalence a testování hraničních hodnot.
- Očekávaný výsledek piš přesně textem z požadavků.
Výstup: pouze JSON objekt podle zadaného schématu, bez komentářů."""

def user_prompt(pozadavky: str) -> str:
    return f"""Navrhni 6 až 10 testovacích případů pro tento formulář.
Pokryj úspěšné odeslání, každé povinné pole, neplatný e-mail a tlačítko RESET.

Požadavky:
{pozadavky}"""
```

Pravidlo "nic si nedomýšlej" a pole pro otázky jsou obrana proti **hallucination** (halucinace), tedy vymyšleným funkcím nebo hláškám. Model, kterému dovolíš říct "nevím", si méně často vymýšlí.

### Krok 5: Strukturovaný výstup (JSON)

Volný text z L35 se dobře čte, ale špatně zpracovává. Pokud chceš testovací případy nahrát do Jira, Xray nebo předat dalšímu skriptu, potřebuješ pevnou strukturu. OpenAI API nabízí dvě úrovně:

| Režim | Parametr | Co zaručuje |
|---|---|---|
| JSON mode | `response_format={"type": "json_object"}` | Odpověď je platný JSON. Strukturu nehlídá. Prompt musí obsahovat slovo „JSON“. |
| Structured Outputs | `response_format={"type": "json_schema", ...}` | Odpověď odpovídá zadanému JSON Schema, pokud model schéma podporuje. |

Tabulka ukazuje, proč je druhý režim lepší: s JSON mode dostaneš syntakticky správný JSON, ale klidně s jinými klíči, než čekáš. Schéma pro náš případ:

```python
SCHEMA = {
    "name": "testovaci_pripady",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["testovaci_pripady", "otazky"],
        "properties": {
            "otazky": {"type": "array", "items": {"type": "string"}},
            "testovaci_pripady": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "nazev", "technika", "kroky", "ocekavany_vysledek", "priorita"],
                    "properties": {
                        "id": {"type": "string"},
                        "nazev": {"type": "string"},
                        "technika": {"type": "string"},
                        "kroky": {"type": "array", "items": {"type": "string"}},
                        "ocekavany_vysledek": {"type": "string"},
                        "priorita": {"type": "string", "enum": ["vysoka", "stredni", "nizka"]},
                    },
                },
            },
        },
    },
}
```

V režimu `strict` musí mít každý objekt `additionalProperties: false` a v `required` všechna pole. Jinak API požadavek odmítne. Pole `technika` nutí model napsat, jakou techniku návrhu testů použil. Recenzent pak rychle vidí, jestli jsou hraniční hodnoty opravdu hraniční.

Ani schéma nenahradí kontrolu. Model může vrátit prázdný seznam kroků, dvakrát stejné ID nebo uříznutý JSON, když narazí na `max_tokens`. Proto výstup vždy ověř vlastní funkcí. Následující validace používá jen standardní knihovnu (ověřeno spuštěním na ukázkových datech, viz `zdroje/_pracovni/bruno/over_offline.py`):

```python
import json

POVINNE = {"id", "nazev", "kroky", "ocekavany_vysledek", "priorita"}
PRIORITY = {"vysoka", "stredni", "nizka"}

def ocisti(text: str) -> str:
    """Odstraní obal ```json ... ```, pokud ho model přidal (v JSON režimu se to nestává)."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()

def validuj(text: str) -> list[dict]:
    data = json.loads(ocisti(text))
    chyby, videna_id = [], set()
    for i, tc in enumerate(data["testovaci_pripady"], 1):
        if chybi := POVINNE - tc.keys():
            chyby.append(f"#{i}: chybí {sorted(chybi)}")
        if tc.get("priorita") not in PRIORITY:
            chyby.append(f"#{i}: neplatná priorita {tc.get('priorita')!r}")
        if not tc.get("kroky"):
            chyby.append(f"#{i}: žádné kroky")
        if tc.get("id") in videna_id:
            chyby.append(f"#{i}: duplicitní id {tc.get('id')}")
        videna_id.add(tc.get("id"))
    if chyby:
        raise ValueError("; ".join(chyby))
    return data["testovaci_pripady"]
```

Funkce `ocisti` řeší zvyk, který Bruno potkal v L42. Model rád obalí odpověď do markdownového bloku kódu se značkou `gherkin` nebo `json`, i když to nechceš. Bruno to řeší větou v promptu. Kód, který obal odstraní, je spolehlivější.

Hlavní skript `generuj_tc.py` vše spojí (neověřeno spuštěním, vyžaduje klíč):

```python
import json, os, sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
# SYSTEM, user_prompt, SCHEMA, validuj: z předchozích kroků (vlož je sem nebo do modulu prompty.py)

load_dotenv()
client = OpenAI()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

def generuj(soubor_pozadavku: str, teplota: float = 0.2) -> dict:
    pozadavky = Path(soubor_pozadavku).read_text(encoding="utf-8")
    odpoved = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt(pozadavky)},
        ],
        response_format={"type": "json_schema", "json_schema": SCHEMA},
        temperature=teplota,
        max_tokens=3000,
    )
    volba = odpoved.choices[0]
    if volba.finish_reason == "length":
        sys.exit("Odpověď se uřízla na max_tokens. Zvyš limit nebo zmenši zadání.")
    pripady = validuj(volba.message.content)
    return {"model": odpoved.model, "usage": odpoved.usage.model_dump(), "pripady": pripady,
            "otazky": json.loads(volba.message.content)["otazky"]}

if __name__ == "__main__":
    vysledek = generuj(sys.argv[1] if len(sys.argv) > 1 else "pozadavky/contact_us.md")
    Path("vystup").mkdir(exist_ok=True)
    cil = Path("vystup/contact_us.json")
    cil.write_text(json.dumps(vysledek, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(vysledek['pripady'])} testovacích případů uloženo do {cil}")
    for o in vysledek["otazky"]:
        print("Otázka k požadavkům:", o)
```

Kontrola `finish_reason == "length"` je důležitá. Bez ní dostaneš uříznutý JSON a `json.loads` spadne s nesrozumitelnou chybou. Klíč `ensure_ascii=False` zachová v souboru českou diakritiku.

Co má vyjít: šest až deset testovacích případů v `vystup/contact_us.json` a případně pár otázek. Typická otázka je třeba „Jaká je maximální délka pole Comments?“. Požadavky ji neuvádějí, a model si ji tedy nemá vymýšlet.

### Krok 6: Teplota a opakovatelnost

**Temperature** (teplota) řídí, jak náhodně model vybírá další token. Při nízké teplotě volí téměř vždy nejpravděpodobnější pokračování. Při vysoké teplotě zkouší i méně pravděpodobná slova, takže je výstup pestřejší a méně předvídatelný. Parametr **top_p** omezuje výběr jen na nejpravděpodobnější tokeny, jejichž pravděpodobnosti dají dohromady hodnotu `top_p`.

Bruno v L52 nastaví `temperature=0.1` a `top_p=1.0`, aby AI návrhy kódu vycházely konzistentně. Pro generování testovacích případů do regresní sady chceš totéž. Pro brainstorming neobvyklých scénářů naopak může vyšší teplota pomoct.

Nízká teplota ale nezaručuje stejný výsledek. Sylabus v oddílu 3.1.4 mluví o **non-deterministic behaviour** (nedeterministické chování). I při teplotě 0 se odpovědi mezi voláními mohou lišit, protože výpočty na serveru nejsou bit po bitu stejné a poskytovatel model průběžně aktualizuje. OpenAI k tomu nabízí parametr `seed`, který opakovatelnost zlepšuje, ale také ji nezaručuje (neověřeno).

Některé novější modely teplotu vůbec nepřijímají. U OpenAI to platí pro část uvažujících (reasoning) modelů. U aktuálních modelů Claude od Anthropicu vrací API od 21. 10. 2026 chybu, pokud `temperature` nebo `top_p` pošleš. Opakovatelnost se tam řeší jinak: přesným promptem, strukturovaným výstupem a kontrolou výsledku.

Vyzkoušej to měřením. Skript `porovnej_behy.py` spustí generování třikrát a porovná, které testovací případy se objevily ve všech bězích (neověřeno spuštěním):

```python
from generuj_tc import generuj

def otisk(pripady):
    """Porovnáváme očekávané výsledky a techniky, ne přesné formulace kroků."""
    return {(tc["technika"].lower(), tc["ocekavany_vysledek"]) for tc in pripady}

for teplota in (0.0, 1.0):
    behy = [otisk(generuj("pozadavky/contact_us.md", teplota)["pripady"]) for _ in range(3)]
    spolecne = set.intersection(*behy)
    vsechny = set.union(*behy)
    print(f"teplota {teplota}: počty {[len(b) for b in behy]}, ve všech bězích {len(spolecne)} z {len(vsechny)}")
```

Při teplotě 0 by měl být podíl společných případů výrazně vyšší než při teplotě 1. Šest volání stojí jednotky centů. Výsledek si zapiš, použiješ ho ve cvičení 2.

### Krok 7: Tokeny, `max_tokens` a cena

Každá odpověď nese objekt `usage` se třemi čísly. `prompt_tokens` je počet tokenů na vstupu, tedy systémový prompt, uživatelský prompt a schéma. `completion_tokens` je počet tokenů odpovědi. `total_tokens` je jejich součet. Platíš za obojí, výstupní tokeny bývají několikanásobně dražší než vstupní.

Cenu spočítáš jednoduchou funkcí. Ceny za milion tokenů si vezmi z ceníku a ulož do `.env` nebo konfigurace, protože se mění častěji než kód:

```python
def cena(input_tokens: int, output_tokens: int, cena_in_1m: float, cena_out_1m: float) -> float:
    return input_tokens / 1_000_000 * cena_in_1m + output_tokens / 1_000_000 * cena_out_1m

# příklad s fiktivními cenami 1 USD / 4 USD za milion: 1 000 + 1 500 tokenů = 0,007 USD
```

Pro odhad velikosti: česky psaný text má víc tokenů na slovo než anglický. Diakritika a dlouhá slova se dělí na víc kusů. Systémový prompt a schéma posíláš s každým voláním znovu. Když generuješ testovací případy pro sto formulářů, zaplatíš je stokrát.

Tři pravidla pro rozumnou cenu:

1. `max_tokens` nastav podle očekávané délky odpovědi s rezervou. Je to pojistka proti zacyklení, ne nástroj kvality.
2. Na hromadné generování zkus nejdřív menší a levnější model a porovnej kvalitu na vzorku. Oddíl 5.1.3 sylabu popisuje výběr modelu přesně tímto způsobem.
3. Sleduj útratu v přehledu Usage na platform.openai.com. Bruno v L35 ukazuje, že pár desítek volání sníží kredit jen nepatrně. Chyba v cyklu ho ale vyčerpá rychle.

### Krok 8: AI jako pomocník pro testovací data (L15–L16)

Bruno začíná jednodušší úlohou. Má program `login_test.py` se třemi napevno zapsanými kombinacemi jména a hesla. V ChatGPT se zeptá, jak automaticky generovat pestřejší případy, a vloží svůj kód. AI vrátí funkci `generate_test_cases()`, která přidá prázdná pole, příliš dlouhé řetězce, speciální znaky a hodnoty `None`. Podstatný kus:

```python
def generate_random_string(length, include_special_chars=False):
    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

test_cases.append({"username": generate_random_string(100), "password": "securePass123"})  # dlouhé jméno
test_cases.append({"username": None, "password": None})                                    # None hodnoty
```

Při revizi takového kódu hledej tři věci. Za prvé, náhodná data bez `random.seed(...)` dávají při každém běhu jiný vstup. Když test jednou selže, chybu nezopakuješ. Za druhé, AI přidala případy, ale k nim žádný očekávaný výsledek. Program jen vypisuje „Login failed“. Bez očekávaného výsledku to není test, ale ukázka. Za třetí, Bruno správně upozorňuje, že do chatu vložil kód bez skutečných přihlašovacích údajů. Kód s reálnými hesly nebo připojovacími řetězci do veřejného modelu nepatří.

Vlastní vylepšení: místo náhodných dat ať model vygeneruje tabulku vstupů a očekávaných výsledků jako JSON se schématem podobným kroku 5. Tabulku pak čte parametrizovaný test (`pytest.mark.parametrize` nebo Scenario Outline v modulu 10). Data jsou pak opakovatelná, revidovatelná a verzovaná v gitu.

### Krok 9: Alternativy – lokální model a Anthropic API

Bruno v L36 zkouší open-source model GPT-Neo 2.7B přes knihovny `transformers` a `torch`. Ukázka sama varuje, ať ji nikdo neopakuje. Model má ke stažení přes 10 GB, kurz musel kvůli kompatibilitě snížit Python z 3.13 na starší verzi a doinstalovat Rust a Visual Studio. Odpověď trvala minuty a byla výrazně horší než z OpenAI. L37 to shrnuje srovnáním:

| Varianta | Výhody | Nevýhody |
|---|---|---|
| Cloudové API (OpenAI, Anthropic) | rychlé, kvalitní, bez nároků na hardware | platí se za tokeny, data opouštějí počítač |
| Lokální model přes aplikaci (GPT4All, Ollama) | data zůstávají na počítači, zdarma | slabší kvalita menších modelů, nároky na RAM |
| Lokální model přímo v Pythonu (transformers) | plná kontrola | složitá instalace, velmi pomalé bez GPU |

Tabulka platí i dnes, jen lokální nástroje mezitím zjednodušily integraci. Nad rámec kurzu: **Ollama** a GPT4All umí spustit lokální server s rozhraním kompatibilním s OpenAI API. Stejný kód z kroku 5 pak stačí přesměrovat (neověřeno, `json_schema` nemusí lokální server podporovat, začni s `json_object`):

```python
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")   # Ollama, klíč se nekontroluje
```

Lokální model je jediná z těchto variant, u které data neopouštějí počítač. Podrobně se lokálním modelům věnuje modul 2. Ani tak do něj ale nevkládej klientská data bez schválení. Licence modelu, umístění a ochrana dat jsou pořád věcí firmy.

Druhá alternativa je **Anthropic API** s modely Claude. Princip je stejný, liší se názvy parametrů. Knihovna se jmenuje `anthropic`, klíč čte z proměnné `ANTHROPIC_API_KEY` a systémový prompt je samostatný parametr `system` (neověřeno spuštěním):

```python
import anthropic

client = anthropic.Anthropic()                       # klíč z ANTHROPIC_API_KEY
zprava = client.messages.create(
    model="claude-opus-5-5",                         # levnější varianta: claude-haiku-5-5
    max_tokens=4000,
    system=SYSTEM,
    messages=[{"role": "user", "content": user_prompt(pozadavky)}],
)
text = "".join(b.text for b in zprava.content if b.type == "text")
print(zprava.usage.input_tokens, zprava.usage.output_tokens)
```

Odpověď je seznam bloků, ne jeden řetězec. Proto se text skládá z bloků typu `text`. Strukturovaný výstup nabízí metoda `client.messages.parse()` s modelem Pydantic. `temperature` u aktuálních modelů Claude neposílej, API ji odmítne. Ceník k říjnu 2026 uvádí pro Claude Opus 5.5 4 USD za milion vstupních a 20 USD za milion výstupních tokenů, pro Claude Haiku 5.5 0,10 a 0,50 USD. Před použitím ceny ověř.

## Ověření

Hotovo máš, když platí všechny body:

1. `git status` ani `git check-ignore -v .env` neukazuje `.env` jako soubor k commitu. Příkaz `git check-ignore` má vypsat řádek z `.gitignore`.
2. `python prvni_volani.py` vypíše odpověď a počet tokenů. V kódu nikde není řetězec klíče. Ověříš to vyhledáním začátku klíče v projektu: `Select-String -Path *.py -Pattern "sk-"` nesmí nic najít.
3. `python generuj_tc.py` vytvoří `vystup/contact_us.json` a funkce `validuj` neohlásí chybu.
4. Ve výstupu je aspoň jeden případ pro každé povinné pole, jeden pro neplatný e-mail a jeden pro RESET. To zkontroluj ručně. Validace hlídá strukturu, ne pokrytí.
5. Očekávané výsledky obsahují přesné texty z požadavků („Thank You for your Message!“). Pokud model napsal jiný text, je to halucinace a prompt potřebuje úpravu.
6. `python porovnej_behy.py` vypíše pro teplotu 0 vyšší podíl společných případů než pro teplotu 1.

Část bez sítě (validace, výpočet ceny) je ověřená skriptem `zdroje/_pracovni/bruno/over_offline.py` na Pythonu 3.12.10. Volání API v tomto modulu jsem nespouštěl.

## Časté chyby

**`AuthenticationError` (401).** Skript nenačetl `.env`, protože běží z jiného adresáře, nebo chybí `load_dotenv()`. Funkce `load_dotenv()` hledá `.env` od aktuálního pracovního adresáře výš. Spouštěj skripty z kořene projektu.

**`RateLimitError` (429) hned při prvním volání.** Na účtu není kredit. Předplatné ChatGPT Plus se na API nepřenáší.

**Model neexistuje (404).** Starý název z kurzu (`gpt-3.5-turbo`) nebo překlep. Seznam dostupných modelů vypíše `client.models.list()`.

**`json.JSONDecodeError`.** Odpověď se uřízla (`finish_reason == "length"`), nebo model přidal text kolem JSON. Použij `response_format` a kontrolu `finish_reason`.

**Výstup se mezi běhy liší, i když se prompt nezměnil.** To je nedeterminismus, ne chyba kódu. Sniž teplotu, zpřesni prompt a porovnávej obsah testovacích případů, ne jejich formulace.

**Model vrací hlášky, které na stránce nejsou.** Model nezná stránku, zná jen prompt. Do požadavků zapiš přesné texty a v systémovém promptu zakaž domýšlení.

**Klíč v historii gitu.** Smazání souboru nestačí, historie ho dál obsahuje. Klíč okamžitě zruš na platform.openai.com.

**Commitnutý `.venv`.** Repozitář má stovky megabajtů a na jiném počítači stejně nefunguje. Přidej `.venv/` do `.gitignore` dřív, než poprvé spustíš `git add`.

## Cvičení

:::cviceni nazev="Login Portal místo Contact Us"
Cíl: ověřit, že skript funguje pro jinou testovací bázi beze změny kódu. Napiš `pozadavky/login.md` pro stránku Login Portal na webdriveruniversity.com (Bruno ji používá v L7 a L8). Spusť `python generuj_tc.py pozadavky/login.md`.
Hotovo: soubor s testovacími případy projde validací, kód skriptu ses nedotkl a aspoň jedna položka v `otazky` upozorňuje na něco, co požadavky neříkají (například blokace účtu po opakovaných pokusech).
:::

:::cviceni nazev="Změř opakovatelnost"
Cíl: mít čísla místo dojmu. Spusť `porovnej_behy.py` pro teploty 0, 0,7 a 1,2, vždy pětkrát. Zapiš do tabulky počet případů v každém běhu a podíl případů společných všem během.
Hotovo: tabulka se třemi řádky a jednou větou závěru, jakou teplotu použiješ pro regresní sadu a proč. Celková cena pokusu (součet z `usage`) je pod 0,20 USD.
:::

:::cviceni nazev="Recenze výstupu podle metrik"
Cíl: procvičit hodnocení výstupu z oddílu 2.3. Vezmi jeden vygenerovaný soubor a ke každému testovacímu případu ručně zapiš, zda je správný (odpovídá požadavkům), relevantní (testuje něco z požadavků) a nový (neopakuje jiný případ).
Hotovo: máš podíl správných, relevantních a duplicitních případů. Podle nejčastější chyby jsi upravil systémový prompt, spustil generování znovu a čísla se zlepšila.
:::

## Souvislost se sylabem CT-GenAI

Modul převádí do kódu to, co kapitola 2 popisuje jako práci s promptem. Rozdělení na systémovou a uživatelskou zprávu odpovídá oddílu 2.1.3 (systémový a uživatelský prompt). Struktura systémového promptu s rolí, pravidly a tvarem výstupu odpovídá komponentám z oddílu 2.1.1. Generování testovacích případů z požadavků je přímo úloha z oddílu 2.2.2 (návrh testů a implementace testování s GenAI). Ruční recenze v cvičení 3 používá metriky z oddílu 2.3.1 a postupné ladění promptu z oddílu 2.3.2.

Kapitola 3 je ve skriptu všude. Pravidlo „nedomýšlej si“, pole `otazky` a kontrola přesných hlášek míří na halucinace z oddílu 3.1.1 a jejich odhalování z oddílu 3.1.2. Pokus s teplotou je praktická ukázka nedeterministického chování z oddílu 3.1.4. Uložení klíče mimo kód a zákaz klientských dat odpovídají rizikům a opatřením z oddílů 3.2.1 a 3.2.3.

Srovnání cloudového API, lokálního modelu a různě velkých modelů podle ceny a kvality je praktická verze výběru LLM nebo SLM z oddílu 5.1.3. Varování před osobním klíčem pro firemní práci odpovídá oddílu 5.1.1 o stínové AI.
