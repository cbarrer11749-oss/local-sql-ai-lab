"""Educational probe limited to this local lab server."""
import json
import urllib.parse
import urllib.request

HOST = '127.0.0.1'
PUERTO = 8765
URL_BASE = f'http://{HOST}:{PUERTO}'


def consultar(nombre):
    url = URL_BASE + '/buscar?' + urllib.parse.urlencode({'nombre': nombre})
    with urllib.request.urlopen(url, timeout=3) as response:
        datos = json.load(response)
    usuarios = datos.get('usuarios') if isinstance(datos, dict) else None
    if not isinstance(usuarios, list) or any(
            not isinstance(usuario, (list, tuple)) or len(usuario) != 2
            for usuario in usuarios):
        raise ValueError('unexpected response format')
    return usuarios


def evaluar():
    try:
        normal = consultar('ana')
        prueba = consultar("' OR '1'='1")
        registros_normales = {tuple(usuario) for usuario in normal}
        registros_prueba = {tuple(usuario) for usuario in prueba}
        if normal and len(prueba) > len(normal) and registros_prueba > registros_normales:
            status = 'suspicious'
            interpretation = 'Possible SQL injection: the probe input expanded the returned records; confirmation required.'
        else:
            status = 'not_detected'
            interpretation = 'This probe did not detect injection; this does not prove that other flaws are absent.'
        return {
            'target': URL_BASE,
            'normal_result_count': len(normal),
            'probe_result_count': len(prueba),
            'status': status,
            'interpretation': interpretation,
            'remediation': 'Use a parameterized query; keep SQL and data separate.',
        }
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {
            'target': URL_BASE,
            'status': 'inconclusive',
            'interpretation': 'The probe could not be completed or validated.',
            'details': str(error),
        }


if __name__ == '__main__':
    print(json.dumps(evaluar(), ensure_ascii=False, indent=2))
