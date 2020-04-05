from typing import Tuple

import pygame
import numpy as np


class Wall(pygame.sprite.Sprite):
    """Stationary wall."""

    colors = {
        'WHITE': (255, 255, 255),
        'RED': (255, 0, 0),
        'GREEN': (0, 255, 0),
        'BLUE': (0, 0, 255),
        'BLACK': (0, 0, 0),
        'GRAY': (100, 100, 100)
    }

    def __init__(self,
                 top: int,
                 left: int,
                 bottom: int,
                 right: int):

        super().__init__()

        # Make surface and fill with color
        width = right - left
        height = bottom - top
        self.surf = pygame.Surface((width, height)).convert_alpha()
        self.surf.fill(Wall.colors['GRAY'])

        # Mask used for collision detection
        self.mask = pygame.mask.from_surface(self.surf)

        # Rectangle and initial position
        self.rect = self.surf.get_rect()
        self.rect.move_ip(top, left)

    def update(self):
        """This wall is static. The function is empty for now."""
        pass
