@echo off
set TASK_ID=%1
if "%TASK_ID%"=="" set TASK_ID=1
"C:\Python313\python.exe" "C:\Users\rafae\.gemini\01_PROYECTOS\0072-cmre-engine\scripts\jules_victoria_daily_scheduler.py" --dispatch %TASK_ID% >> "C:\Users\rafae\.gemini\01_PROYECTOS\0072-cmre-engine\reports\jules_scheduler.log" 2>&1
