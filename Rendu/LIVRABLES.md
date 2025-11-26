# 📋 LIVRABLES - Projet ML Diabète (ML1 → ML6)

## Vue d'Ensemble du Projet

Ce document centralise **tous les livrables attendus** pour le projet de machine learning sur la prédiction du diabète, organisé en 6 briefs progressifs. Chaque brief construit sur le précédent pour aboutir à une application ML complète déployée sur le cloud.

---

## 🎯 Objectifs Pédagogiques Globaux

Ce projet vous permettra de maîtriser :
- **Data Science** : Préparation de données, EDA, feature engineering
- **Machine Learning** : Entraînement, évaluation, optimisation de modèles
- **API Development** : Création d'APIs REST avec FastAPI
- **Frontend Development** : Interfaces web avec Streamlit/Gradio
- **DevOps** : Conteneurisation Docker, orchestration
- **Cloud Computing** : Déploiement sur plateforme cloud (Azure/AWS/GCP)

---

## 📂 Structure Complète du Projet

```
Diabète_Olympia/
├── ML1_Extraction_Preparation_Dataset/
│   ├── README.md ✅
│   ├── data/
│   │   ├── raw/              # Données brutes originales
│   │   ├── cleaned/          # Données nettoyées
│   │   └── processed/        # Train/test sets
│   ├── notebooks/
│   │   └── 01_exploration.ipynb
│   ├── scripts/
│   │   └── preprocess.py
│   └── docs/
│       └── data_preparation_report.md
│
├── ML2_Entrainement_Modele/
│   ├── README.md ✅
│   ├── models/
│   │   ├── best_model.pkl
│   │   └── preprocessors.pkl
│   ├── notebooks/
│   │   └── 02_training.ipynb
│   ├── scripts/
│   │   └── train_model.py
│   └── reports/
│       ├── model_evaluation.md
│       ├── confusion_matrix.png
│       └── feature_importance.png
│
├── ML3_API_Scoring/
│   ├── README.md ✅
│   ├── api/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   └── tests/
│   │       └── test_api.py
│   ├── model/
│   │   ├── best_model.pkl      # Copié depuis ML2
│   │   └── preprocessors.pkl
│   └── docs/
│       ├── api_documentation.md
│       └── api_examples.sh
│
├── ML4_App_Scoring/
│   ├── README.md ✅
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   └── assets/
│   │       └── logo.png
│   └── docs/
│       ├── user_guide.md
│       └── screenshots/
│           ├── home.png
│           └── result.png
│
├── ML5_Orchestration_Docker/
│   ├── README.md ✅
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── model/
│   ├── app/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── docker-compose.yml
│   ├── .dockerignore
│   ├── .env
│   └── scripts/
│       ├── start.sh
│       └── start.ps1
│
├── ML6_Deploy_Cloud/
│   ├── README.md ✅
│   ├── manifests/
│   │   ├── k8s/              # Kubernetes (optionnel)
│   │   ├── terraform/        # Infrastructure as Code (optionnel)
│   │   └── render.yaml       # Configuration Render.com
│   ├── scripts/
│   │   └── deploy.sh
│   ├── .github/
│   │   └── workflows/
│   │       └── deploy.yml    # CI/CD GitHub Actions
│   └── docs/
│       ├── deployment_guide.md
│       ├── cloud_architecture.png
│       └── monitoring_guide.md
│
└── LIVRABLES.md ✅ (ce fichier)
```

---

## 📦 Détail des Livrables par Brief

### ML1 - Extraction et Préparation du Dataset

| # | Livrable | Chemin | Justification | Comment le Produire |
|---|----------|--------|---------------|---------------------|
| 1.1 | Dataset brut | `ML1_Extraction_Preparation_Dataset/data/raw/diabetes_raw.csv` | Point de départ non modifié pour traçabilité | Télécharger depuis Kaggle/UCI, ne jamais modifier |
| 1.2 | Notebook EDA | `ML1_Extraction_Preparation_Dataset/notebooks/01_exploration.ipynb` | Analyse exploratoire des données | Jupyter avec pandas, seaborn, matplotlib |
| 1.3 | Dataset nettoyé | `ML1_Extraction_Preparation_Dataset/data/cleaned/diabetes_clean.csv` | Données après nettoyage et feature engineering | Script `preprocess.py` |
| 1.4 | Train set | `ML1_Extraction_Preparation_Dataset/data/processed/train.csv` | 80% des données pour entraînement | `train_test_split` avec stratification |
| 1.5 | Test set | `ML1_Extraction_Preparation_Dataset/data/processed/test.csv` | 20% des données pour évaluation finale | `train_test_split` avec même random_state |
| 1.6 | Rapport préparation | `ML1_Extraction_Preparation_Dataset/docs/data_preparation_report.md` | Documentation des choix de nettoyage | Markdown récapitulatif |
| 1.7 | Script preprocessing | `ML1_Extraction_Preparation_Dataset/scripts/preprocess.py` | Reproductibilité du pipeline | Python script réutilisable |

**Dépendances** : Aucune  
**Pré-requis** : Python 3.8+, pandas, scikit-learn, jupyter  
**Durée estimée** : 1-2 jours

---

### ML2 - Entraînement du Modèle

| # | Livrable | Chemin | Justification | Comment le Produire |
|---|----------|--------|---------------|---------------------|
| 2.1 | Notebook entraînement | `ML2_Entrainement_Modele/notebooks/02_training.ipynb` | Comparaison de plusieurs modèles | Jupyter avec scikit-learn, xgboost |
| 2.2 | Modèle entraîné | `ML2_Entrainement_Modele/models/best_model.pkl` | Modèle final optimisé | `joblib.dump(model, 'best_model.pkl')` |
| 2.3 | Preprocessors | `ML2_Entrainement_Modele/models/preprocessors.pkl` | Scalers/encoders pour prédictions | `joblib.dump(scaler, 'preprocessors.pkl')` |
| 2.4 | Rapport métriques | `ML2_Entrainement_Modele/reports/model_evaluation.md` | Performances détaillées | Markdown avec classification_report |
| 2.5 | Matrice confusion | `ML2_Entrainement_Modele/reports/confusion_matrix.png` | Visualisation des erreurs | `plt.savefig()` après seaborn.heatmap |
| 2.6 | Feature importance | `ML2_Entrainement_Modele/reports/feature_importance.png` | Variables les plus prédictives | Barplot des `feature_importances_` |
| 2.7 | Script entraînement | `ML2_Entrainement_Modele/scripts/train_model.py` | Automatisation du training | Python script avec GridSearchCV |

**Dépendances** : ML1 (train.csv, test.csv)  
**Pré-requis** : scikit-learn, xgboost, joblib  
**Durée estimée** : 2-3 jours

---

### ML3 - API de Scoring

| # | Livrable | Chemin | Justification | Comment le Produire |
|---|----------|--------|---------------|---------------------|
| 3.1 | API FastAPI | `ML3_API_Scoring/api/main.py` | Endpoint de prédiction REST | FastAPI avec Pydantic |
| 3.2 | Schémas validation | `ML3_API_Scoring/api/schemas.py` | Validation des données entrantes | Pydantic BaseModel |
| 3.3 | Configuration | `ML3_API_Scoring/api/config.py` | Gestion des env vars | Python-dotenv |
| 3.4 | Requirements API | `ML3_API_Scoring/api/requirements.txt` | Dépendances Python | `pip freeze > requirements.txt` |
| 3.5 | Tests API | `ML3_API_Scoring/api/tests/test_api.py` | Tests unitaires et d'intégration | pytest avec httpx |
| 3.6 | Modèle (copie) | `ML3_API_Scoring/model/best_model.pkl` | Modèle pour l'API | Copié depuis ML2 |
| 3.7 | Documentation API | `ML3_API_Scoring/docs/api_documentation.md` | Guide d'utilisation API | Markdown + Swagger auto |
| 3.8 | Exemples cURL | `ML3_API_Scoring/docs/api_examples.sh` | Requêtes d'exemple | Script bash avec curl |

**Dépendances** : ML2 (best_model.pkl)  
**Pré-requis** : fastapi, uvicorn, pydantic  
**Durée estimée** : 1-2 jours

---

### ML4 - Application Web de Scoring

| # | Livrable | Chemin | Justification | Comment le Produire |
|---|----------|--------|---------------|---------------------|
| 4.1 | App Streamlit | `ML4_App_Scoring/app/main.py` | Interface utilisateur web | Streamlit avec requests |
| 4.2 | Configuration | `ML4_App_Scoring/app/config.py` | URL de l'API | Python script |
| 4.3 | Requirements App | `ML4_App_Scoring/app/requirements.txt` | Dépendances frontend | streamlit, requests, plotly |
| 4.4 | Assets | `ML4_App_Scoring/app/assets/logo.png` | Logo et images | Fichiers PNG/SVG |
| 4.5 | Guide utilisateur | `ML4_App_Scoring/docs/user_guide.md` | Mode d'emploi pour utilisateurs finaux | Markdown avec screenshots |
| 4.6 | Screenshots | `ML4_App_Scoring/docs/screenshots/` | Captures d'écran de l'app | PNG de l'interface |

**Dépendances** : ML3 (API en cours d'exécution)  
**Pré-requis** : streamlit, requests, plotly  
**Durée estimée** : 1-2 jours

---

### ML5 - Orchestration Docker

| # | Livrable | Chemin | Justification | Comment le Produire |
|---|----------|--------|---------------|---------------------|
| 5.1 | Dockerfile API | `ML5_Orchestration_Docker/api/Dockerfile` | Conteneurisation de l'API | Multi-stage build |
| 5.2 | Dockerfile App | `ML5_Orchestration_Docker/app/Dockerfile` | Conteneurisation de l'app | FROM python:3.11-slim |
| 5.3 | Docker Compose | `ML5_Orchestration_Docker/docker-compose.yml` | Orchestration des services | YAML avec networks |
| 5.4 | .dockerignore | `ML5_Orchestration_Docker/.dockerignore` | Optimisation du build | Exclure __pycache__, .git, etc. |
| 5.5 | Variables env | `ML5_Orchestration_Docker/.env` | Configuration Docker | API_URL, ports, etc. |
| 5.6 | Script démarrage | `ML5_Orchestration_Docker/scripts/start.sh` | Lancement rapide | Bash/PowerShell script |
| 5.7 | Guide Docker | `ML5_Orchestration_Docker/docs/docker_guide.md` | Documentation Docker | Markdown avec commandes |

**Dépendances** : ML3 (code API), ML4 (code App)  
**Pré-requis** : Docker Desktop, Docker Compose  
**Durée estimée** : 1-2 jours

---

### ML6 - Déploiement Cloud

| # | Livrable | Chemin | Justification | Comment le Produire |
|---|----------|--------|---------------|---------------------|
| 6.1 | Manifestes K8s | `ML6_Deploy_Cloud/manifests/k8s/` | Déploiement Kubernetes (optionnel) | YAML deployments, services |
| 6.2 | Terraform | `ML6_Deploy_Cloud/manifests/terraform/` | Infrastructure as Code (optionnel) | Fichiers .tf |
| 6.3 | Render config | `ML6_Deploy_Cloud/manifests/render.yaml` | Configuration Render.com | YAML avec services |
| 6.4 | Script deploy | `ML6_Deploy_Cloud/scripts/deploy.sh` | Automatisation du déploiement | Bash avec az CLI |
| 6.5 | CI/CD Pipeline | `ML6_Deploy_Cloud/.github/workflows/deploy.yml` | Intégration continue | GitHub Actions YAML |
| 6.6 | Guide déploiement | `ML6_Deploy_Cloud/docs/deployment_guide.md` | Procédure de déploiement | Markdown étape par étape |
| 6.7 | Architecture Cloud | `ML6_Deploy_Cloud/docs/cloud_architecture.png` | Diagramme d'infrastructure | Draw.io ou Lucidchart |
| 6.8 | Guide monitoring | `ML6_Deploy_Cloud/docs/monitoring_guide.md` | Configuration logs/alertes | Markdown avec Azure Monitor |

**Dépendances** : ML5 (images Docker)  
**Pré-requis** : Compte Azure/AWS/GCP, Azure CLI  
**Durée estimée** : 2-3 jours

---

## 🔗 Graphe de Dépendances entre Briefs

```
ML1 (Données)
    │
    ├── train.csv
    └── test.csv
        │
        ▼
    ML2 (Modèle)
        │
        ├── best_model.pkl
        └── preprocessors.pkl
            │
            ▼
        ML3 (API)
            │
            └── Endpoint /predict
                │
                ▼
            ML4 (App)
                │
                └── Interface Web
                    │
                    ▼
                ML5 (Docker)
                    │
                    ├── Image API
                    └── Image App
                        │
                        ▼
                    ML6 (Cloud)
                        │
                        └── Déploiement Production
```

**⚠️ Important** : Chaque brief dépend strictement du précédent. Impossible de sauter des étapes !

---

## 📝 Bonnes Pratiques à Suivre

### 1. Gestion de Version
```bash
# Toujours versionner :
✅ Code source (.py, .ipynb)
✅ Configurations (.yml, .env.example)
✅ Documentation (.md)
✅ Requirements (requirements.txt)

# Ne JAMAIS versionner :
❌ Données brutes (.csv > 10MB → utiliser Git LFS ou cloud)
❌ Modèles entraînés (.pkl > 100MB → utiliser DVC ou Azure Blob)
❌ Secrets (.env avec vraies clés)
❌ Fichiers temporaires (__pycache__, .ipynb_checkpoints)
```

### 2. Nomenclature
```
# Fichiers
snake_case.py           # Python
kebab-case.yml          # Config
PascalCase.md           # Docs (optionnel)

# Variables
UPPER_CASE              # Constantes
snake_case              # Variables/fonctions

# Git commits
feat: ajout de l'API FastAPI
fix: correction du bug de prédiction
docs: mise à jour du README
```

### 3. Documentation
- **README.md** : À la racine de chaque brief
- **Code comments** : Pour logique complexe uniquement
- **Docstrings** : Pour toutes les fonctions publiques
- **Exemples** : Toujours fournir un exemple minimal

### 4. Tests
```python
# Minimum requis
✅ Tests unitaires pour fonctions critiques
✅ Test d'intégration pour l'API
✅ Validation manuelle de l'app web

# Couverture cible : 80% pour ML3 (API)
```

---

## ⏱️ Planning Suggéré (3 Semaines)

| Semaine | Briefs | Livrables Clés |
|---------|--------|----------------|
| **Semaine 1** | ML1 + ML2 | Dataset nettoyé, Modèle entraîné |
| **Semaine 2** | ML3 + ML4 | API fonctionnelle, App déployée localement |
| **Semaine 3** | ML5 + ML6 | Conteneurs Docker, Déploiement cloud |

**⚠️ Buffer** : Prévoir 20% de temps supplémentaire pour debugging et documentation.

---

## ✅ Checklist Finale de Validation

### Avant de rendre le projet

- [ ] Tous les README.md sont complets et à jour
- [ ] Le code fonctionne sur une machine propre (test d'un collègue)
- [ ] Les requirements.txt sont exacts (`pip freeze`)
- [ ] Aucun secret n'est commité dans Git
- [ ] La documentation contient des exemples exécutables
- [ ] L'application est déployée et accessible via URL publique
- [ ] Les tests passent (pytest pour ML3)
- [ ] Le repo Git est propre (pas de fichiers inutiles)
- [ ] LIVRABLES.md liste tous les fichiers produits
- [ ] Avertissement éthique visible sur l'app web

### Qualité du Code

- [ ] Code formaté (black ou autopep8)
- [ ] Pas de warnings lors de l'exécution
- [ ] Gestion des erreurs implémentée
- [ ] Logs informatifs (pas de print() en production)

### Documentation

- [ ] Diagramme d'architecture dans ML6
- [ ] Guide de déploiement testé par quelqu'un d'autre
- [ ] Screenshots de l'app dans ML4
- [ ] Exemples cURL fonctionnels dans ML3

---

## 🚨 Avertissement Éthique (À Afficher dans l'App)

```
⚠️ AVERTISSEMENT IMPORTANT

Ce système est un Proof of Concept (PoC) éducatif développé 
dans un cadre pédagogique. Il NE DOIT PAS être utilisé pour :

❌ Établir un diagnostic médical réel
❌ Remplacer l'avis d'un professionnel de santé
❌ Prendre des décisions médicales

En cas de préoccupations concernant le diabète :
✅ Consultez un médecin qualifié
✅ Effectuez des tests médicaux officiels
✅ Suivez les recommandations de votre médecin traitant

Les prédictions de ce système sont basées sur un modèle statistique
qui peut produire des erreurs. Aucune garantie n'est fournie quant
à l'exactitude des résultats.

Conformité légale : Ce système n'est pas certifié comme dispositif
médical et ne respecte pas les normes réglementaires en vigueur
(CE, FDA, etc.) pour une utilisation clinique.
```

---

## 📚 Ressources Utiles

### Documentation Officielle
- **FastAPI** : https://fastapi.tiangolo.com/
- **Streamlit** : https://docs.streamlit.io/
- **Docker** : https://docs.docker.com/
- **Azure Container Apps** : https://learn.microsoft.com/azure/container-apps/

### Datasets Diabète
- **Pima Indians Diabetes** : https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
- **UCI ML Repository** : https://archive.ics.uci.edu/ml/datasets/diabetes

### Outils
- **GitHub** : Versioning du code
- **VS Code** : IDE recommandé
- **Postman** : Test d'API
- **Azure Portal** : Gestion cloud

---

## 🎓 Compétences Acquises

À la fin de ce projet, vous maîtriserez :

1. **Data Science** : Nettoyage, EDA, feature engineering
2. **Machine Learning** : Classification, optimisation, métriques
3. **Backend** : API REST, FastAPI, validation Pydantic
4. **Frontend** : Streamlit, interfaces utilisateur
5. **DevOps** : Docker, Docker Compose, CI/CD
6. **Cloud** : Azure/AWS/GCP, déploiement production
7. **Éthique ML** : Considérations éthiques et légales

**Félicitations** 🎉 pour avoir suivi ce parcours complet de ML en production !

---

## 📞 Support

Pour toute question sur les livrables :
1. Consulter le README.md du brief concerné
2. Vérifier la section "Erreurs Communes"
3. Consulter les exemples de code fournis
4. Demander de l'aide à votre formateur/mentor

---

**Document généré le 26 novembre 2025**  
**Version 1.0.0**  
**Projet Diabète - Simplon Olympia**
