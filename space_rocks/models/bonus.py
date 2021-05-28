import pygame_assets
from pygame.math import Vector2

from models.game_status import SlowShipStatus
from models.models import GameObject


class Bonus(GameObject):
    def __init__(self, position):
        super().__init__(position, pygame_assets.loaders.image('xdeVt.jpg').convert_alpha(), Vector2(0))


class SlowBonus(Bonus):
    def get_status(self):
        return SlowShipStatus()

    def draw(self, surface):
        super().draw(surface)
