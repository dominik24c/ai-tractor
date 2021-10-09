#!/usr/bin/python3
import copy
import json
import uuid

import pygame
import random

from app import Arg
from app.fields import *
from app.utils import get_class


class Board:
    def __init__(self, fields=None, args: list[Arg] = None):
        if fields is None:
            fields = []
        self.__fields = fields
        self.create_board()
        self.fill()
        self.generate_board()
        if args is not None:
            for arg in args:
                if arg.get_arg_name() == SAVE_MAP:
                    self.save_map()
                elif arg.get_arg_name() == LOAD_MAP:
                    self.load_map(arg.get_value())
        # print(self.__fields)

    def get_fields(self) -> list:
        return self.__fields

    def get_field(self, x: int, y: int) -> Field:
        return self.__fields[x][y]

    def create_board(self) -> None:
        for i in range(HORIZONTAL_NUM_OF_FIELDS):
            self.__fields.append([])
            for j in range(VERTICAL_NUM_OF_FIELDS):
                self.__fields[i].append(None)

    def fill(self) -> None:
        for i in range(len(self.__fields)):
            for j in range(len(self.__fields[i])):
                self.__fields[i][j] = random.choice(FIELD_TYPES).capitalize()

    def generate_board(self) -> None:
        for x in range(len(self.__fields)):
            for y in range(len(self.__fields[x])):
                field_type = self.__fields[x][y]
                c = get_class("app.fields", field_type)
                field = c()
                self.__fields[x][y] = field

    def draw(self, screen: pygame.Surface) -> None:
        for x in range(len(self.__fields)):
            for y in range(len(self.__fields[x])):
                field = self.__fields[x][y]
                pos_x = x * FIELD_SIZE
                pos_y = y * FIELD_SIZE
                field.draw_field(screen, pos_x, pos_y)

    def print_board(self) -> None:
        for i in range(HORIZONTAL_NUM_OF_FIELDS):
            for j in range(VERTICAL_NUM_OF_FIELDS):
                print(f"{j} - {type(self.__fields[i][j]).__name__}", end=" | ")
            print()

    def convert_fields_to_vectors(self) -> list[list]:
        list_of_vectors = []
        for i in range(HORIZONTAL_NUM_OF_FIELDS):
            list_of_vectors.append([])
            for j in range(VERTICAL_NUM_OF_FIELDS):
                list_of_vectors[i].append(self.__fields[i][j].transform())
        print(list_of_vectors)
        return list_of_vectors

    def convert_fields_to_list_of_types(self) -> list:
        data = []
        for i in range(HORIZONTAL_NUM_OF_FIELDS):
            data.append([])
            for j in range(VERTICAL_NUM_OF_FIELDS):
                data[i].append(type(self.__fields[i][j]).__name__)
        return data

    def convert_dict_map_to_list_map(self, dict_map: dict) -> list:
        list_map = []
        for col in dict_map.values():
            list_map.append(copy.copy(col))
        return list_map

    def load_map(self, filename: str):
        try:
            with open(os.path.join(MAP_DIR, f"{filename}.{JSON}")) as f:
                data = json.load(f)
        except IOError:
            raise IOError(f"Cannot load file: {filename}.{JSON}!")

        if data is None:
            raise Exception("Cannot load json file")

        size_flag = True
        # print(data)
        if len(data) != HORIZONTAL_NUM_OF_FIELDS:
            size_flag = False
        for fields in data:
            if len(fields) != VERTICAL_NUM_OF_FIELDS:
                size_flag = False
        if not size_flag:
            raise Exception('Cannot load map! Incorrect size of map')
        print("Map was successfully loaded!")

        # init map
        for x in range(len(data)):
            for y in range(len(data[x])):
                field_type = data[x][y]
                # print(field_type)
                c = get_class("app.fields", field_type)
                self.__fields[x][y] = c()
        print("Map was successfully initialized!")

    def save_map(self) -> None:
        if len(self.__fields) == 0:
            raise Exception('Board is not initialized!')

        fields = self.convert_fields_to_list_of_types()

        try:
            with open(os.path.join(MAP_DIR, f"{MAP_FILE_NAME}-{uuid.uuid4().hex}.{JSON}"), 'w') as f:
                json.dump(fields, f)
        except IOError:
            raise IOError(f"Cannot save file:!")
