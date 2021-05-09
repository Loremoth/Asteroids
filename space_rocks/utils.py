import random

from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame_functions import makeLabel, showLabel, moveLabel


def load_sound(name):
    path = f"C:/Users/ActionICT/PycharmProjects/Asteroids/assets/sounds/{name}.wav"
    return Sound(path)


def load_sprite(name, with_alpha=True):
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


def print_text(text: str):
    test_label = makeLabel(text, 60, 400, 300, fontColour="red",
                           font='juiceitc', background='clear')

    moveLabel(test_label,
              test_label.rect.topleft[0] - test_label.rect.width/2,
              test_label.rect.topleft[1] - test_label.rect.height/2)

    showLabel(test_label)

