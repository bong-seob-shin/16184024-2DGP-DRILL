import game_framework
from pico2d import *

import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 200.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 4.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8




class Bird:

    def __init__(self):
        self.x, self.y = 1600 // 2, 300
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('bird_animation.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0

    def update(self):
        self.x += self.velocity * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        pass

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, self.x, self.y)
        pass
