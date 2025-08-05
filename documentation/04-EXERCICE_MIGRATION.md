# EXERCICE PRATIQUE - Migrations de Base de Données avec SQLAlchemy

## Objectif de l'exercice

Cet exercice vise à vous apprendre comment gérer l’évolution d’un schéma de base de données en production. Vous allez réaliser les opérations suivantes :

1. Sauvegarder le schéma et les données existantes.
2. Modifier le schéma actuel.
3. Écrire un script pour migrer les données vers le nouveau schéma.
4. Vérifier la migration à l’aide de tests.


## Prérequis

* Vous avez terminé le projet précédent (modèles `Etudiant` et `CarteEtudiant` en relation 1:1).
* Vous avez une application fonctionnelle utilisant SQLAlchemy et PySide6.
* Vous comprenez le principe des modèles ORM avec SQLAlchemy.

---

## Situation initiale

Votre application actuelle gère les éléments suivants :

* **Table Etudiants** : `id`, `nom`, `prenom`
* **Table Cartes** : `id`, `numero`, `etudiant_id` (relation 1:1)

### Base de données initiale actuelle

```sql
CREATE TABLE etudiants (
    id INTEGER PRIMARY KEY,
    nom VARCHAR,
    prenom VARCHAR
);

CREATE TABLE cartes (
    id INTEGER PRIMARY KEY,
    numero VARCHAR,
    etudiant_id INTEGER UNIQUE,
    FOREIGN KEY(etudiant_id) REFERENCES etudiants(id)
);
```



## ÉTAPE 1 : Sauvegarder l'état actuel des données

### 1.1 Créer un script de sauvegarde (`backup_schema.py`)

Écrivez précisément ce script Python :

```python
# Script de sauvegarde du schéma et des données actuelles
import sqlite3
import json
from datetime import datetime

def sauvegarder_donnees():
    """Sauvegarde les données actuelles en JSON"""
    conn = sqlite3.connect("etudiants_cartes.db")
    
    etudiants = conn.execute("SELECT * FROM etudiants").fetchall()
    cartes = conn.execute("SELECT * FROM cartes").fetchall()
    
    backup = {
        "date_sauvegarde": datetime.now().isoformat(),
        "version_schema": "1.0",
        "etudiants": [
            {"id": row[0], "nom": row[1], "prenom": row[2]} 
            for row in etudiants
        ],
        "cartes": [
            {"id": row[0], "numero": row[1], "etudiant_id": row[2]} 
            for row in cartes
        ]
    }
    
    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(backup, f, indent=2, ensure_ascii=False)
    
    print(f"Sauvegarde réussie : {len(etudiants)} étudiants et {len(cartes)} cartes.")
    conn.close()

if __name__ == "__main__":
    print("Début de la sauvegarde...")
    sauvegarder_donnees()
    print("Fin de la sauvegarde.")
```

### 1.2 Exécuter le script de sauvegarde

Dans votre terminal, tapez :

```bash
python backup_schema.py
```



## ÉTAPE 2 : Modifier le schéma (nouvelle version)

### 2.1 Nouvelles exigences métier

Votre université souhaite maintenant gérer les informations supplémentaires suivantes :

* Pour chaque étudiant :

  * Email (unique)
  * Date de naissance

* Pour chaque carte étudiante :

  * Date d'émission
  * Date d'expiration
  * Statut de la carte (active, inactive, perdue)

### 2.2 Nouveau fichier modèle ORM (`database_v2.py`)

Écrivez précisément ce code :

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

engine = create_engine("sqlite:///etudiants_cartes_v2.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Etudiant(Base):
    __tablename__ = "etudiants"
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True)
    date_naissance = Column(Date)

    carte = relationship("CarteEtudiant", back_populates="etudiant", uselist=False)

class CarteEtudiant(Base):
    __tablename__ = "cartes"
    id = Column(Integer, primary_key=True)
    numero = Column(String, nullable=False)
    date_emission = Column(DateTime, default=datetime.now)
    date_expiration = Column(Date)
    statut = Column(String, default="active")
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True)

    etudiant = relationship("Etudiant", back_populates="carte")

Base.metadata.create_all(engine)
```



## ÉTAPE 3 : Créer le script de migration des données (`migration_v1_to_v2.py`)

Créez exactement ce script :

```python
import json
from datetime import datetime, date, timedelta
from database_v2 import session, Etudiant, CarteEtudiant
import glob

def charger_backup():
    backup_files = glob.glob("backup_*.json")
    if not backup_files:
        print("Aucun fichier de sauvegarde trouvé.")
        return None
    
    latest_backup = max(backup_files)
    print(f"Chargement du fichier : {latest_backup}")
    
    with open(latest_backup, "r", encoding="utf-8") as f:
        return json.load(f)

def migrer_donnees(backup_data):
    print("Début de la migration...")
    
    for etudiant_data in backup_data["etudiants"]:
        nouvel_etudiant = Etudiant(
            nom=etudiant_data["nom"],
            prenom=etudiant_data["prenom"],
            email=f"{etudiant_data['prenom'].lower()}.{etudiant_data['nom'].lower()}@universite.fr",
            date_naissance=date(2000, 1, 1)
        )
        session.add(nouvel_etudiant)
    
    session.commit()
    
    for carte_data in backup_data["cartes"]:
        etudiant = session.query(Etudiant).filter_by(id=carte_data["etudiant_id"]).first()
        if etudiant:
            nouvelle_carte = CarteEtudiant(
                numero=carte_data["numero"],
                date_emission=datetime.now(),
                date_expiration=date.today() + timedelta(days=4*365),
                statut="active",
                etudiant=etudiant
            )
            session.add(nouvelle_carte)
    
    session.commit()
    print("Migration terminée avec succès.")

if __name__ == "__main__":
    backup_data = charger_backup()
    if backup_data:
        migrer_donnees(backup_data)
```

---

## ÉTAPE 4 : Vérification des résultats de la migration (`test_migration.py`)

Écrivez ce script pour valider la migration :

```python
from database_v2 import session, Etudiant, CarteEtudiant

def test_migration():
    nb_etudiants = session.query(Etudiant).count()
    nb_cartes = session.query(CarteEtudiant).count()
    
    print("Résultats de la migration :")
    print(f"  Étudiants migrés : {nb_etudiants}")
    print(f"  Cartes migrées : {nb_cartes}")
    
    etudiant = session.query(Etudiant).first()
    if etudiant:
        print(f"Premier étudiant : {etudiant.nom}, Email : {etudiant.email}")
        if etudiant.carte:
            print(f"Carte associée : {etudiant.carte.numero}, Statut : {etudiant.carte.statut}")

if __name__ == "__main__":
    test_migration()
```



## TRAVAIL À FAIRE (obligatoire)

* **A - Exécuter complètement la migration** :

  1. Créer et exécuter la sauvegarde initiale.
  2. Créer la nouvelle version du schéma.
  3. Exécuter le script de migration.
  4. Vérifier les résultats avec le test.

* **B - Améliorer la migration** :

  1. Créer des emails réalistes et uniques.
  2. Ajouter des dates de naissance aléatoires.
  3. Ajouter des vérifications pour les données migrées.
  4. Ajouter un fichier journal détaillant chaque étape.

* **C - Mettre à jour l’interface graphique** :

  1. Ajouter les nouveaux champs dans l’interface PySide6.
  2. Permettre la recherche par email.
  3. Permettre le filtrage par statut de carte.



## Critères de succès

* Toutes les données initiales préservées.
* Les nouveaux champs remplis correctement.
* Relations 1:1 toujours valides.
* Application opérationnelle après migration.
* Tests réussis sans erreur.



## Bonus (optionnel)

* Écrire un script de retour arrière (`rollback_v2_to_v1.py`) pour restaurer l’ancien schéma en cas de problème.


<br/>
<br/>


## Commandes


### Création de l’environnement virtuel

```bash
python -m venv env
.\env\Scripts\activate  # Windows
source env/bin/activate  # Linux/macOS
```



### Installation des dépendances

```bash
pip install sqlalchemy
```



### Sauvegarde des données existantes

```bash
python backup_schema.py
```



### Création de la nouvelle base de données (schéma version 2)

```bash
python database_v2.py
```



### Lancement du script de migration

```bash
python migration_v1_to_v2.py
```


### Vérification de la migration

```bash
python test_migration.py
```



### Affichage des fichiers de sauvegarde (optionnel)

```bash
dir backup_*.json  # Windows
ls backup_*.json   # Linux/macOS
```



### (Optionnel) Revenir à l'ancien schéma

```bash
python rollback_v2_to_v1.py
```


