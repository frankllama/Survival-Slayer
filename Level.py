import pygame 
from settings import *
from Tile import Tile
from character import Character
from debug import debug

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
        debug(self.player.direction)    
    
    def createMap(self):
        for row_index, row in enumerate(MAP_1):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x,y), [self.visibile_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Character((x,y), [self.visibile_sprites], self.obstacles_sprites)
                    self.visibile_sprites.add(self.player)

            #print(row_index)
            #print(row)

    
