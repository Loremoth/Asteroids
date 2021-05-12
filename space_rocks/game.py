from time import sleep

import pygame
from pygame_functions import screenSize, moveLabel, showLabel, makeLabel, hideLabel

from space_rocks.constants import FinalScreen
from utils import load_sprite, get_random_position, print_text
from models import Asteroid, Spaceship


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = screenSize(800, 600)
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
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
            elif (
                    self.spaceship
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
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
                    self.spaceship = None
                    self.message = FinalScreen.PROTOTYPE_FINAL_DISPLAY.format(FinalScreen.LOST_MESSAGE, FinalScreen.MESSAGE_ESC_OR_CONTINUE)
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
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

        pygame.display.flip()

        if self.message:
            test_label = makeLabel(self.message, 60, 400, 300, fontColour="red",
                                   font='juiceitc', background='clear')

            moveLabel(test_label,
                      test_label.rect.topleft[0] - test_label.rect.width / 2,
                      test_label.rect.topleft[1] - test_label.rect.height / 2)

            self.screen.fill("black")

            showLabel(test_label)

            while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (
                                event.type == pygame.KEYDOWN and
                                (event.key == pygame.K_ESCAPE)
                        ):
                            quit()
                        elif (
                                event.type == pygame.KEYDOWN
                                and event.key == pygame.K_RETURN
                        ):
                            hideLabel(test_label)
                            self.__init__()
                            self.main_loop()

        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    # def _final_screen_handling(self):

