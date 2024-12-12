# -*- coding: utf-8 -*-
from physicsLab.savTemplate import Generate
from physicsLab.typehint import numType
from ._planetbase import PlanetBase


class Mercury(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Mercury", "Override": None,
            "Name": "水星", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 2439.7, "RadiusVisible": 0.00493933167,
            "RotationPeriod": 58.646225, "RotationPhase": 358.9865,
            "AxialTilt": 0.034, "Mass": 0.33022, "OrbitType": 0,
            "OrbitEstimation": 0, "Density": 5.4288210902782295,
            "Gravity": 3.7027293142758535, "Luminosity": 0.0, "Temperature": 0.0,
            "Albedo": 0.11900000274181366, "PowerAbsorbtion": 0.0,
            "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate,
            "Acceleration": Generate, "Period": 0.0, "Eccentricity": 0.0,
            "OmegaUC": 0.0, "OmegaLC": 0.0, "Inclination": 0.0, "Phase": 0.0,
            "PhaseCurrent": 0.0, "AxisSemi": 10.0, "Perihelion": 10.0,
            "Aphelion": 10.0, "LeavingKepler": False
        }

class Venus(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Venus", "Override": None,
            "Name": "金星", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 6051.8, "RadiusVisible": 0.007779331,
            "RotationPeriod": -243.0187, "RotationPhase": 0.0,
            "AxialTilt": 177.4, "Mass": 4.8676, "OrbitType": 0,
            "OrbitEstimation": 0, "Density": 5.242912514272886,
            "Gravity": 8.870276983364493, "Luminosity": 0.0,
            "Temperature": 0.0, "Albedo": 0.75, "PowerAbsorbtion": 0.0,
            "PlanetariumBalance": 0.0, "Position": Generate,
            "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0,
            "OmegaLC": 0.0, "Inclination": 0.0, "Phase": 0.0,
            "PhaseCurrent": 0.0, "AxisSemi": 10.0, "Perihelion": 10.0,
            "Aphelion": 10.0, "LeavingKepler": False
        }

class Earth(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Earth", "Override": None,
            "Name": "地球", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 6378.0, "RadiusVisible": 0.007986238,
            "RotationPeriod": 0.9972697, "RotationPhase": 0.0,
            "AxialTilt": 23.44, "Mass": 5.9722, "OrbitType": 0,
            "OrbitEstimation": 0, "Density": 5.495309827118606,
            "Gravity": 9.798434986805644, "Luminosity": 0.0,
            "Temperature": 0.0, "Albedo": 0.28999999165534973,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0,
            "AxisSemi": 10.0, "Perihelion": 10.0, "Aphelion": 10.0,
            "LeavingKepler": False
        }
class Mars(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Mars", "Override": None,
            "Name": "火星", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 3397.0, "RadiusVisible": 0.0227075517,
            "RotationPeriod": 1.02595675, "RotationPhase": 0.0, "AxialTilt": 25.2,
            "Mass": 0.64185, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 3.9089335888549033, "Gravity": 3.7122212826765337,
            "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.1599999964237213,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Jupiter(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Jupiter", "Override": None,
            "Name": "木星", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 71492.0, "RadiusVisible": 0.477894723,
            "RotationPeriod": 0.41354, "RotationPhase": 0.0, "AxialTilt": 3.1,
            "Mass": 1898.6, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 1.2404307437459954, "Gravity": 24.791909943543278,
            "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.34299999475479126,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Saturn(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Saturn", "Override": None,
            "Name": "土星", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 60268.0, "RadiusVisible": 0.40286687,
            "RotationPeriod": 6.3875, "RotationPhase": 0.0, "AxialTilt": 26.7,
            "Mass": 568.46, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 0.6199418849015184, "Gravity": 10.445224444042164,
            "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.34200000762939453,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Uranus(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Uranus", "Override": None,
            "Name": "天王星", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 25559.0, "RadiusVisible": 0.170851439,
            "RotationPeriod": 0.71833, "RotationPhase": 0.0, "AxialTilt": 97.8,
            "Mass": 86.81, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 1.241222274811176, "Gravity": 8.868975111182902,
            "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.30000001192092896,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Neptune(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Neptune", "Override": None,
            "Name": "海王星", "Parent": None, "Type": 1, "Changed": False, "Extras": {},
            "Radius": 24622.0, "RadiusVisible": 0.164587975, "RotationPeriod": 0.67125,
            "RotationPhase": 0.0, "AxialTilt": 28.3, "Mass": 102.43, "OrbitType": 0,
            "OrbitEstimation": 0, "Density": 1.6382062699491229, "Gravity": 11.27643778556529,
            "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.28999999165534973,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Pluto(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Pluto", "Override": None,
            "Name": "冥王星", "Parent": None, "Type": 1, "Changed": False,
            "Extras": {}, "Radius": 1188.0, "RadiusVisible": 0.007941293,
            "RotationPeriod": 0.67125, "RotationPhase": 0.0, "AxialTilt": 122.5,
            "Mass": 0.01303, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 1.8552672808526236, "Gravity": 0.6161733964707342,
            "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.4000000059604645,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Sun(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Sun", "Override": None,
            "Name": "太阳", "Parent": None, "Type": 0, "Changed": False,
            "Extras": {}, "Radius": 696000.0, "RadiusVisible": 4.652475,
            "RotationPeriod": 24.47, "RotationPhase": 0.0, "AxialTilt": 0.0,
            "Mass": 1989100.0, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 1.408446287083086, "Gravity": 274.0498358435725,
            "Luminosity": 1.0, "Temperature": 5770.759689842919, "Albedo": 0.0,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Blue_Giant(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Blue Giant", "Override": None,
            "Name": "蓝巨星", "Parent": None, "Type": 0, "Changed": False,
            "Extras": {}, "Radius": 6357138.0, "RadiusVisible": 42.49486,
            "RotationPeriod": 0.0, "RotationPhase": 0.0, "AxialTilt": 0.0,
            "Mass": 10200942.0, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 0.009479092287635387, "Gravity": 16.84645041746542,
            "Luminosity": 427.6326424785209, "Temperature": 8683.093987009028,
            "Albedo": 0.0, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Red_Giant(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Red Giant", "Override": None,
            "Name": "红巨星", "Parent": None, "Type": 0, "Changed": False,
            "Extras": {}, "Radius": 105438592.0, "RadiusVisible": 704.8138,
            "RotationPeriod": 0.0, "RotationPhase": 0.0, "AxialTilt": 0.0,
            "Mass": 6961642.0, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 1.4178303979424782e-06, "Gravity": 0.04179303383227023,
            "Luminosity": 112.28474992545416, "Temperature": 1526.2230364017842,
            "Albedo": 0.0, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Red_Dwarf(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Red Dwarf", "Override": None,
            "Name": "红矮星", "Parent": None, "Type": 0, "Changed": False,
            "Extras": {}, "Radius": 273617.875, "RadiusVisible": 1.82902336,
            "RotationPeriod": 0.0, "RotationPhase": 0.0, "AxialTilt": 0.0,
            "Mass": 341202.5, "OrbitType": 0, "OrbitEstimation": 3,
            "Density": 3.976401218086238, "Gravity": 304.16881180896536,
            "Luminosity": 0.003987913104472093, "Temperature": 2312.873062778083,
            "Albedo": 0.0, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN",
            "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN",
            "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False
        }

class White_Dwarf(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "White Dwarf", "Override": None,
            "Name": "白矮星", "Parent": None, "Type": 0, "Changed": False,
            "Extras": {}, "Radius": 7973.126, "RadiusVisible": 0.05329708,
            "RotationPeriod": 0.0, "RotationPhase": 0.0, "AxialTilt": 0.0,
            "Mass": 781863.7, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 368261.70193835726, "Gravity": 820852.6402126513,
            "Luminosity": 0.02204848750849552, "Temperature": 20776.289920540155,
            "Albedo": 0.0, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Blackhole(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Blackhole", "Override": None,
            "Name": "黑洞", "Parent": None, "Type": -1, "Changed": False,
            "Extras": {}, "Radius": 3035.11, "RadiusVisible": 0.0202884674,
            "RotationPeriod": 0.0, "RotationPhase": 0.0, "AxialTilt": 0.0,
            "Mass": 2044842880.0, "OrbitType": 0, "OrbitEstimation": 0,
            "Density": 17460150441.37334, "Gravity": 14815027084.03691,
            "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.699999988079071,
            "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0,
            "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0,
            "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False
        }

class Fantasy_Star(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Fantasy Star", "Override": None,
            "Name": "幻想恒星", "Parent": None, "Type": 0, "Changed": False,
            "Extras": {}, "Radius": 651325.063, "RadiusVisible": 4.353841,
            "RotationPeriod": 0.0, "RotationPhase": 0.0, "AxialTilt": 0.0,
            "Mass": 2762263.0, "OrbitType": 0, "OrbitEstimation": 3,
            "Density": 2.3866187453169605, "Gravity": 434.5711132851481,
            "Luminosity": 3.719063854941033, "Temperature": 8284.134151462116,
            "Albedo": 0.0, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0,
            "Position": Generate, "Velocity": Generate, "Acceleration": Generate,
            "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN",
            "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN",
            "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False
        }

class Moon(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Moon", "Override": None, "Name": "月球", "Parent": None, "Type": 2, "Changed": False, "Extras": {}, "Radius": 1737.1, "RadiusVisible": 0.0116118016, "RotationPeriod": 27.3, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 0.073477, "OrbitType": 0, "OrbitEstimation": 3, "Density": 3.346481005246245, "Gravity": 1.625149040802321, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.12300000339746475, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Chocolate_Ball(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Chocolate Ball", "Override": None, "Name": "巧克力球", "Parent": None, "Type": 2, "Changed": False, "Extras": {}, "Radius": 60268.0, "RadiusVisible": 0.40286687, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 568.46, "OrbitType": 0, "OrbitEstimation": 3, "Density": 0.6199418849015184, "Gravity": 10.445224444042164, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.10000000149011612, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Continential(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Continential", "Override": None, "Name": "大陆行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 7789.734, "RadiusVisible": 0.0520711765, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 10.6000118, "OrbitType": 0, "OrbitEstimation": 0, "Density": 5.353648773443054, "Gravity": 11.658764094408177, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.2449134993567892, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": 0.0, "OmegaUC": 0.0, "OmegaLC": 0.0, "Inclination": 0.0, "Phase": 0.0, "PhaseCurrent": 0.0, "AxisSemi": 10.0, "Perihelion": 10.0, "Aphelion": 10.0, "LeavingKepler": False}

class Arctic(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Arctic", "Override": None, "Name": "封冻行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 6065.922, "RadiusVisible": 0.0405482, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 4.940184, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.28401556130987, "Gravity": 8.9606789613143, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.4125203241191535, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Arid(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Arid", "Override": None, "Name": "干旱行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 7835.934, "RadiusVisible": 0.0523800068, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 10.7674026, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.34256755968941, "Gravity": 11.703636214389228, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.12364274350842841, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Barren(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Barren", "Override": None, "Name": "贫瘠行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 4541.27246, "RadiusVisible": 0.030356545, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 2.03722143, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.192983592302659, "Gravity": 6.5928702184257375, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.10571566044065506, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Desert(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Desert", "Override": None, "Name": "沙漠行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 4934.40771, "RadiusVisible": 0.03298449, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 2.710787, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.386438443611148, "Gravity": 7.430477946170987, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.21723898875306347, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Jungle(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Jungle", "Override": None, "Name": "丛林行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 2861.00879, "RadiusVisible": 0.0191246718, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 0.5192027, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.2928643631051635, "Gravity": 4.233406517765326, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.10596970288294205, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Toxic(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Toxic", "Override": None, "Name": "剧毒行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 9783.194, "RadiusVisible": 0.0653966442, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 20.55713, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.241213470473673, "Gravity": 14.334829985641749, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.11500446600565795, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Lava(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Lava", "Override": None, "Name": "熔岩行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 5447.97, "RadiusVisible": 0.036417447, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 3.63040853, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.3599744007793495, "Gravity": 8.163519931681726, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.2376526732503912, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}

class Ocean(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {
            "Identifier": Generate, "Model": "Ocean", "Override": None, "Name": "海洋行星", "Parent": None, "Type": 1, "Changed": False, "Extras": {}, "Radius": 6777.314, "RadiusVisible": 0.0453035645, "RotationPeriod": 1.0, "RotationPhase": 0.0, "AxialTilt": 0.0, "Mass": 7.10958433, "OrbitType": 0, "OrbitEstimation": 3, "Density": 5.452338182781527, "Gravity": 10.330477777335007, "Luminosity": 0.0, "Temperature": 0.0, "Albedo": 0.2213094047766173, "PowerAbsorbtion": 0.0, "PlanetariumBalance": 0.0, "Position": Generate, "Velocity": Generate, "Acceleration": Generate, "Period": 0.0, "Eccentricity": "NaN", "OmegaUC": 0.0, "OmegaLC": "NaN", "Inclination": "NaN", "Phase": 0.0, "PhaseCurrent": "NaN", "AxisSemi": "NaN", "Perihelion": "NaN", "Aphelion": "NaN", "LeavingKepler": False}
