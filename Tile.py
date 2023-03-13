import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, grps):
        super().__init__(grps)
        image_not_scaled = pygame.image.load('assets/rock.png').convert_alpha() # for scaling sprite
        self.image = pygame.transform.scale(image_not_scaled, (64, 64)) # for scaling sprite
        #self.image = pygame.image.load('assets/SingleWall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
