"""
Jeg har endret overskriftene i datasettet

Alt dette kjøres helt nederst i programmet:
tabell() er oppgave 9a, synes i konsollen
grafer() er egentlig ikke en av oppgavene, men viser alle grafene for alle årene, synes i eget vindu
gui() er oppgave 9b, synes i pygame vindu
"""

# BIBLIOTEKER
'''Må pip installe matplotlib, tabulate og pygame'''
import os
import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
import pygame as pg
from pg_meny import Knapp, Nedtrekksliste, MENYFARGE, HOVERFARGE, MENY_AVSTAND, MENY_XSTART, MENY_YSTART, VINDU_BREDDE, VINDU_HOYDE

# ARRAYS
aarstall = []
aar_str = []
netto = []
levendefodte = []
innflytting = []
utflytting = []
meny = []

# KONSTANTER
hvit = (255, 255, 255)

# IMPORTERE DATA
with open("Datasett_fodselstall_komma.csv") as fil:
    innhold = csv.reader(fil)

    overskrifter = next(innhold)

    #legger til verdien i listen, eller 0 hvis det ikke er oppgitt en verdi
    for rad in innhold:
        aarstall.append(int(rad[0]) if rad[0].strip() else 0)
        aar_str.append((rad[0]))
        levendefodte.append(int(rad[1]) if rad[1].strip() else 0)
        innflytting.append(int(rad[2]) if rad[2].strip() else 0)
        utflytting.append(int(rad[3]) if rad[3].strip() else 0)

    #fjerner siste verdi, fordi listen er tom her
    aarstall.pop()
    levendefodte.pop()
    innflytting.pop()
    utflytting.pop()

    #regner ut netto befolkningsvekst  
    for i in range (0, len(aarstall)):
        folk = levendefodte[i] + innflytting[i] - utflytting[i]
        netto.append(folk)


# TABELL
def tabell():
    #overskrifter
    tabelldata = [
        ["Årstall", "Levendefødte", "Innflytting", "Utflytting", "Netto befolkningsvekst"]
    ]
    #sette inn data
    for i in range(len(aarstall)):
        tabelldata.append([aarstall[i], netto[i], levendefodte[i], innflytting[i], utflytting[i]])
    #skrive ut tabellen
    print(tabulate(tabelldata, headers="firstrow", tablefmt="grid"))

# GRAFER
def grafer(haandtering = "vise", yverdi = netto, start = 1945, slutt = 2024):
    plt.style.use("bmh")
    #hvis grafene kun skal vises
    if haandtering == "vise":
        plt.figure(figsize=(12,6))

        plt.subplot(2, 1, 1)
        plt.plot(aarstall, netto)
        plt.title("Netto befolkningsvekst")
        plt.subplot(2, 3, 4)
        plt.plot(aarstall, levendefodte)
        plt.title("Levendefødte")
        plt.subplot(2, 3, 5)
        plt.plot(aarstall, innflytting)
        plt.title("Innflytting")
        plt.subplot(2, 3, 6)
        plt.plot(aarstall, utflytting)
        plt.title("Utflytting")

        plt.show()

    #hvis grafen skal lagres som en png
    elif haandtering == "lagre":
        plt.figure(figsize=(6, 3))
        plt.plot(aarstall, yverdi)
        plt.xlim(start, slutt)

        plt.savefig("graf.png", dpi=300)

    #hvis feil i koden    
    else:
        print("Feil variabel i kalling av grafer()")
            
# BRUKERGRENSESNITT
def gui():
    # slette forrige bildefil
    if os.path.exists("graf.png"):
        os.remove("graf.png")
    else:
        pass

    #lage pygame vinduet hvitt
    vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
    vindu.fill(hvit)
    pg.display.set_caption("Befolkningsvekst")

    #legge til interaksjonsmulighetene
    meny.append(Nedtrekksliste(MENY_XSTART, MENY_YSTART, aar_str))
    meny.append(Nedtrekksliste(MENY_XSTART + 150, MENY_YSTART, aar_str))
    meny.append(Nedtrekksliste(MENY_XSTART + 300, MENY_YSTART, ["Levendefødte", "Innflytting", "Utflytting", "Befolkningsvekst"]))
    meny.append(Knapp(MENY_XSTART + 600, MENY_YSTART, "OK"))

    #hva som skjer ved klikk
    def museklikk(posisjon):
        nonlocal feilmelding
        for m in meny:

            if isinstance(m, Nedtrekksliste) and m.aktiv:
                m.visAlternativer(posisjon)

            elif m.rektangel.collidepoint(posisjon):

                if isinstance(m, Nedtrekksliste):
                    m.visAlternativer(posisjon)
                
                elif isinstance(m, Knapp) and m.tekst == "OK":
                    startaar = int(meny[0].tekst)
                    sluttaar = int(meny[1].tekst)

                    if sluttaar <= startaar:
                        feilmelding = "Du må velge et sluttår etter startåret."

                    elif startaar < sluttaar:
                        feilmelding = ""
                        kategori = meny[2].tekst
                        #print(f"Valgt startår: {startaar}")
                        #print(f"Valgt sluttår: {sluttaar}")
                        #print(f"Valgt kategori: {kategori}")

                        #gjøre om kategori til en av listene fra datasettet
                        if kategori == "Levendefødte":
                            kategori = levendefodte
                        elif kategori == "Utflytting":
                            kategori = utflytting
                        elif kategori == "Innflytting":
                            kategori = innflytting
                        elif kategori == "Befolkningsvekst":
                            kategori = netto

                        #lagre bildet med riktige variabler
                        grafer("lagre", kategori, startaar, sluttaar)                    
                else:
                    #print(f"Klikket på: {m.tekst}")
                    pass
            
    #selve løkka
    feilmelding = ""

    fortsett = True
    while fortsett:

        #håndterer input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fortsett = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                museklikk(event.pos)
                
        vindu.fill(hvit)

        #printer feilmelding hvis feil verdier
        if feilmelding:
            font = pg.font.SysFont("Arial", 24)
            tekstboks = font.render(feilmelding, True, (0, 0, 0))
            vindu.blit(tekstboks, (MENY_XSTART + 650, MENY_YSTART))

        #viser grafen hvis den finnes
        try:
            bilde = pg.image.load("graf.png")
            bilde = pg.transform.scale(bilde, (900, 500))
            vindu.blit(bilde, (MENY_XSTART, MENY_YSTART + MENY_AVSTAND))
        except FileNotFoundError:
            pass

        #finne mus-posisjonen
        muspos = pg.mouse.get_pos()
        for m in meny:
            if m.rektangel.collidepoint(muspos):
                m.tegn(vindu, (HOVERFARGE))
            else:
                m.tegn(vindu, MENYFARGE)

        for m in meny:
            if isinstance(m, Nedtrekksliste) and m.aktiv:
                m.tegn(vindu, HOVERFARGE)

        pg.display.flip()

    pg.quit()

"""
tabell() er oppgave 9a, synes i konsollen
grafer() er egentlig ikke en av oppgavene, men viser alle grafene for alle årene, synes i eget vindu
gui() er oppgave 9b, synes i pygame vindu
"""

tabell()
grafer()
gui()