from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024




def handle_events():
    global running
    global hx, hy
    global x2, y2
    global x, y
    global check_mouseClick
    global check_right
    global new_click
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            hx, hy = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x2 = hx-50
            y2 = hy+50
            new_click = False
            check_mouseClick = True
            if hx < x :
                check_right = False
            else :
                check_right = True
    pass


def line_move(p1, p2):

    for i in range(0, 100 + 1, 2):
        t = i/100
        a = (1-t)*p1[0]+t*p2[0]
        b = (1-t)*p1[1]+t*p2[1]
        x = a
        y = b
    pass


open_canvas(KPU_WIDTH, KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')


running = True
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
x2, y2 = KPU_WIDTH // 2, KPU_HEIGHT//2
hx, hy = KPU_WIDTH//2, KPU_HEIGHT//2
check_mouseClick = False
check_right = True
new_Click = True
move_point = [(x, y), (hx, hy)]
frame = 0
hide_cursor()

while running:

    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    if check_right:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    else:
        character.clip_draw(frame * 100, 100 * 0, 100, 100, x, y)
    hand_arrow.clip_draw(0, 0, 100, 100, hx, hy)

    update_canvas()
    frame = (frame + 1) % 8

close_canvas()




