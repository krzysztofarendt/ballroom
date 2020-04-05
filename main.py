import pygame
import numpy as np

from ball import Ball
from wall import Wall
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
N_BALLS = 1
ball_group = pygame.sprite.Group()

for i in range(N_BALLS):
    # radius = np.random.randint(20, 20, 1)[0]
    radius = 20
    b = Ball(
        radius,
        random_position(screen_dim, radius * 2),
        (0, 0, 255),
        screen_dim
    )
    ball_group.add(b)

# Generate walls
wall0 = Wall(100, 100, 200, 200)

wall_group = pygame.sprite.Group()
wall_group.add(wall0)

# Game loop
# Run until the user asks to quit
running = True

while running:

    # Ensure program maintains FPS
    clock.tick(FPS)

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

    # Update all balls
    for index, b in enumerate(ball_group):
        b.update(pressed_keys, ball_group, index, wall_group)

    # Draw balls on the screen
    for b in ball_group:
        screen.blit(b.surf, b.rect)

    # Draw walls on the screen
    for w in wall_group:
        screen.blit(w.surf, w.rect)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit
pygame.quit()
