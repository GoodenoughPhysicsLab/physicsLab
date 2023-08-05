#encoding=utf-8
import setuptools

long_description = None
with open("./README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="plmidi",
    version="0.0",
    author="Goodenough",
    author_email="2381642961@qq.com",
    description="midi player for Python Package physicsLab",
    long_description=long_description,
    url="https://gitee.com/script2000/physicsLab",
    license="MIT",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
    ],
    ext_modules=[
        setuptools.Extension(
            "plmidi",
            sources=["./plmidi_setup.c"]
        )
    ]
)
