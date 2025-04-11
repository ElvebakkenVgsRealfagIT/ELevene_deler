import pygame as pg
import math

pg.init()
font = pg.font.SysFont("Tahoma", 16)

class Start_pause_knapp:

    def __init__(self):
        self.pauset = True

    def oppdater(self, pos):
        self.rect = pg.rect.Rect(self.x, self.y, self.HØYDE, self.BREDDE)
        if self.rect.collidepoint(pos):
             self.pauset = not self.pauset
         
    def tegn(self, vindu, x , y, høyde = 40, farge = (255, 255, 255)):
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
            
class Slider:

    instanser = []

    def __init__(self, start_range, end_range, overskrift, nøyaktighet):

        self.start_range = start_range
        self.end_range = end_range
        self.verdi = (self.start_range+self.end_range)/2
        self.overskrift = overskrift
        self.lengde = 130
        self.høyde = 7
        self.oppdatert = False
        self.nøyaktighet = nøyaktighet
        Slider.instanser.append(self)

    def tegn(self, vindu, x, y):

        self.x = x
        self.y = y
        self.vindu = vindu
        self.rect = pg.Rect(x, y, self.lengde, self.høyde)
        pg.draw.rect(vindu, (140, 140, 140), self.rect, border_radius=5)
        self.tekst = font.render(self.overskrift, True, (0, 0, 0), None)
        self.tall_tekst = font.render(f"{self.verdi}", True, (0, 0, 0), None)
        self.tekst_rect = self.tekst.get_rect(center=(x + int(round(self.lengde/2, 0)), y-15))
        self.tall_rect = self.tall_tekst.get_rect(center=(x + int(round(self.lengde/2, 0)), y+20))
        vindu.blit(self.tall_tekst, self.tall_rect.topleft)
        vindu.blit(self.tekst, self.tekst_rect.topleft)
    
    def oppdater_slider(self, events):

        for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    mus_x, mus_y = pg.mouse.get_pos()
                    if self.rect.collidepoint((mus_x, mus_y)):
                        self.slider_x = mus_x
                        self.oppdatert = True
                        
        if not self.oppdatert:
            self.slider_x = self.x + self.lengde / 2

        self.slider_sirkel(self.slider_x)
        self.verdi = round((self.slider_x-self.x)/self.lengde*(self.end_range-self.start_range) + self.start_range, self.nøyaktighet)

    def slider_sirkel(self, x):          
        pg.draw.circle(self.vindu, (100, 100, 100), (x, self.y+4), 8)