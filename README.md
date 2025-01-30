# physicsLab

![输入图片说明](./cover.jpg)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![build](https://github.com/gaogaotiantian/viztracer/workflows/build/badge.svg)](https://github.com/GoodenoughPhysicsLab/physicsLab/actions)
<!-- ![support-version](https://img.shields.io/pypi/pyversions/viztracer) 支持3.8及以上版本 -->

## 介绍
当我们在[物理实验室AR](https://www.turtlesim.com/)纯手动做实验的时候，往往会遇到一些琐碎、麻烦但又不得不做的事情，比如：重复的搭建某些电路，调整元件的位置，电路内部结构的重复。这些问题都可以通过使用`physicsLab`生成这些电路结构来轻易解决！于是我写了`physicsLab`，让你能用`Python`在物实做实验。

而在参与物实社区的时候, 有时候又会遇到一些手动很麻烦的情况, 我们就可以使用`physicsLab.web`来通过网络api操作物实社区。

## 部分方便且惊艳的功能展示
*  同时支持通过存档的文件名与**存档名**访问存档
*  不受实验室大小地随意摆放元件 (比如在实验室外悬空的元件)
*  将midi转换为物实对应的电路
*  修改物实的实验封面
*  获取用户的所有头像或实验用过的所有封面

更多好用的功能等你来发现

## 功能支持
* 跨平台支持，只要`Python3.8+`能在该平台上运行并且能够读写文件，比如`Windows7+`, `Linux`, `MacOS`, `Android`
* 支持物实**所有**实验类型：电学，天体物理，电与磁
* 支持物实**全部**元件
* 大多数物实网络api封装的支持 (直接与物实服务器进行交互)

## 稳定&兼容
自版本`2.0.0`及之后, `physicsLab`会逐步增加兼容的考虑与支持

但这并不意味着无意义的兼容。通常来说，会采用标注弃用, 并推荐转移到新api的模式。
* v2.0.0: `class Experiment, ExperimentOpenedError, ExperimentClosedError, ExperimentExistError, ExperimentNotExistError`实验性地加入`stable`支持
* v2.0.1: 三大实验所有元件的类名实验性地加入`stable`支持

## 版本发布
`physicsLab`的版本发布采取快照的方式, `physicsLab`仅会维护`trunk`

## 安装教程
1.  请确保你的电脑有[Python](https://www.python.org)（>=3.8）与[物理实验室AR](https://www.turtlesim.com/)（简称`物实`）（也可以联系物理实验室的开发者[John-Chen](https://gitee.com/civitasjohn)）

2.  在cmd或shell输入以下载physicsLab：
```shell
pip install physicsLab
```
在某些非正常情况，你可能无法顺利使用`pip`，此时你可以换为该命令来解决该问题：
```shell
python -m pip install physicsLab
```
> Note: 在`Windows`下你可以输入`py`来使用`Python`，`Linux, MacOS`下可能需要输入`python3`或者`python3.x`（`python`加上你的`Python`版本）来使用`python`

3.  有一个并非必需的功能：播放midi（仅在Windows下可用）。你可以输入下面命令的任意一条：
```shell
pip install plmidi
pip install pygame
```
点击跳转至[plmidi](https://github.com/GoodenoughPhysicsLab/plmidi)

4.  物实存档使用了中文字符，默认编码为`utf-8`。但在一些非正常情况，存档的编码可能被改变。虽然`physicsLab`有一定的处理存档编码问题的能力，但如果还是出现了问题，请输入该命令：
```bash
pip install chardet
```
此时`physicsLab`会自动调用`chardet`来处理更加棘手的文件编码问题。

5.  如果下载成功，就可以查看[快速开始](docs/quick_start.md)，开始你的使用了
> Note: 每次通过`physicsLab`生成了一个新的存档之后，都需要重新加载物实的本地存档，即点击`从本地读取`，再次点击进入对应存档

### 新手解惑: 为什么我明明安装了physicsLab, python却告诉我无法找到？
`pip`安装的包会被放在`site-packages`文件夹下  
这大概率是因为pip安装的包所对应的`site-packages`与你使用的`Python`对应的`site-packages`不一样导致的  
解决方案：找到ide调用的`python`对应的`site-packages`，然后把`physicsLab`与`physicsLab.egg-info`复制过去  
同时我推荐去学一下`Python`的虚拟环境`venv`，有效解决此问题  

如果此方法失效了，虽然这一定不是这个方法的问题，但你还可以在python的开头写上这两行代码来解决这个问题：  
```python
import sys
sys.path.append("/your/path/of/physicsLab") # 将字符串替换为你想添加的路径
```
这个方法很丑陋但很简单好用，可以帮你快速解决问题，毕竟能跑起来就很不错了  
其原理是`Python`会在`sys.path`这个列表里面的路径去寻找`Python Package`，若未找到则会报错。因此该方法的原理就是把`Python`找不到的路径加进去，`Python`就找到了  
注：每次运行的时候的`sys.path`都是临时的，因此该方法必须让`Python`在每次运行的时候都执行一遍  

## 特殊说明事项
* 如果`physicsLab`抛出`AssertionError`，请**报告 bug** (请在issue中附上最小复现)

* 目前`physicsLab`在`windows`上的支持最好，在其他操作系统上仅支持手动导入/导出存档（默认在`physicsLabSav`文件夹中）。

* 在安卓上要使用`physicsLab`的话，可以通过`qpython`或者`Termux`(推荐) 进行使用
  * 在`qpython v3.2.5`中大大削减了python在文件路径操作方面的权限，这意味着在qpython上使用physicsLab生成的存档将很难被物实导入，因为物实没权限访问不了， 但此问题在[qpython v3.2.3](https://github.com/qpython-android/qpython/releases/tag/v3.2.3)中不存在，推荐下载该版本。
  * `Termux`的话，需要设置输出存档的路径到`/storage/emulated/0/` (不同安卓设备路径可能不同), 或者手动`mv`一下生成的存档，这样才能让物实访问对应的存档。
  * 不过由于安卓权限的问题，用起来肯定没有电脑上方便。

* 由于`physicsLab`使用中文注释而且物实的存档也使用了中文，因此我建议你手动在`Python`代码的第一行添加如下注释:
```Python
# -*- coding: utf-8 -*-
```
不过由于编码导致问题的情况似乎很少

## 优点
*  `physicsLab`拥有优秀的与物实存档交互的能力，你甚至可以使用程序完成部分工作之后你再继续完成或者让程序在你已完成的实验的基础上继续完成。
  如此灵活的功能使得`physicsLab`即使是在`Python`的`shell`上也能出色的完成工作！
*  `physicsLab`为纯`Python`库，其c拓展部分(播放midi的部分)被放到了`plmidi`中，但`plmidi`不是必须需要的。纯`Python`库通常意味着更容易使用，更少的问题。
*  封装了物实里的大量元件，即使是***未解锁的元件***也可以轻易用脚本生成，甚至一些常用的电路也被封装好了！
*  物理实验室存档的位置有点隐蔽，但用该脚本生成实验时，你无须亲自寻找这个文件在哪里。
*  外部依赖少
*  相比于手动做实验，代码复用率更高，许多逻辑电路已经被封装，只需简单的一行调用即可生成。
*  程序有利于大型实验的创作
*  改存档做出来的实验往往有十分惊艳的效果！

## 其他
* 一些零七八碎的内容: [other physicsLab](https://gitee.com/script2000/temporary-warehouse/tree/master/other%20physicsLab)
* 主仓库(github): https://github.com/GoodenoughPhysicsLab/physicsLab
* 备份仓库(gitee): https://gitee.com/script2000/physicsLab

## contribute
`physicsLab`没有强行要求代码风格，但需要注意与上下文保持一致

你可以从更新文档、bugfix、写[测试代码](./test_pl)开始入手
