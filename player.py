import pygame
import blocks
import monsters

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#a85832"
EYES = "#000000"
JUMP_POWER = 11
GRAVITY = 0.4


class SpurdoSpuzzelli(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.start_x = int(x)
        self.start_y = int(y)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(self.start_x, self.start_y, WIDTH, HEIGHT)
        self.x_speed = 0
        self.y_speed = 0
        self.on_ground = True

    def update(self, left, right, up, platforms):
        if up:
            if self.on_ground:
                self.y_speed = -JUMP_POWER

        if left:
            self.x_speed = -MOVE_SPEED

        if right:
            self.x_speed = MOVE_SPEED

        if (not left and not right) or (left and right):
            self.x_speed = 0

        if not self.on_ground:
            self.y_speed += GRAVITY

        self.on_ground = False
        self.rect.y += self.y_speed
        self.collide(0, self.y_speed, platforms)

        self.rect.x += self.x_speed
        self.collide(self.x_speed, 0, platforms)

    def collide(self, x_speed, y_speed, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if x_speed > 0:
                    self.rect.right = p.rect.left
                if x_speed < 0:
                    self.rect.left = p.rect.right
                if y_speed > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.y_speed = 0
                if y_speed < 0:
                    self.rect.top = p.rect.bottom
                    self.y_speed = 0
                if isinstance(p, blocks.Spike) or isinstance(p, monsters.Monster):
                    self.die()
                break

    def die(self):
        self.teleport(self.start_x, self.start_y)

    def teleport(self, x, y):
        self.rect.x = x
        self.rect.y = y
