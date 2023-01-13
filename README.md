# 物实程序化

#### 介绍
通过一些命令对物理实验室存档进行操作

#### 安装教程

1.  打开Code文件夹中的physicsLab.py，复制或下载到本地
2.  打开physicsLab.py，在代码中修改文件路径（推荐）
3.  如果你的ide无法找到physicsLab,py，你需要sys.path.append('(path of physicsLab.py)')来解决这个问题

#### 使用说明

'''打开存档'''
open_Experiment("(Your .sav's path)")
'''如果你希望程序不覆盖掉存档中已有的实验状态，需要这样写'''
read_Experiment()
'''创建一个逻辑输入，坐标为(0, 0, 0.1)'''
logicInput(0, 0, 0.1) 
'''你也可以不写坐标，默认是(0,0,0)，请注意2原件的坐标不允许重叠！'''
o = orGate() '''此时o存储的是orGate的self'''
'''wire输入格式：
    wire(SourceLabel, SourcePin : int, TargetLabel, TargetPin : int, color = "蓝")
    SourceLabel与TargetLabel支持传入self与坐标（用tuple表示）
'''
wire(o, 0, (0,0,0), 1)
'''将程序中生成的原件，导线等等写入存档'''
write_Experiment()
'''然后打开存档见证奇迹
（更详细的内容以后写，如果你能加入我就太好了）'''

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
