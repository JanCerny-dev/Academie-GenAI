/* Kartičky ze slovníku s opakováním Leitnerovou metodou.
   Data: window.GENAI_SLOVNIK. Stav v localStorage (genai-karticky):
   přihrádka 1–5 u každého pojmu a číslo kola. Přihrádka b se opakuje každé 2^(b-1). kolo:
   1 každé kolo, 2 každé druhé, 3 každé čtvrté, 4 každé osmé, 5 každé šestnácté.
   „Umím“ posune kartičku o přihrádku výš, „neumím“ ji vrátí do první.
   Klávesy: mezerník otočí, → umím, ← neumím. */
(function () {
  "use strict";

  var D = window.GENAI_SLOVNIK;
  var koren = document.getElementById("karticky");
  if (!D || !koren) return;

  var KLIC = "genai-karticky";
  var stav = { prihradky: {}, kolo: 0, smer: "en", kap: [], klicove: false };
  try { stav = Object.assign(stav, JSON.parse(localStorage.getItem(KLIC)) || {}); } catch (e) { /* nevadí */ }
  function uloz() { try { localStorage.setItem(KLIC, JSON.stringify(stav)); } catch (e) { /* nevadí */ } }

  var fronta = [], pozice = 0, otocena = false, vysledky = { umim: 0, neumim: 0 };

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function zamichane(pole) {
    var a = pole.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function prihradka(p) { return stav.prihradky[p.id] || 1; }
  function vybrane() {
    return D.pojmy.filter(function (p) {
      return (!stav.kap.length || p.kap.some(function (k) { return stav.kap.indexOf(String(k)) >= 0; })) &&
        (!stav.klicove || p.klicove);
    });
  }
  function naRade(p, kolo) {
    var b = prihradka(p);
    return kolo % Math.pow(2, b - 1) === 0;
  }

  function prehled() {
    var vyb = vybrane();
    var pocty = [0, 0, 0, 0, 0];
    vyb.forEach(function (p) { pocty[prihradka(p) - 1]++; });
    var dalsiKolo = stav.kolo + 1;
    var naRadeN = vyb.filter(function (p) { return naRade(p, dalsiKolo); }).length;
    var kapitoly = Object.keys(D.kapitoly).filter(function (k) {
      return D.pojmy.some(function (p) { return p.kap.indexOf(+k) >= 0; });
    });
    koren.innerHTML =
      '<section class="zk-karta">' +
        '<h2>Výběr</h2>' +
        '<div class="zk-tlacitka">' + kapitoly.map(function (k) {
          return '<button type="button" class="zk-btn" data-kap="' + k + '" aria-pressed="' + (stav.kap.indexOf(k) >= 0) + '">Kapitola ' + k + '</button>';
        }).join("") + '</div>' +
        '<p class="napoveda">Bez vybrané kapitoly se berou všechny.</p>' +
        '<label class="zk-volba"><input type="checkbox" data-klicove' + (stav.klicove ? " checked" : "") + '> Jen klíčové pojmy (K1)</label>' +
        '<div class="zk-tlacitka">' +
          '<button type="button" class="zk-btn" data-smer="en" aria-pressed="' + (stav.smer === "en") + '">EN → CZ</button>' +
          '<button type="button" class="zk-btn" data-smer="cz" aria-pressed="' + (stav.smer === "cz") + '">CZ → EN</button>' +
        '</div>' +
        '<ul class="kt-prihradky" aria-label="Přihrádky">' + pocty.map(function (n, i) {
          return '<li><span>Přihrádka ' + (i + 1) + '</span><strong>' + n + '</strong></li>';
        }).join("") + '</ul>' +
        '<p>Vybráno ' + vyb.length + ' pojmů. V kole ' + dalsiKolo + ' je na řadě <strong>' + naRadeN + '</strong>.</p>' +
        '<div class="zk-tlacitka">' +
          '<button type="button" class="zk-btn zk-btn--hlavni" data-start' + (naRadeN ? "" : " disabled") + '>Začít kolo ' + dalsiKolo + '</button>' +
          '<button type="button" class="zk-btn" data-vse' + (vyb.length ? "" : " disabled") + '>Projít všechny vybrané</button>' +
          '<button type="button" class="zk-btn" data-reset>Vynulovat přihrádky</button>' +
        '</div>' +
      '</section>';

    koren.querySelectorAll("[data-kap]").forEach(function (b) {
      b.onclick = function () {
        var k = b.getAttribute("data-kap"), i = stav.kap.indexOf(k);
        if (i >= 0) stav.kap.splice(i, 1); else stav.kap.push(k);
        uloz(); prehled();
      };
    });
    koren.querySelectorAll("[data-smer]").forEach(function (b) {
      b.onclick = function () { stav.smer = b.getAttribute("data-smer"); uloz(); prehled(); };
    });
    koren.querySelector("[data-klicove]").onchange = function (ev) { stav.klicove = ev.target.checked; uloz(); prehled(); };
    koren.querySelector("[data-start]").onclick = function () {
      stav.kolo = dalsiKolo; uloz();
      spust(vyb.filter(function (p) { return naRade(p, dalsiKolo); }));
    };
    koren.querySelector("[data-vse]").onclick = function () { spust(vyb); };
    koren.querySelector("[data-reset]").onclick = function () {
      if (confirm("Vrátit všechny kartičky do první přihrádky?")) { stav.prihradky = {}; stav.kolo = 0; uloz(); prehled(); }
    };
  }

  function spust(seznam) {
    if (!seznam.length) return;
    // Nejdřív nižší přihrádky (to, co umím nejméně), uvnitř náhodně.
    fronta = zamichane(seznam).sort(function (a, b) { return prihradka(a) - prihradka(b); });
    pozice = 0; otocena = false; vysledky = { umim: 0, neumim: 0 };
    karta();
  }

  function karta() {
    var p = fronta[pozice];
    if (!p) return konec();
    var en = '<p class="kt-en" lang="en">' + esc(p.en) + '</p>';
    var cz = '<p class="kt-cz">' + esc(p.cz) + '</p>';
    var lic = stav.smer === "en" ? en : cz;
    var rub = (stav.smer === "en" ? cz : en) + '<p class="kt-def">' + esc(p.def) + '</p>' +
      '<p class="kt-meta">Kapitola ' + p.kap.join(", ") + (p.klicove ? ' · klíčový pojem (K1)' : '') +
      (p.href ? ' · <a href="' + esc(p.href) + '">výklad →</a>' : '') + '</p>';
    koren.innerHTML =
      '<div class="zk-lista"><span>Kartička <strong>' + (pozice + 1) + '</strong> z ' + fronta.length + '</span>' +
        '<span>Přihrádka ' + prihradka(p) + '</span><span>umím ' + vysledky.umim + ' · neumím ' + vysledky.neumim + '</span></div>' +
      '<button type="button" class="kt-karta' + (otocena ? ' kt-karta--rub' : '') + '" data-otocit aria-label="Otočit kartičku">' +
        '<span class="kt-strana">' + (otocena ? "rub" : "líc") + '</span>' + lic + (otocena ? '<div class="kt-rub">' + rub + '</div>' : '') +
      '</button>' +
      '<div class="zk-ovladani">' +
        (otocena
          ? '<button type="button" class="zk-btn kt-neumim" data-neumim>← Neumím</button>' +
            '<button type="button" class="zk-btn zk-btn--hlavni" data-umim>Umím →</button>'
          : '<button type="button" class="zk-btn" data-konec>Ukončit</button>' +
            '<button type="button" class="zk-btn zk-btn--hlavni" data-otocit-tl>Otočit (mezerník)</button>') +
      '</div>';
    koren.querySelector("[data-otocit]").onclick = otoc;
    var t = koren.querySelector("[data-otocit-tl]"); if (t) t.onclick = otoc;
    var u = koren.querySelector("[data-umim]"); if (u) u.onclick = function () { hodnot(true); };
    var n = koren.querySelector("[data-neumim]"); if (n) n.onclick = function () { hodnot(false); };
    var k = koren.querySelector("[data-konec]"); if (k) k.onclick = konec;
  }

  function otoc() { otocena = !otocena; karta(); }

  function hodnot(umim) {
    var p = fronta[pozice];
    if (!p || !otocena) return;
    stav.prihradky[p.id] = umim ? Math.min(5, prihradka(p) + 1) : 1;
    if (umim) vysledky.umim++; else vysledky.neumim++;
    uloz();
    pozice++; otocena = false;
    karta();
  }

  function konec() {
    fronta = [];
    koren.innerHTML = '<section class="zk-karta"><p class="zk-verdikt uspech">Kolo hotovo: umím ' + vysledky.umim +
      ', neumím ' + vysledky.neumim + '.</p><div class="zk-tlacitka"><button type="button" class="zk-btn zk-btn--hlavni" data-zpet>Zpět na přehled</button></div></section>';
    koren.querySelector("[data-zpet]").onclick = prehled;
  }

  document.addEventListener("keydown", function (e) {
    if (!fronta.length || pozice >= fronta.length || e.ctrlKey || e.metaKey || e.altKey) return;
    var cil = e.target && e.target.tagName;
    if (cil === "INPUT" || cil === "SELECT" || cil === "TEXTAREA") return;
    if (e.key === " " || e.key === "Spacebar") { e.preventDefault(); otoc(); }
    else if (e.key === "ArrowRight" && otocena) { e.preventDefault(); hodnot(true); }
    else if (e.key === "ArrowLeft" && otocena) { e.preventDefault(); hodnot(false); }
  });

  if (!D.pojmy.length) {
    koren.innerHTML = '<p class="poznamka">Slovník se připravuje, kartičky zatím nejsou.</p>';
    return;
  }
  prehled();
})();
