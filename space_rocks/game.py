import logging
from time import sleep

import pygame
import pygame_assets
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
        self.font = pygame.font.SysFont('juiceitc', 64)
        self.message = ""
        self.destroyed_small = 0
        self.score = 0
        self.scoretext = self.font.render("Score = " + str(self.score), 1, (255, 0, 0))
        self.mute = mute
        self.previous_time = 0
        self.score_column = pygame.rect.Rect((800, 0, 200, 700))
        self.game_column = pygame.rect.Rect((0, 0, 800, 700))
        self.game_surface = pygame.surface.Surface.subsurface(self.screen, self.game_column)
        self.score_surface = pygame.Surface.subsurface(self.screen, self.score_column)

        logging.debug("mute: " + str(mute))

        if not self.mute:
            self._init_mixer()

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append, mute=self.mute)
        logging.info("Creating initial asteroids")
        self._create_asteroids()

    def _init_mixer(self):
        file = './/assets//music//jlbrock44_-_Stars_Below_Us.mp3'
        logging.info("starting mixer")
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely.

    def _create_asteroids(self):
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
            game_object.move(self.game_surface)

        self._process_asteroid_creation()
        self._process_fired_bullets()

        if not self.asteroids and self.spaceship:
            self.message = FinalScreen.PROTOTYPE_FINAL_DISPLAY.format(FinalScreen.WON_MESSAGE,
                                                                      FinalScreen.MESSAGE_ESC_OR_CONTINUE)

    def _process_asteroid_creation(self):
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    logging.info("game over!!")
                    self.spaceship = None
                    self.message = FinalScreen.PROTOTYPE_FINAL_DISPLAY.format(FinalScreen.LOST_MESSAGE,
                                                                              FinalScreen.MESSAGE_ESC_OR_CONTINUE) \
                                   + ' ' + str(self.score)
                    break

    def _process_fired_bullets(self):
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    if asteroid.size == 1:
                        if not self.mute:
                            pygame_assets.loaders.sound('firework_explosion_001.mp3').play()
                        self.destroyed_small += 1
                        if self.destroyed_small == 4:
                            while True:
                                position = get_random_position(self.game_surface)
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
            if not self.game_surface.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

    def _draw(self):
        self.screen.blit(self.background, self.game_column)
        self.screen.blit(pygame.surface.Surface((300, 700)), self.score_column)

        for game_object in self._get_game_objects():
            game_object.draw(self.game_surface)

        self.scoretext = self.font.render("Score" , 1, (255, 0, 0))
        self.scorevalue = self.font.render(str(self.score), 1, (255, 0, 0))

        self.score_surface.blit(self.scoretext, (30, 0))
        self.score_surface.blit(self.scorevalue, (30, 50))

        # test_label = makeLabel("Score = " + str(self.score), 60, 400, 300, fontColour="red",
        #                        font='juiceitc', background='clear')
        #
        # showLabel(test_label)

        pygame.display.flip()

        if self.message:
            self._handle_quitting()

        self.clock.tick(60)

    def _handle_quitting(self):
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
                    self.__init__(mute=self.mute)
                    self.main_loop()

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
