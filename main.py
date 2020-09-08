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
    displays += seven_seg(score1[-2], int(config.hWidth/2)   - (np+nw), config.padding, config.scale)
    displays += seven_seg(score1[-1], int(config.hWidth/2)   + (np)   , config.padding, config.scale)
    displays += seven_seg(score2[-2], int(3*config.hWidth/2) - (np+nw), config.padding, config.scale)
    displays += seven_seg(score2[-1], int(3*config.hWidth/2) + (np)   , config.padding, config.scale)

    return displays

def updateSize(resize):
    global config
    config.size = resize.w, resize.h
    config.hWidth = int(resize.w/2)
    rescale()

def rescale():
    global config
    scaleH = config.size[1] * 30 / 1080
    scaleW = config.size[0]  * 30 / 1920
    config.scale = scaleW if scaleW < scaleH else scaleH

def load_config():
    global config
    loc = __file__.split("main.py")
    with open(f"{loc[0]}config.json") as file:
        config = Configurator(file)

def clean(items):
    items["win_score"] = int(items["win_score"])
    if items["do_player_switching"].lower() == 'false':
        items["do_player_switching"] = False
    else:
        items["do_player_switching"] = True
    return items

def update_config(screen):
    global config
    y = 20
    with open("config.json", "r+") as file:
        items = json.load(file)
        boxs = []
        for k in items.keys():
            # print(f"{k}:{items[k]}")
            boxs.append(TextBox(20, y, 150, 30, display, str(items[k]), k))
            y += 75
        
        button = Button(20, y, 150, 30, display, text='Done')
        done = False
        clock = pygame.time.Clock()
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                for box in boxs:
                    box.handle_event(event)
                done = button.handle_event(event)

            for box in boxs:
                box.update()

            display.fill((0, 0, 0))
            for box in boxs+[button]:
                box.draw(display)
            
            pygame.display.flip()
            clock.tick(30)
        
        # take new config items from boxs
        for box in boxs:
            items[box.title] = box.text
        # clean up items
        items = clean(items)

        # update config
        config.update(items)

        # update config file
        file.seek(0)
        file.write(json.dumps(items))
        file.truncate()

def calc_delta(t0, t1, aim):
    wait = aim - (t1 - t0)*1000
    return int(wait)

# Main program start
# TODO: make def main()
load_config ()
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
    for seg in get_segments(scores):
        rect = pygame.Rect(
            int(seg[0]),
            int(seg[1]),
            int(seg[2]),
            int(seg[3])
        )
        pygame.draw.rect(display, white, rect)
    
    y_off = int(config.padding + 27*config.scale)
    if current_server % 4 == 0 or current_server % 4 == 1:
        pygame.draw.rect(display, (0, 240, 60), pygame.Rect(0, y_off,config.hWidth,30))
    else:
        pygame.draw.rect(display, (0, 240, 60), pygame.Rect(config.hWidth, y_off,config.hWidth,30))
    
    # TODO: Left string and right string
    left_string = f"{config.p[0]} score {games[0]}"
    right_string = f"{config.p[1]} score {games[1]}"
    if config.do_player_switching and not p1LEFT:
        left_string = f"{config.p[1]} score {games[1]}"
        right_string = f"{config.p[0]} score {games[0]}"
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
            int(config.padding + 30*config.scale)
        )
    )
    display.blit(
        textsurface2,
        (
            int(l2),
            int(config.padding + 30*config.scale)
        )
    )

    pygame.draw.rect(display, (255,255,255), pygame.Rect(config.hWidth-5,0,10,config.size[1]))
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
            
            if keys[K_c]:
                update_config(display)

        if event.type == QUIT:
            sys.exit()
    t1 = time.time()
    # EVENT LOOP

