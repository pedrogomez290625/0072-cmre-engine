import subprocess
import sys

bat_path = r"C:\Users\rafae\.gemini\01_PROYECTOS\0072-cmre-engine\scripts\run_daily_task.bat"

for num, t in [(1, "02:30"), (2, "03:30"), (3, "04:30")]:
    tr_value = f'"{bat_path}" {num}'
    cmd = [
        "schtasks", "/Create",
        "/SC", "DAILY",
        "/TN", f"Jules_Victoria_CMRE_Task_{num}",
        "/TR", tr_value,
        "/ST", t,
        "/F"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Task {num} ({t}): returncode={res.returncode}")
    if res.stdout:
        print("  out:", res.stdout.strip())
    if res.stderr:
        print("  err:", res.stderr.strip())
