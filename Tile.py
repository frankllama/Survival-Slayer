import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, grps):
        super().__init__(grps)
        # for scaling sprite
        self.image = pygame.transform.scale(pygame.image.load(
            'assets/rock.png').convert_alpha(), (64, 64))
        #self.image = pygame.image.load('assets/SingleWall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
