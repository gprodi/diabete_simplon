# Projet MLOps : Déploiement d'une API de Prédiction du Diabète

Ce projet déploie une API de scoring (backend FastAPI) et une application web de démonstration (frontend Streamlit) sur le cloud Render.

## 🔗 URLs des Services Déployés

- **Application Web (Frontend)** : `https://diabete-simplon-2.onrender.com` (remplacez par votre URL)
- **API de Scoring (Backend)** : `https://diabete-simplon-1.onrender.com` (remplacez par votre URL)
- **Endpoint Healthcheck de l'API** : `https://diabete-simplon-1.onrender.com/health` (remplacez par votre URL)

---

## ⚙️ Configuration du Déploiement

### Service 1 : API de Scoring (`diabete-api`)

-   **Fichier source** : `ML Gael/api/app.py`
-   **Dossier racine (Root Directory)** : `api`
-   **Commande de démarrage** : `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Service 2 : Application Web (`diabete-streamlit`)

-   **Fichier source** : `app_web.py`
-   **Dossier racine (Root Directory)** : 'ML Gael/'
-   **Commande de démarrage** : `streamlit run app_web.py --server.port $PORT --server.address=0.0.0.0`
-   **Variable d'environnement requise** :
    -   `API_BASE_URL` : URL complète du service API (ex: `https://diabete-simplon-1.onrender.com`)

---

## 🚀 Procédure de (Re)déploiement et Rollback

### Déploiement Continu (CI/CD)
Le déploiement est automatique. Chaque `git push` sur la branche `main` déclenche un nouveau déploiement sur Render pour le(s) service(s) dont les fichiers ont été modifiés.

### Rollback (Retour en arrière)
1.  Sur le tableau de bord Render du service à restaurer, allez dans l'onglet **Events**.
2.  Trouvez un déploiement précédent dans la liste.
3.  Cliquez sur le bouton **"Deploy"** correspondant pour relancer cette version du code.

---

## 📊 Limites du Plan Gratuit Render

-   **Mise en veille** : Les services s'endorment après 15 minutes d'inactivité. Le premier chargement après une pause peut prendre jusqu'à 30 secondes.
-   **Ressources** : CPU et RAM sont limités et partagés.
-   **Stockage non persistant** : Les fichiers créés par l'application sont effacés à chaque redéploiement.

---

## 📜 Logs d'Exécution

**Exemple de requête réussie (200 OK) sur l'API (vu dans les logs Render) :**
*(Insérez ici votre capture d'écran des logs montrant une ligne avec "200 OK")*
`Oct 21 10:45:12 AM INFO:     10.1.2.3:0 - "POST /predict HTTP/1.1" 200 OK`

**Exemple d'erreur de connexion gérée côté Streamlit :**
*(Insérez ici votre capture d'écran de l'app Streamlit montrant le message d'erreur rouge)*
`🚨 Erreur de connexion à l'API à l'adresse : https://diabete-simplon-1.onrender.com`