# Base Python
FROM python:3.13-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier le code de l'application
COPY ./app /app

# Installer les dépendances
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Lancer main.py et rester actif après son exécution
CMD ["bash", "-c", "python main.py && tail -f /dev/null"]
