# Generátor webu CT-GenAI

Statický web se studijními materiály k ISTQB CT-GenAI. Navazuje na web CTFL
(`Desktop\OSOBNÍ\projekty\ISTQB`): stejný vzhled, stejné principy, převzaté `styl.css`,
`skript.js`, `zkouska.js`, `prirazovani.js` a `procvicovani.js`. Datový kontrakt je
v `../PRAVIDLA_ZPRACOVANI.md` (kap. 4–7).

## Spuštění

```bash
python tools/build_site.py              # obsah/ + data/  ->  web/
python tools/check_site.py              # kontrola web/; návratový kód 0 = OK, 1 = chyby

python tools/_testdata/vytvor.py        # (znovu) vytvoří malá ukázková data
python tools/build_site.py --testdata   # tools/_testdata/  ->  tools/_testdata/web/
python tools/check_site.py --testdata
```

Jen standardní knihovna Pythonu 3.10+. Web funguje i otevřený z disku dvojklikem
(`web/index.html`): relativní cesty, žádný fetch, data jako `.js` s `window.X = …`.

Generátor bere, co zrovna existuje. Chybějící kapitolu, slovník nebo otázky vynechá
a vypíše varování. Neplatné záznamy (otázka bez `cz`, špatné `spravne`…) vynechá
s varováním; `check_site.py` je hlásí jako chyby.

## Struktura

```
tools/
  build_site.py     generátor: kapitoly, úvod, slovník, kartičky, přiřazování, cvičení, cíle, zdroje
  zkousky.py        zkoušky: Sample Exam A (+ dodatkové otázky), cvičné zkoušky, náhodná zkouška,
                    procvičování, lokální část web/lokalni/ (Udemy)
  otazky.py         kontrola otázek, převod pro web, skládání zkoušek podle rozpisu, míchání možností
  obsah.py          načtení obsah/kapitola-N/{vyklad,zkracena}.md, mapa oddílů pro odkazy
  praxe.py          sekce Praxe: obsah/praxe/*.md -> web/praxe/*.html, rozcestník web/praxe.html
  markdown_min.py   vlastní minimální převod Markdownu (h2/h3, seznamy, tabulky, ```kód, :::bloky)
  rozvrzeni.py      hlavička, navigace, patička, kostra stránky
  konfig.py         konstanty, cesty, rozpis zkoušky
  lo.json           studijní cíle, K-úrovně a počty otázek (sylabus v1.1, Exam Structures v1.19)
  check_site.py     kontrola invariantů
  assets/           statické CSS a JS, kopírují se do web/assets/
  _testdata/        ukázková data stejného formátu + vytvor.py
```

## Invarianty (`check_site.py`)

| # | Invariant |
|---|---|
| 1 | Každý zdrojový `.md` má svou stránku |
| 2 | **Počet slov na stránce odpovídá zdroji.** Zdroj se počítá odstraněním značek, stránka z HTML; dva nezávislé výpočty. Slovo = token s písmenem nebo číslicí. |
| 3 | Každý h2 má kotvu a je v bočním obsahu |
| 4 | Všechny vnitřní odkazy a kotvy vedou někam (i odkazy do výkladu v datech otázek a slovníku) |
| 5 | Odkazované CSS a JS existují; každá třída z HTML má pravidlo v CSS |
| 6 | Každá otázka má platné `spravne`, `en` i `cz` stejný počet možností a LO z rozpisu (zdroj i vygenerovaná data) |
| 7 | Cvičné zkoušky: 40 otázek, 46 bodů, počty po LO přesně podle rozpisu; varování při nerovnoměrném rozložení a–d |
| 8 | **Žádný soubor mimo `web/lokalni/` neobsahuje id ani text otázek z `data/udemy/`** (texty, které jsou doslova v Sample Exam A, se nehlásí) |
| 9 | Ve `web/` nejsou PDF, DOCX, PPTX ani ZIP |
| 10 | Praxe: každý `.md` v `obsah/praxe/` má stránku a kartu na `praxe.html`, počet slov sedí, h2 jsou v bočním obsahu, frontmatter má povinná pole (kap. 7b), `modul` sedí s názvem souboru, `kapitoly` existují, každé cvičení má kotvu a zaškrtávátko, nezůstal žádný odkaz `modul:` |

## Praxe

- Moduly `obsah/praxe/NN-slug.md` (formát v PRAVIDLA, kap. 7b), k tomu `tahak.md` (modul 0) a `projekt.md` (modul 99).
  Generátor bere, co ve složce zrovna je; chybějící moduly nevadí.
- Bloky navíc: `:::pozor`, `:::krok` (číslují se v CSS), `:::cviceni nazev="…"` (karta se zaškrtávátkem Hotovo).
  Všechny tři berou volitelný `nazev="…"`. Id cvičení je `praxe-<soubor>-<slug názvu>`, stav v localStorage
  `genai-praxe-hotovo`. Text „Hotovo“ nese `data-nepocitat`, kontrola slov ho přeskočí.
- Skupina na rozcestníku: pole `skupina:` (`chat`, `ide`, `python`, `ci` nebo celý název), jinak podle prvního
  nástroje v poli `nastroje`, který patří některé skupině (`PRAXE_SKUPINY` v `konfig.py`).
- Odkaz na jiný modul: `[text](modul:klicove-slovo)`. Hledá se v názvu souboru, pak v názvu modulu, pak v nástrojích.
  Když modul zatím není, vykreslí se jen text.

## Zkoušky

- **Rozpis** (`lo.json`): každý LO má pevný počet otázek (1.1.2, 2.1.1, 3.2.2 po dvou, ostatní po jedné),
  K3 = 2 body, celkem 40 otázek a 46 bodů, hranice 30 bodů.
- **Cvičné zkoušky** z `data/cvicne-otazky/`: tolik úplných zkoušek, kolik dovolí nejslabší LO.
  Výběr je deterministický (seed 2026). Možnosti se míchají tak, aby správná odpověď byla rovnoměrně
  mezi a–d; nemíchá se u `keep_order`, u výběru více možností a u textu, který odkazuje na písmeno
  nebo pořadí („option a“, „all of the above“, „možnost b“).
- **Sample Exam A** beze změny pořadí. Dodatkové otázky (`navic: true`, typ `razeni` / `prirazeni`)
  jsou na samostatné stránce a do 40/46 se nepočítají.
- **Jazyk**: English, Česky, English + skrytý český překlad (`?jazyk=en|cz|encz`).
- **localStorage** (prefix `genai-`, aby se nemíchal s CTFL): `genai-zkouska-<sada>` rozpracovaný test,
  `genai-zkousky-vysledky` souhrn a historie, `genai-lo-vysledky` úspěšnost po LO (zkoušky a procvičování),
  `genai-cile`, `genai-karticky`, `genai-prirazovani-v1`, `genai-cviceni-hotovo`; lokální část `genai-lokalni-…`.

## Lokální část (Udemy)

`data/udemy/*.json` (formát `{"popis", "zdroj", "testy": [{"nazev", "otazky"}]}`, nebo jen `"otazky"`)
se zpracuje do `web/lokalni/`: každý test jako zkouška, mix podle rozpisu a procvičování.
Odkaz v menu se objeví jen tehdy, když data existují. Složka je v `.gitignore` a každá
její stránka nese upozornění „Jen pro osobní studium, nepublikovat“.

## Přihlášení Google účtem (Firebase)

Web funguje bez přihlášení, postup je v `localStorage`. Volitelně se lze přihlásit Google účtem
a postup se ukládá i do Firebase, takže je na všech zařízeních a přežije smazání historie.

- `assets/ucet-konfig.js`: `window.GENAI_FIREBASE = {apiKey, authDomain, projectId, appId}` z Firebase konzole
  (Project settings → Your apps → Web app). Hodnoty nejsou tajné. Dokud je tam `null`, tlačítko Přihlásit se neukáže.
- `assets/ucet.js`: přihlášení (Firebase Auth SDK z gstatic, verze v `VERZE_SDK`) a synchronizace.
  Zachytává `localStorage.setItem/removeItem` u klíčů `genai-*` a ukládá čas změny (`genai-ucet-casy`).
  Ve Firestore je dokument `uzivatele/{uid}` s poli `stav` a `casy` (JSON text) a `upraveno`; volá se přes REST.
  U každého klíče vyhrává novější změna, klíče bez času (postup z doby před prvním přihlášením) se slučují po položkách.
  Neukládá se `genai-lokalni-*` ani `genai-ucet-*`. Na `file://` přihlášení nejde (Google ho nedovolí), web běží jen lokálně.
- `../firebase/firestore.rules`: pravidla Firestore, vložit v konzoli (Firestore → Rules → Publish).
- Ruční „splněno“: tlačítko `[data-splneno]` pod kapitolou a modulem Praxe (`rozvrzeni.tlacitko_splneno`),
  stav `genai-splneno` (`kapitola-N-varianta`, `modul-<soubor>`). Přehled postupu je na `index.html#postup`.

Nastavení Firebase (jednou): projekt pod osobním Google účtem bez Analytics → Web app → Authentication →
Google → Enable → Authorized domains: `jancerny-dev.github.io` → Firestore v `europe-west3`, production mode →
pravidla z `firebase/firestore.rules`.

## Nasazení

`.github/workflows/pages.yml` publikuje složku `web/` na GitHub Pages (Settings → Pages →
GitHub Actions). CI web jen publikuje, nepřegenerovává ho. Před `git push` vždy
`build_site.py` a `check_site.py`.
