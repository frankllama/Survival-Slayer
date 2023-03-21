import pygame 
from settings import *
from Tile import Tile
from character import Character
from debug import debug

class level: 
    def __init__(self):
        #get surface    
        self.display_surface = pygame.display.get_surface()
        # sprite group set up 
        # self.visibile_sprites = pygame.sprite.Group()
        self.visibile_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.createMap()    

    def run(self):
        self.visibile_sprites.custom_draw(self.player)
        self.visibile_sprites.update()
        #debug(self.player.direction)    got deleted in video, commenting out for now
    
    def createMap(self):
        for row_index, row in enumerate(MAP_1):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x,y), [self.visibile_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Character((x,y), [self.visibile_sprites], self.obstacles_sprites)
                    # self.visibile_sprites.add(self.player)

            #print(row_index)
            #print(row)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor, need to change according to picture we decide to use:
        # self.floor_surface = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_surface = pygame.image.load('assets/plains.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0)) #surf = surface

    def custom_draw(self,player):

        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface,floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

