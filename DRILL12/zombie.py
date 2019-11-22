import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
from boy import Boy
from ball import Ball
import main_state

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


animation_names = ['Attack', 'Dead', 'Idle', 'Walk']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombiefiles/female/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        positions = [(43, 750), (1118, 750), (1050, 530), (575, 220),(235, 33), (575,220),(1050, 530), (1118,750)]
        self.patrol_positions = []
        for p in positions: self.patrol_positions.append((p[0], 1024 - p[1]))
        # convert for origin at bottom, left
        self.patrol_order = 1
        self.target_x, self.target_y = None, None
        self.x, self.y = random.randint(150, 1000), random.randint(150,850)
        self.font = load_font('ENCR10B.TTF', 16)
        #self.x, self.y = 1280 / 4 * 3, 1024 / 4 * 3
        self.load_images()
        self.dir = random.random()*2*math.pi # random moving direction
        self.speed = 0
        self.timer = 1.0 # change direction every 1 sec when wandering
        self.frame = 0
        self.build_behavior_tree()
        self.hp =  50

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random()*2*math.pi

            return BehaviorTree.SUCCESS
        pass

    def find_player_for_runaway(self):
        boy = main_state.get_boy()
        distance = (boy.x - self.x)**2 + (boy.y - self.y)**2
        if distance <(PIXEL_PER_METER*10)**2:
            self.dir = -math.atan2( boy.y - self.y , self.x - boy.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def find_player_for_chase(self):
        boy = main_state.get_boy()
        distance = (boy.x - self.x)**2 + (boy.y - self.y)**2
        if distance <(PIXEL_PER_METER*10)**2:
            self.dir = math.atan2(boy.y - self.y, boy.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def find_ball(self):
        balls = main_state.get_balls()
        temp_distance = (balls[0].x - self.x)**2 + (balls[0].y - self.y)**2
        pos_ball_x = 0
        pos_ball_y = 0
        for ball in balls:
            distance = (ball.x - self.x)**2 + (ball.y - self.y)**2
            if distance < temp_distance:
                temp_distance = distance
                pos_ball_x = ball.x
                pos_ball_y = ball.y

        if temp_distance < (PIXEL_PER_METER*5)**2:
            self.dir = math.atan2(pos_ball_y - self.y, pos_ball_x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS
        pass

    def move_to_ball(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS
        pass

    def runaway_from_player(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.dir = self.dir*-1
        return BehaviorTree.SUCCESS

    def is_compare_hp_less(self):
        boy = main_state.get_boy()
        if self.hp < boy.hp:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_compare_hp_more(self):
        boy = main_state.get_boy()
        if self.hp >= boy.hp:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def get_next_position(self):
        self.target_x, self.target_y = self.patrol_positions[self.patrol_order % len(self.patrol_positions)]
        self.patrol_order += 1
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
        return BehaviorTree.SUCCESS
        pass

    def move_to_target(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        distance = (self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2

        if distance < PIXEL_PER_METER ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

        pass

    def build_behavior_tree(self):
        is_compare_hp_less_node = LeafNode("Is Compare HP Less", self.is_compare_hp_less)
        is_compare_hp_more_node = LeafNode("Is Compare Hp more", self.is_compare_hp_more)
        runaway_from_player_node = LeafNode("Runaway from Player",self.runaway_from_player)
        find_player_for_chase_node = LeafNode("Find Player for Chase", self.find_player_for_chase)
        find_player_for_runaway_node = LeafNode("Find Player for Runaway", self.find_player_for_runaway)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        find_ball_node = LeafNode("Find Ball", self.find_ball)
        move_to_ball_node = LeafNode("Move to Ball", self.move_to_ball)

        runaway_node = SequenceNode("Runaway")
        runaway_node.add_children(is_compare_hp_less_node, find_player_for_runaway_node, runaway_from_player_node)

        chase_node = SequenceNode("Chase")
        chase_node.add_children(is_compare_hp_more_node,find_player_for_chase_node, move_to_player_node)

        eat_ball_node = SequenceNode("Eat Ball")
        eat_ball_node.add_children(find_ball_node,move_to_ball_node)

        runaway_chase_eatball_node = SelectorNode("RunawayChaseEatBall")
        runaway_chase_eatball_node.add_children(chase_node,eat_ball_node,runaway_node)

        self.bt = BehaviorTree(runaway_chase_eatball_node)
        pass




    def get_bb(self):
        return self.x - 35, self.y - 50, self.x + 35, self.y + 40

    def update(self):
        self.bt.run()
        pass


    def draw(self):
        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].draw(self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 60, self.y + 50, '(HP: %3.0f)' % self.hp, (255, 255, 0))
    def handle_event(self, event):
        pass

