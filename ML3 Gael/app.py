# app.py

# --- Imports ---
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

# --- Configuration et Chargement du Modèle ---

# Nom du fichier modèle (doit exister dans le même répertoire)
MODEL_PATH = 'modele_diabete_XX.pkl' 
# 🚨 N'oubliez pas de remplacer XX par vos initiales !

try:
    # Charger le pipeline complet (préprocesseur + modèle)
    model_pipeline = joblib.load(MODEL_PATH)
    print(f"Modèle chargé avec succès depuis {MODEL_PATH}")
except FileNotFoundError:
    print(f"ERREUR: Le fichier modèle {MODEL_PATH} est introuvable. Assurez-vous de le placer dans le répertoire de l'API.")
    # Permet à l'application de démarrer même sans modèle, mais toutes les requêtes /predict échoueront.
    model_pipeline = None 

# Initialisation de l'API
app = FastAPI(
    title="API de Prédiction du Diabète",
    description="Service de classification basé sur un modèle RandomForest.",
    version="1.0.0"
)

# --- Définition du Schéma de Données (Pydantic) ---

# Pydantic garantit que les données reçues correspondent à ce format.
# Cela gère les "erreurs si une valeur manque ou est incorrecte" (Critère de performance).
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

@app.get("/health")
def health_check():
    """
    Endpoint de santé pour vérifier si le service est opérationnel.
    """
    status = "ok" if model_pipeline else "error - model not loaded"
    return {"status": status, "model_loaded": model_pipeline is not None}

@app.post("/predict")
def predict_diabete(patient: PatientFeatures):
    """
    Reçoit les caractéristiques d'un patient et renvoie la prédiction de diabète.
    Les entrées binaires (Gender, Symptômes) doivent être 0 (No/Female) ou 1 (Yes/Male).
    """
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Service non disponible: Modèle de prédiction non chargé.")

    try:
        # 1. Conversion des données Pydantic en DataFrame (format attendu par le pipeline)
        data = patient.model_dump()
        input_df = pd.DataFrame([data])
        
        # S'assurer que les colonnes sont dans le bon ordre (celui utilisé lors de l'entraînement)
        # Note: L'ordre des colonnes du modèle Pydantic doit correspondre aux colonnes du train set
        # L'ordre par défaut de Pydantic est l'ordre de définition.
        
        # 2. Prédiction de probabilité
        proba = model_pipeline.predict_proba(input_df)[:, 1][0]
        score = float(proba) # Probabilité d'être de classe Positive (diabète)
        
        # 3. Décision (Seuil de 0.5)
        prediction_binary = (score >= 0.5) * 1 # 1 si score >= 0.5, 0 sinon
        decision = "Positive" if prediction_binary == 1 else "Negative"
        
        # 4. Retour du résultat
        return {
            "prediction": decision,
            "probability_positive": round(score, 4),
            "comment": "Résultat stable et reproductible car le modèle est fixe."
        }
        
    except Exception as e:
        # Gérer les erreurs inattendues durant la prédiction (ex: mauvaise forme de données après l'étape Pydantic)
        print(f"Erreur de prédiction: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne de prédiction: {str(e)}")

# --- Commandes de Lancement (pour le README) ---
# Pour lancer l'API : uvicorn app:app --reload
# Port par défaut : http://127.0.0.1:8000
# Documentation Swagger : http://127.0.0.1:8000/docs