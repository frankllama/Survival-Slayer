import pygame
import sys
<<<<<<< HEAD
# import os
import random
=======
>>>>>>> main
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
        
        self.map_list = [MAP_1, MAP_2]
        # create an event to randomly change the map on the event queue, timer based.
        self.time_interval = 5000 # 5,000 milliseconds == 5 seconds
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, self.time_interval)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.timer_event:
                    current_map = random.choice(self.map_list)
                    # reset() sets all members to their initial values.
                    self.level.reset(current_map)

            # setting up the background and updating the screen
            self.screen.fill('black')
            self.level.run()
            # player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
