import pygame
from settings import *


class Character(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        image_not_scaled = pygame.image.load('assets/blue_ninja.png').convert_alpha() # for scaling sprite
        self.image = pygame.transform.scale(image_not_scaled, (64, 64)) # for scaling sprite
        #self.image = pygame.image.load('assets/singlePlayerAsset.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0


        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.center += self.direction * speed

    def collision(self, direction):
        if direction == 'horizontal':
            pass

        if direction == 'vertical':
            pass
         
            
    def update(self):
        self.input()
        self.move(self.speed)
        
    
