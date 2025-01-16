# -*- coding: utf-8 -*-
''' `physicsLab` 操作存档的核心文件
    该文件提供操作存档的核心: `class _Experiment` 与所有元件的基类: class `_ElementBase`
    为了避免在physicsLab内出现大量的cyclic import
    该文件仅会对存档进行文件读写方面的操作, 对元件的导入由`class Experiment`负责
    `class Experiment`提供了更加用户友好的接口
'''
import os
import json
import copy
import time
import gzip
import requests
import platform

from physicsLab import plAR
from physicsLab import  _tools
from physicsLab import errors
from physicsLab import _colorUtils
from .web import User, _check_response
from .enums import Category, Tag, ExperimentType, OpenMode
from .typehint import Union, Optional, List, Dict, num_type, Self, Callable, Tuple, final, NoReturn

class _ExperimentStack:
    data: List["_Experiment"] = []

    def __new__(cls):
        return cls

    @classmethod
    def inside(cls, item: "_Experiment") -> bool:
        assert isinstance(item, _Experiment)

        for a_expe in cls.data:
            if a_expe.SAV_PATH == item.SAV_PATH:
                return True
        return False

    @classmethod
    def remove(cls, data: "_Experiment") -> None:
        assert isinstance(data, _Experiment)

        cls.data.remove(data)

    @classmethod
    def clear(cls) -> None:
        cls.data.clear()

    @classmethod
    def push(cls, data: "_Experiment") -> None:
        if not isinstance(data, _Experiment):
            raise TypeError

        cls.data.append(data)

    @classmethod
    def top(cls) -> "_Experiment":
        if len(cls.data) == 0:
            raise errors.ExperimentError("no experiment can be operated (experiment stack is empty)")

        return cls.data[-1]

def get_current_experiment() -> "_Experiment":
    ''' 获取当前正在操作的存档 '''
    return _ExperimentStack.top()

def _check_not_closed(method: Callable) -> Callable:
    def res(self: "_Experiment", *args, **kwargs):
        assert isinstance(self, _Experiment)
        if not _ExperimentStack.inside(self): # 存档已被关闭
            raise errors.ExperimentClosedError

        return method(self, *args, **kwargs)
    return res

class _Experiment:
    ''' 物实实验 (支持物实的三种实验类型) '''

    if "PHYSICSLAB_HOME_PATH" in os.environ.keys():
        SAV_PATH_DIR = os.environ["PHYSICSLAB_HOME_PATH"]
    else:
        if platform.system() == "Windows":
            SAV_PATH_DIR = os.path.join(plAR.WIN_PLAR_HOME_DIR, "Circuit")
        else:
            SAV_PATH_DIR = "physicsLabSav"

    open_mode: OpenMode
    _position2elements: Dict[Tuple[num_type, num_type, num_type], List["_ElementBase"]]
    _id2element: Dict[str, "_ElementBase"]
    Elements: List["_ElementBase"]
    SAV_PATH: str
    PlSav: dict
    CameraSave: dict
    VisionCenter: _tools.position
    TargetRotation: _tools.position
    experiment_type: ExperimentType

    def __init__(*args, **kwargs) -> NoReturn:
        raise NotImplementedError

    @_check_not_closed
    def get_elements_count(self) -> int:
        ''' 该实验的元件的数量 '''
        return len(self.Elements)

    @_check_not_closed
    def clear_elements(self) -> Self:
        ''' 清空该实验的所有元件 '''
        if self.experiment_type == ExperimentType.Circuit:
            self.Wires.clear()
        self.Elements.clear()
        self._position2elements.clear()
        self._id2element.clear()
        return self

    @_check_not_closed
    def del_element(self, element: "_ElementBase") -> Self:
        ''' 删除元件
            @param element: 三大实验的元件
        '''
        if not isinstance(element, _ElementBase):
            raise TypeError
        if element.experiment is not self:
            raise errors.ExperimentError("element is not in this experiment") # TODO 换一个更好的异常类型?
        if element not in self.Elements:
            raise errors.ElementNotFound

        identifier = element.data["Identifier"]

        if self.experiment_type == ExperimentType.Circuit:
            res_Wires = set()
            for a_wire in self.Wires:
                if a_wire.Source.element_self.data["Identifier"] == identifier \
                        or a_wire.Target.element_self.data["Identifier"] == identifier:
                    continue

                res_Wires.add(a_wire)
            self.Wires = res_Wires

        for position, elements in self._position2elements.items():
            can_break: bool = False
            if element in elements:
                elements.remove(element)
                can_break = True
            if len(elements) == 0:
                del self._position2elements[position]

            if can_break:
                break
        else:
            assert False

        assert identifier in self._id2element.keys()
        del self._id2element[identifier]

        assert element in self.Elements
        self.Elements.remove(element)

        return self

    # TODO 统一返回的行为，即始终返回列表之类的
    @_check_not_closed
    def get_element_from_position(
            self,
            x: num_type,
            y: num_type,
            z: num_type,
    ) -> Union["_ElementBase", List["_ElementBase"]]:
        ''' 通过坐标索引元件 '''
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        position = (_tools.round_data(x), _tools.round_data(y), _tools.round_data(z))
        if position not in self._position2elements.keys():
            raise errors.ElementNotFound(f"{position} do not exist")

        result: list = self._position2elements[position]
        return result[0] if len(result) == 1 else result

    @_check_not_closed
    def get_element_from_index(self, index: int) -> "_ElementBase":
        ''' 通过index (元件生成顺序) 索引元件, index从1开始 '''
        if not isinstance(index, int):
            raise TypeError
        if not 0 < index <= self.get_elements_count():
            raise errors.ElementNotFound("index out of range")

        return self.Elements[index - 1]

    @_check_not_closed
    def get_element_from_identifier(self, identifier: str) -> "_ElementBase":
        ''' 通过元件的id获取元件的引用 '''
        res = self._id2element.get(identifier)
        if res is None:
            raise errors.ElementNotFound

        return res

    @_check_not_closed
    def clear_wires(self) -> Self:
        ''' 删除所有导线 '''
        if self.experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError

        self.Wires.clear()
        return self

    @_check_not_closed
    def get_wires_count(self) -> int:
        ''' 获取当前导线数 '''
        if self.experiment_type != ExperimentType.Circuit:
            raise errors.ExperimentTypeError

        return len(self.Wires)

    def __write(self) -> None:
        if self.experiment_type == ExperimentType.Circuit:
            status_save: dict = {
                "SimulationSpeed": 1.0,
                "Elements": [a_element.data for a_element in self.Elements],
                "Wires": [a_wire.release() for a_wire in self.Wires],
            }
        elif self.experiment_type == ExperimentType.Celestial:
            status_save: dict = {
                "MainIdentifier": None,
                "Elements": {a_element.data["Identifier"] : a_element.data for a_element in self.Elements},
                "WorldTime": 0.0,
                "ScalingName": "内太阳系",
                "LengthScale": 1.0,
                "SizeLinear": 0.0001,
                "SizeNonlinear": 0.5,
                "StarPresent": False,
                "Setting": None,
            }
        elif self.experiment_type == ExperimentType.Electromagnetism:
            status_save: dict = {
                "SimulationSpeed": 1.0,
                "Elements": [a_element.data for a_element in self.Elements],
            }
        else:
            assert False

        self.PlSav["Experiment"]["CreationDate"] = int(time.time() * 1000)
        self.PlSav["Summary"]["CreationDate"] = int(time.time() * 1000)

        self.CameraSave["VisionCenter"] = f"{self.VisionCenter.x},{self.VisionCenter.z},{self.VisionCenter.y}"
        self.CameraSave["TargetRotation"] = f"{self.TargetRotation.x},{self.TargetRotation.z},{self.TargetRotation.y}"
        self.PlSav["Experiment"]["CameraSave"] = json.dumps(self.CameraSave)

        self.PlSav["Experiment"]["StatusSave"] = json.dumps(status_save, ensure_ascii=True, separators=(',', ': '))

    @_check_not_closed
    def save(
            self,
            target_path: Optional[str] = None,
            no_print_info: bool = False,
    ) -> Self:
        ''' 以物实存档的格式导出实验
            @param target_path: 将存档保存在此路径 (要求必须是file), 默认为 SAV_PATH
            @param no_print_info: 是否打印写入存档的元件数, 导线数(如果是电学实验的话)
        '''
        if not isinstance(target_path, (str, type(None))) or not isinstance(no_print_info, bool):
            raise TypeError

        if target_path is None:
            target_path = self.SAV_PATH

        if self.open_mode in (OpenMode.load_by_sav_name, OpenMode.load_by_filepath, OpenMode.load_by_plar_app):
            status: str = "update"
        elif self.open_mode == OpenMode.crt:
            status: str = "create"
        else:
            assert False

        self.__write()

        context: str = json.dumps(self.PlSav, indent=2, ensure_ascii=False, separators=(',', ':'))

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(context)

        if not no_print_info:
            if self.experiment_type == ExperimentType.Circuit:
                _colorUtils.color_print(
                    f"Successfully {status} experiment \"{self.PlSav['InternalName']}\"! "
                    f"{self.get_elements_count()} elements, {self.get_wires_count()} wires.",
                    color=_colorUtils.COLOR.GREEN
                )
            elif self.experiment_type == ExperimentType.Celestial \
                    or self.experiment_type == ExperimentType.Electromagnetism:
                _colorUtils.color_print(
                    f"Successfully {status} experiment \"{self.PlSav['InternalName']}\"! "
                    f"{self.get_elements_count()} elements.",
                    color=_colorUtils.COLOR.GREEN
                )
            else:
                assert False

        return self

    @_check_not_closed
    def close(self, *, delete: bool = False) -> None:
        ''' 退出对该存档的操作
            Note: 如果没有在调用Experiment.close前调用Experiment.save, 会丢失对存档的修改
        '''
        if delete:
            if os.path.exists(self.SAV_PATH): # 之所以判断路径是否存在是因为一个实验可能被创建但还未被写入就调用了delete
                os.remove(self.SAV_PATH)
                _colorUtils.color_print(
                    f"Successfully delete experiment \"{self.PlSav['InternalName']}\"(\"{self.SAV_PATH}\")",
                    _colorUtils.COLOR.BLUE
                )
            if os.path.exists(self.SAV_PATH.replace(".sav", ".jpg")): # 用存档生成的实验无图片
                os.remove(self.SAV_PATH.replace(".sav", ".jpg"))

        _ExperimentStack.remove(self)

    def __entitle(self, sav_name: str) -> None:
        assert isinstance(sav_name, str)

        self.PlSav["Summary"]["Subject"] = sav_name
        self.PlSav["InternalName"] = sav_name

    @_check_not_closed
    def entitle(self, sav_name: str) -> Self:
        ''' 对存档名进行重命名 '''
        if not isinstance(sav_name, str):
            raise TypeError

        self.__entitle(sav_name)
        return self

    @_check_not_closed
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

    @_check_not_closed
    def edit_tags(self, *tags: Tag) -> Self:
        if not all(isinstance(tag, Tag) for tag in tags):
            raise TypeError

        temp = self.PlSav["Summary"]["Tags"] + [tag.value for tag in tags]
        self.PlSav["Summary"]["Tags"] = list(set(temp))

        return self

    def __upload(
            self,
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

    @_check_not_closed
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

    @_check_not_closed
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
            x: Optional[num_type] = None,
            y: Optional[num_type] = None,
            z: Optional[num_type] = None,
            distance: Optional[num_type] = None,
            rotation_x: Optional[num_type] = None,
            rotation_y: Optional[num_type] = None,
            rotation_z: Optional[num_type] = None
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

        if not isinstance(x, (int, float)) \
                or not isinstance(y, (int, float)) \
                or not isinstance(z, (int, float)) \
                or not isinstance(distance, (int, float)) \
                or not isinstance(rotation_x, (int, float)) \
                or not isinstance(rotation_y, (int, float)) \
                or not isinstance(rotation_z, (int, float)):
            raise TypeError

        self.VisionCenter = _tools.position(x, y, z)
        self.CameraSave["Distance"] = distance
        self.TargetRotation = _tools.position(rotation_x, rotation_y, rotation_z)

        return self

    @_check_not_closed
    def paused(self, status: bool = True) -> Self:
        ''' 暂停或解除暂停实验 '''
        if not isinstance(status, bool):
            raise TypeError

        self.PlSav["Paused"] = status
        self.PlSav["Experiment"]["Paused"] = status

        return self

    @_check_not_closed
    def export(self, output_path: str = "temp.pl.py", sav_name: str = "temp") -> Self:
        ''' 以physicsLab代码的形式导出实验 '''
        res: str = f"from physicsLab import *\n\n" \
                f"expe = Experiment(OpenMode.crt, '{sav_name}', {self.experiment_type}, force_crt=True)\n"

        for a_element in self.Elements:
            res += f"e{a_element.get_index()} = {str(a_element)}\n"
        for a_wire in self.Wires:
            res += str(a_wire) + '\n'
        res += "expe.save()\nexpe.close()\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(res)

        return self

    @_check_not_closed
    def merge(
            self,
            other: "_Experiment",
            x: num_type = 0,
            y: num_type = 0,
            z: num_type = 0,
            elementXYZ: Optional[bool] = None
    ) -> Self:
        ''' 合并另一实验
            x, y, z, elementXYZ为重新设置要合并的实验的坐标系原点在self的坐标系的位置
            不是电学实验时, elementXYZ参数无效
        '''
        if not isinstance(other, _Experiment) or \
                not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)) or \
                not isinstance(elementXYZ, (bool, type(bool))):
            raise TypeError
        if self.experiment_type != other.experiment_type:
            raise errors.ExperimentTypeError
        if self is other:
            raise errors.ExperimentError("can not merge to itself") # TODO 换一个更好的异常类型?

        assert self.SAV_PATH is not None and other.SAV_PATH is not None

        if self is other:
            return self

        identifier_to_element: dict = {}

        # TODO 对天体与电学实验的支持可能不太好吧
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
                self.Wires.add(a_wire) # TODO 这里wire不深拷贝，通过wire拿到的element不对吧

        return self

class _ElementBase:
    data: dict
    experiment: _Experiment
    _position: _tools.position

    def __init__(self) -> None:
        raise NotImplementedError

    def set_position(self, x: num_type, y: num_type, z: num_type) -> Self:
        ''' 设置元件的位置 '''
        if not isinstance(x, (int, float)) or \
                not isinstance(y, (int, float)) or \
                not isinstance(z, (int, float)):
            raise TypeError

        x, y, z = _tools.round_data(x), _tools.round_data(y), _tools.round_data(z)
        assert hasattr(self, 'experiment')
        _Expe: _Experiment = self.experiment

        for self_list in _Expe._position2elements.values():
            if self in self_list:
                self_list.remove(self)

        assert hasattr(self, 'data')
        self.data['Position'] = f"{x},{z},{y}"

        assert hasattr(self, '_position')
        if self._position in _Expe._position2elements.keys():
            _Expe._position2elements[self._position].append(self)
        else:
            _Expe._position2elements[self._position] = [self]

        return self

    @final
    def get_position(self) -> tuple:
        ''' 获取元件的坐标 '''
        assert hasattr(self, '_position')
        return copy.deepcopy(self._position)

    @final
    def get_index(self) -> int:
        ''' 获取元件的index (每创建一个元件, index就加1 (index从1开始)) '''
        return self.experiment.Elements.index(self) + 1
