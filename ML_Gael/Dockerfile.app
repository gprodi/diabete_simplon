# Utilise une image Python légère
FROM python:3.11-slim

# Empêche Python de créer des fichiers .pyc et met la sortie en temps réel
ENV PYTHONUNBUFFERED=1

# Définit le répertoire de travail
WORKDIR /app

# Copie le fichier de dépendances Streamlit et installe-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie l'application Streamlit
COPY app_web.py .
COPY .env .

# Le port 8501 est le port par défaut de Streamlit
EXPOSE 8501

# Commande de démarrage: lance l'application Streamlit
CMD ["streamlit", "run", "app_web.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
