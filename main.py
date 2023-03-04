import pygame
import sys
import os
from character import *
from settings import *


class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survival Slayer')
        self.clock = pygame.time.Clock()

    def run(self):
        # get the current working directory to locate the spritesheet
        cwd = os.getcwd()
        # set the path to the directory containing the sprite sheet
        sprite_dir = os.path.join(
            "c:/Users/long9/OneDrive/Desktop/Spring2023/CPSC 254/proj/Survival-Slayer/assets/")
        # set the path to the sprite sheet file
        sprite_file = os.path.join(sprite_dir, "player.png")

        player_spritesheet = pygame.image.load(sprite_file).convert_alpha()

        # initializing the player character
        player = Character(500, 500, self.screen, sprite_file)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # check for arrow key presses
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    player.move_up()
                elif keys[pygame.K_DOWN]:
                    player.move_down()
                elif keys[pygame.K_LEFT]:
                    player.move_left()
                elif keys[pygame.K_RIGHT]:
                    player.move_right()

                # setting up the background and updating the screen
                self.screen.fill('black')
                player.draw()
                pygame.display.update()
                self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
