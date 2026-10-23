# -*- coding: utf-8 -*-
"""Společné části stránky: hlavička s navigací, patička a kostra HTML (podle webu CTFL)."""

from __future__ import annotations

import html
import json
from pathlib import Path

from konfig import KAPITOLY, NAZEV_WEBU, PODNAZEV_WEBU, PREFIX


def e(text) -> str:
    return html.escape(str(text), quote=False)


def a(text) -> str:
    return html.escape(str(text), quote=True)


def tlacitko_splneno(id_: str, ne: str = "Označit jako prostudované", ano: str = "✓ Prostudováno") -> str:
    """Ruční „splněno“ (stav genai-splneno, obsluhuje skript.js). Stojí mimo #text, slova se nepočítají."""
    return (f'<div class="splneno-radek" data-nepocitat><button type="button" class="tlacitko splneno" '
            f'data-splneno="{a(id_)}" data-text-ne="{a(ne)}" data-text-ano="{a(ano)}" aria-pressed="false">'
            f'{e(ne)}</button></div>')


class Web:
    """Stav sestavení sdílený stránkami: co existuje, kam odkazovat."""

    def __init__(self, vystup: Path, dokumenty: dict, lokalni: bool):
        self.vystup = vystup
        self.dokumenty = dokumenty
        self.lokalni = lokalni

    def cil_kapitoly(self, k: int, varianta: str = "vyklad") -> str | None:
        for v in (varianta, "vyklad", "zkracena"):
            if (k, v) in self.dokumenty:
                return f"kapitola-{k}/{v}.html"
        return None

    def zapis(self, relativni: str, obsah: str) -> None:
        cil = self.vystup / relativni
        cil.parent.mkdir(parents=True, exist_ok=True)
        cil.write_text(obsah, encoding="utf-8")

    def zapis_js(self, relativni: str, promenna: str, data, puvod: str) -> None:
        js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        self.zapis(relativni, f"/* Vygenerováno z {puvod}, neupravovat ručně. */\nwindow.{promenna} = {js};\n")

    # --- kostra -----------------------------------------------------------

    def hlavicka(self, koren: str, aktivni: str, varianta: str, aktivni_kapitola: int | None) -> str:
        def odkaz(cil: str, popisek: str, klic: str, trida: str = "") -> str:
            aktualni = ' aria-current="page"' if klic == aktivni else ""
            t = f' class="{trida}"' if trida else ""
            return f'<a href="{koren}{cil}"{t}{aktualni}>{popisek}</a>'

        polozky = []
        for k in sorted(KAPITOLY):
            cil = self.cil_kapitoly(k, varianta)
            if not cil:
                continue
            aktualni = ' aria-current="page"' if k == aktivni_kapitola else ""
            polozky.append(f'<li><a href="{koren}{cil}"{aktualni}><b>{k}</b> {e(KAPITOLY[k]["kratce"])}</a></li>')
        podmenu = (f'<ul class="podmenu" id="podmenu-kapitoly" aria-label="Seznam kapitol">{"".join(polozky)}</ul>'
                   if polozky else "")
        # Lokální část se nepublikuje: odkaz je skrytý a skript.js ho ukáže jen na disku a na localhostu.
        lokalni = (odkaz("lokalni/index.html", "Lokální testy", "lokalni", "lokalni-odkaz")
                   .replace("<a ", "<a data-jen-lokalne hidden ", 1) if self.lokalni else "")
        return f"""<a class="preskocit" href="#text">Přeskočit na text</a>
<div class="postup" aria-hidden="true"></div>
<header class="hlavicka">
  <div class="hlavicka-vnitrek">
    <a class="znacka" href="{koren}index.html">{NAZEV_WEBU} <span>{PODNAZEV_WEBU}</span></a>
    <nav class="navigace" aria-label="Hlavní navigace">
      {odkaz('index.html', 'Úvod', 'uvod')}
      <span class="skupina" data-skupina>
        {odkaz('kapitoly.html', 'Kapitoly', 'kapitoly', 'zvyraznit')}
        {podmenu}
      </span>
      {odkaz('slovnik.html', 'Slovník', 'slovnik')}
      {odkaz('karticky.html', 'Kartičky', 'karticky')}
      {odkaz('prirazovani.html', 'Přiřazování', 'prirazovani')}
      {odkaz('cviceni.html', 'Cvičení', 'cviceni')}
      {odkaz('praxe.html', 'Praxe', 'praxe')}
      {odkaz('cile.html', 'Cíle', 'cile')}
      {odkaz('zkouska.html', 'Zkouška', 'zkouska')}
      {lokalni}
      <button type="button" class="prepinac-tema" data-prepinac-tema>Tmavý režim</button>
      <button type="button" class="ucet-tlacitko" data-ucet hidden>Přihlásit</button>
    </nav>
  </div>
</header>"""

    def paticka(self, koren: str) -> str:
        return f"""<footer class="paticka">
  <div class="paticka-vnitrek">
    <p><strong>Neoficiální studijní materiál.</strong> Tento web není produktem ani publikací ISTQB®.
    ISTQB® je registrovaná ochranná známka International Software Testing Qualifications Board.
    Texty jsou vlastním zpracováním autora vytvořeným při přípravě na zkoušku CT-GenAI; oficiální sylabus
    a vzorovou zkoušku si stáhněte přímo na istqb.org.</p>
    <p>Ke zkoušce vždy platí znění oficiálního sylabu CT-GenAI v1.1. Doplněné informace a příklady z praxe
    slouží k porozumění, nikoli jako zdroj správných odpovědí u zkoušky.</p>
    <ul>
      <li><a href="https://istqb.org/certifications/gen-ai/" target="_blank" rel="noopener noreferrer">ISTQB — CT-GenAI</a></li>
      <li><a href="https://glossary.istqb.org" target="_blank" rel="noopener noreferrer">Slovník ISTQB</a></li>
      <li><a href="https://casqb.org" target="_blank" rel="noopener noreferrer">CaSQB</a></li>
      <li><a href="{koren}zdroje.html">Zdroje a autorská práva</a></li>
    </ul>
  </div>
</footer>"""

    def stranka(self, *, titulek: str, popis: str, telo: str, koren: str = "", aktivni: str = "",
                kapitola: int | None = None, varianta: str = "vyklad", skripty: list[str] | None = None,
                atributy_body: str = "") -> str:
        atr = f' data-kapitola="{kapitola}"' if kapitola else ""
        skripty_html = "".join(f'\n<script src="{koren}{s}"></script>' for s in (skripty or []))
        return f"""<!doctype html>
<html lang="cs" data-tema="">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulek)}</title>
<meta name="description" content="{a(popis)}">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="{koren}assets/styl.css">
<script>
/* Nastaví uložený režim ještě před vykreslením, aby stránka neproblikla. */
(function(){{try{{var t=localStorage.getItem('{PREFIX}tema');if(t){{document.documentElement.setAttribute('data-tema',t);}}}}catch(e){{}}}})();
</script>
</head>
<body{atr}{atributy_body}>
{self.hlavicka(koren, aktivni, varianta, kapitola)}
{telo}
{self.paticka(koren)}
<script src="{koren}assets/ucet-konfig.js"></script>
<script src="{koren}assets/ucet.js"></script>
<script src="{koren}assets/skript.js"></script>{skripty_html}
</body>
</html>
"""
