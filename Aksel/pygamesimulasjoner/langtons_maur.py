import pygame as pg
import sys
import os
from pg_knapp_klasser import *
import time as t

class Celle:
    STØRRELSE = 12
    instanser = []

    def __init__(self, x_koord, y_koord):

        self.x_koord, self.y_koord = x_koord, y_koord
        self.x, self.y = self.x_koord * Celle.STØRRELSE, self.y_koord * Celle.STØRRELSE
        self.rect = pg.rect.Rect(self.x, self.y, Celle.STØRRELSE, Celle.STØRRELSE)
        self.farge = (255, 255, 255)
        Celle.instanser.append(self)

    def tegn(self, farge = None):

        if farge == None:
            farge = self.farge
        self.x, self.y = self.x_koord * Celle.STØRRELSE, self.y_koord * Celle.STØRRELSE
        self.rect = pg.rect.Rect(self.x, self.y, Celle.STØRRELSE, Celle.STØRRELSE)
        pg.draw.rect(vindu, farge, self.rect)
        pg.draw.rect(vindu, (0, 0, 0), self.rect, width = 1)

class Brett:

    def initier_grid(self): 
        self.grid = []
        for x in range(int(BREDDE / Celle.STØRRELSE)):
            self.grid.append([])
            for y in range(int(HØYDE / Celle.STØRRELSE)):
                self.grid[x].append(Celle(x, y))

    def __init__(self):

        self.initier_grid()

    def tegn(self):
                
        for celle in Celle.instanser:
            celle.tegn()

class Maur(Celle):
    
    def __init__(self):

        super().__init__(int(round(len(brett.grid) / 2, 0)), int(round(len(brett.grid[0]) / 2, 0)))
        self.vinkel = 90
    
    def roter(self, retning):

        if retning == "høyre":
            if self.vinkel == -90:
                self.vinkel = 180
            else:
                self.vinkel -= 90
        elif retning == "venstre":
            if self.vinkel == 180:
                self.vinkel = -90
            else:
                self.vinkel += 90
            
    def flytt(self):

        self.står_på = brett.grid[self.x_koord][self.y_koord]
        if self.står_på.farge == (255, 255, 255):
            self.står_på.farge = (0, 0, 0)
            self.roter("høyre")
        elif self.står_på.farge == (0, 0, 0):
            self.står_på.farge = (255, 255, 255)
            self.roter("venstre")
        
        if self.vinkel == 0:
            self.x_koord += 1
        elif self.vinkel == 90:
            self.y_koord -= 1
        elif self.vinkel == 180:
            self.x_koord -= 1
        elif self.vinkel == -90:
            self.y_koord += 1
    
        self.rect = pg.rect.Rect(self.x_koord * Celle.STØRRELSE, self.y_koord * Celle.STØRRELSE, Celle.STØRRELSE, Celle.STØRRELSE)

BREDDE, HØYDE = 1000, 650
vindu = pg.display.set_mode((BREDDE, HØYDE))
størrelse_slider = Slider(4, 20, "Cellestørrelse", 0)
størrelse = størrelse_slider.verdi
brett = Brett()
maur = Maur()
run = True
klokke = pg.time.Clock()
tids_slider = Slider(0, 16, "Hastighet", 1)
start_knapp = Start_pause_knapp()
prev_time = t.time()

while run:
    pos = None 
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()

    brett.tegn()
    maur.tegn((255, 0, 255))
    pg.draw.rect(vindu, (255, 255, 255), (BREDDE - 200, HØYDE - 200, 180, 180), border_radius= 20)
    tids_slider.tegn(vindu, BREDDE - 175, HØYDE - 160)
    tids_slider.oppdater_slider(events)
    størrelse_slider.tegn(vindu, BREDDE - 175, HØYDE - 100)
    størrelse_slider.oppdater_slider(events)
    start_knapp.tegn(vindu, 30, HØYDE - 70)

    if størrelse_slider.verdi != størrelse:
        Celle.STØRRELSE = størrelse_slider.verdi
        brett.initier_grid()
        størrelse = størrelse_slider.verdi

    if pos != None:
        start_knapp.oppdater(pos)
        for celle in Celle.instanser:
            if celle.rect.collidepoint(pos):
                celle.farge = (0, 0, 0)

    tick = 1 / (tids_slider.verdi**2)
    if t.time() - tick >= prev_time and not start_knapp.pauset:
        maur.flytt()
        prev_time = t.time()

    pg.display.flip()
