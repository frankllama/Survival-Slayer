import pygame
from settings import *
from entity import Entity
from support import *
import random

#The enemy entity is done implemented here. Stats, sprites, particles and player
#interaction are its main responsibility 
class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        

        #player intereaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        self.drops = [('health', 0.5), ('mana', 0.25)] # 50 percent of heart drop, 25 percent of potion drop


        # sounds
        self.death_sound = pygame.mixer.Sound('audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.3)

        # invincibility timer, after being attacked by player
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def checkAttackCooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time -self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        # if self.attack_cooldown >= 0:
        #     self.attack_cooldown -= .1
        # if self.attack_cooldown <= 0:
        #     self.can_attack = True
        #     self.attack_cooldown  =5

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center) 

        if player_vector == enemy_vector:
            enemy_vector[0] = enemy_vector[0] -1
            distance = (player_vector - enemy_vector).magnitude() #converting a vector into distance
            direction = (player_vector - enemy_vector).normalize()# convertin a vector into a direction by normalizing  
        else: 
            distance = (player_vector - enemy_vector).magnitude() #converting a vector into distance
            if player_vector == enemy_vector:
                enemy_vector[0] = enemy_vector[0] -1
            direction = (player_vector - enemy_vector).normalize()# convertin a vector into a direction by normalizing
       
        if distance > 0: 
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            print('attack')
            self.status = 'attack'
        elif distance <= self.notice_radius:
            print('move')
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            print("move")
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()
            items = [item[0] for item in self.drops]
            weights = [item[1] for item in self.drops]
            item_dropped = random.choices(items, weights)[0]
            self.heart_group = pygame.sprite.Group()

            Drops(item_dropped, self.rect.center,self.heart_group)
            # if item_dropped == 'health':
            #    Drops()
            #     # create a new health heart entity at the enemy's position
            # elif item_dropped == 'potion':
            #     self.support.add_entity('potion', self.rect.center, self.groups)

    def hit_reaction(self):
        # enemy will be pushed away in the same facing direction as the player.
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.checkAttackCooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)


class Drops(Entity):
    def __init__(self, dropType, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'item'
        if dropType == 'health':
            self.image = pygame.image.load('graphics/Heart/Heart.png').convert_alpha()
        if dropType == 'mana':
            self.image = pygame.image.load('graphics/Mana/ManaPotion.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
    
    def update(self):
        pass