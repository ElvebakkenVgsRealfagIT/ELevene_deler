#Kommentert av chat 

import pygame as pg  # Importerer pygame-biblioteket

# ----------------------- Celle-klasse -----------------------
class Celle:
    STØRRELSE = 20               # Størrelsen (bredde og høyde) på hver celle i piksler
    instanser = []               # Liste som holder styr på alle opprettede celler

    def __init__(self, x_koord, y_koord):
        # Grid-koordinater (rad og kolonne)
        self.x_koord, self.y_koord = x_koord, y_koord

        # Piksel-koordinater basert på posisjon i grid og størrelse
        self.x = self.x_koord * Celle.STØRRELSE
        self.y = self.y_koord * Celle.STØRRELSE

        # pygame-rect som representerer celleområdet
        self.rect = pg.rect.Rect(self.x, self.y, Celle.STØRRELSE, Celle.STØRRELSE)

        # Legger denne cellen til i felleslisten over celler
        Celle.instanser.append(self)

    def tegn(self, farge = (255, 255, 255)):
        # Tegner cellen med fyllfarge
        pg.draw.rect(vindu, farge, self.rect)

        # Tegner svart kant rundt cellen
        pg.draw.rect(vindu, (0, 0, 0), self.rect, width=1)

# ----------------------- Brett-klasse -----------------------
class Brett:
    def __init__(self):
        self.grid = []    # 2D-liste med celler

        # Fyller brettet med celler basert på størrelse og skjermdimensjoner
        for x in range(int(BREDDE / Celle.STØRRELSE)):
            self.grid.append([])
            for y in range(int(HØYDE / Celle.STØRRELSE)):
                self.grid[x].append(Celle(x, y))

    def tegn(self):
        # Tegner alle cellene i instans-listen
        for celle in Celle.instanser:
            celle.tegn()

# ----------------------- Oppsett og hovedløkke -----------------------

BREDDE, HØYDE = 800, 600                        # Størrelse på vinduet
vindu = pg.display.set_mode((BREDDE, HØYDE))    # Oppretter pygame-vindu
brett = Brett()                                 # Lager et brett med celler
run = True                                      # Kontrollvariabel for while-løkka

# Hovedløkke som kjører programmet
while run:
    events = pg.event.get()  # Henter hendelser fra pygame (tastetrykk, museklikk, osv.)

    brett.tegn()             # Tegner alle cellene

    # Går gjennom hendelser og avslutter programmet hvis vinduet lukkes
    for event in events:
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()        # Oppdaterer skjermen med det som er tegnet
