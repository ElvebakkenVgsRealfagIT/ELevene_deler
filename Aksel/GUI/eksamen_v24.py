import pandas as pd
import pygame as pg
import io
from matplotlib import pyplot as plt
import os 
import sys
import numpy as np

sys.path.append(os.path.abspath("./datasett innlevering"))

from graf_knapp_klasser import *

data = pd.read_csv("datasett_tidsbruk.csv", encoding="latin1", delimiter = ";", skiprows = 1)


df = pd.DataFrame(data)

def autopct_if_large(pct):
    return f"{pct:.0f}%" if pct > 4 else ""

def plotter(x, y, type):
    buf = io.BytesIO()
    fig, ax = plt.subplots(figsize = (15, 5.75))
    ax.set_position([0.2, 0.1, 0.4, 0.8])
    if type == "Linje":
        ax.plot(x, y)
    elif type == "Bar":
        ax.barh(x, y)
    elif type == "Sektor":
        fig, ax = plt.subplots(figsize = (12, 6))
        wedges, texts, autotexts = ax.pie(y, autopct=autopct_if_large)
        ax.legend(wedges, x, loc="center left", bbox_to_anchor=(-0.6, 0.5), frameon=False)
        ax.set_position([0.05, 0.05, 0.9, 0.9])  # fill most of the figure
    elif type == "Gruppert stolpediagram":
        offset = 0.2
        x_arr = np.arange(len(x))
        ax.barh(x_arr + offset, y[0], label = "Menn", height = offset * 2)
        ax.barh(x_arr - offset, y[1], label = "Kvinner", height = offset * 2)
        ax.set_yticks(x_arr)
        ax.set_yticklabels(x)
        ax.legend(loc = "upper right", fontsize = 8)

    plt.savefig(buf, format="PNG")
    buf.seek(0)
    return pg.image.load(buf, ".png")

BREDDE, HØYDE = pg.display.Info().current_w - 100, pg.display.Info().current_h - 100
vindu = pg.display.set_mode((BREDDE, HØYDE))
run = True
vis = False

nedtrekksmeny = Nedtrekksliste(30, 45, ["Menn", "Kvinner", "Alle", "Begge"], "Velg data", 150)
velg_graf = Nedtrekksliste(270, 45, ["Bar", "Sektor", "Gruppert stolpediagram"], "Velg graftype", 200)
vis_knapp = Knapp(BREDDE - 200, 40, "Ok")


aktiviteter = []

for a in df["alle aktiviteter"].to_list():
    if a not in aktiviteter:
        aktiviteter.append(a)

aktiviteter.pop(0)
menn_indekser = [i for i in range(2, len(df["kjønn"])) if df["kjønn"][i] == "Menn"]
kvinne_indekser = [i + 1 for i in menn_indekser]
alle_indekser = [i -1 for i in menn_indekser]
menn_tidsforbruk = [df["Tidsbruk 2000 I alt"][i] for i in menn_indekser]
kvinner_tidsforbruk = [df["Tidsbruk 2000 I alt"][i] for i in kvinne_indekser]
alle_tidsforbruk = [df["Tidsbruk 2000 I alt"][i] for i in alle_indekser]


while run:
    pos = None

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
    
    vindu.fill((255, 255, 255))

    if vis: 
        vindu.blit(graf_overflate, (180, 75))

    if pos != None: 

        nedtrekksmeny.visAlternativer(pos)
        velg_graf.visAlternativer(pos)

        if vis_knapp.rektangel.collidepoint(pos):
            vis = True
            if nedtrekksmeny.tekst == "Begge" or velg_graf.tekst == "Gruppert stolpediagram":
                graf_overflate = plotter(aktiviteter, [menn_tidsforbruk, kvinner_tidsforbruk], "Gruppert stolpediagram")
            elif nedtrekksmeny.tekst == "Menn":
                graf_overflate = plotter(aktiviteter, menn_tidsforbruk, velg_graf.tekst)
            elif nedtrekksmeny.tekst == "Kvinner":
                graf_overflate = plotter(aktiviteter, kvinner_tidsforbruk, velg_graf.tekst)
            elif nedtrekksmeny.tekst == "Alle":
                graf_overflate = plotter(aktiviteter, alle_tidsforbruk, velg_graf.tekst)
          
    vis_knapp.tegn(vindu, (0, 0, 0))
    nedtrekksmeny.tegn(vindu, (0, 0, 0))
    velg_graf.tegn(vindu, (0, 0, 0))

    pg.display.flip()
    
    
    