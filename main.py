#!venv/bin/python

import pygame
from src.seven_seg import seven_seg
from src.textbox_pg import TextBox
from src.button_pg import Button 
from src.conf import Configurator
import sys, random, json, sys, os, time
from pygame import (
    init,
    KEYDOWN,
    K_F1,
    K_F2,
    K_F6,
    K_F7,
    K_F11,
    K_F12,
    K_q,
    K_c,
    QUIT,
    VIDEORESIZE,
    RESIZABLE
)

global config

def get_segments(scores):
    score1 = str(scores[0])
    if(len(score1) < 2):
        score1 = "0" + score1
    
    score2 = str(scores[1])
    if(len(score2) < 2):
        score2 = "0" + score2

    displays = []

    np  = int(.275*config.scale)  # number padding
    nw  = 14*config.scale        # number width
    displays.append(seven_seg(score1[-2], int(config.hWidth/2)   - (np+nw), config.baseY, config.scale))
    displays.append(seven_seg(score1[-1], int(config.hWidth/2)   + (np)   , config.baseY, config.scale))
    displays.append(seven_seg(score2[-2], int(3*config.hWidth/2) - (np+nw), config.baseY, config.scale))
    displays.append(seven_seg(score2[-1], int(3*config.hWidth/2) + (np)   , config.baseY, config.scale))

    return displays

def updateSize(resize):
    global config
    config.height = resize.h
    config.width = resize.w
    config.hWidth = int(config.width/2)
    config.size = config.width, config.height
    rescale()

def rescale():
    global config
    scaleH = config.height * 30 / 1080
    scaleW = config.width  * 30 / 1920
    config.scale = scaleW if scaleW < scaleH else scaleH

def load_config():
    config = {}
    loc = __file__.split("main.py")
    with open(f"{loc[0]}config.json") as file:
        config = Configurator(file)
    return config

def reload():
    pass

def update_config(screen):
    # screen = pygame.display.set_mode([300, 800])
    # display.fill((0, 0, 0))
    y = 20
    with open("config.json") as file:
        items = json.load(file)
        boxs = []
        for k in items.keys():
            # print(f"{k}:{items[k]}")
            boxs.append(TextBox(20, y, 150, 30, display, str(items[k]), k))
            y += 40
        
        button = Button(20, y, 150, 30, display, text='Done')
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                for box in boxs:
                    box.handle_event(event)
                done = button.handle_event(event)

            for box in boxs:
                box.update()

            display.fill((0, 0, 0))
            for box in boxs+[button]:
                box.draw(display)


def calc_delta(t0, t1, aim):
    wait = aim - (t1 - t0)*1000
    return int(wait)

config = load_config ()
init()
my_font = pygame.font.SysFont('Nato Mono', config.font_size)

scores = [0, 0]
games = [0, 0]
display = pygame.display.set_mode(config.size, RESIZABLE)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255,255,255)

start_server = random.choice([0,2])
current_server = start_server
change = False
p1LEFT = True
rescale ()
t0 = t1 = 0
while(True):
    pygame.time.delay(calc_delta(t0, t1, config.delta))
    t0 = time.time()
    display.fill(black)
    for num in get_segments(scores):
        for seg in num:
            rect = pygame.Rect(
                int(seg[0]),
                int(seg[1]),
                int(seg[2]),
                int(seg[3])
            )
            pygame.draw.rect(display, white, rect)
    
    if config.do_server_tracking:
        y_off = int(config.baseY + 27*config.scale)
        if current_server % 4 == 0 or current_server % 4 == 1:
            pygame.draw.rect(display, (0, 240, 60), pygame.Rect(0, y_off,config.hWidth,30))
        else:
            pygame.draw.rect(display, (0, 240, 60), pygame.Rect(config.hWidth, y_off,config.hWidth,30))
    
    # TODO: Left string and right string
    left_string = f"{config.p1} score {games[0]}"
    right_string = f"{config.p2} score {games[1]}"
    if config.do_player_switching and not p1LEFT:
        left_string = f"{config.p2} score {games[1]}"
        right_string = f"{config.p1} score {games[0]}"
    textsurface1 = my_font.render(left_string, True, (255,255,255))
    textsurface2 = my_font.render(right_string, True, (255,255,255))

    w1 = textsurface1.get_size()[0]
    w2 = textsurface2.get_size()[0]
    l1 = int(config.hWidth/2-w1/2)
    l2 = int(3*config.hWidth/2-w2/2)
    display.blit(
        textsurface1,
        (
            int(l1),
            int(config.baseY + 30*config.scale)
        )
    )
    display.blit(
        textsurface2,
        (
            int(l2),
            int(config.baseY + 30*config.scale)
        )
    )

    pygame.draw.rect(display, (255,255,255), pygame.Rect(config.hWidth-5,0,10,config.height))
    pygame.display.update()

    # EVENT LOOP
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            updateSize(event)
            display = pygame.display.set_mode(config.size, RESIZABLE)

        if event.type == KEYDOWN:
            keys=pygame.key.get_pressed()
            if keys[K_F1]:
                scores[0] -= 1
                current_server -= 1
            elif keys[K_F2]:
                scores[0] += 1
                current_server += 1
            elif keys[K_F11]:
                scores[1] -= 1
                current_server -= 1
            elif keys[K_F12]:
                scores[1] += 1
                current_server += 1
            
            if keys[K_F6] or keys[K_F7]:
                if scores[0] >= config.MAX_SCORE or scores[1] >= config.MAX_SCORE:
                    if p1LEFT or not config.do_player_switching:
                        if scores[0] >= config.MAX_SCORE and scores[0] > scores[1]:
                            games[0] += 1
                        elif scores[1] >= config.MAX_SCORE:
                            games[1] += 1
                    else:
                        if scores[0] >= config.MAX_SCORE and scores[0] > scores[1]:
                            games[1] += 1
                        elif scores[1] >= config.MAX_SCORE:
                            games[0] += 1
                    if not change and config.do_player_switching:
                        p1LEFT = not p1LEFT
                    else:
                        start_server += 2
                    start_server %= 4
                    change = not change

                current_server = start_server
                scores = [0, 0]
            
            if keys[K_q]:
                sys.exit()
            
            # if keys[K_c]:
            #     update_config(display)

        if event.type == QUIT:
            sys.exit()
    t1 = time.time()
    # EVENT LOOP

