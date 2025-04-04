import pygame as pg

# Farger
TEKSTFARGE = (255, 255, 255)
MENYFARGE = (0, 0, 255)
HOVERFARGE = (100, 100, 150)

# Nedtrekksmeny
NEDTREKKS_BREDDE, NEDTREKKS_HOYDE = 200, 50

# Menyfelt
# MENYFELT_START = 400
# MENYFELT_BREDDE = 200

# Initialiserer/starter pygame
pg.init()

# Angir hvilken skrifttype og tekststørrelse vi vil bruke på tekst
font = pg.font.SysFont("Tahoma", 16)

class Knapp:
    instanser = []
    """Klasse for å representere en knapp"""
    def __init__(self, xPosisjon, yPosisjon, tekst):
        Knapp.instanser.append(self)
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.bredde = 100
        self.hoyde = 40
        self.tekst = tekst
        self.rektangel = pg.Rect(
            self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde
        )

    def tegn(self, vindu, farge):
        pg.draw.rect(vindu, farge, self.rektangel, border_radius=int(round(self.bredde/2, 0)))
        tekst = font.render(self.tekst, True, TEKSTFARGE)
        tekstRamme = tekst.get_rect(center=self.rektangel.center)
        vindu.blit(tekst, tekstRamme.topleft)

class Nedtrekksliste:
    instanser = []
    def __init__(self, xPosisjon, yPosisjon, alternativer, overskrift):
        Nedtrekksliste.instanser.append(self)
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.alternativer = alternativer
        self.aktiv = False
        self.overskrift = overskrift
        self.tekst = alternativer[0]
        self.bredde = 150
        self.hoyde = 40
        self.rektangel = pg.Rect(
            self.xPosisjon, self.yPosisjon, self.bredde + 10, self.hoyde
        )
    def lengsteTekst(self):
        # Returnerer lengden til det lengste alternativet
        lengst = 0
        for alternativ in self.alternativer:
            if len(alternativ) > lengst:
                lengst = len(alternativ) + 3    # Legger til litt pga forskyvning
        return lengst

    def tegn(self, vindu, farge):
        pg.draw.rect(vindu, farge, self.rektangel)
        rekt = self.rektangel
        tekst = font.render(self.tekst, True, TEKSTFARGE)
        overskrift = font.render(self.overskrift, True, (0, 0, 0))
        tekstRamme = tekst.get_rect(center=self.rektangel.center)
        tekstRamme.left = rekt.left + 10 # Venstrejusterer teksten
        tekstRamme.centery = rekt.centery  # Sentraliserer teksten vertikalt
        vindu.blit(tekst, tekstRamme.topleft)
        vindu.blit(overskrift, (tekstRamme.x-10, tekstRamme.y-40))

        if self.aktiv:
            i = 0
            for alternativ in self.alternativer:
                rekt = self.alternativRamme(i)
                pg.draw.rect(vindu, HOVERFARGE, rekt)
                tekst = font.render(alternativ, True, TEKSTFARGE)
                tekstRamme = tekst.get_rect(center=rekt.center)
                tekstRamme.left = rekt.left + 10 # Venstrejusterer teksten
                tekstRamme.centery = rekt.centery  # Sentraliserer teksten vertikalt
                vindu.blit(tekst, tekstRamme.topleft)
                i += 1

    def alternativRamme(self, i):
        return pg.Rect(
            self.xPosisjon + 10,
            self.yPosisjon + (i + 1) * self.hoyde,
            self.bredde,
            self.hoyde
        )

    def visAlternativer(self, pos):
        if pos == None:
            return
        elif self.rektangel.collidepoint(pos):
            self.aktiv = not self.aktiv
        elif self.aktiv:
            i = 0
            while i < len(self.alternativer):
                if self.alternativRamme(i).collidepoint(pos):
                    self.tekst = self.alternativer[i]
                    print(f"Valgt alternativ: {self.tekst}")
                    self.aktiv = False
                    break
                i += 1
        else:
            self.aktiv = False
        
                    # Klikk utenfor alternativer deaktiverer nedtrekkslisten

class Input_felt:
    instanser = []
    PADDING = 10
    def __init__(self, x, y, beskrivelse, overskrift):
        self.innhold = beskrivelse
        self.x = x
        self.y = y
        self.overskrift = overskrift
        self.aktiv = False
        self.bredde = 150
        Input_felt.instanser.append(self)

    def aktiver(self, pos):
        if pos != None: 
            if self.tekst_ramme.collidepoint(pos):
                self.aktiv = True
            else: 
                self.aktiv = False

    def tegn(self, vindu, farge, keys = None):
        if self.aktiv:
            if keys != None:
                for key in keys:
                    if key == "backspace":
                        if self.innhold[len(self.innhold)-1] != " ":
                            self.innhold = self.innhold[:-1]
                        else: 
                            pass
                    elif key.isnumeric(): 
                        self.innhold += key
                    else:
                        if key == "return":
                            self.aktiv = False
                        pass
        tekst_obj = font.render(self.innhold, True, (255, 255, 255))
        overskrift = font.render(self.overskrift, True, (0, 0, 0))
        rect = tekst_obj.get_rect()
        self.tekst_ramme = pg.Rect(self.x - Input_felt.PADDING, self.y - Input_felt.PADDING, self.bredde, rect.height + 2 * Input_felt.PADDING)
        
        pg.draw.rect(vindu, farge, self.tekst_ramme)

        if self.aktiv:
            pg.draw.rect(vindu, (0, 0, 0), self.tekst_ramme, width=1)

        vindu.blit(tekst_obj, (self.x, self.y))
        vindu.blit(overskrift, (self.x-10, self.y - 40))

