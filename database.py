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