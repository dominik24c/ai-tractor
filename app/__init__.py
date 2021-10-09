#!/usr/bin/python3
import copy
import random
from queue import Queue, PriorityQueue
from threading import Event

import pygame

from config import *
from app.cmd_parser import Arg
from app.graphsearch import Node
from app.board import Board
from app.tractor import Tractor
from app.a_star import AStar
from app.bfs import Bfs


class App:
    def __init__(self, args: list[Arg]):
        self.__running = True
        self.__screen = None
        self.__clock = None
        self.__board = Board(args=args)
        self.__tractor = Tractor(self.__board)
        self.__bot_is_running = Event()
        self.__moves = None
        self.__auto_mode = self.get_auto_mode_arg(args)

    def get_auto_mode_arg(self, args: list[Arg]):
        for arg in args:
            if arg.get_arg_name() == AUTO_MODE:
                return True
        return False

    def initialize(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.__clock = pygame.time.Clock()

    def event_handler(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.__running = False

    def loop_handler(self):
        self.__board.draw(self.__screen)
        self.__tractor.draw(self.__screen)

    def keys_pressed_handler(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.__tractor.move()
            print(self.__tractor)

        if keys[pygame.K_n]:
            self.__bot_is_running.set()
            self.__tractor.harvest_checked_fields_handler(self.__bot_is_running)

        if keys[pygame.K_h]:
            self.__tractor.harvest()

        if keys[pygame.K_v]:
            self.__tractor.sow()

        if keys[pygame.K_j]:
            self.__tractor.hydrate()

        if keys[pygame.K_f]:
            self.__tractor.fertilize()

        if keys[pygame.K_l]:
            self.__tractor.rotate_left()

        if keys[pygame.K_r]:
            self.__tractor.rotate_right()

        if keys[pygame.K_b]:
            self.get_moves_by_bfs()
            if not self.__moves:
                print(f"Bfs is failed")
            else:
                print(f"Bfs is succeed")
                self.__bot_is_running.set()
                self.__tractor.run_bot_handler(self.__moves, self.__bot_is_running)

        if keys[pygame.K_c]:
            self.get_moves_by_a_star_with_random_coords()
            if not self.__moves:
                print(f"A Star is failed")
            else:
                print(f"A Star is succeed")
                self.__bot_is_running.set()
                self.__tractor.run_bot_handler(self.__moves, self.__bot_is_running)

        if keys[pygame.K_a]:
            self.auto_moving_mode()

    def update_screen(self) -> None:
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()

    def auto_moving_mode(self):
        coords, action = self.get_coords_and_action()
        x, y = self.__tractor.get_position()
        if coords is not None:
            x1, y1 = coords
        else:
            x1, y1 = None, None
        print(action, coords)
        if action != A_DO_NOTHING and x1 == x and y == y1:
            self.__tractor.do_action_on_fields(action)
        elif action == A_DO_NOTHING:
            print(action)
        elif not self.__moves:
            print(f"A Star is failed")
        else:
            print(f"A Star is succeed")
            self.__bot_is_running.set()
            self.__tractor.run_auto_bot_handler(action, self.__moves, self.__bot_is_running)

    def get_coords_and_action(self) -> tuple[tuple[int, int], str]:
        coords, action = self.__tractor.choose_action()
        if coords is not None:
            self.get_moves_by_a_star(coords)
        else:
            self.__moves = None
        return coords, action[0]

    def get_moves_by_a_star_with_random_coords(self) -> None:
        x1 = random.randint(0, HORIZONTAL_NUM_OF_FIELDS)
        y1 = random.randint(0, VERTICAL_NUM_OF_FIELDS)
        dest = (x1, y1)
        self.get_moves_by_a_star(dest)

    def get_moves_by_a_star(self, coords: tuple[int, int]) -> None:
        x, y = self.__tractor.get_position()
        node = Node(None, x, y, self.__tractor.get_direction(), 0, "movement", "initial state")
        board = copy.deepcopy(self.__board)
        self.__moves = AStar.search_solution(PriorityQueue(), Queue(), coords, node,
                                             lambda n=node, b=board: AStar.succ(n, b),
                                             lambda d=coords, n=node: AStar.goaltest_by_coords(d, n), board)

    def get_moves_by_bfs(self) -> None:
        x, y = self.__tractor.get_position()
        node = Node(None, x, y, self.__tractor.get_direction(), 0, "movement", "initial state")
        board = copy.deepcopy(self.__board)
        self.__moves = Bfs.search(Queue(), Queue(), node,
                                  lambda n=node, b=board: Bfs.succ(n, b),
                                  lambda n=node: Bfs.goaltest(n), board)

    def run(self) -> None:
        self.initialize()

        while self.__running:
            self.__clock.tick(FPS)

            for event in pygame.event.get():
                self.event_handler(event)

            if not self.__bot_is_running.is_set() and not self.__auto_mode:
                self.keys_pressed_handler()
            if not self.__bot_is_running.is_set() and self.__auto_mode:
                self.auto_moving_mode()

            self.loop_handler()
            self.update_screen()

        self.quit()
