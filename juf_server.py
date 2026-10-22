#!/usr/bin/env python3
"""G2B Schoolspelen — Juf-server (optioneel, alleen voor de maker-versie).

Draait lokaal op http://localhost:8410 en beantwoordt vrije vragen van kinderen
via een lokale llama.cpp-server. De juf kent de naam, de taal (NL/EN) en de
zwakke vakken van het kind mee — antwoorden zijn dus écht persoonlijk.
Volledig gratis + open source (MIT) — regel 1.

Aanbevolen model: Qwen2.5-3B-Instruct (Q4 GGUF ≈ 2,5 GB) — klein genoeg om
lekker op CPU te draaien op 16 GB machines. Qwen3-4B werkt ook (trager).

Gebruik:
  1. Start llama.cpp server:  ./llama-server -m qwen2.5-3b-instruct-q4.gguf --port 8080
  2. Start dit script:        python juf_server.py
  3. Maak een bestand juf_server.js naast index.html met:
       var JUF_SERVER="http://localhost:8410/juf";
  4. In de app: "Vraag het aan Juf/Meester" gebruikt nu de échte AI-juf.
     Zonder dit bestand of zonder server werkt alles automatisch offline verder.
"""
import json, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

LLAMA = "http://localhost:8080/v1/chat/completions"

SYSTEEM_NL = (
    "Je bent {juf}, een lieve Nederlandse juf/meester voor kinderen van 4 tot 18 jaar. "
    "Beantwoord elke vraag kort (2-3 zinnen), vriendelijk, correct en in simpel "
    "Nederlands. Geef een voorbeeld als het helpt. Eindig positief en moedig het "
    "kind aan om verder te vragen. Geen emoji's — je antwoord wordt voorgelezen."
)
SYSTEEM_EN = (
    "You are {juf}, a kind teacher for children aged 4 to 18. "
    "Answer every question briefly (2-3 sentences), friendly, correct and in simple "
    "English. Give an example if it helps. End positively and encourage the child to "
    "keep asking questions. No emojis — your answer is read aloud."
)


def beantwoord(vraag: str, naam: str = "", taal: str = "nl",
               zwak: list = None, juf: str = "Juf Jet") -> str:
    sjabloon = SYSTEEM_EN if taal == "en" else SYSTEEM_NL
    systeem = sjabloon.format(juf=juf)
    ctx = []
    if naam:
        ctx.append(("the child's name is " + naam) if taal == "en"
                   else ("het kind heet " + naam))
    if zwak:
        ctx.append(("currently practices extra on: " + ", ".join(zwak)) if taal == "en"
                   else ("oefent nu vooral met: " + ", ".join(zwak)))
    if ctx:
        systeem += " Context: " + "; ".join(ctx) + "."
    body = json.dumps({
        "messages": [
            {"role": "system", "content": systeem},
            {"role": "user", "content": vraag},
        ],
        "temperature": 0.5,
        "max_tokens": 140,
    }).encode()
    req = urllib.request.Request(LLAMA, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.load(r)
    return j["choices"][0]["message"]["content"].strip()


class Juf(BaseHTTPRequestHandler):
    def _headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self._headers(204)

    def do_POST(self):
        if self.path != "/juf":
            self._headers(404)
            self.wfile.write(b"{}")
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            b = json.loads(self.rfile.read(n) or b"{}")
            q = b.get("vraag", "")[:400]
            antwoord = (beantwoord(q, naam=b.get("naam", "")[:60],
                                   taal=b.get("taal", "nl"),
                                   zwak=b.get("zwak") or [],
                                   juf=b.get("juf", "Juf Jet")[:60])
                        if q else "Stel eerst een vraag!")
        except Exception as e:
            antwoord = f"De juf-server kon je vraag niet verwerken ({e})."
        self._headers(200)
        self.wfile.write(json.dumps({"antwoord": antwoord}).encode())


if __name__ == "__main__":
    print("Juf-server draait op http://localhost:8410/juf (Ctrl+C = stop)")
    HTTPServer(("127.0.0.1", 8410), Juf).serve_forever()
