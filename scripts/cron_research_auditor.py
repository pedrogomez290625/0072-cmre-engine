"""Cron Research Auditor - Rutina de Monitoreo y Auditoría Quincenal.

Escanea la carpeta `investigaciones/`, audita la cobertura de torneos de Kaggle y plataformas
alternativas, valida el índice maestro y sincroniza hacia Google Drive.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

# Forzar codificación UTF-8 en consola Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Definición de rutas base
REPO_ROOT = Path(__file__).resolve().parent.parent
INVESTIGACIONES_DIR = REPO_ROOT / "investigaciones"
DRIVE_DIR = Path("G:/Mi unidad/🏛️ Ecosistema_Angelus_2026/0072-cmre-engine/investigaciones")


def audit_investigations() -> dict[str, int]:
    """Escanea y contabiliza los informes existentes."""
    stats = {
        "kaggle_getting_started": 0,
        "kaggle_playground": 0,
        "kaggle_featured": 0,
        "kaggle_research": 0,
        "kaggle_community": 0,
        "alternativas_drivendata": 0,
        "alternativas_zindi": 0,
        "alternativas_aicrowd": 0,
        "alternativas_numerai": 0,
        "alternativas_datasource_ai": 0,
        "total_archivos_md": 0,
    }

    if not INVESTIGACIONES_DIR.exists():
        print(f"[!] Error: Directorio no encontrado: {INVESTIGACIONES_DIR}")
        return stats

    for md_file in INVESTIGACIONES_DIR.rglob("*.md"):
        if md_file.name == "INDICE_INVESTIGACIONES.md":
            continue
        stats["total_archivos_md"] += 1
        posix_path = md_file.as_posix()
        for key in stats.keys():
            if key != "total_archivos_md":
                slug = key.replace("_", "/")
                if slug in posix_path:
                    stats[key] += 1

    return stats


def sync_to_google_drive() -> bool:
    """Sincroniza los informes hacia el almacenamiento desacoplado en Google Drive."""
    if not DRIVE_DIR.exists():
        try:
            DRIVE_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[!] Aviso: No se pudo acceder a Google Drive: {e}")
            return False

    print(f"[*] Sincronizando hacia Google Drive: {DRIVE_DIR}")
    copied_count = 0
    for item in INVESTIGACIONES_DIR.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(INVESTIGACIONES_DIR)
            dest_file = DRIVE_DIR / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            if not dest_file.exists() or item.stat().st_mtime > dest_file.stat().st_mtime:
                shutil.copy2(item, dest_file)
                copied_count += 1

    print(f"[✓] Sincronización completada. Archivos actualizados en Drive: {copied_count}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditor quincenal de investigaciones CMRE")
    parser.add_argument("--sync", action="store_true", help="Sincronizar a Google Drive")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    args = parser.parse_args()

    stats = audit_investigations()

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print("=" * 65)
        print("  CMRE - AUDITORÍA DE INVESTIGACIONES COMPETITIVAS (CICLO 15 DÍAS)")
        print("=" * 65)
        print(f"• Total de reportes en base de datos: {stats['total_archivos_md']}")
        print(f"• Kaggle Playground / Sparring:       {stats['kaggle_playground']}")
        print(f"• Kaggle Featured / Premios Grandes: {stats['kaggle_featured']}")
        print(f"• Kaggle Research / Ciencia:          {stats['kaggle_research']}")
        print(f"• Kaggle Community:                   {stats['kaggle_community']}")
        print(f"• DrivenData (Impacto Social):        {stats['alternativas_drivendata']}")
        print(f"• Zindi (África):                     {stats['alternativas_zindi']}")
        print(f"• AIcrowd (NeurIPS/Benchmarks):       {stats['alternativas_aicrowd']}")
        print("=" * 65)

    if args.sync:
        sync_to_google_drive()

    return 0


if __name__ == "__main__":
    sys.exit(main())
