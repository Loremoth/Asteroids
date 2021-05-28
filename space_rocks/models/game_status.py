from abc import ABC, abstractmethod

import pygame.time

from models.ships import Spaceship, SlowShip


class GameStatus(ABC):
    @abstractmethod
    def get_finished(self):
        pass

    @abstractmethod
    def get_ship(self):
        pass


class NormalStatus(GameStatus):
    def get_finished(self):
        return False

    def get_ship(self):
        return Spaceship


class SlowShipStatus(GameStatus):
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def get_ship(self):
        return SlowShip

    def get_finished(self) -> bool:
        return True if pygame.time.get_ticks() - self.start_time > 5000 else False


