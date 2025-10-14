## 🚀 ML2 – Entraînement du modèle prédictif

### 🎯 Objectif
Créer un modèle capable de prédire la présence ou l’absence de diabète.

### 📊 Données utilisées
- Variables principales :  
`age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, polyphagia, genital_thrush, visual_blurring, itching, irritability, delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity, class`
- `class` :  
  - `1` → diabète détecté  
  - `0` → aucun diabète

### ⚙️ Étapes
1. **Chargement des données** depuis CSV ou base.
2. **Prétraitement** :
   - Conversion des variables catégorielles (ex : `gender`) en numérique.
   - Gestion des valeurs manquantes.
   - Normalisation ou standardisation si nécessaire.
3. **Séparation du dataset** : train / test.
4. **Entraînement du modèle** : Random Forest ou Logistic Regression.
5. **Évaluation** : précision, rappel, F1-score, matrice de confusion.
6. **Sauvegarde** du modèle :  
```python
joblib.dump(model, "model/modele_diabete_XX.pkl")
```