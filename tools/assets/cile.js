/* Studijní cíle: sebehodnocení (neumím / trochu / umím) a úspěšnost po LO.
   Sebehodnocení: genai-cile. Úspěšnost: genai-lo-vysledky (zapisuje zkouska.js a procvicovani.js). */
(function () {
  "use strict";

  var KLIC = "genai-cile";
  var KLIC_LO = "genai-lo-vysledky";
  var cile = [].slice.call(document.querySelectorAll(".cil[data-lo]"));
  if (!cile.length) return;

  function cti(k) { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } }
  var hodnoceni = cti(KLIC);
  var vysledky = cti(KLIC_LO);
  var souhrn = document.getElementById("cile-souhrn");
  var NAZVY = ["neumím", "trochu", "umím"];

  function procenta(ok, n) { return Math.round(ok / n * 100) + " %"; }

  function obnov() {
    var pocty = [0, 0, 0], bez = 0;
    cile.forEach(function (li) {
      var lo = li.getAttribute("data-lo");
      var h = hodnoceni[lo];
      li.querySelectorAll("[data-hodnoceni]").forEach(function (b) {
        b.setAttribute("aria-pressed", String(h === +b.getAttribute("data-hodnoceni")));
      });
      li.classList.remove("cil--0", "cil--1", "cil--2");
      if (h === 0 || h === 1 || h === 2) { pocty[h]++; li.classList.add("cil--" + h); } else bez++;

      var z = vysledky[lo], stat = li.querySelector("[data-stat]"), t = [];
      if (z && z.celkem) t.push("zkoušky " + z.ok + "/" + z.celkem + " (" + procenta(z.ok, z.celkem) + ")");
      if (z && z.pr_celkem) t.push("procvičování " + z.pr_ok + "/" + z.pr_celkem + " (" + procenta(z.pr_ok, z.pr_celkem) + ")");
      stat.textContent = t.join(" · ");
      var vse = (z ? (z.ok || 0) + (z.pr_ok || 0) : 0), n = (z ? (z.celkem || 0) + (z.pr_celkem || 0) : 0);
      stat.className = "cil-stat" + (n ? (vse / n >= 0.8 ? " cil-stat--ok" : vse / n < 0.65 ? " cil-stat--slabe" : "") : "");
    });
    if (souhrn) {
      souhrn.textContent = "Sebehodnocení: " + NAZVY.map(function (n, i) { return n + " " + pocty[i]; }).join(" · ") +
        " · nehodnoceno " + bez + " z " + cile.length + ".";
    }
  }

  cile.forEach(function (li) {
    var lo = li.getAttribute("data-lo");
    li.querySelectorAll("[data-hodnoceni]").forEach(function (b) {
      b.addEventListener("click", function () {
        var h = +b.getAttribute("data-hodnoceni");
        if (hodnoceni[lo] === h) delete hodnoceni[lo]; else hodnoceni[lo] = h;
        try { localStorage.setItem(KLIC, JSON.stringify(hodnoceni)); } catch (e) { /* nevadí */ }
        obnov();
      });
    });
  });
  var reset = document.getElementById("cile-reset");
  if (reset) reset.addEventListener("click", function () {
    if (!confirm("Smazat sebehodnocení všech studijních cílů?")) return;
    hodnoceni = {};
    try { localStorage.removeItem(KLIC); } catch (e) { /* nevadí */ }
    obnov();
  });
  obnov();
})();
