import logging

from game import SpaceRocks

if __name__ == "__main__":
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    logging.info("\n\n------------------------------------------------------------\n\n")
    logging.info("starting game")
    space_rocks = SpaceRocks(mute=True)
    space_rocks.main_loop()