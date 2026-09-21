"""
Despachador de sesión Jules para Victoria Perez (victoriaperez050622@gmail.com)
Proyecto: 0072-cmre-engine
"""
import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

CREDS_FILE = r"C:\Users\rafae\.gemini\01_PROYECTOS\planes_jules_2026\credenciales_jules_multicuenta.json"
URL_SESSIONS = "https://jules.googleapis.com/v1alpha/sessions"

with open(CREDS_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

vic_acc = [acc for acc in data['cuentas'] if acc['email'] == 'victoriaperez050622@gmail.com'][0]
api_key = vic_acc['jules_api_key']

prompt_text = """Hola Jules. Iniciamos el ciclo diario de auto-evolución en el proyecto `0072-cmre-engine` (Competitive ML Reasoning Engine) para **Perez, Ernesto Rafael ("Rafa")** y **Victoria Perez**.

Pasos de Inicialización y Memoria:
1. Abre y lee `ARQUITECTURA_ESTADO.md` y `JULES_DYNAMIC_TASKS.md` para conocer el estado del código, módulos canónicos e inventario.
2. Revisa `JULES_EXECUTION_LOG.md` para comprobar los hitos de la entrada 001.
3. Ejecuta `pytest tests/` para validar el estado de partida del repositorio (85/85 tests pasando al 100%).
4. Verifica la estructura de `src/cmre/modules/` y familiarízate con las tareas de `JULES_DYNAMIC_TASKS.md`.
5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."""

payload = {
    "prompt": prompt_text,
    "sourceContext": {
        "source": "sources/github/perezernestorafael933/0072-cmre-engine",
        "githubRepoContext": {
            "startingBranch": "main"
        }
    },
    "title": "0072-CMRE: Tarea 1 - Ciclo Diario de Auto-Evolucion e Inspeccion Canonica"
}

req = urllib.request.Request(
    URL_SESSIONS,
    data=json.dumps(payload).encode('utf-8'),
    headers={
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read().decode())
        print("SUCCESS! Jules Session Created:")
        print(json.dumps(body, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP ERROR {e.code}: {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
