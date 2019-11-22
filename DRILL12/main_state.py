import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from ground import Ground
from zombie import Zombie
from ball import Ball,BigBall

name = "MainState"

boy = None
zombie = None
def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True



def enter():
    global is_eat_ball_done
    is_eat_ball_done = False
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global zombie
    zombie = Zombie()
    game_world.add_object(zombie, 1)

    ground = Ground()
    game_world.add_object(ground, 0)

    global balls
    global big_balls
    global ball_count
    global big_ball_count
    ball_count = 10
    big_ball_count = 10
    balls = [Ball() for i in range(10)]
    big_balls = [BigBall() for i in range(10)]
    game_world.add_objects(balls, 1)
    game_world.add_objects(big_balls, 1)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass



def get_boy():
    return boy

def get_balls():
    return balls

def get_big_balls():
    return big_balls

def get_big_ball_count():
    return big_ball_count

def get_ball_count():
    return ball_count

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    global  zombie
    global boy
    global ball_count, big_ball_count
    global is_eat_ball_done
    global balls, big_balls
    for game_object in game_world.all_objects():
        game_object.update()

    if big_ball_count == 0:
        for ball in balls:
            if collide(zombie, ball):
                balls.remove(ball)
                game_world.remove_object(ball)
                zombie.hp += ball.hp
                ball_count -= 1

    for big_ball in big_balls:
        if collide(zombie, big_ball):
            big_balls.remove(big_ball)
            game_world.remove_object(big_ball)
            zombie.hp += big_ball.hp
            big_ball_count -= 1
            if big_ball_count == 0:
                is_eat_ball_done = True

    if collide(zombie, boy):
        if is_eat_ball_done == True:
            game_world.remove_object(boy)
        else:
            game_world.remove_object(zombie)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






