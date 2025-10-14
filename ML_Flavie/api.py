# main.py
import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel


# =========================
# === API FastAPI ========
# =========================

app = FastAPI()

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

@app.post("/predict")
def predict(data: PatientData):
    # Ici tu mets ton modèle ML (exemple avec valeurs aléatoires)
    # Remplace par ton joblib.load et model.predict
    pred = 1 if data.age > 50 else 0  # exemple
    proba = 0.75 if pred == 1 else 0.20
    return {"prediction": pred, "probability": proba}