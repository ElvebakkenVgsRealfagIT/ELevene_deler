import pygame as pg
import math

class Start_pause_knapp:

    def __init__(self):
        self.pauset = True

    def oppdater(self, pos):
        self.rect = pg.rect.Rect(self.x, self.y, self.HØYDE, self.BREDDE)
        if self.rect.collidepoint(pos):
             self.pauset = not self.pauset
         
    def tegn(self, vindu, farge, x , y, høyde):
        self.HØYDE = høyde
        self.BREDDE = int(round(math.sqrt(self.HØYDE**2-(self.HØYDE/2)**2), 0))
        self.x = x
        self.y = y
        if self.pauset:
            pg.draw.polygon(vindu, farge, [(x, y), (x, y + self.HØYDE), (x + self.BREDDE, y + self.HØYDE/2)])
            pg.draw.polygon(vindu, (0, 0, 0), [(x, y), (x, y + self.HØYDE), (x + self.BREDDE, y + self.HØYDE/2)], width=2)
        else:
             rect_bredde = int(round(self.HØYDE/4, 0))
             pg.draw.rect(vindu, farge, (self.x, self.y, rect_bredde, self.HØYDE))
             pg.draw.rect(vindu, farge, (self.x + 2 * rect_bredde, self.y, rect_bredde, self.HØYDE))
             pg.draw.rect(vindu, (0, 0, 0), (self.x, self.y, rect_bredde, self.HØYDE), width = 2)
             pg.draw.rect(vindu, (0, 0, 0), (self.x + 2 * rect_bredde, self.y, rect_bredde, self.HØYDE), width = 2)