/* FreeTool - catalogo strumenti + registrazione (smoke test).
   NIENTE file caricati: il browser legge solo nome/tipo del file scelto. Si invia solo email + strumento richiesto al worker contatti-form.
   Dati: assets/data/strumenti.json (un solo file: aggiungere strumenti = aggiungere righe li'). Home = griglia; pagina strumento = dropzone + registrazione. */
(function () {
  'use strict';
  var app = document.getElementById('ft-app');
  if (!app) return;
  var L = app.getAttribute('data-lang') === 'en' ? 'en' : 'it';
  var MODE = app.getAttribute('data-mode') || 'home';
  var TOOL = app.getAttribute('data-tool') || '';
  var BASE = (app.getAttribute('data-base') || '').replace(/\/+$/, '');
  var ENDPOINT = app.getAttribute('data-endpoint') || '';
  var T0 = Date.now();

  var TX = {
    it: {
      h1: 'Tutti gli strumenti che ti servono, gratis', sub: 'Documenti, PDF, immagini e molto altro: scegli lo strumento, carica il file e fai in un attimo.',
      cerca: 'Cerca uno strumento (es. unisci, comprimi, word...)', tutti: 'Tutti', nuovo: 'Nuovo', vuoto: 'Nessuno strumento trovato. Scrivici quale ti serve: lo aggiungiamo.',
      altri: 'Altri strumenti', home: 'Tutti gli strumenti', sel: 'Seleziona file', selUrl: 'Scegli un indirizzo web', vai: 'Continua', trascina: 'oppure trascina qui il file',
      urlPh: 'https://www.esempio.it', testoPh: 'Incolla qui il testo',
      mTit: 'Crea il tuo account gratuito', mTxt: 'Per usare questo strumento gratis basta la tua email. Nessun file viene caricato: resta sul tuo dispositivo.',
      email: 'La tua email', reg: 'Registrati gratis', annulla: 'Chiudi', priv: 'Usiamo la tua email solo per avvisarti quando lo strumento e\' attivo.',
      okT: 'Sei dentro!', okP: 'Stiamo aprendo gli strumenti a gruppi: ti scriviamo all\'email indicata appena questo e\' attivo. Intanto guarda gli altri.',
      errEmail: 'Inserisci un\'email valida.', errNet: 'Invio non riuscito. Riprova tra poco.', errOff: 'Registrazione non ancora attiva.', invio: 'Invio in corso...',
      sc: 'Strumenti online gratuiti', f1: 'Gratis per iniziare', f2: 'Nessuna installazione', f3: 'I tuoi file restano tuoi',
      f1t: 'Usa gli strumenti ogni giorno senza pagare.', f2t: 'Funziona nel browser, da computer e telefono.', f3t: 'Non carichiamo i tuoi file in questa fase.',
      manca: 'Ti manca uno strumento? Dicci quale', manca2: 'Scrivici'
    },
    en: {
      h1: 'Every tool you need, for free', sub: 'Documents, PDFs, images and more: pick a tool, add your file and get it done in seconds.',
      cerca: 'Search a tool (e.g. merge, compress, word...)', tutti: 'All', nuovo: 'New', vuoto: 'No tool found. Tell us which one you need and we will add it.',
      altri: 'More tools', home: 'All tools', sel: 'Select file', selUrl: 'Enter a web address', vai: 'Continue', trascina: 'or drop your file here',
      urlPh: 'https://www.example.com', testoPh: 'Paste your text here',
      mTit: 'Create your free account', mTxt: 'To use this tool for free all you need is your email. No file is uploaded: it stays on your device.',
      email: 'Your email', reg: 'Sign up free', annulla: 'Close', priv: 'We only use your email to tell you when the tool is live.',
      okT: 'You are in!', okP: 'We are opening the tools in groups: we will email you as soon as this one is live. Meanwhile, check out the others.',
      errEmail: 'Please enter a valid email.', errNet: 'Could not send. Please try again shortly.', errOff: 'Sign-up is not active yet.', invio: 'Sending...',
      sc: 'Free online tools', f1: 'Free to start', f2: 'No installation', f3: 'Your files stay yours',
      f1t: 'Use the tools every day without paying.', f2t: 'Works in your browser, on computer and phone.', f3t: 'We do not upload your files at this stage.',
      manca: 'Missing a tool? Tell us which one', manca2: 'Write to us'
    }
  };
  var tx = TX[L];

  function h(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function toolUrl(id) { return BASE + (L === 'en' ? '/en/tools/' : '/strumenti/') + id + '/'; }
  function homeUrl() { return BASE + (L === 'en' ? '/en/' : '/'); }
  function contactUrl() { return BASE + (L === 'en' ? '/en/contact/' : '/contatti/'); }

  /* CSS caricato dal JS: un solo file da includere nelle pagine */
  var me = document.querySelector('script[src*="freetool.js"]');
  if (me) { var lk = document.createElement('link'); lk.rel = 'stylesheet'; lk.href = me.src.replace(/js\/freetool\.js.*$/, 'css/freetool.css?v=1'); document.head.appendChild(lk); }

  var DATA = null;
  function cat(id) { for (var i = 0; i < DATA.categorie.length; i++) if (DATA.categorie[i].id === id) return DATA.categorie[i]; return { colore: '#e5322d' }; }
  function toolById(id) { for (var i = 0; i < DATA.strumenti.length; i++) if (DATA.strumenti[i].id === id) return DATA.strumenti[i]; return null; }

  function card(t) {
    var c = cat(t.cat);
    var a = h('a', 'ft-card');
    a.href = toolUrl(t.id);
    a.innerHTML = (t.nuovo ? '<span class="ft-new">' + tx.nuovo + '</span>' : '') +
      '<span class="ft-ico" style="background:' + c.colore + '">' + t.ico + '</span>' +
      '<b>' + esc(t[L][0]) + '</b><span class="ft-d">' + esc(t[L][1]) + '</span>';
    return a;
  }

  /* ---------------------------------- HOME ---------------------------------- */
  function home() {
    var st = { q: '', sett: DATA.settori[0].id, cat: 'all', tutti: true };
    app.innerHTML = '';
    app.className = 'ft ft-home';
    var hero = h('section', 'ft-hero');
    hero.innerHTML = '<h1>' + tx.h1 + '</h1><p>' + tx.sub + '</p>';
    var q = h('input', 'ft-q'); q.type = 'search'; q.placeholder = tx.cerca; q.setAttribute('aria-label', tx.cerca);
    hero.appendChild(q);
    var tabs = h('div', 'ft-tabs');
    var grid = h('div', 'ft-grid');
    app.appendChild(hero); app.appendChild(tabs); app.appendChild(grid);

    function drawTabs() {
      tabs.innerHTML = '';
      if (DATA.settori.length > 1) {
        var row = h('div', 'ft-sett');
        var all = h('button', 'ft-pill' + (st.tutti ? ' on' : ''), tx.tutti); all.type = 'button';
        all.onclick = function () { st.tutti = true; st.cat = 'all'; draw(); };
        row.appendChild(all);
        DATA.settori.forEach(function (s) {
          var b = h('button', 'ft-pill' + (!st.tutti && st.sett === s.id ? ' on' : ''), esc(s[L])); b.type = 'button';
          b.onclick = function () { st.tutti = false; st.sett = s.id; st.cat = 'all'; draw(); };
          row.appendChild(b);
        });
        tabs.appendChild(row);
      }
      var row2 = h('div', 'ft-cats');
      var b0 = h('button', 'ft-pill' + (st.cat === 'all' ? ' on' : ''), tx.tutti); b0.type = 'button';
      b0.onclick = function () { st.cat = 'all'; draw(); };
      row2.appendChild(b0);
      DATA.categorie.forEach(function (c) {
        if (!st.tutti && c.settore !== st.sett) return;
        var b = h('button', 'ft-pill' + (st.cat === c.id ? ' on' : ''), esc(c[L])); b.type = 'button';
        b.onclick = function () { st.cat = c.id; draw(); };
        row2.appendChild(b);
      });
      tabs.appendChild(row2);
    }
    function drawGrid() {
      grid.innerHTML = '';
      var n = 0, s = st.q.toLowerCase();
      DATA.strumenti.forEach(function (t) {
        var c = cat(t.cat);
        if (!st.tutti && c.settore !== st.sett) return;
        if (st.cat !== 'all' && t.cat !== st.cat) return;
        if (s && (t[L][0] + ' ' + t[L][1]).toLowerCase().indexOf(s) < 0) return;
        grid.appendChild(card(t)); n++;
      });
      if (!n) grid.appendChild(h('p', 'ft-vuoto', tx.vuoto));
    }
    function draw() { drawTabs(); drawGrid(); }
    q.addEventListener('input', function () { st.q = q.value; drawGrid(); });
    draw();

    var f = h('section', 'ft-feat');
    f.innerHTML = '<div><b>' + tx.f1 + '</b><span>' + tx.f1t + '</span></div><div><b>' + tx.f2 + '</b><span>' + tx.f2t + '</span></div><div><b>' + tx.f3 + '</b><span>' + tx.f3t + '</span></div>';
    app.appendChild(f);
    var m = h('p', 'ft-manca', tx.manca + ' - <a href="' + contactUrl() + '">' + tx.manca2 + '</a>');
    app.appendChild(m);
  }

  /* ---------------------------------- ALTCHA (stessa prova del form contatti) ---------------------------------- */
  var pre = null, preT = 0;
  function hex(b) { return Array.prototype.map.call(new Uint8Array(b), function (x) { return ('0' + x.toString(16)).slice(-2); }).join(''); }
  async function altcha() {
    var sep = ENDPOINT.indexOf('?') < 0 ? '?' : '&';
    var c = await (await fetch(ENDPOINT + sep + 'challenge=1')).json();
    if (!c.challenge) throw new Error('altcha');
    var enc = new TextEncoder();
    for (var n = 0; n <= c.maxnumber; n++) {
      if (hex(await crypto.subtle.digest('SHA-256', enc.encode(c.salt + n))) === c.challenge) {
        return btoa(JSON.stringify({ algorithm: c.algorithm, challenge: c.challenge, number: n, salt: c.salt, signature: c.signature }));
      }
    }
    throw new Error('altcha');
  }
  function prepara() { preT = Date.now(); pre = altcha().catch(function () { return ''; }); }
  function token() {
    if (!pre || Date.now() - preT > 480000) prepara();
    return pre.then(function (v) { if (v) return v; prepara(); return pre; });
  }

  function saved() { try { return localStorage.getItem('ft_email') || ''; } catch (e) { return ''; } }
  function save(v) { try { localStorage.setItem('ft_email', v); } catch (e) { } }

  /* invia: nome fisso, email, messaggio = strumento + riepilogo file (solo nome estensione/numero). Ritorna Promise<bool> */
  function invia(email, tool, riepilogo) {
    if (!ENDPOINT) return Promise.resolve('off');
    var attesa = Math.max(0, 3600 - (Date.now() - T0));
    return new Promise(function (r) { setTimeout(r, attesa); }).then(token).then(function (tk) {
      if (!tk) return 'net';
      var d = new URLSearchParams();
      d.set('nome', 'Registrazione FreeTool');
      d.set('email', email);
      d.set('messaggio', 'Strumento richiesto: ' + tool.id + ' (' + tool.it[0] + ') | ' + riepilogo + ' | lingua: ' + L);
      d.set('altcha', tk); d.set('t', String(T0)); d.set('tipo', 'registrazione-tool');
      d.set('sito', location.hostname); d.set('pagina', location.pathname);
      return fetch(ENDPOINT, { method: 'POST', body: d }).then(function (r) { return r.json(); }).then(function (j) { prepara(); return j.status === 'ok' ? 'ok' : 'net'; });
    }).catch(function () { return 'net'; });
  }

  /* ---------------------------------- PAGINA STRUMENTO ---------------------------------- */
  function pagina() {
    var t = toolById(TOOL);
    if (!t) { app.innerHTML = '<p class="ft-vuoto"><a href="' + homeUrl() + '">' + tx.home + '</a></p>'; return; }
    var c = cat(t.cat);
    app.innerHTML = ''; app.className = 'ft ft-tool';
    if (ENDPOINT) prepara();
    var bc = h('p', 'ft-bc', '<a href="' + homeUrl() + '">' + tx.home + '</a> &rsaquo; ' + esc(c[L]));
    var box = h('section', 'ft-box');
    box.innerHTML = '<span class="ft-ico big" style="background:' + c.colore + '">' + t.ico + '</span><h1>' + esc(t[L][0]) + '</h1><p>' + esc(t[L][1]) + '</p>';
    app.appendChild(bc); app.appendChild(box);

    var drop = h('div', 'ft-drop'); box.appendChild(drop);
    var picked = '';
    function prosegui(riep) {
      picked = riep;
      var em = saved();
      if (em) { fatto(em, riep, true); } else { modale(); }
    }
    if (t.input === 'url' || t.input === 'testo') {
      var inp = t.input === 'url' ? h('input', 'ft-url') : h('textarea', 'ft-url ft-ta');
      if (t.input === 'url') { inp.type = 'url'; inp.placeholder = tx.urlPh; } else { inp.placeholder = tx.testoPh; inp.rows = 6; }
      var go = h('button', 'ft-btn', tx.vai); go.type = 'button';
      go.onclick = function () { if (!inp.value.trim()) { inp.focus(); return; } prosegui(t.input + ': ' + inp.value.trim().slice(0, 120)); };
      drop.appendChild(inp); drop.appendChild(go);
    } else {
      var fi = h('input'); fi.type = 'file'; fi.hidden = true; if (t.accept) fi.accept = t.accept; if (t.multi) fi.multiple = true;
      var b = h('button', 'ft-btn big', tx.sel); b.type = 'button';
      var ou = h('span', 'ft-or', tx.trascina);
      drop.appendChild(b); drop.appendChild(ou); drop.appendChild(fi);
      function files(fl) {
        if (!fl || !fl.length) return;
        var ext = {}, kb = 0;
        for (var i = 0; i < fl.length; i++) { var m = /\.([A-Za-z0-9]+)$/.exec(fl[i].name); var e = m ? m[1].toLowerCase() : '?'; ext[e] = 1; kb += fl[i].size / 1024; }
        prosegui('file: ' + fl.length + 'x ' + Object.keys(ext).join('/') + ' ' + Math.round(kb) + 'KB');
      }
      b.onclick = function () { fi.click(); };
      fi.onchange = function () { files(fi.files); fi.value = ''; };
      ['dragenter', 'dragover'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('over'); }); });
      ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('over'); }); });
      drop.addEventListener('drop', function (e) { files(e.dataTransfer && e.dataTransfer.files); });
    }

    function fatto(email, riep, auto) {
      var stato = h('div', 'ft-stato', '<p>' + tx.invio + '</p>');
      drop.replaceWith(stato);
      invia(email, t, riep).then(function (r) {
        if (r === 'ok') {
          stato.innerHTML = '<h2>' + tx.okT + '</h2><p>' + tx.okP + '</p>';
        } else {
          stato.innerHTML = '<p class="ft-err">' + (r === 'off' ? tx.errOff : tx.errNet) + '</p><button class="ft-btn" type="button">' + tx.vai + '</button>';
          stato.querySelector('button').onclick = function () { stato.replaceWith(drop); };
        }
      });
    }

    function modale() {
      var ov = h('div', 'ft-ov');
      var m = h('form', 'ft-modal');
      m.noValidate = true;
      m.innerHTML = '<h2>' + tx.mTit + '</h2><p>' + tx.mTxt + '</p>' +
        '<input type="email" name="email" placeholder="' + tx.email + '" autocomplete="email" required>' +
        '<input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0">' +
        '<p class="ft-err" hidden></p><button class="ft-btn big" type="submit">' + tx.reg + '</button>' +
        '<button class="ft-x" type="button">' + tx.annulla + '</button><small>' + tx.priv + '</small>';
      ov.appendChild(m); document.body.appendChild(ov);
      var em = m.querySelector('input[name=email]'); em.focus();
      var er = m.querySelector('.ft-err');
      function chiudi() { ov.remove(); }
      m.querySelector('.ft-x').onclick = chiudi;
      ov.addEventListener('click', function (e) { if (e.target === ov) chiudi(); });
      m.addEventListener('submit', function (e) {
        e.preventDefault();
        if (m.website.value) { chiudi(); return; }
        var v = em.value.trim();
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) { er.hidden = false; er.textContent = tx.errEmail; return; }
        save(v); chiudi(); fatto(v, picked, false);
      });
    }

    /* altri strumenti della stessa categoria */
    var altri = h('section', 'ft-altri', '<h2>' + tx.altri + '</h2>');
    var g = h('div', 'ft-grid'); var n = 0;
    DATA.strumenti.forEach(function (x) { if (x.id !== t.id && x.cat === t.cat && n < 6) { g.appendChild(card(x)); n++; } });
    DATA.strumenti.forEach(function (x) { if (x.id !== t.id && x.cat !== t.cat && n < 6) { g.appendChild(card(x)); n++; } });
    altri.appendChild(g); app.appendChild(altri);
    document.title = t[L][0] + ' | FreeTool';
  }

  fetch(BASE + '/assets/data/strumenti.json?v=1').then(function (r) { return r.json(); }).then(function (d) {
    DATA = d; if (MODE === 'tool') pagina(); else home();
  }).catch(function () { app.innerHTML = '<p class="ft-vuoto">...</p>'; });
})();
