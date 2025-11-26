FROM python:3.13-slim

WORKDIR /app

# Copier le code Gradio
COPY app/ /app
COPY assets/ /assets
COPY model/ /app/model/
COPY requirements.txt /app

# Installer les dépendances
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Exposer le port Gradio
EXPOSE 7860

# Lancer Gradio
CMD ["python", "main.py"]
