from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    player_width, player_height, tmp, tmp = target_rect
    tmp, tmp, w, h = camera
    player_width, player_height = -player_width + WIN_WIDTH / 2, -player_height + WIN_HEIGHT / 2

    player_width = min(0, player_width)
    player_width = max(-(camera.width - WIN_WIDTH), player_width)
    player_height = max(-(camera.height - WIN_HEIGHT), player_height)
    player_height = min(0, player_height)

    return Rect(player_width, player_height, w, h)
