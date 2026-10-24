# -*- coding: utf-8 -*-
"""aggiungi_strumenti_3.py - famiglia ANONIMIZZA (privacy prima dell'LLM). Rilanciabile: aggiorna il tool esistente e salta gli id gia' presenti.
LOGICA (voluta da Mirco): si carica un documento, il tool RILEVA i dati sensibili (nomi, codici fiscali, IBAN, indirizzi, telefoni, dati sanitari...)
e li RIMUOVE sostituendoli con *** (oppure con segnaposto reversibili [PERSONA_1]). Serve come passo PRIMA di dare il file a un LLM,
cosi' dati personali, cartelle cliniche e documenti riservati non vengono mai inviati/pubblicati. Il motore previsto e' open source in locale
(es. Microsoft Presidio + modelli NER; nessun dato esce dalla VPS). Il rilevamento automatico non e' perfetto: va sempre ricontrollato a mano.
Dopo: python automation\\genera_strumenti.py  e  python automation\\allinea_hash.py en"""
import io, json, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "strumenti.json")  # percorso ricavato da solo
ACC = {"pdf": ".pdf,application/pdf", "pdfimg": ".pdf,application/pdf,image/*", "doc": ".doc,.docx,.xls,.xlsx,.csv", "txt": ".txt,.md,.docx,.csv,.json", "key": ".json,.txt,.pdf,.docx"}
j = json.load(io.open(P, encoding="utf-8"))
by = {s["id"]: s for s in j["strumenti"]}
# 1) il tool esistente prende il nome e la descrizione della logica "prima dell'LLM"
t = by["anonimizza-pdf"]
t["it"] = ["Anonimizza PDF per l'IA", "Rileva nomi, codici fiscali, IBAN e dati sanitari e li sostituisce con *** prima di darli a un LLM."]
t["en"] = ["Anonymize PDF for AI", "Detects names, tax IDs, IBANs and health data and replaces them with *** before you give them to an LLM."]
# 2) famiglia: (id, cat, ico, acc, multi, nuovo, it, itd, en, end)
F = [
 ("chat-privata-pdf", "ai", "🛡️", "pdf", False, True, "Chat privata con il PDF", "Anonimizza, chiede all'IA e rimette i dati veri nella risposta: l'LLM non vede nulla di sensibile.", "Private chat with PDF", "Anonymizes, asks the AI and restores the real data in the answer: the LLM never sees anything sensitive."),
 ("anonimizza-cartelle-cliniche", "ai", "🏥", "pdfimg", True, True, "Anonimizza cartelle cliniche", "Referti, diagnosi e anagrafiche oscurati prima di condividerli o analizzarli con l'IA.", "Anonymize medical records", "Reports, diagnoses and patient details masked before sharing or analyzing with AI."),
 ("anonimizza-reversibile", "ai", "🔁", "pdf", False, True, "Anonimizza con ripristino", "Sostituisce i dati con segnaposto ([PERSONA_1]) e ti dà la chiave per ripristinarli dopo.", "Reversible anonymization", "Swaps data for placeholders ([PERSON_1]) and gives you the key to restore them later."),
 ("ripristina-dati-anonimi", "ai", "🔓", "key", False, True, "Ripristina dati anonimizzati", "Rimette nomi e dati veri nella risposta dell'IA usando la chiave.", "Restore anonymized data", "Puts real names and data back into the AI's answer using the key."),
 ("anonimizza-word", "ai", "🕶️", "doc", True, True, "Anonimizza Word ed Excel", "Oscura i dati sensibili in documenti, fogli e CSV.", "Anonymize Word & Excel", "Masks sensitive data in documents, spreadsheets and CSV files."),
 ("anonimizza-testo", "ai", "🔤", "txt", False, True, "Anonimizza testo", "Incolla o carica un testo: i dati personali diventano ***, pronto per ChatGPT e simili.", "Anonymize text", "Paste or upload text: personal data becomes ***, ready for ChatGPT and the like."),
 ("anonimizza-scansioni", "ai", "📠", "pdfimg", True, True, "Anonimizza scansioni e foto", "Legge il testo con OCR e oscura i dati sensibili anche nelle immagini.", "Anonymize scans & photos", "Reads text with OCR and masks sensitive data even in images."),
 ("rileva-dati-sensibili", "sicurezza", "🔎", "pdfimg", True, True, "Cerca dati sensibili", "Un rapporto di cosa c'è di riservato nel documento, prima di condividerlo.", "Find sensitive data", "A report of what's confidential in the document before you share it."),
]
agg = 0
pos = [s["id"] for s in j["strumenti"]].index("anonimizza-pdf") + 1  # tutti subito dopo il tool originale, nell'ordine scritto
for (i, cat, ico, acc, multi, nuovo, itn, itd, enn, end) in F:
    if i in by: continue
    j["strumenti"].insert(pos, {"id": i, "cat": cat, "ico": ico, "input": "file", "accept": ACC[acc], "multi": multi, "nuovo": nuovo, "it": [itn, itd], "en": [enn, end]})
    pos += 1; agg += 1
ok = {c["id"] for c in j["categorie"]}
ids = [s["id"] for s in j["strumenti"]]
assert len(ids) == len(set(ids)) and all(s["cat"] in ok for s in j["strumenti"])
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(j, f, ensure_ascii=False, indent=1); f.write("\n")
# nota nella filosofia (una volta sola)
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "FILOSOFIA.md")
tx = io.open(D, encoding="utf-8").read()
if "Famiglia ANONIMIZZA" not in tx:
    tx = tx.rstrip("\n") + "\n- Famiglia ANONIMIZZA: rileva dati sensibili (nomi, CF, IBAN, dati sanitari) e li sostituisce con *** o con segnaposto reversibili PRIMA di passare il documento a un LLM (privacy, GDPR, cartelle cliniche). Motore previsto: Presidio + NER in locale su VPS. Il rilevamento non e' perfetto: avvisare di ricontrollare.\n"
    io.open(D, "w", encoding="utf-8", newline="\n").write(tx)
sys.stdout.reconfigure(encoding="utf-8")
print("aggiunti", agg, "- totale", len(ids))
