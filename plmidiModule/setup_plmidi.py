#encoding=utf-8
import setuptools

setuptools.setup(
    ext_modules=[
        setuptools.Extension(
            "plmidi",
            sources=["./midi_sound.c"]
        )
    ]
)
