#!/usr/bin/env python3
"""
Farcaster Frame Server - Production
Serves Farcaster frames with Base payment unlock.
"""
import http.server
import json
import os
import socketserver
import urllib.request
from pathlib import Path

PORT = int(os.environ.get("PORT", 8080))
WALLET = "0x2d44fc27a616606b42448309F4d8e3F423d93267"

# Knowledge base index - lightweight
KB = {
    "openwork_credentials": "/home/user/wiki/raw/openwork_credentials.json",
    "delx_artifacts": "/home/user/wiki/raw/delx_ontology_path_artifacts.json",
}

def serve_frame_html():
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta property="fc:frame" content="vNext" />
  <meta property="fc:frame:image" content="https://arweave.net/agenticdao-unlock-v1" />
  <meta property="fc:frame:post_url" content="https://{os.environ.get('RAILWAY_URL', 'localhost')}/frame/action" />
  <meta property="fc:frame:button:1" content="🔓 Unlock Premium — 0.01 ETH" />
  <meta property="fc:frame:button:1:action" content="tx" />
  <meta property="fc:frame:button:1:target" content="{WALLET}" />
  <meta property="og:title" content="AgenticDAO Premium Frame" />
  <meta property="og:description" content="Unlock premium agent capabilities with Base micro-payment." />
  <meta property="og:image" content="https://arweave.net/agenticdao-unlock-v1" />
</head>
<body>
  <h1>AgenticDAO Premium Frame</h1>
  <p>Unlock premium agent capabilities.</p>
  <p>Payment: 0.01 ETH on Base</p>
  <p>Wallet: {WALLET}</p>
</body>
</html>"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/frame":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(serve_frame_html().encode())
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving Farcaster Frame on port {PORT}")
    print(f"Credentials loaded from: {KB}")
    httpd.serve_forever()
