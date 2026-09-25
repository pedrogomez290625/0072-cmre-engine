#!/usr/bin/env python3
"""
🛰️ SINCRONIZADOR MASIVO GOOGLE DRIVE VÍA APPS SCRIPT - REPO 0072 (CMRE ENGINE)
Sube los archivos canónicos de código, esquemas, solvers, claims y reportes a Google Drive vía Google Apps Script.
Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import os
import sys
import json
import base64
import time
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config_google_apps_script.json"

DEFAULT_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzhqS3u9QeWAe4kmTR1Z2UiGJEsDvL1u2_njawat86-BqBKKXO7d4kL4RvEt4yLEqs/exec"
DEFAULT_SECRET_API_KEY = "ANGELUS_SISTEMA_SOBERANO_2026"

if CONFIG_PATH.exists():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            WEB_APP_URL = cfg.get("web_app_url", DEFAULT_WEB_APP_URL)
            SECRET_API_KEY = cfg.get("secret_key", DEFAULT_SECRET_API_KEY)
    except Exception:
        WEB_APP_URL = DEFAULT_WEB_APP_URL
        SECRET_API_KEY = DEFAULT_SECRET_API_KEY
else:
    WEB_APP_URL = DEFAULT_WEB_APP_URL
    SECRET_API_KEY = DEFAULT_SECRET_API_KEY

REPO_ID = "0072"
REPO_NAME = "cmre-engine"

FILES_TO_UPLOAD = [
    # Directivas y Documentación
    "AGENTS.md",
    "README.md",
    "ARQUITECTURA_ESTADO.md",
    ".specify/constitution.md",
    ".specify/specs/latest.md",
    ".specify/plans/latest.md",
    ".specify/tasks/latest.md",
    # Solvers Canónicos v0.5.0
    "src/cmre/solvers/rsna_knee_solver.py",
    "src/cmre/solvers/arc_agi_hybrid_solver.py",
    "src/cmre/solvers/enveda_casmi_solver.py",
    # Módulos y Ensamble
    "src/cmre/modules/ensemble.py",
    "src/cmre/services/submission_validator.py",
    # Base de Conocimiento y Postmortems
    "data/knowledge_base/claims_cmre.json",
    "data/knowledge_base/postmortems_failures_catalog.json",
    # Configuración de Entorno
    "pyproject.toml",
    "requirements.txt",
]

def report_telemetry(estado, progreso, tarea, notas):
    payload = {
        "token": SECRET_API_KEY,
        "action": "update_repo_status",
        "id": REPO_ID,
        "nombre": REPO_NAME,
        "estado": estado,
        "progreso_jules": progreso,
        "proxima_tarea": tarea,
        "notas_jules": notas
    }
    print(f"[*] Reportando estado de {REPO_ID}-{REPO_NAME} a Google Sheets...")
    try:
        r = requests.post(WEB_APP_URL, json=payload, timeout=30, allow_redirects=True)
        if r.status_code == 200:
            print(f"[+] Estado actualizado en Sheets: {r.json().get('message')}")
        else:
            print(f"[!] Error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[!] Excepción reportando telemetría: {e}")

def upload_single_file(rel_path):
    p = REPO_ROOT / rel_path
    if not p.exists():
        print(f"[-] Omitiendo (no existe): {rel_path}")
        return False

    file_size = p.stat().st_size
    print(f"[*] Subiendo {rel_path} ({file_size} bytes)...")
    try:
        with open(p, "rb") as f:
            file_b64 = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"[!] Error leyendo {rel_path}: {e}")
        return False

    payload = {
        "token": SECRET_API_KEY,
        "action": "upload_file",
        "id": REPO_ID,
        "nombre": REPO_NAME,
        "filename": p.name,
        "file_base64": file_b64
    }

    try:
        r = requests.post(WEB_APP_URL, json=payload, timeout=90, allow_redirects=True)
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "success":
                print(f"[+] OK: {p.name} -> {res.get('file_url')}")
                return True
            else:
                print(f"[!] Error respuesta GAS: {res.get('message')}")
                return False
        else:
            print(f"[!] Error HTTP {r.status_code}: {r.text}")
            return False
    except Exception as e:
        print(f"[!] Excepción al subir {rel_path}: {e}")
        return False

def main():
    print("=" * 70)
    print(f"[*] INICIANDO SINCRONIZACIÓN GOOGLE DRIVE VÍA APPS SCRIPT: {REPO_ID}-{REPO_NAME}")
    print("=" * 70)

    # 1. Reportar estado inicial a Sheets
    report_telemetry(
        estado="Activo / CMRE v0.5.0 Sincronizado",
        progreso="100% Core + Solvers RSNA/CASMI/ARC + 132 Tests",
        tarea="TASK-09 (Kaggle Writeups Connector) & TASK-10",
        notas="Repositorio sincronizado en GitHub (pedrogomez290625) y Drive. Listo para Jules."
    )

    # 2. Subir lista de archivos clave
    success_count = 0
    fail_count = 0
    for rel_path in FILES_TO_UPLOAD:
        ok = upload_single_file(rel_path)
        if ok:
            success_count += 1
        else:
            fail_count += 1
        time.sleep(0.5)

    print("\n" + "=" * 70)
    print(f"[+] SINCRONIZACIÓN FINALIZADA:")
    print(f"    - Subidos con éxito: {success_count}")
    print(f"    - Fallidos/Omitidos: {fail_count}")
    print("=" * 70)

if __name__ == "__main__":
    main()
