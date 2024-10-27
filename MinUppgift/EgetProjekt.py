import json
import os # Kollar om filen existerar JSON format
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QInputDialog, QDialog, QMessageBox, QVBoxLayout, QCalendarWidget, QPushButton, QLabel, QLineEdit, QComboBox)
import sys


class Häst:
    def __init__(self, namn, pris_per_kilo):
        self.namn = namn
        self.pris_per_kilo = pris_per_kilo
        self.data = {}  # Höintag per dag lagras här
        self.filnamn = f'{self.namn}.json'  # fil för att lagra hästens (Vasse/Loco) data

    def lägg_till_ho(self, datum, kilo):
        månad = datum.strftime('%Y-%m') # Grupperar datan månadsvis (år-månad)
        self.data.setdefault(månad, {})[datum.strftime('%Y-%m-%d')] = kilo # lägger till höintag för dag eller skapar ny om det ej finns
  
    def ladda_data(self): 
        if os.path.exists(self.filnamn):
            with open(self.filnamn, 'r') as fil:
                self.data = json.load(fil) # laddar data från json fil om de finns
    
    def spara_data(self): 
        with open(self.filnamn, 'w') as fil:
            json.dump(self.data, fil, indent=4) #sparar all data till json filen
    
    def beräkna_kostnad(self, månad):
        if månad not in self.data:
            print(f"Ingen data för {månad}.")
            return None # Finns ingen data för månaden returneras none
        
        total_kilo = sum(self.data[månad].values()) # Beräknar totala höintaget för månaden
        return total_kilo * self.pris_per_kilo #beräknar kostnaden baserat på pris per kilo


class CalendarDialog(QDialog): # Dialogruta där man kan välja datum och lägga in höintag för vald häst
    def __init__(self, häst): 
        super().__init__() # Ärver från klassen Häst
        self.häst = häst
        self.initUI()

    def initUI(self): # skapar fönstret med kalender och inmatningsfältet
        self.setWindowTitle(f"Logga höintag för {self.häst.namn}") # titel med hästens namn
        self.setGeometry(500, 200, 500, 400) # fönstrets storlek

        layout = QVBoxLayout()
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar) #här visas kalandern

        self.kilo_input = QLineEdit(self)
        layout.addWidget(QLabel("Ange antal kilo hö:"))
        layout.addWidget(self.kilo_input) # här matar vi in kilo hö

        btn_ok = QPushButton("Logga hö", self)
        btn_ok.clicked.connect(self.log_data) # anropar log_data när man klickar på knappen
        layout.addWidget(btn_ok) 
        self.setLayout(layout) 

    def log_data(self): # Hämtar det valda datumet och inmatat antal kilo hö
        datum_input = self.calendar.selectedDate().toString("yyyy-MM-dd")
        kilo_input = self.kilo_input.text()

        try:
            datum = datetime.strptime(datum_input, '%Y-%m-%d')
            kilo = float(kilo_input)
            self.häst.lägg_till_ho(datum, kilo) # här lägger vi till höintag för valt datum
            self.häst.spara_data() # och sparar datan till json filen
            QMessageBox.information(self, "Tjoho!", f"{kilo} kg hö har lagts till den {datum_input}.")
            self.accept()
        except ValueError: # Felhantering, användarvänligt
            QMessageBox.warning(self, "Fel", "Felaktigt datum eller kilo, försök igen!")


class MainDialog(QDialog): 
    def __init__(self, hästar):
        super().__init__()
        self.hästar = hästar
        self.initUI()

    def initUI(self): # Sätter upp huvudfönstret
        self.setWindowTitle("Höintagssystem")
        self.setGeometry(500, 200, 300, 200) # storlek o placering

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Välj häst:"))

        self.häst_combo = QComboBox(self) # Rullgardinsmeny för att välja häst
        self.häst_combo.addItems(self.hästar.keys())
        layout.addWidget(self.häst_combo)

        btn_add = QPushButton("Lägg till höintag", self) # Knappen för att mata in hö
        btn_add.clicked.connect(self.open_calendar)
        layout.addWidget(btn_add)

        btn_cost = QPushButton("Beräkna månadskostnad", self) # Knappen för att beräkna månadskostnad
        btn_cost.clicked.connect(self.calculate_cost)
        layout.addWidget(btn_cost)

        btn_exit = QPushButton("Avsluta", self) # Knappen för att avsluta programmet
        btn_exit.clicked.connect(self.close_program)
        layout.addWidget(btn_exit)
        self.setLayout(layout) 

    def open_calendar(self): # öppnar kalenderrutan för att logga hö till vald häst
        häst_namn = self.häst_combo.currentText()
        calendar_dialog = CalendarDialog(self.hästar[häst_namn])
        calendar_dialog.exec_()

    def calculate_cost(self): # beräkna kostnad för specifik månad
        häst_namn = self.häst_combo.currentText()
        häst = self.hästar[häst_namn]

        månad_input, ok = QInputDialog.getText(self, "Ange månad", "Ange månad (YYYY-MM):")
        if ok and månad_input:
            kostnad = häst.beräkna_kostnad(månad_input) # beräknar kostnad för val månad
            if kostnad is not None:
                QMessageBox.information(self, "Kostnadsberäkning", # visar den beräknade kostnaden
                                        f"Total kostnad för {månad_input}: {kostnad:.2f} kr") 
            else:
                QMessageBox.warning(self, "Fel", "Ingen data för denna månad.")

    def close_program(self): # Sparar all data och avslutar programmet
        for häst in self.hästar.values():
            häst.spara_data() # sparar varje hästs data
        print("Data sparad, Programmet avslutas.")
        self.close()


def main():
    hästar = {'Vasse': Häst('Vasse', 3.8), 'Loco': Häst('Loco', 3.8)} # skapar två hästar och laddar deras data
    for häst in hästar.values():                                      
        häst.ladda_data()

    app = QApplication(sys.argv)
    main_dialog = MainDialog(hästar)
    main_dialog.exec_()

if __name__ == "__main__":
    main()
