rd /s /q .\build
rd /s /q .\dist
rd /s /q .\plmidi.egg-info

py plmidi_setup.py sdist bdist_wheel
twine upload dist/*