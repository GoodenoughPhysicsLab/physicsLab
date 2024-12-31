# -*- coding: utf-8 -*-
''' `physicsLab` 操作存档的核心文件
    该文件提供操作存档的核心: class `Experiment`
    该文件仅会对存档进行文件读写方面的操作, 这也是为什么需要显示调用`load_elements`的原因
'''
import os
import json
import copy
import time
import gzip
import requests
import platform

from enum import unique, Enum

from physicsLab import plAR
from physicsLab import  _tools
from physicsLab import errors
from physicsLab import savTemplate
from physicsLab import _colorUtils
from .web import User, _check_response
from .enums import Category, Tag
from .savTemplate import Generate
from .enums import ExperimentType
from ._element_base import ElementBase
from .typehint import Union, Optional, List, Dict, numType, Self, overload, Callable

class _ExperimentStack:
    data: List["Experiment"] = []

    def __new__(cls):
        return cls

    @classmethod
    def inside(cls, item: "Experiment") -> bool:
        assert isinstance(item, Experiment)

        for a_expe in cls.data:
            if a_expe.SAV_PATH == item.SAV_PATH:
                return True
        return False

    @classmethod
    def remove(cls, data: "Experiment"):
        assert isinstance(data, Experiment)

        cls.data.remove(data)

    @classmethod
    def push(cls, data: "Experiment") -> None:
        if not isinstance(data, Experiment):
            raise TypeError

        cls.data.append(data)

    @classmethod
    def top(cls) -> "Experiment":
        if len(cls.data) == 0:
            raise errors.ExperimentError("no experiment can be operated (experiment stack is empty)")

        return cls.data[-1]

def get_current_experiment() -> "Experiment":
    ''' 获取当前正在操作的存档 '''
    return _ExperimentStack.top()

def _check_method(method: Callable) -> Callable:
    def res(self: "Experiment", *args, **kwargs):
        assert isinstance(self, Experiment)
        if not _ExperimentStack.inside(self): # 存档已被关闭
            raise errors.ExperimentClosedError

        return method(self, *args, **kwargs)
    return res

@unique
class OpenMode(Enum):
    ''' 用Experiment打开存档的模式 '''
    load_by_sav_name = 0 # 存档的名字 (在物实内给存档取的名字)
    load_by_filepath = 1 # 用户自己提供的存档的完整路径
    load_by_plar_app = 2 # 通过网络请求从物实读取的存档
    crt = 3 # 新建存档

class Experiment:
    ''' 物实实验 (支持物实的三种实验类型) '''

    if "PHYSICSLAB_HOME_PATH" in os.environ.keys():
        SAV_PATH_DIR = os.environ["PHYSICSLAB_HOME_PATH"]
    else:
        if platform.system() == "Windows":
            SAV_PATH_DIR = os.path.join(plAR.WIN_PLAR_HOME_DIR, "Circuit")
        else:
            SAV_PATH_DIR = "physicsLabSav"

    SAV_PATH: str # 存档的完整路径

    @overload
    def __init__(self, open_mode: OpenMode, sav_name: str) -> None:
        ''' 根据存档名打开存档
            @open_mode = OpenMode.open_from_sav_name
            @sav_name: 存档的名字
        '''

    @overload
    def __init__(self, open_mode: OpenMode, filepath: str) -> None:
        ''' 根据存档对应的文件路径打开存档
            @open_mode = OpenMode.open_from_abs_path
            @filepath: 存档对应的文件的完整路径
        '''

    @overload
    def __init__(self, open_mode: OpenMode, content_id: str, category: Category, user: User = User()) -> None:
        ''' 从物实服务器中获取存档
            @open_mode = OpenMode.open_from_plar_app
            @content_id: 物实 实验/讨论 的id
            @category: 实验区还是黑洞区
            @user: 执行获取实验操作的用户, 若未指定则会创建一个临时匿名用户执行该操作 (会导致程序变慢)
        '''

    @overload
    def __init__(self, open_mode: OpenMode, sav_name: str, experiment_type: ExperimentType, force_crt: bool) -> None:
        ''' 创建一个新实验
            @open_mode = OpenMode.crt
        '''

    #TODO support **kwargs
    def __init__(self, open_mode: OpenMode, *args) -> None:
        if not isinstance(open_mode, OpenMode) or len(args) == 0:
            raise TypeError

        self.open_mode: OpenMode = open_mode
        # 通过坐标索引元件; key: self._position, value: List[self...]
        self._elements_position: Dict[tuple, list] = {}
        # 通过index（元件生成顺序）索引元件
        self.Elements:List[ElementBase] = []
        # 是否读取过实验的元件状态 (也就是是否调用过 load_elements)
        self.is_load_elements: bool = False

        # 尽管读取存档时会将元件的字符串一并读入, 但只有在调用 load_elements 将元件的信息
        # 导入self.Elements与self._element_position之后, 元件信息才被完全导入
        if open_mode == OpenMode.load_by_sav_name or open_mode == OpenMode.load_by_filepath:
            sav_name, *rest = args

            if not isinstance(sav_name, str) or len(rest) != 0:
                raise TypeError

            if open_mode == OpenMode.load_by_filepath:
                self.SAV_PATH = os.path.abspath(sav_name)

                if not os.path.exists(self.SAV_PATH):
                    raise errors.ExperimentNotExistError(f"{self.SAV_PATH} not found")
                if _ExperimentStack.inside(self):
                    raise errors.ExperimentOpenedError

                _ExperimentStack.push(self)
                _temp = _open_sav(self.SAV_PATH)

                assert _temp is not None # ??? 万一就是用户的输入不对呢

                if "Experiment" in _temp.keys():
                    self.PlSav = _temp
                else: # 读取物实导出的存档只含有.sav的Experiment部分
                    if _temp["Type"] == ExperimentType.Circuit.value:
                        self.PlSav = savTemplate.Circuit
                    elif _temp["Type"] == ExperimentType.Celestial.value:
                        self.PlSav = savTemplate.Celestial
                    elif _temp["Type"] == ExperimentType.Electromagnetism.value:
                        self.PlSav = savTemplate.Electromagnetism
                    else:
                        raise errors.InternalError

                    self.PlSav["Experiment"] = _temp
            elif open_mode == OpenMode.load_by_sav_name:
                filename = search_experiment(sav_name)
                if filename is None:
                    raise errors.ExperimentNotExistError(f'No such experiment "{sav_name}"')

                self.SAV_PATH = os.path.join(Experiment.SAV_PATH_DIR, filename)
                if _ExperimentStack.inside(self):
                    raise errors.ExperimentOpenedError

                _ExperimentStack.push(self)

                self.PlSav = search_experiment.sav
            else:
                raise errors.InternalError

            self._read_CameraSave(self.PlSav["Experiment"]["CameraSave"])

            if self.PlSav["Summary"] is None:
                self.PlSav["Summary"] = savTemplate.Circuit["Summary"]

            if self.PlSav["Experiment"]["Type"] == ExperimentType.Circuit.value:
                self.experiment_type = ExperimentType.Circuit
                # 该实验是否是元件坐标系
                self.is_elementXYZ: bool = False
                # 元件坐标系的坐标原点
                self.elementXYZ_origin_position: _tools.position = _tools.position(0, 0, 0)
                self.Wires: set = set() # Set[Wire] # 存档对应的导线
                # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
                self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": Generate, "Wires": Generate}
            elif self.PlSav["Experiment"]["Type"] == ExperimentType.Celestial.value:
                self.experiment_type = ExperimentType.Celestial
                self.StatusSave: dict = {
                    "MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                    "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                    "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None,
                }
            elif self.PlSav["Experiment"]["Type"] == ExperimentType.Electromagnetism.value:
                self.experiment_type = ExperimentType.Electromagnetism
                self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}
            else:
                raise errors.InternalError
        elif open_mode == OpenMode.load_by_plar_app:
            content_id, category, *rest = args

            if not isinstance(content_id, str) or not isinstance(category, Category):
                raise TypeError
            if len(rest) == 0:
                user = User()
            elif len(rest) == 1:
                if not isinstance(rest[0], User):
                    raise TypeError
                user = rest[0]
            else:
                raise TypeError

            self.SAV_PATH = os.path.join(Experiment.SAV_PATH_DIR, f"{content_id}.sav")
            if _ExperimentStack.inside(self):
                    raise errors.ExperimentOpenedError

            _ExperimentStack.push(self)

            _summary = user.get_summary(content_id, category)["Data"]
            del _summary["$type"]
            _summary["Category"] = category.value
            self.PlSav["Summary"] = _summary # 此处应该有问题, 存档不完整
        elif open_mode == OpenMode.crt:
            sav_name, experiment_type, force_crt, *rest = args

            if not isinstance(sav_name, str) or \
                    not isinstance(experiment_type, ExperimentType) or \
                    not isinstance(force_crt, bool) or \
                    len(rest) != 0:
                raise TypeError

            search = search_experiment(sav_name)
            if not force_crt and search is not None:
                raise errors.ExperimentExistError
            elif force_crt and search is not None:
                # TODO 要是在一个force_crt的实验中又force_crt这个实验呢？
                path = os.path.join(Experiment.SAV_PATH_DIR, search)
                os.remove(path)
                if os.path.exists(path.replace(".sav", ".jpg")): # 用存档生成的实验无图片，因此可能删除失败
                    os.remove(path.replace(".sav", ".jpg"))

            _ExperimentStack.push(self)

            self.experiment_type = experiment_type
            self.SAV_PATH = os.path.join(Experiment.SAV_PATH_DIR, f"{_tools.randString(34)}.sav")

            if self.experiment_type == ExperimentType.Circuit:
                self.is_elementXYZ: bool = False
                # 元件坐标系的坐标原点
                self.elementXYZ_origin_position: _tools.position = _tools.position(0, 0, 0)
                self.PlSav: dict = copy.deepcopy(savTemplate.Circuit)
                self.Wires: set = set() # Set[Wire] # 存档对应的导线
                # 存档对应的StatusSave, 存放实验元件，导线（如果是电学实验的话）
                self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": Generate, "Wires": Generate}
                self.CameraSave: dict = {
                    "Mode": 0, "Distance": 2.7, "VisionCenter": Generate, "TargetRotation": Generate
                }
                self.VisionCenter: _tools.position = _tools.position(0, -0.45, 1.08)
                self.TargetRotation: _tools.position = _tools.position(50, 0, 0)
            elif self.experiment_type == ExperimentType.Celestial:
                self.PlSav: dict = copy.deepcopy(savTemplate.Celestial)
                self.StatusSave: dict = {
                    "MainIdentifier": None, "Elements": {}, "WorldTime": 0.0,
                    "ScalingName": "内太阳系", "LengthScale": 1.0, "SizeLinear": 0.0001,
                    "SizeNonlinear": 0.5, "StarPresent": False, "Setting": None
                }
                self.CameraSave: dict = {
                    "Mode": 2, "Distance": 2.75, "VisionCenter": Generate, "TargetRotation": Generate
                }
                self.VisionCenter: _tools.position = _tools.position(0 ,0, 1.08)
                self.TargetRotation: _tools.position = _tools.position(90, 0, 0)
            elif self.experiment_type == ExperimentType.Electromagnetism:
                self.PlSav: dict = copy.deepcopy(savTemplate.Electromagnetism)
                self.StatusSave: dict = {"SimulationSpeed": 1.0, "Elements": []}
                self.CameraSave: dict = {
                    "Mode": 0, "Distance": 3.25, "VisionCenter": Generate, "TargetRotation": Generate,
                }
                self.VisionCenter: _tools.position = _tools.position(0, 0 ,0.88)
                self.TargetRotation: _tools.position = _tools.position(90, 0, 0)
            else:
                raise errors.InternalError

            self.entitle(sav_name)
        else:
            raise errors.InternalError

        assert isinstance(self.SAV_PATH, str)

    # TODO 将该函数放到elements.py中
    def get_element_from_identifier(self, identifier: str):
        ''' 通过 原件的["Identifier"]获取元件的引用 '''
        for element in self.Elements:
            assert hasattr(element, "data")
            if element.data["Identifier"] == identifier: # type: ignore -> has attr .data
                return element
        raise errors.ElementNotFound

    def _read_CameraSave(self, camera_save: str) -> None:
        self.CameraSave = json.loads(camera_save)
        temp = eval(f"({self.CameraSave['VisionCenter']})")
        self.VisionCenter: _tools.position = _tools.position(temp[0], temp[2], temp[1]) # x, z, y
        temp = eval(f"({self.CameraSave['TargetRotation']})")
        self.TargetRotation: _tools.position = _tools.position(temp[0], temp[2], temp[1]) # x, z, y

    def __write(self) -> None:
        self.PlSav["Experiment"]["CreationDate"] = int(time.time() * 1000)
        self.PlSav["Summary"]["CreationDate"] = int(time.time() * 1000)

        self.CameraSave["VisionCenter"] = f"{self.VisionCenter.x},{self.VisionCenter.z},{self.VisionCenter.y}"
        self.CameraSave["TargetRotation"] = f"{self.TargetRotation.x},{self.TargetRotation.z},{self.TargetRotation.y}"
        self.PlSav["Experiment"]["CameraSave"] = json.dumps(self.CameraSave)

        if self.experiment_type == ExperimentType.Circuit:
            self.StatusSave["Elements"] = [a_element.data for a_element in self.Elements]
            self.StatusSave["Wires"] = [a_wire.release() for a_wire in self.Wires]
        elif self.experiment_type == ExperimentType.Celestial:
            self.StatusSave["Elements"] = {
                a_element.data["Identifier"] : a_element.data for a_element in self.Elements
            }
        elif self.experiment_type == ExperimentType.Electromagnetism:
            self.StatusSave["Elements"] = [a_element.data for a_element in self.Elements]
        else:
            raise errors.InternalError

        self.PlSav["Experiment"]["StatusSave"] = json.dumps(self.StatusSave, ensure_ascii=False, separators=(',', ': '))

    @_check_method
    def save(
            self,
            extra_filepath: Optional[str] = None, # 改为target_output_path: str | List[str], 默认是SAV_PATH_ROOT
            ln: bool = False,
            no_print_info: bool = False,
    ) -> Self:
        ''' 以物实存档的格式导出实验
            @param extra_filepath: 自定义保存存档的路径, 但仍会在 SAV_PATH_ROOT 下保存存档
            @param ln: 是否将StatusSave字符串换行 (便于查看存档, 但会导致不符合标准json的格式, 虽然物实可以读取)
            @param no_print_info: 是否打印写入存档的元件数, 导线数(如果是电学实验的话)
        '''
        def _format_StatusSave(json_str: str) -> str:
            ''' 将StatusSave字符串换行
                注意: 换行之后的结果不符合json语法(json无多行字符串)
                     但物实可以读取
                     因此, 仅用于调试
                     暂时只支持电学存档
            '''
            json_str = json_str.replace( # format element json
                "{\\\"ModelID", "\n      {\\\"ModelID"
            )
            json_str = json_str.replace( # format end element json
                "DiagramRotation\\\": 0}]", "DiagramRotation\\\": 0}\n    ]"
            )
            json_str = json_str.replace("{\\\"Source", "\n      {\\\"Source")
            json_str = json_str.replace("色导线\\\"}]}", "色导线\\\"}\n    ]}")
            return json_str

        if not isinstance(extra_filepath, (str, type(None))) or \
                not isinstance(ln, bool) or \
                not isinstance(no_print_info, bool):
            raise TypeError

        if self.open_mode in (OpenMode.load_by_sav_name, OpenMode.load_by_filepath, OpenMode.load_by_plar_app):
            status: str = "update"
        elif self.open_mode == OpenMode.crt:
            status: str = "create"
        else:
            raise errors.InternalError

        assert self.SAV_PATH is not None

        self.__write()

        context: str = json.dumps(self.PlSav, indent=2, ensure_ascii=False, separators=(',', ':'))
        if ln:
            context = _format_StatusSave(context)

        with open(self.SAV_PATH, "w", encoding="utf-8") as f:
            f.write(context)
        if extra_filepath is not None:
            if not extra_filepath.endswith(".sav"):
                extra_filepath += ".sav"
            with open(extra_filepath, "w", encoding="utf-8") as f:
                f.write(context)

        if not no_print_info:
            if self.experiment_type == ExperimentType.Circuit:
                _colorUtils.color_print(
                    f"Successfully {status} experiment \"{self.PlSav['InternalName']}\"! "
                    f"{self.Elements.__len__()} elements, {self.Wires.__len__()} wires.",
                    color=_colorUtils.COLOR.GREEN
                )
            elif self.experiment_type == ExperimentType.Celestial \
                    or self.experiment_type == ExperimentType.Electromagnetism:
                _colorUtils.color_print(
                    f"Successfully {status} experiment \"{self.PlSav['InternalName']}\"! "
                    f"{self.Elements.__len__()} elements.",
                    color=_colorUtils.COLOR.GREEN
                )
            else:
                raise errors.InternalError

        return self

    @_check_method
    def exit(self, delete: bool = False) -> None:
        ''' 立刻退出对该存档的操作
            Note: 如果没有在调用Experiment.exit前调用Experiment.save, 会丢失对存档的修改
        '''
        if delete:
            if os.path.exists(self.SAV_PATH): # 之所以判断路径是否存在是因为一个实验可能被创建但还未被写入就调用了delete
                os.remove(self.SAV_PATH)
                _colorUtils.color_print(
                    f"Successfully delete experiment \"{self.PlSav['InternalName']}\"!({self.SAV_PATH})",
                    _colorUtils.COLOR.BLUE
                )
            elif self.open_mode != OpenMode.crt:
                raise InterruptedError
            if os.path.exists(self.SAV_PATH.replace(".sav", ".jpg")): # 用存档生成的实验无图片
                os.remove(self.SAV_PATH.replace(".sav", ".jpg"))

        _ExperimentStack.remove(self)

    @_check_method
    def entitle(self, sav_name: str) -> Self:
        ''' 对存档名进行重命名 '''
        if not isinstance(sav_name, str):
            raise TypeError

        self.PlSav["Summary"]["Subject"] = sav_name
        self.PlSav["InternalName"] = sav_name

        return self

    @_check_method
    def edit_publish_info(
            self,
            title: Optional[str] = None,
            introduction: Optional[str] = None,
            wx: bool = False,
    ) -> Self:
        ''' 生成与发布实验有关的存档内容
            @param title: 标题
            @param introduction: 简介
            @param wx: 是否续写简介
        '''
        def introduce_Experiment(introduction: Union[str, None]) -> None:
            '''  发布实验时输入实验介绍 '''
            if introduction is not None:
                if self.PlSav['Summary']['Description'] is not None and wx:
                    self.PlSav['Summary']['Description'] += introduction.split('\n')
                else:
                    self.PlSav['Summary']['Description'] = introduction.split('\n')

        def name_Experiment(title: Union[str, None]) -> None:
            ''' 发布实验时输入实验标题 '''
            if title is not None:
                self.PlSav['Summary']['Subject'] = title

        assert self.SAV_PATH is not None # ???

        introduce_Experiment(introduction)
        name_Experiment(title)

        return self

    @_check_method
    def edit_tags(self, *tags: Tag) -> Self:
        if not all(isinstance(tag, Tag) for tag in tags):
            raise TypeError

        temp = self.PlSav["Summary"]["Tags"] + [tag.value for tag in tags]
        self.PlSav["Summary"]["Tags"] = list(set(temp))

        return self

    def __upload(self,
            user: User,
            category: Optional[Category],
            image_path: Optional[str],
    ):
        if image_path is not None and not isinstance(image_path, str) or \
            category is not None and not isinstance(category, Category) or \
            not isinstance(user, User):
            raise TypeError
        if image_path is not None and (not os.path.exists(image_path) or not os.path.isfile(image_path)):
            raise FileNotFoundError
        if user.is_anonymous:
            raise PermissionError("you must register first")

        self.__write()
        workspace = copy.deepcopy(self.PlSav)
        workspace["Summary"] = None
        _summary = self.PlSav["Summary"]

        if _summary["Language"] is None:
            _summary["Language"] = "Chinese"
        _summary["User"]["ID"] = user.user_id
        _summary["User"]["Nickname"] = user.nickname
        _summary["User"]["Signature"] = user.signature
        _summary["User"]["Avatar"] = user.avatar
        _summary["User"]["AvatarRegion"] = user.avatar_region
        _summary["User"]["Decoration"] = user.decoration
        _summary["User"]["Verification"] = user.verification

        if category is not None:
            _summary["Category"] = category.value

        plar_version = plAR.get_plAR_version()
        if plar_version is not None:
            plar_version = int(f"{plar_version[0]}{plar_version[1]}{plar_version[2]}")
        else:
            plar_version = 2411
        _summary["Version"] = plar_version

        # 请求更新实验
        submit_data = {
            "Summary": _summary,
            "Workspace": workspace,
        }

        if image_path is not None:
            image_size = os.path.getsize(image_path)
            if image_size >= 1048576:
                errors.warning("image size is bigger than 1MB")
                image_size = -image_size # 利用物实bug发布大图片
            submit_data["Request"] = {
                "FileSize": image_size,
                'Extension': ".jpg",
            }

        submit_response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/SubmitExperiment",
            data=gzip.compress(json.dumps(submit_data).encode("utf-8")),
            headers={
                "x-API-Token": user.token,
                "x-API-AuthCode": user.auth_code,
                "x-API-Version": str(plar_version),
                "Accept-Encoding": "gzip",
                "Content-Type": "gzipped/json",
            }
        )
        def callback(status_code):
            if status_code == 403:
                _colorUtils.color_print(
                    "you can't submit experiment because you are not the author "
                    "or experiment status(elements, tags...) is invalid",
                    _colorUtils.COLOR.RED,
                )
        _check_response(submit_response, callback)

        return submit_response.json(), submit_data

    @_check_method
    def upload(
            self,
            user: User,
            category: Category,
            image_path: Optional[str] = None,
    ) -> Self:
        ''' 发布新实验
            @user: 不允许匿名登录
            @param category: 实验区还是黑洞区
            @param image_path: 图片路径
        '''
        if not isinstance(category, Category) or \
            image_path is not None and not isinstance(image_path, str):
            raise TypeError
        if self.PlSav["Summary"]["ID"] is not None:
            raise Exception(
                "upload can only be used to upload a brand new experiment, try using `.update` instead"
            )

        submit_response, submit_data = self.__upload(user, category, image_path)

        if image_path is not None:
            submit_data["Summary"]["Image"] += 1

        user.confirm_experiment(
            submit_response["Data"]["Summary"]["ID"], {
                Category.Experiment.value: Category.Experiment,
                Category.Discussion.value: Category.Discussion,
            }[category.value], submit_data["Summary"]["Image"]
        )

        if image_path is not None:
            user.upload_image(submit_response["Data"]["Token"]["Policy"],
                            submit_response["Data"]["Token"]["Authorization"],
                            image_path)

        return self

    @_check_method
    def update(
            self,
            user: User,
            image_path: Optional[str] = None,
    ) -> Self:
        ''' 更新实验到物实
            @user: 不允许匿名登录
            @param image_path: 图片路径
        '''
        if self.PlSav["Summary"]["ID"] is None:
            raise Exception(
                "update can only be used to upload an exist experiment, try using `.upload` instead"
            )

        submit_response, submit_data = self.__upload(user, None, image_path)

        if image_path is not None:
            submit_data["Summary"]["Image"] += 1

        response = requests.post(
            "https://physics-api-cn.turtlesim.com/Contents/SubmitExperiment",
            data=gzip.compress(json.dumps(submit_data).encode("utf-8")),
            headers={
                "x-API-Token": user.token,
                "x-API-AuthCode": user.auth_code,
                "x-API-Version": str(submit_data["Summary"]["Version"]),
                "Accept-Encoding": "gzip",
                "Content-Type": "gzipped/json",
            }
        )
        _check_response(response)

        if image_path is not None:
            user.upload_image(submit_response["Data"]["Token"]["Policy"],
                            submit_response["Data"]["Token"]["Authorization"],
                            image_path)

        return self

    def observe(
            self,
            x: Optional[numType] = None,
            y: Optional[numType] = None,
            z: Optional[numType] = None,
            distance: Optional[numType] = None,
            rotation_x: Optional[numType] = None,
            rotation_y: Optional[numType] = None,
            rotation_z: Optional[numType] = None
    ) -> Self:
        ''' 设置实验者的视角
            x, y, z : 实验者观察的坐标
            distance: 实验者到(x, y, z)的距离
            rotation: 实验者观察的角度
        '''
        if x is None:
            x = self.VisionCenter.x
        if y is None:
            y = self.VisionCenter.y
        if z is None:
            z = self.VisionCenter.z
        if distance is None:
            distance = self.CameraSave["Distance"]
        if rotation_x is None:
            rotation_x = self.TargetRotation.x
        if rotation_y is None:
            rotation_y = self.TargetRotation.y
        if rotation_z is None:
            rotation_z = self.TargetRotation.z

        if not isinstance(x, (int, float)):
            raise TypeError
        if not isinstance(y, (int, float)):
            raise TypeError
        if not isinstance(z, (int, float)):
            raise TypeError
        if not isinstance(distance, (int, float)):
            raise TypeError
        if not isinstance(rotation_x, (int, float)):
            raise TypeError
        if not isinstance(rotation_y, (int, float)):
            raise TypeError
        if not isinstance(rotation_z, (int, float)):
            raise TypeError

        self.VisionCenter = _tools.position(x, y, z)
        self.CameraSave["Distance"] = distance
        self.TargetRotation = _tools.position(rotation_x, rotation_y, rotation_z)

        return self

    @_check_method
    def paused(self, status: bool = True) -> Self:
        ''' 暂停或解除暂停实验 '''
        if not isinstance(status, bool):
            raise TypeError

        self.PlSav["Paused"] = status
        self.PlSav["Experiment"]["Paused"] = status

        return self

    @_check_method
    def export(self, output_path: str = "temp.pl.py", sav_name: str = "temp") -> Self:
        ''' 以physicsLab代码的形式导出实验 '''
        res: str = f"from physicsLab import *\nexp = Experiment('{sav_name}')\n"

        for a_element in self.Elements:
            res += f"e{a_element.get_index()} = {str(a_element)}\n"
        for a_wire in self.Wires:
            res += str(a_wire) + '\n'
        res += "\nexp.write()"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(res)

        return self

    @_check_method
    def merge(
            self,
            other: "Experiment",
            x: numType = 0,
            y: numType = 0,
            z: numType = 0,
            elementXYZ: Optional[bool] = None
    ) -> Self:
        ''' 合并另一实验
            x, y, z, elementXYZ为重新设置要合并的实验的坐标系原点在self的坐标系的位置
            不是电学实验时, elementXYZ参数无效
        '''
        if not isinstance(other, Experiment) or \
                not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)) or \
                not isinstance(elementXYZ, (bool, type(bool))):
            raise TypeError
        if self.experiment_type != other.experiment_type:
            raise errors.ExperimentTypeError

        assert self.SAV_PATH is not None and other.SAV_PATH is not None

        if self is other:
            return self

        identifier_to_element: dict = {}

        for a_element in other.Elements:
            a_element = copy.deepcopy(a_element, memo={id(a_element.experiment): self})
            e_x, e_y, e_z = a_element.get_position()
            if self.experiment_type == ExperimentType.Circuit:
                from .circuit.elementXYZ import xyzTranslate, translateXYZ
                if elementXYZ and not a_element.is_elementXYZ:
                    e_x, e_y, e_z = translateXYZ(e_x, e_y, e_z, a_element.is_bigElement)
                elif not elementXYZ and a_element.is_elementXYZ:
                    e_x, e_y, e_z = xyzTranslate(e_x, e_y, e_z, a_element.is_bigElement)
            a_element.set_position(e_x + x, e_y + y, e_z + z, elementXYZ)
            # set_Position已处理与_elements_position有关的操作
            self.Elements.append(a_element)

            identifier_to_element[a_element.data["Identifier"]] = a_element

        if self.experiment_type == ExperimentType.Circuit and other.experiment_type == ExperimentType.Circuit:
            for a_wire in other.Wires:
                a_wire = copy.deepcopy(
                    a_wire, memo={
                        id(a_wire.Source.element_self):
                            identifier_to_element[a_wire.Source.element_self.data["Identifier"]],
                        id(a_wire.Target.element_self):
                            identifier_to_element[a_wire.Target.element_self.data["Identifier"]],
                })
                self.Wires.add(a_wire)

        return self
def _get_all_pl_sav() -> List[str]:
    ''' 获取所有物实存档的文件名 '''
    from os import walk
    savs = [i for i in walk(Experiment.SAV_PATH_DIR)][0]
    savs = savs[savs.__len__() - 1]
    return [aSav for aSav in savs if aSav.endswith('sav')]

def _open_sav(sav_path) -> Optional[dict]:
    ''' 打开一个存档, 返回存档对应的dict
        @param sav_path: 存档的绝对路径
    '''
    def encode_sav(path: str, encoding: str) -> Optional[dict]:
        try:
            with open(path, encoding=encoding) as f:
                d = json.loads(f.read().replace('\n', ''))
        except (json.decoder.JSONDecodeError, UnicodeDecodeError): # 文件不是物实存档
            return None
        else:
            return d

    assert os.path.exists(sav_path)

    res = encode_sav(sav_path, "utf-8")
    if res is not None:
        return res

    try:
        import chardet
    except ImportError:
        for encoding in ("utf-8-sig", "gbk"):
            res = encode_sav(sav_path, encoding)
            if res is not None:
                return res
    else:
        with open(sav_path, "rb") as f:
            encoding = chardet.detect(f.read())["encoding"]
        return encode_sav(sav_path, encoding)

def search_experiment(sav_name: str) -> Optional[str]:
    ''' 检测实验是否存在
        @param sav_name: 存档名

        若存在则返回存档对应的文件名, 若不存在则返回None
    '''
    for aSav in _get_all_pl_sav():
        sav = _open_sav(os.path.join(Experiment.SAV_PATH_DIR, aSav))
        if sav is None:
            continue
        if sav["InternalName"] == sav_name:
            search_experiment.sav = sav
            return aSav

    return None
