import pygame
import sys
import random
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
        self.time_interval = 10000 # 5,000 milliseconds == 5 seconds
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, self.time_interval)

        # an event to display a countdown timer on screen
        self.countdown_display = pygame.USEREVENT+2
        pygame.time.set_timer(self.countdown_display, 910) # adjust milliseconds manually to equal 1 second
        self.countdown_font = pygame.font.Font(None, 36)
        self.countdown_counter = 10
        self.countdown_text = '10'

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
                if event.type == self.countdown_display:
                    if self.countdown_counter == 0:
                        self.countdown_counter = 11
                    self.countdown_counter -= 1
                    self.countdown_text = str(self.countdown_counter)

            # setting up the background and updating the screen
            self.screen.fill('black')
            self.level.run()
            
            # render to the screen the countdown timer, might affect performance.
            self.screen.blit(self.countdown_font.render(
                self.countdown_text, True, (255, 255, 255)), (1250, 10))
            
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
