# 物实程序化

#### 介绍
通过一些命令对物理实验室存档进行操作

#### 安装教程

1.  请确保你的电脑有[Python](https://www.python.org)与[物理实验室PC版](https://www.turtlesim.com/)（也可以联系[开发者Jone-Chen](https://gitee.com/civitasjohn)）
2.  打开Code文件夹中的physicsLab.py，复制或下载到本地
3.  如果你的ide无法找到physicsLab,py，你需要在代码开头写  
```python
import sys
sys.path.append('(path of physicsLab.py)')
```

#### 使用说明

```python
 # 打开存档  
open_Experiment("在物实保存的存档的名字")
 # 例：open_Experiment('测逝')  
 # 也支持输入存档的文件名（也就是xxx.sav）
 # 如果你希望程序不覆盖掉存档中已有的实验状态，需要这样写  
read_Experiment()  
 # 创建一个逻辑输入，坐标为(0, 0, 0.1)  
Logic_Input(0, 0, 0.1)   
 # 你也可以不写坐标，默认是(0,0,0)，请注意2原件的坐标不允许重叠！  
o = Or_Gate() # 此时o存储的是orGate的self  
 # crt_wire输入格式：  
 #    crt_wire(SourcePin, TargetPin, color = "蓝")  
crt_wire(o.i_up, o.i_low)  
 # 将程序中生成的原件，导线等等写入存档  
write_Experiment()  
 # 然后打开存档见证奇迹  
 # （更详细的内容请在Code文件夹中查看，同时我也贴上来了一些测试代码作为示例代码）
```
#### 优点
1. 通过read_Experiment()，你无须把所有工作交给代码。因为用代码写并不总是意味着方便（比如连接导线）。  
你现在可以手动连接部分导线，并通过保存的形式，让程序在下次也可以轻松读取。  
这也意味着你不用一口气把控制整个电路的脚本写出来，而是每次写一部分，并把更适合代码的工作交给代码完成。  
也就是说，写这个脚本的感觉更像在控制台上操作，非常灵活。
2. 封装了物实里的大量原件，即使是**未解锁的原件**也可以轻易用脚本生成，甚至一些常用的电路已经被封装好了！
3. 物理实验室的存档的位置有点隐蔽，但用该脚本生成实验时，你无须亲自寻找这个文件在哪里。
4. 所有调用的库皆为Python的内置库

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
5.  补充readme

#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
