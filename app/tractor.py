#!/usr/bin/python3
from __future__ import annotations
import random
import threading

import pygame
import os
import time
from threading import Thread
from typing import Union

from app.base_field import BaseField
from app.board import Board
from app.neural_network import NeuralNetwork
from app.utils import get_class
from app.fields import CROPS, PLANTS, Crops, Sand, Clay, Field
from config import *

from app.fields import Plant, Soil, Crops
from app.decision_tree import DecisionTree
from app.weather import Weather


class Tractor(BaseField):
    def __init__(self, board: Board):
        super().__init__(os.path.join(RESOURCE_DIR, f"{TRACTOR}.{PNG}"))
        self.__pos_x = (int(HORIZONTAL_NUM_OF_FIELDS / 2) - 1) * FIELD_SIZE
        self.__pos_y = (int(VERTICAL_NUM_OF_FIELDS / 2) - 1) * FIELD_SIZE
        self.__direction = 0.0
        self.__move = FIELD_SIZE
        self.__board = board
        self.__harvested_corps = []
        self.__fuel = 10
        self.__neural_network = NeuralNetwork()
        self.__tree = DecisionTree()
        self.__weather = Weather()

    def draw(self, screen: pygame.Surface) -> None:
        self.draw_field(screen, self.__pos_x + FIELD_SIZE / 2, self.__pos_y + FIELD_SIZE / 2,
                        is_centered=True, size=(FIELD_SIZE, FIELD_SIZE), angle=self.__direction)

    #  Key methods handlers
    def move(self) -> None:
        if self.__direction == D_EAST:
            self.move_right()
        elif self.__direction == D_NORTH:
            self.move_up()
        elif self.__direction == D_WEST:
            self.move_left()
        else:
            self.move_down()

    def move_up(self) -> None:
        if self.__pos_y - self.__move >= 0:
            self.__pos_y -= self.__move

    def move_down(self) -> None:
        if self.__pos_y + self.__move + FIELD_SIZE <= HEIGHT:
            self.__pos_y += self.__move

    def move_left(self) -> None:
        if self.__pos_x - self.__move >= 0:
            self.__pos_x -= self.__move

    def move_right(self) -> None:
        if self.__pos_x + self.__move + FIELD_SIZE <= WIDTH:
            self.__pos_x += self.__move

    def rotate_left(self) -> None:
        self.__direction = (self.__direction - 90.0) % 360.0

    def rotate_right(self) -> None:
        self.__direction = (self.__direction + 90.0) % 360.0

    def hydrate(self) -> None:
        if self.check_field(Sand):
            field = self.get_field_from_board()
            if not field.is_hydrated and field.is_sowed:
                print('Hydrate soil')
                self.irrigate_sand(field)
        elif self.check_field(Plant):
            field = self.get_field_from_board()
            if not field.is_hydrated:
                print("Hydrate plant")
                self.irrigate_plants(field)

    def hydrate_sand(self) -> None:
        if self.check_field(Sand):
            field = self.get_field_from_board()
            if not field.is_hydrated and field.is_sowed:
                print('Hydrate soil')
                self.irrigate_sand(field)

    def hydrate_plant(self) -> None:
        if self.check_field(Plant):
            field = self.get_field_from_board()
            if not field.is_hydrated:
                print("Hydrate plant")
                self.irrigate_plants(field)

    def sow(self) -> None:
        field = self.get_field_from_board()
        if self.check_field(Sand) and not field.is_sowed:
            print('Sow')
            field.is_sowed = True

    def harvest(self) -> None:
        field = self.get_field_from_board()
        prediction = self.__neural_network.check(field)

        if prediction.capitalize() in CROPS:
            print('Harvest')
            field = self.get_field_from_board()
            self.harvest_crops(field)
            self.get_result_of_harvesting()

    def fertilize(self) -> None:
        if self.check_field(Clay):
            print('Fertilize soil')
            field = self.get_field_from_board()
            self.fertilize_clay(field)

    ################################################################################

    def fertilize_clay(self, field: Clay) -> None:
        field.is_fertilized = True
        self.do_action((Sand.__name__,))

    def irrigate_plants(self, field: Plant) -> None:
        field.is_hydrated = True
        # self.do_time_action(CROPS)
        self.do_action(CROPS)

    def irrigate_sand(self, field: Sand) -> None:
        field.is_hydrated = True
        # self.do_time_action(PLANTS)
        self.do_action(PLANTS)

    def harvest_crops(self, field: Crops) -> None:
        self.__harvested_corps.append(type(field).__name__)
        self.do_action((Clay.__name__,))

    def do_action(self, TYPE: tuple) -> None:
        choosen_type = random.choice(TYPE)
        obj = get_class("app.fields", choosen_type)
        x, y = self.get_position()
        self.__board.get_fields()[x][y] = obj()

    def do_time_action(self, TYPE: tuple) -> None:
        thread = Thread(target=self.do_time_action_handler, args=(TYPE,), daemon=True)
        thread.start()

    def do_time_action_handler(self, TYPE: tuple) -> None:
        time.sleep(TIME_OF_GROWING)
        self.do_action(TYPE)

    def check_field(self, class_name: Union[type(Plant), type(Crops), type(Soil)]) -> bool:
        if isinstance(self.get_field_from_board(), class_name):
            return True
        return False

    def get_field_from_board(self) -> BaseField:
        x, y = self.get_position()
        return self.__board.get_fields()[x][y]

    def get_field_from_board_by_positions(self, x, y) -> BaseField:
        return self.__board.get_fields()[x][y]

    def get_position(self) -> tuple[int, int]:
        x = self.__pos_x // FIELD_SIZE
        y = self.__pos_y // FIELD_SIZE
        return x, y

    def get_result_of_harvesting(self) -> None:
        crops = set(self.__harvested_corps)
        result = 0.0
        for crop in crops:
            amount = self.__harvested_corps.count(crop)
            print(f"{amount} x {crop}")
            result += amount * get_class("app.fields", crop).price

        print(f"Price for collected crops: {result:.2f}")

    def __str__(self) -> str:
        x, y = self.get_position()
        return f"Position: {x}:{y} - {type(self.__board.get_fields()[x][y]).__name__}"

    def get_direction(self) -> float:
        return self.__direction

    def run_bot_handler(self, moves: list[tuple[str, str]], is_running: threading.Event) -> None:
        thread = threading.Thread(target=self.run_bot, args=(moves, is_running), daemon=True)
        thread.start()

    def run_bot(self, moves: list[tuple[str, str]], is_running: threading.Event) -> None:
        print(moves)
        print(f"Length of Moves {len(moves)}")  # - {3 ** len(moves)}")
        while len(moves) > 0:
            movement, action = moves.pop(0)

            # do action
            time.sleep(0.5)
            self.do_action_on_fields(action)

            # move
            time.sleep(1)
            self.move_or_rotate(movement)

            time.sleep(TIME_OF_MOVING)
        is_running.clear()

    def do_action_on_fields(self, action: str) -> None:
        print(f"Action {action}")
        if action == A_FERTILIZE:
            self.fertilize()
        elif action == A_SOW:
            self.sow()
            # self.hydrate()
        elif action == A_HYDRATE:
            self.hydrate()
        elif action == A_HARVEST:
            self.harvest()

    def run_auto_bot_handler(self, action: str, moves: list[tuple[str, str]], is_running: threading.Event) -> None:
        thread = threading.Thread(target=self.run_auto_bot, args=(action, moves, is_running), daemon=True)
        thread.start()

    def run_auto_bot(self, action_type: str, moves: list[tuple[str, str]], is_running: threading.Event) -> None:
        print(moves)
        # print('Auto mode')
        while len(moves) > 0:
            movement, action = moves.pop(0)
            # move
            self.move_or_rotate(movement)
            time.sleep(0.7)

        self.do_action_on_fields(action_type)
        time.sleep(1)
        is_running.clear()

    def move_or_rotate(self, movement: str) -> None:
        print(f"Move {movement}")
        if movement == M_GO_FORWARD:
            self.move()
        elif movement == M_ROTATE_LEFT:
            self.rotate_left()
        elif movement == M_ROTATE_RIGHT:
            self.rotate_right()

    @staticmethod
    def move_is_correct(x: int, y: int, direction: float) -> Union[(int, int), None]:
        pos_x = x * FIELD_SIZE
        pos_y = y * FIELD_SIZE

        if direction == D_NORTH and pos_y - FIELD_SIZE >= 0:
            return x, y - 1
        if direction == D_SOUTH and pos_y + 2 * FIELD_SIZE <= HEIGHT:
            return x, y + 1
        if direction == D_WEST and pos_x - FIELD_SIZE >= 0:
            return x - 1, y
        if direction == D_EAST and pos_x + 2 * FIELD_SIZE <= WIDTH:
            return x + 1, y

        return None

    @staticmethod
    def fertilize_clay_succ(field: Clay, board: Board, x: int, y: int) -> Sand:
        field.is_fertilized = True
        return Tractor.do_action_succ(board, x, y, (Sand.__name__,))

    @staticmethod
    def sow_succ(field: Sand) -> Sand:
        field.is_sowed = True
        return field

    @staticmethod
    def irrigate_plants_succ(field: Plant, board: Board, x: int, y: int) -> Crops:
        field.is_hydrated = True
        return Tractor.do_action_succ(board, x, y, CROPS)

    @staticmethod
    def irrigate_sand_succ(field: Sand, board: Board, x: int, y: int) -> Plant:
        field.is_hydrated = True
        return Tractor.do_action_succ(board, x, y, PLANTS)

    @staticmethod
    def harvest_crops_succ(board: Board, x: int, y: int) -> Clay:
        # Tractor.__harvested_corps.append(type(field).__name__)
        return Tractor.do_action_succ(board, x, y, (Clay.__name__,))

    @staticmethod
    def do_action_succ(board: Board, x: int, y: int, types: tuple) -> Union[Sand, Clay, Plant, Crops]:
        choosen_type = random.choice(types)
        obj = get_class("app.fields", choosen_type)
        board.get_fields()[x][y] = obj()
        return obj()

    def harvest_checked_fields_handler(self, is_running: threading.Event) -> None:
        thread = threading.Thread(target=self.harvest_checked_fields, args=(is_running,), daemon=True)
        thread.start()

    def go_forward_is_legal_move(self) -> bool:
        flag = False
        if (self.__direction == D_EAST and self.__pos_y - self.__move >= 0) or \
                (self.__direction == D_NORTH and self.__pos_y + self.__move + FIELD_SIZE <= HEIGHT) or \
                (self.__direction == D_WEST and self.__pos_x - self.__move >= 0) or \
                (self.__direction == D_SOUTH and self.__pos_x + self.__move + FIELD_SIZE <= WIDTH):
            flag = True

        return flag

    def harvest_checked_fields(self, is_running: threading.Event) -> None:
        while True:
            moves = [M_GO_FORWARD, M_ROTATE_LEFT, M_ROTATE_RIGHT]
            distribution = [0.6, 0.2, 0.2]

            field = self.get_field_from_board()

            self.__neural_network = NeuralNetwork()
            prediction = self.__neural_network.check(field)

            if prediction.capitalize() in CROPS:
                self.harvest()
                break

            if not self.go_forward_is_legal_move():
                moves = moves[1:]
                distribution = distribution[1:]

            chosen_move = random.choices(moves, distribution)
            self.move_or_rotate(chosen_move[0])
            time.sleep(1)

        is_running.clear()

    def choose_action(self) -> tuple[tuple[int, int], str]:
        vectors = self.__board.convert_fields_to_vectors()
        print(vectors)
        coords = None
        action = None

        i_max = HORIZONTAL_NUM_OF_FIELDS
        j_max = VERTICAL_NUM_OF_FIELDS

        i_min = random.randint(0, HORIZONTAL_NUM_OF_FIELDS - 1)
        j_min = random.randint(0, VERTICAL_NUM_OF_FIELDS - 1)

        i = i_min
        flag = True
        while i < i_max and flag:
            for j in range(j_min, j_max):
                action = self.__tree.make_decision(self.__weather, vectors[i][j])
                if action != A_DO_NOTHING:
                    coords = (i, j)
                    flag = False
                    break
            i += 1
        print(coords, action)
        return coords, action
