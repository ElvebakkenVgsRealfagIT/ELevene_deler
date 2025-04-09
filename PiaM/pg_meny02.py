import pygame as pg

pg.init()

MENYFARGE = (200, 200, 200)
HOVERFARGE = (150, 150, 150)
TEKSTFARGE = (0, 0, 0)
FONT = pg.font.SysFont("Arial", 24)

class Knapp:
    def __init__(self, x, y, bredde, hoyde, tekst, farge, hoverfarge, font):
        self.tekst = tekst
        self.rektangel = pg.Rect(x, y, bredde, hoyde)
        self.farge = farge
        self.hoverfarge = hoverfarge
        self.font = font

    def tegn(self, vindu):
        mus = pg.mouse.get_pos()
        aktuell_farge = self.hoverfarge if self.rektangel.collidepoint(mus) else self.farge

        pg.draw.rect(vindu, aktuell_farge, self.rektangel)
        tekst_surface = self.font.render(self.tekst, True, TEKSTFARGE)
        tekst_rect = tekst_surface.get_rect(center=self.rektangel.center)
        vindu.blit(tekst_surface, tekst_rect)
