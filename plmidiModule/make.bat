@REM 切换至plmidiModule目录运行该批处理程序

@echo off

rd /s /q .\build

..\venv\Scripts\python.exe plmidi_setup.py build

rem 将*.pyd复制到venv目录下以使venv中的python能够使用
for /d /r "build" %%d in (lib.*) do (
    copy %%d\*.pyd ..\venv\Lib\site-packages
)