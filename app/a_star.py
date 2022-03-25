from __future__ import annotations

import copy
import math
from typing import Callable, Union
from queue import Queue, PriorityQueue

from app.board import Board
from config import *
from app.graphsearch import Node, Graphsearch


class PriorityItem:
    def __init__(self, node: Node, priority: float):
        self.node = node
        self.priority = priority

    def __lt__(self, other: PriorityItem):
        return self.priority < other.priority


class AStar(Graphsearch):
    @staticmethod
    def convert_queue_of_priority_items_to_list(q: Queue[PriorityItem], *args) -> list:
        return [(i.node.get_x(), i.node.get_y(), i.node.get_direction(), *args) for i in q.queue]

    @staticmethod
    def convert_queue_of_priority_items_with_priority_to_list(q: Queue[PriorityItem], *args) -> list:
        return [(i.node.get_x(), i.node.get_y(), i.node.get_direction(), i.priority, *args) for i in q.queue]

    @staticmethod
    def replace_node_in_fringe_queue(fringe: PriorityQueue[PriorityItem], state) -> None:
        tmp_queue = Queue()
        while not fringe.empty():
            item = fringe.get()

            if state == item.node.transform_node_to_tuple():
                break
            else:
                tmp_queue.put(item)

        while not tmp_queue.empty():
            fringe.put(tmp_queue.get())

    @staticmethod
    def replace_nodes(fringe: PriorityQueue[PriorityItem], priority: float, state: tuple[int, int, float]):
        fringe_items = AStar.convert_queue_of_priority_items_with_priority_to_list(fringe)
        for s in fringe_items:
            if s[:-1] == state[:-1]:
                if s[-1] > priority:
                    # s[-1] is priority (last element of state tuple)
                    # remove and add node to fringe - PriorityQueue
                    AStar.replace_node_in_fringe_queue(fringe, state[:-1])
                    break

    @staticmethod
    def g(board: Board, node: Node) -> float:
        """cost function"""
        result = 0
        while node.get_node() is not None:
            field = board.get_field(node.get_x(), node.get_y())
            result += field.get_value()
            node = node.get_node()
        return result

    @staticmethod
    def h(destination: tuple[int, int], node: Node) -> float:
        """heuristic function"""
        return round(math.sqrt(abs(destination[0] - node.get_x())**2 + abs(destination[0] - node.get_y())**2), 2)

    @staticmethod
    def f(board: Board, destination: tuple[int, int], node: Node) -> float:
        """evaluation function"""
        return AStar.g(board, node) + AStar.h(destination, node)

    @staticmethod
    def goaltest_by_coords(destination: tuple[int, int], item: Node) -> bool:
        # print(item)
        # print(destination)
        if destination[0] == item.get_x() and destination[1] == item.get_y():
            return True
        else:
            return False

    @staticmethod
    def search_solution(fringe: PriorityQueue, explored: Queue, destination: tuple[int, int], istate: Node,
               succ: Callable[[Node, Board], list],
               goaltest: Callable[[tuple[int, int], Node], bool], board: Board) -> Union[bool, list]:

        print(f"Start A*")
        fringe.put(PriorityItem(istate, 0))

        while True:
            if fringe.empty():
                return False

            item = fringe.get()
            if goaltest(destination, item.node):
                return AStar.get_all_moves(item.node)

            copied_item = copy.deepcopy(item)
            explored.put(item)

            for (action, state) in succ(copied_item.node, board):
                # print(state)
                fringe_items = AStar.convert_queue_of_priority_items_to_list(fringe)
                explored_items = AStar.convert_queue_of_priority_items_to_list(explored)

                n = Node(item.node, *state, *action)
                priority = AStar.f(board, destination, n)
                # print(priority)
                if state[:-1] not in fringe_items and state[:-1] not in explored_items:
                    fringe.put(PriorityItem(n, priority))
                elif state[:-1] in fringe_items:
                    AStar.replace_nodes(fringe, priority, state[:-1])
