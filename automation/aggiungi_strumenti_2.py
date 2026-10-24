# -*- coding: utf-8 -*-
"""build_freetool_tools2.py - 2a ondata del catalogo FreeTool (smoke test): "regala" cio' che i concorrenti vendono
e i servizi dei repo GitHub con piu' stelle. Rilanciabile: non crea doppioni (salta gli id gia' presenti).
COME FUNZIONA:
 - PDF: ogni tool ha un "after" = id dopo cui inserirlo (cosi' resta nell'ordine di profitto del file).
 - NUOVI SETTORI (Immagini, Audio e video): aggiunge settore + categorie + tool in fondo, nell'ordine scritto qui (= priorita').
 - Dopo: python automation\\genera_strumenti.py  e  python automation\\allinea_hash.py en
FONTI della scelta (ricerche 24/10/2026): Smallpdf Pro vende Edit Text, compressione forte, AI, batch, firme; iLovePDF Premium workflow,
firme, no limiti; stelle GitHub: markitdown ~120k, Stirling-PDF ~78k, Whisper ~95k, Upscayl ~43k, PDFMathTranslate ~35k, Real-ESRGAN ~34k, OCRmyPDF ~33k."""
import io, json, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "strumenti.json")  # percorso ricavato da solo
ACC = {"pdf": ".pdf,application/pdf", "pdfimg": ".pdf,application/pdf,image/*", "img": "image/*", "url": "",
       "audio": "audio/*,.mp3,.wav,.m4a,.ogg,.flac", "video": "video/*,.mp4,.mov,.mkv,.avi,.webm", "av": "audio/*,video/*",
       "office": ".doc,.docx,.xls,.xlsx,.ppt,.pptx,.html,.htm,.csv,.epub,.pdf", "xml": ".xml,.p7m", "p7m": ".p7m",
       "sub": ".srt,.vtt", "svg": ".svg,image/svg+xml", "none": ".pdf,application/pdf"}
PDF = []   # (id, cat, ico, acc, multi, nuovo, it, itd, en, end, after)
def A(*a): PDF.append(a)
# ---- PDF: quello che i concorrenti fanno pagare + i repo con piu' stelle ----
A("xml-fattura-in-pdf","converti","🇮🇹","xml",True,True,"Fattura elettronica XML in PDF","Leggi e stampa la fattura elettronica (XML o P7M) in un PDF chiaro.","Italian e-invoice XML to PDF","Read and print Italian electronic invoices (XML or P7M) as a clear PDF.","estrai-dati-pdf")
A("apri-p7m","sicurezza","🔏","p7m",True,True,"Apri file P7M","Estrai il documento dentro un file firmato .p7m.","Open P7M file","Extract the document inside a signed .p7m file.","firma-pdf")
A("file-in-markdown","estrai","⬇️","office",True,True,"Qualsiasi file in Markdown","Word, Excel, PowerPoint, HTML e PDF in Markdown pulito per gli LLM.","Any file to Markdown","Word, Excel, PowerPoint, HTML and PDF as clean Markdown for LLMs.","pdf-in-markdown")
A("prepara-pdf-per-rag","estrai","🧱","pdf",True,True,"Prepara PDF per chatbot","Spezza il documento in blocchi pronti per un chatbot o una ricerca con IA.","Prepare PDF for chatbots","Splits the document into chunks ready for a chatbot or AI search.","file-in-markdown")
A("pdf-in-latex","estrai","∑","pdf",False,True,"PDF in LaTeX","Articoli e dispense in LaTeX, con le formule al loro posto.","PDF to LaTeX","Papers and handouts as LaTeX, with formulas intact.","pdf-in-json")
A("estrai-formule-pdf","estrai","🔣","pdfimg",False,True,"Estrai formule matematiche","Le formule del PDF o di una foto in LaTeX.","Extract math formulas","Formulas from a PDF or photo as LaTeX.","pdf-in-latex")
A("traduci-paper-pdf","ai","🧪","pdf",False,True,"Traduci articolo scientifico","Traduce paper con formule e figure senza rovinare l'impaginazione.","Translate research paper","Translates papers with formulas and figures without breaking the layout.","traduci-pdf")
A("pdf-bilingue","ai","🌍","pdf",False,True,"PDF bilingue affiancato","Originale e traduzione affiancati, pagina per pagina.","Bilingual side-by-side PDF","Original and translation side by side, page by page.","traduci-paper-pdf")
A("pdf-in-presentazione-ia","ai","📽️","pdf",False,True,"Crea presentazione dal PDF","Slide con titoli e punti chiave a partire da un documento.","Make slides from PDF","Slides with titles and key points from a document.","riassumi-pdf")
A("riassunto-in-email","ai","✉️","pdf",False,True,"PDF in email","Una bozza di email che riassume il documento.","PDF to email","A draft email that sums up the document.","riassumi-pdf")
A("azioni-da-verbale","ai","✅","pdf",False,True,"Estrai azioni dal verbale","Decisioni, responsabili e scadenze in una lista.","Extract action items","Decisions, owners and deadlines as a list.","clausole-a-rischio")
A("modifica-testo-pdf","modifica","📝","pdf",False,True,"Modifica testo nel PDF","Cambia le parole direttamente nel documento.","Edit PDF text","Change the words right inside the document.","modifica-pdf")
A("comprimi-forte-pdf","ottimizza","🗜️","pdf",False,False,"Compressione forte","Il massimo risparmio di spazio per i file più pesanti.","Strong compression","Maximum space savings for the heaviest files.","comprimi-a-dimensione")
A("elabora-in-blocco","organizza","📦","pdf",True,True,"Elabora in blocco","Applica la stessa operazione a decine di PDF insieme.","Batch process","Apply the same operation to dozens of PDFs at once.","domande-su-piu-pdf")
A("automazioni-pdf","organizza","⚙️","pdf",True,True,"Automazioni PDF","Concatena più passaggi (comprimi, OCR, firma) in un solo flusso.","PDF workflows","Chain several steps (compress, OCR, sign) into one flow.","elabora-in-blocco")
A("richiedi-firme-pdf","sicurezza","📨","pdf",False,True,"Richiedi firme","Invia il documento a più persone e raccogli le firme.","Request signatures","Send the document to several people and collect signatures.","firma-pdf")
A("firma-con-certificato-pdf","sicurezza","🪪","pdf",False,False,"Firma con certificato","Firma digitale con il tuo certificato.","Sign with certificate","Digital signature with your own certificate.","richiedi-firme-pdf")
A("pdf-accessibile","ottimizza","♿","pdf",False,True,"Rendi il PDF accessibile","Tag, ordine di lettura e testo alternativo con IA.","Make PDF accessible","Tags, reading order and alt text with AI.","pdf-in-pdfa")
A("pdf-per-stampa","ottimizza","🖨️","pdf",False,False,"PDF per la stampa","Controlla e prepara il file per la tipografia (PDF/X).","Print-ready PDF","Checks and prepares your file for the print shop (PDF/X).","pdf-in-pdfa")
A("ocr-cjk","ottimizza","🈶","pdfimg",False,True,"OCR cinese, giapponese, coreano","Riconosce testi in ideogrammi con alta precisione.","CJK OCR","Reads ideographic text with high accuracy.","ocr-multilingua")
# ---- NUOVI SETTORI: (id, cat, ico, acc, multi, nuovo, it, itd, en, end) in ordine di priorita' ----
SET = [
 {"id": "immagini", "it": "Strumenti immagini", "en": "Image tools", "slug": {"it": "strumenti-immagini", "en": "image-tools"},
  "ico": "🖼️", "colore": "#7c3aed", "desc": {"it": "Togli lo sfondo, ingrandisci, comprimi e converti le tue immagini.", "en": "Remove backgrounds, upscale, compress and convert your images."}},
 {"id": "audio-video", "it": "Audio e video", "en": "Audio & video", "slug": {"it": "audio-e-video", "en": "audio-video-tools"},
  "ico": "🎬", "colore": "#0ea5e9", "desc": {"it": "Trascrivi, sottotitola, comprimi e converti audio e video.", "en": "Transcribe, caption, compress and convert audio and video."}},
]
CAT = [
 {"id": "img-ia", "settore": "immagini", "it": "Immagini e IA", "en": "Images and AI", "colore": "#7c3aed"},
 {"id": "img-ottimizza", "settore": "immagini", "it": "Ottimizza immagini", "en": "Optimize images", "colore": "#22a559"},
 {"id": "img-converti", "settore": "immagini", "it": "Converti immagini", "en": "Convert images", "colore": "#f59e0b"},
 {"id": "img-modifica", "settore": "immagini", "it": "Modifica immagini", "en": "Edit images", "colore": "#e5322d"},
 {"id": "av-trascrivi", "settore": "audio-video", "it": "Trascrivi e sottotitola", "en": "Transcribe & caption", "colore": "#0ea5e9"},
 {"id": "av-video", "settore": "audio-video", "it": "Video", "en": "Video", "colore": "#e5322d"},
 {"id": "av-audio", "settore": "audio-video", "it": "Audio", "en": "Audio", "colore": "#22a559"},
]
NEW = []
def N(*a): NEW.append(a)
# ---------- IMMAGINI (stelle GitHub: Upscayl ~43k, Real-ESRGAN ~34k, rembg; concorrenti a pagamento: remove.bg, Topaz, TinyPNG Pro) ----------
N("rimuovi-sfondo","img-ia","✂️","img",True,True,"Rimuovi sfondo","Toglie lo sfondo da una foto e lascia solo il soggetto.","Remove background","Cuts the background out and keeps only the subject.")
N("ingrandisci-immagine","img-ia","🔭","img",False,True,"Ingrandisci immagine con IA","Porta le foto piccole in alta risoluzione senza sgranare.","AI image upscaler","Brings small photos to high resolution without pixelation.")
N("comprimi-immagine","img-ottimizza","🗜️","img",True,False,"Comprimi immagine","Meno peso per JPG, PNG e WebP, con qualità quasi uguale.","Compress image","Smaller JPG, PNG and WebP files with almost identical quality.")
N("rimuovi-oggetti-foto","img-ia","🧹","img",False,True,"Rimuovi oggetti dalla foto","Cancella persone, scritte o oggetti e riempie lo spazio.","Remove objects from photo","Erases people, text or objects and fills the gap.")
N("heic-in-jpg","img-converti","📱","img",True,False,"HEIC in JPG","Le foto dell'iPhone in JPG leggibili ovunque.","HEIC to JPG","iPhone photos as JPG that open anywhere.")
N("foto-tessera","img-modifica","🪪","img",False,True,"Foto tessera","Ritaglio e sfondo a norma per documenti, pronti da stampare.","Passport photo maker","Compliant crop and background for IDs, ready to print.")
N("migliora-foto-volti","img-ia","😀","img",False,True,"Migliora volti","Rende nitidi i volti nelle foto sfocate o vecchie.","Enhance faces","Sharpens faces in blurry or old photos.")
N("restaura-foto-vecchie","img-ia","🕰️","img",False,True,"Restaura foto vecchie","Toglie graffi e macchie e riporta vita ai ricordi.","Restore old photos","Removes scratches and stains and brings memories back.")
N("colora-foto","img-ia","🎨","img",False,True,"Colora foto in bianco e nero","Aggiunge i colori alle foto storiche.","Colorize black & white photos","Adds color to historic photos.")
N("immagine-in-testo","img-ia","🔍","img",True,False,"Immagine in testo (OCR)","Copia il testo da foto, screenshot e scansioni.","Image to text (OCR)","Copy text from photos, screenshots and scans.")
N("descrivi-immagine","img-ia","🏷️","img",True,True,"Descrivi immagine","Testo alternativo e didascalie SEO generati dall'IA.","Describe image","AI-written alt text and SEO captions.")
N("sfoca-volti-foto","img-ia","🫥","img",True,True,"Sfoca volti e targhe","Anonimizza persone e targhe in foto e immagini.","Blur faces & plates","Anonymize people and license plates in photos.")
N("ridimensiona-immagine","img-ottimizza","📏","img",True,False,"Ridimensiona immagine","Scegli larghezza e altezza o i formati dei social.","Resize image","Pick width and height or social media sizes.")
N("ritaglia-immagine","img-modifica","✂️","img",False,False,"Ritaglia immagine","Taglia a mano o con formati pronti.","Crop image","Crop by hand or with ready-made ratios.")
N("rimuovi-metadati-immagine","img-ottimizza","🧼","img",True,False,"Rimuovi dati EXIF","Toglie posizione GPS e info dello scatto.","Remove EXIF data","Strips GPS location and shot info.")
N("png-in-jpg","img-converti","🔄","img",True,False,"PNG in JPG","Converti PNG in JPG leggeri.","PNG to JPG","Convert PNG into lightweight JPG.")
N("jpg-in-png","img-converti","🔄","img",True,False,"JPG in PNG","Converti JPG in PNG.","JPG to PNG","Convert JPG into PNG.")
N("webp-in-jpg","img-converti","🔄","img",True,False,"WebP in JPG","Converti WebP in JPG o PNG.","WebP to JPG","Convert WebP into JPG or PNG.")
N("svg-in-png","img-converti","🔄","svg",True,False,"SVG in PNG","Rasterizza un SVG alla dimensione che vuoi.","SVG to PNG","Rasterize an SVG at any size.")
N("immagine-in-svg","img-converti","✒️","img",False,True,"Immagine in vettoriale","Trasforma logo e disegni in SVG ridimensionabile.","Image to vector","Turns logos and drawings into scalable SVG.")
N("aggiungi-filigrana-immagine","img-modifica","💧","img",True,False,"Filigrana su immagine","Proteggi le tue foto con testo o logo.","Watermark image","Protect your photos with text or a logo.")
N("unisci-immagini","img-modifica","🧩","img",True,False,"Unisci immagini","Collage e strisce di più foto in una.","Combine images","Collages and strips of several photos in one.")
N("ruota-immagine","img-modifica","🔃","img",True,False,"Ruota e specchia","Gira le foto nel verso giusto.","Rotate & flip","Turn photos the right way up.")
# ---------- AUDIO E VIDEO (Whisper ~95k stelle; concorrenti a pagamento: Otter, Descript, Veed, Kapwing) ----------
N("trascrivi-audio","av-trascrivi","🎤","audio",True,True,"Trascrivi audio","Da registrazioni e messaggi vocali a testo, in 99 lingue.","Transcribe audio","From recordings and voice notes to text, in 99 languages.")
N("sottotitoli-automatici","av-trascrivi","💬","video",False,True,"Sottotitoli automatici","Crea i sottotitoli (SRT) di un video, anche tradotti.","Auto subtitles","Creates subtitles (SRT) for a video, even translated.")
N("verbale-riunione","av-trascrivi","📋","av",False,True,"Verbale di riunione","Dall'audio o dal video a verbale con decisioni e azioni.","Meeting minutes","From audio or video to minutes with decisions and action items.")
N("riassumi-video","av-trascrivi","📺","url",False,True,"Riassumi video","Incolla il link di un video e ricevi i punti chiave.","Summarize video","Paste a video link and get the key points.")
N("trascrivi-video","av-trascrivi","🎞️","video",False,True,"Trascrivi video","Il parlato di un video in testo con i tempi.","Transcribe video","A video's speech as timestamped text.")
N("traduci-sottotitoli","av-trascrivi","🌍","sub",False,True,"Traduci sottotitoli","Da SRT in una lingua a SRT in un'altra.","Translate subtitles","From SRT in one language to another.")
N("comprimi-video","av-video","🗜️","video",False,False,"Comprimi video","Riduci il peso senza rovinare la qualità.","Compress video","Cut file size without hurting quality.")
N("video-in-mp4","av-video","🔄","video",True,False,"Video in MP4","Converti MOV, AVI, MKV e WebM in MP4.","Video to MP4","Convert MOV, AVI, MKV and WebM to MP4.")
N("video-in-gif","av-video","🌀","video",False,False,"Video in GIF","Una clip diventa una GIF animata.","Video to GIF","A clip becomes an animated GIF.")
N("taglia-video","av-video","✂️","video",False,False,"Taglia video","Scegli inizio e fine e salva solo quel pezzo.","Trim video","Pick the start and end and keep just that part.")
N("video-per-social","av-video","📱","video",False,False,"Video per i social","Ridimensiona per Reels, TikTok, Shorts e Stories.","Video for social","Resize for Reels, TikTok, Shorts and Stories.")
N("rimuovi-sfondo-video","av-video","🪄","video",False,True,"Rimuovi sfondo dal video","Toglie lo sfondo di una clip, senza green screen.","Remove video background","Removes a clip's background, no green screen needed.")
N("estrai-audio-da-video","av-audio","🎵","video",False,False,"Estrai audio dal video","Salva la traccia audio in MP3.","Extract audio from video","Save the audio track as MP3.")
N("converti-audio","av-audio","🔄","audio",True,False,"Converti audio","MP3, WAV, M4A, OGG e FLAC l'uno nell'altro.","Convert audio","MP3, WAV, M4A, OGG and FLAC into one another.")
N("taglia-audio","av-audio","✂️","audio",False,False,"Taglia audio","Ritaglia una parte della registrazione.","Trim audio","Cut out part of a recording.")
N("unisci-audio","av-audio","🔗","audio",True,False,"Unisci audio","Metti insieme più tracce in un solo file.","Merge audio","Join several tracks into one file.")
N("rimuovi-rumore-audio","av-audio","🔇","audio",False,True,"Rimuovi rumore","Toglie fruscii e rumore di fondo dalla voce.","Remove noise","Strips hiss and background noise from voice.")
N("separa-voce-musica","av-audio","🎼","audio",False,True,"Separa voce e musica","Isola la voce o la base strumentale da un brano.","Split vocals & music","Isolates the vocals or the instrumental from a track.")
N("testo-in-voce","av-audio","🗣️","none",False,True,"Testo in voce","Scrivi un testo e ascolta una voce naturale in MP3.","Text to speech","Type text and get a natural voice as MP3.")
N("doppiaggio-ia","av-audio","🎙️","video",False,True,"Doppiaggio con IA","Traduce il parlato di un video e lo rifà in un'altra lingua.","AI dubbing","Translates a video's speech and re-voices it in another language.")

# ---------- applica ----------
j = json.load(io.open(P, encoding="utf-8"))
ids = [s["id"] for s in j["strumenti"]]
sett = {s["id"] for s in j["settori"]}
for s in SET:
    if s["id"] not in sett: j["settori"].append(s)
cats = {c["id"] for c in j["categorie"]}
for c in CAT:
    if c["id"] not in cats: j["categorie"].append(c)
def mk(i, cat, ico, acc, multi, nuovo, itn, itd, enn, end):
    return {"id": i, "cat": cat, "ico": ico, "input": "url" if acc == "url" else "file", "accept": ACC[acc],
            "multi": multi, "nuovo": nuovo, "it": [itn, itd], "en": [enn, end]}
ag = 0
for a in PDF:                       # inserimento dopo l'id "after"
    if a[0] in ids: continue
    pos = ids.index(a[10]) + 1      # se l'ancora manca: errore chiaro (ValueError) invece di un ordine sbagliato
    j["strumenti"].insert(pos, mk(*a[:10])); ids.insert(pos, a[0]); ag += 1
for a in NEW:                       # settori nuovi: in fondo, nell'ordine scritto
    if a[0] in ids: continue
    j["strumenti"].append(mk(*a)); ids.append(a[0]); ag += 1
okc = {c["id"] for c in j["categorie"]}
assert len(ids) == len(set(ids)), "id doppi"
assert all(s["cat"] in okc for s in j["strumenti"]), "categoria sconosciuta"
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(j, f, ensure_ascii=False, indent=1); f.write("\n")
sys.stdout.reconfigure(encoding="utf-8")
print("aggiunti", ag, "- totale", len(ids), "- settori", [s["id"] for s in j["settori"]])
