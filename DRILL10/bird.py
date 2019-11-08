import game_framework
from pico2d import *

import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 4.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5




class Bird:

    def __init__(self):
        self.x, self.y = 1600 // 2, 300
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('bird_animation.png')
        self.dir = 1
        self.velocity = RUN_SPEED_PPS
        self.frame = 0
        self.frameCount = 1

    def update(self):
        self.x += self.velocity * game_framework.frame_time
        if self.x > 1600:
            self.velocity = self.velocity*-1;
        if self.x<0:
            self.velocity = self.velocity*-1;
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if self.frame > 4:
            self.frameCount = (self.frameCount) % 3
            self.frameCount += 1
        pass

    def draw(self):
        self.image.clip_draw(int(self.frame) * 180, 175*self.frameCount, 180, 180, self.x, self.y)
        pass
