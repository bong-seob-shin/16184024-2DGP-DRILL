from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024


def handle_events():
    global running
    global hx, hy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            hx, hy = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass


open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')


running = True
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
hx, hy = KPU_WIDTH//2, KPU_HEIGHT//2
frame = 0
hide_cursor()

while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    hand_arrow.clip_draw(0, 0, 100, 100, hx, hy)
    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()




