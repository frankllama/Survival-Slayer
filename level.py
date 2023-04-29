import pygame 
from settings import *
from tile import Tile
from character import Character
from debug import debug
from support import *
from random import choice
import math
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade



class Level: 
    def __init__(self, game):
        self.game = game
        #print(type(self.game))

        self.reset() # to set all members to their initial value per map.
        

    def reset(self, current_map=MAP_1):
        
       
        #get surface    
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
    
        # sprite group set up 
        # Create camera for the current map.
        if current_map == MAP_1:
            self.game.current_music.stop()
            self.game.current_music = self.game.day_music
            self.game.current_music.play(loops = -1)
            self.visibile_sprites = YSortCameraGroup()
        else:
            self.visibile_sprites = YSortCameraGroup_2()

        self.obstacles_sprites = pygame.sprite.Group()
       

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        # Create the current map to use.
        if current_map == MAP_1:
            
            self.createMap()    
        else:
            self.createMap_2()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)


    def run(self):
        self.visibile_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()        
        else:
            self.visibile_sprites.update()
            self.visibile_sprites.enemy_update(self.player)
            # debug(self.player.status)
            self.player_attack_logic()

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visibile_sprites, self.attack_sprites])
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visibile_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visibile_sprites,self.attack_sprites])
        #print(style)
        #print(strength)
        #print(cost)

    def add_exp(self,amount):
        self.player.exp += amount

    def createMap(self):
        
        
        self.game.change_music(0) # 0 for day 1 for night

        layouts = {
                'boundary': import_csv_layout('map/FirstLevel_FloorBlocks.csv'),
                'object': import_csv_layout('map/FirstLevel_Obstacles.csv'), 
                'entities': import_csv_layout('map/FirstLevelData_Entities.csv')

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
                        if style == 'boundary' and col == '16':
                            Tile((x, y), [ self.obstacles_sprites], 'invisible')
                        if style == 'object':
                            surf = graphics['objects'][int(col)] #uses index of the file
                            Tile((x,y), [self.visibile_sprites, self.obstacles_sprites], 'object', surf)

                        if style == 'entities' and col != '2': 
                            # if col == '394': #el:4:10
                            #     self.player = Character(
                            #         (x, y),
                            #         [self.visibile_sprites],
                            #         self.obstacles_sprites,
                            #         self.create_attack,
                            #         self.destroy_attack,
                            #         self.create_magic)
                            # else:
                                if col == '390': 
                                    monster_name = 'OgreSkull'
                                elif col == '391': 
                                    monster_name = 'CyclopSkull'
                                elif col == '392': 
                                    monster_name = 'EvilSkull'
                                elif col == '393': 
                                    monster_name = 'OxSkull' #this is "working"/running, but need to figure out which numbers insead of 390-392 IF they don't change later

                                Enemy(
                                    monster_name, 
                                    (x,y), 
                                    [self.visibile_sprites, self.attackable_sprites], 
                                    self.obstacles_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)
        self.player = Character(
            (600,760),
            [self.visibile_sprites], 
            self.obstacles_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic)
            #print(row_index)
            #print(row)
        

    def createMap_2(self):
        #self.game.time_of_the_day == 1
        self.game.change_music(1) # 0 for day 1 for night
        layouts = {
                'boundary': import_csv_layout('map/FirstLevelData_FloorBlocks.csv'),               
                'object': import_csv_layout('map/FirstLevel_Obstacles.csv'), 
                'entities': import_csv_layout('map/FirstLevelData_Entities.csv')
        }
        graphics = {                   
                    'objects': import_folder('graphics/objectsNight')
        }
        # print(graphics)
        # print(graphics['objects'])

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary' and col == '16':
                            Tile((x, y), [ self.obstacles_sprites], 'invisible')
                        if style == 'object':
                            surf = graphics['objects'][int(col)] #uses index of the file
                            Tile((x,y), [self.visibile_sprites, self.obstacles_sprites], 'object', surf)

                        if style == 'entities' and col != '2': 
                    # if col == '394': #el:4:10
                    #     self.player = Character(
                    #         (x, y),
                    #         [self.visibile_sprites],
                    #         self.obstacles_sprites,
                    #         self.create_attack,
                    #         self.destroy_attack,
                    #         self.create_magic)
                    # else:
                            if col == '390': 
                                monster_name = 'OgreSKull'
                            elif col == '391': 
                                monster_name = 'CyclopSkull'
                            elif col == '392': 
                                monster_name = 'EvilSkull'
                            elif col == '393':
                                monster_name = 'OxSkull' #this is "working"/running, but need to figure out which numbers insead of 390-392 IF they don't change later

                            Enemy(
                                monster_name, 
                                (x,y), 
                                [self.visibile_sprites, self.attackable_sprites], 
                                self.obstacles_sprites,
                                self.damage_player,
                                self.trigger_death_particles,
                                self.add_exp)

        self.player = Character(
            (1200,1500),
            [self.visibile_sprites], 
            self.obstacles_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic)
            #print(row_index)
            #print(row)


    def toggle_menu(self):
        self.game_paused = not self.game_paused 


    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            # TODO: add create_grass_particles method later.
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)


    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visibile_sprites])
            # TODO: spawn particles


    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visibile_sprites)



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


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() 
                         if hasattr(sprite,'sprite_type') and
                                    sprite.sprite_type == 'enemy']
        for enemy  in enemy_sprites:
            enemy.enemy_update(player)



class YSortCameraGroup_2(pygame.sprite.Group):
    def __init__(self):
        # general setup

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor, need to change according to picture we decide to use:
        self.floor_surface = pygame.image.load('assets/FirstLevelNight.png').convert()
        # self.map_surface = pygame.Surface((6000, 5000)).convert()
        # self.scaled_map_surface = pygame.transform.scale(self.floor_surface, (2000, 1800))
        #self.floor_surface = pygame.Surface((2000, 1800)).convert()
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


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() 
                         if hasattr(sprite,'sprite_type') and
                                    sprite.sprite_type == 'enemy']
        for enemy  in enemy_sprites:
            enemy.enemy_update(player)
