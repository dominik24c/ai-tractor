#!/usr/bin/python3
import os

from app.base_field import BaseField
from config import *


class Field(BaseField):
    def __init__(self, img_path: str):
        super().__init__(img_path)
        self._value = 0

    def get_value(self) -> int:
        return self._value


class Soil(Field):
    def __init__(self, img_path: str):
        super().__init__(img_path)


class Crops(Field):
    price = 0

    def __init__(self, img_path: str):
        super().__init__(img_path)
        self.weight = 1.0
        self._value = VALUE_OF_CROPS

    def transform(self) -> list:
        return [0, 0, 0, 1]


class Plant(Field):
    def __init__(self, img_path: str):
        super().__init__(img_path)
        self.is_hydrated = False
        self._value = VALUE_OF_PLANT

    def transform(self) -> list:
        return [0, 1, 0, 0]


class Clay(Soil):
    def __init__(self):
        super().__init__(os.path.join(RESOURCE_DIR, f"{CLAY}.{PNG}"))
        self.is_fertilized = False
        self._value = VALUE_OF_CLAY

    def transform(self) -> list:
        return [1, 0, 0, 0]


class Sand(Soil):
    def __init__(self):
        super().__init__(os.path.join(RESOURCE_DIR, f"{SAND}.{PNG}"))
        self.is_sowed = False
        self.is_hydrated = False
        self._value = VALUE_OF_SAND

    def transform(self) -> list:
        if not self.is_sowed :
            return [0, 0, 1, 0]
        else:
            return [0, 1, 0, 0]


class Grass(Plant):
    def __init__(self):
        super().__init__(os.path.join(RESOURCE_DIR, f"{GRASS}.{PNG}"))


class Sunflower(Crops):
    price = 7.90

    def __init__(self):
        super().__init__(os.path.join(RESOURCE_DIR, f"{SUNFLOWER}.{PNG}"))


class Corn(Crops):
    price = 9.15

    def __init__(self):
        super().__init__(os.path.join(RESOURCE_DIR, f"{CORN}.{PNG}"))


CROPS = (Sunflower.__name__, Corn.__name__)
PLANTS = (Grass.__name__,)
SOILS = (Clay.__name__, Sand.__name__)
