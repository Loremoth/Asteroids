import logging

import pygame.time
import pygame_assets.loaders
from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, wrap_position, get_random_velocity

UP = Vector2(0, -1)


class GameObject:

    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Asteroid(GameObject):

    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(
            position, sprite, get_random_velocity(1, 3)
        )

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)


class Spaceship(GameObject):
    MANEUVERABILITY = 5
    ACCELERATION = 0.25
    BULLET_SPEED = 3
    MAX_SPEED = 5

    def __init__(self, position, create_bullet_callback, mute):
        self.create_bullet_callback = create_bullet_callback
        # Make a copy of the original UP vector
        if not mute:
            self.laser_sound = pygame_assets.loaders.sound("laser.wav")
            self.laser_sound.set_volume(0.1)
        self.direction = Vector2(UP)
        self.mute = mute
        super().__init__(position, load_sprite("spaceship"), Vector2(0))
        self.last_shoot_time = 0

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
            bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
            bullet = Bullet(self.position, bullet_velocity)
            self.create_bullet_callback(bullet)
            if not self.mute:
                self.laser_sound.play()


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
