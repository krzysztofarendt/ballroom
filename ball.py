from typing import Tuple
import pygame
import numpy as np


class Ball(pygame.sprite.Sprite):
    """Moving ball.

    Args:
        radius: radius in pixels
        center: initial position of the ball center
        color: fill color
        screen_dim: screen dimensions in pixels
    """
    colors = {
        'WHITE': (255, 255, 255)
    }

    def __init__(self,
                 radius: int,
                 center: Tuple[int, int],
                 color: Tuple[int, int, int],
                 screen_dim: Tuple[int, int]):

        super().__init__()
        self.screen_width = screen_dim[0]
        self.screen_height = screen_dim[1]

        # Make surface and draw circle
        self.surf = pygame.Surface((2 * radius, 2 * radius))
        self.surf.fill(Ball.colors['WHITE'])
        pygame.draw.circle(self.surf, color, (radius, radius), radius)

        # Transparent background
        self.surf.set_colorkey((255, 255, 255))

        # Rectangle and initial position
        self.rect = self.surf.get_rect()
        self.rect.move_ip(center[0], center[1])

        # velocity [dx, dy]
        self.velocity = np.array([0., 0.])

        # Acceleration due to key press
        self.dv = 0.33

        # Position buffer, used to handle sub-pixel movements
        # (i.e. moves below 1 pixel per frame)
        self.pos_buff = np.array([0., 0.])

    def update(self, pressed_keys):
        # Update velocity
        if pressed_keys[pygame.K_UP]:
            self.velocity[1] -= self.dv
        if pressed_keys[pygame.K_DOWN]:
            self.velocity[1] += self.dv
        if pressed_keys[pygame.K_LEFT]:
            self.velocity[0] -= self.dv
        if pressed_keys[pygame.K_RIGHT]:
            self.velocity[0] += self.dv

        # Increase position buffer
        self.pos_buff += self.velocity

        # Update position
        if (np.abs(self.pos_buff) >= 1).any():
            # Move only in whole pixels
            dxy = self.pos_buff.astype(int)
            self.rect.move_ip(dxy[0], dxy[1])
            # Update position buffer
            self.pos_buff -= dxy

        # Bounce off the screen boundaries
        if self.rect.left + self.velocity[0] < 0:
            self.velocity[0] *= -1
        elif self.rect.right + self.velocity[0] > self.screen_width:
            self.velocity[0] *= -1

        if self.rect.top + self.velocity[1] < 0:
            self.velocity[1] *= -1
        elif self.rect.bottom + self.velocity[1] > self.screen_height:
            self.velocity[1] *= -1

        # Keep ball on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
