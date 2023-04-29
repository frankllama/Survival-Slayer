import pygame
import sys
import random

from pygame.draw import rect
from character import *
from settings import *
from level import Level
from time import sleep
from button import Button



class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survival Slayer')
        self.clock = pygame.time.Clock()
        self.time_of_the_day = 0 # 0 for day 1 for night
        
        self.map_list = [MAP_1, MAP_2]
        # create an event to randomly change the map on the event queue, timer based.
        self.time_interval = 10000 # 5,000 milliseconds == 5 seconds
        self.timer_event = pygame.USEREVENT+1
        #pygame.time.set_timer(self.timer_event, self.time_interval)
        
        # sound
        self.current_music = pygame.mixer.Sound('audio/dayTime.mp3')
        self.current_music.set_volume(0.5)
        
        
        self.game_over_sound = pygame.mixer.Sound('audio/gameover.wav')
        self.game_over_sound.set_volume(0.5)
        self.time_of_the_day = 0 # 0 for day 1 for night
        self.evil_laugh = pygame.mixer.Sound('audio/evil.mp3')
        self.evil_laugh.set_volume(0.5)
        self.day_music = pygame.mixer.Sound('audio/dayTime.mp3')
        self.day_music.set_volume(0.5)
        self.night_music = pygame.mixer.Sound('audio/nightTime.mp3')
        self.night_music.set_volume(0.5)
        
        self.level = Level(self)

        # game over state
        self.game_over_state = False


    def run(self):
        # start map change timer here.
        pygame.time.set_timer(self.timer_event, self.time_interval)
        while True:
            if self.level.player.health <= 0:
                self.game_over_state = True
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
                    current_weapon_index = self.level.player.weapon_index
                    current_weapon = list(weapon_data.keys())[current_weapon_index]
                    current_magic_index = self.level.player.magic_index
                    current_magic = list(magic_data.keys())[current_magic_index]

                    self.level.reset(current_map)

                    # assign current stats to now current map after the reset.
                    self.level.player.exp = current_score
                    self.level.player.health = current_health
                    self.level.player.energy = current_energy
                    self.level.player.weapon_index = current_weapon_index
                    self.level.player.weapon = current_weapon
                    self.level.player.magic_index = current_magic_index
                    self.level.player.magic = current_magic

                    # refill 1 magic
                    self.level.player.energy_recovery()

            if self.game_over_state:
                player_choice = self.game_over()
                if player_choice == 1:
                    self.game_over_state = False
                    pygame.time.set_timer(self.timer_event, self.time_interval)
                    self.level.reset()
                  
                elif player_choice == 2:
                    pygame.quit()
                    sys.exit()
                else:
                    pass


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

    def change_music(self, time_of_day):
        if self.time_of_the_day != time_of_day:
            self.current_music.stop()
            if time_of_day == 0: 
                self.current_music = self.day_music
                self.current_music.play(loops = -1)
            if time_of_day == 1:
                self.current_music = self.night_music
                self.current_music.play(loops= -1)
       
        

    def game_over(self):
        # Render text to display
        self.current_music.stop()
        self.game_over_sound.play()
        self.evil_laugh.play()

        game_over_font = pygame.font.Font('graphics/font/joystix.ttf', 72)
        game_over_text = pygame.font.Font.render(game_over_font, "Game Over", True, (200, 200, 200))

        play_again_font = pygame.font.Font('graphics/font/joystix.ttf', 48)
        play_again_text = pygame.font.Font.render(play_again_font, "(1) Play Again?", True, (200, 200, 200))

        quit_game_font = pygame.font.Font('graphics/font/joystix.ttf', 48)
        quit_game_text = pygame.font.Font.render(quit_game_font, "(2) Quit", True, (200, 200, 200))

        # draw to screen
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, (400, 200))
        self.screen.blit(play_again_text, (300, 400))
        self.screen.blit(quit_game_text, (300, 500))

        pygame.display.update()

        for sprite in self.level.attackable_sprites:
            sprite.kill()

        game_running = True
        while game_running:
            for event in pygame.event.get():
                #wait = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_running = False
                        return 1
                    elif event.key == pygame.K_2:
                        game_running = False
                        return 2
                    else:
                        pass


    def intro_screen(self):
        # Render text to display
        intro_font = pygame.font.Font('graphics/font/joystix.ttf', 72)
        intro_text = pygame.font.Font.render(intro_font, "Survival Slayer", True, (200, 200, 200))

        intro = True

        play_button = Button(400, 400, 400, 74, (200,200,200), (0,0,0), '(1) Play', 48)
        quit_button = Button(400, 500, 400, 74, (200,200,200), (0,0,0), '(2) quit', 48)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()
                    sys.exit()


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_1:  # key press event for number 1
                        intro = False
                        break


                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()

                if play_button.is_pressed(mouse_pos, mouse_pressed) :
                    intro = False
                if quit_button.is_pressed(mouse_pos, mouse_pressed) :
                    intro = False
                    pygame.quit()
                    sys.exit()

                self.screen.fill((0, 0, 0))
                self.screen.blit(intro_text, (160, 150))
                self.screen.blit(play_button.image, play_button.rect)
                self.screen.blit(quit_button.image, quit_button.rect)
                #self.clock.tick(FPS)
                pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.intro_screen()
    game.run()
