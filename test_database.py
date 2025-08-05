#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que la base de données fonctionne correctement
"""

from database import session, Etudiant, CarteEtudiant

def test_ajout_etudiant():
    """Test d'ajout d'un étudiant avec sa carte"""
    print("🧪 Test d'ajout d'un étudiant avec sa carte...")
    
    # Créer un étudiant de test
    etudiant_test = Etudiant(nom="TestNom", prenom="TestPrenom")
    
    # Créer une carte de test
    carte_test = CarteEtudiant(numero="TEST001", etudiant=etudiant_test)
    
    # Ajouter à la session
    session.add(etudiant_test)
    session.add(carte_test)
    
    try:
        # Valider les changements
        session.commit()
        print(f"✅ Étudiant ajouté : {etudiant_test}")
        print(f"✅ Carte ajoutée : {carte_test}")
        
        # Vérifier la relation
        print(f"🔗 Relation étudiant->carte : {etudiant_test.carte}")
        print(f"🔗 Relation carte->étudiant : {carte_test.etudiant}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erreur : {e}")

def afficher_tous_les_etudiants():
    """Afficher tous les étudiants et leurs cartes"""
    print("\n📋 Liste de tous les étudiants :")
    
    etudiants = session.query(Etudiant).all()
    
    if not etudiants:
        print("Aucun étudiant trouvé.")
        return
    
    for etudiant in etudiants:
        carte_info = f"Carte: {etudiant.carte.numero}" if etudiant.carte else "Pas de carte"
        print(f"- {etudiant.nom} {etudiant.prenom} | {carte_info}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests de la base de données...\n")
    
    # Tester l'ajout
    test_ajout_etudiant()
    
    # Afficher tous les étudiants
    afficher_tous_les_etudiants()
    
    print("\n✅ Tests terminés !")