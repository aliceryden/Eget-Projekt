
import json
import os
from colorama import Fore, Style
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QCalendarWidget, QPushButton
import sys
from PyQt5 import QtGui


class Häst: 
    def __init__(self, namn, pris_per_kilo):
        self.namn = namn
        self.pris_per_kilo = pris_per_kilo
        self.data = {}  # Här sparar vi höintaget för varje dag
        self.filnamn = f'{self.namn}.json'  # Varje häst får sin egen fil
    
    def lägg_till_ho(self, datum, kilo):
        månad = datum.strftime('%Y-%m')  # Använd år-månad format för att gruppera dagarna
        if månad not in self.data:
            self.data[månad] = {}
        self.data[månad][datum.strftime('%Y-%m-%d')] = kilo
  
    def ladda_data(self): 
        if os.path.exists(self.filnamn):
            with open(self.filnamn, 'r') as fil:
                self.data = json.load(fil)
    
    def spara_data(self): 
        with open(self.filnamn, 'w') as fil:
            json.dump(self.data, fil, indent=4)
    
    def beräkna_kostnad(self, månad):
        if månad not in self.data:
            print(f"Ingen data för {månad}.")
            return
        

        dagar = self.data[månad]
        total_kilo = sum(dagar.values())
        total_kostnad = total_kilo * self.pris_per_kilo
        print(f"Total kostnad för {månad}: {total_kostnad} kr")
        return total_kostnad


# Specifika hästklasser som ärver från förälder klassen "Häst"
class Vasse(Häst):
    def __init__(self):
        super().__init__("Vasse", 3.8)


class Loco(Häst):
    def __init__(self):
        super().__init__("Loco", 3.8)


class CalendarDialog(QDialog):
    def __init__(self, hästar):
        super().__init__()
        self.hästar = hästar
        self.selected_date = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Logga Höintag för {self.häst.namn}")
        self.setGeometry(500, 200, 500, 400)

        layout = QVBoxLayout()
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        self.btn_ok = QPushButton("Logga hö", self)
        self.btn_ok.clicked.connect(self.get_selected_date)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def get_selected_date(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-mm-dd")
        self.accept()
        return selected_date
 

def main(): # Skapar hästar
    hästar = {
        'Vasse': Vasse(), 
        'Loco': Loco()
    }
    
    for häst in hästar.values():
        häst.ladda_data() 
    
    while True: 
        print("\nMeny:")
        print("1. Lägg till höintag för en dag")
        print("2. Beräkna månadskostnad")
        print("3. Avsluta och spara data")
        val = input("Välj ett alternativ (1-3): ")

        if val == '1': # här väljer vi häst
            häst_namn = input("Ange hästens namn (Vasse, Loco): ")
            häst = hästar.get(häst_namn)
            if häst:
                app = QApplication(sys.argv)
                calendar_dialog = CalendarDialog(hästar)
                if calendar_dialog.exec_() == QDialog.Accepted:
                    datum_input = calendar_dialog.calendar.selectDate().toString("yyyy-mm-dd") # här skriver vi in vilket datum
                    kilo_input = input("Ange antal kilo hö: ") # Här lägger vi in hur många kg hö hästen fått det datumet
                    try:
                        datum = datetime.strptime(datum_input, '%Y-%m-%d')
                        kilo = float(kilo_input)
                        häst.lägg_till_ho(datum, kilo)
                        print(f"{kilo} kg hö har lagts till den {datum_input} för {häst_namn}.")
                    except ValueError:
                        print("Felaktigt datum eller kilo, försök igen.")
                else:
                    print("Ogiltigt hästnamn, försök igen.")
        
            elif val == '2': # Här räknar vi ut månadskostnaden på höet
                häst_namn = input("Vilken häst - Vasse eller Loco? ")
                häst = hästar.get(häst_namn)
                if häst:
                    månad_input = input("Ange månad (YYYY-MM): ")
                    häst.beräkna_kostnad(månad_input)
                else:
                    print("Ogiltigt hästnamn, försök igen!")
        
            elif val == '3': # Här stänger vi programmet och sparar
                for häst in hästar.values():
                    häst.spara_data()
                print("Data sparad, Programmet avslutas. :)")
                break
        
            else:
                print("Ogiltigt val, försök igen!")

if __name__ == "__main__":
    main()