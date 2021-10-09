import pygame

from config import *


class BaseField:
    def __init__(self, img_path: str):
        self._img_path = img_path

    def get_img_path(self):
        return self._img_path

    def draw_field(self, screen: pygame.Surface, pos_x: int,
                   pos_y: int, is_centered: bool = False,
                   size: tuple = None, angle: float = 0.0) -> None:
        img = pygame.image.load(self._img_path)
        img = pygame.transform.rotate(img, angle)

        scale = pygame.transform.scale(img, (FIELD_SIZE, FIELD_SIZE))
        rect = img.get_rect()

        if is_centered:
            rect.center = (pos_x, pos_y)
        else:
            rect.topleft = (pos_x, pos_y)

        if size is not None:
            rect.size = (FIELD_SIZE, FIELD_SIZE)

        screen.blit(scale, rect)
