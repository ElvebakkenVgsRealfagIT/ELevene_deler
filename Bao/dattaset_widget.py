"""
Program har ikke alle limiter/funksjon ennå og du må manuel sette år gjennom klikk fordi jeg finne ikke hvordan å lage dropdown på PyQt6
men jeg tror jeg har ganske bra kontrol med plt og csv men jeg har ikke veldig godt med pandas ennå
"""

import csv
import os.path
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QApplication
import PyQt6.QtWidgets as pw
import sys

filnavn = "Datasett_fodselstall_komma.csv"
this_path= os.path.abspath(os.path.dirname(__file__))
file_path=os.path.join(this_path,filnavn)

år = []
start_år=0
slutt_år=0
levendefødte = []
innflyttinger = []
utflyttinger = []

def convert_to_int_list(string_list):
    new_list = []
    for x in string_list:
        if x.strip().isdigit():
            new_list.append(int(x))
        else:
            new_list.append(0)
    return new_list

def plot_plot(x,y,ylab):
    plt.plot(x,y)
    plt.xlabel('År')
    plt.ylabel(ylab)
    plt.grid()
    plt.show()

with open(file_path, encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=",")
    overskrift = next(filinnhold)
    
    for rad in filinnhold:
        år.append(rad[0])   
        levendefødte.append(rad[1])
        innflyttinger.append(rad[2])   
        utflyttinger.append(rad[3])

år = convert_to_int_list(år)
levendefødte = convert_to_int_list(levendefødte)
innflyttinger = convert_to_int_list(innflyttinger)
utflyttinger = convert_to_int_list(utflyttinger)

#mian window
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.list_chooser= ['levendefødte','innflytninger','utflytninger']
        self.chooser_index=0
        self.counter_1=1945
        self.counter_2=1945

        #overskrift top
        self.overskrift = pw.QLabel("Valg en år og en element")
        self.knapp = pw.QPushButton("start år: "+ str(self.counter_1)) #det viser number som har klikk
        self.knapp_2 = pw.QPushButton("slutt år: "+ str(self.counter_2))
        self.knapp_3= pw.QPushButton(str(self.list_chooser[self.chooser_index]))
        self.knapp_4= pw.QPushButton("Enter")

        #menu maker
        self.menu_1= pw.QMenu(self)
        self.menu_2=pw.QMenu(self)
        self.menu_3= pw.QMenu(self)

        #add item in menu

        for item in self.list_chooser:
            action=self.menu_3.addAction(item)
            action.triggered.connect(lambda checked, text=item: self.klikk_3(text))


#/**/ er kommentarer
        self.setStyleSheet("""
            QWidget { /* bytte background farge */
                background-color: #FF69B4;
                color: #255105180;
            }
            /*for alle label eller button (litt dum)*/
            QLabel {
                font-size: 24px;
                font-weight: lighter;
                margin-left: 50px;
                margin-right: auto;
                margin-top: -100px;
                margin-bottom: auto;
            }
            QPushButton {
                background-color: #555555;
                color: #ffffff;
            }
        """)
        
        #event handler 
        self.knapp_3.setMenu(self.menu_3)
        self.knapp.clicked.connect(self.klikk)
        self.knapp_2.clicked.connect(self.klikk_2)
        #self.knapp_3.clicked.connect(self.klikk_3)
        self.knapp_4.clicked.connect(self.klikk_4)

        #layout output 
        layout = pw.QVBoxLayout()
        layout.addWidget(self.overskrift)
        layout.addWidget(self.knapp)
        layout.addWidget(self.knapp_2)
        layout.addWidget(self.knapp_3)
        layout.addWidget(self.knapp_4)

        self.setLayout(layout)
    
    def start_år_getter(self, år):
        def handler():
            if år <self.counter_2:
                self.counter_1= år
                self.knapp.setText("Start år: " + str(self.counter_1))
        return handler
    
    def slutt_år_getter(self,år):
        def handler():
            if år>self.counter_1:
                self.counter_2= år
                self.knapp_2.setText("Slutt år: " + str(self.counter_2))
        return handler
    #event knatt 1
    def klikk(self):
        if self.counter_1<self.counter_2:
            self.counter_1 += 1
            self.knapp.setText("start år: "+ str(self.counter_1))
        else:
            self.sounter_1=self.counter_1

    #event knatt 2
    def klikk_2(self):
        if self.counter_2<2023:
            self.counter_2 += 1
            self.knapp_2.setText("slutt år: "+ str(self.counter_2))
        else:
            self.counter_2=self.counter_2

    def klikk_3(self,text):
        self.chooser_index= self.list_chooser.index(text)
        self.knapp_3.setText(text)

    def klikk_4(self):
        start_index = år.index(self.counter_1)
        end_index = år.index(self.counter_2+1)
        selected_year_list = år[start_index:end_index]

        if str(self.list_chooser[self.chooser_index])== 'levendefødte':
            plot_plot(selected_year_list,levendefødte[start_index:end_index],"levendefødte")
        elif  str(self.list_chooser[self.chooser_index])== 'innflytninger':
            plot_plot(selected_year_list, innflyttinger[start_index:end_index],"innfltninger")
        else:
            plot_plot(selected_year_list, utflyttinger[start_index:end_index],"utflytninger")


#window obj ini
app = QApplication(sys.argv)

#ini window
window = Main()
window.setWindowTitle("PyQt6 something something befolkning")  
window.resize(400, 300)  
window.show()

sys.exit(app.exec())