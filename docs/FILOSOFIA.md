# Filosofia di FreeTool (leggere prima di toccare qualsiasi cosa)

**Dominio reale:** freetool.ipermark.com (DNS: CNAME `freetool` -> `cialdecompatibili-netizen.github.io`; poi file `CNAME` nella radice e dominio personalizzato nelle impostazioni Pages).

## A cosa serve questo sito
E' uno **smoke test (porta finta)**: un catalogo di strumenti online gratuiti in stile iLovePDF. **Gli strumenti NON funzionano ancora, di proposito.**
Quando una persona sceglie uno strumento e carica un file, il sito la invita a **registrarsi solo con l'email**. Ogni registrazione e' un segnale di domanda:
dice quale strumento le serviva. Cosi' si capisce **dove vale la pena sviluppare** prima di spendere tempo.

## Flusso
1. Home = griglia di tutti gli strumenti (ricerca + categorie). Ogni strumento ha la sua pagina SEO: `/strumenti/<id>/` (IT), `/en/tools/<id>/` (EN).
2. Pagina strumento = dropzone. Scelto un file (o incollato un indirizzo) compare la registrazione con la sola email.
3. **Il file non lascia mai il browser.** Si leggono solo numero, estensione e peso. Non scrivere mai che il file e' stato elaborato.
4. La registrazione va al worker Cloudflare **contatti-form** (`C:\Users\mirco\Desktop\claudetemp\contatti-worker`, antispam ALTCHA + honeypot + tempo minimo) che la scrive nel **foglio Google** (voce "Messaggi" dell'admin). Riconoscibile da: nome `Registrazione FreeTool`, tipo `registrazione-tool`, messaggio `Strumento richiesto: <id> ...`.
5. Lo stesso utente, dopo la prima volta, non reinserisce l'email (localStorage `ft_email`): ogni nuovo strumento provato e' un nuovo voto.

## Il catalogo
- Obiettivo: **tutti gli strumenti utili del mondo, in ordine di profitto/domanda**. Si parte dai PDF; poi immagini, video e audio, ufficio e fatture, testi, LLM e IA, sviluppatori, SEO e marketing, studenti, immobiliare, HR, ecc.
- Fonte unica: `assets/data/strumenti.json` (settori > categorie > strumenti). **L'ordine nel file e' la priorita' di profitto.** Un nuovo settore = una voce in `settori`, le sue `categorie` e i suoi `strumenti`: i tab compaiono da soli.
- Dopo ogni modifica: `python automation\genera_strumenti.py` (crea le pagine IT+EN e il fallback della home), poi `python automation\allinea_hash.py`, commit e push.
- Per sapere cosa sviluppare: leggere il foglio, contare le righe per `Strumento richiesto`.

## Come diventano veri (dopo i dati)
Si sviluppa solo cio' che la gente chiede. Gli strumenti si installano **una volta sola sulla VPS** e poi girano **gratis a vita, senza costi per ogni uso**: software open source self-hosted (Stirling-PDF, ConvertX, LibreOffice, ffmpeg, Pandoc, Tesseract, ImageMagick, modelli LLM locali). Il sito GitHub resta la vetrina; la VPS sta accanto alla repo.
Modello previsto: registrazione, alcuni crediti gratis al giorno con reset dopo qualche ora, poi a pagamento (idea stile freemium).

## Regole
- Niente promesse false: nessun "file elaborato", nessun download finto.
- Email usata solo per avvisare quando lo strumento e' attivo.
- Non riusare il worker per clienti: questo e' il worker personale `contatti-form`.
