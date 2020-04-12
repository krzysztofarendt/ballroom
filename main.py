import pygame
import numpy as np
import cv2

from camera import Camera
from ball import Ball
from wall import Wall
from utils import random_color, random_position
from config import CONFIG


if __name__ == "__main__":
    # Frames per second
    fps = CONFIG['fps']

    # Initialize pygame
    pygame.init()

    # Clock
    clock = pygame.time.Clock()

    # Set up the drawing window
    screen_width = CONFIG['screen_width']
    screen_height = CONFIG['screen_height']
    screen_dim = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_dim)

    # Initialize camera
    cam = Camera(screen_width, screen_height)

    # Generate balls
    n_balls = CONFIG['n_balls']
    ball_group = pygame.sprite.Group()

    for i in range(n_balls):
        # radius = np.random.randint(20, 20, 1)[0]
        radius = 10
        b = Ball(
            radius,
            random_position(screen_dim, radius * 2),
            (0, 0, 255),
            screen_dim,
            CONFIG['dissipation']
        )
        ball_group.add(b)

    # Generate walls
    wall0 = Wall(200, 200, 300, 300)

    wall_group = pygame.sprite.Group()
    wall_group.add(wall0)

    # Game loop
    # Run until the user asks to quit
    running = True

    while running:

        # Ensure program maintains FPS
        clock.tick(fps)

        # Look for exit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Capture frame from camera and convert to surface
        cam_frame = cam.capture_frame()
        cam_surf = pygame.surfarray.make_surface(cam_frame)

        # Draw camera frame on the screen (as the background)
        screen.blit(cam_surf, (0, 0))

        # Get pressed keys
        pressed_keys = pygame.key.get_pressed()

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

    # Terminate camera process
    del cam
