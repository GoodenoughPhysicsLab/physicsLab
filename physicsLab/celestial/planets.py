# -*- coding: utf-8 -*-
from physicsLab.savTemplate import Generate
from physicsLab.typehint import numType, Self
from ._planetbase import PlanetBase


class Mercury(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {'Identifier': Generate, 'Model': 'Mercury', 'Override': None,
                     'Name': '水星', 'Parent': None, 'Type': 1, 'Changed': False,
                     'Extras': {}, 'Radius': 2439.7, 'RadiusVisible': 0.00493933167,
                     'RotationPeriod': 58.646225, 'RotationPhase': 358.9865,
                     'AxialTilt': 0.034, 'Mass': 0.33022, 'OrbitType': 0,
                     'OrbitEstimation': 0, 'Density': 5.4288210902782295,
                     'Gravity': 3.7027293142758535, 'Luminosity': 0.0, 'Temperature': 0.0,
                     'Albedo': 0.11900000274181366, 'PowerAbsorbtion': 0.0,
                     'PlanetariumBalance': 0.0, 'Position': Generate, 'Velocity': Generate,
                     'Acceleration': Generate, 'Period': 0.0, 'Eccentricity': 0.0,
                     'OmegaUC': 0.0, 'OmegaLC': 0.0, 'Inclination': 0.0, 'Phase': 0.0,
                     'PhaseCurrent': 0.0, 'AxisSemi': 10.0, 'Perihelion': 10.0,
                     'Aphelion': 10.0, 'LeavingKepler': False}

class Venus(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {'Identifier': Generate, 'Model': 'Venus', 'Override': None,
                     'Name': '金星', 'Parent': None, 'Type': 1, 'Changed': False,
                     'Extras': {}, 'Radius': 6051.8, 'RadiusVisible': 0.007779331,
                     'RotationPeriod': -243.0187, 'RotationPhase': 0.0,
                     'AxialTilt': 177.4, 'Mass': 4.8676, 'OrbitType': 0,
                     'OrbitEstimation': 0, 'Density': 5.242912514272886,
                     'Gravity': 8.870276983364493, 'Luminosity': 0.0,
                     'Temperature': 0.0, 'Albedo': 0.75, 'PowerAbsorbtion': 0.0,
                     'PlanetariumBalance': 0.0, 'Position': Generate,
                     'Velocity': Generate, 'Acceleration': Generate,
                     'Period': 0.0, 'Eccentricity': 0.0, 'OmegaUC': 0.0,
                     'OmegaLC': 0.0, 'Inclination': 0.0, 'Phase': 0.0,
                     'PhaseCurrent': 0.0, 'AxisSemi': 10.0, 'Perihelion': 10.0,
                     'Aphelion': 10.0, 'LeavingKepler': False}

class Earth(PlanetBase):
    def __init__(self, x: numType, y: numType, z: numType) -> None:
        self.data = {'Identifier': Generate, 'Model': 'Earth', 'Override': None,
                     'Name': '地球', 'Parent': None, 'Type': 1, 'Changed': False,
                     'Extras': {}, 'Radius': 6378.0, 'RadiusVisible': 0.007986238,
                     'RotationPeriod': 0.9972697, 'RotationPhase': 0.0,
                     'AxialTilt': 23.44, 'Mass': 5.9722, 'OrbitType': 0,
                     'OrbitEstimation': 0, 'Density': 5.495309827118606,
                     'Gravity': 9.798434986805644, 'Luminosity': 0.0,
                     'Temperature': 0.0, 'Albedo': 0.28999999165534973,
                     'PowerAbsorbtion': 0.0, 'PlanetariumBalance': 0.0,
                     'Position': Generate, 'Velocity': Generate, 'Acceleration': Generate,
                     'Period': 0.0, 'Eccentricity': 0.0, 'OmegaUC': 0.0, 'OmegaLC': 0.0,
                     'Inclination': 0.0, 'Phase': 0.0, 'PhaseCurrent': 0.0,
                     'AxisSemi': 10.0, 'Perihelion': 10.0, 'Aphelion': 10.0,
                     'LeavingKepler': False}
