import pygame
from game_model import GameModel


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("SlippyPants")
    game = GameModel("levels/graphic_test.json", 800, 600)
    game.run(screen)


if __name__ == "__main__":
    main()
