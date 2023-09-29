@REM 删除旧的build
rd /s /q .\build
@REM 注释：运行该批处理文件必须在plmidiMoudule文件夹下
py plmidi_setup.py build
@REM 将.pyd复制到venv以便于测试
copy  .\build\lib.win-amd64-3.8\*.pyd  ..\venv\Lib\site-packages