import csv
import pygame as pg
import matplotlib
import matplotlib.pyplot as plt
import sys
from io import BytesIO
from pygame.locals import MOUSEBUTTONDOWN
from pg_meny import Knapp, Nedtrekksliste, Tekstinput
from pg_meny import MENYFARGE, HOVERFARGE

def csv_til_dict(filnavn:str) -> dict:
    with open(filnavn, encoding="utf-8-sig") as fil:
        filinnhold = csv.reader(fil, delimiter=",")
        nokler = next(filinnhold)
        data = []
        for linje in filinnhold:
            element = {}
            for i in range(len(nokler)):
                element[nokler[i]] = linje[i]
            data.append(element)
    return data

# Lagrer data i csv-fil som dict der alt er string
min_data = csv_til_dict("Datasett_fodselstall_komma.csv")

# Sett Matplotlib til ikke-interaktiv modus med 'Agg' som backend
matplotlib.use('Agg')

def plotGraf(x_verdier:list[float], y_verdier:list[float], vis_som_punkter:bool = False, vis_rutenett:bool = True, tittel:str = "", x_akse_tittel:str = "$x$", y_akse_tittel:str = "$y$", maks_x_verdi:float = None, min_x_verdi:float = None, maks_y_verdi:float = None, min_y_verdi:float = None, vis_tydelig_x_og_y_akse:bool = True, graf_farge:str="skyblue"):
    """
    Plotter en graf basert på to lister
    """
    if vis_rutenett: # Plotter rutenett
        plt.grid()

    # Begrenser hvor mye av grafen man kan se i x-aksen basert på brukerinput
    if maks_x_verdi != None or min_x_verdi != None:
        if maks_x_verdi == None:
            maks_x_verdi = max(x_verdier)
        elif min_x_verdi == None:
            min_x_verdi = min(x_verdier)
        plt.xlim(min_x_verdi, maks_x_verdi)

    # Begrenser hvor mye av grafen man kan se i y-aksen basert på brukerinput
    if maks_y_verdi != None or min_y_verdi != None:
        if maks_y_verdi == None:
            maks_y_verdi = max(y_verdier)
        elif min_y_verdi == None:
            min_y_verdi = min(y_verdier)
        plt.ylim(min_y_verdi, maks_y_verdi)

    # Markerer x- og y-aksen
    if vis_tydelig_x_og_y_akse:
        plt.axvline(0, color="black", zorder=2)
        plt.axhline(0, color="black", zorder=2)

    # Sjekker om man skal plotte som punkter eller graf
    if vis_som_punkter:
        plt.scatter(x_verdier, y_verdier, color=graf_farge, zorder=3)
    else:
        plt.plot(x_verdier, y_verdier, color=graf_farge, zorder=3)

    # Aksetitler
    plt.xlabel(x_akse_tittel)
    plt.ylabel(y_akse_tittel)

    # Tittel
    plt.title(tittel)

def tegnMatPlotLibDiagram(valg:str, x_akse_nokkel:str, min_verdi:float, max_verdi:float):
    x_verdier = []
    y_verdier = []
    for element in min_data:
        try:
            y_verdier.append(float(element[valg]))
            x_verdier.append(float(element[x_akse_nokkel]))
        except:
            pass

    # Lukker den forrige grafen
    plt.close()
    # Ploter grafen
    plotGraf(x_verdier, y_verdier, x_akse_tittel=x_akse_nokkel, y_akse_tittel=valg, maks_x_verdi=max_verdi, min_x_verdi=min_verdi, maks_y_verdi=max(y_verdier), min_y_verdi=min(y_verdier))
    # Lagre diagrammet som en bildebuffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    bilde = pg.image.load(buf)

    # Skalerer bildet til å passe til vinduet.
    bilde = pg.transform.scale(bilde, (MENY_XSTART, VINDU_HOYDE))
    return bilde

# Farger
BAKGRUNNSFARGE = (255, 255, 255)
MORK_GRA = (169, 169, 169)
LYS_GRA = (211, 211, 211)
BLA = (0, 120, 215)

# Definerer et vindu
VINDU_BREDDE = 1000
VINDU_HOYDE = 600

# Definerer menyfeltet til høyre i vinduet
MENY_XSTART = 600
MENY_YSTART = 20
MENY_YAVSTAND = 160  # y-avstand for hvert element

VINDU = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])

# Initialiserer/starter pygame
pg.init()

# En liste med menyelementer
meny = []

# Lager liste med alternativer til hva brukeren kan se informasjon om
alternativer = []
for nokkel in min_data[0].keys(): # Henter nøklene
    alternativer.append(nokkel)
x_akse_tittel = alternativer.pop(0) # Legger til den første nøkkelen (som regel år/årstall) som x-aksen og fjerner den fra alternativene

# Legger til nedtrekksliste for hva man ønsker info om
meny.append(
    Nedtrekksliste(MENY_XSTART, MENY_YSTART, alternativer)
)

meny.append(
    Tekstinput(MENY_XSTART, MENY_YSTART + MENY_YAVSTAND, min_data[0][x_akse_tittel])
)

meny.append(
    Tekstinput(MENY_XSTART, MENY_YSTART + MENY_YAVSTAND*4/3, min_data[-1][x_akse_tittel])
)

# OK-knapp
meny.append(Knapp(MENY_XSTART, MENY_YSTART + 2*MENY_YAVSTAND, "OK"))

diagramBilde = None

# Gjenta helt til brukeren lukker vinduet
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            for element in meny: # Sjekker om noen elementer i menyen klikkes
                if isinstance(element, Nedtrekksliste) and element.aktiv:
                    element.visAlternativer(event.pos)
                elif isinstance(element, Tekstinput) and element.aktiv: # Deaktiverer tekstbokser som ikke brukes
                    element.aktiv = False
                    if element.tekst == "":
                        element.tekst = element.standard_tekst
                elif element.rektangel.collidepoint(event.pos):
                    if element.tekst == "OK": # Tegner grafen om "OK"-knappen trykkes
                        meny[1].korriger_input(float(meny[1].standard_tekst), float(meny[2].standard_tekst))
                        meny[2].korriger_input(float(meny[1].standard_tekst), float(meny[2].standard_tekst))
                        if float(meny[1].tekst) >= float(meny[2].tekst):
                            meny[1].tekst = meny[1].standard_tekst
                            meny[2].tekst = meny[2].standard_tekst
                        diagramBilde = tegnMatPlotLibDiagram(meny[0].tekst, x_akse_tittel, float(meny[1].tekst), float(meny[2].tekst))
                    elif isinstance(element, Nedtrekksliste):
                        element.visAlternativer(event.pos)
                    elif isinstance(element, Tekstinput):
                        element.aktiv = True
                        element.tekst = ""
        elif event.type == pg.KEYDOWN:
            for element in meny:
                if isinstance(element, Tekstinput) and element.aktiv:
                    element.bruker_skriver(event)

    # Fyller vinduet
    VINDU.fill(BAKGRUNNSFARGE)
    # Henter mus-posisjonen
    musPos = pg.mouse.get_pos()

    # Tegner elementene i menyen og endrer fargen ved hover
    for element in meny:
        if element.rektangel.collidepoint(musPos):
            element.tegn(VINDU, HOVERFARGE)
        else:
            element.tegn(VINDU, MENYFARGE)

    # Tegner diagrambildet om det finnes
    if diagramBilde:
        VINDU.blit(diagramBilde, (0, 0), pg.Rect(0, 0, MENY_XSTART+200, VINDU_HOYDE+100))

    # Tegner de aktive nedtrekkslistene (som viser sine alternativer)
    for element in meny:
        if isinstance(element, Nedtrekksliste) and element.aktiv:
            element.tegn(VINDU, MENYFARGE)

    # Oppdaterer vinduet
    pg.display.flip()