import pygame 
from settings import *
from Tile import Tile
from character import Character
class level: 
    def __init__(self):
        #get surface    
        self.display_surface = pygame.display.get_surface()
        #sprite group set up 
        self.visibile_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        self.createMap()    
    def run(self):
        self.visibile_sprites.draw(self.display_surface)
        self.visibile_sprites.update()
        
    
    def createMap(self):
        for row_index, row in enumerate(MAP_1):
            for col_index, col in enumerate(row):
                x  = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x,y), [self.visibile_sprites, self.obstacles_sprites])
                if col == 'p':
                    Character((x,y), [self.visibile_sprites])

            #print(row_index)
            #print(row)