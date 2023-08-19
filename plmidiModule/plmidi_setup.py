#encoding=utf-8
import setuptools

long_description = None
with open("./README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="plmidi",
    version="1.0.2",
    author="Goodenough",
    author_email="2381642961@qq.com",
    description="midi player for Python Package physicsLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/script2000/physicsLab",
    license="MIT",
    packages=setuptools.find_packages(),
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
            sources=[
                "./plmidi_sound.c"
            ]
        )
    ]
)
