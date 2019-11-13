from pico2d import *
import game_framework


class Brick:
    def __init__(self):
        self.image = load_image('brick180x40.png')
        self.x = 400
        self.y = 200
        self.move_speed = 0
    def update(self):
        self.x -= self.move_speed * game_framework.frame_time

        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        # fill here


    # fill here
    def get_bb(self):
        return 0, 0, 1600-1,
