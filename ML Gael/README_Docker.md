Projet MLOps : Démo de Prédiction de Diabète (API + Streamlit)Ce projet utilise Docker et Docker Compose pour lancer l'API d'inférence (FastAPI) et l'application de démonstration (Streamlit) en une seule commande.1. PrérequisAssurez-vous d'avoir installé les outils suivants sur votre machine :DockerDocker Compose2. Structure des Fichiers.
├── api/                  # Code et dépendances du service FastAPI
├── .env                  # Configuration (URL et ports)
├── docker-compose.yml    # Fichier d'orchestration
├── Dockerfile.api        # Dockerfile pour le service API
├── Dockerfile.app        # Dockerfile pour l'application Streamlit
├── README.md
├── app_web.py            # Code de l'application Streamlit
└── requirements.txt      # Dépendances de l'application Streamlit
3. Commandes Principales3.1. Construction des ImagesSi c'est le premier lancement ou si vous avez modifié un Dockerfile :docker compose build
3.2. Lancement du ProjetCette commande démarre les deux services (api et app) et les connecte :docker compose up
# ou pour lancer en arrière-plan :
# docker compose up -d
3.3. Arrêt des ServicesPour arrêter et nettoyer les conteneurs et le réseau :docker compose down
4. AccèsUne fois que docker compose up a démarré les deux services (cela peut prendre quelques secondes), vous pouvez y accéder via les liens suivants :ServiceAdresse LocaleApplication Streamlithttp://localhost:8501API FastAPI (Endpoint)http://localhost:8000/predictVérification de Santé APIhttp://localhost:8000/health5. Démonstration et ÉvaluationPour la démo de 3 minutes, vous pouvez montrer :Cas de Succès : Accéder à l'application web, remplir les champs, cliquer sur "Obtenir la Prédiction" et vérifier que l'API renvoie un résultat (200 OK).Cas d'Erreur API : L'API FastAPI utilise Pydantic pour valider les données. Modifiez le fichier api/app.py pour simuler une erreur, ou tentez d'envoyer manuellement à http://localhost:8000/predict un JSON avec un champ manquant ou invalide (ex: "age": 200 ou "age": "abc"). FastAPI renverra automatiquement un code 422 Unprocessable Entity.Logs : Afficher les logs des deux conteneurs via docker compose logs et montrer que l'API reçoit la requête de l'application.