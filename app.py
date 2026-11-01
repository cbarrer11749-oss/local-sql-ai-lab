"""SQL injection lab with fictional data; listens on loopback only."""
import argparse
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def buscar(nombre, seguro):
    db = sqlite3.connect(':memory:')
    try:
        db.execute('CREATE TABLE usuarios (id INTEGER, nombre TEXT)')
        db.executemany('INSERT INTO usuarios VALUES (?, ?)', [(1, 'ana'), (2, 'luis'), (3, 'maria')])
        if seguro:
            return db.execute('SELECT id, nombre FROM usuarios WHERE nombre = ?', (nombre,)).fetchall()
        # Intentional vulnerability: concatenating input lets it alter the query.
        return db.execute("SELECT id, nombre FROM usuarios WHERE nombre = '" + nombre + "'").fetchall()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seguro', action='store_true')
    parser.add_argument('--puerto', type=int, default=8765)
    args = parser.parse_args()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlparse(self.path)
            if url.path == '/buscar':
                nombre = parse_qs(url.query, keep_blank_values=True).get('nombre', [''])[0]
                try:
                    body = json.dumps({'usuarios': buscar(nombre, args.seguro)}).encode()
                    status = 200
                except sqlite3.Error:
                    body, status = b'{"error": "invalid query"}', 400
                content_type = 'application/json'
            elif url.path == '/':
                body = ('<!doctype html><meta charset="utf-8"><title>SQL Lab</title>'
                        '<h1>Local lab: SQL injection</h1>'
                        '<p>Fictional data: ana, luis, maria.</p>'
                        '<form action="/buscar"><label>Name: <input name="nombre" value="ana"></label>'
                        '<button>Search</button></form>').encode()
                status, content_type = 200, 'text/html; charset=utf-8'
            else:
                body, status, content_type = b'Not found', 404, 'text/plain'
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = HTTPServer(('127.0.0.1', args.puerto), Handler)
    print('Mode:', 'parameterized' if args.seguro else 'vulnerable', flush=True)
    print(f'Open http://127.0.0.1:{args.puerto} — stop with Ctrl+C', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
