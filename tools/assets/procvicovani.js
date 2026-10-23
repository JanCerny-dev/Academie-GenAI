/* Procvičování otázek po kapitolách a po studijních cílech s okamžitým vyhodnocením
   (převzato z webu CTFL a upraveno). Data: window.CVICNE_OTAZKY.
   Jazyk en | cz | encz jako u zkoušky. Výsledky po LO se přičítají do genai-lo-vysledky. */
(function () {
  "use strict";

  var C = window.CVICNE_OTAZKY;
  var koren = document.getElementById("procvicovani");
  if (!C || !koren) return;

  var PISMENA = "abcdef";
  var KOREN_WEBU = koren.getAttribute("data-koren") || "";
  var PREFIX = koren.getAttribute("data-prefix") || "genai-";
  var KLIC = PREFIX + "procvicovani";
  var KLIC_LO = "genai-lo-vysledky";
  var JAZYKY = { en: "English", cz: "Česky", encz: "EN + skrytý překlad" };
  var vse = C.otazky;

  var nast = { kap: "vse", lo: "", jazyk: "cz", oficialni: true };
  try { nast = Object.assign(nast, JSON.parse(localStorage.getItem(KLIC)) || {}); } catch (e) { /* nevadí */ }
  var m = /[?&]lo=(GenAI-[\d.]+)/.exec(window.location.search);
  if (m) { nast.lo = m[1]; nast.kap = "vse"; }
  var fronta = [], pozice = 0, odpoved = [], hotovo = false, skore = { ok: 0, celkem: 0 }, preklad = false;

  function uloz() { try { localStorage.setItem(KLIC, JSON.stringify(nast)); } catch (e) { /* nevadí */ } }
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
  function kapitola(q) { return String(q.lo || "").replace("GenAI-", "").split(".")[0]; }
  function maOficialni() { return vse.some(function (q) { return q.oficialni; }); }
  function vyber() {
    return vse.filter(function (q) {
      if (q.oficialni && !nast.oficialni) return false;
      if (nast.lo) return q.lo === nast.lo;
      return nast.kap === "vse" || kapitola(q) === nast.kap;
    });
  }
  function novaFronta() {
    fronta = zamichane(vyber());
    pozice = 0; odpoved = []; hotovo = false; preklad = false; skore = { ok: 0, celkem: 0 };
    vykresli();
  }
  function spravne(q) {
    return odpoved.length === q.ok.length && q.ok.every(function (x) { return odpoved.indexOf(x) >= 0; });
  }
  function tx(q, j) {
    j = j || nast.jazyk;
    return j === "cz" ? (q.cz || q.en) : (q.en || q.cz);
  }
  function zapisLo(q, ok) {
    try {
      var d = JSON.parse(localStorage.getItem(KLIC_LO)) || {};
      var z = d[q.lo] || (d[q.lo] = { ok: 0, celkem: 0, pr_ok: 0, pr_celkem: 0 });
      z.pr_celkem = (z.pr_celkem || 0) + 1;
      if (ok) z.pr_ok = (z.pr_ok || 0) + 1;
      localStorage.setItem(KLIC_LO, JSON.stringify(d));
    } catch (e) { /* nevadí */ }
  }

  function filtry() {
    var pocty = {}, poctyLo = {};
    vse.forEach(function (q) {
      if (q.oficialni && !nast.oficialni) return;
      pocty[kapitola(q)] = (pocty[kapitola(q)] || 0) + 1;
      poctyLo[q.lo] = (poctyLo[q.lo] || 0) + 1;
    });
    var celkem = Object.keys(pocty).reduce(function (s, k) { return s + pocty[k]; }, 0);
    var tl = '<button type="button" class="zk-btn" data-kap="vse" aria-pressed="' + (nast.kap === "vse" && !nast.lo) + '">Všechny kapitoly (' + celkem + ')</button>';
    Object.keys(C.kapitoly).forEach(function (k) {
      if (!pocty[k]) return;
      tl += '<button type="button" class="zk-btn" data-kap="' + k + '" aria-pressed="' + (nast.kap === k && !nast.lo) + '" title="' +
        esc(C.kapitoly[k]) + '">Kapitola ' + k + ' (' + pocty[k] + ')</button>';
    });
    var volby = '<option value="">— všechny studijní cíle —</option>' + Object.keys(C.lo).map(function (lo) {
      return '<option value="' + lo + '"' + (nast.lo === lo ? " selected" : "") + (poctyLo[lo] ? "" : " disabled") + '>' +
        esc(lo.replace("GenAI-", "")) + ' (' + C.lo[lo].k + ', ' + (poctyLo[lo] || 0) + ') ' + esc(C.lo[lo].text.slice(0, 70)) + '</option>';
    }).join("");
    var jaz = Object.keys(JAZYKY).map(function (j) {
      return '<button type="button" class="zk-btn" data-jazyk="' + j + '" aria-pressed="' + (nast.jazyk === j) + '">' + JAZYKY[j] + '</button>';
    }).join("");
    return '<section class="zk-karta">' +
      '<div class="zk-tlacitka">' + tl + '</div>' +
      '<label class="pr-lo-volba">Studijní cíl <select data-lo>' + volby + '</select></label>' +
      '<div class="zk-tlacitka">' + jaz + '</div>' +
      (maOficialni() ? '<label class="zk-volba"><input type="checkbox" data-oficialni' + (nast.oficialni ? " checked" : "") + '> ' +
        'Zahrnout otázky Sample Exam A</label>' : '') +
    '</section>';
  }

  function moznosti(q, t, vyhodnoceno) {
    var typ = q.vyber > 1 ? "checkbox" : "radio";
    return '<ul class="zk-moznosti' + (vyhodnoceno ? ' zk-moznosti--rozbor' : '') + '">' +
      t.m.map(function (m, k) {
        if (!vyhodnoceno) {
          return '<li><label class="zk-moznost"><input type="' + typ + '" name="odp" value="' + k + '"' +
            (odpoved.indexOf(k) >= 0 ? " checked" : "") + '><span class="zk-pismeno">' + PISMENA[k] +
            ')</span> <span>' + m + '</span></label></li>';
        }
        var jeSpravna = q.ok.indexOf(k) >= 0, vybrana = odpoved.indexOf(k) >= 0;
        var vys = (t.vys || {})[PISMENA[k]];
        return '<li class="' + (jeSpravna ? "spravna" : (vybrana ? "chybna" : "")) + '">' +
          '<div class="zk-moznost-text"><span class="zk-pismeno">' + PISMENA[k] + ')</span> <span>' + m + '</span>' +
          (vybrana ? ' <em class="zk-vase" lang="cs">vaše odpověď</em>' : '') + '</div>' +
          (vys ? '<p class="zk-zduvodneni">' + vys + '</p>' : '') + '</li>';
      }).join("") +
    '</ul>' + (vyhodnoceno && t.obecne ? '<div class="zk-obecne">' + t.obecne + '</div>' : '');
  }

  function vykresli() {
    var q = fronta[pozice];
    var html = filtry();
    if (!q) {
      html += '<section class="zk-karta"><p>' + (fronta.length
        ? 'Hotovo — správně ' + skore.ok + ' z ' + skore.celkem + '.'
        : 'V tomto výběru nejsou žádné otázky.') + '</p>' +
        (fronta.length ? '<div class="zk-tlacitka"><button type="button" class="zk-btn zk-btn--hlavni" data-znovu>Projít znovu v jiném pořadí</button></div>' : '') +
        '</section>';
      koren.innerHTML = html;
      navaz();
      return;
    }
    var t = tx(q);
    var cz = nast.jazyk === "encz" && q.cz;
    html += '<div class="zk-lista">' +
        '<span>Otázka <strong>' + (pozice + 1) + '</strong> z ' + fronta.length + '</span>' +
        '<span>Správně ' + skore.ok + ' / ' + skore.celkem + '</span>' +
        '<span>' + esc(q.lo) + ' · ' + esc(q.k) + '</span>' +
      '</div>' +
      '<article class="zk-karta zk-otazka' + (hotovo ? (spravne(q) ? " spravne" : " chybne") : "") + '" lang="' + (nast.jazyk === "cz" ? "cs" : "en") + '">' +
        '<div class="zk-zadani">' + t.q + '</div>' +
        '<p class="zk-pokyn">' + (nast.jazyk === "cz"
          ? (q.vyber > 1 ? 'Vyberte DVĚ možnosti.' : 'Vyberte JEDNU možnost.')
          : (q.vyber > 1 ? 'Select TWO options.' : 'Select ONE option.')) + '</p>' +
        moznosti(q, t, hotovo) +
        (cz ? '<div class="zk-preklad-obal" lang="cs"><button type="button" class="zk-btn zk-btn--preklad" data-preklad aria-expanded="' + preklad + '">' +
          (preklad ? 'Skrýt český překlad' : 'Zobrazit český překlad') + '</button>' +
          '<div class="zk-preklad"' + (preklad ? '' : ' hidden') + '><div class="zk-zadani">' + q.cz.q + '</div>' +
          (hotovo ? moznosti(q, q.cz, true)
            : '<ol class="zk-preklad-moznosti" type="a">' + q.cz.m.map(function (x) { return '<li>' + x + '</li>'; }).join("") + '</ol>') +
          '</div></div>' : '') +
        (hotovo
          ? '<p class="zk-verdikt ' + (spravne(q) ? 'uspech">Správně.' : 'neuspech">Špatně.') + '</p>' +
            (q.kap && q.kap.href ? '<p class="zk-odkaz">Sylabus ' + esc(q.kap.c) + (q.kap.nazev ? ' — ' + esc(q.kap.nazev) : '') +
              ' · <a href="' + esc(KOREN_WEBU + q.kap.href) + '">výklad →</a></p>' : '') +
            '<p class="zk-meta">' + esc(q.zdroj || "") + '</p>'
          : '') +
        '<div class="zk-ovladani" lang="cs">' +
          (hotovo
            ? '<button type="button" class="zk-btn zk-btn--hlavni" data-dalsi>Další otázka →</button>'
            : '<button type="button" class="zk-btn zk-btn--hlavni" data-vyhodnotit disabled>Vyhodnotit</button>') +
        '</div>' +
      '</article>';
    koren.innerHTML = html;
    navaz();

    var btn = koren.querySelector("[data-vyhodnotit]");
    koren.querySelectorAll('input[name="odp"]').forEach(function (inp) {
      inp.addEventListener("change", function () {
        var v = [].slice.call(koren.querySelectorAll('input[name="odp"]:checked')).map(function (x) { return +x.value; });
        if (q.vyber > 1 && v.length > q.vyber) {
          inp.checked = false;
          v = v.filter(function (x) { return x !== +inp.value; });
        }
        odpoved = v;
        btn.disabled = odpoved.length !== q.vyber;
      });
    });
    if (btn) btn.onclick = function () {
      hotovo = true; skore.celkem++;
      if (spravne(q)) skore.ok++;
      zapisLo(q, spravne(q));
      vykresli();
    };
    var pr = koren.querySelector("[data-preklad]");
    if (pr) pr.onclick = function () { preklad = !preklad; vykresli(); };
    var dalsi = koren.querySelector("[data-dalsi]");
    if (dalsi) dalsi.onclick = function () {
      pozice++; odpoved = []; hotovo = false; preklad = false; vykresli();
      window.scrollTo(0, koren.offsetTop - 80);
    };
  }

  function navaz() {
    koren.querySelectorAll("[data-kap]").forEach(function (b) {
      b.onclick = function () { nast.kap = b.getAttribute("data-kap"); nast.lo = ""; uloz(); novaFronta(); };
    });
    koren.querySelectorAll("[data-jazyk]").forEach(function (b) {
      b.onclick = function () { nast.jazyk = b.getAttribute("data-jazyk"); uloz(); vykresli(); };
    });
    koren.querySelector("[data-lo]").onchange = function (ev) { nast.lo = ev.target.value; uloz(); novaFronta(); };
    var of = koren.querySelector("[data-oficialni]");
    if (of) of.onchange = function (ev) { nast.oficialni = ev.target.checked; uloz(); novaFronta(); };
    var z = koren.querySelector("[data-znovu]");
    if (z) z.onclick = novaFronta;
  }

  novaFronta();
})();
