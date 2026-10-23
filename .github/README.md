# Akademie GenAI – příprava na ISTQB CT-GenAI v češtině

Neoficiální česká studijní příručka k certifikaci **ISTQB Certified Tester Testing with Generative AI
(CT-GenAI)**, sylabus v1.1. Výklad je česky, termíny anglicky.

**Web:** https://jancerny-dev.github.io/Academie-GenAI/

Na webu je:
- výklad 5 kapitol sylabu, plný a zkrácený,
- slovník a kartičky,
- přiřazovací a praktická cvičení,
- sekce Praxe s návody k AI nástrojům v testování,
- Sample Exam A, cvičné zkoušky a procvičování.

## Postup a přihlášení

Web funguje bez přihlášení, postup se pak ukládá v prohlížeči. Kdo se přihlásí Google účtem,
má postup uložený ve Firebase (Firestore, region EU) a vidí ho na všech zařízeních.
Ukládá se jen postup na webu. Podrobnosti jsou na stránce [Zdroje](https://jancerny-dev.github.io/Academie-GenAI/zdroje.html#ucet).

## Struktura

```
obsah/      výklad kapitol a modulů Praxe (Markdown)
data/       slovník, cvičení, přiřazování, vlastní cvičné otázky, Sample Exam A
tools/      generátor webu (Python 3.10+, jen standardní knihovna), popis v tools/README.md
web/        vygenerovaný web, publikuje ho .github/workflows/pages.yml
firebase/   pravidla Firestore
```

```bash
python tools/build_site.py
python tools/check_site.py
```

## Autorská práva

Web není produktem ISTQB®. ISTQB® je registrovaná ochranná známka International Software Testing
Qualifications Board. Texty jsou vlastním zpracováním autora. Otázky z placených kurzů v repozitáři nejsou.
Kód v `tools/` je pod licencí MIT, na textový obsah se nevztahuje.
