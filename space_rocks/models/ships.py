import logging

import pygame.time
import pygame_assets.loaders
from pygame.math import Vector2
from pygame.transform import rotozoom
from models.models import GameObject, UP, Bullet
from utils import load_sprite


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 10
    MAX_SPEED = 5

    def __init__(self, position, create_bullet_callback, mute, direction=None, velocity=Vector2(0)):
        self.create_bullet_callback = create_bullet_callback
        # Make a copy of the original UP vector
        if not mute:
            self.laser_sound = pygame_assets.loaders.sound("laser.wav")
            self.laser_sound.set_volume(0.1)
        self.direction = direction if direction else Vector2(UP)
        self.mute = mute
        super().__init__(position, load_sprite("spaceship"), Vector2(0))
        self.last_shoot_time = 0

        self.velocity = velocity

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        self._limit_velocity()

    def _limit_velocity(self):
        if self.velocity[0] > self.MAX_SPEED:
            self.velocity[0] = self.MAX_SPEED
        if self.velocity[1] > self.MAX_SPEED:
            self.velocity[1] = self.MAX_SPEED

        if self.velocity[0] < -self.MAX_SPEED:
            self.velocity[0] = -self.MAX_SPEED
        if self.velocity[1] < -self.MAX_SPEED:
            self.velocity[1] = -self.MAX_SPEED

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time > 100:
            self.last_shoot_time = current_time
            logging.debug("Shooting at time " + str(pygame.time.get_ticks()))
            bullet_velocity = self.direction * self.BULLET_SPEED #+ self.velocity
            bullet = Bullet(self.position, bullet_velocity)
            self.create_bullet_callback(bullet)
            if not self.mute:
                self.laser_sound.play()


class SlowShip(Spaceship):

    def __init__(self, position, create_bullet_callback, mute, direction, velocity):
        super().__init__(position, create_bullet_callback, mute)
        self.MANEUVERABILITY = 1
        self.ACCELERATION = 0.1
        self.BULLET_SPEED = 5
        self.MAX_SPEED = 3
        self.direction = direction
        self.velocity = velocity

    def draw(self, surface):
        super().draw(surface)
