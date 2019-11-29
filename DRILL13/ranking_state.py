import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world

import main_state
import world_build_state
from boy import Boy
from zombie import Zombie


boy = None


name = "RankingState"

menu = None

def enter():
    global font
    global times
    hide_cursor()
    hide_lattice()
    font = load_font('ENCR10B.TTF', 50)
    with open('rank.json', 'r') as f:
        times = json.load(f)


def exit():
    global menu
    del menu

def pause():
    pass

def resume():
    pass

def get_boy():
    return boy



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.change_state(world_build_state)

def update():
    pass

def draw():
    clear_canvas()
    x=get_canvas_width()//2
    y=get_canvas_height()//2
    for time in times:

        font.draw(x, y, '(Time: %3.2f)' % (time), (255, 255, 0))
        y -= 20
    update_canvas()






