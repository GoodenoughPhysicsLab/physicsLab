@REM 删除旧的build
del /s /q .\build
@REM 注释：运行该批处理文件必须在plmidiMoudule文件夹下
py plmidi_setup.py build
@REM 你可能无法在你的电脑上正确运行该批处理文件，即将.pyd复制到venv，目的是便于测试
copy  .\build\lib.win-amd64-3.7\plmidi.cp37-win_amd64.pyd  ..\venv\Lib\site-packages