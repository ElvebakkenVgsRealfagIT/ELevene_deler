import csv
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path

class FlervalgsMeny:
    """
    En flervalgsmeny der alle alternativene alltid vises

    root - tkinter master
    alternativer (list[tuple[str, str]]) - liste med tupler der den første verdien er alternativet som skal vises, og den andre verdien er verdien som lagres når alternativet velges
    start_rad (int) - grid-raden alternativene skal starte på
    kolonne (int) - grid-kolonnen til menyen
    """
    def __init__(self, root, alternativer:list[tuple[str, str]], start_rad:int, kolonne:int):
        self.root = root
        # Velger verdien til det første elementet som standard, endres om et annet blir valg
        self.valgt_verdi = tk.StringVar(self.root, alternativer[0][1])

        # Lager alternativene/knappene
        i = 0
        for (tekst, verdi) in alternativer:
            tk.Radiobutton(root, text=tekst, variable=self.valgt_verdi, value=verdi, indicator=0, background="light blue").grid(row=start_rad+i, column=kolonne, padx=5, pady=5)
            i += 1

class plotApp:
    """
    Plotter en graf i tkinter der man kan endre på hva som skal vises med knapper og tekstinput

    Variabler:
    root - tkinter master
    tittel(str) - tittelen på vinduet
    data (list[dict]) - Dataen som grafes

    Funksjoner:
    oppdater_plot(self)
        Oppdaterer plotet i vinduet
    
    fiks_om_feil_tekstinput(self) -> tuple[float, float]
        Reseter inputen i tekstfeltene om den er feil og returnerer den minste og største x-verdien som skal vises på grafen
    
    """
    def __init__(self, root, tittel:str, data:list[dict]):
        self.root = root
        self.tittel = tittel
        self.data = data

        # Lager figuren
        self.figur, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figur, master=self.root)
        #self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=7)

        # Plot-knapp
        self.plot_knapp = tk.Button(self.root, text="Plot", command=self.oppdater_plot)
        self.plot_knapp.grid(column=5, row=2)

        # Finner nøklene i datasettet og legger de til som alternativer i flervalgsmenyen
        self.nokler = []
        liste_i_flervalgsmeny = []
        for nokkel in data[0].keys():
            self.nokler.append(nokkel)
            liste_i_flervalgsmeny.append((nokkel, nokkel))

        # Fjerner nøkkelen til x-aksen fra listen med alternativer i flervalgsmenyen
        self.x_akse_nokkel = liste_i_flervalgsmeny.pop(0)[0]

        # Lag en meny for hva brukeren ønsker graf over
        self.meny = FlervalgsMeny(self.root, liste_i_flervalgsmeny, 1, 0)

        # Tekstinput for det første året som skal vises
        self.fra_aar_tekst = tk.Label(root, text="Fra").grid(row=1, column=2)
        self.fra_aar_var = tk.StringVar(self.root, self.data[0][self.x_akse_nokkel])
        self.fra_entry = tk.Entry(self.root, textvariable=self.fra_aar_var)
        self.fra_entry.grid(row=2, column=2)

        # Tekstinput for det siste året som skal vises
        self.til_aar_tekst = tk.Label(root, text="Til").grid(row=1, column=3)
        self.til_aar_var = tk.StringVar(self.root, self.data[-1][self.x_akse_nokkel])
        self.til_entry = tk.Entry(self.root, textvariable=self.til_aar_var)
        self.til_entry.grid(row=2, column=3)

        # Original plot
        self.oppdater_plot()

    def oppdater_plot(self):
        """
        Oppdaterer plotet i vinduet
        """
        # Finner minste og største x-verdi som skal vises i grafen, om input er feil, vil den bli rettet på
        min_x, maks_x = self.fiks_om_feil_tekstinput()

        # Fjerner forrige plot
        self.ax.clear()

        # Lager lister med x-verdier og y-verdier for plotting av graf
        x_verdier = []
        y_verdier = []
        for element in self.data:
            try:   
                # Sørger for at dataen er gyldig
                if float(element[self.x_akse_nokkel]) >= min_x and float(element[self.x_akse_nokkel]) <=maks_x:
                    y_verdier.append(float(element[self.meny.valgt_verdi.get()]))
                    x_verdier.append(float(element[self.x_akse_nokkel]))
            except:
                pass

        plotGraf(x_verdier=x_verdier, y_verdier=y_verdier, base=self.ax, min_x_verdi=min_x, maks_x_verdi=maks_x, maks_y_verdi=max(y_verdier), min_y_verdi=min(y_verdier), x_akse_tittel=self.x_akse_nokkel, y_akse_tittel=self.meny.valgt_verdi.get(), tittel=self.tittel)
        # Tegner den nye ploten på canvasen
        self.canvas.draw()

    def fiks_om_feil_tekstinput(self) -> tuple[float, float]:
        """
        Reseter inputen i tekstfeltene om den er feil og returnerer den minste og største x-verdien som skal vises på grafen
        """
        try:
            # Henter verdiene fra tekst-feltene
            minimum_x_verdi = float(self.fra_aar_var.get())
            maksimum_x_verdi = float(self.til_aar_var.get())

            # Reseter den minste x-verdien som skal vises på grafen om den ikke er innenfor dataene i datasettet
            if minimum_x_verdi < float(self.data[0][self.x_akse_nokkel]) or minimum_x_verdi >= float(self.data[-1][self.x_akse_nokkel]):
                self.fra_entry.delete(0, tk.END)
                self.fra_entry.insert(0, self.data[0][self.x_akse_nokkel])
                minimum_x_verdi = float(self.fra_aar_var.get())

            # Reseter den største x-verdien som skal vises på grafen om den ikke er innenfor dataene i datasettet
            if maksimum_x_verdi <= float(self.data[0][self.x_akse_nokkel]) or maksimum_x_verdi > float(self.data[-1][self.x_akse_nokkel]):
                self.til_entry.delete(0, tk.END)
                self.til_entry.insert(0, self.data[-1][self.x_akse_nokkel])
                maksimum_x_verdi = float(self.fra_aar_var.get())

            # Reseter den minste x-verdien som skal vises på grafen om den er større eller lik den største x-verdien som skal vises
            if minimum_x_verdi >= maksimum_x_verdi:
                self.fra_entry.delete(0, tk.END)
                self.fra_entry.insert(0, self.data[0][self.x_akse_nokkel])
                minimum_x_verdi = float(self.fra_aar_var.get())

        except: # Reseter begge verdiene om en av verdiene ikke kan gjøres om til float
            self.fra_entry.delete(0, tk.END)
            self.fra_entry.insert(0, self.data[0][self.x_akse_nokkel])
            minimum_x_verdi = float(self.fra_aar_var.get())
            self.til_entry.delete(0, tk.END)
            self.til_entry.insert(0, self.data[-1][self.x_akse_nokkel])
            maksimum_x_verdi = float(self.til_aar_var.get())

        return minimum_x_verdi, maksimum_x_verdi

def plotGraf(x_verdier:list[float], y_verdier:list[float], base=plt, vis_som_punkter:bool = False, vis_rutenett:bool = True, tittel:str = "", x_akse_tittel:str = "$x$", y_akse_tittel:str = "$y$", maks_x_verdi:float = None, min_x_verdi:float = None, maks_y_verdi:float = None, min_y_verdi:float = None, vis_tydelig_x_og_y_akse:bool = True, graf_farge:str="skyblue"):
    """
    Plotter en graf basert på to lister

    x-verdier (list[float]) - liste med x-verdiene som skal plottes
    y-verdier (list[float]) - liste med y-verdiene som skal plottes
    base - stedet grafen skal plottes
    vis_som_punkter (bool) - bestemmer om grafen skal tegnes sammenhengene eller bare som enkeltpunkter
    vis_rutenett (bool) - bestemmer om det skal være et rutenett i ploten
    tittel (str) - tittelen på plotet
    x_akse_tittel (str) - tittelen på x-aksen
    y_akse_tittel (str) - tittelen på y-aksen
    maks_x_verdi (float) - den største x-verdien som skal vises i plotet, brukes ikke om den er None
    min_x_verdi (float) - den minste x-verdien som skal vises i plotet, brukes ikke om den er None
    maks_y_verdi (float) - den største y-verdien som skal vises i plotet, brukes ikke om den er None
    min_y_verdi (float) - den minste y-verdien som skal vises i plotet, brukes ikke om den er None
    vis_tydelig_x_og_y_akse (bool) - bestemmer om en tydelig x-akse og y-akse skal vises
    graf_farge (str) - fargen på grafen
    """
    if vis_rutenett: # Plotter rutenett
        base.grid()

    # Begrenser hvor mye av grafen man kan se i x-aksen basert på brukerinput
    if maks_x_verdi != None or min_x_verdi != None:
        if maks_x_verdi == None:
            maks_x_verdi = max(x_verdier)
        elif min_x_verdi == None:
            min_x_verdi = min(x_verdier)
        base.set_xlim(min_x_verdi, maks_x_verdi)

    # Begrenser hvor mye av grafen man kan se i y-aksen basert på brukerinput
    if maks_y_verdi != None or min_y_verdi != None:
        if maks_y_verdi == None:
            maks_y_verdi = max(y_verdier)
        elif min_y_verdi == None:
            min_y_verdi = min(y_verdier)
        base.set_ylim(min_y_verdi, maks_y_verdi)

    # Markerer x- og y-aksen
    if vis_tydelig_x_og_y_akse:
        base.axvline(0, color="black", zorder=2)
        base.axhline(0, color="black", zorder=2)

    # Sjekker om man skal plotte som punkter eller graf
    if vis_som_punkter:
        base.scatter(x_verdier, y_verdier, color=graf_farge, zorder=3)
    else:
        base.plot(x_verdier, y_verdier, color=graf_farge, zorder=3)

    # Aksetitler
    base.set_xlabel(x_akse_tittel)
    base.set_ylabel(y_akse_tittel)

    # Tittel
    base.set_title(tittel)

def csv_til_liste_av_dict(filnavn:str, min_delimiter:str=",") -> list[dict]:
    """
    Leser en csv-fil og returnerer en liste med ordbøker

    filnavn (str) - navnet på csv-filen som skal leses
    min_delimiter(str) - det som skiller verdiene i csv-filen
    """
    with open(filnavn, encoding="utf-8-sig") as fil:
        filinnhold = csv.reader(fil, delimiter=min_delimiter)
        nokler = next(filinnhold)
        data = []
        for linje in filinnhold:
            element = {}
            for i in range(len(nokler)):
                element[nokler[i]] = linje[i]
            data.append(element)
    return data

file_name = "Datasett_fodselstall_komma.csv"

# Korrekterer stien
this_path = os.path.abspath(os.path.dirname(__file__))
path_file = os.path.join(this_path, file_name)

# Lagrer data i csv-fil som dict der alt er string
min_data = csv_til_liste_av_dict(path_file)

# Legger til netto folkevekst i data-en
for element in min_data:
    try:
        element["Netto folkevekst"] = float(element["Levendefødte i alt"]) + float(element["Innflyttinger"]) - float(element["Utflyttinger"])
    except:
        element["Netto folkevekst"] = ""

root = tk.Tk()
app = plotApp(root, "Graf eksamensoppgave 9", min_data)
root.mainloop()