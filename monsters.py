import pygame

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#e35124"


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, walking_speed, walking_length):
        pygame.sprite.Sprite.__init__(self)
        self.start_x = x
        self.start_y = y
        self.image = pygame.Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(pygame.Color(MONSTER_COLOR))
        self.rect = pygame.Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.walking_length = walking_length
        self.x_speed = walking_speed

    def update(self, platforms):
        self.rect.x += self.x_speed
        self.collide(platforms)
        if abs(self.start_x - self.rect.x) > self.walking_length:
            self.x_speed = -self.x_speed

    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and self != p:
                self.x_speed = - self.x_speed
                break
