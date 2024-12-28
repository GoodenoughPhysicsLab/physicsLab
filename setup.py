# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name="physicsLab",
    version="1.6.3",
    license="MIT",
    author="Arendelle",
    author_email="2381642961@qq.com",
    description="Python API for Quantum-Physics App",
    long_description="show description in [github](https://github.com/GoodenoughPhysicsLab/physicsLab)",
    long_description_content_type="text/markdown",
    url="https://github.com/GoodenoughPhysicsLab/physicsLab",
    packages=setuptools.find_packages(include=["physicsLab", "physicsLab.*"]),
    install_requires=["typing-extensions", "requests", "colorama"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
