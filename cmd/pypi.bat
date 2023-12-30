rd /s /q .\build
rd /s /q .\dist
rd /s /q .\physicsLab.egg-info

py setup.py sdist bdist_wheel
twine upload dist/*