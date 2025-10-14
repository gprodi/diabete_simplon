# Projet Prédiction du Diabète
============================

Ce projet permet de prédire le risque de diabète à partir de données patient via une API FastAPI et une interface Gradio.

## Structure du projet
------------------
```bash
ML_Flavie/
├── api/                  # Contient le code FastAPI
│   └── api.py
├── app/                  # Contient le code Gradio
│   └── main.py
├── model/                # Contient le modèle entraîné
│   └── modele_diabete_XX.pkl
├── Dockerfile.api
├── Dockerfile.app
└── docker-compose.yml
```

## Problèmes rencontrés et solutions
---------------------------------

1. Erreur : modèle introuvable dans Docker
   FileNotFoundError: No such file or directory: 'model/modele_diabete_XX.pkl'
   - Cause : chemin incorrect dans le conteneur Docker.
   - Solution :
     - Dans main.py de l’app Gradio, utiliser le chemin absolu dans le conteneur :
       model_path = "/model/modele_diabete_XX.pkl"
       model = joblib.load(model_path)
     - Vérifier que le volume Docker mappe bien le dossier model :
       volumes:
         - ./model:/model

2. Erreur HTTP 127.0.0.1:8000 connexion refusée
   Connection refused
   - Cause : Gradio essayait d’appeler l’API avant qu’elle ne soit disponible, ou l’URL était incorrecte.
   - Solution :
     - Définir correctement la variable d’environnement API_BASE_URL dans docker-compose.yml :
       environment:
         - API_BASE_URL=http://api:8000/predict
     - Dans main.py utiliser :
       API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/predict")

3. Erreur HTTP 0.0.0.0 inaccessible dans le navigateur
   ERR_ADDRESS_INVALID
   - Cause : 0.0.0.0 est utilisé pour écouter toutes les interfaces à l’intérieur du conteneur, mais il n’est pas directement accessible depuis le navigateur.
   - Solution :
     - Toujours lancer Gradio avec :
       demo.launch(server_name="0.0.0.0", server_port=7860)
     - Accéder depuis le navigateur via http://localhost:7860/

4. Erreur variable non définie dans Gradio
   name 'age' is not defined
   - Cause : mauvais scope dans le code Gradio.
   - Solution : vérifier que tous les composants Gradio (age, gender, etc.) sont définis dans le même bloc with gr.Blocks() avant d’être utilisés dans predict_btn.click().

5. Favicon introuvable
   GET /favicon.ico 404 Not Found
   - Cause : navigateur cherche un favicon.
   - Solution : optionnel, ajouter un fichier favicon.ico dans app/ ou ignorer.

## Lancer le projet avec Docker
---------------------------

1. Construire et lancer les containers :

docker compose up --build

2. Vérifier les containers :

docker ps -a

- ml_flavie-api-1 → API FastAPI
- ml_flavie-app-1 → Gradio

3. Accéder à Gradio :

http://localhost:7860/

4. Vérifier l’API :

http://localhost:8000/

## Commandes utiles
----------------

- Arrêter les containers :

docker compose down

- Voir les logs d’un container :

docker logs -f ml_flavie-app-1
docker logs -f ml_flavie-api-1

- Rebuild et relancer :

docker compose up --build

## Résumé
------

- Docker containers isolent API et interface Gradio.
- Les volumes permettent de partager le modèle .pkl.
- Gradio écoute sur 0.0.0.0 pour Docker, mais le navigateur doit utiliser localhost.
- L’API doit être disponible avant l’interface Gradio pour éviter les erreurs de connexion.
- Message clair dans le terminal pour Gradio :
  ✅ Gradio est prêt ! Ouvrez votre navigateur sur : http://localhost:7860/
