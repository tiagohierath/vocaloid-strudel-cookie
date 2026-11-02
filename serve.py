#!/usr/bin/env python3
"""Sophie Pallas local server: Python standard library only."""
import argparse
import hashlib
import io
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent

def revision():
    return hashlib.sha256('|'.join(f'{p.name}:{p.stat().st_mtime_ns}' for p in sorted(ROOT.iterdir()) if p.suffix in {'.html', '.js', '.css'}).encode()).hexdigest()

class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        route = urlsplit(self.path).path
        if route == '/__dev_version':
            data = revision().encode()
            content_type = 'text/plain'
        elif route in ('/', '/index.html'):
            source = (ROOT / 'index.html').read_text()
            # Inject only while serving locally; the game files remain portable.
            reload_script = '''<script>(()=>{const initial=VERSION;let reloading=false;
setInterval(async()=>{try{const r=await fetch('/__dev_version',{cache:'no-store'});
if(r.ok&&(await r.text())!==initial&&!reloading){reloading=true;location.reload();}}catch{}},1500);
})();</script>'''.replace('VERSION', json.dumps(revision()))
            data = source.replace('</body>', reload_script + '</body>').encode()
            content_type = 'text/html; charset=utf-8'
        else:
            return super().send_head()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        return io.BytesIO(data)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        if '/__dev_version' not in str(args):
            super().log_message(format, *args)

def main():
    parser = argparse.ArgumentParser(description='Run Sophie Pallas locally.')
    parser.add_argument('--port', type=int, default=5175)
    parser.add_argument('--host', default='127.0.0.1')
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer((args.host, args.port), partial(Handler, directory=str(ROOT)))
    except OSError as error:
        parser.exit(1, f'Cannot start Sophie Pallas: {error}\nIf it is already running, open http://localhost:{args.port}. Otherwise try ./run.sh --port 5176\n')
    print(f'Sophie Pallas: http://localhost:{args.port}\nPress Ctrl+C to stop. File edits reload the page automatically.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
