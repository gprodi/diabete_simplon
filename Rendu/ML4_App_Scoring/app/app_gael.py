import streamlit as st
import requests
import json
import os
import time

# --- 0. Configuration de l'environnement ---

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


# --- DEBUG: Vérifiez la variable d'environnement ---
# if not API_BASE_URL:
#     st.error("ERREUR DE CONFIGURATION: La variable API_URL n'a pas été trouvée dans le fichier .env.")
#     st.stop() # Arrête l'exécution pour que l'erreur soit visible
# else:
#     # Affiche l'URL si elle est trouvée 
#     st.sidebar.success(f"API cible : {API_BASE_URL}") 
# --- FIN DEBUG ---

# --- 1. Définition du Schéma de l'API (Contrat d'E/S) ---

# Les 15 caractéristiques binaires (Yes/No)
BINARY_FEATURES = [
    "gender", "polyuria", "polydipsia", "sudden_weight_loss", "weakness",
    "polyphagia", "genital_thrush", "visual_blurring", "itching",
    "irritability", "delayed_healing", "partial_paresis", 
    "muscle_stiffness", "alopecia", "obesity"
]

# --- 2. Fonctions d'Appel de l'API ---

def get_prediction_from_api(data: dict):
    """
    Appelle l'endpoint /predict de l'API FastAPI avec gestion des erreurs.
    """
    url = f"{API_BASE_URL}/predict"
    
    # 5 secondes de timeout (Critère "Application solide")
    TIMEOUT_SECONDS = 5 
    
    try:
        response = requests.post(
            url, 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT_SECONDS
        )
        
    # Gestion du timeout (si l'API ne répond pas dans les 5s)
    except requests.exceptions.Timeout:
        st.error("❌ Erreur: L'API a mis trop de temps à répondre (> 5s). Veuillez réessayer.")
        return None
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Erreur: Impossible de se connecter à l'API à l'adresse {API_BASE_URL}. Assurez-vous qu'elle est lancée (uvicorn app:app).")
        return None
    
    # Gestion des statuts HTTP (y compris 422 pour les erreurs de validation)
    if response.status_code == 200:
        return response.json()
    else:
        # Afficher l'erreur retournée par l'API (ex: 422 Pydantic error)
        try:
            error_data = response.json()
            st.error(f"⚠️ Erreur de l'API (Code {response.status_code}): Problème de validation des données.")
            
            # Tente d'afficher les erreurs Pydantic de manière claire
            if 'detail' in error_data and isinstance(error_data['detail'], list):
                for detail in error_data['detail']:
                    # Afficher l'emplacement et le message de l'erreur
                    loc = detail.get('loc', ['N/A', 'N/A'])
                    st.warning(f"  Champ: **{loc[-1]}** - Message: *{detail.get('msg', 'Erreur inconnue')}*")
            else:
                st.error(f"Réponse API détaillée: {error_data}")
        except json.JSONDecodeError:
            st.error(f"❌ Erreur non JSON de l'API (Code {response.status_code}).")
        
        return None


# --- 3. Interface Streamlit ---

st.set_page_config(
    page_title="🩺 Démonstration PoC : Prédiction du Diabète", 
    layout="wide", # ⭐ Utiliser l'espace entier de l'écran
    initial_sidebar_state="auto"
)
st.title("🩺 Démonstration PoC : Prédiction du Diabète")

st.markdown("""
Cette application est une preuve de concept éducative. Elle utilise une API REST 
pour prédire la probabilité de diabète à partir de 16 caractéristiques.
""")

# 🎯 Début du formulaire unique
with st.form("prediction_form"):
    st.header("Caractéristiques du Patient")
    
    # --- Champs Numériques ---
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Âge (années)", min_value=1, max_value=150, value=40)
    with col2:
        # gender est traité comme binaire mais on utilise un selectbox pour l'UX
        gender_input = st.selectbox("Sexe", options=["Male (1)", "Female (0)"])
        gender = 1 if "Male" in gender_input else 0

    st.subheader("Symptômes (Cocher si vous avez le symptome)")
    
    # --- Champs Binaires (Checkbox pour les 14 symptômes restants) ---
    input_data = {}
    
    # Ajout de l'Age et Gender au dictionnaire
    input_data['age'] = age
    input_data['gender'] = gender
    
    # Utilisation de colonnes pour les 14 symptômes
    cols = st.columns(3)
    
    for i, feature in enumerate(BINARY_FEATURES[1:]): # On commence à polyuria
        # Nettoyage pour l'affichage (ex: sudden_weight_loss -> Sudden Weight Loss)
        label = feature.replace('_', ' ').title()
        
        # Crée la checkbox dans la colonne appropriée
        input_data[feature] = cols[i % 3].checkbox(label, key=feature)
        input_data[feature] = int(input_data[feature]) # True/False -> 1/0

    # Séparateur et Bouton de Soumission
    st.markdown("---")
    
    # 🎯 On garde SEULEMENT le bouton de soumission DANS le formulaire
    submitted = st.form_submit_button("Obtenir la Prédiction")
    


# --- 4. Logique de Soumission ---

if submitted:
    st.subheader("Résultat de la Prédiction")
    
    # Appel à l'API
    with st.spinner('Communication avec l\'API de prédiction...'):
        result = get_prediction_from_api(input_data)
    
    if result:
        # Récupère la probabilité positive (valeur entre 0 et 1)
        prob_positive = result.get('probability_positive', 0)
        pred = result.get('prediction', 'N/A')
        
        # --- NOUVELLE LOGIQUE D'AFFICHAGE DE LA PROBABILITÉ ---
        if pred == "Positive":
            # Si c'est positif, on affiche la probabilité positive
            prob_display = prob_positive * 100
            pred_label = "Probabilité :"
        elif pred == "Negative":
            # Si c'est négatif, on affiche (1 - probabilité positive)
            prob_display = (1 - prob_positive) * 100
            pred_label = "Probabilité :"
        else:
            # Cas par défaut ou erreur
            prob_display = prob_positive * 100
            pred_label = "Probabilité (Information non complète)"
        
        st.metric(pred_label, f"{prob_display:.2f}%")
        # --- FIN NOUVELLE LOGIQUE ---

        
        # 🎯 Logique de couleur conditionnelle
        if pred == "Positive":
            # 🟥 Cadre ROUGE pour un résultat Positif (risque élevé)
            st.error(f"⚠️ Prédiction de l'API : **{pred}**")
            st.warning("Risque élevé détecté (Note : Ceci est une démonstration éducative).")
            
        elif pred == "Negative":
            # 🟩 Cadre VERT pour un résultat Négatif (risque faible)
            st.success(f"✅ Prédiction de l'API : **{pred}**")
            st.balloons() 
            st.info("Risque faible détecté (Note : Ceci est une démonstration éducative).")
            
        else:
             # Cas par défaut si la prédiction n'est pas celle attendue (sécurité)
             st.info(f"Prédiction de l'API : **{pred}**")
