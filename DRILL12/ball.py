import random
from pico2d import *
import game_world
import game_framework

class Ball:
    image = None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = random.randint(50, 1200), random.randint(50, 950)

    def get_bb(self):
        # fill here
        return self.x-10,self.y-10,self.x+10,self.y+10

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
    # fill here for draw


    def update(self):
     pass

class BigBall(Ball):
    MIN_FALL_SPEED = 50
    MAX_FALL_SPEED = 200
    image = None

    def __init__(self):
        if BigBall.image == None:
            BigBall.image = load_image('ball41x41.png')
        self.x, self.y = random.randint(50, 1200), random.randint(50, 950)



    def get_bb(self):
        return self.x - 20, self.y -20, self.x +20, self.y +20




