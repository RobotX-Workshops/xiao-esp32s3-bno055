#!/usr/bin/env python3
"""Local 3D viewer for the webserial_3d firmware.

Reads the board's serial output and serves a three.js page on localhost that
streams the data to the browser (server-sent events). No browser serial
permission prompt is needed.

Usage: viewer.py [port] [http_port]   (defaults: /dev/ttyACM0, 8000)
"""
import json
import queue
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
HTTP_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
PAGE = (Path(__file__).resolve().parent.parent / "viewer" / "index.html").read_bytes()

clients = []
clients_lock = threading.Lock()
state = {}


def broadcast(msg):
    with clients_lock:
        for q in clients:
            q.put(msg)


def read_serial():
    with serial.Serial(PORT, 115200, timeout=1) as s:
        while True:
            line = s.readline().decode(errors="replace").strip()
            key, _, rest = line.partition(":")
            if key not in ("Orientation", "Quaternion", "Calibration"):
                continue
            try:
                state[key.lower()] = [float(v) for v in rest.split(",")]
            except ValueError:
                continue
            if key == "Calibration":  # last line of each sample
                broadcast(json.dumps(state))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            q = queue.Queue()
            with clients_lock:
                clients.append(q)
            try:
                while True:
                    self.wfile.write(f"data: {q.get()}\n\n".encode())
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                with clients_lock:
                    clients.remove(q)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(PAGE)


threading.Thread(target=read_serial, daemon=True).start()
url = f"http://localhost:{HTTP_PORT}"
print(f"Reading {PORT}. Viewer at {url} (Ctrl+C to stop)")
webbrowser.open(url)
try:
    ThreadingHTTPServer(("127.0.0.1", HTTP_PORT), Handler).serve_forever()
except KeyboardInterrupt:
    pass
