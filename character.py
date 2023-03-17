import pygame
from settings import *


class Character(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        # for scaling sprite
        self.image = pygame.transform.scale(pygame.image.load(
            'assets/blue_ninja.png').convert_alpha(), (64, 64))
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

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')
        # self.rect.center += self.direction * speed

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # character is moving to the right to object's left side.
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    # character is moving to the left to object's right side.
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # character is moving down to object's top side.
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    # character is moving up to object's bottom side.
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
            

    def update(self):
        self.input()
        self.move(self.speed)
        
    
