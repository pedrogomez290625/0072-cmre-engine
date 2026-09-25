"""
SYNC LOCAL REPO TO GOOGLE DRIVE GITHUB FOLDER
Sincroniza todos los archivos actualizados del repositorio local
a Google Drive para que Spark (o cualquier agente de Drive) pueda leerlos.
"""
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR = Path(__file__).resolve().parent.parent
DST_DIR = Path(r"G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\github\0072-cmre-engine")

EXCLUDE_PARTS = {'.git', '.venv', '__pycache__', '.pytest_cache'}

def sync_repo():
    if not DST_DIR.exists():
        DST_DIR.mkdir(parents=True, exist_ok=True)
    
    copied = 0
    updated = 0
    skipped = 0
    errors = 0
    
    print(f"Sincronizando desde:\n  {SRC_DIR}\nHacia:\n  {DST_DIR}\n")
    
    for p in SRC_DIR.rglob('*'):
        if any(part in p.parts for part in EXCLUDE_PARTS):
            continue
        
        rel = p.relative_to(SRC_DIR)
        target = DST_DIR / rel
        
        if p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        
        if p.is_file():
            should_copy = False
            if not target.exists():
                should_copy = True
                action = "CREADO"
                copied += 1
            else:
                # Comprobar si el origen es mas reciente o de diferente tamaño
                src_stat = p.stat()
                dst_stat = target.stat()
                if src_stat.st_mtime > dst_stat.st_mtime or src_stat.st_size != dst_stat.st_size:
                    should_copy = True
                    action = "ACTUALIZADO"
                    updated += 1
                else:
                    skipped += 1
            
            if should_copy:
                try:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, target)
                    print(f"[{action}] {rel}")
                except Exception as e:
                    print(f"[ERROR] {rel}: {e}")
                    errors += 1

    print("\n" + "=" * 50)
    print("📊 RESUMEN DE SINCRONIZACIÓN A GOOGLE DRIVE:")
    print(f"  • Archivos nuevos copiados:      {copied}")
    print(f"  • Archivos existentes renovados: {updated}")
    print(f"  • Archivos idénticos omitidos:   {skipped}")
    print(f"  • Errores:                       {errors}")
    print("=" * 50)

if __name__ == "__main__":
    sync_repo()
