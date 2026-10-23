---
modul: 1
nazev: Ukázkový modul v chatu (testovací data)
podtitul: Prověří bloky Praxe, odkazy na kapitoly a sousední moduly.
cas: 1–2 h
uroven: začátečník
nastroje: ChatGPT, NotebookLM
kapitoly: 1, 2
zdroje: Shetty L3–L13; Bruno L6–L13
---

## Co postavíš
Odstavec s **tučným** textem a odkazem na [Python modul](modul:ukazka-python) i na [tahák](modul:tahak).
Odkaz na [neexistující modul](modul:neexistuje) se vykreslí jen jako text.

## Předpoklady
:::pozor nazev="Žádná firemní data"
Do veřejného chatbota nevkládej klientská data. API klíč patří do proměnné prostředí.
:::

## Postup
### 1. Otevři chatbot
:::krok
Přihlas se a otevři nový chat.
:::

:::krok nazev="Vlož prompt"
Zkopíruj prompt tlačítkem Kopírovat.

```text
You are a test analyst. Derive test conditions for the Contact Us form.
```
:::

### 2. Zkontroluj výstup
| Metrika | Co měří |
|---|---|
| recall | pokrytí požadavků |

## Cvičení
:::cviceni nazev="Testovací podmínky pro formulář"
Cíl: deset podmínek. **Hotovo**, když každá odkazuje na požadavek.
:::

:::cviceni nazev="Porovnání dvou promptů"
Porovnej zero-shot a few-shot.
:::

## Souvislost se sylabem CT-GenAI
Kapitola 2, oddíl 2.3.1.
