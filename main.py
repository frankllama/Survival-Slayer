import pygame
import sys
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

           # setting up the background and updating the screen
            self.screen.fill(WATER_COLOR)
            self.level.run()
            # player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
