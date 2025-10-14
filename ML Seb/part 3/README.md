# API de Prédiction du Diabète (ML 3)

Ce service implémente l'étape de prédiction du modèle de classification de diabète développé dans le brief 2 (Random Forest).

## Technologies Utilisées
- **Framework :** FastAPI (pour sa rapidité et sa validation de données native via Pydantic).
- **Modèle :** `modele_diabete_XX.pkl` (Pipeline scikit-learn contenant le StandardScaler et le RandomForestClassifier).

## 1. Prérequis

Assurez-vous d'avoir Python 3.8+ et d'installer les dépendances :

```bash
pip install -r requirements.txt

## 2. Lancement du Service
Utilisez uvicorn pour lancer le serveur :

```bash
uvicorn app:app --reload

Le service sera accessible à l'adresse : http://127.0.0.1:8000
La documentation interactive de l'API est disponible ici : http://127.0.0.1:8000/docs

## 3. Endpoints
### 3.1. Endpoint de Santé : /health (GET)
Vérifie l'état de l'API et le chargement du modèle.

```bash

curl -X 'GET' 'http://127.0.0.1:8000/health'
# Réponse OK : {"status":"ok","model_loaded":true}

### 3.2. Endpoint de Prédiction : /predict (POST)
Reçoit les caractéristiques d'un patient en JSON et renvoie la prédiction.
Les caractéristiques binaires doivent être 0 (Négatif/No/Female) ou 1 (Positif/Yes/Male).

Exemple 1 : Cas Négatif (OK)
Jeune patient avec peu de symptômes.


```bash
curl -X 'POST' 'http://127.0.0.1:8000/predict' \
-H 'Content-Type: application/json' \
-d '{
  "age": 30,
  "gender": 1,
  "polyuria": 0,
  "polydipsia": 0,
  "sudden_weight_loss": 0,
  "weakness": 0,
  "polyphagia": 0,
  "genital_thrush": 0,
  "visual_blurring": 0,
  "itching": 0,
  "irritability": 0,
  "delayed_healing": 0,
  "partial_paresis": 0,
  "muscle_stiffness": 0,
  "alopecia": 0,
  "obesity": 0
}'
Exemple 2 : Cas Positif (OK)
Patient d'âge moyen avec Polyurie et Polydipsie.

```bash
curl -X 'POST' 'http://127.0.0.1:8000/predict' \
-H 'Content-Type: application/json' \
-d '{
  "age": 30,
  "gender": 1,
  "polyuria": 1,
  "polydipsia": 1,
  "sudden_weight_loss": 0,
  "weakness": 0,
  "polyphagia": 1,
  "genital_thrush": 0,
  "visual_blurring": 0,
  "itching": 0,
  "irritability": 0,
  "delayed_healing": 0,
  "partial_paresis": 1,
  "muscle_stiffness": 0,
  "alopecia": 0,
  "obesity": 0
}'
Exemple 3 : Cas Erreur (Code 422 - Validation Pydantic)
Tentative d'envoyer 'Yes' au lieu de 1 pour polyuria.

```bash
curl -X POST "http://127.0.0.1:8000/predict" 
-H "Content-Type: application/json" 
-d "{
    \"age\": 55, 
    \"gender\": 1, 
    \"polyuria\": \"NON\", 
    \"polydipsia\": 1, 
    \"sudden_weight_loss\": 1, 
    \"weakness\": 1, 
    \"polyphagia\": 1, 
    \"genital_thrush\": 1, 
    \"visual_blurring\": 1, 
    \"itching\": 1, 
    \"irritability\": 0, 
    \"delayed_healing\": 1, 
    \"partial_paresis\": 1, 
    \"muscle_stiffness\": 0, 
    \"alopecia\": 1, 
    \"obesity\": 0
    }"
# Réponse : Code 422 Unprocessable Entity avec message d'erreur clair.

Rappel éthique :
C’est un exemple éducatif, pas un vrai outil médical.