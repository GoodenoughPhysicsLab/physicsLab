# physicsLab 物实程序化

[English](./README.md)

![输入图片说明](./cover.jpg)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![build](https://github.com/gaogaotiantian/viztracer/workflows/build/badge.svg)](https://github.com/GoodenoughPhysicsLab/physicsLab/actions)
![support-version](https://img.shields.io/pypi/pyversions/viztracer)

## 介绍
在物理实验室做实验的时候，我们可能会苦恼于元件不够整齐，需要重复的搭建某些电路且重复地做测试，或元件无法浮空等问题。这些问题都可以通过改存档来轻易解决！然而，手动改存档操作麻烦且出错率高。于是我写了`physicsLab`，并在其中封装了一些常用功能，让你用`Python`也能够轻易地在物实做实验，而且***你甚至不需用知道存档在电脑的哪里！***

## 安装教程

1.  请确保你的电脑有[Python](https://www.python.org)（大于等于3.8）与[物理实验室PC版](https://www.turtlesim.com/)（简称`物实`）（也可以联系[开发者Jone-Chen](https://gitee.com/civitasjohn)）

2.  在cmd或shell输入以下载physicsLab：
```shell
pip install physicsLab
```
在某些非正常情况，你可能无法顺利使用`pip`，此时你可以换为该命令来解决该问题：
```shell
python -m pip install physicsLab
```
在`Windows`下，该命令等价于:
```shell
py -m pip install physicsLab
```

3.  有一个并非必需的功能：播放midi。你可以输入下面命令的任意一条：
```shell
pip install plmidi
pip install pygame
```
点击跳转至[plmidi](https://github.com/GoodenoughPhysicsLab/plmidi)  

之所以没有做安装physicsLab的时候自动安装这两个库，是因为安卓的`qpython`在下载含c的库的时候存在问题  

4.  物实存档使用了中文字符，默认编码为`utf-8`。但在一些非正常情况，存档的编码可能被改变。虽然`physicsLab`有一定的处理存档编码问题的能力，但如果还是出现了问题，请输入该命令：  
```bash
pip install chardet
```
此时`physicsLab`会自动调用`chardet`来处理更加棘手的文件编码问题。  

5. 如果下载成功，请输入下面的代码以验证`physicsLab`已经可以使用了  
```Python
from physicsLab import *

with experiment("example"):
    Logic_Input(0, 0, 0.1)
```
然后打开物实，点击`从本地读取`，点击一个名为`example`的实验。如果出现了一个悬空的逻辑输入，则说明一切都成功了。
> Note:  每次运行`physicsLab`后都需要重新加载物实的本地存档，即点击`从本地读取`，再次点击对应存档，使物实重新加载该存档

## 搭建开发环境
切换至physicsLab根目录，输入以下指令 (仅限于`Windows`):
```
.\cmd\setup_project.bat
```

## 新手解惑: 为什么我明明安装了physicsLab, python却告诉我无法找到？
pip安装的包会被放在`site-package`文件夹下  
这大概率是因为pip安装的包所对应的`site-package`与你使用的`python`对应的`site-package`不一样导致的  
解决方案：找到ide调用的`python`对应的`site-package`，然后把`physicsLab`与`physicsLab.egg-info`复制过去  
同时我推荐去学一下`python`的虚拟环境`venv`，有效解决此问题  
  
如果此方法失效了，虽然这一定不是这个方法的问题，但你还可以在python的开头写上这两行代码来解决这个问题：  
```python
import sys
sys.path.append("/your/path/of/physicsLab") # 将字符串替换为你想添加的路径
```
这个方法很丑陋但很简单好用，可以帮你快速解决问题，毕竟能跑起来就很不错了   
其原理是python会在sys.path这个列表里面的路径去寻找python package，若未找到则会报错。因此该方法的原理就是把python找不到的路径加进去，python就找到了   
注：每次运行的时候加入的path都是临时的，因此该方法必须让python在每次运行的时候都执行一遍   


## 已经测试过的环境
* windows: python 3.8, 3.9, 3.10, 3.11, 3.12  
* Android: qpython(app) 3.11.4  

## 使用说明
*目前`physicsLab`在`windows`上的支持最好，在`Android`上仅支持手动导入/导出存档（默认在`physicsLabSav`文件夹中）。*  
其他操作系统上的行为与在`Android`上应该一致，但未经过测试。  

> 在`qpython v3.2.5`中大大削减了python在文件路径操作方面的权限，这意味着在qpython上使用physicsLab生成的存档将很难被物实导入，因为物实没权限访问不了。
> 但此问题在[qpython v3.2.3](https://github.com/qpython-android/qpython/releases/tag/v3.2.3)中不存在，推荐下载该版本。
> 不过由于安卓权限的问题，用起来肯定没有电脑上方便。

下面给出一个简单的例子（该例子仅用于讲解，你大概率无法运行）：
```Python
from physicsLab import *

  # 打开存档
  # 也支持输入存档的文件名（也就是xxx.sav）
e = Experiment("example")
  # 如果你希望程序不覆盖掉存档中已有的实验状态，需要这样写
e.read()
  # 创建一个逻辑输入，坐标为(0, 0, 0.1)
Logic_Input(0, 0, 0.1)
  # 你也可以不写坐标，默认是(0,0,0)
o = Or_Gate()
  # 元件含有引脚属性，是对物实原始的引脚表示方法的封装
  # 比如或门（Or_Gate），含有 i_up, i_low, o三个引脚属性
  # 通过引脚属性，就可以更方便的连接导线了

  # crt_Wire()函数用来连接导线，有三个参数：SourcePin, TargetPin, color
  # SourcePin与TargetPin必须传入元件的引脚
  # color可以不写，默认为蓝色
crt_Wire(o.i_up, o.i_low)
  # 将程序中生成的原件，导线等等写入存档
e.write()
  # 然后用物实打开存档见证奇迹
```

`physicsLab`还支持等价但更优雅的方式 (这也是我最推荐的方式):
```python
from physicsLab import *

with experiment("example", read=True):
    Logic_Input(0, 0, 0.1)
    o = Or_Gate()
    o.i_up - o.i_low # 连接导线
```
上面两段代码产生的结果是一样的  
  
更详细的内容请在[文档](docs)中查看  

由于`physicsLab`使用中文注释而且物实的存档也使用了中文  
因此我建议你手动在`Python`代码的第一行添加如下注释:
```Python
# -*- coding: utf-8 -*-
```  
不过由于编码导致问题的情况似乎很少

## 优点
1.  `physicsLab`拥有优秀的与物实存档交互的能力，你甚至可以使用程序完成部分工作之后你再继续完成或者让程序在你已完成的实验的基础上继续完成。  
  如此灵活的功能使得physicsLab即使是在python shell上也能出色的完成工作！
2.  `physicsLab`为纯python库，其c拓展部分(主要是midi相关的)被放到了`plmidi`中，但`plmidi`不是必须需要的。纯Python库通常意味着更容易使用，更少的问题。
3.  封装了物实里的大量原件，即使是***未解锁的原件***也可以轻易用脚本生成，甚至一些常用的电路也被封装好了！
4.  物理实验室存档的位置有点隐蔽，但用该脚本生成实验时，你无须亲自寻找这个文件在哪里。
5.  绝大多数调用的库皆为Python的内置库，唯一的外置库为`mido`，但没有mido带来的影响仅仅是`physicsLab.music`无法使用罢了。
6.  相比于手动做实验，代码复用率更高，许多逻辑电路已经被封装，只需简单的一行调用即可生成。
7.  程序有利于大型实验的创作
8.  最重要的一点：改存档做出来的实验往往有十分惊艳的效果！

## 不足
1. 在物理实验室连接导线只需要点击两下，但用程序连接导线相对麻烦一些。
2. 在物理实验室选择原件只需要点击一下，但用程序选择原件相对麻烦一些。
3. 作者在接下来一段时间内将因为学业难以维护该仓库，但这并不代表弃坑。

## 其他
* 更多内容请在 [other physicsLab](https://gitee.com/script2000/temporary-warehouse/tree/master/other%20physicsLab) 中查看
* github: https://github.com/GoodenoughPhysicsLab/physicsLab
* gitee: https://gitee.com/script2000/physicsLab

## contribute
`physicsLab`没有强行要求代码风格，但需要注意与上下文保持一致  

你可以从更新文档、bugfix、写[测试代码](test_physicsLab.py)开始入手
