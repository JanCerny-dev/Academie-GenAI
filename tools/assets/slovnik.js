/* Slovník: vyhledávání (EN i CZ, bez diakritiky), filtr kapitoly a klíčových pojmů.
   Pojmy jsou ve statickém HTML; skript je jen skrývá. */
(function () {
  "use strict";

  var seznam = document.getElementById("slovnik-seznam");
  var filtr = document.getElementById("slovnik-filtr");
  if (!seznam || !filtr) return;
  filtr.hidden = false;

  var dotaz = document.getElementById("slovnik-dotaz");
  var klicove = document.getElementById("slovnik-klicove");
  var pocet = document.getElementById("slovnik-pocet");
  var polozky = [].slice.call(seznam.querySelectorAll(".pojem-polozka"));
  var kap = "vse";

  function normalizuj(t) {
    return String(t).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
  }

  function obnov() {
    var q = normalizuj(dotaz.value);
    var n = 0;
    polozky.forEach(function (li) {
      var ok = (!q || li.getAttribute("data-hledat").indexOf(q) >= 0) &&
        (kap === "vse" || (" " + li.getAttribute("data-kap") + " ").indexOf(" " + kap + " ") >= 0) &&
        (!klicove.checked || li.getAttribute("data-klicove") === "1");
      li.hidden = !ok;
      if (ok) n++;
    });
    pocet.textContent = "Zobrazeno " + n + " z " + polozky.length + " pojmů.";
  }

  dotaz.addEventListener("input", obnov);
  klicove.addEventListener("change", obnov);
  filtr.querySelectorAll("[data-filtr-kap]").forEach(function (b) {
    b.addEventListener("click", function () {
      kap = b.getAttribute("data-filtr-kap");
      filtr.querySelectorAll("[data-filtr-kap]").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      obnov();
    });
  });
  obnov();
})();
