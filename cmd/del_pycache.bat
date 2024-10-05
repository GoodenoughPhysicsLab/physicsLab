@echo off
for /d /r "physicsLab" %%d in (__pycache__) do (
    if exist "%%d" (
        echo Deleting %%d
        rd /s /q "%%d"
    )
)