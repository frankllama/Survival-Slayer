import pygame
import sys
import os
from character import *
from settings import *
from Level import level



class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survival Slayer')
        self.clock = pygame.time.Clock()

        self.level = level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # setting up the background and updating the screen
            self.screen.fill('black')
            self.level.run()
            # player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

            current_time = pygame.time.get_ticks()
            if current_time > 3000:
                self.level.reset(MAP_2)
                current_time = 0


if __name__ == '__main__':
    game = Game()
    game.run()
