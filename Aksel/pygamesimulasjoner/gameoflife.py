import pygame as pg
import random as r
import time
from pg_knapp_klasser import Start_pause_knapp
from graf_knapp_klasser import Knapp

class Celle:
    STØRRELSE = 25
    FARGE_DØD = (10, 10, 30)
    FARGE_LEVENDE = (150, 255, 150)

    def __init__(self, x, y):
        if r.randint(0, 3) == 1:
            self.levende = True
        else: 
            self.levende = False
        self.rect = pg.rect.Rect(x, y, Celle.STØRRELSE, Celle.STØRRELSE)
        self.x = x
        self.y = y
        self.antall_naboer = 0
        populasjon.celler.append(self)

    def endre_tilstand(self):
        if self.antall_naboer == 3:
            self.levende = True
        elif self.antall_naboer > 3 or self.antall_naboer < 2:
            self.levende = False

    def tegn(self):
        if not self.levende:
            pg.draw.rect(vindu, Celle.FARGE_DØD, self.rect)
        else: 
            pg.draw.rect(vindu, Celle.FARGE_LEVENDE, self.rect)
        pg.draw.rect(vindu, (0, 0, 0), (self.rect), width = 1)    

class Populasjon:
    def __init__(self):
        self.celler = []

    def oppdater(self):
        for i in range(len(self.celler)):
            self.celler[i].antall_naboer = 0
            for j in range(len(self.celler)):
                if (self.celler[i].x == self.celler[j].x - Celle.STØRRELSE and self.celler[i].y == self.celler[j].y) or (self.celler[i].x == self.celler[j].x + Celle.STØRRELSE and self.celler[i].y == self.celler[j].y) or (self.celler[i].x == self.celler[j].x and self.celler[i].y == self.celler[j].y - Celle.STØRRELSE) or (self.celler[i].x == self.celler[j].x and self.celler[i].y == self.celler[j].y + Celle.STØRRELSE) or (self.celler[i].x == self.celler[j].x + Celle.STØRRELSE and self.celler[i].y == self.celler[j].y + Celle.STØRRELSE) or (self.celler[i].x == self.celler[j].x + Celle.STØRRELSE and self.celler[i].y == self.celler[j].y - Celle.STØRRELSE) or (self.celler[i].x == self.celler[j].x - Celle.STØRRELSE and self.celler[i].y == self.celler[j].y + Celle.STØRRELSE) or (self.celler[i].x == self.celler[j].x - Celle.STØRRELSE and self.celler[i].y == self.celler[j].y - Celle.STØRRELSE): 
                    if self.celler[j].levende == True:
                        self.celler[i].antall_naboer += 1

def initier_celler():
    for x in range(0, BREDDE, Celle.STØRRELSE):
        for y in range(0, HØYDE, Celle.STØRRELSE):
            Celle(x, y)


BREDDE = 500
HØYDE = 500
run = True

vindu = pg.display.set_mode((BREDDE, HØYDE))
tidligere_tick = time.time()

populasjon = Populasjon()
initier_celler()
start_pause = Start_pause_knapp()
klarer_knapp = Knapp(BREDDE - 110, HØYDE - 80, "Klarer")
genererer_knapp = Knapp(BREDDE - 220, HØYDE - 80, "Randomiser")

while run: 

    pos = None 

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()

    for celle in populasjon.celler:
        celle.tegn()
        if pos != None:
            if celle.rect.collidepoint(pos):
                celle.levende = not celle.levende

    start_pause.tegn(vindu, (255, 255, 255), 40, 420, 40)
    klarer_knapp.tegn(vindu, (0, 0, 0))
    genererer_knapp.tegn(vindu, (0, 0, 0))

    if pos != None: 
        start_pause.oppdater(pos)
        if klarer_knapp.rektangel.collidepoint(pos):
            for celle in populasjon.celler:
                celle.levende = False
        if genererer_knapp.rektangel.collidepoint(pos):
            for celle in populasjon.celler:
                if r.randint(0, 3) == 1:
                    celle.levende = True
                else:
                    celle.levende = False

    if not start_pause.pauset:
        if time.time() - 1 >= tidligere_tick:
            populasjon.oppdater()
            for celle in populasjon.celler:
                celle.endre_tilstand()

            tidligere_tick = time.time()
    pg.display.flip()