import pygame
import numpy as np

from ball import Ball
from utils import random_color, random_position


# Frames per second
FPS = 60

# Initialize pygame
pygame.init()

# Clock
clock = pygame.time.Clock()

# Set up the drawing window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_dim = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_dim)

# Generate balls
N_BALLS = 300
BALL_RADIUS = 7

balls = list()
ball_group = pygame.sprite.Group()

for i in range(N_BALLS):
    balls.append(Ball(
        BALL_RADIUS,
        random_position(screen_dim, BALL_RADIUS * 2),
        random_color(),
        screen_dim
    ))
    ball_group.add(balls[-1])


# Game loop
# Run until the user asks to quit
running = True

while running:

    # Look for exit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Get pressed keys
    pressed_keys = pygame.key.get_pressed()

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Update some ball
    for b in balls:
        b.update(pressed_keys)

    # Draw the player on the screen
    for b in balls:
        screen.blit(b.surf, b.rect)

    # Flip the display
    pygame.display.flip()

    # Ensure program maintains FPS
    clock.tick(FPS)

# Done! Time to quit
pygame.quit()
