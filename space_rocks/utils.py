import random

from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame_functions import makeLabel, showLabel


def load_sound(name):
    path = f"C:/Users/ActionICT/PycharmProjects/Asteroids/assets/sounds/{name}.wav"
    return Sound(path)


def load_sprite(name, with_alpha=True):
    print(name)
    path = f"C:/Users/ActionICT/PycharmProjects/Asteroids/assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def print_text(surface, text, font, color=Color("tomato")):

    test_label = makeLabel(text, 40, 100, 200, fontColour="red", font="Arial")

    showLabel(test_label)
