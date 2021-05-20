import logging
from time import sleep

import pygame
import pygame_assets
from pygame.mixer import Sound
from pygame_functions import screenSize, moveLabel, showLabel, makeLabel, hideLabel

from space_rocks.constants import FinalScreen
from utils import load_sprite, get_random_position, print_text
from models import Asteroid, Spaceship


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 500

    def __init__(self, mute=False):
        self._init_pygame()
        self.screen = screenSize(1000, 700)
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.destroyed_small = 0
        self.score = 0
        self.scoretext = self.font.render("Score = " + str(self.score), 1, (255, 0, 0))
        self.mute = mute
        self.previous_time = 0

        logging.debug("mute: " + str(mute))

        if not mute:
            file = 'C://Users//ActionICT//PycharmProjects//Asteroids//assets//music//jlbrock44_-_Stars_Below_Us.mp3'
            logging.info("starting mixer")
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely.

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append, mute = self.mute)
        logging.info("Creating initial asteroids")

        for _ in range(5):
            while True:
                position = get_random_position(self.screen)
                if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        logging.info("Starting main loop")
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif self.spaceship and ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                self.spaceship.shoot()

        current_time = pygame.time.get_ticks()

        if current_time - self.previous_time > 200:
            logging.debug("Previous time " + str(self.previous_time))
            logging.debug("Current time " + str(current_time))
            self.previous_time = current_time
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    logging.info("game over!!")
                    self.spaceship = None
                    #Sound('C:/Users/ActionICT/PycharmProjects/Asteroids/assets/sound/Blastwave_FX_BankSafeExplosion_HV.37.mp3').play()
                    self.message = FinalScreen.PROTOTYPE_FINAL_DISPLAY.format(FinalScreen.LOST_MESSAGE, FinalScreen.MESSAGE_ESC_OR_CONTINUE) +' '+ str(self.score)
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    if asteroid.size == 1:
                        if not self.mute:
                            pygame_assets.loaders.sound('firework_explosion_001.mp3').play()
                        self.destroyed_small += 1
                        if self.destroyed_small == 4:
                            while True:
                                position = get_random_position(self.screen)
                                if (
                                        position.distance_to(self.spaceship.position)
                                        > self.MIN_ASTEROID_DISTANCE
                                ):
                                    break
                            self.destroyed_small = 0
                            self.asteroids.append(Asteroid(position, self.asteroids.append))
                    elif asteroid.size == 3:
                        if not self.mute:
                            pygame_assets.loaders.sound('zapsplat_explosion_large.mp3').play()
                    else:
                        if not self.mute:
                            pygame_assets.loaders.sound("boom.mp3").play()
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    self.score += 10
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = FinalScreen.PROTOTYPE_FINAL_DISPLAY.format(FinalScreen.WON_MESSAGE, FinalScreen.MESSAGE_ESC_OR_CONTINUE)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        # self.spaceship.draw(self.screen)
        # self.asteroid.draw(self.screen)
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        self.screen.blit(self.scoretext, (500, 10))
        self.scoretext = self.font.render("Score = " + str(self.score), 1, (255, 0, 0))

        pygame.display.flip()

        if self.message:
            test_label = makeLabel(self.message, 60, 400, 300, fontColour="red",
                                   font='juiceitc', background='clear')

            moveLabel(test_label,
                      test_label.rect.topleft[0] - test_label.rect.width / 2,
                      test_label.rect.topleft[1] - test_label.rect.height / 2)

            self.screen.fill("black")

            showLabel(test_label)

            pygame.mixer.music.stop()

            while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (
                                event.type == pygame.KEYDOWN and
                                (event.key == pygame.K_ESCAPE)
                        ):
                            logging.info("Quitting game")
                            quit()
                        elif (
                                event.type == pygame.KEYDOWN
                                and event.key == pygame.K_RETURN
                        ):
                            hideLabel(test_label)
                            logging.info("Restarting...")
                            logging.info("\n\n----------------------------------------------------------\n\n")
                            self.__init__(mute=True)
                            self.main_loop()

        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    # def _final_screen_handling(self):

