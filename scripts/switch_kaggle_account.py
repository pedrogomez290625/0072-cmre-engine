"""Kaggle Multi-Account Switcher & Vault Manager.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
Fecha: Septiembre de 2026
Ecosistema: 0072-cmre-engine

Allows switching seamlessly between Kaggle accounts (e.g. Sandbox/Testing vs Official Competition).
"""

import json
import shutil
import sys
from pathlib import Path

KAGGLE_DIR = Path.home() / ".kaggle"
ACTIVE_JSON = KAGGLE_DIR / "kaggle.json"


def get_account_username(filepath: Path) -> str:
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
        return data.get("username", "unknown")
    except Exception:
        return "error_reading"


def list_accounts() -> None:
    if not KAGGLE_DIR.exists():
        print(f"[ERROR] Directory {KAGGLE_DIR} does not exist.")
        return

    active_user = get_account_username(ACTIVE_JSON) if ACTIVE_JSON.exists() else "None"
    print(f"\n=== KAGGLE MULTI-ACCOUNT VAULT ===")
    print(f"Directory: {KAGGLE_DIR}")
    print(f"Active Account: [ {active_user} ]\n")

    files = list(KAGGLE_DIR.glob("kaggle*.json"))
    for f in sorted(files):
        user = get_account_username(f)
        marker = "-> [ACTIVE]" if f.name == "kaggle.json" else "  [STORED]"
        print(f"  {marker} {f.name:35} (username: {user})")
    print()


def switch_account(target_name: str) -> None:
    if not KAGGLE_DIR.exists():
        print(f"[ERROR] Directory {KAGGLE_DIR} does not exist.")
        return

    # Find matching file
    candidates = []
    for f in KAGGLE_DIR.glob("kaggle*.json"):
        if f.name == "kaggle.json":
            continue
        if target_name.lower() in f.name.lower() or target_name.lower() in get_account_username(f).lower():
            candidates.append(f)

    if not candidates:
        print(f"[ERROR] No stored account matched '{target_name}'.")
        list_accounts()
        return

    selected = candidates[0]
    username = get_account_username(selected)

    # Safe swap
    shutil.copyfile(selected, ACTIVE_JSON)
    print(f"[SUCCESS] Switched active Kaggle account to: {username} (from {selected.name})")


def import_new_token(source_path: str, label: str) -> None:
    src = Path(source_path)
    if not src.exists():
        print(f"[ERROR] Source file {src} not found.")
        return

    username = get_account_username(src)
    dest_name = f"kaggle_{username}_{label}.json" if label else f"kaggle_{username}.json"
    dest = KAGGLE_DIR / dest_name

    shutil.copyfile(src, dest)
    shutil.copyfile(src, ACTIVE_JSON)
    print(f"[SUCCESS] Imported new token for '{username}' as '{dest.name}' and set as ACTIVE.")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("list", "-l", "--list"):
        list_accounts()
        return

    cmd = sys.argv[1].lower()
    if cmd in ("switch", "-s", "--switch"):
        if len(sys.argv) < 3:
            print("Usage: python switch_kaggle_account.py switch <name_or_username>")
            return
        switch_account(sys.argv[2])
    elif cmd in ("import", "-i", "--import"):
        if len(sys.argv) < 3:
            print("Usage: python switch_kaggle_account.py import <path_to_kaggle.json> [label]")
            return
        label = sys.argv[3] if len(sys.argv) > 3 else ""
        import_new_token(sys.argv[2], label)
    else:
        # Direct target name passed
        switch_account(sys.argv[1])


if __name__ == "__main__":
    main()
