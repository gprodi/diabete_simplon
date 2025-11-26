# ML5 - Orchestration avec Docker

## 📋 Contexte du Brief

Ce brief consiste à conteneuriser l'API et l'application web développées précédemment, puis à orchestrer les deux services avec Docker Compose pour permettre un déploiement simplifié et reproductible.

## 🎯 Objectifs

- Créer un Dockerfile pour l'API (ML3)
- Créer un Dockerfile pour l'application web (ML4)
- Configurer Docker Compose pour orchestrer les services
- Gérer les réseaux et volumes Docker
- Implémenter des health checks
- Optimiser les images (multi-stage builds)
- Documenter le processus de build et déploiement
- Tester la communication inter-conteneurs

## 📦 Livrables Attendus

| Livrable | Description | Emplacement |
|----------|-------------|-------------|
| Dockerfile API | Image Docker pour l'API FastAPI | `api/Dockerfile` |
| Dockerfile App | Image Docker pour l'app Streamlit | `app/Dockerfile` |
| docker-compose.yml | Orchestration des services | `docker-compose.yml` |
| .dockerignore | Fichiers à exclure du build | `.dockerignore` |
| .env | Variables d'environnement | `.env` |
| Documentation | Guide Docker complet | `docs/docker_guide.md` |
| Scripts | Scripts de démarrage/arrêt | `scripts/` |

## ✅ Critères d'Évaluation

- **Fonctionnalité** : Les conteneurs se lancent et communiquent correctement
- **Optimisation** : Images légères et build rapide
- **Reproductibilité** : Déploiement en une commande
- **Isolation** : Services correctement isolés
- **Networking** : Communication inter-conteneurs fonctionnelle
- **Persistence** : Volumes pour les données importantes
- **Robustesse** : Health checks et restart policies
- **Documentation** : Guide clair pour build et run

## 🛠️ Technologies Recommandées

```yaml
# Docker
Docker >= 24.0
Docker Compose >= 2.20

# Images de base recommandées
python:3.11-slim  # Pour API et App
```

## 📊 Architecture des Services

```
┌─────────────────────────────────────┐
│     Utilisateur (Navigateur)        │
└──────────────┬──────────────────────┘
               │ Port 8501
               ▼
┌─────────────────────────────────────┐
│   Conteneur: streamlit-app          │
│   Image: diabetes-app:latest        │
│   - Streamlit UI                    │
│   - Communique avec API             │
└──────────────┬──────────────────────┘
               │ Réseau interne
               │ Port 8000
               ▼
┌─────────────────────────────────────┐
│   Conteneur: fastapi-api            │
│   Image: diabetes-api:latest        │
│   - FastAPI REST API                │
│   - Modèle ML chargé                │
└─────────────────────────────────────┘
```

## 📊 Entrées / Sorties

| Type | Description | Source |
|------|-------------|--------|
| **Entrée** | Code API + modèle | ML3 |
| **Entrée** | Code App | ML4 |
| **Sortie** | Image Docker API | `diabetes-api:latest` |
| **Sortie** | Image Docker App | `diabetes-app:latest` |
| **Sortie** | Services orchestrés | Docker Compose |

## 🚀 Comment Lancer

### 1. Structure minimale du projet

```
ML5_Orchestration_Docker/
├── api/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── model/
│       └── best_model.pkl
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml
├── .dockerignore
├── .env
└── README.md
```

### 2. Dockerfile pour l'API

**`api/Dockerfile`**
```dockerfile
# Multi-stage build pour optimiser la taille
FROM python:3.11-slim as builder

WORKDIR /app

# Installation des dépendances dans un environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage final
FROM python:3.11-slim

WORKDIR /app

# Copie de l'environnement virtuel depuis le builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copie du code et du modèle
COPY main.py .
COPY model/ ./model/

# Utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exposition du port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Lancement de l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Dockerfile pour l'App

**`app/Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY main.py .
COPY assets/ ./assets/

# Utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exposition du port Streamlit
EXPOSE 8501

# Health check pour Streamlit
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Lancement de Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 4. Docker Compose

**`docker-compose.yml`**
```yaml
version: '3.8'

services:
  # Service API FastAPI
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: diabetes-api
    image: diabetes-api:latest
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - diabetes-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # Service Application Streamlit
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: diabetes-app
    image: diabetes-app:latest
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
      - PYTHONUNBUFFERED=1
    depends_on:
      api:
        condition: service_healthy
    networks:
      - diabetes-network
    restart: unless-stopped

networks:
  diabetes-network:
    driver: bridge
    name: diabetes-network

# Volumes (optionnel pour logs ou données)
volumes:
  api-logs:
    name: diabetes-api-logs
  app-logs:
    name: diabetes-app-logs
```

### 5. .dockerignore

**`.dockerignore`**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# Jupyter
*.ipynb
.ipynb_checkpoints

# IDE
.vscode/
.idea/
*.swp

# Git
.git/
.gitignore

# Documentation
README.md
docs/

# Tests
tests/
*.pytest_cache

# OS
.DS_Store
Thumbs.db
```

### 6. Variables d'environnement

**`.env`**
```bash
# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# App Configuration
APP_PORT=8501
STREAMLIT_SERVER_PORT=8501

# Model
MODEL_PATH=./model/best_model.pkl
```

### 7. Lancement des services

```bash
# Build et lancement
docker-compose up --build

# Mode détaché (background)
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

### 8. Accès aux services

- **API** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs
- **Application** : http://localhost:8501

### 9. Scripts utilitaires

**`scripts/start.sh`** (Linux/Mac)
```bash
#!/bin/bash
echo "🚀 Démarrage des services Docker..."
docker-compose up -d
echo "✅ Services démarrés!"
echo "📊 API: http://localhost:8000"
echo "🖥️  App: http://localhost:8501"
```

**`scripts/start.ps1`** (Windows PowerShell)
```powershell
Write-Host "🚀 Démarrage des services Docker..." -ForegroundColor Green
docker-compose up -d
Write-Host "✅ Services démarrés!" -ForegroundColor Green
Write-Host "📊 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🖥️  App: http://localhost:8501" -ForegroundColor Cyan
```

## ⚠️ Erreurs Communes

### Erreur 1 : Image trop volumineuse
```dockerfile
# ❌ MAUVAIS : Image complète
FROM python:3.11

# ✅ BON : Image slim
FROM python:3.11-slim

# ✅ MEILLEUR : Multi-stage build
FROM python:3.11-slim as builder
# ... installation dépendances ...
FROM python:3.11-slim
COPY --from=builder /opt/venv /opt/venv
```

### Erreur 2 : Services ne communiquent pas
```yaml
# ❌ MAUVAIS : Pas de réseau défini
services:
  api:
    ...
  app:
    ...

# ✅ BON : Réseau commun
services:
  api:
    networks:
      - diabetes-network
  app:
    networks:
      - diabetes-network
    environment:
      - API_URL=http://api:8000  # Utiliser le nom du service!
```

### Erreur 3 : App démarre avant l'API
```yaml
# ❌ MAUVAIS : Pas de dépendance
services:
  app:
    ...

# ✅ BON : depends_on avec health check
services:
  app:
    depends_on:
      api:
        condition: service_healthy
```

### Erreur 4 : Rebuild nécessaire ignoré
```bash
# ❌ MAUVAIS : docker-compose up (utilise cache)
docker-compose up

# ✅ BON : Forcer le rebuild
docker-compose up --build

# ✅ MEILLEUR : Rebuild sans cache
docker-compose build --no-cache
docker-compose up
```

### Erreur 5 : Permissions dans le conteneur
```dockerfile
# ✅ BON : Utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser
```

## 📚 Checklist de Validation

- [ ] Dockerfiles créés pour API et App
- [ ] Images se build sans erreur
- [ ] docker-compose.yml fonctionnel
- [ ] Health checks configurés
- [ ] Réseau Docker configuré
- [ ] Services communiquent entre eux
- [ ] Variables d'environnement correctes
- [ ] .dockerignore optimisé
- [ ] Images optimisées (< 500MB chacune)
- [ ] Restart policies configurées
- [ ] Documentation complète
- [ ] Scripts de démarrage testés
- [ ] Logs accessibles (`docker-compose logs`)

## 🔍 Commandes Utiles

```bash
# Voir les conteneurs en cours
docker-compose ps

# Logs en temps réel
docker-compose logs -f api
docker-compose logs -f app

# Entrer dans un conteneur
docker-compose exec api bash
docker-compose exec app bash

# Reconstruire un service spécifique
docker-compose build api

# Voir l'utilisation des ressources
docker stats

# Nettoyer les ressources Docker
docker system prune -a
```

## 🔗 Dépendances

- **ML3_API_Scoring** : Code et modèle de l'API
- **ML4_App_Scoring** : Code de l'application web

## ➡️ Suite du Projet

Les conteneurs Docker seront déployés sur le cloud dans **ML6_Deploy_Cloud**.

---

## ⚠️ Avertissement Éthique

**Ce projet est un PoC éducatif et ne constitue en aucun cas un outil médical.**  
En production, assurez-vous de respecter les normes de sécurité (HTTPS, authentification, chiffrement des données) et les réglementations médicales en vigueur.
