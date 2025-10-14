# app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib
import pandas as pd

# === Charger le modèle ===
try:
    model = joblib.load("model/modele_diabete_XX.pkl")
except Exception as e:
    raise RuntimeError(f"Impossible de charger le modèle : {e}")

# === Créer l'application FastAPI ===
app = FastAPI(title="API Prédiction Diabète")

# === Définir le format des données d'entrée ===

class PatientData(BaseModel):
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

# === Endpoint de santé ===
@app.get("/health")
def health():
    return {"status": "ok"}

# === Endpoint de prédiction ===
@app.post("/predict")
def predict(data: PatientData):
    # ici tu appelles ton modèle
    return {"prediction": 1, "probability": 0.85}

