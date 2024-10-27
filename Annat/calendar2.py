import json
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QInputDialog, QDialog, QMessageBox, QVBoxLayout, QCalendarWidget, QPushButton, QLabel, QLineEdit, QComboBox
import sys


class Häst:
    def __init__(self, namn, pris_per_kilo):
        self.namn = namn
        self.pris_per_kilo = pris_per_kilo
        self.data = {}  # Här sparar vi höintaget för varje dag
        self.filnamn = f'{self.namn}.json'  # Varje häst får sin egen fil
    
    def lägg_till_ho(self, datum, kilo):
        månad = datum.strftime('%Y-%m')  # Använd år-månad format för att gruppera dagarna
        self.data.setdefault(månad, {})[datum.srfttime('%Y-%m-%d')] = kilo
  
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
            return None
        
        dagar = self.data[månad]
        total_kilo = sum(dagar.values())
        total_kostnad = total_kilo * self.pris_per_kilo
        print(f"Total kostnad för {månad}: {total_kostnad} kr")
        return total_kostnad

class CalendarDialog(QDialog):
    def __init__(self, häst):
        super().__init__()
        self.häst = häst
        self.selected_date = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Logga höintag för {self.häst.namn}")
        self.setGeometry(500, 200, 500, 400)

        layout = QVBoxLayout()
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        self.kilo_label = QLabel("Ange antal kilo hö:")
        self.kilo_input = QLineEdit(self)
        layout.addWidget(self.kilo_label)
        layout.addWidget(self.kilo_input)

        self.btn_ok = QPushButton("Logga hö", self)
        self.btn_ok.clicked.connect(self.log_data)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def log_data(self):
        datum_input = self.calendar.selectedDate().toString("yyyy-MM-dd")
        kilo_input = self.kilo_input.text()

        try:
            datum = datetime.strptime(datum_input, '%Y-%m-%d')
            kilo = float(kilo_input)
            self.häst.lägg_till_ho(datum, kilo)
            self.häst.spara_data()
            self.accept()
            print(f"{kilo} kg hö har lagts till den {datum_input} för {self.häst.namn}.")
        except ValueError:
            print("Felaktigt datum eller kilo, försök igen.")


class MainDialog(QDialog):
    def __init__(self, hästar):
        super().__init__()
        self.hästar = hästar
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Höintagssystem")
        self.setGeometry(500, 200, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Välj häst:")
        layout.addWidget(self.label)

        self.häst_combo = QComboBox(self)
        self.häst_combo.addItems(self.hästar.keys())
        layout.addWidget(self.häst_combo)

        self.btn_add = QPushButton("Lägg till höintag", self)
        self.btn_add.clicked.connect(self.open_calendar)
        layout.addWidget(self.btn_add)

        self.btn_cost = QPushButton("Beräkna månadskostnad", self)
        self.btn_cost.clicked.connect(self.calculate_cost)
        layout.addWidget(self.btn_cost)

        self.btn_exit = QPushButton("Avsluta", self)
        self.btn_exit.clicked.connect(self.close_program)
        layout.addWidget(self.btn_exit)
        self.setLayout(layout)

    def open_calendar(self):
        häst_namn = self.häst_combo.currentText()
        häst = self.hästar[häst_namn]
        calendar_dialog = CalendarDialog(häst)
        calendar_dialog.exec_()

    def calculate_cost(self):
        häst_namn = self.häst_combo.currentText()
        häst = self.hästar[häst_namn]

        månad_input, ok = QInputDialog.getText(self, "Ange månad", "Ange månad (YYYY-MM):")
        if ok and månad_input:
            try:
                kostnad = häst.beräkna_kostnad(månad_input)
                if kostnad is not None:
                    QMessageBox.information(self, "Kostnadsberäkning",
                                            f"Total kostnad för {månad_input}: {kostnad:.2f} kr")
            except ValueError:
                QMessageBox.warning(self, "Fel", "Ingen data för denna månad. ")

    def close_program(self):
        for häst in self.hästar.values():
            häst.spara_data()
        print("Data sparad, Programmet avslutas.")
        self.close()

def main():
    hästar = {'Vasse': Häst('Vasse', 3.8), 'Loco': Häst('Loco', 3.8)}
    for häst in hästar.values():
        häst.ladda_data()

    app = QApplication(sys.argv)
    main_dialog = MainDialog(hästar)
    main_dialog.exec_()

if __name__ == "__main__":
    main()