# -*- coding: utf-8 -*-
from enum import Enum, unique

@unique
class ExperimentType(Enum):
    ''' 实验的类型 '''
    # 电学实验
    Circuit = 0
    # 电路图模式 2
    # 天体物理实验
    Celestial = 3
    # 天体彩蛋模式 4
    # 电与磁实验
    Electromagnetism = 4

class Category(Enum):
    ''' 实验区与黑洞区 '''
    Experiment = "Experiment"
    Discussion = "Discussion"
    BlackHole = Discussion # Discussion的别名

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
