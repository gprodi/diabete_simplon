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
    age: float = Field(..., example=50)
    glucose: float = Field(..., example=130)
    insulin: float = Field(..., example=90)
    bmi: float = Field(..., example=28.5)
    blood_pressure: float = Field(..., example=85)
    gender: str = Field(..., example="male")
    polyuria: int = Field(..., example=0)
    polydipsia: int = Field(..., example=0)
    sudden_weight_loss: int = Field(..., example=0)
    weakness: int = Field(..., example=0)
    polyphagia: int = Field(..., example=0)
    genital_thrush: int = Field(..., example=0)
    visual_blurring: int = Field(..., example=0)
    itching: int = Field(..., example=0)
    irritability: int = Field(..., example=0)
    delayed_healing: int = Field(..., example=0)
    partial_paresis: int = Field(..., example=0)
    muscle_stiffness: int = Field(..., example=0)
    alopecia: int = Field(..., example=0)
    obesity: int = Field(..., example=0)

# === Endpoint de santé ===
@app.get("/health")
def health():
    return {"status": "ok"}

# === Endpoint de prédiction ===
@app.post("/predict")
def predict(data: PatientData):
    try:
        # Convertir les données en DataFrame
        df = pd.DataFrame([data.dict()])

        # Prédiction
        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0][1]

        # Retour JSON clair
        return {
            "prediction": int(prediction),
            "probability": round(float(proba), 3),
            "decision": "Diabète détecté" if prediction == 1 else "Aucun diabète détecté"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Données invalides ou manquantes : {e}")

# === Gestion globale des erreurs de validation Pydantic ===
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Données invalides ou manquantes", "details": str(exc)}
    )
