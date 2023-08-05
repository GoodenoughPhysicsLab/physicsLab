del /s /q .\build
del /s /q .\dist
del /s /q .\physicsLab.egg-info

py setup.py sdist bdist_wheel
twine upload dist/*