import pygame
from settings import *


class Character:
    def __init__(self, x, y, screen,  image):
        self.x = x
        self.y = y
        self.screen = screen
        self.width = 20
        self.height = 22
        self.image = pygame.image.load(image).convert_alpha()

        self.frames = [pygame.Rect(self.x, self.y, self.width, self.height)
                       for x in range(0, self.image.get_width(), 19)]

        self.current_frame = 0
        self.rect = self.frames[self.current_frame]

        self.rect.x = x
        self.rect.y = y

        self.speed = 100

        self. last_update = pygame.time.get_ticks()

    def update(self):
        # Calculate the time since the last frame was drawn
        now = pygame.time.get_ticks()
        elapsed = now - self.last_update

        # If enough time has passed, increment the current frame
        if elapsed > self.speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

        # Update the rect of the sprite
        self.rect = self.frames[self.current_frame]

    def move(self, adjusted_x, adjusted_y):
        self.x += adjusted_x
        self.y += adjusted_y

    def input_handler(self, key):
        if key == pygame.K_LEFT:
            self.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.move(1, 0)
        elif key == pygame.K_UP:
            self.move(0, -1)
        elif key == pygame.K_DOWN:
            self.move(0, 1)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        #pygame.draw.rect(self.screen, (255, 0, 0),(self.x, self.y, self.width, self.height))
