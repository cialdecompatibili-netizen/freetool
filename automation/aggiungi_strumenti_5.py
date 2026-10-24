# -*- coding: utf-8 -*-
"""aggiungi_strumenti_5.py - tool scelti dalla ricerca di ottobre 2026 (cosa cerca e paga la gente davvero). Rilanciabile: salta gli id gia' presenti.
FONTI (reali): traffico iLovePDF ~216M visite/mese (Semrush, dic 2025: keyword top = jpg to pdf, pdf to word, pdf to jpg); GitHub PDF/doc AI in crescita
(MinerU ~78k stelle, Docling ~65k, PaddleOCR ~88k, Marker ~35k, markitdown, Stirling-PDF; trend 2026: PDF -> dati/Markdown per LLM, firma open source, PDF accessibile);
classifiche AI tools 2026 (RankmyAI, theresanaiforthat): sottotitoli, voiceover, background remover, video enhancer, subtitle remover, vocal remover/karaoke, upscaler;
Italia: Rizzo-PII (Simone Rizzo, anonimizzazione locale, luglio 2026) = origine famiglia ANONIMIZZA; bollette/buste paga/referti/FatturaPA = ricerche italiane ad alta intenzione.
Dopo: python automation\\genera_strumenti.py  e  python automation\\allinea_hash.py en"""
import io, json, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "strumenti.json")
j = json.load(io.open(P, encoding="utf-8"))
ACC = {"pdf": ".pdf,application/pdf", "pdfimg": ".pdf,application/pdf,image/*", "img": "image/*", "aud": "audio/*,.mp3,.wav,.m4a,.ogg,.flac",
       "vid": "video/*,.mp4,.mov,.mkv,.avi,.webm", "av": "audio/*,video/*", "": ""}
# (id, cat, ico, input, acc, multi, it, itd, en, end)   in ordine di priorita' (i piu' cercati prima dentro ogni settore)
N = [
 # ---- PDF e IA (Italia: ricerche pratiche, alta intenzione) ----
 ("spiega-busta-paga", "ai", "\U0001F4B6", "file", "pdfimg", False, "Spiega busta paga", "Carica la busta paga e ricevi voci, trattenute e netto spiegati in parole semplici.", "Explain payslip", "Upload a payslip and get items, deductions and net pay explained in plain words."),
 ("analizza-bolletta", "ai", "\U0001F4A1", "file", "pdfimg", False, "Analizza bolletta luce e gas", "Legge la bolletta, spiega le voci e ti dice dove stai pagando di piu'.", "Utility bill analyzer", "Reads your bill, explains each line and shows where you may be overpaying."),
 ("spiega-referto", "ai", "\U0001FA7A", "file", "pdfimg", False, "Spiega referto medico", "Un referto in linguaggio semplice. Non sostituisce il medico.", "Explain medical report", "A medical report in plain language. Does not replace your doctor."),
 ("riassumi-sentenza", "ai", "\u2696\uFE0F", "file", "pdfimg", False, "Riassumi sentenza o atto legale", "Esito, parti, motivazioni e scadenze in una pagina.", "Summarize ruling or legal act", "Outcome, parties, reasoning and deadlines on one page."),
 ("estrai-dati-schema", "estrai", "\U0001F9EC", "file", "pdfimg", True, "Estrai dati con il tuo schema", "Dici quali campi vuoi e ottieni JSON o Excel pulito da qualsiasi PDF (alternativa a Docling e Marker).", "Extract data with your schema", "Name the fields you want and get clean JSON or Excel from any PDF (Docling/Marker alternative)."),
 ("pdf-in-fattura-xml", "crea", "\U0001F9FE", "file", "pdfimg", False, "PDF in fattura elettronica XML", "Da una fattura PDF o foto a XML FatturaPA pronto per lo SDI.", "PDF to e-invoice XML", "From a PDF or photo invoice to FatturaPA XML ready for the Italian SDI."),
 # ---- IMMAGINI (background remover, upscaler, generatori: categorie piu' cercate) ----
 ("genera-immagine", "img-ia", "\U0001F3A8", "testo", "", False, "Genera immagine da testo", "Descrivi cosa vuoi e ottieni l'immagine, senza registrarti.", "AI image generator", "Describe what you want and get the image, no sign-up."),
 ("modifica-foto-comando", "img-ia", "\U0001FA84", "file", "img", False, "Modifica foto con un comando", "Scrivi cosa cambiare (colori, oggetti, stile) e l'IA lo fa.", "Edit photo with a prompt", "Type what to change (colors, objects, style) and the AI does it."),
 ("foto-prodotto-ia", "img-ia", "\U0001F6CD\uFE0F", "file", "img", True, "Foto prodotto con sfondo IA", "Sfondo pulito o ambientato per i tuoi prodotti, pronto per ecommerce e Amazon.", "AI product photos", "Clean or styled backgrounds for your products, ready for ecommerce and Amazon."),
 ("foto-profilo-ia", "img-ia", "\U0001F454", "file", "img", False, "Foto profilo professionale IA", "Dal selfie a una foto da LinkedIn e curriculum.", "AI professional headshot", "From a selfie to a LinkedIn and CV-ready photo."),
 ("foto-in-3d", "img-ia", "\U0001F9CA", "file", "img", False, "Foto in modello 3D", "Trasforma una foto in un modello 3D scaricabile (GLB).", "Photo to 3D model", "Turn a photo into a downloadable 3D model (GLB)."),
 ("genera-logo", "img-ia", "\u2728", "testo", "", False, "Crea logo con IA", "Descrivi la tua attivita' e ricevi proposte di logo in SVG e PNG.", "AI logo maker", "Describe your business and get logo options as SVG and PNG."),
 # ---- AUDIO ----
 ("karaoke-togli-voce", "av-audio", "\U0001F3A4", "file", "aud", False, "Karaoke: togli la voce", "Cancella la voce da una canzone e tieni la base musicale.", "Karaoke vocal remover", "Remove the vocals from a song and keep the instrumental."),
 ("migliora-voce", "av-audio", "\U0001F399\uFE0F", "file", "aud", False, "Migliora voce da studio", "Registrazione con eco e rumore? Esce con suono da studio.", "Studio voice enhancer", "Recording with echo and noise? It comes out studio-clean."),
 ("cambia-voce", "av-audio", "\U0001F3AD", "file", "aud", False, "Cambia voce con IA", "Trasforma la tua voce in un'altra voce naturale.", "AI voice changer", "Turn your voice into another natural-sounding voice."),
 ("normalizza-volume", "av-audio", "\U0001F50A", "file", "aud", True, "Normalizza volume", "Porta tutti i file allo stesso livello, per podcast e video.", "Normalize volume", "Brings all files to the same level, for podcasts and videos."),
 ("registra-e-trascrivi", "av-trascrivi-audio", "\U0001F534", "file", "aud", False, "Registra e trascrivi", "Registra dal microfono e ottieni subito il testo.", "Record and transcribe", "Record from your microphone and get the text right away."),
 ("podcast-capitoli", "av-trascrivi-audio", "\U0001F4D1", "file", "aud", False, "Capitoli e note del podcast", "Capitoli con orari, riassunto e show notes dal tuo episodio.", "Podcast chapters & show notes", "Timestamped chapters, summary and show notes from your episode."),
 # ---- VIDEO ----
 ("sottotitoli-nel-video", "av-video", "\U0001F4AC", "file", "vid", False, "Sottotitoli incorporati nel video", "Scrive i sottotitoli direttamente sul video, in stile social.", "Burn subtitles into video", "Writes captions straight onto the video, social-media style."),
 ("clip-virali", "av-video", "\U0001F525", "file", "vid", False, "Clip per i social dai video lunghi", "Trova i momenti migliori e crea clip verticali con sottotitoli.", "Viral clips from long videos", "Finds the best moments and makes vertical clips with captions."),
 ("migliora-video-ia", "av-video", "\U0001F4FA", "file", "vid", False, "Migliora e ingrandisci video", "Piu' nitido e in alta risoluzione, anche per video vecchi.", "AI video enhancer", "Sharper and higher resolution, even for old videos."),
 ("rimuovi-sottotitoli-video", "av-video", "\U0001F9FD", "file", "vid", False, "Rimuovi sottotitoli dal video", "Cancella le scritte fisse dei sottotitoli dai tuoi video.", "Remove subtitles from video", "Erase hard-coded subtitles from your own videos."),
 ("tutorial-da-registrazione", "av-video", "\U0001F5A5\uFE0F", "file", "vid", False, "Tutorial dalla registrazione schermo", "Da una registrazione muta a un tutorial con voce e passaggi scritti.", "Tutorial from screen recording", "From a silent recording to a tutorial with voice-over and written steps."),
 ("unisci-video", "av-video", "\U0001F517", "file", "vid", True, "Unisci video", "Metti insieme piu' clip in un unico video.", "Merge videos", "Join several clips into one video."),
 ("estrai-fotogrammi", "av-video", "\U0001F5BC\uFE0F", "file", "vid", False, "Estrai fotogrammi dal video", "Salva le immagini migliori del video come JPG o PNG.", "Extract video frames", "Save the best frames of the video as JPG or PNG."),
 ("video-in-articolo", "av-trascrivi-video", "\U0001F4DD", "url", "", False, "Video in articolo di blog", "Incolla il link di un video e ottieni un articolo pronto da pubblicare.", "Video to blog post", "Paste a video link and get an article ready to publish."),
]
by = {t["id"]: t for t in j["strumenti"]}
cats = {c["id"]: c for c in j["categorie"]}
agg = 0
for (i, cat, ico, inp, acc, multi, itn, itd, enn, end) in N:
    if i in by: continue
    sett = cats[cat]["settore"]
    ids = [k for k, t in enumerate(j["strumenti"]) if cats[t["cat"]]["settore"] == sett]
    pos = ids[min(2, len(ids) - 1)] + 1  # dopo i 3 tool gia' piu' forti del settore
    # i nuovi dello stesso settore si dispongono nell'ordine scritto sopra
    nuovi = [k for k in ids if j["strumenti"][k].get("_n5")]
    if nuovi: pos = nuovi[-1] + 1
    j["strumenti"].insert(pos, {"id": i, "cat": cat, "ico": ico, "input": inp, "accept": ACC[acc], "multi": multi, "nuovo": True, "it": [itn, itd], "en": [enn, end], "_n5": True})
    by[i] = j["strumenti"][pos]; agg += 1
for t in j["strumenti"]: t.pop("_n5", None)
# correzione: Testo in voce ora chiede un testo, non un PDF
t = by["testo-in-voce"]; t["input"] = "testo"; t["accept"] = ""; t["multi"] = False
ok = {c["id"] for c in j["categorie"]}
ids = [s["id"] for s in j["strumenti"]]
assert len(ids) == len(set(ids)) and all(s["cat"] in ok for s in j["strumenti"])
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(j, f, ensure_ascii=False, indent=1); f.write("\n")
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "FILOSOFIA.md")
tx = io.open(D, encoding="utf-8").read()
if "Ricerca ottobre 2026" not in tx:
    tx = tx.rstrip("\n") + "\n- Ricerca ottobre 2026 (script aggiungi_strumenti_5.py): famiglia ANONIMIZZA nata dal modello Rizzo-PII di Simone Rizzo (YouTube, AI engineer, Bologna); da seguire: pasqualepillitteri.it (recensioni tool AI). Tool aggiunti dove c'e' domanda reale: PDF italiani (busta paga, bolletta, referto, FatturaPA), estrazione dati con schema, immagini (generatore, prodotto, 3D, logo), audio (karaoke, voce studio), video (clip social, enhancer, sottotitoli). Fonti: Semrush, GitTrend, RankmyAI.\n"
    io.open(D, "w", encoding="utf-8", newline="\n").write(tx)
sys.stdout.reconfigure(encoding="utf-8")
print("aggiunti", agg, "- totale", len(ids))
