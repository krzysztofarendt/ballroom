from typing import Tuple

import pygame
import numpy as np

from collisions import ball_elastic_collision


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

        # Physical properties
        self.radius = radius
        self.area = np.pi * self.radius ** 2
        self.mass = self.area

        # Make surface and draw circle
        self.surf = pygame.Surface((2 * self.radius, 2 * self.radius))
        self.surf.fill(Ball.colors['WHITE'])
        pygame.draw.circle(self.surf, color, (self.radius, self.radius), self.radius)

        # Transparent background
        self.surf.set_colorkey((255, 255, 255))

        # Rectangle and initial position
        self.rect = self.surf.get_rect()
        self.rect.move_ip(center[0], center[1])

        # Velocity [dx, dy]
        self.velocity = np.array([0., 0.])

        # Momentum
        self.momentum = self.mass * self.velocity

        # Acceleration due to key press
        self.dv = 0.33

        # Position buffer, used to handle sub-pixel movements
        # (i.e. moves below 1 pixel per frame)
        self.pos_buff = np.array([0., 0.])

    def update(self,
               pressed_keys: tuple,
               group: pygame.sprite.Group,
               index: int) -> None:
        """Update sprite.

        Args:
            pressed_keys: tuple returned by pygame.key.get_pressed()
            group: reference to sprite.Group containing this sprite
            index: current's ball index in the group

        Return:
            None
        """
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

        # Find potential rectangle-like collisions (fast search)
        all_balls = group.sprites()
        overlapping = self.rect.collidelistall(all_balls)
        overlapping = [x for x in overlapping if x != index]

        # Confirm circle-like collisions (slow search)
        for j in overlapping:
            collision = pygame.sprite.collide_circle(all_balls[index], all_balls[j])

            if collision:
                # Bounce off both balls
                other = all_balls[j]

                # Conservation of momentum
                ux1 = self.velocity[0]
                ux2 = other.velocity[0]
                uy1 = self.velocity[1]
                uy2 = other.velocity[1]
                m1 = self.mass
                m2 = other.mass
                x1 = self.rect.centerx
                x2 = other.rect.centerx
                y1 = self.rect.centery
                y2 = other.rect.centery
                vx1, vy1, vx2, vy2 = ball_elastic_collision(
                    ux1, uy1, ux2, uy2, m1, m2, x1, y1, x2, y2
                )

                self.velocity = np.array([vx1, vy1])
                other.velocity = np.array([vx2, vy2])

                # Position correction (if overlap exists)
                distance = np.sqrt(
                    (self.rect.centerx - other.rect.centerx) ** 2 + \
                    (self.rect.centery - other.rect.centery) ** 2
                )
                if distance < 1e-3:
                    # Do not allow zero-distance
                    distance = 1e-3
                overlap = self.radius + other.radius - distance
                dist_x = self.rect.centerx - other.rect.centerx
                dist_y = self.rect.centery - other.rect.centery
                sin_alpha = dist_y / distance
                cos_alpha = dist_x / distance
                dx = int((overlap + 0.5) * cos_alpha)
                dy = int((overlap + 0.5) * sin_alpha)

                self.rect.move_ip(dx, dy)
                other.rect.move_ip(-dx, -dy)

        # Keep ball on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
