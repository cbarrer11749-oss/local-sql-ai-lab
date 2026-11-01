import json
import socket
import subprocess
import sys
import threading
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch

import detectar


class EvaluationUnitTests(unittest.TestCase):
    def test_http_error_is_inconclusive(self):
        with patch.object(detectar, 'consultar', side_effect=urllib.error.HTTPError(
                detectar.URL_BASE, 400, 'bad request', {}, None)):
            resultado = detectar.evaluar()
        self.assertEqual(resultado['status'], 'inconclusive')

    def test_invalid_json_is_inconclusive(self):
        respuesta = type('Respuesta', (), {
            '__enter__': lambda self: self,
            '__exit__': lambda self, *args: None,
            'read': lambda self: b'{no-json',
        })()
        with patch.object(urllib.request, 'urlopen', return_value=respuesta):
            resultado = detectar.evaluar()
        self.assertEqual(resultado['status'], 'inconclusive')

    def test_unavailable_server_is_inconclusive(self):
        with patch.object(detectar, 'consultar', side_effect=OSError('offline')):
            resultado = detectar.evaluar()
        self.assertEqual(resultado['status'], 'inconclusive')


class NonFixedIdsTests(unittest.TestCase):
    def evaluar_con_ids_cambiados(self, vulnerable):

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                nombre = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('nombre', [''])[0]
                if nombre == 'ana':
                    usuarios = [[10, 'ana']]
                elif vulnerable:
                    usuarios = [[10, 'ana'], [20, 'luis'], [30, 'maria']]
                else:
                    usuarios = []
                cuerpo = json.dumps({'usuarios': usuarios}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(cuerpo)))
                self.end_headers()
                self.wfile.write(cuerpo)

            def log_message(self, *args):
                pass

        servidor = HTTPServer(('127.0.0.1', 0), Handler)
        hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        try:
            base = 'http://127.0.0.1:%d' % servidor.server_port
            with patch.object(detectar, 'URL_BASE', base):
                return detectar.evaluar()
        finally:
            servidor.shutdown()
            servidor.server_close()
            hilo.join()

    def test_changed_ids_10_20_30_detect_vulnerable_behavior(self):
        self.assertEqual(self.evaluar_con_ids_cambiados(True)['status'], 'suspicious')

    def test_legitimate_suggestions_are_labeled_as_possible_injection(self):
        class SugerenciasHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                nombre = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('nombre', [''])[0]
                usuarios = [[10, 'ana']] if nombre == 'ana' else [
                    [10, 'ana'], [20, 'luis'], [30, 'maria']]
                cuerpo = json.dumps({'usuarios': usuarios}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(cuerpo)))
                self.end_headers()
                self.wfile.write(cuerpo)

            def log_message(self, *args):
                pass

        servidor = HTTPServer(('127.0.0.1', 0), SugerenciasHandler)
        hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        try:
            base = 'http://127.0.0.1:%d' % servidor.server_port
            with patch.object(detectar, 'URL_BASE', base):
                resultado = detectar.evaluar()
            self.assertEqual(resultado['status'], 'suspicious')
            self.assertEqual(resultado['interpretation'], 'Possible SQL injection: the probe input expanded the returned records; confirmation required.')
        finally:
            servidor.shutdown()
            servidor.server_close()
            hilo.join()

    def test_changed_ids_10_20_30_parameterized_behavior_not_detected(self):
        self.assertEqual(self.evaluar_con_ids_cambiados(False)['status'], 'not_detected')


class IntegrationModeTests(unittest.TestCase):
    def ejecutar_modo(self, seguro):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            puerto = sock.getsockname()[1]
        args = [sys.executable, 'app.py', '--puerto', str(puerto)]
        if seguro:
            args.append('--seguro')
        proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            url_base = f'http://127.0.0.1:{puerto}'
            with patch.object(detectar, 'URL_BASE', url_base):
                limite = time.time() + 4
                while time.time() < limite:
                    try:
                        urllib.request.urlopen(url_base + '/', timeout=.2).close()
                        break
                    except OSError:
                        if proc.poll() is not None:
                            self.fail('Could not start app.py')
                        time.sleep(.05)
                else:
                    self.fail('Timed out waiting for app.py to start')
                return detectar.evaluar()['status']
        finally:
            proc.terminate()
            proc.wait(timeout=3)

    def test_vulnerable_mode_is_suspicious(self):
        self.assertEqual(self.ejecutar_modo(False), 'suspicious')

    def test_parameterized_mode_is_not_detected(self):
        self.assertEqual(self.ejecutar_modo(True), 'not_detected')


if __name__ == '__main__':
    unittest.main()
