import game_framework
from pico2d import *
import main_state

name = "PauseState"
image = None


def enter():
    global image
    global boy, grass
    boy = main_state.boy
    grass = main_state.grass
    image = load_image('pause.png')
    pass


def exit():
    global image
    del(image)
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()
    pass


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    image.clip_draw(0, 0, 100, 100, 400, 300)
    update_canvas()
    pass







def update():
    pass


def pause():
    pass


def resume():
    pass
