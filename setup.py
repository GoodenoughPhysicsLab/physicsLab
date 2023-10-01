#coding=utf-8
import setuptools  # 导入setuptools打包工具

with open("./README_zh.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="physicsLab",
    version="1.3.5",  # 包版本号，便于维护版本
    license="MIT",
    author="Goodenough",  # 作者，可以写自己的姓名
    author_email="2381642961@qq.com",  # 作者联系方式，可写自己的邮箱地址
    description="Doing experiments in the physics lab AR by python",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://gitee.com/script2000/physicsLab",  # 项目地址
    packages=setuptools.find_packages(),
    install_requires=["mido"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'  # 对python的最低版本要求
)
