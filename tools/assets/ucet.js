/* Přihlášení Google účtem a uložení postupu do Firebase.
   Web funguje i bez přihlášení: postup je v localStorage (klíče genai-*), jako dřív.
   Tento skript si u každého klíče genai-* pamatuje čas poslední změny (genai-ucet-casy).
   Když je vyplněná konfigurace (assets/ucet-konfig.js) a stránka běží na http(s),
   ukáže v hlavičce tlačítko Přihlásit. Přihlášený uživatel má ve Firestore jeden
   dokument uzivatele/{uid}:
     stav  JSON {klíč localStorage: hodnota, nebo null = smazáno}
     casy  JSON {klíč: čas změny v ms}
   Slučování: u každého klíče vyhrává novější změna. Klíč změněný na tomto zařízení ještě
   před prvním přihlášením (bez času) se s cloudem sloučí po položkách, aby se nic neztratilo.
   Firebase SDK se používá jen na přihlášení, Firestore se volá přes REST.
   Lokální testy (genai-lokalni-*) se do účtu neukládají. */
(function () {
  "use strict";

  var PREFIX = "genai-";
  var KLIC_CASY = PREFIX + "ucet-casy";
  var KLIC_PRIHLASEN = PREFIX + "ucet-prihlasen";
  var VERZE_SDK = "12.4.0";
  var ODLOZENI = 2000;          // ms od poslední změny do uložení
  var ZNOVU_PO_CHYBE = 30000;
  var STAHNOUT_PO = 30000;      // po návratu na záložku stáhnout změny z jiných zařízení

  function synchronizovany(k) {
    return typeof k === "string" && k.indexOf(PREFIX) === 0 &&
      k.indexOf(PREFIX + "ucet-") !== 0 && k.indexOf(PREFIX + "lokalni-") !== 0;
  }

  var uloziste;
  try { uloziste = window.localStorage; } catch (e) { return; /* soukromý režim */ }
  if (!uloziste) return;

  var proto = Object.getPrototypeOf(uloziste);
  var puvodniSet = proto.setItem, puvodniRemove = proto.removeItem;

  function cti(k) { try { return uloziste.getItem(k); } catch (e) { return null; } }
  function zapisPrimo(k, v) {
    try {
      if (v === null || v === undefined) puvodniRemove.call(uloziste, k);
      else puvodniSet.call(uloziste, k, v);
    } catch (e) { /* plné úložiště */ }
  }

  var casy;
  function nactiCasy() { try { casy = JSON.parse(cti(KLIC_CASY)) || {}; } catch (e) { casy = {}; } }
  function ulozCasy() { zapisPrimo(KLIC_CASY, JSON.stringify(casy)); }
  nactiCasy();

  var poZmene = null;   // po přihlášení naplánuje uložení

  function zaznamenej(k) {
    casy[k] = Date.now();
    ulozCasy();
    if (poZmene) poZmene();
  }

  /* Ostatní skripty ukládají přes localStorage.setItem/removeItem; tady se jen přidá čas změny. */
  proto.setItem = function (k, v) {
    var hlidat = this === uloziste && synchronizovany(k);
    var pred = hlidat ? puvodniGet(k) : null;
    puvodniSet.apply(this, arguments);
    if (hlidat && pred !== String(v)) zaznamenej(String(k));
  };
  proto.removeItem = function (k) {
    var hlidat = this === uloziste && synchronizovany(k) && puvodniGet(k) !== null;
    puvodniRemove.apply(this, arguments);
    if (hlidat) zaznamenej(String(k));
  };
  function puvodniGet(k) { try { return proto.getItem.call(uloziste, k); } catch (e) { return null; } }

  /* Změna v jiné záložce: přepsala genai-ucet-casy, načíst znovu. */
  window.addEventListener("storage", function (u) {
    if (u.key === KLIC_CASY) nactiCasy();
    else if (synchronizovany(u.key) && poZmene) poZmene();
  });

  /* --- odtud jen s konfigurací a na webu -------------------------------- */

  var K = window.GENAI_FIREBASE;
  var naWebu = location.protocol === "https:" || location.protocol === "http:";
  if (!K || !K.apiKey || !K.projectId || !naWebu) return;

  var tlacitko = document.querySelector("[data-ucet]");
  var auth = null, slibAuth = null, uzivatel = null;
  var panel = null, zprava = null, stavText = "";
  var bezi = null, jesteJednou = false, casovac = null, posledniCloud = null, naposledyStazeno = 0;
  var interakce = false;

  ["pointerdown", "keydown"].forEach(function (u) {
    document.addEventListener(u, function () { interakce = true; }, { once: true, capture: true });
  });

  function nactiSkript(src) {
    return new Promise(function (hotovo, chyba) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = hotovo;
      s.onerror = function () { chyba(new Error("Nepodařilo se načíst " + src)); };
      document.head.appendChild(s);
    });
  }

  function pripravAuth() {
    if (slibAuth) return slibAuth;
    var cdn = "https://www.gstatic.com/firebasejs/" + VERZE_SDK + "/";
    slibAuth = nactiSkript(cdn + "firebase-app-compat.js")
      .then(function () { return nactiSkript(cdn + "firebase-auth-compat.js"); })
      .then(function () {
        var app = window.firebase.apps.length ? window.firebase.app() : window.firebase.initializeApp(K);
        auth = app.auth();
        auth.languageCode = "cs";
        auth.onAuthStateChanged(zmenaUzivatele);
        return auth;
      });
    slibAuth.catch(function () {
      slibAuth = null;
      if (tlacitko) tlacitko.textContent = "Přihlásit";
    });
    return slibAuth;
  }

  /* --- Firestore přes REST ---------------------------------------------- */

  function adresa() {
    return "https://firestore.googleapis.com/v1/projects/" + encodeURIComponent(K.projectId) +
      "/databases/(default)/documents/uzivatele/" + encodeURIComponent(uzivatel.uid);
  }

  function dotaz(metoda, telo, keepalive) {
    return uzivatel.getIdToken().then(function (token) {
      var nastaveni = { method: metoda, headers: { Authorization: "Bearer " + token } };
      if (telo) {
        nastaveni.headers["Content-Type"] = "application/json";
        nastaveni.body = JSON.stringify(telo);
      }
      if (keepalive) nastaveni.keepalive = true;
      return fetch(adresa(), nastaveni);
    }).then(function (r) {
      if (!r.ok && !(metoda === "GET" && r.status === 404)) throw new Error("Firestore " + metoda + " " + r.status);
      return r;
    });
  }

  function stahni() {
    return dotaz("GET").then(function (r) {
      if (r.status === 404) return { stav: {}, casy: {} };
      return r.json().then(function (d) {
        var f = d.fields || {};
        function pole(n) { try { return JSON.parse(f[n].stringValue) || {}; } catch (e) { return {}; } }
        return { stav: pole("stav"), casy: pole("casy") };
      });
    });
  }

  function nahraj(dok, keepalive) {
    return dotaz("PATCH", { fields: {
      stav: { stringValue: JSON.stringify(dok.stav) },
      casy: { stringValue: JSON.stringify(dok.casy) },
      upraveno: { timestampValue: new Date().toISOString() }
    } }, keepalive);
  }

  /* --- slučování ---------------------------------------------------------- */

  function mistni() {
    var stav = {}, c = {};
    for (var i = 0; i < uloziste.length; i++) {
      var k = uloziste.key(i);
      if (synchronizovany(k)) { stav[k] = cti(k); c[k] = casy[k] || 0; }
    }
    Object.keys(casy).forEach(function (k) {
      if (!(k in stav) && synchronizovany(k)) { stav[k] = null; c[k] = casy[k]; }
    });
    return { stav: stav, casy: c };
  }

  function jeObjekt(x) { return !!x && typeof x === "object" && !Array.isArray(x); }

  /* Sloučení po položkách; při shodě klíče vyhrává b. */
  function sluc(a, b) {
    var v = {};
    Object.keys(a).forEach(function (k) { v[k] = a[k]; });
    Object.keys(b).forEach(function (k) { v[k] = jeObjekt(a[k]) && jeObjekt(b[k]) ? sluc(a[k], b[k]) : b[k]; });
    return v;
  }

  function slucText(mist, cloud) {
    try {
      var a = JSON.parse(mist), b = JSON.parse(cloud);
      if (jeObjekt(a) && jeObjekt(b)) return JSON.stringify(sluc(a, b));
    } catch (e) { /* není JSON */ }
    return cloud;
  }

  function spoj(mist, cloud) {
    var vysl = { stav: {}, casy: {} }, ted = Date.now(), klice = {};
    Object.keys(mist.stav).concat(Object.keys(cloud.stav)).forEach(function (k) { klice[k] = true; });
    Object.keys(klice).forEach(function (k) {
      if (!synchronizovany(k)) return;
      var mv = mist.stav[k], cv = cloud.stav[k];
      var mt = mist.casy[k] || 0, ct = cloud.casy[k] || 0;
      var v, t;
      if (!(k in mist.stav)) { v = cv; t = ct; }
      else if (!(k in cloud.stav)) { v = mv; t = mt || ted; }
      else if (mt === 0) {
        v = mv !== null && cv !== null ? slucText(mv, cv) : (mv !== null ? mv : cv);
        t = v === cv ? ct : ted;
      }
      else if (mt >= ct) { v = mv; t = mt; }
      else { v = cv; t = ct; }
      vysl.stav[k] = v === undefined ? null : v;
      vysl.casy[k] = t;
    });
    return vysl;
  }

  function stejne(a, b) {
    var ka = Object.keys(a.stav), kb = Object.keys(b.stav);
    if (ka.length !== kb.length) return false;
    return ka.every(function (k) { return a.stav[k] === b.stav[k] && a.casy[k] === b.casy[k]; });
  }

  /* --- synchronizace ------------------------------------------------------ */

  function cas() {
    var d = new Date();
    return d.getHours() + ":" + String(d.getMinutes()).padStart(2, "0");
  }

  function naplanuj() {
    clearTimeout(casovac);
    casovac = setTimeout(synchronizuj, ODLOZENI);
    nastavStav("Změny se za chvíli uloží do účtu.");
  }

  /* Stáhne dokument, sloučí s localStorage, zapíše obě strany. duvod: "start", "prihlaseni", "navrat". */
  function synchronizuj(duvod) {
    if (!uzivatel) return Promise.resolve();
    if (bezi) { jesteJednou = true; return bezi; }
    clearTimeout(casovac);
    casovac = null;
    var kdo = uzivatel;
    bezi = stahni().then(function (cloud) {
      if (uzivatel !== kdo) return false;
      naposledyStazeno = Date.now();
      var vysl = spoj(mistni(), cloud), zmena = false;
      Object.keys(vysl.stav).forEach(function (k) {
        if (cti(k) !== vysl.stav[k]) { zapisPrimo(k, vysl.stav[k]); zmena = true; }
        casy[k] = vysl.casy[k];
      });
      ulozCasy();
      posledniCloud = vysl;
      return (stejne(vysl, cloud) ? Promise.resolve() : nahraj(vysl)).then(function () { return zmena; });
    }).then(function (zmena) {
      bezi = null;
      nastavStav("Postup je uložený v účtu (" + cas() + ").");
      if (zmena) noveData(duvod);
      if (jesteJednou) { jesteJednou = false; naplanuj(); }
    }, function (chyba) {
      bezi = null;
      if (window.console) console.warn("Uložení postupu do účtu:", chyba);
      nastavStav("Uložení do účtu se nepovedlo, zkusím to znovu. Postup je zatím v tomto prohlížeči.");
      casovac = setTimeout(synchronizuj, ZNOVU_PO_CHYBE);
    });
    return bezi;
  }

  /* Odchod ze stránky: neuložené změny poslat hned, bez čekání na stažení. */
  function odesliHned() {
    if (!uzivatel || !casovac || !posledniCloud) return;
    clearTimeout(casovac);
    casovac = null;
    var vysl = spoj(mistni(), posledniCloud);
    posledniCloud = vysl;
    nahraj(vysl, true).catch(function () { /* dorovná se při další návštěvě */ });
  }

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") odesliHned();
    else if (uzivatel && Date.now() - naposledyStazeno > STAHNOUT_PO) synchronizuj("navrat");
  });
  window.addEventListener("pagehide", odesliHned);

  /* Z účtu přišla jiná data, než stránka vykreslila. */
  function noveData(duvod) {
    var znovu = false;
    try {
      znovu = Date.now() - (+sessionStorage.getItem(PREFIX + "ucet-obnoveno") || 0) < 10000;
    } catch (e) { /* nevadí */ }
    if (!znovu && (duvod === "prihlaseni" || (duvod === "start" && !interakce))) {
      try { sessionStorage.setItem(PREFIX + "ucet-obnoveno", String(Date.now())); } catch (e) { /* nevadí */ }
      location.reload();
      return;
    }
    ukazZpravu("Z jiného zařízení přibyl postup.", "Obnovit stránku", function () { location.reload(); });
  }

  /* --- přihlášení ---------------------------------------------------------- */

  var CHYBY = {
    "auth/popup-blocked": "Prohlížeč zablokoval okno přihlášení. Povol pro tuto stránku vyskakovací okna a zkus to znovu.",
    "auth/unauthorized-domain": "Tahle adresa není ve Firebase povolená (Authentication → Settings → Authorized domains).",
    "auth/network-request-failed": "Přihlášení se nepovedlo, zkontroluj připojení k internetu.",
    "auth/operation-not-allowed": "Přihlášení Googlem není ve Firebase zapnuté."
  };

  var cekaPrihlaseni = false;

  function prihlas() {
    pripravAuth().then(function (a) {
      cekaPrihlaseni = true;
      return a.signInWithPopup(new window.firebase.auth.GoogleAuthProvider());
    }).catch(function (chyba) {
      cekaPrihlaseni = false;
      var kod = chyba && chyba.code;
      if (kod === "auth/popup-closed-by-user" || kod === "auth/cancelled-popup-request") return;
      ukazZpravu(CHYBY[kod] || "Přihlášení se nepovedlo." + (kod ? " (" + kod + ")" : ""));
    });
  }

  function zmenaUzivatele(u) {
    var duvod = cekaPrihlaseni ? "prihlaseni" : "start";
    cekaPrihlaseni = false;
    uzivatel = u;
    posledniCloud = null;
    if (u) {
      zapisPrimo(KLIC_PRIHLASEN, "1");
      poZmene = naplanuj;
      nastavStav("Načítám postup z účtu…");
      synchronizuj(duvod);
    } else {
      zapisPrimo(KLIC_PRIHLASEN, null);
      poZmene = null;
      clearTimeout(casovac);
      casovac = null;
    }
    vykresli();
  }

  function odhlas() {
    var hotovo = casovac ? synchronizuj() : Promise.resolve();
    hotovo.then(function () { return auth.signOut(); }).then(function () {
      zavriPanel();
      ukazZpravu("Odhlášeno. Postup zůstává i v tomto prohlížeči.");
    });
  }

  function smazZUctu() {
    if (!confirm("Smazat postup uložený v Google účtu?\n\nV tomto prohlížeči postup zůstane. Zároveň tě odhlásím.")) return;
    clearTimeout(casovac);
    casovac = null;
    poZmene = null;
    dotaz("DELETE").then(function () { return auth.signOut(); }).then(function () {
      zavriPanel();
      ukazZpravu("Postup z účtu je smazaný a jsi odhlášený.");
    }, function () {
      poZmene = naplanuj;
      ukazZpravu("Smazání se nepovedlo, zkus to prosím znovu.");
    });
  }

  /* --- vzhled --------------------------------------------------------------- */

  function el(tag, trida, text) {
    var x = document.createElement(tag);
    if (trida) x.className = trida;
    if (text !== undefined) x.textContent = text;
    return x;
  }

  function nastavStav(text) {
    stavText = text;
    var p = panel && panel.querySelector(".ucet-stav");
    if (p) p.textContent = text;
  }

  function ukazZpravu(text, akce, poKliku) {
    if (!zprava) {
      zprava = el("div", "ucet-zprava");
      zprava.setAttribute("role", "status");
      document.body.appendChild(zprava);
    }
    zprava.textContent = "";
    zprava.appendChild(el("span", "", text));
    if (akce) {
      var b = el("button", "tlacitko", akce);
      b.type = "button";
      b.addEventListener("click", poKliku);
      zprava.appendChild(b);
    }
    var zavrit = el("button", "ucet-zavrit", "×");
    zavrit.type = "button";
    zavrit.setAttribute("aria-label", "Zavřít zprávu");
    zavrit.addEventListener("click", function () { zprava.hidden = true; });
    zprava.appendChild(zavrit);
    zprava.hidden = false;
    if (!akce) setTimeout(function () { if (zprava) zprava.hidden = true; }, 6000);
  }

  function zavriPanel() {
    if (!panel) return;
    panel.hidden = true;
    tlacitko.setAttribute("aria-expanded", "false");
  }

  function otevriPanel() {
    if (!panel) {
      panel = el("div", "ucet-panel");
      panel.id = "ucet-panel";
      panel.hidden = true;
      tlacitko.setAttribute("aria-controls", panel.id);
      tlacitko.parentNode.insertBefore(panel, tlacitko.nextSibling);
      document.addEventListener("click", function (u) {
        if (!panel.hidden && !panel.contains(u.target) && u.target !== tlacitko) zavriPanel();
      });
      document.addEventListener("keydown", function (u) {
        if (u.key === "Escape" && !panel.hidden) { zavriPanel(); tlacitko.focus(); }
      });
    }
    panel.textContent = "";
    var kdo = el("p", "ucet-kdo");
    kdo.appendChild(el("strong", "", uzivatel.displayName || "Přihlášený uživatel"));
    if (uzivatel.email) kdo.appendChild(el("span", "", uzivatel.email));
    panel.appendChild(kdo);
    panel.appendChild(el("p", "ucet-stav", stavText));
    var akce = el("div", "ucet-akce");
    var odhlasit = el("button", "tlacitko", "Odhlásit");
    odhlasit.type = "button";
    odhlasit.addEventListener("click", odhlas);
    var smazat = el("button", "tlacitko ucet-smazat", "Smazat postup z účtu");
    smazat.type = "button";
    smazat.addEventListener("click", smazZUctu);
    akce.append(odhlasit, smazat);
    panel.appendChild(akce);
    panel.appendChild(el("p", "ucet-pozn",
      "Do účtu se ukládá jen postup na tomto webu (testy, kartičky, cvičení, splněné části). " +
      "E-mail a jméno zná přihlášení Google a vidí je jen správce webu."));
    panel.hidden = false;
    tlacitko.setAttribute("aria-expanded", "true");
  }

  function vykresli() {
    if (!tlacitko) return;
    tlacitko.hidden = false;
    if (uzivatel) {
      var jmeno = (uzivatel.displayName || "").split(" ")[0] || "Účet";
      tlacitko.textContent = "✓ " + jmeno;
      tlacitko.title = "Přihlášen Google účtem, postup se ukládá do účtu";
      tlacitko.classList.add("ucet-tlacitko--prihlasen");
      tlacitko.setAttribute("aria-haspopup", "true");
      tlacitko.setAttribute("aria-expanded", panel && !panel.hidden ? "true" : "false");
    } else {
      tlacitko.textContent = "Přihlásit";
      tlacitko.title = "Přihlásit se Google účtem a mít postup na všech zařízeních";
      tlacitko.classList.remove("ucet-tlacitko--prihlasen");
      tlacitko.removeAttribute("aria-haspopup");
      tlacitko.removeAttribute("aria-expanded");
      zavriPanel();
    }
  }

  function start() {
    tlacitko = document.querySelector("[data-ucet]");
    [].forEach.call(document.querySelectorAll("[data-ucet-info]"), function (x) { x.hidden = false; });
    if (!tlacitko) return;
    tlacitko.hidden = false;
    tlacitko.textContent = cti(KLIC_PRIHLASEN) ? "Účet…" : "Přihlásit";
    tlacitko.addEventListener("click", function () {
      if (!uzivatel) prihlas();
      else if (panel && !panel.hidden) zavriPanel();
      else otevriPanel();
    });
    /* SDK se načte hned, aby okno přihlášení otevřel přímo klik (jinak ho prohlížeč zablokuje). */
    pripravAuth();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
