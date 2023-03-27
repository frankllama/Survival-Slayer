import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, grps, sprite_type, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(grps)
        self.sprite_type = sprite_type

        # for scaling sprite
        # self.image = pygame.transform.scale(pygame.image.load(
        #     'assets/rock.png').convert_alpha(), (64, 64))
        self.image = surface
        #self.image = pygame.image.load('assets/SingleWall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) #full size of image
        self.hitbox = self.rect.inflate(0,-10)