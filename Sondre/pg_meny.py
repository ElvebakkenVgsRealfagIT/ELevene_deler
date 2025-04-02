import pygame as pg

# Farger
TEKSTFARGE = (255, 255, 255)
MENYFARGE = (0, 0, 255)
HOVERFARGE = (0, 150, 255)

# Nedtrekksmeny
NEDTREKKS_BREDDE, NEDTREKKS_HOYDE = 200, 50

# Menyfelt
# MENYFELT_START = 400
# MENYFELT_BREDDE = 200

# Initialiserer/starter pygame
pg.init()

# Angir hvilken skrifttype og tekststørrelse vi vil bruke på tekst
font = pg.font.SysFont("Tahoma", 24)

class Knapp:
    """
    Klasse for å representere en knapp

    xPosisjon (float) - x-posisjonen til knappen
    yPosisjon (float) - y-posisjonen til knappen
    tekst (str) - teksten til knappen
    """
    def __init__(self, xPosisjon:float, yPosisjon:float, tekst:str, hoyde:float = 40):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.bredde = len(tekst) * 14 + 20
        self.hoyde = 40
        self.tekst = tekst
        self.rektangel = pg.Rect(
            self.xPosisjon, self.yPosisjon, self.bredde, self.hoyde
        )

    def tegn(self, vindu, farge):
        pg.draw.rect(vindu, farge, self.rektangel)
        tekst = font.render(self.tekst, True, TEKSTFARGE)
        tekstRamme = tekst.get_rect(center=self.rektangel.center)
        vindu.blit(tekst, tekstRamme.topleft)

class Nedtrekksliste:
    def __init__(self, xPosisjon, yPosisjon, alternativer):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        self.alternativer = alternativer
        self.aktiv = False
        self.tekst = alternativer[0]
        self.bredde = self.lengsteTekst() * 14
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
        tekstRamme = tekst.get_rect(center=self.rektangel.center)
        tekstRamme.left = rekt.left + 10 # Venstrejusterer teksten
        tekstRamme.centery = rekt.centery  # Sentraliserer teksten vertikalt
        vindu.blit(tekst, tekstRamme.topleft)

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
        if self.rektangel.collidepoint(pos): # Lukker/åpner nedtrekkslisten om den blir trykket på
            self.aktiv = not self.aktiv
        elif self.aktiv:
            ingenErBlittTrykket = True
            for i in range(len(self.alternativer)): # Går gjennom hvert element og sjekker om den blir trykket
                if self.alternativRamme(i).collidepoint(pos):
                    # Oppdaterer teksten til alternativet som blir valgt
                    self.tekst = self.alternativer[i]
                    self.aktiv = False
                    ingenErBlittTrykket = False
                    break
            # Deaktiverer nedtrekkslisten om brukeren trykker utenfor
            if ingenErBlittTrykket:
                self.aktiv = False


class Tekstinput:
    def __init__(self, x_posisjon:float, y_posisjon:float, standard_tekst:str, bredde:float=140, hoyde:float=32, font_storrelse:int=32):
        self.rektangel = pg.Rect(x_posisjon, y_posisjon, bredde, hoyde)
        self.standard_tekst = standard_tekst
        self.tekst = standard_tekst
        self.font = pg.font.Font(None, font_storrelse)
        self.aktiv = False
    def tegn(self, vindu, farge):
        pg.draw.rect(vindu, farge, self.rektangel)
        print(self.tekst)
        text_surface = self.font.render(self.tekst, True, (255, 255, 255))
        vindu.blit(text_surface, (self.rektangel.x + 5, self.rektangel.y + 5))
        self.rektangel.w = max(100, text_surface.get_width() + 10) # Tilpasser rektangelet til teksten
    def bruker_skriver(self, event):
        if event.key == pg.K_BACKSPACE:
            self.tekst = self.tekst[:-1]
        else:
            self.tekst += event.unicode
    def korriger_input(self, minste_verdi:float, storste_verdi:float):
        # Ikke helt fullført
        try:
            float(self.tekst)
        except:
            self.tekst = self.standard_tekst