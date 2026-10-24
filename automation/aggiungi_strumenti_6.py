# -*- coding: utf-8 -*-
"""aggiungi_strumenti_6.py - ESPANSIONE A TUTTE LE CATEGORIE (non solo PDF/immagini/audio/video): 8 nuovi settori
testo, office (Word/Excel/dati), business (fisco IT), studio, marketing (SEO/social), sviluppatori, privacy, calcolatori.
Dati in automation/dati_strumenti_6.txt (una riga per tool). Rilanciabile: salta gli id gia' presenti, non duplica settori/categorie.
Perche' queste: gli strumenti "piccoli" (contatore parole, JSON, QR, IVA, password, convertitori) hanno volumi di ricerca enormi e sono i piu' facili da
costruire davvero nel browser; le versioni con IA (riassunto, email, SEO, studio) sono quelle che i concorrenti fanno pagare.
Dopo: python automation\\genera_strumenti.py  e  python automation\\allinea_hash.py en"""
import io, json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, "assets", "data", "strumenti.json")
j = json.load(io.open(P, encoding="utf-8"))
ACC = {"x": ".xls,.xlsx,.csv", "w": ".doc,.docx", "p": ".pdf,application/pdf", "i": "image/*",
       "a": "audio/*,.mp3,.wav,.m4a,.ogg,.flac", "v": "video/*,.mp4,.mov,.mkv,.avi,.webm"}
S = lambda i, it, en, si, se, ico, col, di, de: {"id": i, "it": it, "en": en, "slug": {"it": si, "en": se}, "ico": ico, "colore": col, "desc": {"it": di, "en": de}}
SET = [
 S("testo", "Strumenti testo e scrittura", "Writing tools", "strumenti-testo", "writing-tools", "✍️", "#0ea5e9", "Riassumi, correggi, traduci e riscrivi i tuoi testi.", "Summarize, proofread, translate and rewrite your texts."),
 S("office", "Strumenti Word, Excel e dati", "Office and data tools", "strumenti-office", "office-tools", "📊", "#22a559", "Converti, pulisci e analizza file Excel, CSV e Word.", "Convert, clean and analyze Excel, CSV and Word files."),
 S("business", "Strumenti business e fisco", "Business and tax tools", "strumenti-business", "business-tools", "💼", "#f59e0b", "IVA, codice fiscale, preventivi, modelli e calcoli per chi lavora in Italia.", "VAT, tax code, quotes, templates and calculators for Italy."),
 S("studio", "Strumenti per studiare", "Study tools", "strumenti-studio", "study-tools", "🎓", "#8b5cf6", "Quiz, flashcard, schemi, bibliografia e tutor per studenti.", "Quizzes, flashcards, outlines, bibliography and tutors for students."),
 S("marketing", "Strumenti SEO e social", "SEO and social tools", "strumenti-seo-social", "seo-social-tools", "📈", "#e5322d", "Meta tag, hashtag, post e piani editoriali con l'IA.", "Meta tags, hashtags, posts and content calendars with AI."),
 S("sviluppatori", "Strumenti per sviluppatori", "Developer tools", "strumenti-sviluppatori", "developer-tools", "💻", "#4b5563", "JSON, regex, Base64, hash, QR code e codice con l'IA.", "JSON, regex, Base64, hashes, QR codes and code with AI."),
 S("privacy", "Strumenti privacy e sicurezza", "Privacy and security tools", "strumenti-privacy", "privacy-tools", "🔒", "#2d7ff9", "Password, truffe, phishing e protezione dei tuoi dati.", "Passwords, scams, phishing and protecting your data."),
 S("utility", "Calcolatori e convertitori", "Calculators and converters", "strumenti-calcolatori", "calculators", "🧮", "#f08a24", "Percentuali, unità, mutuo, date e tutto quello che serve ogni giorno.", "Percentages, units, mortgage, dates and everyday helpers."),
]
C = lambda i, s, it, en, col: {"id": i, "settore": s, "it": it, "en": en, "colore": col}
CAT = [
 C("txt-scrivi", "testo", "Scrivi e correggi", "Write and proofread", "#0ea5e9"), C("txt-analizza", "testo", "Analizza testo", "Analyze text", "#22a559"),
 C("off-excel", "office", "Excel e CSV", "Excel and CSV", "#22a559"), C("off-word", "office", "Word e documenti", "Word and documents", "#2d7ff9"),
 C("biz-fisco", "business", "Fisco e calcoli", "Tax and calculations", "#f59e0b"), C("biz-doc", "business", "Documenti e modelli", "Documents and templates", "#8b5cf6"),
 C("stu-impara", "studio", "Impara e ripassa", "Learn and review", "#8b5cf6"), C("stu-scrivi", "studio", "Tesi e voti", "Thesis and grades", "#f59e0b"),
 C("mkt-seo", "marketing", "SEO e contenuti", "SEO and content", "#e5322d"), C("mkt-social", "marketing", "Social media", "Social media", "#0ea5e9"),
 C("dev-formato", "sviluppatori", "Formattatori", "Formatters", "#4b5563"), C("dev-codici", "sviluppatori", "Codifica e hash", "Encoding and hashing", "#2d7ff9"),
 C("dev-ia", "sviluppatori", "Codice con l'IA", "Code with AI", "#7c3aed"), C("dev-web", "sviluppatori", "Strumenti web", "Web tools", "#22a559"),
 C("prv-password", "privacy", "Password", "Passwords", "#2d7ff9"), C("prv-dati", "privacy", "Truffe e dati", "Scams and data", "#e5322d"),
 C("cal-conv", "utility", "Calcolatori", "Calculators", "#f08a24"), C("cal-data", "utility", "Date e orari", "Dates and time", "#0ea5e9"),
]
for s in SET:
    if not any(x["id"] == s["id"] for x in j["settori"]): j["settori"].append(s)
for c in CAT:
    if not any(x["id"] == c["id"] for x in j["categorie"]): j["categorie"].append(c)
def acc(a):  # "it" con apostrofo ASCII -> lettera accentata (solo testi italiani)
    a = re.sub(r"\b(piu|unita|eta|attivita|leggibilita|citta|pubblicita|li|e)'(?=\s|$|[.,;:?!])", lambda m: ({"piu": "più", "unita": "unità", "eta": "età", "attivita": "attività", "leggibilita": "leggibilità", "citta": "città", "pubblicita": "pubblicità", "li": "lì", "e": "è"}[m.group(1).lower()]).capitalize() if m.group(1)[0].isupper() else {"piu": "più", "unita": "unità", "eta": "età", "attivita": "attività", "leggibilita": "leggibilità", "citta": "città", "pubblicita": "pubblicità", "li": "lì", "e": "è"}[m.group(1)], a, flags=re.I)
    return a
by = {t["id"]: t for t in j["strumenti"]}
agg = 0
for riga in io.open(os.path.join(R, "automation", "dati_strumenti_6.txt"), encoding="utf-8"):
    riga = riga.rstrip("\n")
    if not riga.strip() or riga.startswith("#"): continue
    i, cat, ico, tipo, it_n, it_d, en_n, en_d = riga.split("|")
    if i in by: continue
    multi = tipo.endswith("m"); tipo = tipo.rstrip("m")
    if tipo == "t": inp, ac = "testo", ""
    elif tipo == "u": inp, ac = "url", ""
    else: inp, ac = "file", ",".join(ACC[k] for k in tipo[1:])
    t = {"id": i, "cat": cat, "ico": ico, "input": inp, "accept": ac, "multi": multi, "nuovo": True, "it": [acc(it_n), acc(it_d)], "en": [en_n, en_d]}
    j["strumenti"].append(t); by[i] = t; agg += 1
# rifinitura accenti anche sui tool delle ricerche precedenti (script 5 usava piu' e attivita' senza accento)
for t in j["strumenti"]: t["it"] = [acc(t["it"][0]), acc(t["it"][1])]
ok = {c["id"] for c in j["categorie"]}; oks = {s["id"] for s in j["settori"]}
ids = [s["id"] for s in j["strumenti"]]
assert len(ids) == len(set(ids)) and all(s["cat"] in ok for s in j["strumenti"]) and all(c["settore"] in oks for c in j["categorie"])
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(j, f, ensure_ascii=False, indent=1); f.write("\n")
D = os.path.join(R, "docs", "FILOSOFIA.md")
tx = io.open(D, encoding="utf-8").read()
if "ESPANSIONE A TUTTE LE CATEGORIE" not in tx:
    tx = tx.rstrip("\n") + "\n- ESPANSIONE A TUTTE LE CATEGORIE (script aggiungi_strumenti_6.py + automation/dati_strumenti_6.txt): oltre a PDF, immagini, audio e video ora ci sono testo, Word/Excel/dati, business e fisco italiano, studio, SEO e social, sviluppatori, privacy e calcolatori (12 settori; il menu 'Strumenti' li raggruppa in una tendina). Regola: ogni idea nuova = una riga nel file dati, poi genera_strumenti.py. Ordine di sviluppo reale (nel browser, senza VPS): contatore parole, JSON, Base64, QR, password, IVA, convertitori; poi quelli con IA (serve la VPS).\n"
    io.open(D, "w", encoding="utf-8", newline="\n").write(tx)
sys.stdout.reconfigure(encoding="utf-8")
print("aggiunti", agg, "- totale", len(ids), "- settori", len(j["settori"]))
