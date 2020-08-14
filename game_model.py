import pygame
import json
import blocks
import camera
import player
import monsters


class GameModel:
    def __init__(self, level_data, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.background = pygame.Surface((self.win_width, self.win_height))
        self.background_color = "#630500"
        self.background.fill(pygame.Color(self.background_color))
        self.platforms = []
        self.platform_width = 32
        self.platform_height = 32
        self.platform_color = "#FF6262"
        self.entities = pygame.sprite.Group()

        with open(level_data) as data:
            data_level = data.read()
        lvl = json.loads(data_level)
        self.level = lvl["level"]
        self.createLevel()

        self.monsters = pygame.sprite.Group()
        for i in range(1, 10):
            self.createMonster(0, *lvl["monster_" + str(i)])

        self.hero = player.SpurdoSpuzzelli(lvl["spawn_player_x"], lvl["spawn_player_y"])
        self.entities.add(self.hero)
        self.total_level_width = len(self.level[0]) * blocks.PLATFORM_WIDTH
        self.total_level_height = len(self.level) * blocks.PLATFORM_HEIGHT
        self.camera = camera.Camera(
            camera.camera_configure,
            self.total_level_width,
            self.total_level_height
        )

    def run(self, screen):
        timer = pygame.time.Clock()
        left = up = right = False
        pygame.mixer.music.load("music/dB soundworks - Can o' Salt.mp3")
        volume = pygame.mixer.music.get_volume()
        volume /= 12
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(0, 0)
        while True:
            timer.tick(60)
            left, right, up = playerControl(left, right, up)
            screen.blit(self.background, (0, 0))
            self.hero.update(left, right, up, self.platforms)
            self.camera.update(self.hero)
            self.monsters.update(self.platforms)
            for e in self.entities:
                screen.blit(e.image, self.camera.apply(e))
            pygame.display.update()

    def createMonster(self, monster_id, *args):
        if monster_id == 0:
            monster = monsters.Monster(*args)
            self.entities.add(monster)
            self.monsters.add(monster)
            self.platforms.append(monster)

    def createBlock(self, block_id, *args):
        if block_id == "-":
            floor = blocks.Platform(args[0], args[1])
            self.entities.add(floor)
            self.platforms.append(floor)
        elif block_id == "*":
            spike = blocks.Spike(args[0], args[1])
            self.entities.add(spike)
            self.platforms.append(spike)

    def createLevel(self):
        x = y = 0
        for row in self.level:
            for col in row:
                self.createBlock(col, x, y)
                x += blocks.PLATFORM_WIDTH
            y += blocks.PLATFORM_HEIGHT
            x = 0


def playerControl(left, right, up):
    for button in pygame.event.get():
        if button.type == pygame.KEYUP and button.key == pygame.K_LEFT:
            left = False
        elif button.type == pygame.KEYUP and button.key == pygame.K_RIGHT:
            right = False
        elif button.type == pygame.KEYUP and button.key == pygame.K_SPACE:
            up = False
        elif button.type == pygame.KEYDOWN and button.key == pygame.K_LEFT:
            left = True
        elif button.type == pygame.KEYDOWN and button.key == pygame.K_RIGHT:
            right = True
        elif button.type == pygame.KEYDOWN and button.key == pygame.K_SPACE:
            up = True
        elif button.type == pygame.QUIT:
            raise SystemExit("QUIT")
    return left, right, up
