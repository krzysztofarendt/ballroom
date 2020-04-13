from typing import Tuple

import pygame
import numpy as np

from .wall import Wall


class MovingWall(Wall):

    def __init__(self,
                 top: int = 0,
                 left: int = 0,
                 bottom: int = 1,
                 right: int = 1):
        super().__init__(top, left, bottom, right)

    def update(self, left, top, right, bottom):
        # Change size -> new surface
        width = right - left
        height = bottom - top
        self.surf = pygame.Surface((width, height)).convert_alpha()
        self.surf.fill((0, 255, 0, 90))

        # Mask used for collision detection
        self.mask = pygame.mask.from_surface(self.surf, 50)

        # Rectangle and initial position
        self.rect = self.surf.get_rect()

        # New rectangle to fit in
        new_rect = pygame.Rect(left, top, width, height)

        # Fit
        self.rect = self.rect.fit(new_rect)
