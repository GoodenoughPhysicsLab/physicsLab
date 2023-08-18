del /s /q .\build
del /s /q .\dist
del /s /q .\plmidi.egg-info

py plmidi_setup.py sdist bdist_wheel
twine upload dist/*