from pico2d import *
import game_framework


class Brick:
    def __init__(self):
        self.image = load_image('brick180x40.png')
        self.x = 400
        self.y = 200
        self.move_speed = 100
    def update(self):
       self.x -= self.move_speed * game_framework.frame_time
       if self.x+90 >1600-25:
           self.move_speed *= -1
       elif self.x-90 < 25:
            self.move_speed *= -1

    def draw(self):
        self.image.draw(self.x, self.y)
        # fill here
    # fill here
    def get_bb(self):
        return self.x-90, self.y-20, self.x+90, self.y+20
