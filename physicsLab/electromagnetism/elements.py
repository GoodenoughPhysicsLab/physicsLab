# -*- coding: utf-8 -*-
from physicsLab.savTemplate import Generate
from ._electromagnetismBase import ElectromagnetismBase
from physicsLab._typing import (
    num_type,
    Optional,
    final,
    LiteralString,
)

class Negative_Charge(ElectromagnetismBase):
    def __init__(self, x: num_type, y: num_type, z: num_type, /, *, identifier: Optional[str] = None) -> None:
        self.data = {
            "ModelID": "Negative Charge", "Identifier": Generate,
            "Properties": {"锁定": 1.0, "强度": -1e-07, "质量": 0.1},
            "Position": Generate, "Rotation": Generate, "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0"
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "负电荷"

class Positive_Charge(ElectromagnetismBase):
    def __init__(self, x: num_type, y: num_type, z: num_type, /, *, identifier: Optional[str] = None) -> None:
        self.data = {
            "ModelID": "Positive Charge", "Identifier": Generate,
            "Properties": {"锁定": 1.0, "强度": 1e-07, "质量": 0.1},
            "Position": Generate, "Rotation": Generate, "Velocity": "0,0,0",
            "AngularVelocity": "0,0,0"
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "正电荷"

class Negative_Test_Charge(ElectromagnetismBase):
    def __init__(self, x: num_type, y: num_type, z: num_type, /, *, identifier: Optional[str] = None) -> None:
        self.data = {
            'ModelID': 'Negative Test Charge', 'Identifier': Generate,
            'Properties': {'锁定': 0.0, '强度': -1e-10, '质量': 5e-06},
            'Position': Generate, 'Rotation': Generate, 'Velocity': '0,0,0',
            'AngularVelocity': '0,0,0'
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "正试验电荷"

class Positive_Test_Charge(ElectromagnetismBase):
    def __init__(self, x: num_type, y: num_type, z: num_type, /, *, identifier: Optional[str] = None) -> None:
        self.data = {
            'ModelID': 'Positive Test Charge', 'Identifier': Generate,
            'Properties': {'锁定': 0.0, '强度': -1e-10, '质量': 5e-06},
            'Position': Generate, 'Rotation': Generate, 'Velocity': '0,0,0',
            'AngularVelocity': '0,0,0'
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "负试验电荷"

class Bar_Magnet(ElectromagnetismBase):
    def __init__(self, x: num_type, y: num_type, z: num_type, /, *, identifier: Optional[str] = None) -> None:
        self.data = {
            'ModelID': 'Bar Magnet', 'Identifier': Generate,
            'Properties': {'锁定': 1.0, '强度': 1.0, '质量': 10.0},
            'Position': Generate, 'Rotation': Generate, 'Velocity': '0,0,0',
            'AngularVelocity': '0,0,0'
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "条形磁铁"

class Compass(ElectromagnetismBase):
    def __init__(self, x: num_type, y: num_type, z: num_type, /, *, identifier: Optional[str] = None) -> None:
        self.data = {
            'ModelID': 'Compass', 'Identifier': Generate,
            'Properties': {'锁定': 1.0},
            'Position': Generate, 'Rotation': Generate,
            'Velocity': '0,0,0', 'AngularVelocity': '0,0,0'
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "指南针"

class Uniform_Magnetic_Field(ElectromagnetismBase):
    def __init__(self, x: num_type, y: num_type, z: num_type, /, *, identifier: Optional[str] = None) -> None:
        self.data = {
            'ModelID': 'Uniform Magnetic Field', 'Identifier': Generate,
            'Properties': {'锁定': 0.0, '强度': 1000.0, '方向': 1.0},
            'Position': Generate, 'Rotation': Generate,
            'Velocity': '0,0,0', 'AngularVelocity': '0,0,0'
        }

    @final
    @staticmethod
    def zh_name() -> LiteralString:
        return "匀强磁场"

