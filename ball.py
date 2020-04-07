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
        dissipation: dissipation of energy at each bounce (default 0)
    """
    colors = {
        'WHITE': (255, 255, 255)
    }

    def __init__(self,
                 radius: int,
                 center: Tuple[int, int],
                 color: Tuple[int, int, int],
                 screen_dim: Tuple[int, int],
                 dissipation: float = 0.):

        super().__init__()
        self.screen_width = screen_dim[0]
        self.screen_height = screen_dim[1]

        # Physical properties
        self.radius = radius
        self.area = np.pi * self.radius ** 2
        self.mass = self.area
        self.dissipation = dissipation

        # Make surface and draw circle
        self.surf = pygame.Surface((2 * self.radius, 2 * self.radius))
        self.surf.fill(Ball.colors['WHITE'])
        pygame.draw.circle(self.surf, color, (self.radius, self.radius), self.radius)

        # Transparent background
        self.surf.set_colorkey(Ball.colors['WHITE'])

        # Mask used for collision detection
        self.mask = pygame.mask.from_surface(self.surf)

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
               ball_group: pygame.sprite.Group,
               index: int,
               wall_group: pygame.sprite.Group) -> None:
        """Update sprite.

        Args:
            pressed_keys: tuple returned by pygame.key.get_pressed()
            ball_group: reference to sprite.Group containing this sprite
            index: current's ball index in the ball_group
            wall_group: reference to sprite.Group containing the walls

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
            self.velocity[0] *= -1 * (1 - self.dissipation)
        elif self.rect.right + self.velocity[0] > self.screen_width:
            self.velocity[0] *= -1 * (1 - self.dissipation)

        if self.rect.top + self.velocity[1] < 0:
            self.velocity[1] *= -1 * (1 - self.dissipation)
        elif self.rect.bottom + self.velocity[1] > self.screen_height:
            self.velocity[1] *= -1 * (1 - self.dissipation)

        # Find potential rectangle-like collisions (fast search)
        all_balls = ball_group.sprites()
        overlapping = self.rect.collidelistall(all_balls)
        overlapping = [x for x in overlapping if x != index]

        # Confirm circle-like collisions (slow search)
        for j in overlapping:
            collision = pygame.sprite.collide_circle(all_balls[index], all_balls[j])

            if collision:
                # Bounce off both balls
                other = all_balls[j]

                # Conservation of momentum
                u1 = self.velocity
                u2 = other.velocity
                m1 = self.mass
                m2 = other.mass
                c1 = np.array([self.rect.centerx, self.rect.centery])
                c2 = np.array([other.rect.centerx, other.rect.centery])

                v1, v2 = ball_elastic_collision(
                    u1, u2, m1, m2, c1, c2, self.dissipation)

                self.velocity = v1
                other.velocity = v2

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

        # Check wall collision
        all_walls = wall_group.sprites()
        w = self.rect.collidelist(all_walls)

        if w >=0:
            # Bounce off the wall
            wall = all_walls[w]
            wall_point = pygame.sprite.collide_mask(self, wall)

            if wall_point is not None:
                wall_point = (
                    wall_point[0] + self.rect.left,
                    wall_point[1] + self.rect.top
                )

                # Position and velocity correction
                # Which side of the wall was hit?
                dist_l = abs(wall.rect.left - wall_point[0])
                dist_t = abs(wall.rect.top - wall_point[1])
                dist_r = abs(wall.rect.right - wall_point[0])
                dist_b = abs(wall.rect.bottom - wall_point[1])

                side_list = np.array(['left', 'top', 'right', 'bottom'])
                dist_all = np.array([dist_l, dist_t, dist_r, dist_b])
                order = np.argsort(dist_all)
                side_hit = side_list[order[0]]

                # Corner hit?
                corner_name = side_list[order[0:2]]
                corner_xy = np.zeros(2)
                if 'left' in corner_name:
                    corner_xy[0] = wall.rect.left
                else:
                    corner_xy[0] = wall.rect.right

                if 'top' in corner_name:
                    corner_xy[1] = wall.rect.top
                else:
                    corner_xy[1] = wall.rect.bottom

                ## The below code detects if the ball hits the corner of the wall.
                ## It might be usefull in the future.
                # if abs(corner_xy[0] - self.rect.centerx) < self.radius \
                #     and abs(corner_xy[1] - self.rect.centery) < self.radius:
                #     corner_hit = True
                # else:
                #     corner_hit = False

                dx, dy = 0, 0

                if side_hit == 'left':
                    # Move ball right
                    self.velocity[0] *= -1 * (1 - self.dissipation)
                    dx = wall_point[0] - self.rect.right - 2
                    dy = 0
                elif side_hit == 'top':
                    # Move ball up
                    self.velocity[1] *= -1 * (1 - self.dissipation)
                    dx = 0
                    dy = wall_point[1] - self.rect.bottom - 2
                elif side_hit == 'right':
                    # Move ball left
                    self.velocity[0] *= -1 * (1 - self.dissipation)
                    dx = wall_point[0] - self.rect.left + 2
                    dy = 0
                elif side_hit == 'bottom':
                    # Move ball down
                    self.velocity[1] *= -1 * (1 - self.dissipation)
                    dx = 0
                    dy = wall_point[1] - self.rect.top + 2

                self.rect.move_ip(dx, dy)

        # Keep ball on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
