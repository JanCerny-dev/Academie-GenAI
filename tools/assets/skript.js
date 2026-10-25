/* ISTQB CT-GenAI — česká studijní příručka (převzato z webu CTFL a upraveno)
   Bez závislostí a bez modulů, aby stránka fungovala i po otevření z disku. */

(function () {
  "use strict";

  var PREFIX = "genai-";
  var KLIC_TEMA = PREFIX + "tema";
  var KLIC_CVICENI = PREFIX + "cviceni-hotovo";
  var KLIC_PRAXE = PREFIX + "praxe-hotovo";
  var KLIC_SPLNENO = PREFIX + "splneno";

  function uloz(klic, hodnota) {
    try { localStorage.setItem(klic, hodnota); } catch (e) { /* soukromý režim */ }
  }

  function nacti(klic) {
    try { return localStorage.getItem(klic); } catch (e) { return null; }
  }

  /* --- světlý / tmavý režim ---------------------------------------------- */

  function systemJeTmavy() {
    return !!(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
  }

  /* Platný režim, ne jen ten uložený: bez vlastní volby rozhoduje systém. */
  function jeTmavy() {
    var volba = document.documentElement.getAttribute("data-tema");
    if (volba === "tmavy") return true;
    if (volba === "svetly") return false;
    return systemJeTmavy();
  }

  function nastavTema() {
    var tlacitko = document.querySelector("[data-prepinac-tema]");
    if (!tlacitko) return;

    function popis() {
      var tmavy = jeTmavy();
      tlacitko.textContent = tmavy ? "☀ Světlý režim" : "☾ Tmavý režim";
      tlacitko.setAttribute("aria-label", tmavy ? "Přepnout na světlý režim" : "Přepnout na tmavý režim");
    }

    popis();

    tlacitko.addEventListener("click", function () {
      var nove = jeTmavy() ? "svetly" : "tmavy";
      document.documentElement.setAttribute("data-tema", nove);
      uloz(KLIC_TEMA, nove);
      popis();
    });

    if (window.matchMedia) {
      var dotaz = window.matchMedia("(prefers-color-scheme: dark)");
      var reakce = function () {
        if (!document.documentElement.getAttribute("data-tema")) popis();
      };
      if (dotaz.addEventListener) dotaz.addEventListener("change", reakce);
      else if (dotaz.addListener) dotaz.addListener(reakce);
    }
  }

  /* --- ukazatel postupu čtení -------------------------------------------- */

  function nastavPostup() {
    var pruh = document.querySelector(".postup");
    if (!pruh) return;
    /* Kde to prohlížeč umí, pruh kreslí CSS (animation-timeline) a stránka se při
       posunu vůbec nemění. Změny DOM při posunu zasekávají Číst nahlas v Edge. */
    if (window.CSS && CSS.supports && CSS.supports("animation-timeline: scroll()")) return;

    var ceka = false;
    function prekresli() {
      var vyska = document.documentElement.scrollHeight - window.innerHeight;
      var podil = vyska > 0 ? window.scrollY / vyska : 0;
      pruh.style.width = Math.min(100, Math.max(0, podil * 100)).toFixed(2) + "%";
      ceka = false;
    }

    window.addEventListener("scroll", function () {
      if (ceka) return;
      ceka = true;
      window.requestAnimationFrame(prekresli);
    }, { passive: true });

    prekresli();
  }

  /* --- zvýraznění aktivního oddílu v bočním obsahu ------------------------ */

  function nastavStrom() {
    var odkazy = Array.prototype.slice.call(document.querySelectorAll(".strom a[href^='#']"));
    if (!odkazy.length || !("IntersectionObserver" in window)) return;

    var podleId = {};
    var nadpisy = [];
    odkazy.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute("href").slice(1));
      var cil = document.getElementById(id);
      if (cil) { podleId[id] = a; nadpisy.push(cil); }
    });

    var viditelne = {};
    var posledni;

    /* Číst nahlas v Edge posouvá stránku samo a zastaví se, když se během čtení
       změní DOM. Obsah se proto přepíná jen při posunu, který udělal čtenář. */
    var vstup = 0, tlacitkoDole = false;
    ["wheel", "touchstart", "touchmove", "keydown", "click"].forEach(function (u) {
      window.addEventListener(u, function () { vstup = Date.now(); }, { passive: true, capture: true });
    });
    window.addEventListener("mousedown", function () { tlacitkoDole = true; vstup = Date.now(); }, true);
    window.addEventListener("mouseup", function () { tlacitkoDole = false; vstup = Date.now(); }, true);
    function posunulCtenar() { return tlacitkoDole || Date.now() - vstup < 2000; }

    function obnov(vzdy) {
      var aktivni = null;
      for (var i = 0; i < nadpisy.length; i++) {
        if (viditelne[nadpisy[i].id]) { aktivni = nadpisy[i]; break; }
      }
      if (!aktivni) {
        for (var j = nadpisy.length - 1; j >= 0; j--) {
          if (nadpisy[j].getBoundingClientRect().top < 120) { aktivni = nadpisy[j]; break; }
        }
      }
      if (aktivni === posledni) return;
      if (vzdy !== true && !posunulCtenar()) return;
      posledni = aktivni;
      odkazy.forEach(function (a) { a.classList.remove("aktivni"); });
      if (aktivni && podleId[aktivni.id]) podleId[aktivni.id].classList.add("aktivni");
    }

    var pozorovatel = new IntersectionObserver(function (zaznamy) {
      zaznamy.forEach(function (z) { viditelne[z.target.id] = z.isIntersecting; });
      obnov();
    }, { rootMargin: "-100px 0px -70% 0px", threshold: 0 });

    nadpisy.forEach(function (h) { pozorovatel.observe(h); });
    window.addEventListener("scroll", obnov, { passive: true });
    obnov(true);
  }

  /* --- tlačítko Kopírovat u bloků kódu (prompty do chatbota) -------------- */

  function zkopiruj(text, hotovo) {
    function zaloha() {
      var t = document.createElement("textarea");
      t.value = text;
      t.setAttribute("readonly", "");
      t.style.position = "fixed";
      t.style.opacity = "0";
      document.body.appendChild(t);
      t.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(t);
      hotovo(ok);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { hotovo(true); }, zaloha);
    } else {
      zaloha();
    }
  }

  function nastavKopirovani(koren) {
    (koren || document).querySelectorAll(".kod").forEach(function (blok) {
      if (blok.querySelector(".kod-kopirovat")) return;
      var kod = blok.querySelector("code");
      if (!kod) return;
      var tl = document.createElement("button");
      tl.type = "button";
      tl.className = "kod-kopirovat";
      tl.textContent = "Kopírovat";
      tl.setAttribute("aria-label", "Zkopírovat obsah bloku do schránky");
      tl.addEventListener("click", function () {
        zkopiruj(kod.textContent, function (ok) {
          tl.textContent = ok ? "Zkopírováno ✓" : "Nejde kopírovat";
          setTimeout(function () { tl.textContent = "Kopírovat"; }, 1800);
        });
      });
      blok.appendChild(tl);
    });
  }
  window.genaiKopirovani = nastavKopirovani;

  /* --- praktická cvičení: zaškrtnutí „hotovo“ ----------------------------- */

  function nastavCviceni() {
    var policka = document.querySelectorAll("[data-hotovo]");
    if (!policka.length) return;
    var stav;
    try { stav = JSON.parse(nacti(KLIC_CVICENI)) || {}; } catch (e) { stav = {}; }
    var souhrn = document.getElementById("cv-souhrn");

    function prepocti() {
      var hotovo = 0;
      policka.forEach(function (p) {
        if (p.checked) hotovo++;
        var karta = p.closest(".cv-karta");
        if (karta) karta.classList.toggle("cv-karta--hotovo", p.checked);
      });
      if (souhrn) souhrn.textContent = "Hotovo " + hotovo + " z " + policka.length + " cvičení.";
    }

    policka.forEach(function (p) {
      p.checked = !!stav[p.getAttribute("data-hotovo")];
      p.addEventListener("change", function () {
        if (p.checked) stav[p.getAttribute("data-hotovo")] = Date.now();
        else delete stav[p.getAttribute("data-hotovo")];
        uloz(KLIC_CVICENI, JSON.stringify(stav));
        prepocti();
      });
    });
    prepocti();
  }

  /* --- Praxe: cvičení „hotovo“ a postup po modulech ------------------------ */

  /* Stav je {id cvičení: čas zaškrtnutí}. Stránka modulu má zaškrtávátka
     [data-praxe-hotovo], rozcestník a souhrny mají [data-praxe-cviceni] se seznamem id. */
  function nastavPraxe() {
    var policka = document.querySelectorAll("[data-praxe-hotovo]");
    var prehledy = document.querySelectorAll("[data-praxe-cviceni]");
    if (!policka.length && !prehledy.length) return;
    var stav;
    try { stav = JSON.parse(nacti(KLIC_PRAXE)) || {}; } catch (e) { stav = {}; }

    function obnov() {
      [].forEach.call(policka, function (p) {
        var blok = p.closest(".vsuvka--cviceni");
        if (blok) blok.classList.toggle("praxe-cviceni--hotovo", p.checked);
      });
      [].forEach.call(prehledy, function (el) {
        var ids = (el.getAttribute("data-praxe-cviceni") || "").split(/\s+/).filter(Boolean);
        var cil = el.hasAttribute("data-praxe-postup") ? el : el.querySelector("[data-praxe-postup]");
        if (!cil || !ids.length) return;
        var hotovo = ids.filter(function (id) { return stav[id]; }).length;
        cil.textContent = "Hotovo " + hotovo + " z " + ids.length + " cvičení";
        if (el.classList.contains("karta")) el.classList.toggle("praxe-karta--hotovo", hotovo === ids.length);
      });
    }

    [].forEach.call(policka, function (p) {
      var id = p.getAttribute("data-praxe-hotovo");
      p.checked = !!stav[id];
      p.addEventListener("change", function () {
        if (p.checked) stav[id] = Date.now();
        else delete stav[id];
        uloz(KLIC_PRAXE, JSON.stringify(stav));
        obnov();
      });
    });
    obnov();
  }

  /* --- ruční „splněno“ u kapitol a modulů Praxe ---------------------------- */

  /* Stav je {id: čas označení}. Tlačítko [data-splneno] přepíná, odkazy
     [data-splneno-odkaz] na rozcestnících dostanou fajfku. */
  function nastavSplneno() {
    var tlacitka = document.querySelectorAll("[data-splneno]");
    var odkazy = document.querySelectorAll("[data-splneno-odkaz]");
    if (!tlacitka.length && !odkazy.length) return;
    var stav;
    try { stav = JSON.parse(nacti(KLIC_SPLNENO)) || {}; } catch (e) { stav = {}; }

    function obnov() {
      [].forEach.call(tlacitka, function (b) {
        var ano = !!stav[b.getAttribute("data-splneno")];
        b.setAttribute("aria-pressed", String(ano));
        b.textContent = b.getAttribute(ano ? "data-text-ano" : "data-text-ne");
        b.title = ano ? "Kliknutím označení zrušíš" : "";
      });
      [].forEach.call(odkazy, function (a) {
        a.classList.toggle("splneno-odkaz--ano", !!stav[a.getAttribute("data-splneno-odkaz")]);
      });
    }

    [].forEach.call(tlacitka, function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-splneno");
        if (stav[id]) delete stav[id];
        else stav[id] = Date.now();
        uloz(KLIC_SPLNENO, JSON.stringify(stav));
        obnov();
      });
    });
    obnov();
  }

  /* --- přehled postupu na úvodní stránce ----------------------------------- */

  function nastavPrehled() {
    var radky = document.querySelectorAll("[data-prehled]");
    if (!radky.length) return;

    function json(klic) {
      try { return JSON.parse(nacti(klic)) || {}; } catch (e) { return {}; }
    }
    function hodnoty(o) { return Object.keys(o).map(function (k) { return o[k]; }); }

    var spocti = {
      splneno: function (ids) { var s = json(KLIC_SPLNENO); return [ids.filter(function (i) { return s[i]; }).length, ids.length]; },
      mapa: function (ids, el) { var s = json(el.getAttribute("data-klic")); return [ids.filter(function (i) { return s[i]; }).length, ids.length]; },
      prirazovani: function (ids, el, celkem) {
        var s = json(PREFIX + "prirazovani-v1").sady || {};
        return [hodnoty(s).filter(function (z) { return z && z.nejlepe >= 100; }).length, celkem];
      },
      karticky: function (ids, el, celkem) {
        var s = json(PREFIX + "karticky").prihradky || {};
        return [hodnoty(s).filter(function (b) { return b >= 5; }).length, celkem];
      },
      cile: function (ids, el, celkem) {
        return [hodnoty(json(PREFIX + "cile")).filter(function (h) { return h === 2; }).length, celkem];
      },
      zkousky: function () {
        var z = hodnoty(json(PREFIX + "zkousky-vysledky")).filter(function (x) { return x && x.celkem; });
        return [z.filter(function (x) { return x.nejlepe >= x.hranice; }).length, z.length];
      }
    };

    [].forEach.call(radky, function (el) {
      var typ = el.getAttribute("data-prehled");
      if (!spocti[typ]) return;
      var ids = (el.getAttribute("data-ids") || "").split(/\s+/).filter(Boolean);
      var celkem = +el.getAttribute("data-celkem") || 0;
      var v = spocti[typ](ids, el, celkem), hotovo = v[0], z = v[1];
      var hodnota = el.querySelector("[data-hodnota]");
      hodnota.textContent = typ === "zkousky"
        ? (z ? hotovo + " z " + z + " vyzkoušených" : "zatím žádná")
        : hotovo + " z " + z;
      var pruh = el.querySelector(".prehled-pruh span");
      if (pruh) pruh.style.width = (z ? Math.round(hotovo / z * 100) : 0) + "%";
      el.classList.toggle("prehled--hotovo", z > 0 && hotovo === z);
    });
  }

  /* --- podmenu kapitol ---------------------------------------------------- */

  function nastavPodmenu() {
    var skupina = document.querySelector("[data-skupina]");
    if (!skupina) return;
    document.addEventListener("keydown", function (udalost) {
      if (udalost.key !== "Escape") return;
      if (!skupina.contains(document.activeElement)) return;
      document.activeElement.blur();
    });
  }

  /* --- výsledky zkoušek na rozcestníku ----------------------------------- */

  /* Souhrn zapisuje assets/zkouska.js po odevzdání testu (v bodech). */
  function nastavVysledky() {
    var karty = document.querySelectorAll("[data-vysledek]");
    if (!karty.length) return;
    var klic = document.body.getAttribute("data-vysledky") || (PREFIX + "zkousky-vysledky");
    var vse;
    try { vse = JSON.parse(nacti(klic)) || {}; } catch (e) { vse = {}; }

    function body(b, z) {
      return b + " / " + z.celkem + " b. (" + Math.round(b / z.celkem * 100) + " %)";
    }

    [].forEach.call(karty, function (karta) {
      var z = vse[karta.getAttribute("data-vysledek")];
      if (!z || !z.celkem) return;
      var splneno = z.nejlepe >= z.hranice;
      karta.classList.add(splneno ? "karta--splneno" : "karta--nesplneno");

      var blok = document.createElement("div");
      blok.className = "karta-vysledek";
      var stitek = document.createElement("span");
      stitek.className = "karta-vysledek-stitek " + (splneno ? "uspech" : "neuspech");
      stitek.textContent = splneno ? "✓ Splněno" : "Zatím nesplněno";
      var radek = document.createElement("span");
      radek.textContent = "Naposledy " + body(z.posledni, z) + " · nejlépe " + body(z.nejlepe, z) +
        " · pokusů " + z.pokusu;
      blok.append(stitek, radek);
      karta.insertBefore(blok, karta.querySelector("ul"));
    });
  }

  /* --- odkazy na lokální testy jen na tomto počítači ---------------------- */

  /* web/lokalni/ se nepublikuje, na GitHub Pages by odkaz vedl na 404. */
  function nastavLokalni() {
    var h = location.hostname;
    if (location.protocol !== "file:" && h !== "localhost" && h !== "127.0.0.1") return;
    [].forEach.call(document.querySelectorAll("[data-jen-lokalne]"), function (x) { x.hidden = false; });
  }

  function start() {
    nastavLokalni();
    nastavTema();
    nastavVysledky();
    nastavPodmenu();
    nastavPostup();
    nastavStrom();
    nastavKopirovani();
    nastavCviceni();
    nastavPraxe();
    nastavSplneno();
    nastavPrehled();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
