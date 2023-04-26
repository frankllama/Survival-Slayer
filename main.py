import pygame
import sys
import random
from character import *
from settings import *
from level import Level
from time import sleep



class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survival Slayer')
        self.clock = pygame.time.Clock()

        self.level = Level()

        self.map_list = [MAP_1, MAP_2]
        # create an event to randomly change the map on the event queue, timer based.
        self.time_interval = 10000 # 5,000 milliseconds == 5 seconds
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, self.time_interval)
        
        # sound
        main_sound = pygame.mixer.Sound('audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                       if event.key == pygame.K_m:
                           self.level.toggle_menu()
                if event.type == self.timer_event:
                    current_map = random.choice(self.map_list)
                    # reset() sets all members to their initial values.
                    sleep(0.3)
                    self._fade(WIDTH, HEIGHT)
                    # get current stats before resetting and changing maps.
                    current_score = self.level.player.exp
                    current_health = self.level.player.health
                    current_energy = self.level.player.energy

                    self.level.reset(current_map)

                    # assign current stats to now current map after the reset.
                    self.level.player.exp = current_score
                    self.level.player.health = current_health
                    self.level.player.energy = current_energy
                    # refill 1 magic
                    self.level.player.energy_recovery()

           # setting up the background and updating the screen
            self.screen.fill(WATER_COLOR)
            self.level.run()
            # player.draw(self.screen)
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
