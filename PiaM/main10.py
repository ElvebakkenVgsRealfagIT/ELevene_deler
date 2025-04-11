import pygame as pg
import matplotlib.pyplot as plt
import csv
import io

from pg_meny02 import Knapp, MENYFARGE, HOVERFARGE

pg.init()

# ---------------- Data & Klasse ----------------

class Aarsdata:
    def __init__(self, aarstall:int, fodselstall:int, innflyttere:int, utflyttere:int):
        self.aarstall = aarstall
        self.fodselstall = fodselstall
        self.innflyttere = innflyttere
        self.utflyttere = utflyttere
        self.netto_folkevekst = fodselstall + innflyttere - utflyttere

    def lagListe(self):
        return [self.aarstall, self.fodselstall, self.innflyttere, self.utflyttere, self.netto_folkevekst]

aarsdata = []
filnavn = "fødselstall_datasett.csv"

with open(filnavn, encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=",")
    next(filinnhold)
    for rad in filinnhold:
        if rad[0] and rad[0].isdigit():
            aarsdata.append(Aarsdata(
                int(rad[0]),
                int(rad[1]) if rad[1].isdigit() else 0,
                int(rad[2]) if rad[2].isdigit() else 0,
                int(rad[3]) if rad[3].isdigit() else 0
            ))

# ---------------- Pygame-oppsett ----------------

BREDDE, HOYDE = 900, 600
VINDU = pg.display.set_mode((BREDDE, HOYDE))
pg.display.set_caption("Folketallsanalyse")

BAKGRUNNSFARGE = (255, 255, 255)
FONT = pg.font.SysFont("Arial", 18)

dropdown_valg = ["Fødsler", "Innflytting", "Utflytting", "Folkevekst"]
valgt_valg = dropdown_valg[0]
vis_dropdown = False
graf_bilde = None

fra_aar, til_aar = 2000, 2020
input_fra = str(fra_aar)
input_til = str(til_aar)
aktivt_felt = None

def lag_graf(kol_index, tittel, ylabel):
    aarstall = [a.aarstall for a in aarsdata if fra_aar <= a.aarstall <= til_aar]
    verdier = [a.lagListe()[kol_index] for a in aarsdata if fra_aar <= a.aarstall <= til_aar]

    fig, ax = plt.subplots()
    ax.plot(aarstall, verdier, marker='o')
    ax.set_title(tittel)
    ax.set_xlabel("Årstall")
    ax.set_ylabel(ylabel)
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return pg.image.load(buf, 'graf.png')

def tegn_tabell(surface):
    FONT = pg.font.SysFont("Courier New", 18)
    x = 20
    y = 20
    header = f"{'Årstall':<10}{'Fødsler':<10}{'Innflytt':<12}{'Utflytt':<12}{'Netto vekst':<14}"
    tekst = FONT.render(header, True, (0, 0, 0))
    surface.blit(tekst, (x, y))
    y += 30

    for a in aarsdata[:20]:  # Viser de 20 første radene
        rad = a.lagListe()
        rad_tekst = f"{rad[0]:<10}{rad[1]:<10}{rad[2]:<12}{rad[3]:<12}{rad[4]:<14}"
        tekst = FONT.render(rad_tekst, True, (0, 0, 0))
        surface.blit(tekst, (x, y))
        y += 25

# Lager knappen og meny-liste
meny = [Knapp(20, 520, 120, 40, "Vis tabell", MENYFARGE, HOVERFARGE, FONT)]
aktiv_visning = "graf"


def museklikk(pos):
    global aktiv_visning, valgt_valg
    for m in meny:
        if m.rektangel.collidepoint(pos):
            if m.tekst == "Vis tabell":
                aktiv_visning = "tabell"
                m.tekst = "Vis graf"
            elif m.tekst == "Vis graf":
                aktiv_visning = "graf"
                m.tekst = "Vis tabell"


def oppdater_graf():
    global graf_bilde
    if valgt_valg == "Fødsler":
        graf_bilde = lag_graf(1, "Fødsler per år", "Antall fødsler")
    elif valgt_valg == "Innflytting":
        graf_bilde = lag_graf(2, "Innflytting per år", "Antall innflyttere")
    elif valgt_valg == "Utflytting":
        graf_bilde = lag_graf(3, "Utflytting per år", "Antall utflyttere")
    elif valgt_valg == "Folkevekst":
        graf_bilde = lag_graf(4, "Netto folkevekst per år", "Netto folkevekst")

oppdater_graf()

# ---------------- Hovedløkke ----------------

klokke = pg.time.Clock()
kjører = True
while kjører:
    VINDU.fill(BAKGRUNNSFARGE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            kjører = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            mus_x, mus_y = event.pos
            museklikk((mus_x, mus_y)) 

            mus_x, mus_y = event.pos
            aktivt_felt = None
            if 50 <= mus_x <= 250 and 20 <= mus_y <= 50:
                vis_dropdown = not vis_dropdown
            
            elif vis_dropdown:
                for i, valg in enumerate(dropdown_valg):
                    if 50 <= mus_x <= 250 and 60 + i * 30 <= mus_y <= 90 + i * 30:
                        valgt_valg = valg
                        vis_dropdown = False
                        oppdater_graf()
            elif 270 <= mus_x <= 370 and 20 <= mus_y <= 50:
                aktivt_felt = "fra"
            elif 390 <= mus_x <= 490 and 20 <= mus_y <= 50:
                aktivt_felt = "til"
            else:
                vis_dropdown = False



        elif event.type == pg.KEYDOWN and aktivt_felt:
            if event.key == pg.K_BACKSPACE:
                if aktivt_felt == "fra":
                    input_fra = input_fra[:-1]
                elif aktivt_felt == "til":
                    input_til = input_til[:-1]
            elif event.key == pg.K_RETURN:
                try:
                    fra_aar = int(input_fra)
                    til_aar = int(input_til)
                    oppdater_graf()
                except:
                    pass
                aktivt_felt = None
            else:
                if event.unicode.isdigit():
                    if aktivt_felt == "fra":
                        input_fra += event.unicode
                    elif aktivt_felt == "til":
                        input_til += event.unicode

    # Dropdown-meny
    pg.draw.rect(VINDU, (175, 202, 204), (50, 20, 200, 30))
    tekst = FONT.render(valgt_valg, True, (0, 0, 0))
    VINDU.blit(tekst, (60, 25))

    if vis_dropdown:
        for i, valg in enumerate(dropdown_valg):
            pg.draw.rect(VINDU, (137, 173, 176), (50, 60 + i * 30, 200, 30))
            tekst = FONT.render(valg, True, (0, 0, 0))
            VINDU.blit(tekst, (60, 65 + i * 30))

    # Tekstfelt: Fra år
    pg.draw.rect(VINDU, (255, 255, 255), (270, 20, 100, 30), 0)
    pg.draw.rect(VINDU, (0, 0, 0), (270, 20, 100, 30), 2 if aktivt_felt == "fra" else 1)
    VINDU.blit(FONT.render(input_fra, True, (0, 0, 0)), (275, 25))

    # Tekstfelt: Til år
    pg.draw.rect(VINDU, (255, 255, 255), (390, 20, 100, 30), 0)
    pg.draw.rect(VINDU, (0, 0, 0), (390, 20, 100, 30), 2 if aktivt_felt == "til" else 1)
    VINDU.blit(FONT.render(input_til, True, (0, 0, 0)), (395, 25))

    if aktiv_visning == "graf" and graf_bilde:
        skalert = pg.transform.scale(graf_bilde, (600, 400))
        VINDU.blit(skalert, (150, 100))
    elif aktiv_visning == "tabell":
        tegn_tabell(VINDU)

        # Tegner knappen(e)
    for knapp in meny:
        knapp.tegn(VINDU)

    pg.display.flip()
    klokke.tick(60)

pg.quit()
