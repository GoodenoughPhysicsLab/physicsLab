# -*- coding: utf-8 -*-
from enum import Enum, unique

@unique
class ExperimentType(Enum):
    ''' 实验的类型 '''
    # 电学实验
    Circuit = 0
    # 电路图模式 1
    # 天体彩蛋模式 2
    # 天体物理实验
    Celestial = 3
    # 电与磁实验
    Electromagnetism = 4

@unique
class Category(Enum):
    ''' 实验区与黑洞区 '''
    Experiment = "Experiment"
    Discussion = "Discussion"

@unique
class Tag(Enum):
    ''' 标签 '''
    #TODO 投稿 标签
    # 实验区
    Circuit = "Type-0"
    Celestial = "Type-3"
    Electromagnetism = "Type-4"
    KnowledgeBase = "知识库"
    Featured = "精选"
    ElementarySchool = "小学"
    HighSchool = "高中"
    MiddleSchool = "初中"
    College = "大学"
    Professional = "专科"
    FunExperiment = "娱乐实验"
    SmallProject = "小作品"
    Curricular = "教学实验"
    NoRemixes = "禁止改编"
    ApplyForFeature = "精选申请"
    # 黑洞区
    BUG = "BUG"
    Discussion = "交流"
    Stories = "小说专区"
    Charroom = "聊天"
    Q_A = "问与答"
    # 远古标签
    Logic_Circuit = "逻辑电路"
    DC_Circuit = "直流电路"
    AC_Circuit = "交流电路"
    Electronic = "电子电路"
    Interest = "兴趣"

@unique
class OpenMode(Enum):
    ''' 用Experiment打开存档的模式 '''
    load_by_sav_name = 0 # 存档的名字 (在物实内给存档取的名字)
    load_by_filepath = 1 # 用户自己提供的存档的完整路径
    load_by_plar_app = 2 # 通过网络请求从物实读取的存档
    crt = 3 # 新建存档

@unique
class WireColor(Enum):
    black = "黑"
    blue = "蓝"
    red = "红"
    green = "绿"
    yellow = "黄"
