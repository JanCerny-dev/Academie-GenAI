/* Simulace zkoušky ISTQB CT-GenAI (převzato z webu CTFL a upraveno).
   Data: window.VZOROVA_ZKOUSKA (pevný test) nebo window.CVICNE_OTAZKY (náhodná zkouška / mix,
   losování v prohlížeči přesně podle rozpisu po LO). Vylosovaná id se ukládají do stavu testu.
   Body: K3 = 2 body, ostatní 1; hranice 65 % bodů (30 ze 46).
   Jazyk: en | cz | encz (anglicky se skrytým českým překladem u každé otázky).
   Průběh: úvod → test → výsledek → (oprava 10 min) → vyhodnocení.
   Nic se nenačítá přes fetch, stránka funguje i otevřená z disku. */
(function () {
  "use strict";

  var koren = document.getElementById("zkouska");
  if (!koren) return;
  var SADA = koren.getAttribute("data-sada") || "test";
  var C = window.CVICNE_OTAZKY;
  var NAHODNA = !window.VZOROVA_ZKOUSKA || SADA === "nahodna" || SADA === "mix";
  var D = NAHODNA ? (C && { sada: SADA, oficialni: false, otazky: [] }) : window.VZOROVA_ZKOUSKA;
  if (!D) return;

  var KOREN_WEBU = koren.getAttribute("data-koren") || "";
  var PREFIX = koren.getAttribute("data-prefix") || "genai-";
  var OTAZKY = D.otazky;
  var OFICIALNI = !!D.oficialni;
  var KLIC = PREFIX + "zkouska-" + SADA.toLowerCase();
  var KLIC_VYSLEDKY = PREFIX + "zkousky-vysledky";   // souhrn pro rozcestník
  var KLIC_LO = "genai-lo-vysledky";                 // úspěšnost po LO pro stránku Cíle
  var KLIC_JAZYK = "genai-jazyk";
  var MINUT_TEST = 60, MINUT_PRODLOUZENO = 75, MINUT_OPRAVA = 10;
  var PISMENA = "abcdef";
  var JAZYKY = { en: "English", cz: "Česky", encz: "English + skrytý český překlad" };

  var S = null;          // stav, ukládá se do localStorage
  var casovac = null;

  /* --- úložiště (v soukromém režimu nemusí být k dispozici) --- */
  function ctiJson(klic, vychozi) {
    try { return JSON.parse(localStorage.getItem(klic)) || vychozi; } catch (e) { return vychozi; }
  }
  function pisJson(klic, h) {
    try { localStorage.setItem(klic, JSON.stringify(h)); } catch (e) { /* nevadí */ }
  }
  function uloz() { pisJson(KLIC, S); }
  function nacti() { return ctiJson(KLIC, null); }
  function smaz() { try { localStorage.removeItem(KLIC); } catch (e) { /* nevadí */ } }

  function celkemBodu() { return OTAZKY.reduce(function (s, q) { return s + (q.body || 1); }, 0); }
  function hranice() { return Math.ceil(celkemBodu() * 0.65 - 1e-9); }
  function pocet() { return OTAZKY.length; }

  // Výsledek pokusu do souhrnu a historie. Oprava přepíše výsledek téhož pokusu.
  function zapisVysledek(b) {
    var vse = ctiJson(KLIC_VYSLEDKY, {});
    var sada = SADA.toLowerCase();
    var z = vse[sada] || { pokusu: 0, nejlepe: 0, historie: [] };
    z.historie = z.historie || [];
    var zaznam = { cas: S.pokus, body: b, celkem: celkemBodu(), jazyk: S.jazyk };
    if (z.pokus !== S.pokus) { z.pokusu++; z.pokus = S.pokus; z.historie.push(zaznam); }
    else if (z.historie.length) z.historie[z.historie.length - 1] = zaznam;
    if (z.historie.length > 30) z.historie = z.historie.slice(-30);
    z.posledni = b;
    z.nejlepe = Math.max(z.nejlepe, b);
    z.celkem = celkemBodu();
    z.hranice = hranice();
    vse[sada] = z;
    pisJson(KLIC_VYSLEDKY, vse);
  }
  // Úspěšnost po LO (jednou za pokus, po vyhodnocení).
  function zapisLo() {
    if (S.loZapsano) return;
    var vse = ctiJson(KLIC_LO, {});
    OTAZKY.forEach(function (q, i) {
      if (!q.lo) return;
      var z = vse[q.lo] || (vse[q.lo] = { ok: 0, celkem: 0, pr_ok: 0, pr_celkem: 0 });
      z.celkem++;
      if (spravne(i, S.odp[i])) z.ok++;
    });
    pisJson(KLIC_LO, vse);
    S.loZapsano = true;
    uloz();
  }

  /* --- pomocné funkce --- */
  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function el(html) {
    var t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }
  function spravne(i, odp) {
    var ok = OTAZKY[i].ok;
    return !!odp && odp.length === ok.length && ok.every(function (x) { return odp.indexOf(x) >= 0; });
  }
  function skore(odpovedi) {
    var b = 0;
    for (var i = 0; i < pocet(); i++) if (spravne(i, odpovedi[i])) b += OTAZKY[i].body || 1;
    return b;
  }
  function pocetSpravnych(odpovedi) {
    var n = 0;
    for (var i = 0; i < pocet(); i++) if (spravne(i, odpovedi[i])) n++;
    return n;
  }
  function zodpovezeno(odpovedi) {
    return odpovedi.filter(function (o) { return o && o.length; }).length;
  }
  function mmss(ms) {
    var s = Math.max(0, Math.round(ms / 1000));
    return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
  }
  function nahoru() { window.scrollTo(0, koren.offsetTop - 80); }
  function bodu(n) { return n + " " + (n === 1 ? "bod" : (n >= 2 && n <= 4 ? "body" : "bodů")); }

  function jazyk() { return (S && S.jazyk) || "en"; }
  function tx(q, j) {
    j = j || jazyk();
    if (j === "cz") return q.cz || q.en;
    return q.en || q.cz;
  }
  function pokyn(q, j) {
    var cz = (j || jazyk()) === "cz";
    var n = q.vyber || 1;
    if (cz) return n > 1 ? "Vyberte " + (["", "", "DVĚ", "TŘI", "ČTYŘI"][n] || n) + " možnosti." : "Vyberte JEDNU možnost.";
    return n > 1 ? "Select " + (["", "", "TWO", "THREE", "FOUR"][n] || n) + " options." : "Select ONE option.";
  }
  function odkazVykladu(q) {
    if (!q.kap || !q.kap.href) return "";
    return '<p class="zk-odkaz">Sylabus ' + esc(q.kap.c) + (q.kap.nazev ? " — " + esc(q.kap.nazev) : "") +
      ' · <a href="' + esc(KOREN_WEBU + q.kap.href) + '">výklad →</a></p>';
  }
  function vychoziJazyk() {
    var m = /[?&]jazyk=(en|cz|encz)\b/.exec(window.location.search);
    if (m) return m[1];
    try { var j = localStorage.getItem(KLIC_JAZYK); if (JAZYKY[j]) return j; } catch (e) { /* nevadí */ }
    return "en";
  }

  /* --- náhodná zkouška: losování přesně podle rozpisu --- */
  function nahodne(pole, n) {
    var a = pole.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a.slice(0, n);
  }
  function maOficialni() { return C && C.otazky.some(function (q) { return q.oficialni; }); }
  function losuj(sOficialnimi) {
    var ids = [];
    var los = Object.keys(C.rozpis);
    for (var i = 0; i < los.length; i++) {
      var lo = los[i], n = C.rozpis[lo];
      var zasoba = C.otazky.filter(function (q) { return q.lo === lo && (sOficialnimi || !q.oficialni); });
      if (zasoba.length < n) return null;
      nahodne(zasoba, n).forEach(function (q) { ids.push(q.id); });
    }
    return ids;
  }
  function otazkyPodleId(ids) {
    var mapa = {};
    C.otazky.forEach(function (q) { mapa[q.id] = q; });
    return ids.map(function (id) { return mapa[id]; }).filter(Boolean);
  }
  function pripravStav(stav) {
    if (NAHODNA && stav && stav.ids) OTAZKY = otazkyPodleId(stav.ids);
    if (stav && !stav.jazyk) stav.jazyk = "en";
    return stav;
  }

  /* --- časovač --- */
  function spustCasovac() { zastavCasovac(); casovac = setInterval(tik, 1000); tik(); }
  function zastavCasovac() { if (casovac) clearInterval(casovac); casovac = null; }
  function tik() {
    var zbyva = S.konec - Date.now();
    var u = koren.querySelector("[data-cas]");
    if (u) {
      u.textContent = mmss(zbyva);
      u.classList.toggle("dochazi", zbyva < 5 * 60 * 1000);
    }
    if (zbyva <= 0) {
      zastavCasovac();
      if (S.faze === "test") odevzdej();
      else if (S.faze === "oprava") ukonciOpravu();
    }
  }

  /* --- úvod --- */
  function historie() {
    var z = ctiJson(KLIC_VYSLEDKY, {})[SADA.toLowerCase()];
    if (!z || !z.historie || !z.historie.length) return "";
    var radky = z.historie.slice(-6).reverse().map(function (h) {
      var d = new Date(h.cas);
      var ok = h.body >= Math.ceil(h.celkem * 0.65 - 1e-9);
      return '<li><span>' + d.toLocaleDateString("cs-CZ") + " " + d.toLocaleTimeString("cs-CZ", { hour: "2-digit", minute: "2-digit" }) +
        '</span><span>' + esc(JAZYKY[h.jazyk] || "") + '</span><strong class="' + (ok ? "uspech" : "neuspech") + '">' +
        h.body + " / " + h.celkem + "</strong></li>";
    }).join("");
    return '<h3>Předchozí pokusy</h3><ul class="zk-historie">' + radky + "</ul>";
  }

  function uvod() {
    zastavCasovac();
    var ulozeny = nacti();
    var rozpracovany = ulozeny && ulozeny.faze !== "vyhodnoceni" && ulozeny.faze;
    var celkem = NAHODNA ? Object.keys(C.rozpis).reduce(function (s, lo) { return s + C.rozpis[lo]; }, 0) : pocet();
    var bodyText = NAHODNA ? "46 bodů" : bodu(celkemBodu());
    var hr = NAHODNA ? 30 : hranice();
    var zvoleny = vychoziJazyk();
    koren.innerHTML = "";
    koren.appendChild(el(
      '<section class="zk-karta zk-uvod">' +
        '<h2>Pravidla</h2>' +
        '<ul>' +
          '<li><strong>' + celkem + ' otázek, ' + bodyText + '</strong>. Otázka K3 má 2 body, ostatní 1 bod.</li>' +
          '<li><strong>' + MINUT_TEST + ' minut</strong>. Po vypršení času se test odevzdá sám.</li>' +
          '<li>K úspěchu je potřeba <strong>' + hr + ' bodů</strong> (65 %).</li>' +
          '<li>Po odevzdání uvidíte jen počet bodů. Pokud test nesplníte, můžete ještě ' +
            '<strong>' + MINUT_OPRAVA + ' minut opravovat</strong> — které odpovědi jsou špatně, se ale nedozvíte.</li>' +
          '<li>Rozbor všech otázek se zdůvodněním přijde až ve vyhodnocení.</li>' +
          (NAHODNA ? '<li>Otázky se losují při každém spuštění přesně podle rozpisu ostré zkoušky.</li>' : '') +
        '</ul>' +
        '<fieldset class="zk-jazyk"><legend>Jazyk otázek</legend>' +
          Object.keys(JAZYKY).map(function (j) {
            return '<label class="zk-volba"><input type="radio" name="jazyk" value="' + j + '"' +
              (j === zvoleny ? " checked" : "") + '> ' + JAZYKY[j] + '</label>';
          }).join("") +
        '</fieldset>' +
        (NAHODNA && maOficialni() ? '<label class="zk-volba"><input type="checkbox" data-oficialni checked> ' +
          'Losovat i z otázek oficiální Sample Exam A</label>' : '') +
        '<label class="zk-volba"><input type="checkbox" data-prodlouzeni checked> ' +
          'Skládám zkoušku v jiném než rodném jazyce (+25 % času, tedy ' + MINUT_PRODLOUZENO + ' minut)</label>' +
        '<div class="zk-tlacitka">' +
          (rozpracovany
            ? '<button type="button" class="zk-btn zk-btn--hlavni" data-pokracovat>Pokračovat v rozpracovaném testu</button>' +
              '<button type="button" class="zk-btn" data-start>Začít znovu</button>'
            : '<button type="button" class="zk-btn zk-btn--hlavni" data-start>Spustit test</button>') +
        '</div>' +
        historie() +
      '</section>'
    ));
    koren.querySelector("[data-start]").onclick = function () {
      var minut = koren.querySelector("[data-prodlouzeni]").checked ? MINUT_PRODLOUZENO : MINUT_TEST;
      var j = koren.querySelector('input[name="jazyk"]:checked').value;
      try { localStorage.setItem(KLIC_JAZYK, j); } catch (e) { /* nevadí */ }
      var ids = null;
      if (NAHODNA) {
        var sOf = koren.querySelector("[data-oficialni]");
        ids = losuj(sOf ? sOf.checked : false);
        if (!ids) { alert("Z dostupných otázek se nepodařilo sestavit úplnou zkoušku podle rozpisu."); return; }
        OTAZKY = otazkyPodleId(ids);
      }
      S = {
        ids: ids, jazyk: j,
        pokus: Date.now(),
        faze: "test", i: 0,
        odp: OTAZKY.map(function () { return []; }),
        oznacene: [], preklady: [],
        konec: Date.now() + minut * 60 * 1000,
        prvni: null, odpPrvni: null
      };
      uloz();
      vykresliTest();
    };
    var pokr = koren.querySelector("[data-pokracovat]");
    if (pokr) pokr.onclick = function () { S = pripravStav(ulozeny); obnov(); };
  }

  function obnov() {
    if (S.faze === "test" || S.faze === "oprava") {
      if (S.konec <= Date.now()) {
        if (S.faze === "test") odevzdej(); else ukonciOpravu();
      } else vykresliTest();
    } else if (S.faze === "vysledek") vysledek();
    else vyhodnoceni();
  }

  function prekladOtazky(q, k) {
    if (jazyk() !== "encz" || !q.cz) return "";
    var ukazany = (S.preklady || []).indexOf(k) >= 0;
    return '<div class="zk-preklad-obal">' +
      '<button type="button" class="zk-btn zk-btn--preklad" data-preklad aria-expanded="' + ukazany + '">' +
        (ukazany ? "Skrýt český překlad" : "Zobrazit český překlad") + '</button>' +
      '<div class="zk-preklad" lang="cs"' + (ukazany ? "" : " hidden") + '>' +
        '<div class="zk-zadani">' + q.cz.q + '</div>' +
        '<ol class="zk-preklad-moznosti" type="a">' + q.cz.m.map(function (m) { return "<li>" + m + "</li>"; }).join("") + '</ol>' +
      '</div></div>';
  }

  /* --- test a oprava (stejné rozhraní) --- */
  function vykresliTest() {
    var oprava = S.faze === "oprava";
    var q = OTAZKY[S.i];
    var t = tx(q);
    var odp = S.odp[S.i];
    var typ = q.vyber > 1 ? "checkbox" : "radio";
    var oznacena = S.oznacene.indexOf(S.i) >= 0;
    var N = pocet();

    koren.innerHTML = "";
    var w = el(
      '<div class="zk-test">' +
        (oprava ? '<p class="zk-banner">Režim opravy: máte ' + MINUT_OPRAVA + ' minut na změnu odpovědí. ' +
          'Které odpovědi jsou špatně, se nedozvíte — projděte otázky sami.</p>' : '') +
        '<div class="zk-lista">' +
          '<span>Otázka <strong>' + (S.i + 1) + '</strong> z ' + N + ' · ' + bodu(q.body || 1) + '</span>' +
          '<span>Zodpovězeno ' + zodpovezeno(S.odp) + ' / ' + N + '</span>' +
          '<span class="zk-cas" aria-live="off">Zbývá <strong data-cas></strong></span>' +
        '</div>' +
        '<article class="zk-karta zk-otazka" lang="' + (jazyk() === "cz" ? "cs" : "en") + '">' +
          '<div class="zk-zadani">' + t.q + '</div>' +
          (q.pozn ? '<p class="zk-poznamka" lang="cs"><strong>Poznámka webu:</strong> ' + q.pozn + '</p>' : '') +
          '<p class="zk-pokyn">' + pokyn(q) + '</p>' +
          '<ul class="zk-moznosti">' +
            t.m.map(function (m, k) {
              return '<li><label class="zk-moznost">' +
                '<input type="' + typ + '" name="odp" value="' + k + '"' + (odp.indexOf(k) >= 0 ? " checked" : "") + '>' +
                '<span class="zk-pismeno">' + PISMENA[k] + ')</span> <span>' + m + '</span></label></li>';
            }).join("") +
          '</ul>' +
          prekladOtazky(q, S.i) +
          '<div class="zk-ovladani" lang="cs">' +
            '<button type="button" class="zk-btn" data-pred' + (S.i === 0 ? " disabled" : "") + '>← Předchozí</button>' +
            '<button type="button" class="zk-btn' + (oznacena ? ' zk-btn--oznacena' : '') + '" data-oznacit aria-pressed="' + oznacena + '">' +
              (oznacena ? 'Označeno k revizi' : 'Označit k revizi') + '</button>' +
            '<button type="button" class="zk-btn zk-btn--hlavni" data-dalsi' + (S.i === N - 1 ? " disabled" : "") + '>Další →</button>' +
          '</div>' +
        '</article>' +
        '<nav class="zk-mrizka" aria-label="Přehled otázek">' +
          OTAZKY.map(function (_, k) {
            var tr = [];
            if (S.odp[k].length) tr.push("zodpovezena");
            if (S.oznacene.indexOf(k) >= 0) tr.push("oznacena");
            if (k === S.i) tr.push("aktualni");
            return '<button type="button" class="' + tr.join(" ") + '" data-k="' + k + '"' +
              (k === S.i ? ' aria-current="true"' : '') + '>' + (k + 1) + '</button>';
          }).join("") +
        '</nav>' +
        '<p class="zk-legenda"><span class="zk-tecka zodpovezena"></span> zodpovězeno ' +
          '<span class="zk-tecka oznacena"></span> označeno k revizi</p>' +
        '<div class="zk-odevzdat" data-odevzdat-blok>' +
          '<button type="button" class="zk-btn zk-btn--hlavni" data-odevzdat>' +
            (oprava ? 'Ukončit opravu a zobrazit vyhodnocení' : 'Odevzdat test') + '</button>' +
        '</div>' +
      '</div>'
    );
    koren.appendChild(w);

    w.querySelectorAll('input[name="odp"]').forEach(function (inp) {
      inp.addEventListener("change", function () {
        var vybrane = [].slice.call(w.querySelectorAll('input[name="odp"]:checked')).map(function (x) { return +x.value; });
        if (q.vyber > 1 && vybrane.length > q.vyber) {
          inp.checked = false;
          vybrane = vybrane.filter(function (x) { return x !== +inp.value; });
        }
        S.odp[S.i] = vybrane;
        uloz();
        var b = w.querySelector('.zk-mrizka [data-k="' + S.i + '"]');
        b.classList.toggle("zodpovezena", vybrane.length > 0);
        w.querySelector(".zk-lista span:nth-child(2)").textContent = "Zodpovězeno " + zodpovezeno(S.odp) + " / " + N;
      });
    });
    var pr = w.querySelector("[data-preklad]");
    if (pr) pr.onclick = function () {
      var blok = w.querySelector(".zk-preklad");
      var ukaz = blok.hidden;
      blok.hidden = !ukaz;
      pr.setAttribute("aria-expanded", ukaz);
      pr.textContent = ukaz ? "Skrýt český překlad" : "Zobrazit český překlad";
      S.preklady = S.preklady || [];
      if (ukaz && S.preklady.indexOf(S.i) < 0) S.preklady.push(S.i);
      if (!ukaz) S.preklady = S.preklady.filter(function (x) { return x !== S.i; });
      uloz();
    };
    function jdi(k) { S.i = k; uloz(); vykresliTest(); nahoru(); }
    w.querySelector("[data-pred]").onclick = function () { if (S.i > 0) jdi(S.i - 1); };
    w.querySelector("[data-dalsi]").onclick = function () { if (S.i < N - 1) jdi(S.i + 1); };
    w.querySelector("[data-oznacit]").onclick = function () {
      var p = S.oznacene.indexOf(S.i);
      if (p >= 0) S.oznacene.splice(p, 1); else S.oznacene.push(S.i);
      uloz(); vykresliTest();
    };
    w.querySelectorAll(".zk-mrizka button").forEach(function (b) {
      b.onclick = function () { jdi(+b.getAttribute("data-k")); };
    });
    w.querySelector("[data-odevzdat]").onclick = function () { potvrd(w, oprava); };
    spustCasovac();
  }

  function potvrd(w, oprava) {
    var blok = w.querySelector("[data-odevzdat-blok]");
    var chybi = pocet() - zodpovezeno(S.odp);
    var oznac = S.oznacene.length;
    blok.innerHTML =
      '<div class="zk-potvrzeni" role="alertdialog" aria-label="Potvrzení odevzdání">' +
        '<p><strong>' + (oprava ? 'Opravdu ukončit opravu?' : 'Opravdu odevzdat test?') + '</strong></p>' +
        (chybi ? '<p>Nezodpovězených otázek: <strong>' + chybi + '</strong>. Za nezodpovězenou otázku je 0 bodů.</p>' : '') +
        (oznac ? '<p>Otázek označených k revizi: <strong>' + oznac + '</strong>.</p>' : '') +
        '<div class="zk-tlacitka">' +
          '<button type="button" class="zk-btn zk-btn--hlavni" data-ano>' + (oprava ? 'Ano, ukončit' : 'Ano, odevzdat') + '</button>' +
          '<button type="button" class="zk-btn" data-ne>Zpět do testu</button>' +
        '</div>' +
      '</div>';
    blok.querySelector("[data-ano]").onclick = function () { if (oprava) ukonciOpravu(); else odevzdej(); };
    blok.querySelector("[data-ne]").onclick = function () { vykresliTest(); };
    blok.querySelector("[data-ano]").focus();
  }

  function odevzdej() {
    zastavCasovac();
    S.prvni = skore(S.odp);
    S.odpPrvni = S.odp.map(function (o) { return o.slice(); });
    S.faze = "vysledek";
    uloz();
    zapisVysledek(S.prvni);
    vysledek();
  }

  function ukonciOpravu() {
    zastavCasovac();
    S.faze = "vyhodnoceni";
    uloz();
    zapisVysledek(skore(S.odp));
    vyhodnoceni();
  }

  /* --- obrazovka s výsledkem (bez rozboru) --- */
  function vysledek() {
    zastavCasovac();
    var b = S.prvni, celkem = celkemBodu(), hr = hranice();
    var ok = b >= hr;
    koren.innerHTML = "";
    var w = el(
      '<section class="zk-karta zk-vysledek">' +
        '<p class="zk-skore ' + (ok ? "uspech" : "neuspech") + '">' + b + ' <span>/ ' + celkem + ' bodů</span></p>' +
        '<p class="zk-hranice">K úspěchu je potřeba <strong>' + hr + '</strong> bodů (65 %). Správně ' +
          pocetSpravnych(S.odp) + ' z ' + pocet() + ' otázek.</p>' +
        (ok
          ? '<p class="zk-verdikt uspech">Test jste splnili.</p>' +
            '<div class="zk-tlacitka"><button type="button" class="zk-btn zk-btn--hlavni" data-vyhodnoceni>Přejít na vyhodnocení</button></div>'
          : '<p class="zk-verdikt neuspech">Test jste nesplnili — chybí ' + bodu(hr - b) + '.</p>' +
            '<p>Můžete test ukončit a podívat se na rozbor, nebo si dát ještě ' + MINUT_OPRAVA + ' minut na opravu. ' +
            'Při opravě se nedozvíte, které odpovědi jsou špatně — musíte je najít sami.</p>' +
            '<div class="zk-tlacitka">' +
              '<button type="button" class="zk-btn" data-vyhodnoceni>Ukončit test a přejít na vyhodnocení</button>' +
              '<button type="button" class="zk-btn zk-btn--hlavni" data-oprava>Opravit odpovědi (' + MINUT_OPRAVA + ' minut)</button>' +
            '</div>') +
      '</section>'
    );
    koren.appendChild(w);
    w.querySelector("[data-vyhodnoceni]").onclick = function () { S.faze = "vyhodnoceni"; uloz(); vyhodnoceni(); };
    var opr = w.querySelector("[data-oprava]");
    if (opr) opr.onclick = function () {
      S.faze = "oprava";
      S.i = 0;
      S.konec = Date.now() + MINUT_OPRAVA * 60 * 1000;
      uloz();
      vykresliTest();
      nahoru();
    };
    nahoru();
  }

  /* --- vyhodnocení s rozborem --- */
  function pruhy(skupiny, popisek) {
    return Object.keys(skupiny).sort(function (a, b) {
      return a.localeCompare(b, "en", { numeric: true });
    }).map(function (k) {
      var z = skupiny[k];
      return '<li><span>' + popisek(k) + '</span><span class="zk-pruh"><i style="width:' +
        Math.round(z.spravne / z.celkem * 100) + '%"></i></span><strong>' + z.spravne + ' / ' + z.celkem + '</strong></li>';
    }).join("");
  }

  function vyhodnoceni() {
    zastavCasovac();
    zapisLo();
    var b = skore(S.odp), celkem = celkemBodu(), hr = hranice();
    var ok = b >= hr;
    var opraveno = S.odpPrvni && S.odp.some(function (o, i) {
      return o.join() !== (S.odpPrvni[i] || []).join();
    });

    var kapitoly = {}, lo = {};
    OTAZKY.forEach(function (q, i) {
      var k = String(q.lo || "").replace("GenAI-", "").split(".")[0] || "?";
      var body = q.body || 1;
      var z = kapitoly[k] || (kapitoly[k] = { spravne: 0, celkem: 0 });
      z.celkem += body;
      if (spravne(i, S.odp[i])) z.spravne += body;
      var l = lo[q.lo] || (lo[q.lo] = { spravne: 0, celkem: 0 });
      l.celkem++;
      if (spravne(i, S.odp[i])) l.spravne++;
    });
    var chyb = pocet() - pocetSpravnych(S.odp);

    koren.innerHTML = "";
    var w = el(
      '<div class="zk-vyhodnoceni">' +
        '<section class="zk-karta zk-souhrn">' +
          '<p class="zk-skore ' + (ok ? "uspech" : "neuspech") + '">' + b + ' <span>/ ' + celkem + ' bodů</span></p>' +
          '<p class="zk-verdikt ' + (ok ? "uspech" : "neuspech") + '">' +
            (ok ? 'Splněno' : 'Nesplněno') + ' — hranice je ' + hr + ' bodů. Správně ' + pocetSpravnych(S.odp) + ' z ' + pocet() + ' otázek.</p>' +
          (S.odpPrvni && (S.prvni !== b || opraveno)
            ? '<p class="zk-hranice">Po prvním odevzdání: ' + S.prvni + ' / ' + celkem + ', po opravě: ' + b + ' / ' + celkem + '.</p>'
            : '') +
          (S.preklady && S.preklady.length ? '<p class="zk-hranice">Český překlad zobrazen u ' + S.preklady.length + ' otázek.</p>' : '') +
          '<h3>Podle kapitol sylabu (body)</h3>' +
          '<ul class="zk-kapitoly">' + pruhy(kapitoly, function (k) { return "Kapitola " + esc(k); }) + '</ul>' +
          '<details class="zk-lo-det"><summary>Podle studijních cílů (otázky)</summary>' +
            '<ul class="zk-kapitoly zk-kapitoly--lo">' + pruhy(lo, function (k) {
              return '<a href="' + esc(KOREN_WEBU) + 'cile.html#lo-' + esc(String(k).replace("GenAI-", "").replace(/\./g, "-")) + '">' +
                esc(String(k).replace("GenAI-", "")) + '</a>';
            }) + '</ul></details>' +
          '<div class="zk-tlacitka">' +
            '<button type="button" class="zk-btn" aria-pressed="true" data-filtr="vse">Všechny otázky</button>' +
            '<button type="button" class="zk-btn" aria-pressed="false" data-filtr="spatne">Jen chybné (' + chyb + ')</button>' +
            '<button type="button" class="zk-btn" data-znovu>Začít test znovu</button>' +
          '</div>' +
        '</section>' +
        '<div class="zk-rozbor">' + OTAZKY.map(function (q, i) { return rozborOtazky(q, i); }).join("") + '</div>' +
      '</div>'
    );
    koren.appendChild(w);

    w.querySelectorAll("[data-filtr]").forEach(function (t) {
      t.onclick = function () {
        w.querySelectorAll("[data-filtr]").forEach(function (x) { x.setAttribute("aria-pressed", x === t); });
        var jenSpatne = t.getAttribute("data-filtr") === "spatne";
        w.querySelectorAll(".zk-rozbor-otazka").forEach(function (c) {
          c.hidden = jenSpatne && c.classList.contains("spravne");
        });
      };
    });
    w.querySelector("[data-znovu]").onclick = function () { smaz(); S = null; uvod(); nahoru(); };
    nahoru();
  }

  function moznostiRozbor(q, t, odp) {
    return '<ul class="zk-moznosti zk-moznosti--rozbor">' +
      t.m.map(function (m, k) {
        var jeSpravna = q.ok.indexOf(k) >= 0;
        var vybrana = odp.indexOf(k) >= 0;
        var tr = jeSpravna ? "spravna" : (vybrana ? "chybna" : "");
        var vys = (t.vys || {})[PISMENA[k]];
        return '<li class="' + tr + '">' +
          '<div class="zk-moznost-text"><span class="zk-pismeno">' + PISMENA[k] + ')</span> <span>' + m + '</span>' +
            (vybrana ? ' <em class="zk-vase" lang="cs">vaše odpověď</em>' : '') + '</div>' +
          (vys ? '<p class="zk-zduvodneni">' + vys + '</p>' : '') +
        '</li>';
      }).join("") +
    '</ul>' + (t.obecne ? '<div class="zk-obecne">' + t.obecne + '</div>' : '');
  }

  function rozborOtazky(q, i) {
    var odp = S.odp[i];
    var ok = spravne(i, odp);
    var zmena = S.odpPrvni && odp.join() !== (S.odpPrvni[i] || []).join();
    var j = jazyk();
    var t = tx(q);
    var cz = j === "encz" && q.cz
      ? '<details class="zk-preklad-det" lang="cs"><summary>Český překlad otázky a zdůvodnění</summary>' +
          '<div class="zk-zadani">' + q.cz.q + '</div>' + moznostiRozbor(q, q.cz, odp) + '</details>'
      : '';
    return '<article class="zk-karta zk-rozbor-otazka ' + (ok ? "spravne" : "chybne") + '" id="otazka-' + (i + 1) + '">' +
      '<header class="zk-rozbor-hlava">' +
        '<span class="zk-stitek ' + (ok ? "uspech" : "neuspech") + '">' + (ok ? "Správně" : (odp.length ? "Špatně" : "Nezodpovězeno")) + '</span>' +
        '<strong>Otázka ' + (i + 1) + '</strong>' +
        '<span class="zk-meta">' + esc(q.lo) + ' · ' + esc(q.k) + ' · ' + bodu(q.body || 1) + '</span>' +
        (q.zdroj && (!OFICIALNI || NAHODNA) ? '<span class="zk-meta">' + esc(q.zdroj) + '</span>' : '') +
        (S.preklady && S.preklady.indexOf(i) >= 0 ? '<span class="zk-meta">překlad zobrazen</span>' : '') +
        (zmena ? '<span class="zk-meta">změněno při opravě</span>' : '') +
      '</header>' +
      '<div lang="' + (j === "cz" ? "cs" : "en") + '">' +
        '<div class="zk-zadani">' + t.q + '</div>' +
        (q.pozn ? '<p class="zk-poznamka" lang="cs"><strong>Poznámka webu:</strong> ' + q.pozn + '</p>' : '') +
        moznostiRozbor(q, t, odp) +
      '</div>' +
      cz +
      odkazVykladu(q) +
    '</article>';
  }

  /* --- start --- */
  var ulozeny = pripravStav(nacti());
  if (ulozeny && ulozeny.faze === "vyhodnoceni") { S = ulozeny; vyhodnoceni(); }
  else if (ulozeny && ulozeny.faze === "vysledek") { S = ulozeny; vysledek(); }
  else uvod();
})();
