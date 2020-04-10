import pygame
import json

from blocks import *
from camera import *
from player import *
from monsters import *


class GameModel:
    def __init__(self, level_data):
        self.win_width = 800
        self.win_height = 640
        self.background = Surface((self.win_width, self.win_height))
        self.background_color = "#630500"
        self.platform_width = 32
        self.platform_height = 32
        self.platform_color = "#FF6262"

        with open(level_data) as data:
            data_level = data.read()
        lvl = json.loads(data_level)

        self.platforms = []
        self.entities = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.background.fill(Color(self.background_color))
        for i in range(1, 9):
            monster = self.createMonster(0, *lvl["monster_" + str(i)])
            self.entities.add(monster)
            self.monsters.add(monster)
            self.platforms.append(monster)
        self.level = lvl["level"]
        x = y = 0
        for row in self.level:
            for col in row:
                self.createBlock(col, x, y)
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0

        self.hero = Player(lvl["spawn_player_x"], lvl["spawn_player_y"])
        self.entities.add(self.hero)
        self.total_level_width = len(self.level[0]) * PLATFORM_WIDTH
        self.total_level_height = len(self.level) * PLATFORM_HEIGHT
        self.camera = Camera(camera_configure, self.total_level_width, self.total_level_height)

    def run(self, screen):
        timer = pygame.time.Clock()
        left = up = right = False
        while True:
            timer.tick(60)
            left, right, up = self.playerControl(left, right, up)
            screen.blit(self.background, (0, 0))
            self.hero.update(left, right, up, self.platforms)
            self.camera.update(self.hero)
            self.monsters.update(self.platforms)
            for e in self.entities:
                screen.blit(e.image, self.camera.apply(e))
            pygame.display.update()

    def createMonster(self, monster_id, *args):
        if monster_id == 0:
            return Monster(*args)

    def createBlock(self, block_id, *args):
        if block_id == "-":
            floor = Platform(args[0], args[1])
            self.entities.add(floor)
            self.platforms.append(floor)
        elif block_id == "*":
            spike = Spike(args[0], args[1])
            self.entities.add(spike)
            self.platforms.append(spike)

    def playerControl(self, left, right, up):
        for button in pygame.event.get():
            if button.type == KEYUP and button.key == K_LEFT:
                left = False
            elif button.type == KEYUP and button.key == K_RIGHT:
                right = False
            elif button.type == KEYUP and button.key == K_UP:
                up = False
            elif button.type == KEYDOWN and button.key == K_LEFT:
                left = True
            elif button.type == KEYDOWN and button.key == K_RIGHT:
                right = True
            elif button.type == KEYDOWN and button.key == K_UP:
                up = True
            elif button.type == QUIT:
                raise SystemExit("QUIT")
        return left, right, up
