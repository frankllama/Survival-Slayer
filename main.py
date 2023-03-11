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
        # get the currect working directory to locate the spritesheet
        #cwd = os.getcwd()
        # set the path to the directory containing the sprite sheet
        ##sprite_file = os.path.join(sprite_dir, "character.png")
        #player_spritesheet = pygame.image.load(sprite_file)
        #player = Character(500, 500)  # initializing the player character
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


if __name__ == '__main__':
    game = Game()
    game.run()
