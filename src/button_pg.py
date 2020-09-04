import pygame as pg


pg.init()

class Button:

    def __init__(self, x, y, w, h, screen, 
            text='', ci=pg.Color('lightskyblue3'), ca=pg.Color('dodgerblue2'), font=pg.font.Font(None, 32)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(x, y, w, h)
        self.color  = ci
        self.colorI = ci
        self.colorA = ca
        self.font = font
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def over (self):
        mouse = pg.mouse.get_pos()
        return self.x <= mouse[0] <= self.x+self.w and self.y <= mouse[1] <= self.y+self.h

    def handle_event(self, event):
        return event.type == pg.MOUSEBUTTONDOWN and self.over()


    def draw(self, screen):
        # Change the current color of the button
        self.color = self.colorA if self.over() else self.colorI
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    button = Button(20, 20, 150, 30, screen, text='Done')
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            print(button.handle_event(event))

        # button.update()

        screen.fill((30, 30, 30))
        button.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()