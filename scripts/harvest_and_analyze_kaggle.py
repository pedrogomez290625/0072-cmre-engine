"""Industrial Kaggle Harvester and Forensic Intelligence Pipeline.

Systematic workflow to harvest, dissect, and synthesize competitor notebooks
for any Kaggle competition.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
sys.stdout.reconfigure(encoding="utf-8")

from cmre.connectors.kaggle import KaggleConnector
from cmre.services.notebook_analyzer import NotebookAnalyzer

GDRIVE_BASE = Path(r"G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\investigaciones")


def run_pipeline(
    competition_slug: str,
    top_n: int = 10,
    output_dir: Path | None = None,
    sync_drive: bool = True,
    account: str = "oficial"
) -> Path:
    """Execute complete harvest and forensic analysis pipeline."""
    if output_dir is None:
        output_dir = Path(f"investigaciones/{competition_slug}_notebooks")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n==================================================================")
    print(f"🚀 CMRE HARVEST & FORENSIC PIPELINE: {competition_slug}")
    print(f"==================================================================")

    # 1. Conectar y Cosechar
    print(f"\n[1/3] Cosechando Top {top_n} notebooks ordenados por score...")
    connector = KaggleConnector(account_type=account)
    kernels = connector.list_top_kernels(competition_slug, sort_by="scoreDescending", page_size=top_n)

    downloaded_files = []
    for k in kernels:
        ref = k["ref"]
        slug = k["slug"]
        sub_dir = output_dir / slug
        print(f"  ⬇ Descargando [{ref}]...")
        saved_file = connector.download_kernel(ref, sub_dir)
        if saved_file:
            downloaded_files.append(saved_file)
            print(f"    ✓ {saved_file.name} guardado.")

    # 2. Análisis Forense
    print(f"\n[2/3] Ejecutando análisis forense de AST y estrategias sobre {len(downloaded_files)} cuadernos...")
    analyzer = NotebookAnalyzer(downloaded_files)
    batch_results = analyzer.run_batch_analysis()

    # Guardar resultados JSON
    json_path = output_dir / "MATRIZ_CONSENSO_SOTA.json"
    json_path.write_text(json.dumps(batch_results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  ✓ Matriz JSON generada en {json_path}")

    # Guardar Dossier Markdown
    dossier_md = analyzer.generate_dossier_markdown(competition_slug)
    md_path = output_dir / f"DOSSIER_FORENSE_{competition_slug.upper().replace('-', '_')}.md"
    md_path.write_text(dossier_md, encoding="utf-8")
    print(f"  ✓ Dossier Markdown generado en {md_path}")

    # 3. Sincronización con Google Drive
    if sync_drive and GDRIVE_BASE.exists():
        print(f"\n[3/3] Sincronizando con Google Drive ({GDRIVE_BASE})...")
        drive_dest = GDRIVE_BASE / f"{competition_slug}_notebooks"
        drive_dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(json_path, drive_dest / json_path.name)
        shutil.copy2(md_path, drive_dest / md_path.name)
        for f in downloaded_files:
            target = drive_dest / f.parent.name / f.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
        print(f"  ✓ Sincronización completa en Google Drive: {drive_dest}")

    print(f"\n🎉 ¡Pipeline finalizado con éxito para {competition_slug}!")
    return md_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CMRE Industrial Notebook Harvester & Forensic Analyzer.")
    parser.add_argument("--competition", "-c", required=True, help="Competition slug (e.g. enveda-CASMI26-molecule-id-mass-spectra)")
    parser.add_argument("--top", "-n", type=int, default=10, help="Number of notebooks to harvest.")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Local output directory.")
    parser.add_argument("--no-drive", action="store_true", help="Disable Google Drive synchronization.")
    parser.add_argument("--account", choices=["oficial", "pedro"], default="oficial", help="Account credentials to use.")

    args = parser.parse_args()
    run_pipeline(
        competition_slug=args.competition,
        top_n=args.top,
        output_dir=args.output,
        sync_drive=not args.no_drive,
        account=args.account
    )
