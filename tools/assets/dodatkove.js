/* Dodatkové otázky Sample Exam A (drag & drop) bez přetahování:
   „razeni“ — ke každé položce se vybere pořadí 1–n; spravne = písmena v pořadí od prvního kroku.
   „prirazeni“ — ke každé položce se vybere skupina; spravne[i] = číslo skupiny (1–n) pro položku i.
   Data: window.DODATKOVE_OTAZKY. */
(function () {
  "use strict";

  var D = window.DODATKOVE_OTAZKY;
  var koren = document.getElementById("dodatkove");
  if (!D || !koren) return;

  var PISMENA = "abcdefghij";
  var KOREN_WEBU = koren.getAttribute("data-koren") || "";
  var jazyk = "en";
  try { var j = localStorage.getItem("genai-jazyk"); if (j === "cz" || j === "en" || j === "encz") jazyk = j; } catch (e) { /* nevadí */ }
  var odpovedi = {}, vyhodnoceno = {};

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function tx(q) { return jazyk === "cz" ? q.cz : q.en; }

  // Správná hodnota výběru u položky i (pořadí nebo číslo skupiny, číslováno od 1).
  function spravnaHodnota(q, i) {
    if (q.typ === "razeni") return String(q.spravne.indexOf(PISMENA[i]) + 1);
    return String(q.spravne[i]);
  }
  function popisHodnoty(q, t, h) {
    if (q.typ === "razeni") return h + ". krok";
    return h + " – " + (t.skupiny[+h - 1] || "");
  }

  function vykresli() {
    var html = '<div class="zk-tlacitka">' + [["en", "English"], ["cz", "Česky"], ["encz", "English + skrytý český překlad"]].map(function (x) {
      return '<button type="button" class="zk-btn" data-jazyk="' + x[0] + '" aria-pressed="' + (jazyk === x[0]) + '">' + x[1] + '</button>';
    }).join("") + '</div>';
    D.otazky.forEach(function (q, n) {
      var t = tx(q), hotovo = vyhodnoceno[q.id], odp = odpovedi[q.id] || [];
      var pocetVoleb = q.typ === "razeni" ? t.m.length : t.skupiny.length;
      var vsechnoOk = hotovo && t.m.every(function (_, i) { return odp[i] === spravnaHodnota(q, i); });
      html += '<article class="zk-karta zk-otazka' + (hotovo ? (vsechnoOk ? " spravne" : " chybne") : "") + '" lang="' + (jazyk === "cz" ? "cs" : "en") + '">' +
        '<p class="zk-meta">Dodatková otázka A' + (n + 1) + ' · ' + esc(q.lo) + ' · ' + esc(q.k) + ' · ' +
          (q.typ === "razeni" ? "seřazení" : "přiřazení") + '</p>' +
        '<div class="zk-zadani">' + t.q + '</div>' +
        (q.typ === "prirazeni" ? '<ol class="zk-skupiny">' + t.skupiny.map(function (s) { return "<li>" + s + "</li>"; }).join("") + '</ol>' : '') +
        '<ul class="zk-moznosti zk-moznosti--rozbor">' + t.m.map(function (m, i) {
          var volby = '<option value="">—</option>';
          for (var h = 1; h <= pocetVoleb; h++) {
            volby += '<option value="' + h + '"' + (odp[i] === String(h) ? " selected" : "") + '>' +
              esc(q.typ === "razeni" ? h + "." : h + " – " + String(t.skupiny[h - 1]).replace(/<[^>]+>/g, "").slice(0, 50)) + '</option>';
          }
          var tr = hotovo ? (odp[i] === spravnaHodnota(q, i) ? "spravna" : "chybna") : "";
          return '<li class="' + tr + '"><div class="zk-moznost-text"><span class="zk-pismeno">' + PISMENA[i] + ')</span> <span>' + m + '</span></div>' +
            '<label class="zk-dd-volba"><span>' + (q.typ === "razeni" ? "Pořadí" : "Skupina") + '</span> ' +
            '<select data-q="' + n + '" data-i="' + i + '"' + (hotovo ? " disabled" : "") + '>' + volby + '</select></label>' +
            (hotovo && odp[i] !== spravnaHodnota(q, i) ? '<p class="zk-zduvodneni">Správně: ' + esc(popisHodnoty(q, t, spravnaHodnota(q, i)).replace(/<[^>]+>/g, "")) + '</p>' : '') +
          '</li>';
        }).join("") + '</ul>' +
        (jazyk === "encz" ? '<details class="zk-preklad-det" lang="cs"><summary>Český překlad</summary><div class="zk-zadani">' + q.cz.q + '</div>' +
          (q.typ === "prirazeni" ? '<ol class="zk-skupiny">' + q.cz.skupiny.map(function (s) { return "<li>" + s + "</li>"; }).join("") + '</ol>' : '') +
          '<ol class="zk-preklad-moznosti" type="a">' + q.cz.m.map(function (x) { return "<li>" + x + "</li>"; }).join("") + '</ol>' +
          (hotovo && q.cz.obecne ? '<div class="zk-obecne">' + q.cz.obecne + '</div>' : '') + '</details>' : '') +
        (hotovo
          ? '<p class="zk-verdikt ' + (vsechnoOk ? 'uspech">Vše správně.' : 'neuspech">Některá přiřazení jsou špatně.') + '</p>' +
            (t.obecne ? '<div class="zk-obecne">' + t.obecne + '</div>' : '') +
            (q.kap && q.kap.href ? '<p class="zk-odkaz">Sylabus ' + esc(q.kap.c) + ' · <a href="' + esc(KOREN_WEBU + q.kap.href) + '">výklad →</a></p>' : '')
          : '') +
        '<div class="zk-ovladani" lang="cs">' +
          (hotovo ? '<button type="button" class="zk-btn" data-znovu="' + n + '">Zkusit znovu</button>'
                  : '<button type="button" class="zk-btn zk-btn--hlavni" data-vyhodnotit="' + n + '">Vyhodnotit</button>') +
        '</div></article>';
    });
    koren.innerHTML = html;

    koren.querySelectorAll("[data-jazyk]").forEach(function (b) {
      b.onclick = function () { jazyk = b.getAttribute("data-jazyk"); vykresli(); };
    });
    koren.querySelectorAll("select[data-q]").forEach(function (s) {
      s.onchange = function () {
        var q = D.otazky[+s.getAttribute("data-q")];
        (odpovedi[q.id] = odpovedi[q.id] || [])[+s.getAttribute("data-i")] = s.value;
      };
    });
    koren.querySelectorAll("[data-vyhodnotit]").forEach(function (b) {
      b.onclick = function () { vyhodnoceno[D.otazky[+b.getAttribute("data-vyhodnotit")].id] = true; vykresli(); };
    });
    koren.querySelectorAll("[data-znovu]").forEach(function (b) {
      b.onclick = function () {
        var id = D.otazky[+b.getAttribute("data-znovu")].id;
        delete vyhodnoceno[id]; delete odpovedi[id]; vykresli();
      };
    });
  }

  vykresli();
})();
