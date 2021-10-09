import copy
from queue import Queue
from typing import Callable, Union

from app import Board
from app.graphsearch import Graphsearch, Node


class Bfs(Graphsearch):

    @staticmethod
    def search(fringe: Queue, explored: Queue, istate: Node,
               succ: Callable[[Node, Board], list],
               goaltest: Callable[[Node], bool], board: Board) -> Union[bool, list]:

        print(f"Start bfs")
        fringe.put(istate)

        while True:
            if fringe.empty():
                # print(list(explored.queue))
                # return Graphsearch.get_all_moves(explored.get())
                return False

            item = fringe.get()

            if goaltest(item):
                # board.print_board()
                return Graphsearch.get_all_moves(item)

            copied_item = copy.deepcopy(item)
            explored.put(item)

            for (action, state) in succ(copied_item, board):
                # print(state)
                fringe_items = []
                explored_items = []
                [fringe_items.append((i.get_x(), i.get_y(), i.get_direction()))
                 for i in fringe.queue]
                [explored_items.append((i.get_x(), i.get_y(), i.get_direction()))
                 for i in explored.queue]
                if state[:-1] not in fringe_items and state[:-1] not in explored_items:
                    n = Node(item, *state, *action)
                    fringe.put(n)
