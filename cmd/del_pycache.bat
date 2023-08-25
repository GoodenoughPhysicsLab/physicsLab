@REM ./cmd/del_pycache
@echo off
for /d /r "physicsLab" %%d in (__pycache__) do (
    if exist "%%d" (
@REM    echo Deleting %%d
        rd /s /q "%%d"
    )
)