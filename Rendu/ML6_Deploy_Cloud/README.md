# ML6 - Déploiement Cloud

## 📋 Contexte du Brief

Ce brief final consiste à déployer l'application ML complète (API + Application Web) sur une plateforme cloud (Azure, AWS, GCP, ou alternatives comme Render, Heroku) pour la rendre accessible publiquement et scalable.

## 🎯 Objectifs

- Choisir une plateforme cloud adaptée
- Déployer l'API sur le cloud (Azure Container Apps, AWS ECS, Cloud Run, etc.)
- Déployer l'application web (Azure Web Apps, AWS Amplify, Streamlit Cloud, etc.)
- Configurer le domaine et HTTPS
- Mettre en place du monitoring et logging
- Implémenter des mécanismes de scaling
- Sécuriser les endpoints (authentification si nécessaire)
- Documenter le processus de déploiement et la CI/CD

## 📦 Livrables Attendus

| Livrable | Description | Emplacement |
|----------|-------------|-------------|
| Manifestes Kubernetes (optionnel) | Fichiers de déploiement K8s | `manifests/k8s/` |
| Terraform/Bicep (optionnel) | Infrastructure as Code | `manifests/terraform/` ou `manifests/bicep/` |
| Scripts de déploiement | Automatisation du déploiement | `scripts/deploy.sh` |
| CI/CD Pipeline | GitHub Actions / Azure Pipelines | `.github/workflows/` ou `azure-pipelines.yml` |
| Documentation déploiement | Guide complet de déploiement | `docs/deployment_guide.md` |
| Architecture Cloud | Diagramme d'architecture | `docs/cloud_architecture.png` |
| Guide monitoring | Configuration monitoring/alerting | `docs/monitoring_guide.md` |

## ✅ Critères d'Évaluation

- **Accessibilité** : Application accessible via URL publique
- **Performance** : Temps de réponse < 1s, scalabilité démontrée
- **Sécurité** : HTTPS, variables d'environnement sécurisées, pas de secrets exposés
- **Fiabilité** : Monitoring et logging configurés
- **Automatisation** : CI/CD fonctionnelle
- **Documentation** : Guide de déploiement complet et reproductible
- **Coûts** : Solution optimisée (free tier privilégié pour le PoC)

## 🛠️ Technologies Recommandées

### Options Cloud

#### **Option 1 : Azure (Recommandé pour entreprise)**
```bash
# Services recommandés
- Azure Container Apps (API + App)
- Azure Container Registry (Images Docker)
- Azure Monitor (Logging/Monitoring)
- Azure Key Vault (Secrets)
```

#### **Option 2 : AWS**
```bash
# Services recommandés
- AWS ECS / Fargate (Conteneurs)
- AWS ECR (Images Docker)
- AWS CloudWatch (Monitoring)
- AWS Secrets Manager (Secrets)
```

#### **Option 3 : GCP**
```bash
# Services recommandés
- Google Cloud Run (Conteneurs serverless)
- Google Container Registry
- Google Cloud Monitoring
```

#### **Option 4 : Alternatives Low-Cost**
```bash
# Plateformes avec free tier généreux
- Render.com (Très simple, free tier)
- Railway.app (Simple, pay-as-you-go)
- Fly.io (Edge computing)
- Streamlit Cloud (Pour l'app uniquement)
- Heroku (Classique mais payant)
```

## 📊 Architecture Cloud (Exemple Azure)

```
                    ┌─────────────────────┐
                    │   Azure Front Door   │
                    │    (HTTPS/CDN)      │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        ┌───────▼────────┐          ┌────────▼───────┐
        │  Container App │          │ Container App  │
        │   (Streamlit)  │─────────▶│   (FastAPI)    │
        │  Port 8501     │          │   Port 8000    │
        └────────────────┘          └────────────────┘
                │                            │
                └────────────┬───────────────┘
                             │
                    ┌────────▼─────────┐
                    │  Azure Monitor   │
                    │  Application     │
                    │    Insights      │
                    └──────────────────┘
```

## 📊 Entrées / Sorties

| Type | Description | Source |
|------|-------------|--------|
| **Entrée** | Images Docker | ML5 - Docker images |
| **Entrée** | Configuration IaC | Terraform/Bicep/K8s |
| **Sortie** | API déployée | URL publique API |
| **Sortie** | App déployée | URL publique App |
| **Sortie** | Pipeline CI/CD | GitHub Actions/Azure Pipelines |

## 🚀 Comment Lancer

### Option A : Déploiement Azure Container Apps (Simplifié)

#### 1. Prérequis

```bash
# Installation Azure CLI
# Windows (PowerShell)
winget install Microsoft.AzureCLI

# Connexion
az login

# Créer un groupe de ressources
az group create --name rg-diabetes-app --location westeurope
```

#### 2. Déploiement de l'API

```bash
# Créer un Container Registry
az acr create --resource-group rg-diabetes-app \
  --name diabetesregistry --sku Basic

# Build et push de l'image API
az acr build --registry diabetesregistry \
  --image diabetes-api:latest \
  --file api/Dockerfile api/

# Créer Container App Environment
az containerapp env create \
  --name diabetes-env \
  --resource-group rg-diabetes-app \
  --location westeurope

# Déployer l'API
az containerapp create \
  --name diabetes-api \
  --resource-group rg-diabetes-app \
  --environment diabetes-env \
  --image diabetesregistry.azurecr.io/diabetes-api:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server diabetesregistry.azurecr.io \
  --cpu 0.5 --memory 1Gi
```

#### 3. Déploiement de l'App

```bash
# Build et push de l'image App
az acr build --registry diabetesregistry \
  --image diabetes-app:latest \
  --file app/Dockerfile app/

# Récupérer l'URL de l'API
API_URL=$(az containerapp show \
  --name diabetes-api \
  --resource-group rg-diabetes-app \
  --query properties.configuration.ingress.fqdn -o tsv)

# Déployer l'App avec l'URL de l'API
az containerapp create \
  --name diabetes-app \
  --resource-group rg-diabetes-app \
  --environment diabetes-env \
  --image diabetesregistry.azurecr.io/diabetes-app:latest \
  --target-port 8501 \
  --ingress external \
  --registry-server diabetesregistry.azurecr.io \
  --env-vars API_URL=https://$API_URL \
  --cpu 0.5 --memory 1Gi
```

### Option B : Déploiement Render.com (Plus Simple)

#### 1. Configuration `render.yaml`

**`render.yaml`**
```yaml
services:
  # API Service
  - type: web
    name: diabetes-api
    env: docker
    dockerfilePath: ./api/Dockerfile
    dockerContext: ./api
    plan: free
    healthCheckPath: /health
    envVars:
      - key: PORT
        value: 8000

  # App Service
  - type: web
    name: diabetes-app
    env: docker
    dockerfilePath: ./app/Dockerfile
    dockerContext: ./app
    plan: free
    envVars:
      - key: STREAMLIT_SERVER_PORT
        value: 8501
      - key: API_URL
        sync: false  # À configurer manuellement après déploiement de l'API
```

#### 2. Déploiement

1. Créer un compte sur [Render.com](https://render.com)
2. Connecter votre repo GitHub
3. Créer un "Blueprint" avec `render.yaml`
4. Lancer le déploiement
5. Récupérer l'URL de l'API et la configurer dans l'App

### Option C : CI/CD avec GitHub Actions

**`.github/workflows/deploy.yml`**
```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  AZURE_RESOURCE_GROUP: rg-diabetes-app
  API_NAME: diabetes-api
  APP_NAME: diabetes-app
  REGISTRY_NAME: diabetesregistry

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Build and push API image
        run: |
          az acr build --registry ${{ env.REGISTRY_NAME }} \
            --image diabetes-api:${{ github.sha }} \
            --image diabetes-api:latest \
            --file api/Dockerfile api/
      
      - name: Build and push App image
        run: |
          az acr build --registry ${{ env.REGISTRY_NAME }} \
            --image diabetes-app:${{ github.sha }} \
            --image diabetes-app:latest \
            --file app/Dockerfile app/
      
      - name: Deploy API to Container Apps
        run: |
          az containerapp update \
            --name ${{ env.API_NAME }} \
            --resource-group ${{ env.AZURE_RESOURCE_GROUP }} \
            --image ${{ env.REGISTRY_NAME }}.azurecr.io/diabetes-api:latest
      
      - name: Deploy App to Container Apps
        run: |
          az containerapp update \
            --name ${{ env.APP_NAME }} \
            --resource-group ${{ env.AZURE_RESOURCE_GROUP }} \
            --image ${{ env.REGISTRY_NAME }}.azurecr.io/diabetes-app:latest
```

### Option D : Kubernetes (Avancé)

**`manifests/k8s/api-deployment.yaml`**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: diabetes-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: diabetes-api
  template:
    metadata:
      labels:
        app: diabetes-api
    spec:
      containers:
      - name: api
        image: diabetesregistry.azurecr.io/diabetes-api:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: diabetes-api-service
spec:
  type: LoadBalancer
  selector:
    app: diabetes-api
  ports:
  - port: 80
    targetPort: 8000
```

## ⚠️ Erreurs Communes

### Erreur 1 : Variables d'environnement non configurées
```bash
# ✅ BON : Configurer les env vars dans le cloud
az containerapp update \
  --name diabetes-app \
  --set-env-vars API_URL=https://diabetes-api.azurewebsites.net
```

### Erreur 2 : CORS bloque les requêtes
```python
# Dans l'API (main.py)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://diabetes-app.azurewebsites.net"],  # URL spécifique en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Erreur 3 : Secrets exposés dans le code
```bash
# ❌ MAUVAIS : Secrets en dur
API_KEY = "secret123"

# ✅ BON : Utiliser Azure Key Vault ou variables d'environnement
API_KEY = os.getenv("API_KEY")
```

### Erreur 4 : Pas de monitoring
```bash
# ✅ BON : Activer Application Insights (Azure)
az containerapp update \
  --name diabetes-api \
  --enable-dapr \
  --dapr-app-id diabetes-api \
  --dapr-app-protocol http
```

## 📚 Checklist de Validation

- [ ] Images Docker buildées et pushées sur registry
- [ ] API déployée et accessible via URL publique
- [ ] App déployée et accessible via URL publique
- [ ] HTTPS configuré (certificat SSL)
- [ ] Variables d'environnement correctement configurées
- [ ] CORS configuré pour la communication App → API
- [ ] Health checks fonctionnels
- [ ] Monitoring/logging configuré
- [ ] CI/CD pipeline opérationnelle
- [ ] Scaling configuré (auto-scaling si possible)
- [ ] Documentation de déploiement complète
- [ ] Tests en production effectués
- [ ] Budget/coûts surveillés

## 🔍 Commandes de Monitoring

```bash
# Azure : Voir les logs de l'API
az containerapp logs show \
  --name diabetes-api \
  --resource-group rg-diabetes-app \
  --follow

# Azure : Voir les métriques
az monitor metrics list \
  --resource /subscriptions/.../diabetes-api \
  --metric-names "Requests"

# Kubernetes : Logs
kubectl logs deployment/diabetes-api -f

# Kubernetes : Métriques
kubectl top pods
```

## 💰 Estimation des Coûts (Azure)

| Service | Tier | Coût mensuel estimé |
|---------|------|---------------------|
| Container Apps (2 apps) | Consumption | ~5-10€ (trafic faible) |
| Container Registry | Basic | ~4€ |
| Application Insights | Basic | ~0-5€ (inclus dans free tier) |
| **Total** | | **~10-20€/mois** |

**Free Tier** : Azure offre 180 000 vCPU-secondes gratuits/mois pour Container Apps.

## 🔗 Dépendances

- **ML5_Orchestration_Docker** : Images Docker à déployer

## ➡️ Fin du Projet

Ce brief finalise le parcours ML complet : de la donnée brute au déploiement cloud en production !

---

## ⚠️ Avertissement Éthique et Légal

**Ce projet est un PoC éducatif et ne constitue en aucun cas un outil médical certifié.**

### En production, vous DEVEZ :
- ✅ Obtenir une **certification dispositif médical** (marquage CE, FDA selon zone géographique)
- ✅ Respecter le **RGPD** pour toute donnée de santé
- ✅ Mettre en place une **authentification robuste** (OAuth2, SAML)
- ✅ Chiffrer toutes les communications (HTTPS obligatoire)
- ✅ Implémenter un **audit trail** complet
- ✅ Ajouter des mentions légales et CGU
- ✅ Obtenir le consentement explicite des utilisateurs
- ✅ Mettre en place une supervision médicale

**Ne jamais déployer cet outil en production sans ces prérequis légaux et éthiques.**
