# GUIDE COMPLET SQLAlchemy + PySide6 pour Étudiants

## Vue d'ensemble du projet

Ce projet démontre la création d'une application Python complète avec :
- **Base de données** : SQLAlchemy ORM avec relation 1:1
- **Interface graphique** : PySide6 
- **Fonctionnalité** : Gestion d'étudiants et leurs cartes

## Structure finale du projet

```
etudiant_carte_project/
├── env/                          ← Environnement virtuel Python
├── database.py                   ← Modèles SQLAlchemy (1.4 KB)
├── interface.py                  ← Interface PySide6 (3.9 KB)
├── interface.ui                  ← Fichier Qt Designer (3.1 KB)
├── main.py                       ← Application principale (1.8 KB)
├── test_database.py              ← Script de test (1.9 KB)
├── etudiants_cartes.db           ← Base SQLite (créée automatiquement)
└── GUIDE_ETUDIANTS.md            ← Ce guide
```

## Installation et lancement

### 1. Prérequis
- Windows 10/11
- Python 3.10+ installé

### 2. Installation rapide
```bash
# Créer et naviguer dans le projet
New-Item -ItemType Directory -Path "etudiant_carte_project" -Force
cd etudiant_carte_project

# Créer environnement virtuel
python -m venv env
.\env\Scripts\activate

# Installer dépendances
pip install sqlalchemy pyside6
```

### 3. Lancement
```bash
# Activer environnement (si pas déjà fait)
.\env\Scripts\activate

# Lancer l'application
python main.py
```

## Comment utiliser l'application

1. **Saisir les données** :
   - Nom de l'étudiant
   - Prénom de l'étudiant
   - Numéro de carte (ex: CART001)

2. **Cliquer sur "Ajouter"**

3. **Vérifier le message de confirmation**

4. **Les champs se vident automatiquement** pour une nouvelle saisie

## Architecture technique

### Base de données (database.py)
- **Moteur** : SQLite local
- **ORM** : SQLAlchemy 2.0
- **Tables** : `etudiants` et `cartes`
- **Relation** : 1:1 (un étudiant = une carte)

### Interface (interface.py + main.py)
- **Framework** : PySide6 (Qt6)
- **Composants** : QLineEdit, QPushButton, QLabel
- **Gestion événements** : Signal/slot Qt

### Relation 1:1 expliquée

```sql
-- Table etudiants
CREATE TABLE etudiants (
    id INTEGER PRIMARY KEY,
    nom VARCHAR,
    prenom VARCHAR
);

-- Table cartes
CREATE TABLE cartes (
    id INTEGER PRIMARY KEY,
    numero VARCHAR,
    etudiant_id INTEGER UNIQUE,  -- UNIQUE = relation 1:1
    FOREIGN KEY(etudiant_id) REFERENCES etudiants(id)
);
```

**Contraintes** :
- Un étudiant ne peut avoir qu'une seule carte
- Une carte appartient à un seul étudiant
- `etudiant_id` est unique dans `cartes`

## Code source détaillé

### 1. Modèles SQLAlchemy (database.py)

```python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///etudiants_cartes.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Etudiant(Base):
    __tablename__ = "etudiants"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    
    # Relation 1:1 vers CarteEtudiant
    carte = relationship("CarteEtudiant", back_populates="etudiant", uselist=False)

class CarteEtudiant(Base):
    __tablename__ = "cartes"
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True)
    
    # Relation inverse
    etudiant = relationship("Etudiant", back_populates="carte")

Base.metadata.create_all(engine)
```

**Points clés** :
- `uselist=False` : Force relation 1:1 (pas une liste)
- `unique=True` : Contrainte unicité base de données
- `back_populates` : Relation bidirectionnelle

### 2. Application principale (main.py)

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
                self.ui.labelResultat.setText("Erreur : Tous les champs requis !")
                return

            nouvel_etudiant = Etudiant(nom=nom, prenom=prenom)
            nouvelle_carte = CarteEtudiant(numero=numero, etudiant=nouvel_etudiant)

            session.add(nouvel_etudiant)
            session.add(nouvelle_carte)
            session.commit()

            self.ui.labelResultat.setText(f"Succès : {nom} {prenom} ajouté avec carte {numero}")
            
            self.ui.lineEditNom.clear()
            self.ui.lineEditPrenom.clear()
            self.ui.lineEditNumero.clear()

        except Exception as e:
            session.rollback()
            self.ui.labelResultat.setText(f"Erreur : {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
```

## Test et validation

### Script de test (test_database.py)

```python
# -*- coding: utf-8 -*-
from database import session, Etudiant, CarteEtudiant

def test_ajout_etudiant():
    etudiant_test = Etudiant(nom="TestNom", prenom="TestPrenom")
    carte_test = CarteEtudiant(numero="TEST001", etudiant=etudiant_test)
    
    session.add(etudiant_test)
    session.add(carte_test)
    session.commit()
    
    print(f"Test réussi : {etudiant_test}")
    print(f"Carte associée : {carte_test}")

if __name__ == "__main__":
    test_ajout_etudiant()
```

### Lancement du test
```bash
python test_database.py
```

## Résolution de problèmes

### Erreur 1 : "ModuleNotFoundError: No module named 'PySide6'"
```bash
.\env\Scripts\activate
pip install pyside6
```

### Erreur 2 : "SyntaxError: Non-UTF-8 code"
- Ajouter `# -*- coding: utf-8 -*-` en première ligne
- Éviter les émojis dans le code
- Sauvegarder en UTF-8

### Erreur 3 : "can't open file 'main.py'"
```bash
# Vérifier le répertoire
pwd
dir *.py
```

### Erreur 4 : Application ne se lance pas
```bash
# Vérifier environnement virtuel
.\env\Scripts\activate
python --version
pip list
```

## Extensions possibles

### 1. Ajouter validation des données
```python
def valider_numero_carte(self, numero):
    if len(numero) < 4:
        return False, "Minimum 4 caractères"
    if not numero.startswith("CART"):
        return False, "Doit commencer par CART"
    return True, ""
```

### 2. Ajouter date d'émission
```python
from datetime import datetime

class CarteEtudiant(Base):
    # ... autres champs ...
    date_emission = Column(DateTime, default=datetime.now)
```

### 3. Bouton "Afficher tous"
```python
def afficher_tous(self):
    etudiants = session.query(Etudiant).all()
    texte = "\n".join([f"{e.nom} {e.prenom} - {e.carte.numero}" 
                       for e in etudiants])
    self.ui.labelResultat.setText(texte)
```

## Concepts pédagogiques abordés

### 1. Programmation Orientée Objet
- Classes et héritage
- Méthodes et attributs
- Encapsulation

### 2. Base de données relationnelle
- Modèles ORM
- Relations entre tables
- Contraintes d'intégrité

### 3. Interface graphique
- Architecture MVC
- Événements et signaux
- Gestion d'état

### 4. Gestion d'erreurs
- Exceptions Python
- Transactions base de données
- Validation utilisateur

## Aide-mémoire commandes

```bash
# Gestion environnement
.\env\Scripts\activate              # Activer
deactivate                          # Désactiver

# Installation
pip install sqlalchemy pyside6     # Installer dépendances
pip list                           # Lister paquets installés
pip show sqlalchemy               # Détails paquet

# Lancement
python main.py                    # Application principale
python test_database.py          # Tests

# Développement
pyside6-designer                  # Qt Designer (optionnel)
python -c "import database"      # Test import
```

## Ressources supplémentaires

- **SQLAlchemy** : https://docs.sqlalchemy.org/
- **PySide6** : https://doc.qt.io/qtforpython/
- **Python** : https://docs.python.org/
- **Qt Designer** : Interface graphique pour créer des UI

## Conclusion

Ce projet illustre une application Python complète intégrant :
- Persistance de données avec SQLAlchemy
- Interface utilisateur avec PySide6  
- Architecture logicielle propre
- Gestion d'erreurs robuste

Il constitue une base solide pour développer des applications plus complexes avec des relations de données avancées et des interfaces riches.