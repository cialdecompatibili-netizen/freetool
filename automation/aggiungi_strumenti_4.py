# -*- coding: utf-8 -*-
"""aggiungi_strumenti_4.py - divide il settore "Audio e video" in due settori: Strumenti audio e Strumenti video.
Cosi' i settori diventano 4 (PDF, immagini, audio, video) e genera_strumenti.py mette da solo la tendina "Strumenti" nel menu.
Rilanciabile: se audio-video non esiste piu' non fa nulla. Dopo: python automation\\genera_strumenti.py  e  python automation\\allinea_hash.py en"""
import io, json, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "strumenti.json")
j = io.open(P, encoding="utf-8").read()
j = json.loads(j)
if not any(s["id"] == "audio-video" for s in j["settori"]):
    print("gia' diviso, niente da fare"); sys.exit(0)
AUDIO = {"id": "audio", "it": "Strumenti audio", "en": "Audio tools", "slug": {"it": "strumenti-audio", "en": "audio-tools"}, "ico": "\U0001F3A7", "colore": "#22a559",
         "desc": {"it": "Trascrivi, converti, taglia e pulisci i tuoi file audio.", "en": "Transcribe, convert, trim and clean your audio files."}}
VIDEO = {"id": "video", "it": "Strumenti video", "en": "Video tools", "slug": {"it": "strumenti-video", "en": "video-tools"}, "ico": "\U0001F3AC", "colore": "#e5322d",
         "desc": {"it": "Sottotitola, comprimi, taglia e converti i tuoi video.", "en": "Caption, compress, trim and convert your videos."}}
i = [s["id"] for s in j["settori"]].index("audio-video")
j["settori"][i:i + 1] = [AUDIO, VIDEO]
# categorie: av-trascrivi si divide in audio e video
cats = [c for c in j["categorie"] if c["id"] != "av-trascrivi"]
for c in cats:
    if c["id"] == "av-audio": c["settore"] = "audio"
    if c["id"] == "av-video": c["settore"] = "video"
k = [c["id"] for c in cats].index("av-audio")
cats.insert(k, {"id": "av-trascrivi-audio", "settore": "audio", "it": "Trascrivi audio", "en": "Transcribe audio", "colore": "#0ea5e9"})
k = [c["id"] for c in cats].index("av-video")
cats.insert(k, {"id": "av-trascrivi-video", "settore": "video", "it": "Sottotitoli e riassunti", "en": "Captions & summaries", "colore": "#0ea5e9"})
j["categorie"] = cats
for t in j["strumenti"]:
    if t["id"] in ("trascrivi-audio", "verbale-riunione"): t["cat"] = "av-trascrivi-audio"
    elif t["cat"] == "av-trascrivi": t["cat"] = "av-trascrivi-video"
    elif t["id"] == "doppiaggio-ia": t["cat"] = "av-video"
ok = {c["id"] for c in j["categorie"]}
assert all(t["cat"] in ok for t in j["strumenti"])
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(j, f, ensure_ascii=False, indent=1); f.write("\n")
print("settori:", [s["id"] for s in j["settori"]])
