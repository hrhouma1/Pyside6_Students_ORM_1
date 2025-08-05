# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from interface import Ui_MainWindow
from database import session, Etudiant, CarteEtudiant

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonAjouter.clicked.connect(self.ajouter_etudiant)

    def ajouter_etudiant(self):
        try:
            nom = self.ui.lineEditNom.text().strip()
            prenom = self.ui.lineEditPrenom.text().strip()
            numero = self.ui.lineEditNumero.text().strip()

            if not nom or not prenom or not numero:
                self.ui.labelResultat.setText("Erreur : Tous les champs doivent etre remplis !")
                return

            nouvel_etudiant = Etudiant(nom=nom, prenom=prenom)
            nouvelle_carte = CarteEtudiant(numero=numero, etudiant=nouvel_etudiant)

            session.add(nouvel_etudiant)
            session.add(nouvelle_carte)
            session.commit()

            self.ui.labelResultat.setText(f"Succes : Etudiant {nom} {prenom} ajoute avec la carte numero {numero}")

            self.ui.lineEditNom.clear()
            self.ui.lineEditPrenom.clear()
            self.ui.lineEditNumero.clear()

            print(f"Etudiant ajoute en base : {nouvel_etudiant}")
            print(f"Carte ajoutee en base : {nouvelle_carte}")

        except Exception as e:
            session.rollback()
            self.ui.labelResultat.setText(f"Erreur lors de l'ajout : {str(e)}")
            print(f"Erreur : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())