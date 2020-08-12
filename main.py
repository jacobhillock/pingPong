#!venv/bin/python

import pygame
from seven_seg import seven_seg
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
    QUIT,
    VIDEORESIZE,
    RESIZABLE
)

def get_segments(scores):
    score1 = str(scores[0])
    if(len(score1) < 2):
        score1 = "0" + score1
    
    score2 = str(scores[1])
    if(len(score2) < 2):
        score2 = "0" + score2

    displays = []

    np  = int(.275*scale)  # number padding
    nw  = 14*scale        # number width
    displays.append(seven_seg(score1[-2], int(hWidth/2)   - (np+nw), baseY, scale))
    displays.append(seven_seg(score1[-1], int(hWidth/2)   + (np)   , baseY, scale))
    displays.append(seven_seg(score2[-2], int(3*hWidth/2) - (np+nw), baseY, scale))
    displays.append(seven_seg(score2[-1], int(3*hWidth/2) + (np)   , baseY, scale))

    return displays

def updateSize(resize):
    global height, width, hWidth, size, scale
    height = resize.h
    width = resize.w
    hWidth = int(width/2)
    size = width, height
    rescale()

def rescale():
    global scale
    scaleH = height * 30 / 1080
    scaleW = width  * 30 / 1920
    scale = scaleW if scaleW < scaleH else scaleH

def load_config():
    config = {}
    loc = __file__.split("main.py")
    with open(f"{loc[0]}config.json") as file:
        config = json.load(file)
    return config

def calc_delta(t0, t1, aim):
    wait = aim - (t1 - t0)*1000
    return int(wait)

config = load_config ()
FPS = config.get("FPS", 15)
delta = int(1000/FPS)
height = config.get("height", 720)
width = config.get("width", 1280)
hWidth = int(width/2)
size = width, height
MAX_SCORE = config.get("win_score", 11)
baseX = 10
baseY = 10
scale = 5

init()
pygame.font.init()
my_font = pygame.font.SysFont('Nato Mono', config.get("font_size", 64))

scores = [0, 0]
games = [0, 0]
display = pygame.display.set_mode(size, RESIZABLE)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255,255,255)

display.fill(black)
start_server = random.choice([0,2])
current_server = start_server
change = False
p1LEFT = True
p1 = config.get('p1','Player 1')
p2 = config.get('p2','Player 2')
do_player_switching = config.get("do_player_switching", True)
do_server_tracking = config.get("do_server_tracking", True)

rescale ()
t0 = t1 = 0
while(True):
    pygame.time.delay(calc_delta(t0, t1, delta))
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
    
    if do_server_tracking:
        y_off = int(baseY + 27*scale)
        if current_server % 4 == 0 or current_server % 4 == 1:
            pygame.draw.rect(display, (0, 240, 60), pygame.Rect(0, y_off,hWidth,30))
        else:
            pygame.draw.rect(display, (0, 240, 60), pygame.Rect(hWidth, y_off,hWidth,30))
    
    textsurface1 = my_font.render(f"{p1} score {games[0]}", True, (255,255,255))
    textsurface2 = my_font.render(f"{p2} score {games[1]}", True, (255,255,255))
    if do_player_switching and not p1LEFT:
        textsurface1 = my_font.render(f"{p2} score {games[1]}", True, (255,255,255))
        textsurface2 = my_font.render(f"{p1} score {games[0]}", True, (255,255,255))
    w1 = textsurface1.get_size()[0]
    w2 = textsurface2.get_size()[0]
    l1 = int(hWidth/2-w1/2)
    l2 = int(3*hWidth/2-w2/2)
    display.blit(
        textsurface1,
        (
            int(l1),
            int(baseY + 30*scale)
        )
    )
    display.blit(
        textsurface2,
        (
            int(l2),
            int(baseY + 30*scale)
        )
    )

    pygame.draw.rect(display, (255,255,255), pygame.Rect(hWidth-5,0,10,height))
    pygame.display.update()

    # EVENT LOOP
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            updateSize(event)
            display = pygame.display.set_mode(size, RESIZABLE)

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
                if scores[0] >= MAX_SCORE or scores[1] >= MAX_SCORE:
                    if p1LEFT or not do_player_switching:
                        if scores[0] >= MAX_SCORE and scores[0] > scores[1]:
                            games[0] += 1
                        elif scores[1] >= MAX_SCORE:
                            games[1] += 1
                    else:
                        if scores[0] >= MAX_SCORE and scores[0] > scores[1]:
                            games[1] += 1
                        elif scores[1] >= MAX_SCORE:
                            games[0] += 1
                    if not change and do_player_switching:
                        p1LEFT = not p1LEFT
                    else:
                        start_server += 2
                    start_server %= 4
                    change = not change

                current_server = start_server
                scores = [0, 0]
            
            if keys[K_q]:
                sys.exit()

        if event.type == QUIT:
            sys.exit()
    t1 = time.time()
    # EVENT LOOP

