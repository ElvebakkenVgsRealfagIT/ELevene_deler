import matplotlib.pyplot as plt
import pygame as pg
import io
import sys
from graf_knapp_klasser import *   
from data import *

def pg_plot(x_verdier, y_verdier, type, start, slutt, x_tittel, y_tittel):
    global graf_surface
    fig, ax = plt.subplots(figsize = (5.4, 5))

    if type == "Linje":
        ax.plot(x_verdier, y_verdier) 
    elif type == "Bar":
        ax.bar(x_verdier, y_verdier)
    elif type == "Scatter":
        ax.scatter(x_verdier, y_verdier)

    ax.set_xlabel(x_tittel, labelpad=8, fontsize = 14)
    ax.set_ylabel(y_tittel, labelpad=8, fontsize = 14)
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG', bbox_inches = "tight")
    buf.seek(0)
    plt.close(fig)
    graf_surface = pg.image.load(buf, '.png')

pg.init()

BREDDE = 800
HØYDE = 600

screen = pg.display.set_mode((BREDDE, HØYDE))
pg.display.set_caption("Matplotlib-graf i Pygame")

show = False


velg_graf = Nedtrekksliste(BREDDE - 190, 70, ["Linje", "Bar", "Scatter"], "Velg graftype")
velg_y_akse = Nedtrekksliste(BREDDE - 190, 160, ["Innflyttinger", "Utflyttinger", "Levendefødte", "Nettovekst"], "Velg y-akse")
start_input = Input_felt(BREDDE - 180, 270, "Start: ", "Skriv startår (fra 1945)")
slutt_input = Input_felt(BREDDE - 180, 370, "Slutt: ", "Skriv sluttår (til 2023)")
ok_knapp = Knapp(BREDDE -170, 435, "Vis graf")

MENYFARGE = (130, 130, 255)

running = True

pos = None

while running:

    screen.fill((255, 255, 255))  # Hvit bakgrunn
    pg.draw.rect(screen, (225, 225, 225), (BREDDE-240, 0, 250, HØYDE))

    events = pg.event.get()
    keys_pressed = []

    for event in events:
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
        if event.type == pg.KEYDOWN:       
            keys_pressed.append(pg.key.name(event.key))
    
 
    ok_knapp.tegn(screen, (50, 50, 125))

    if pos != None:
        if ok_knapp.rektangel.collidepoint(pos):
            st = start_input.innhold
            sl = slutt_input.innhold
            start = int(st[st.index(" "):])
            slutt = int(sl[sl.index(" "):])
            print(start, slutt)
            x_liste = df["År"].to_list()
            valgt_y = velg_y_akse.tekst
            if valgt_y == "Levendefødte":
                valgt_y = "Levendefødte i alt"
            x_verdier = x_liste[x_liste.index(start):x_liste.index(slutt)]
            y_verdier = df[valgt_y][x_liste.index(start):x_liste.index(slutt)]
            pg_plot(x_verdier, y_verdier, velg_graf.tekst, None, None, "År", valgt_y)
            show = True

    for instans in Input_felt.instanser:
        instans.tegn(screen, MENYFARGE)
        instans.aktiver(pos)
        if not instans.aktiv:
            instans.tegn(screen, MENYFARGE)
        elif instans.aktiv:
            instans.tegn(screen, MENYFARGE, keys_pressed)
    for instans in Nedtrekksliste.instanser:
        if instans.aktiv:
            tegn_sist = instans
        instans.tegn(screen, MENYFARGE)
        instans.visAlternativer(pos)
    try: 
        tegn_sist.tegn(screen, MENYFARGE)
    except: 
        None

    if show: 
        screen.blit(graf_surface, (25, 50))  # Tegn grafen
    
    pos = None

    pg.display.flip()


pg.quit()
sys.exit()
