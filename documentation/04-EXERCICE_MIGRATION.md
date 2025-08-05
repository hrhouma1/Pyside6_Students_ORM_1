# EXERCICE PRATIQUE - Migrations de Base de Données

## 🎯 Objectif de l'exercice

Apprendre à gérer l'évolution d'un schéma de base de données en production en :
1. Modifiant le schéma existant
2. Créant une migration
3. Sauvegardant l'ancien schéma  
4. Appliquant la migration

---

## 📋 Prérequis

- Avoir terminé le projet de base (documents 01-03)
- Application SQLAlchemy + PySide6 fonctionnelle
- Comprendre les modèles `Etudiant` et `CarteEtudiant`

---

## 🗂️ Situation initiale

Votre application actuelle gère :
- **Étudiants** : `id`, `nom`, `prenom`
- **Cartes** : `id`, `numero`, `etudiant_id` (relation 1:1)

### Base de données actuelle
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

---

## 🚀 ÉTAPE 1 : Sauvegarder l'état actuel

### 1.1 Créer un script de sauvegarde

Créer `backup_schema.py` :

```python
# -*- coding: utf-8 -*-
"""
Script de sauvegarde du schéma et des données actuelles
"""
import sqlite3
import json
from datetime import datetime

def sauvegarder_donnees():
    """Sauvegarde les données actuelles en JSON"""
    conn = sqlite3.connect("etudiants_cartes.db")
    
    # Récupérer tous les étudiants
    etudiants = conn.execute("SELECT * FROM etudiants").fetchall()
    cartes = conn.execute("SELECT * FROM cartes").fetchall()
    
    # Créer la sauvegarde
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
    
    # Sauvegarder en JSON
    with open(f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w", encoding="utf-8") as f:
        json.dump(backup, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Sauvegarde créée : {len(etudiants)} étudiants, {len(cartes)} cartes")
    conn.close()

if __name__ == "__main__":
    print("🔄 Sauvegarde en cours...")
    sauvegarder_donnees()
    print("✅ Sauvegarde terminée !")
```

### 1.2 Exécuter la sauvegarde

```bash
python backup_schema.py
```

---

## 🔄 ÉTAPE 2 : Modifier le schéma

### 2.1 Nouvelles exigences

L'université souhaite ajouter :
- **Date de naissance** pour les étudiants
- **Date d'émission** et **date d'expiration** pour les cartes
- **Email** de l'étudiant
- **Statut** de la carte (active/inactive/perdue)

### 2.2 Nouveau modèle `database_v2.py`

```python
# -*- coding: utf-8 -*-
"""
Modèles SQLAlchemy version 2.0 - Schéma étendu
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Configuration de la base SQLite
engine = create_engine("sqlite:///etudiants_cartes_v2.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Modèle Etudiant Version 2
class Etudiant(Base):
    __tablename__ = "etudiants"
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True)  # NOUVEAU
    date_naissance = Column(Date)        # NOUVEAU

    # Relation 1:1 vers CarteEtudiant
    carte = relationship("CarteEtudiant", back_populates="etudiant", uselist=False)

# Modèle CarteEtudiant Version 2
class CarteEtudiant(Base):
    __tablename__ = "cartes"
    id = Column(Integer, primary_key=True)
    numero = Column(String, nullable=False)
    date_emission = Column(DateTime, default=datetime.now)    # NOUVEAU
    date_expiration = Column(Date)                            # NOUVEAU
    statut = Column(String, default="active")                # NOUVEAU
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True)

    # Relation inverse
    etudiant = relationship("Etudiant", back_populates="carte")

# Création des tables
Base.metadata.create_all(engine)
```

---

## 🔀 ÉTAPE 3 : Créer le script de migration

### 3.1 Script `migration_v1_to_v2.py`

```python
# -*- coding: utf-8 -*-
"""
Script de migration de la version 1 vers la version 2
"""
import json
from datetime import datetime, date, timedelta
from database_v2 import session, Etudiant, CarteEtudiant

def charger_backup():
    """Charge les données de l'ancienne base"""
    import glob
    backup_files = glob.glob("backup_*.json")
    if not backup_files:
        print("❌ Aucun fichier de sauvegarde trouvé !")
        return None
    
    latest_backup = max(backup_files)
    print(f"📂 Chargement de {latest_backup}")
    
    with open(latest_backup, "r", encoding="utf-8") as f:
        return json.load(f)

def migrer_donnees(backup_data):
    """Migre toutes les données"""
    print("🔄 Migration des données...")
    
    for etudiant_data in backup_data["etudiants"]:
        # Créer nouvel étudiant avec nouveaux champs
        nouvel_etudiant = Etudiant(
            nom=etudiant_data["nom"],
            prenom=etudiant_data["prenom"],
            email=f"{etudiant_data['prenom'].lower()}.{etudiant_data['nom'].lower()}@universite.fr",
            date_naissance=date(2000, 1, 1)
        )
        session.add(nouvel_etudiant)
    
    session.commit()
    
    # Migrer les cartes
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
    print("✅ Migration terminée !")

if __name__ == "__main__":
    backup_data = charger_backup()
    if backup_data:
        migrer_donnees(backup_data)
```

---

## 🧪 ÉTAPE 4 : Tests et validation

### 4.1 Script de test `test_migration.py`

```python
# -*- coding: utf-8 -*-
"""
Tests pour valider la migration
"""
from database_v2 import session, Etudiant, CarteEtudiant

def test_migration():
    """Vérifie que la migration s'est bien passée"""
    nb_etudiants = session.query(Etudiant).count()
    nb_cartes = session.query(CarteEtudiant).count()
    
    print(f"📊 Résultats :")
    print(f"   - Étudiants migrés : {nb_etudiants}")
    print(f"   - Cartes migrées : {nb_cartes}")
    
    # Vérifier les nouveaux champs
    etudiant = session.query(Etudiant).first()
    if etudiant:
        print(f"✅ Exemple : {etudiant.nom} ({etudiant.email})")
        if etudiant.carte:
            print(f"   Carte : {etudiant.carte.numero} - {etudiant.carte.statut}")

if __name__ == "__main__":
    test_migration()
```

---

## 📝 TRAVAIL À FAIRE

### Exercice A : Exécution de la migration

1. **Sauvegarder** : Créer et exécuter `backup_schema.py`
2. **Nouveau schéma** : Créer `database_v2.py`
3. **Migrer** : Créer et exécuter `migration_v1_to_v2.py`
4. **Tester** : Créer et exécuter `test_migration.py`

### Exercice B : Améliorer la migration

1. **Générer des emails** plus réalistes
2. **Calculer des dates de naissance** aléatoires
3. **Ajouter une validation** des données
4. **Créer un log** détaillé

### Exercice C : Interface mise à jour

1. **Adapter l'interface** pour les nouveaux champs
2. **Ajouter une recherche** par email
3. **Implémenter un filtre** par statut
4. **Créer un rapport** de migration

---

## 🏆 Critères de réussite

- ✅ Toutes les données originales sont préservées
- ✅ Les nouveaux champs ont des valeurs cohérentes
- ✅ Les relations 1:1 fonctionnent toujours
- ✅ L'application v2 fonctionne
- ✅ Les tests passent

---

## 💡 Bonus

Créer un script `rollback_v2_to_v1.py` pour revenir à l'ancien schéma si nécessaire.

---

## 📚 Concepts appris

- **Versioning** de base de données
- **Migrations** de schéma
- **Sauvegarde/Restauration** de données
- **Tests** de migration
- **Planification** de montée de version

---

*Cet exercice simule une situation réelle où le schéma évolue mais les données doivent être préservées.*