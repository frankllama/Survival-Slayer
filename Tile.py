import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, grps):
        super().__init__(grps)
        self.image = pygame.image.load('assets/SingleWall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)