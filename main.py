#!venv/bin/python
import pygame
from seven_seg import seven_seg
import sys, random, json, sys, os
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
    QUIT
)

config = {}
loc = __file__.split("main.py")
with open(f"{loc[0]}config.json") as file:
    config = json.load(file)

FPS = config.get("FPS", 30)
height = config.get("height", 720)
width = config.get("width", 1280)
hWidth = int(width/2)
size = width, height
MAX_SCORE = config.get("win_score", 11)
baseX = 10
baseY = 10
scale = config.get("scale", 20)

init()
pygame.font.init()
my_font = pygame.font.SysFont('Nato Mono', config.get("font_size", 48))

def get_segments(score1: int, score2: int):
    score1 = str(score1)
    if(len(score1) < 2):
        score1 = "0" + score1
    
    score2 = str(score2)
    if(len(score2) < 2):
        score2 = "0" + score2

    displays = []
    displays.append(seven_seg(score1[0], int(baseX), baseY, scale))
    displays.append(seven_seg(score1[1], int(baseX + 59*scale/4), baseY, scale))
    displays.append(seven_seg(score2[0], int(baseX + 135*scale/4), baseY, scale))
    displays.append(seven_seg(score2[1], int(baseX + 194*scale/4), baseY, scale))

    return displays

def main():
    scores = [0, 0]
    games = [0, 0]
    display = pygame.display.set_mode(size)
    black = pygame.Color(0, 0, 0)
    display.fill(black)
    white = pygame.Color(255,255,255)
    start_server = random.choice([0,2])
    current_server = start_server
    change = False
    p1LEFT = True
    p1 = config.get('p1','Player 1')
    p2 = config.get('p2','Player 2')
    do_player_switching = config.get("do_player_switching", True)
    do_server_tracking = config.get("do_server_tracking", True)

    while(True):
        pygame.time.delay(int(1000/FPS))
        display.fill(black)
        for num in get_segments(scores[0], scores[1]):
            for seg in num:
                rect = pygame.Rect(seg[0], seg[1], seg[2], seg[3])
                pygame.draw.rect(display, white, rect)
        
        if do_server_tracking:
            if current_server % 4 == 0 or current_server % 4 == 1:
                pygame.draw.rect(display, (0, 240, 60), pygame.Rect(baseX, baseY + 27*scale,hWidth-10,30))
            else:
                pygame.draw.rect(display, (0, 240, 60), pygame.Rect(baseX + hWidth, baseY + 27*scale,hWidth-10,30))
        
        if do_player_switching:
            if p1LEFT:
                textsurface1 = my_font.render(f"{p1} score {games[0]}", True, (255,255,255))
                textsurface2 = my_font.render(f"{p2} score {games[1]}", True, (255,255,255))
                display.blit(textsurface1, (baseX + 9*scale, baseY + 30*scale))
                display.blit(textsurface2, (baseX + 9*scale + int(hWidth*1.04), baseY + 30*scale))
            else:
                textsurface2 = my_font.render(f"{p1} score {games[0]}", True, (255,255,255))
                textsurface1 = my_font.render(f"{p2} score {games[1]}", True, (255,255,255))
                display.blit(textsurface1, (baseX + 9*scale, baseY + 30*scale))
                display.blit(textsurface2, (baseX + 9*scale + int(hWidth*1.04), baseY + 30*scale))
        else:
            textsurface1 = my_font.render(f"{p1} score {games[0]}", True, (255,255,255))
            textsurface2 = my_font.render(f"{p2} score {games[1]}", True, (255,255,255))
            display.blit(textsurface1, (baseX + 9*scale, baseY + 30*scale))
            display.blit(textsurface2, (baseX + 9*scale + int(hWidth*1.04), baseY + 30*scale))

        pygame.display.update()

        # EVENT LOOP
        for event in pygame.event.get():
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
                            if scores[0] >= MAX_SCORE:
                                games[0] += 1
                            else:
                                games[1] += 1
                        else:
                            if scores[0] >= MAX_SCORE:
                                games[1] += 1
                            else:
                                games[0] += 1
                        if not change and do_player_switching:
                            p1LEFT = not p1LEFT
                        else:
                            start_server += 2
                        start_server %= 4
                        current_server = start_server
                        change = not change


                    scores = [0, 0]
                
                if keys[K_q]:
                    sys.exit()

            if event.type == QUIT:
                sys.exit()
        # EVENT LOOP


if __name__ == '__main__':
    main()
