# TUTORIEL COMPLET : Application SQLAlchemy ORM avec PySide6

## OBJECTIFS DU COURS

A la fin de ce tutoriel, vous serez capable de :
- Créer une base de données avec SQLAlchemy ORM
- Modéliser une relation 1:1 entre deux tables
- Créer une interface graphique avec PySide6
- Connecter l'interface à la base de données
- Gérer les erreurs d'encodage Python

## PRÉREQUIS

- Windows 10 ou 11
- Python 3.10+ installé
- Terminal PowerShell
- Aucune connaissance préalable requise

## PARTIE 1 : PRÉPARATION DE L'ENVIRONNEMENT

### Étape 1 : Créer le dossier du projet

Ouvrir PowerShell et taper :

```bash
New-Item -ItemType Directory -Path "etudiant_carte_project" -Force
cd etudiant_carte_project
```

### Étape 2 : Créer l'environnement virtuel

```bash
python -m venv env
.\env\Scripts\activate
```

Vérifier que `(env)` apparaît au début de votre ligne de commande.

### Étape 3 : Installer les dépendances

```bash
pip install sqlalchemy pyside6
```

Vérifier l'installation :

```bash
pip show sqlalchemy
pip show pyside6
```

## PARTIE 2 : CRÉATION DE LA BASE DE DONNÉES

### Étape 4 : Créer le fichier database.py

Créer un fichier `database.py` avec le contenu suivant :

```python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Configuration de la base SQLite
engine = create_engine("sqlite:///etudiants_cartes.db", echo=True)

# Base pour tous les modèles
Base = declarative_base()

# Session pour interagir avec la base
Session = sessionmaker(bind=engine)
session = Session()

# Modèle Etudiant
class Etudiant(Base):
    __tablename__ = "etudiants"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)

    # Relation 1:1 vers CarteEtudiant
    carte = relationship("CarteEtudiant", back_populates="etudiant", uselist=False)

    def __repr__(self):
        return f"<Etudiant(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"

# Modèle CarteEtudiant
class CarteEtudiant(Base):
    __tablename__ = "cartes"
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True)

    # Relation inverse
    etudiant = relationship("Etudiant", back_populates="carte")

    def __repr__(self):
        return f"<CarteEtudiant(id={self.id}, numero='{self.numero}', etudiant_id={self.etudiant_id})>"

# Création physique des tables dans la base
Base.metadata.create_all(engine)
```

**POINTS IMPORTANTS :**
- `# -*- coding: utf-8 -*-` : Déclaration d'encodage obligatoire
- `uselist=False` : Force la relation un-à-un
- `unique=True` : Empêche qu'un étudiant ait plusieurs cartes
- `back_populates` : Relation bidirectionnelle

### Étape 5 : Tester la base de données

```bash
python -c "import database; print('Base de donnees creee avec succes')"
```

## PARTIE 3 : CRÉATION DE L'INTERFACE GRAPHIQUE

### Étape 6 : Créer le fichier interface.py

Créer un fichier `interface.py` avec le contenu suivant :

```python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.labelNom = QLabel(self.centralwidget)
        self.labelNom.setObjectName(u"labelNom")
        self.labelNom.setGeometry(QRect(50, 50, 100, 30))
        self.lineEditNom = QLineEdit(self.centralwidget)
        self.lineEditNom.setObjectName(u"lineEditNom")
        self.lineEditNom.setGeometry(QRect(160, 50, 200, 30))
        self.labelPrenom = QLabel(self.centralwidget)
        self.labelPrenom.setObjectName(u"labelPrenom")
        self.labelPrenom.setGeometry(QRect(50, 100, 100, 30))
        self.lineEditPrenom = QLineEdit(self.centralwidget)
        self.lineEditPrenom.setObjectName(u"lineEditPrenom")
        self.lineEditPrenom.setGeometry(QRect(160, 100, 200, 30))
        self.labelNumero = QLabel(self.centralwidget)
        self.labelNumero.setObjectName(u"labelNumero")
        self.labelNumero.setGeometry(QRect(50, 150, 100, 30))
        self.lineEditNumero = QLineEdit(self.centralwidget)
        self.lineEditNumero.setObjectName(u"lineEditNumero")
        self.lineEditNumero.setGeometry(QRect(160, 150, 200, 30))
        self.pushButtonAjouter = QPushButton(self.centralwidget)
        self.pushButtonAjouter.setObjectName(u"pushButtonAjouter")
        self.pushButtonAjouter.setGeometry(QRect(160, 200, 100, 40))
        self.labelResultat = QLabel(self.centralwidget)
        self.labelResultat.setObjectName(u"labelResultat")
        self.labelResultat.setGeometry(QRect(50, 260, 500, 60))
        self.labelResultat.setWordWrap(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 600, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Application Etudiant - Carte", None))
        self.labelNom.setText(QCoreApplication.translate("MainWindow", u"Nom :", None))
        self.labelPrenom.setText(QCoreApplication.translate("MainWindow", u"Prenom :", None))
        self.labelNumero.setText(QCoreApplication.translate("MainWindow", u"N° Carte :", None))
        self.pushButtonAjouter.setText(QCoreApplication.translate("MainWindow", u"Ajouter", None))
        self.labelResultat.setText(QCoreApplication.translate("MainWindow", u"Pret a ajouter un etudiant...", None))
    # retranslateUi
```

## PARTIE 4 : APPLICATION PRINCIPALE

### Étape 7 : Créer le fichier main.py

Créer un fichier `main.py` avec le contenu suivant :

```python
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

            self.ui.labelResultat.setText(f"Succes : Etudiant {nom} {prenom} ajoute avec carte {numero}")

            self.ui.lineEditNom.clear()
            self.ui.lineEditPrenom.clear()
            self.ui.lineEditNumero.clear()

            print(f"Etudiant ajoute : {nouvel_etudiant}")

        except Exception as e:
            session.rollback()
            self.ui.labelResultat.setText(f"Erreur : {str(e)}")
            print(f"Erreur : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
```

## PARTIE 5 : LANCEMENT ET TEST

### Étape 8 : Lancer l'application

```bash
# S'assurer que l'environnement virtuel est activé
.\env\Scripts\activate

# Lancer l'application
python main.py
```

### Étape 9 : Utiliser l'application

1. Saisir un nom (ex: "Dupont")
2. Saisir un prénom (ex: "Marie")
3. Saisir un numéro de carte (ex: "CART001")
4. Cliquer sur "Ajouter"
5. Vérifier le message de succès

## PARTIE 6 : CRÉATION D'UN SCRIPT DE TEST (OPTIONNEL)

### Étape 10 : Créer test_database.py

```python
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que la base de données fonctionne correctement
"""

from database import session, Etudiant, CarteEtudiant

def test_ajout_etudiant():
    """Test d'ajout d'un étudiant avec sa carte"""
    print("Test d'ajout d'un étudiant avec sa carte...")
    
    etudiant_test = Etudiant(nom="TestNom", prenom="TestPrenom")
    carte_test = CarteEtudiant(numero="TEST001", etudiant=etudiant_test)
    
    session.add(etudiant_test)
    session.add(carte_test)
    
    try:
        session.commit()
        print(f"Etudiant ajoute : {etudiant_test}")
        print(f"Carte ajoutee : {carte_test}")
        print(f"Relation etudiant->carte : {etudiant_test.carte}")
        print(f"Relation carte->etudiant : {carte_test.etudiant}")
        
    except Exception as e:
        session.rollback()
        print(f"Erreur : {e}")

def afficher_tous_les_etudiants():
    """Afficher tous les étudiants et leurs cartes"""
    print("\nListe de tous les etudiants :")
    
    etudiants = session.query(Etudiant).all()
    
    if not etudiants:
        print("Aucun etudiant trouve.")
        return
    
    for etudiant in etudiants:
        carte_info = f"Carte: {etudiant.carte.numero}" if etudiant.carte else "Pas de carte"
        print(f"- {etudiant.nom} {etudiant.prenom} | {carte_info}")

if __name__ == "__main__":
    print("Demarrage des tests de la base de donnees...\n")
    test_ajout_etudiant()
    afficher_tous_les_etudiants()
    print("\nTests termines !")
```

### Lancer le test :

```bash
python test_database.py
```

## PARTIE 7 : DÉPANNAGE DES ERREURS COMMUNES

### Erreur 1 : "ModuleNotFoundError: No module named 'PySide6'"

**Solution :**
```bash
.\env\Scripts\activate
pip install pyside6
```

### Erreur 2 : "SyntaxError: Non-UTF-8 code starting with '\xff'"

**Cause :** Problème d'encodage des fichiers Python

**Solution :**
1. Ajouter `# -*- coding: utf-8 -*-` en première ligne de chaque fichier Python
2. Éviter les émojis dans le code
3. Sauvegarder les fichiers en UTF-8

### Erreur 3 : "can't open file 'main.py'"

**Solution :**
```bash
# Vérifier que vous êtes dans le bon répertoire
pwd
dir *.py

# Si les fichiers ne sont pas là, les recréer
```

### Erreur 4 : Interface ne s'affiche pas

**Solutions :**
1. Vérifier que l'environnement virtuel est activé
2. Vérifier que tous les fichiers sont présents
3. Relancer avec : `python main.py`

## PARTIE 8 : STRUCTURE FINALE DU PROJET

```
etudiant_carte_project/
│
├── env/                          ← Environnement virtuel Python
├── database.py                   ← Modèles SQLAlchemy (1.4 KB)
├── interface.py                  ← Interface PySide6 (3.9 KB)
├── main.py                       ← Application principale (1.8 KB)
├── test_database.py              ← Script de test (1.9 KB)
├── etudiants_cartes.db           ← Base SQLite (créée automatiquement)
└── __pycache__/                  ← Fichiers Python compilés
```

## PARTIE 9 : EXPLICATIONS TECHNIQUES

### Relation 1:1 expliquée

```
Table: etudiants           Table: cartes
+----+---------+---------+  +----+---------+-------------+
| id | nom     | prenom  |  | id | numero  | etudiant_id |
+----+---------+---------+  +----+---------+-------------+
| 1  | Dupont  | Jean    |  | 1  | CART001 | 1           |
| 2  | Martin  | Sophie  |  | 2  | CART002 | 2           |
+----+---------+---------+  +----+---------+-------------+
```

**Contraintes de la relation 1:1 :**
- Un étudiant ne peut avoir qu'une seule carte
- Une carte ne peut appartenir qu'à un seul étudiant
- `etudiant_id` est UNIQUE dans la table `cartes`
- Pas de carte sans étudiant (clé étrangère obligatoire)

### Code SQLAlchemy expliqué

```python
# Relation 1:1 côté Etudiant
carte = relationship("CarteEtudiant", back_populates="etudiant", uselist=False)

# Relation 1:1 côté CarteEtudiant
etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True)
etudiant = relationship("Etudiant", back_populates="carte")
```

**Paramètres importants :**
- `uselist=False` : Force un objet unique (pas une liste)
- `unique=True` : Contrainte d'unicité en base
- `back_populates` : Relation bidirectionnelle

## PARTIE 10 : EXTENSIONS POSSIBLES

### Extension 1 : Ajouter une date d'émission

```python
from sqlalchemy import DateTime
from datetime import datetime

class CarteEtudiant(Base):
    __tablename__ = "cartes"
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    date_emission = Column(DateTime, default=datetime.now)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True)
```

### Extension 2 : Bouton "Afficher tous"

```python
def afficher_tous_etudiants(self):
    etudiants = session.query(Etudiant).all()
    texte = "\n".join([f"{e.nom} {e.prenom} - Carte: {e.carte.numero}" 
                       for e in etudiants])
    self.ui.labelResultat.setText(texte)
```

### Extension 3 : Validation des données

```python
def valider_numero_carte(self, numero):
    if len(numero) < 4:
        return False, "Le numéro doit contenir au moins 4 caractères"
    if not numero.startswith("CART"):
        return False, "Le numéro doit commencer par CART"
    return True, ""
```

## PARTIE 11 : BONNES PRATIQUES

### À faire :
- Toujours ajouter `# -*- coding: utf-8 -*-` en première ligne
- Utiliser un environnement virtuel
- Tester chaque modification
- Gérer les exceptions avec try/except
- Valider les données utilisateur

### À éviter :
- Modifier directement `interface.py` (utiliser Qt Designer)
- Utiliser des émojis dans le code Python
- Oublier d'activer l'environnement virtuel
- Ignorer les erreurs d'encodage
- Créer des fichiers avec `echo` sous PowerShell

## CONCLUSION

Vous avez maintenant une application complète qui :
- Modélise une relation 1:1 avec SQLAlchemy
- Propose une interface graphique PySide6
- Valide et sauvegarde les données
- Gère les erreurs de manière robuste

Cette base peut être étendue pour créer des applications plus complexes avec d'autres types de relations (1:n, n:n) et des interfaces plus avancées.

## AIDE-MÉMOIRE COMMANDES

```bash
# Activer environnement
.\env\Scripts\activate

# Installer dépendances
pip install sqlalchemy pyside6

# Lancer application
python main.py

# Tester base de données
python test_database.py

# Vérifier installation
pip show sqlalchemy pyside6
```