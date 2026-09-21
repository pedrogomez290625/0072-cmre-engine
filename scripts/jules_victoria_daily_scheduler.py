"""
JULES VICTORIA DAILY SCHEDULER (02:30 AM - 03:30 AM - 04:30 AM)
Proyecto: 0072-cmre-engine & Ecosistema Angelus
Cuenta: Victoria Perez (victoriaperez050622@gmail.com)
Investigador Principal: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

CREDS_FILE = r"C:\Users\rafae\.gemini\01_PROYECTOS\planes_jules_2026\credenciales_jules_multicuenta.json"
URL_SESSIONS = "https://jules.googleapis.com/v1alpha/sessions"
DEFAULT_SOURCE = "sources/github/perezernestorafael933/0072-cmre-engine"

SCHEDULED_TASKS = {
    1: {
        "time": "02:30",
        "title": "0072-CMRE: Tarea Programada 1/3 (02:30 AM) - Inicio de Día y Memoria",
        "prompt": """Hola Jules. Iniciamos el ciclo diario de auto-evolución en el proyecto `0072-cmre-engine` (Competitive ML Reasoning Engine) para **Perez, Ernesto Rafael ("Rafa")** y **Victoria Perez**.

Pasos de Inicialización y Memoria:
1. Abre y lee `ARQUITECTURA_ESTADO.md` y `JULES_DYNAMIC_TASKS.md` para conocer el estado del código, módulos canónicos e inventario.
2. Revisa `JULES_EXECUTION_LOG.md`. Si la sesión anterior terminó con algún error o tarea incompleta, toma nota del fallo para corregirlo prioritariamente.
3. Si `JULES_DYNAMIC_TASKS.md` no existe o está vacío, créalo analizando los 6 módulos canónicos en disco (`src/cmre/modules/`).
4. Ejecuta `pytest tests/` para validar el estado de partida del repositorio (debe mantener el 100% de tests en verde).
5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."""
    },
    2: {
        "time": "03:30",
        "title": "0072-CMRE: Tarea Programada 2/3 (03:30 AM) - Ejecución Intermedia & Módulos Canónicos",
        "prompt": """Hola Jules. Continuamos con el desarrollo autónomo en `0072-cmre-engine` (Competitive ML Reasoning Engine) para **Perez, Ernesto Rafael ("Rafa")** y **Victoria Perez**.

Pasos de Ejecución Intermedia:
1. Consulta las 7 reglas de arquitectura en `JULES_ARCHITECTURE_RULES.md` y las tareas dinámicas en `JULES_DYNAMIC_TASKS.md`.
2. Ejecuta las tareas enfocadas en la misión principal del proyecto: Optimización de razonamiento ML, funciones de pérdida diferenciables, validación cruzada purgada, pipelines DICOM y kernels HPC.
3. Refactoriza e incrementa los módulos principales (`src/cmre/modules/` y `src/cmre/services/`) sin romper funcionalidades previas ni alterar firmas públicas, asegurando resiliencia en la base de datos (fallback SQLite/PostgreSQL) y en los Servidores MCP de `AGENTS.md`.
4. Corre `pytest tests/` y confirma pasaje al 100%. En caso de error, no te detengas; registra el diagnóstico parcial en `JULES_EXECUTION_LOG.md` y aplica la recuperación quirúrgica.
5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."""
    },
    3: {
        "time": "04:30",
        "title": "0072-CMRE: Tarea Programada 3/3 (04:30 AM) - Cierre, Logs y Reescritura Dinámica",
        "prompt": """Hola Jules. Sesión final de cierre y auto-evolución en `0072-cmre-engine` para **Perez, Ernesto Rafael ("Rafa")** y **Victoria Perez**.

Pasos de Cierre, Registro de Log y Reescritura Autónoma:
1. Ejecuta la suite completa de pruebas con `pytest tests/` y documenta el resultado de la sesión.
2. REGISTRO DE LOG DE EJECUCIÓN: Registra una entrada en `JULES_EXECUTION_LOG.md` anotando la fecha, tareas completadas, pruebas pasadas y cualquier fallo o advertencia detectada con su plan de remediación.
3. Actualiza `ARQUITECTURA_ESTADO.md` registrando la lista de módulos actualizados y el diff de arquitectura de hoy.
4. AUTO-REESCRITURA DINÁMICA: Evalúa los requerimientos futuros del motor CMRE (HPC, kernels GPU, validadores de torneos), Y REESCRIBE TOTALMENTE `JULES_DYNAMIC_TASKS.md` grabando entre 5 y 10 nuevas super-tareas autónomas para la sesión de mañana.
5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."""
    }
}

def get_victoria_api_key():
    if not os.path.exists(CREDS_FILE):
        raise FileNotFoundError(f"Credenciales no encontradas en {CREDS_FILE}")
    with open(CREDS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    vic = [c for c in data.get('cuentas', []) if c.get('email') == 'victoriaperez050622@gmail.com']
    if not vic:
        raise ValueError("Cuenta victoriaperez050622@gmail.com no encontrada en credenciales")
    return vic[0]['jules_api_key']

def dispatch_task(task_num, source=DEFAULT_SOURCE):
    if task_num not in SCHEDULED_TASKS:
        print(f"[ERROR] Tarea inválida: {task_num}. Use 1, 2 o 3.")
        return None
    
    api_key = get_victoria_api_key()
    task = SCHEDULED_TASKS[task_num]
    
    payload = {
        "prompt": task["prompt"],
        "sourceContext": {
            "source": source,
            "githubRepoContext": {
                "startingBranch": "main"
            }
        },
        "title": task["title"]
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
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SUCCESS] Tarea {task_num} despachada a Jules!")
            print(f"  Session ID: {body.get('id')}")
            print(f"  URL: {body.get('url')}")
            print(f"  Title: {body.get('title')}")
            return body
    except urllib.error.HTTPError as e:
        print(f"[HTTP ERROR {e.code}]: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"[ERROR]: {e}")
        return None

def show_status():
    api_key = get_victoria_api_key()
    url = f"{URL_SESSIONS}?pageSize=10"
    req = urllib.request.Request(url, headers={'X-Goog-Api-Key': api_key})
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode())
            sessions = body.get('sessions', [])
            print(f"\n--- ÚLTIMAS SESIONES JULES (CUENTA VICTORIA: victoriaperez050622@gmail.com) ---")
            for s in sessions:
                name = s.get('name')
                state = s.get('state')
                title = s.get('title', '')[:50]
                url = s.get('url')
                print(f"• [{state:12}] {name} | {title}")
                print(f"  Web: {url}")
    except Exception as e:
        print(f"[ERROR consultando status]: {e}")

def run_daemon(source=DEFAULT_SOURCE):
    print("=" * 70)
    print("🌙 INICIANDO DAEMON DIARIO JULES PARA VICTORIA PEREZ")
    print(f"Repositorio: {source}")
    print("Horarios programados todos los días:")
    print("  • 02:30 AM -> Tarea 1 (Inicio de Día & Memoria)")
    print("  • 03:30 AM -> Tarea 2 (Ejecución Intermedia & Módulos)")
    print("  • 04:30 AM -> Tarea 3 (Cierre, Logs & Reescritura)")
    print("=" * 70)
    
    targets = [
        (1, 2, 30),
        (2, 3, 30),
        (3, 4, 30)
    ]
    
    while True:
        now = datetime.now()
        next_events = []
        for task_num, hour, minute in targets:
            sched = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if sched <= now:
                sched += timedelta(days=1)
            wait_sec = (sched - now).total_seconds()
            next_events.append((wait_sec, task_num, sched))
        
        next_events.sort(key=lambda x: x[0])
        wait_seconds, next_task, next_time = next_events[0]
        
        hours_wait = wait_seconds / 3600
        print(f"\n[DAEMON] Próxima tarea: Tarea {next_task} programada para {next_time.strftime('%Y-%m-%d %H:%M:%S')} (espera: {hours_wait:.2f} h / {int(wait_seconds)} s)")
        
        # Dormir hasta la hora programada
        time.sleep(wait_seconds)
        
        print(f"\n[ALERTA] Hora alcanzada: ejecutando Tarea {next_task}...")
        dispatch_task(next_task, source=source)
        # Esperar 60 segundos para evitar re-disparos en el mismo minuto
        time.sleep(65)

def print_windows_schtasks():
    py_path = sys.executable
    script_path = os.path.abspath(__file__)
    print("\n" + "=" * 70)
    print("🛠️ COMANDOS PARA REGISTRAR EN WINDOWS TASK SCHEDULER (schtasks.exe):")
    print("Ejecuta estos 3 comandos en PowerShell o CMD como Administrador para que")
    print("Windows despache automáticamente las 3 tareas de Jules sin depender del IDE:")
    print("=" * 70)
    
    for num, task in SCHEDULED_TASKS.items():
        t = task["time"]
        cmd = f'schtasks /create /tn "Jules_Victoria_CMRE_Task_{num}" /tr "\"{py_path}\" \"{script_path}\" --dispatch {num}" /sc daily /st {t} /f'
        print(f"\n# Tarea {num} ({t} AM):")
        print(cmd)
    print("=" * 70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jules Victoria Daily Scheduler")
    parser.add_argument("--dispatch", type=int, choices=[1, 2, 3], help="Despachar inmediatamente tarea 1, 2 o 3")
    parser.add_argument("--status", action="store_true", help="Mostrar estado de sesiones recientes")
    parser.add_argument("--daemon", action="store_true", help="Ejecutar en modo daemon continuo")
    parser.add_argument("--windows-tasks", action="store_true", help="Mostrar comandos de Windows Task Scheduler")
    parser.add_argument("--source", type=str, default=DEFAULT_SOURCE, help="Source GitHub en Jules API")
    
    args = parser.parse_args()
    
    if args.dispatch:
        dispatch_task(args.dispatch, source=args.source)
    elif args.status:
        show_status()
    elif args.daemon:
        run_daemon(source=args.source)
    elif args.windows_tasks:
        print_windows_schtasks()
    else:
        parser.print_help()
        print("\n" + "=" * 70)
        for num, task in SCHEDULED_TASKS.items():
            print(f"Tarea {num} [{task['time']} AM]: {task['title']}")
        print("=" * 70)
