# 4. Lancement de l'Application Web (Streamlit)

Cette application web est le client de démonstration pour l'API du Brief 3.

### Prérequis

1.  **L'API doit être lancée :** Dans un premier terminal, exécutez `uvicorn app:app --reload`.
2.  **Configuration :** Le fichier `.env` doit contenir la bonne adresse (ex: `API_URL=http://127.0.0.1:8000`).

### Commandes de Lancement

1.  Assurez-vous d'avoir installé les dépendances (`pip install -r requirements.txt`).
2.  Lancez l'application Streamlit dans un **deuxième terminal** (après avoir activé le même environnement virtuel) :

```bash
streamlit run app_web.py