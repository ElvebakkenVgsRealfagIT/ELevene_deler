import random as r
import time
import pygame as pg

class Person:

    def __init__(self, x, y, tilstand="Smittet"):

        self.x = x
        self.y = y
        self.tilstand = tilstand
        self.dager_smittet = 1
        self.dager_syk = 0
        populasjon.befolkning.append(self)
        populasjon.koords.append((self.x, self.y))
    
    def __str__(self):
        return f"Jeg er {self.tilstand}"

    def oppdater(self):

        if self.tilstand == "Smittet": 
            if self.dager_smittet >= 3:
                self.tilstand = "Syk"
                self.dager_syk = 1
            else: 
                self.dager_smittet += 1

        elif self.tilstand == "Syk":
            if r.randint(0, 1000) in range(0, round(dødsrate_glider.verdi*10)):
                self.tilstand = "Død"
            if self.dager_syk >= 4:
                self.tilstand = "Frisk_med_immunitet"
            else: 
                self.dager_syk += 1
    
    def tegn(self):
        
        if self.tilstand == "Smittet":  
            pg.draw.rect(vindu, (255, 150, 150), (self.x, self.y, rute_sidelengde, rute_sidelengde))
            pg.draw.line(vindu, (0, 0, 0), (self.x + rute_sidelengde/5, self.y + rute_sidelengde/5), (self.x + rute_sidelengde - rute_sidelengde/5, self.y + rute_sidelengde - rute_sidelengde/5), 2)
        elif self.tilstand == "Syk":
            pg.draw.rect(vindu, (255, 0, 0), (self.x, self.y, rute_sidelengde, rute_sidelengde))
            pg.draw.line(vindu, (255, 255, 255), (self.x + rute_sidelengde - rute_sidelengde/5, self.y + rute_sidelengde/5), (self.x + rute_sidelengde/5, self.y + rute_sidelengde - rute_sidelengde/5), 2)
        elif self.tilstand == "Død":
            pg.draw.rect(vindu, (0, 0, 0), (self.x, self.y, rute_sidelengde, rute_sidelengde))
        elif self.tilstand == "Frisk_med_immunitet":
            pg.draw.rect(vindu, (80, 80, 80), (self.x, self.y, rute_sidelengde, rute_sidelengde))
            pg.draw.circle(vindu, (255, 255, 255), (self.x + rute_sidelengde/2, self.y + rute_sidelengde/2), rute_sidelengde/10)

class Populasjon: 
    
    def __init__(self):
        
        self.befolkning = []
        self.koords = []
    
    def smitteforløp(self, smittesannsynlighet):

        for person in self.befolkning.copy():

            if person.tilstand != "Frisk_med_immunitet" and person.tilstand != "Død":
                if (person.x + rute_sidelengde, person.y) not in populasjon.koords:
                    if r.randint(0, 100) in range(0, round(smittesannsynlighet*100)):
                        Person(person.x + rute_sidelengde, person.y)
                if (person.x, person.y + rute_sidelengde) not in populasjon.koords:
                    if r.randint(0, 100) in range(0, round(smittesannsynlighet*100)):
                        Person(person.x, person.y + rute_sidelengde)
                if (person.x - rute_sidelengde, person.y) not in populasjon.koords:
                    if r.randint(0, 100) in range(0, round(smittesannsynlighet*100)):
                        Person(person.x - rute_sidelengde, person.y)
                if (person.x, person.y  - rute_sidelengde) not in populasjon.koords:
                    if r.randint(0, 100) in range(0, round(smittesannsynlighet*100)):
                        Person(person.x, person.y - rute_sidelengde)

class Glider:

    instanser = []

    def __init__(self, start_range, end_range, overskrift, nøyaktighet):

        self.start_range = start_range
        self.end_range = end_range
        self.verdi = (self.start_range+self.end_range)/2
        self.overskrift = overskrift
        self.lengde = 130
        self.høyde = 7
        self.glider_x = BREDDE-95
        self.nøyaktighet = nøyaktighet
        Glider.instanser.append(self)

    def tegn(self, x, y):

        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, self.lengde, self.høyde)
        pg.draw.rect(vindu, (140, 140, 140), self.rect, border_radius=5)
        self.tekst = font_obj.render(self.overskrift, True, (0, 0, 0), None)
        self.tall_tekst = font_obj.render(f"{self.verdi}", True, (0, 0, 0), None)
        self.tekst_rect = self.tekst.get_rect(center=(BREDDE-95, y-15))
        self.tall_rect = self.tall_tekst.get_rect(center=(BREDDE-95, y+20))
        vindu.blit(self.tall_tekst, self.tall_rect.topleft)
        vindu.blit(self.tekst, self.tekst_rect.topleft)
    
    def oppdater_glider(self, eventss):

        for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    mus_x, mus_y = pg.mouse.get_pos()
                    if self.rect.collidepoint((mus_x, mus_y)):
                        self.glider_x = mus_x

        self.glider_sirkel(self.glider_x)
        self.verdi = round((self.glider_x-self.x)/self.lengde*self.end_range, self.nøyaktighet)

    def glider_sirkel(self, x):          
        pg.draw.circle(vindu, (100, 100, 100), (x, self.y+4), 8)

def rutenett():

    x = 0
    y = 0
    fortsett_x = True
    fortsett_y = True
    
    while fortsett_x:
        if x > BREDDE:
            fortsett_x = False
        else: 
            pg.draw.line(vindu, (255, 255, 255), (x, 0), (x, HØYDE))
            x += rute_sidelengde

    while fortsett_y:
        if y > HØYDE:
            fortsett_y = False
        else: 
            pg.draw.line(vindu, (255, 255, 255), (0, y), (BREDDE, y))
            y += rute_sidelengde

pg.init()
rute_sidelengde = 10
BREDDE, HØYDE = rute_sidelengde*61, rute_sidelengde*61
vindu = pg.display.set_mode((BREDDE, HØYDE))
run = True

font_obj = pg.font.Font(None, 20)
font_overskrift = pg.font.Font(None, 35)
info_font = pg.font.Font(None, 28)


tidligere_tick = time.time()
dag_count = 0

smitterate_glider = Glider(0, 1, "Smitterate", 2)
dødsrate_glider = Glider(0, 10, "Dødsrate/dag (%)", 1)
hastighet_glider = Glider(0, 2, "Hastighet", 2)

populasjon = Populasjon()
patient_zero = Person(BREDDE/2-rute_sidelengde/2, HØYDE/2-rute_sidelengde/2, "Syk")

while run: 

    vindu.fill((200, 200, 200))
    rutenett()

    for person in populasjon.befolkning:
        person.tegn()

    if time.time() - tidligere_tick >= (1/hastighet_glider.verdi**2):

        dag_count += 1 
        populasjon.smitteforløp(smitterate_glider.verdi)
        for person in populasjon.befolkning:
            person.oppdater()
        tidligere_tick = time.time()

    pg.draw.rect(vindu, (255, 255, 255), (BREDDE-170, HØYDE-220, 150, 200), border_radius=15)

    smitterate_glider.tegn(BREDDE - 160, HØYDE - 180)
    dødsrate_glider.tegn(BREDDE - 160, HØYDE - 120)
    hastighet_glider.tegn(BREDDE - 160, HØYDE - 60)

    overskrift = font_overskrift.render("Sykdomsimulator", True, (0, 0, 0))
    dager_passert = info_font.render(f"Dager passert: {dag_count}", True, (0, 0, 0))
    antall_tilfeller = info_font.render(f"Antall tilfeller: {len(populasjon.befolkning)}", True, (0, 0, 0))

    dødscount = 0

    for person in populasjon.befolkning:
        if person.tilstand == "Død":
            dødscount += 1
    
    antall_dødsfall = info_font.render(f"Antall dødsfall: {dødscount}", True, (0, 0, 0))

    vindu.blit(overskrift, (20, 20))
    vindu.blit(dager_passert, (BREDDE-200, 20))
    vindu.blit(antall_tilfeller, (BREDDE-200, 50))
    vindu.blit(antall_dødsfall, (BREDDE-200, 80))

    events = pg.event.get()
    
    for glider in Glider.instanser:
        glider.oppdater_glider(events)

    for event in events:
        if event.type == pg.QUIT:
            run = False

    pg.display.flip() 

    


