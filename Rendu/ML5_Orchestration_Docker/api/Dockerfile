# Utiliser une image légère Python
FROM python:3.13-slim

# Définir le dossier de travail
WORKDIR /app

# Copier le code API et le modèle
COPY api/ .   
COPY assets/ . 
COPY model/ ./model/    
COPY model/ /app/model/  
COPY app/ /app
COPY assets/ /assets       
COPY requirements.txt .     

# Installer les dépendances
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Exposer le port FastAPI
EXPOSE 8000

# Lancer FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
