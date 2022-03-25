from __future__ import annotations
from abc import abstractmethod
from typing import Callable, Union
from queue import Queue

from app.board import Board
from app.tractor import Tractor
from app.fields import Clay, Sand, Plant, CROPS
from config import *


class Node:
    def __init__(self, parent: Union[Node, None], x: int, y: int,
                 direction: float, amount_of_harvested_crops: int,
                 movement: str, action: str):
        self.__x = x
        self.__y = y
        self.__parent = parent
        self.__direction = direction
        self.__movement = movement
        self.__action = action
        self.__amount_of_harvested_crops = amount_of_harvested_crops
        # self.__type_field = type_field

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def get_node(self) -> Node:
        return self.__parent

    def get_direction(self) -> float:
        return self.__direction

    def get_action(self) -> str:
        return self.__action

    def get_movement(self) -> str:
        return self.__movement

    def get_amount_of_harvested_crops(self) -> int:
        return self.__amount_of_harvested_crops

    def transform_node_to_tuple(self) -> tuple[int, int, float]:
        return self.__x, self.__y, self.__direction


class Graphsearch:
    @staticmethod
    def convert_queue_of_nodes_to_list(q: Queue[Node], *args) -> list:
        return [(i.get_x(), i.get_y(), i.get_direction(), *args) for i in q.queue]

    @staticmethod
    def succ(item: Node, board: Board) -> list:
        # list of tuples (movement,action),(x,y,direction, harvested_crops)
        actions = []
        x = item.get_x()
        y = item.get_y()
        current_harvested_crops = item.get_amount_of_harvested_crops()

        # do action ex. harvest:
        field = board.get_field(x, y)
        action_name = A_DO_NOTHING

        if isinstance(field, Clay):
            # fertilize
            action_name = A_FERTILIZE
            field = Tractor.fertilize_clay_succ(field, board, x, y)

        elif isinstance(field, Sand):
            # sow, letter hydrate
            action_name = A_SOW
            field = Tractor.sow_succ(field)
            field = Tractor.irrigate_sand_succ(field, board, x, y)
            # action_name = A_HYDRATE

        elif isinstance(field, Plant):
            # hydrate
            action_name = A_HYDRATE
            field = Tractor.irrigate_plants_succ(field, board, x, y)

        elif type(field).__name__ in CROPS:
            # harvest
            action_name = A_HARVEST
            field = Tractor.harvest_crops_succ(board, x, y)
            current_harvested_crops += 1
            # print(current_harvested_crops)

        # move
        current_direction = item.get_direction()

        tractor_move = Tractor.move_is_correct(x, y, current_direction)
        # print(f"res: {tractor_move}")
        if tractor_move is not None:
            pos_x, pos_y = tractor_move
            actions.append(((M_GO_FORWARD, action_name),
                            (pos_x, pos_y, current_direction, current_harvested_crops)))

        rotated_direction = (current_direction - 90.0) % 360.0
        actions.append(((M_ROTATE_LEFT, action_name), (x, y, rotated_direction, current_harvested_crops)))

        rotated_direction = (current_direction + 90.0) % 360.0
        actions.append(((M_ROTATE_RIGHT, action_name), (x, y, rotated_direction, current_harvested_crops)))

        return actions

    @staticmethod
    def goaltest(item: Node) -> bool:
        # print(item.get_amount_of_harvested_crops())
        if item.get_amount_of_harvested_crops() == AMOUNT_OF_CROPS:
            return True
        else:
            return False

    @staticmethod
    def get_all_moves(item: Node) -> list:
        moves = []
        str_moves = []
        while item.get_node() is not None:
            moves.append((item.get_movement(), item.get_action()))
            str_moves.append(
                f"{item.get_action()} - {item.get_movement()} - {item.get_x()}:{item.get_y()} {item.get_direction()}")
            item = item.get_node()
        print(str_moves[::-1])
        return moves[::-1]

    @staticmethod
    @abstractmethod
    def search(fringe: Queue, explored: Queue, istate: Node,
               succ: Callable[[Node, Board], list],
               goaltest: Callable[[Node], bool], board: Board) -> Union[bool, list]:
        raise NotImplementedError
