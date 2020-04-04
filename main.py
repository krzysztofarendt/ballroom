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
N_BALLS = 400

ball_group = pygame.sprite.Group()

for i in range(N_BALLS):
    radius = np.random.randint(5, 10, 1)[0]
    b = Ball(
        radius,
        random_position(screen_dim, radius * 2),
        (0, 0, 255),
        screen_dim
    )
    ball_group.add(b)

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
        b.update(pressed_keys, ball_group, index)

    # Draw the ball on the screen
    for b in ball_group:
        screen.blit(b.surf, b.rect)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit
pygame.quit()
