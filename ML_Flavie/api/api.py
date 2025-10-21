from fastapi import FastAPI
from pydantic import BaseModel, Field, conint
import joblib
import os



# === Charger le modèle ===
# chemin absolu vers le modèle
model_path = '/model/modele_diabete_XX.pkl'
model = joblib.load(model_path)

app = FastAPI(title="API Prédiction Diabète")

# === Définition du schéma des données ===
class PatientData(BaseModel):
    age: conint(ge=0, le=120) = Field(..., description="Âge du patient (0-120)")
    gender: conint(ge=0, le=1) = Field(..., description="1 = Homme, 0 = Femme")
    polyuria: conint(ge=0, le=1)
    polydipsia: conint(ge=0, le=1)
    sudden_weight_loss: conint(ge=0, le=1)
    weakness: conint(ge=0, le=1)
    polyphagia: conint(ge=0, le=1)
    genital_thrush: conint(ge=0, le=1)
    visual_blurring: conint(ge=0, le=1)
    itching: conint(ge=0, le=1)
    irritability: conint(ge=0, le=1)
    delayed_healing: conint(ge=0, le=1)
    partial_paresis: conint(ge=0, le=1)
    muscle_stiffness: conint(ge=0, le=1)
    alopecia: conint(ge=0, le=1)
    obesity: conint(ge=0, le=1)

# === Endpoint /predict ===
@app.post("/predict")
def predict(patient: PatientData):
    try:
        # --- Convertir en DataFrame pour le modèle ---
        import pandas as pd
        data = pd.DataFrame([patient.dict()])

        # --- Prédiction ---
        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0][1]  # probabilité du diabète

        return {
            "prediction": int(pred),
            "probability": float(proba)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Ceci est mon main"}

@app.get("/predict")
def predict(value: float):
    # ici tu peux appeler ton modèle
    return {"result": value * 2}