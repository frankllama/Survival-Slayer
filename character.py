import pygame
from settings import *


class Character:
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image.load('assets/singlePlayerAsset.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        

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

    def draw(self):
        pygram.draw.rect(screen, (255, 0, 0),
                         (self.x, self.y, self.width, self.height))
