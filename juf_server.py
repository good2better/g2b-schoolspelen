#!/usr/bin/env python3
"""G2B Schoolspelen — Juf-server (optioneel, alleen voor de maker-versie).

Draait lokaal op http://localhost:8410 en beantwoordt vrije vragen van kinderen
via een lokale llama.cpp-server (bijv. Qwen3-4B, zoals in PagePlay gebruikt).
Volledig gratis + open source (MIT) — regel 1.

Gebruik:
  1. Start llama.cpp server:  ./llama-server -m qwen3-4b.gguf --port 8080
  2. Start dit script:        python juf_server.py
  3. Maak een bestand juf_server.js naast index.html met:
       var JUF_SERVER="http://localhost:8410/juf";
  4. In de app: "Vraag het aan Juf/Meester" gebruikt nu de échte AI-juf.
     Zonder dit bestand of zonder server werkt alles automatisch offline verder.
"""
import json, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

LLAMA = "http://localhost:8080/v1/chat/completions"

SYSTEEM = (
    "Je bent Juf Jet, een lieve Nederlandse juf voor kinderen van 4 tot 18 jaar. "
    "Beantwoord elke vraag kort (2-3 zinnen), vriendelijk, correct en in simpel "
    "Nederlands. Geef een voorbeeld als het helpt. Eindig positief en moedig het "
    "kind aan om verder te vragen. Geen emoji's — je antwoord wordt voorgelezen."
)

def beantwoord(vraag: str) -> str:
    body = json.dumps({
        "messages": [
            {"role": "system", "content": SYSTEEM},
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
            q = json.loads(self.rfile.read(n) or b"{}").get("vraag", "")[:400]
            antwoord = beantwoord(q) if q else "Stel eerst een vraag!"
        except Exception as e:
            antwoord = f"De juf-server kon je vraag niet verwerken ({e})."
        self._headers(200)
        self.wfile.write(json.dumps({"antwoord": antwoord}).encode())

if __name__ == "__main__":
    print("Juf-server draait op http://localhost:8410/juf (Ctrl+C = stop)")
    HTTPServer(("127.0.0.1", 8410), Juf).serve_forever()
