import pygame
import sys
import random
from character import *
from settings import *
from Level import level
from time import sleep



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
        self.time_interval = 10000 # 5,000 milliseconds == 5 seconds
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
                    sleep(0.3)
                    self._fade(WIDTH, HEIGHT)
                    self.level.reset(current_map)

            # setting up the background and updating the screen
            self.screen.fill('black')
            self.level.run()
            
            pygame.display.update()
            self.clock.tick(FPS)


    def _fade(self, width, height):
        fade = pygame.Surface((width, height))
        fade.fill((30,30,30))
        for alpha in range(0, 250):
            fade.set_alpha(alpha)
            self.screen.fill((200,200,200))
            self.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(1)


if __name__ == '__main__':
    game = Game()
    game.run()
