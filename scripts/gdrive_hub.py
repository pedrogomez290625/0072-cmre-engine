#!/usr/bin/env python3
"""
🛰️ ANGELUS GDRIVE & TELEMETRY CLIENT - REPO 0072 (COMPETITIVE ML REASONING ENGINE - CMRE)
Permite a Jules, Angelus y agentes reportar telemetría a Google Sheets y sincronizar artefactos en Google Drive vía Apps Script.
Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import sys
import os
import json
import base64
import argparse
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
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

def report_status(estado=None, progreso=None, tarea=None, notas=None):
    payload = {
        "token": SECRET_API_KEY,
        "action": "update_repo_status",
        "id": REPO_ID,
        "nombre": REPO_NAME
    }
    if estado: payload["estado"] = estado
    if progreso: payload["progreso_jules"] = progreso
    if tarea: payload["proxima_tarea"] = tarea
    if notas: payload["notas_jules"] = notas

    print(f"[*] Enviando telemetría de {REPO_ID}-{REPO_NAME} a Google Sheets...")
    try:
        r = requests.post(WEB_APP_URL, json=payload, timeout=30, allow_redirects=True)
        if r.status_code == 200:
            print(f"[+] Éxito: {r.json().get('message', 'Telemetría enviada')}")
        else:
            print(f"[!] Error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[!] Error de conexión: {e}")

def upload_file_to_drive(file_path_str):
    p = Path(file_path_str)
    if not p.is_absolute():
        p = REPO_ROOT / p

    if not p.exists():
        print(f"[!] Error: El archivo {p} no existe.")
        return False

    file_size = p.stat().st_size
    print(f"[*] Codificando archivo {p.name} ({file_size} bytes)...")
    try:
        with open(p, "rb") as f:
            file_b64 = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"[!] Error leyendo {p}: {e}")
        return False

    payload = {
        "token": SECRET_API_KEY,
        "action": "upload_file",
        "id": REPO_ID,
        "nombre": REPO_NAME,
        "filename": p.name,
        "file_base64": file_b64
    }

    print(f"[*] Subiendo {p.name} a Google Drive (vía Apps Script) para {REPO_ID}-{REPO_NAME}...")
    try:
        r = requests.post(WEB_APP_URL, json=payload, timeout=90, allow_redirects=True)
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "success":
                print(f"[+] ¡Archivo subido exitosamente a Google Drive!")
                print(f"    - Nombre: {res.get('file_name')}")
                print(f"    - URL:    {res.get('file_url')}")
                return True
            else:
                print(f"[!] Error en respuesta GAS: {res.get('message')}")
                return False
        else:
            print(f"[!] Error HTTP {r.status_code}: {r.text}")
            return False
    except Exception as e:
        print(f"[!] Error enviando a Drive: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Hub de Google Drive y Telemetría para Jules/Angelus")
    subparsers = parser.add_subparsers(dest="cmd")

    status_parser = subparsers.add_parser("report", help="Reportar estado del repo a Sheets")
    status_parser.add_argument("--estado", type=str, help="Estado general (Activo, En progreso, Completado)")
    status_parser.add_argument("--progreso", type=str, help="Porcentaje o descripción del progreso")
    status_parser.add_argument("--tarea", type=str, help="Próxima tarea a ejecutar por Jules")
    status_parser.add_argument("--notas", type=str, help="Observaciones o notas")

    upload_parser = subparsers.add_parser("upload", help="Subir archivo a Google Drive")
    upload_parser.add_argument("file", type=str, help="Ruta al archivo a subir")

    args = parser.parse_args()

    if args.cmd == "report":
        report_status(args.estado, args.progreso, args.tarea, args.notas)
    elif args.cmd == "upload":
        upload_file_to_drive(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
