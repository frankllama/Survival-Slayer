import pygame 
from settings import *
from Tile import Tile
from character import Character
from debug import debug
from support import *
from random import choice
import math
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
        layouts = {
                'boundary': import_csv_layout('map/FirstLevelData_FloorBlocks.csv'),
                'object': import_csv_layout('map/FirstLevelData_Obstacles.csv')


        }
        graphics = {
                    'objects': import_folder('graphics/objects')
        }
        # print(graphics)
        # print(graphics['objects'])

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [ self.obstacles_sprites], 'invisible')
                            
                        if style == 'object':
                            surf = graphics['objects'][int(col)] #uses index of the file

                            Tile((x,y), [self.visibile_sprites, self.obstacles_sprites], 'object', surf)
        #         if col == 'x':
        #             Tile((x,y), [self.visibile_sprites, self.obstacles_sprites])
        #         if col == 'p':
        #             self.player = Character((x,y), [self.visibile_sprites], self.obstacles_sprites)
        #             # self.visibile_sprites.add(self.player)
        self.player = Character((500,500), [self.visibile_sprites], self.obstacles_sprites)
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

        ##--------------------------    
        # self.scale = 1.0  # default scale
        # self.min_scale = 0.5  # minimum scale allowed
        # self.max_scale = 2.0  # maximum scale allowed
        # self.zoom_speed = 0.02  # how fast the zoom happens
        #---------------------------

        #creating the floor, need to change according to picture we decide to use:
        # self.floor_surface = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_surface = pygame.image.load('assets/FirstLevel.png').convert()
        # self.map_sruface = pygame.Surface((6000, 5000)).convert()

        # self.scaled_map_surface = pygame.transform.scale(self.floor_surface, (2000, 1800))

        #self.floor_surface = pygame.Surface((2000, 1800)).convert()

        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0)) #surf = surface

    def custom_draw(self,player):

        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height


        #------------------------        
         # calculate the distance between the player and the center of the screen
        # dx = abs(self.offset.x - self.half_width)
        # dy = abs(self.offset.y - self.half_height)
        # distance = math.sqrt(dx ** 2 + dy ** 2)



        #  # adjust the scale based on the distance and the zoom speed
        # target_scale = 1.0 + (distance / 500) * self.zoom_speed
        # self.scale = max(min(target_scale, self.max_scale), self.min_scale)

        # self.scaled_map_surface = pygame.transform.scale(
        #     self.floor_surface,
        #     (int(self.floor_surface.get_width() * self.scale),
        #         int(self.floor_surface.get_height() * self.scale)))
        #------------------------
        # scale the floor surface
        #scaled_floor_surface = pygame.transform.scale(self.floor_surface, (int(self.floor_rect.width * self.zoom_level), int(self.floor_rect.height * self.zoom_level)))
    

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface,floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

