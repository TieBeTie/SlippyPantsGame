import pygame
from pygame import *
from game_model import GameModel


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 640))
    pygame.display.set_caption("SpurdoSpudelli")
    game = GameModel("levels/graphic_test.json")
    game.run(screen)


if __name__ == "__main__":
    main()
