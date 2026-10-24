# -*- coding: utf-8 -*-
"""build_freetool_tools.py - AGGIUNGE i nuovi strumenti a freetool/assets/data/strumenti.json (fonte unica del catalogo).
COME FUNZIONA: legge il json, aggiunge solo gli id che NON esistono ancora (rilanciabile senza doppioni),
aggiunge le categorie nuove (estrai, crea), sposta alcuni tool esistenti in 'estrai', poi RIORDINA tutto con PRIORITA:
l'ordine nel file = priorita' di profitto/domanda (pagina settore, ricerca e menu seguono questo ordine).
NON TOCCA i tool esistenti (testi, accept, multi): cambia solo cat per quelli in SPOSTA.
Dopo: python automation\\genera_strumenti.py  e  python automation\\allinea_hash.py"""
import io, json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # radice repo (ricavata da sola)
P = os.path.join(R, "assets", "data", "strumenti.json")
ACC = {
    "pdf": ".pdf,application/pdf", "img": "image/*", "pdfimg": ".pdf,application/pdf,image/*",
    "txt": ".txt,.md,.rtf,.odt", "epub": ".epub,.mobi,.azw,.azw3", "url": "", "odt": ".odt,.rtf",
    "md": ".md,.markdown,.txt", "heic": ".heic,.heif", "tif": ".tif,.tiff", "none": ".pdf,application/pdf",
}
# (id, cat, ico, accept, multi, nuovo, it_nome, it_desc, en_nome, en_desc)
N = []
def T(*a): N.append(a)

# ---------- IA (il nostro punto di forza: servizi con LLM) ----------
T("spiega-contratto","ai","⚖️","pdf",False,True,"Spiega contratto","Il legalese tradotto in italiano semplice, clausola per clausola.","Explain contract","Legalese turned into plain language, clause by clause.")
T("clausole-a-rischio","ai","🚩","pdf",False,True,"Trova clausole a rischio","Evidenzia penali, rinnovi automatici ed esclusività prima di firmare.","Find risky clauses","Flags penalties, auto-renewals and exclusivity before you sign.")
T("confronta-contratti-ia","ai","🆚","pdf",True,True,"Confronta contratti con IA","Dice in parole semplici cosa è cambiato tra due versioni.","Compare contracts with AI","Explains in plain words what changed between two versions.")
T("anonimizza-pdf","ai","🕶️","pdf",False,True,"Anonimizza PDF","Trova e oscura nomi, IBAN e codici fiscali in automatico.","Anonymize PDF","Finds and blacks out names, IBANs and tax codes automatically.")
T("quiz-da-pdf","ai","🎓","pdf",False,True,"Quiz dal PDF","Trasforma appunti e dispense in domande a risposta multipla.","Quiz from PDF","Turns notes and handouts into multiple-choice questions.")
T("flashcard-da-pdf","ai","🃏","pdf",False,True,"Flashcard dal PDF","Crea carte di ripasso, esportabili in Anki.","Flashcards from PDF","Creates review cards, exportable to Anki.")
T("mappa-concettuale-pdf","ai","🧠","pdf",False,True,"Mappa concettuale dal PDF","Uno schema ad albero con i concetti di un capitolo.","Mind map from PDF","A tree diagram of the concepts in a chapter.")
T("appunti-da-pdf","ai","📒","pdf",False,True,"Appunti dal PDF","Riassunto per studiare: schema, glossario e parole chiave.","Study notes from PDF","A study summary: outline, glossary and keywords.")
T("pdf-in-audio","ai","🔊","pdf",False,True,"Leggi il PDF ad alta voce","Ascolta il documento come file audio MP3.","PDF to audio","Listen to your document as an MP3 file.")
T("pdf-in-podcast","ai","🎙️","pdf",False,True,"PDF in podcast","Due voci che spiegano il documento a modo loro.","PDF to podcast","Two voices discussing your document.")
T("rinomina-pdf-ia","ai","🏷️","pdf",True,True,"Rinomina PDF con IA","Dà a ogni file un nome dal contenuto: data, fornitore, tipo.","Rename PDFs with AI","Names each file from its content: date, vendor, type.")
T("classifica-documenti","ai","🗃️","pdf",True,True,"Classifica documenti","Smista fatture, contratti e ricevute in cartelle da solo.","Sort documents","Sorts invoices, contracts and receipts into folders by itself.")
T("compila-modulo-ia","ai","🖋️","pdf",False,True,"Compila modulo con IA","Compila il modulo partendo dai tuoi dati.","Fill form with AI","Fills in the form from your details.")
T("analizza-cv","ai","👤","pdf",False,True,"Analizza CV","Punti forti, lacune e adattamento a un annuncio.","Analyze resume","Strengths, gaps and fit for a job post.")
T("riassumi-articolo-scientifico","ai","🔬","pdf",False,True,"Riassumi articolo scientifico","Metodo, risultati e limiti in poche righe.","Summarize research paper","Method, results and limits in a few lines.")
T("controlla-bando","ai","📑","pdf",False,True,"Controlla bando o gara","Requisiti e scadenze in una checklist.","Check tender documents","Requirements and deadlines as a checklist.")
T("correggi-testo-pdf","ai","🔤","pdf",False,True,"Correggi testo del PDF","Grammatica e tono, con le modifiche evidenziate.","Proofread PDF text","Grammar and tone, with changes highlighted.")
T("dividi-con-ia","ai","🧩","pdf",False,True,"Dividi con IA","Separa i documenti diversi di una scansione unica.","Split with AI","Separates different documents in a single scan.")
T("domande-su-piu-pdf","ai","📚","pdf",True,True,"Chatta con più PDF","Una sola chat su un'intera cartella di documenti.","Chat with many PDFs","One chat across a whole folder of documents.")
# ---------- Estrai ----------
T("estrai-tabelle-pdf","estrai","🧮","pdfimg",False,True,"Estrai tabelle","Tabelle anche da scansioni, in Excel o CSV.","Extract tables","Tables, even from scans, as Excel or CSV.")
T("scontrini-in-excel","estrai","🧾","img",True,True,"Scontrini in Excel","Foto di scontrini in un foglio spese pronto.","Receipts to Excel","Receipt photos into a ready expense sheet.")
T("pdf-in-json","estrai","{}","pdf",False,True,"PDF in JSON","Dati strutturati pronti per i tuoi software.","PDF to JSON","Structured data ready for your software.")
T("manoscritto-in-testo","estrai","✍️","pdfimg",False,True,"Manoscritto in testo","Riconosce la scrittura a mano e la trasforma in testo.","Handwriting to text","Reads handwriting and turns it into text.")
T("estrai-bibliografia","estrai","📖","pdf",False,True,"Estrai bibliografia","Le citazioni del documento in formato BibTeX.","Extract references","The document's citations in BibTeX.")
T("estrai-immagini-pdf","estrai","🖼️","pdf",False,False,"Estrai immagini","Salva tutte le immagini contenute nel PDF.","Extract images","Saves every image contained in the PDF.")
T("estrai-link-pdf","estrai","🔗","pdf",False,False,"Estrai link","L'elenco di tutti i collegamenti del PDF.","Extract links","A list of every link in the PDF.")
# ---------- Organizza ----------
T("inverti-pagine","organizza","↕️","pdf",False,False,"Inverti ordine pagine","L'ultima pagina diventa la prima.","Reverse page order","The last page becomes the first.")
T("inserisci-pagine","organizza","➕","pdf",True,False,"Inserisci pagine","Aggiungi pagine o un altro PDF in un punto preciso.","Insert pages","Add pages or another PDF at an exact spot.")
T("sostituisci-pagina","organizza","🔁","pdf",True,False,"Sostituisci pagina","Cambia una pagina con quella di un altro file.","Replace page","Swap a page with one from another file.")
T("unisci-alternando","organizza","🔀","pdf",True,False,"Unisci alternando","Fronte e retro di due scansioni in un unico documento.","Alternate & merge","Front and back from two scans in one document.")
T("dividi-per-capitoli","organizza","📑","pdf",False,False,"Dividi per capitoli","Un file per ogni segnalibro o capitolo.","Split by chapters","One file per bookmark or chapter.")
T("dividi-per-peso","organizza","⚖️","pdf",False,False,"Dividi per peso","File sotto una dimensione, utili per gli allegati email.","Split by size","Files under a size limit, handy for email attachments.")
T("rimuovi-pagine-bianche","organizza","⬜","pdf",False,False,"Rimuovi pagine bianche","Elimina le pagine vuote delle scansioni.","Remove blank pages","Deletes the empty pages from scans.")
T("piu-pagine-per-foglio","organizza","🔲","pdf",False,False,"Più pagine per foglio","Stampa 2 o 4 pagine su un solo foglio.","Multiple pages per sheet","Print 2 or 4 pages on a single sheet.")
T("crea-opuscolo","organizza","📖","pdf",False,False,"Crea opuscolo","Impaginazione per stampa fronte e retro a libretto.","Create booklet","Imposition for double-sided booklet printing.")
T("aggiungi-segnalibri","organizza","🔖","pdf",False,False,"Aggiungi segnalibri","Un indice cliccabile, anche generato in automatico.","Add bookmarks","A clickable table of contents, even auto-generated.")
# ---------- Ottimizza ----------
T("comprimi-a-dimensione","ottimizza","🎯","pdf",False,False,"Comprimi a una dimensione","Porta il PDF sotto un peso preciso, come 2 MB.","Compress to a size","Brings the PDF under a set size, such as 2 MB.")
T("ottimizza-per-web","ottimizza","⚡","pdf",False,False,"Ottimizza per il web","PDF a caricamento rapido nel browser.","Optimize for web","PDFs that load fast in the browser.")
T("ridimensiona-a4","ottimizza","📏","pdf",False,False,"Ridimensiona a A4","Porta tutte le pagine allo stesso formato.","Resize to A4","Brings every page to the same size.")
T("raddrizza-scansione","ottimizza","📐","pdfimg",False,False,"Raddrizza scansione","Corregge l'inclinazione delle pagine scansionate.","Deskew scan","Fixes the tilt of scanned pages.")
T("migliora-scansione","ottimizza","✨","pdfimg",False,False,"Migliora scansione","Toglie ombre e rende bianco lo sfondo.","Enhance scan","Removes shadows and whitens the background.")
T("ocr-multilingua","ottimizza","🌐","pdfimg",False,True,"OCR in tante lingue","Riconoscimento del testo in oltre 100 lingue.","Multilingual OCR","Text recognition in 100+ languages.")
# ---------- Converti ----------
T("png-in-pdf","converti","🖼️","img",True,False,"PNG in PDF","Crea un PDF dalle tue immagini PNG.","PNG to PDF","Create a PDF from your PNG images.")
T("webp-in-pdf","converti","🖼️","img",True,False,"WebP in PDF","Trasforma le immagini WebP in PDF.","WebP to PDF","Turn WebP images into a PDF.")
T("heic-in-pdf","converti","📱","heic",True,False,"HEIC in PDF","Le foto dell'iPhone in un PDF.","HEIC to PDF","iPhone photos into a PDF.")
T("tiff-in-pdf","converti","🗞️","tif",True,False,"TIFF in PDF","Converti le scansioni TIFF in PDF.","TIFF to PDF","Convert TIFF scans to PDF.")
T("pdf-in-png","converti","🏞️","pdf",False,False,"PDF in PNG","Salva ogni pagina come immagine PNG.","PDF to PNG","Save every page as a PNG image.")
T("pdf-in-webp","converti","🏞️","pdf",False,False,"PDF in WebP","Pagine PDF in immagini WebP leggere.","PDF to WebP","PDF pages as lightweight WebP images.")
T("pdf-in-tiff","converti","🗞️","pdf",False,False,"PDF in TIFF","Pagine PDF in immagini TIFF.","PDF to TIFF","PDF pages as TIFF images.")
T("pdf-in-epub","converti","📗","pdf",False,False,"PDF in EPUB","Il PDF diventa un e-book per il tuo lettore.","PDF to EPUB","Turn the PDF into an e-book for your reader.")
T("epub-in-pdf","converti","📘","epub",False,False,"EPUB in PDF","Converti i tuoi e-book in PDF.","EPUB to PDF","Convert your e-books to PDF.")
T("mobi-in-pdf","converti","📙","epub",False,False,"MOBI in PDF","Dai libri Kindle a un PDF.","MOBI to PDF","From Kindle books to a PDF.")
T("pdf-in-html","converti","🌐","pdf",False,False,"PDF in HTML","Trasforma il PDF in una pagina web.","PDF to HTML","Turn the PDF into a web page.")
T("pdf-in-csv","converti","🗒️","pdf",False,False,"PDF in CSV","Le tabelle del PDF in un file CSV.","PDF to CSV","The PDF's tables in a CSV file.")
T("testo-in-pdf","converti","🔤","txt",True,False,"Testo in PDF","Da file di testo a PDF ben impaginato.","Text to PDF","From a text file to a well-laid-out PDF.")
T("markdown-in-pdf","converti","⬆️","md",False,False,"Markdown in PDF","Dai tuoi appunti in Markdown a un PDF curato.","Markdown to PDF","From your Markdown notes to a polished PDF.")
T("rtf-in-pdf","converti","📄","odt",True,False,"RTF e ODT in PDF","Documenti RTF e ODT convertiti in PDF.","RTF & ODT to PDF","RTF and ODT documents converted to PDF.")
T("sito-in-pdf","converti","📸","url",False,False,"Sito web in PDF","Cattura una pagina intera, anche lunga.","Website to PDF","Capture a whole page, even a long one.")
T("immagini-in-pdf-ricercabile","converti","🔎","img",True,True,"Immagini in PDF ricercabile","Foto di documenti in un PDF con testo selezionabile.","Images to searchable PDF","Document photos into a PDF with selectable text.")
# ---------- Modifica ----------
T("aggiungi-testo-pdf","modifica","🅰️","pdf",False,False,"Aggiungi testo","Scrivi sopra il PDF dove vuoi.","Add text","Write on top of the PDF wherever you like.")
T("aggiungi-immagine-pdf","modifica","🖼️","pdf",False,False,"Aggiungi immagine","Inserisci logo, firma o foto nelle pagine.","Add image","Place a logo, signature or photo on the pages.")
T("aggiungi-link-pdf","modifica","🔗","pdf",False,False,"Aggiungi link","Rendi cliccabili testi e aree.","Add links","Make text and areas clickable.")
T("evidenzia-pdf","modifica","🖍️","pdf",False,False,"Evidenzia e annota","Sottolineature, evidenziatore e note.","Highlight & annotate","Underlines, highlighter and notes.")
T("sovrapponi-pdf","modifica","🗂️","pdf",True,False,"Sovrapponi PDF","Metti la carta intestata sotto un PDF.","Overlay PDF","Put letterhead behind a PDF.")
# ---------- Crea ----------
T("crea-fattura-pdf","crea","🧾","none",False,True,"Crea fattura PDF","Un modello ordinato per le tue fatture.","Create invoice PDF","A tidy template for your invoices.")
T("crea-cv-pdf","crea","📋","none",False,True,"Crea CV PDF","Un curriculum da modello, in pochi minuti.","Create resume PDF","A template-based resume in minutes.")
T("crea-contratto-pdf","crea","📝","none",False,True,"Crea contratto o lettera","Modelli compilabili con l'aiuto dell'IA.","Create contract or letter","Fillable templates with AI help.")
T("qr-code-pdf","crea","🔳","pdf",False,False,"QR code nel PDF","Inserisci un QR code in una pagina.","QR code in PDF","Place a QR code on a page.")
# ---------- Sicurezza ----------
T("rimuovi-metadati-pdf","sicurezza","🧼","pdf",False,False,"Rimuovi metadati","Toglie autore, date e programma usato.","Remove metadata","Strips author, dates and software used.")
T("modifica-metadati-pdf","sicurezza","🏷️","pdf",False,False,"Modifica metadati","Titolo, autore e parole chiave.","Edit metadata","Title, author and keywords.")
T("appiattisci-pdf","sicurezza","🧱","pdf",False,False,"Appiattisci PDF","Blocca moduli e annotazioni nella pagina.","Flatten PDF","Locks forms and annotations into the page.")
T("verifica-firma-pdf","sicurezza","✅","pdf",False,False,"Verifica firma digitale","Controlla se la firma è valida.","Verify digital signature","Checks whether the signature is valid.")
T("rimuovi-annotazioni-pdf","sicurezza","🧽","pdf",False,False,"Rimuovi annotazioni","Toglie commenti ed evidenziazioni.","Remove annotations","Removes comments and highlights.")

# ---------- Categorie nuove e tool esistenti spostati ----------
CAT_NUOVE = [
    {"id": "estrai", "settore": "pdf", "it": "Estrai da PDF", "en": "Extract from PDF", "colore": "#0ea5e9"},
    {"id": "crea", "settore": "pdf", "it": "Crea PDF", "en": "Create PDF", "colore": "#f59e0b"},
]
SPOSTA = {"estrai-dati-pdf": "estrai", "pdf-in-markdown": "estrai", "pdf-in-testo": "estrai"}

# ---------- PRIORITA' (profitto/domanda + stelle su GitHub: Stirling-PDF, Docling, MinerU) ----------
# L'ordine qui = ordine nel file. Gli id non elencati vanno in coda nell'ordine in cui sono.
PRIORITA = """comprimi-pdf unisci-pdf pdf-in-word riassumi-pdf chatta-con-pdf ocr-pdf traduci-pdf estrai-dati-pdf
firma-pdf dividi-pdf word-in-pdf modifica-pdf pdf-in-excel estrai-tabelle-pdf spiega-contratto clausole-a-rischio
anonimizza-pdf scontrini-in-excel pdf-in-markdown jpg-in-pdf pdf-in-jpg manoscritto-in-testo pdf-in-json
confronta-contratti-ia quiz-da-pdf flashcard-da-pdf appunti-da-pdf domande-su-piu-pdf comprimi-a-dimensione
proteggi-pdf sblocca-pdf organizza-pdf ruota-pdf rimuovi-pagine-pdf estrai-pagine-pdf powerpoint-in-pdf pdf-in-powerpoint
excel-in-pdf censura-pdf scansiona-in-pdf immagini-in-pdf-ricercabile ocr-multilingua filigrana-pdf numeri-di-pagina
rinomina-pdf-ia classifica-documenti analizza-cv crea-fattura-pdf crea-cv-pdf mappa-concettuale-pdf pdf-in-audio pdf-in-podcast
riassumi-articolo-scientifico controlla-bando compila-modulo-ia crea-contratto-pdf dividi-con-ia correggi-testo-pdf
estrai-bibliografia html-in-pdf sito-in-pdf png-in-pdf heic-in-pdf webp-in-pdf pdf-in-png pdf-in-epub epub-in-pdf mobi-in-pdf
confronta-pdf moduli-pdf ripara-pdf pdf-in-pdfa pdf-in-testo ritaglia-pdf aggiungi-testo-pdf aggiungi-immagine-pdf
evidenzia-pdf raddrizza-scansione migliora-scansione ottimizza-per-web ridimensiona-a4 estrai-immagini-pdf pdf-in-csv
rimuovi-metadati-pdf appiattisci-pdf verifica-firma-pdf dividi-per-capitoli dividi-per-peso rimuovi-pagine-bianche
aggiungi-segnalibri inserisci-pagine sostituisci-pagina unisci-alternando inverti-pagine aggiungi-link-pdf sovrapponi-pdf
piu-pagine-per-foglio crea-opuscolo qr-code-pdf modifica-metadati-pdf rimuovi-annotazioni-pdf pdf-in-html pdf-in-webp
pdf-in-tiff tiff-in-pdf testo-in-pdf markdown-in-pdf rtf-in-pdf estrai-link-pdf""".split()

j = json.load(io.open(P, encoding="utf-8"))
esist = {s["id"] for s in j["strumenti"]}
agg = 0
for (i, cat, ico, acc, multi, nuovo, itn, itd, enn, end) in N:
    if i in esist: continue  # rilanciabile: niente doppioni
    inp = "url" if acc == "url" else "file"
    s = {"id": i, "cat": cat, "ico": ico, "input": inp, "accept": ACC[acc], "multi": multi, "nuovo": nuovo, "it": [itn, itd], "en": [enn, end]}
    j["strumenti"].append(s); agg += 1
ids_cat = {c["id"] for c in j["categorie"]}
for c in CAT_NUOVE:
    if c["id"] not in ids_cat: j["categorie"].append(c)
for s in j["strumenti"]:
    if s["id"] in SPOSTA: s["cat"] = SPOSTA[s["id"]]
pos = {i: n for n, i in enumerate(PRIORITA)}
j["strumenti"].sort(key=lambda s: pos.get(s["id"], 10000))  # sort stabile: i non elencati restano in coda
# controlli: ogni cat esiste, nessun id doppio
cat_ok = {c["id"] for c in j["categorie"]}
ids = [s["id"] for s in j["strumenti"]]
assert len(ids) == len(set(ids)), "id doppi"
assert all(s["cat"] in cat_ok for s in j["strumenti"]), "categoria sconosciuta"
mancanti = [i for i in PRIORITA if i not in set(ids)]
if mancanti: print("ATTENZIONE id in PRIORITA senza tool:", mancanti)
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(j, f, ensure_ascii=False, indent=1); f.write("\n")
sys.stdout.reconfigure(encoding="utf-8")
print("aggiunti", agg, "- totale", len(ids))
