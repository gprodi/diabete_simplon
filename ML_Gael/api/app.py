# app.py

# --- Imports ---
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

# --- Configuration et Chargement du Modèle ---

# Nom du fichier modèle (doit exister dans le même répertoire)
# 🚨 N'oubliez pas de remplacer XX par vos initiales !
MODEL_PATH = 'modele_diabete_XX.pkl' 

# 🔑 CHARGEMENT DU MODÈLE À L'INITIALISATION (UNE SEULE FOIS)
try:
    # Charger le pipeline complet (préprocesseur + modèle)
    model_pipeline = joblib.load(MODEL_PATH)
    print(f"Modèle chargé avec succès depuis {MODEL_PATH}")
except FileNotFoundError:
    print(f"ERREUR: Le fichier modèle {MODEL_PATH} est introuvable. Assurez-vous de le placer dans le répertoire de l'API.")
    # Le service sera disponible, mais l'endpoint /predict renverra une erreur 503.
    model_pipeline = None 

# Initialisation de l'API (l'objet 'app' est ce que Gunicorn cherchera)
app = FastAPI(
    title="API de Prédiction du Diabète",
    description="Service de classification basé sur un modèle RandomForest.",
    version="1.0.0"
)

# --- Définition du Schéma de Données (Pydantic) ---

# Pydantic garantit que les données reçues correspondent à ce format.
class PatientFeatures(BaseModel):
    age: int
    gender: int
    polyuria: int
    polydipsia: int
    sudden_weight_loss: int
    weakness: int
    polyphagia: int
    genital_thrush: int
    visual_blurring: int
    itching: int
    irritability: int
    delayed_healing: int
    partial_paresis: int
    muscle_stiffness: int
    alopecia: int
    obesity: int

# --- Définition des Endpoints ---

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Endpoint de santé pour vérifier si le service est opérationnel.
    """
    status = "ok" if model_pipeline else "error - model not loaded"
    return {"status": status, "model_loaded": model_pipeline is not None}

@app.post("/predict", tags=["Prediction"])
def predict_diabete(patient: PatientFeatures):
    """
    Reçoit les caractéristiques d'un patient et renvoie la prédiction de diabète.
    """
    # Vérification du modèle
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Service non disponible: Modèle de prédiction non chargé.")

    try:
        # 1. Conversion des données Pydantic en DataFrame (format attendu par le pipeline)
        data = patient.model_dump()
        input_df = pd.DataFrame([data])
        
        # 2. Prédiction de probabilité
        # La prédiction est maintenant rapide car le modèle est déjà en mémoire.
        proba = model_pipeline.predict_proba(input_df)[:, 1][0]
        score = float(proba)
        
        # 3. Décision (Seuil de 0.5)
        decision = "Positive" if score >= 0.5 else "Negative"
        
        # 4. Retour du résultat
        return {
            "prediction": decision,
            "probability_positive": round(score, 4),
            "comment": "Résultat stable et reproductible car le modèle est fixe."
        }
        
    except Exception as e:
        # Gérer les erreurs inattendues
        print(f"Erreur de prédiction: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne de prédiction: {type(e).__name__}: {str(e)}")