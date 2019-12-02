import random
from pico2d import *
import game_world
import game_framework

class Ball:
    image = None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = random.randint(50, 1200), random.randint(50, 1000)
        self.cx, self.cy = self.x, self.y
    def get_bb(self):
        # fill here
        return self.cx-10,self.cy-10,self.cx+10,self.cy+10

    def set_background(self, bg):
        self.bg = bg


    def draw(self):
        self.cx, self.cy = self.x - self.bg.window_left, self.y-self.bg.window_bottom
        self.image.draw(self.cx, self.cy)
        draw_rectangle(*self.get_bb())
    # fill here for draw


    def update(self):
     pass



