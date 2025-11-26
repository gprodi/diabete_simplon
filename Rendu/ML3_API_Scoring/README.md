# ML3 - API de Scoring (Prédiction en Temps Réel)

## 📋 Contexte du Brief

Ce brief consiste à créer une API REST permettant d'exposer le modèle de prédiction entraîné. L'API doit recevoir des données patient et retourner une prédiction de risque de diabète avec un niveau de confiance.

## 🎯 Objectifs

- Créer une API REST avec FastAPI ou Flask
- Charger et servir le modèle entraîné
- Implémenter un endpoint de prédiction
- Valider les données d'entrée avec des schémas Pydantic
- Gérer les erreurs et exceptions
- Ajouter de la documentation automatique (Swagger/OpenAPI)
- Implémenter des endpoints de santé (health check)
- Logger les prédictions pour monitoring

## 📦 Livrables Attendus

| Livrable | Description | Emplacement |
|----------|-------------|-------------|
| API FastAPI | Code de l'API REST | `api/main.py` |
| Schémas Pydantic | Validation des données | `api/schemas.py` |
| Configuration | Variables d'environnement | `api/.env` et `api/config.py` |
| Requirements | Dépendances Python | `api/requirements.txt` |
| Tests API | Tests unitaires et d'intégration | `api/tests/test_api.py` |
| Documentation | Guide d'utilisation de l'API | `docs/api_documentation.md` |
| Exemples cURL | Requêtes d'exemple | `docs/api_examples.sh` |

## ✅ Critères d'Évaluation

- **Fonctionnalité** : API opérationnelle retournant des prédictions correctes
- **Robustesse** : Gestion des erreurs et validation des données
- **Documentation** : Swagger automatique + documentation markdown
- **Performance** : Temps de réponse < 500ms
- **Sécurité** : Validation des inputs, gestion des erreurs sans exposition de détails sensibles
- **Logging** : Traçabilité des requêtes et prédictions
- **Tests** : Couverture de test ≥ 80%

## 🛠️ Technologies Recommandées

```python
# Framework API
fastapi >= 0.104.0
uvicorn[standard] >= 0.24.0

# Validation & Serialization
pydantic >= 2.4.0

# ML
scikit-learn >= 1.2.0
joblib >= 1.2.0

# Logging & Monitoring
python-json-logger >= 2.0.0

# Testing
pytest >= 7.4.0
httpx >= 0.25.0  # Pour tester FastAPI
```

## 📊 Entrées / Sorties

| Type | Description | Format | Source |
|------|-------------|--------|--------|
| **Entrée** | Modèle entraîné | PKL | ML2 - `models/best_model.pkl` |
| **Entrée** | Preprocessors | PKL | ML2 - `models/preprocessors.pkl` |
| **Entrée API** | Données patient (JSON) | JSON | Client HTTP |
| **Sortie API** | Prédiction + probabilité | JSON | Endpoint `/predict` |

### Exemple de requête/réponse

**Requête POST** `/predict`
```json
{
  "Pregnancies": 2,
  "Glucose": 120,
  "BloodPressure": 70,
  "SkinThickness": 20,
  "Insulin": 80,
  "BMI": 25.5,
  "DiabetesPedigreeFunction": 0.5,
  "Age": 33
}
```

**Réponse**
```json
{
  "prediction": 0,
  "prediction_label": "Pas de diabète",
  "probability": 0.85,
  "confidence": "haute",
  "timestamp": "2025-11-26T10:30:00Z"
}
```

## 🚀 Comment Lancer

### 1. Installation des dépendances

```bash
cd ML3_API_Scoring/api
pip install -r requirements.txt
```

### 2. Structure minimale du projet

```
ML3_API_Scoring/
├── api/
│   ├── main.py              # Point d'entrée de l'API
│   ├── schemas.py           # Modèles Pydantic
│   ├── config.py            # Configuration
│   ├── model_loader.py      # Chargement du modèle
│   ├── requirements.txt
│   └── tests/
│       └── test_api.py
├── model/
│   ├── best_model.pkl       # Copié depuis ML2
│   └── preprocessors.pkl
├── docs/
│   ├── api_documentation.md
│   └── api_examples.sh
└── README.md
```

### 3. Exemple minimal d'API

**`api/main.py`**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
from datetime import datetime
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation FastAPI
app = FastAPI(
    title="Diabetes Prediction API",
    description="API de prédiction du risque de diabète",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schéma de validation
class PatientData(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=20, description="Nombre de grossesses")
    Glucose: float = Field(..., gt=0, le=250, description="Taux de glucose (mg/dL)")
    BloodPressure: float = Field(..., ge=0, le=200, description="Pression artérielle (mm Hg)")
    SkinThickness: float = Field(..., ge=0, le=100, description="Épaisseur de peau (mm)")
    Insulin: float = Field(..., ge=0, le=900, description="Niveau d'insuline (μU/ml)")
    BMI: float = Field(..., gt=0, le=70, description="Indice de masse corporelle")
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3, description="Fonction de pedigree")
    Age: int = Field(..., ge=1, le=120, description="Âge en années")

    class Config:
        json_schema_extra = {
            "example": {
                "Pregnancies": 2,
                "Glucose": 120,
                "BloodPressure": 70,
                "SkinThickness": 20,
                "Insulin": 80,
                "BMI": 25.5,
                "DiabetesPedigreeFunction": 0.5,
                "Age": 33
            }
        }

# Chargement du modèle au démarrage
@app.on_event("startup")
async def load_model():
    global model
    try:
        model = joblib.load("../model/best_model.pkl")
        logger.info("Modèle chargé avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle: {e}")
        raise

@app.get("/")
async def root():
    """Endpoint racine."""
    return {
        "message": "Diabetes Prediction API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/predict")
async def predict(patient: PatientData):
    """
    Effectue une prédiction de risque de diabète.
    
    - **patient**: Données du patient (voir schéma PatientData)
    - **returns**: Prédiction avec probabilité et niveau de confiance
    """
    try:
        # Conversion en array
        features = np.array([[
            patient.Pregnancies,
            patient.Glucose,
            patient.BloodPressure,
            patient.SkinThickness,
            patient.Insulin,
            patient.BMI,
            patient.DiabetesPedigreeFunction,
            patient.Age
        ]])
        
        # Prédiction
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][prediction])
        
        # Interprétation
        label = "Diabète détecté" if prediction == 1 else "Pas de diabète"
        confidence = "haute" if probability > 0.8 else "moyenne" if probability > 0.6 else "faible"
        
        result = {
            "prediction": prediction,
            "prediction_label": label,
            "probability": round(probability, 3),
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Prédiction effectuée: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la prédiction")

# Pour le développement local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**`api/requirements.txt`**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
scikit-learn==1.3.2
joblib==1.3.2
numpy==1.24.3
pytest==7.4.3
httpx==0.25.2
```

### 4. Lancement de l'API

```bash
# Mode développement avec rechargement automatique
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Mode production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Test de l'API

```bash
# Health check
curl http://localhost:8000/health

# Prédiction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Pregnancies": 2,
    "Glucose": 120,
    "BloodPressure": 70,
    "SkinThickness": 20,
    "Insulin": 80,
    "BMI": 25.5,
    "DiabetesPedigreeFunction": 0.5,
    "Age": 33
  }'
```

Accéder à la documentation interactive : `http://localhost:8000/docs`

## ⚠️ Erreurs Communes

### Erreur 1 : Modèle non chargé correctement
```python
# ✅ BON : Vérifier que le modèle est chargé au startup
@app.on_event("startup")
async def load_model():
    global model
    try:
        model = joblib.load("../model/best_model.pkl")
        logger.info("✅ Modèle chargé")
    except FileNotFoundError:
        logger.error("❌ Fichier modèle introuvable")
        raise
```

### Erreur 2 : Pas de validation des données
```python
# ❌ MAUVAIS : Accepter n'importe quelle valeur
@app.post("/predict")
def predict(data: dict):
    features = list(data.values())  # Dangereux!

# ✅ BON : Utiliser Pydantic pour validation
@app.post("/predict")
def predict(patient: PatientData):  # Validation automatique
    ...
```

### Erreur 3 : Ordre des features incorrect
```python
# ✅ BON : S'assurer que l'ordre correspond à l'entraînement
# Documenter l'ordre attendu
FEATURE_ORDER = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]
```

### Erreur 4 : Pas de gestion des erreurs
```python
# ✅ BON : try/except + logging
try:
    prediction = model.predict(features)
    return {"prediction": int(prediction[0])}
except Exception as e:
    logger.error(f"Erreur: {e}")
    raise HTTPException(status_code=500, detail="Erreur interne")
```

## 📚 Checklist de Validation

- [ ] API répond sur tous les endpoints
- [ ] Documentation Swagger accessible
- [ ] Validation Pydantic fonctionnelle
- [ ] Health check implémenté
- [ ] Modèle chargé au démarrage
- [ ] Prédictions correctes
- [ ] Gestion des erreurs
- [ ] Logging configuré
- [ ] Tests unitaires passent
- [ ] CORS configuré si nécessaire
- [ ] Requirements.txt à jour

## 🔗 Dépendances

- **ML2_Entrainement_Modele** : Fournit le modèle `best_model.pkl` et les preprocessors

## ➡️ Suite du Projet

L'API sera consommée par l'application web dans **ML4_App_Scoring** et orchestrée avec Docker dans **ML5_Orchestration_Docker**.

---

## ⚠️ Avertissement Éthique

**Ce projet est un PoC éducatif et ne constitue en aucun cas un outil médical.**  
L'API ne doit pas être utilisée pour des diagnostics médicaux réels. Aucune donnée patient réelle ne doit transiter par cette API sans conformité RGPD et validation clinique.
