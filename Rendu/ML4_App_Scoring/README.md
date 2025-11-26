# ML4 - Application Web de Scoring

## 📋 Contexte du Brief

Ce brief consiste à créer une application web conviviale permettant aux utilisateurs de saisir les données d'un patient et d'obtenir une prédiction de risque de diabète en temps réel via l'API développée en ML3.

## 🎯 Objectifs

- Créer une interface web interactive avec Streamlit ou Gradio
- Connecter l'application à l'API de prédiction
- Implémenter un formulaire de saisie avec validation
- Afficher les résultats de manière claire et visuelle
- Gérer les erreurs de connexion API
- Ajouter des visualisations (jauge de probabilité, graphiques)
- Rendre l'application responsive
- Documenter l'utilisation pour l'utilisateur final

## 📦 Livrables Attendus

| Livrable | Description | Emplacement |
|----------|-------------|-------------|
| Application Streamlit | Code de l'interface web | `app/main.py` |
| Configuration | Variables d'environnement | `app/.env` et `app/config.py` |
| Styles CSS (optionnel) | Personnalisation visuelle | `app/styles.css` |
| Assets | Images, logos, icônes | `app/assets/` |
| Requirements | Dépendances Python | `app/requirements.txt` |
| Documentation utilisateur | Guide d'utilisation | `docs/user_guide.md` |
| Screenshots | Captures d'écran de l'app | `docs/screenshots/` |

## ✅ Critères d'Évaluation

- **Ergonomie** : Interface intuitive et claire
- **Fonctionnalité** : Tous les champs fonctionnels, prédictions correctes
- **Gestion d'erreurs** : Messages clairs en cas de problème
- **Design** : Interface agréable et professionnelle
- **Validation** : Vérification des données saisies
- **Visualisation** : Affichage clair des résultats (probabilité, recommandations)
- **Responsiveness** : Adaptation mobile/desktop
- **Documentation** : Guide utilisateur complet

## 🛠️ Technologies Recommandées

```python
# Interface Web
streamlit >= 1.28.0
# OU
gradio >= 4.0.0

# Communication API
requests >= 2.31.0
httpx >= 0.25.0

# Visualisation
plotly >= 5.17.0
matplotlib >= 3.8.0

# Utilities
python-dotenv >= 1.0.0
```

## 📊 Entrées / Sorties

| Type | Description | Format | Source |
|------|-------------|--------|--------|
| **Entrée** | Saisie utilisateur (formulaire) | Interface Web | Utilisateur |
| **Sortie** | Requête vers API | JSON | ML3 - `/predict` |
| **Entrée** | Réponse API | JSON | ML3 - `/predict` |
| **Sortie** | Résultat affiché | Interface Web | Utilisateur |

## 🚀 Comment Lancer

### 1. Installation des dépendances

```bash
cd ML4_App_Scoring/app
pip install -r requirements.txt
```

### 2. Structure minimale du projet

```
ML4_App_Scoring/
├── app/
│   ├── main.py              # Application Streamlit
│   ├── config.py            # Configuration
│   ├── requirements.txt
│   ├── .env                 # Variables d'environnement
│   └── assets/
│       └── logo.png
├── docs/
│   ├── user_guide.md
│   └── screenshots/
│       ├── home.png
│       └── result.png
└── README.md
```

### 3. Exemple minimal avec Streamlit

**`app/main.py`**
```python
import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Diabète",
    page_icon="🏥",
    layout="wide"
)

# Configuration API
API_URL = "http://localhost:8000/predict"

# Titre et description
st.title("🏥 Système de Prédiction du Risque de Diabète")
st.markdown("""
Cette application utilise un modèle de machine learning pour évaluer le risque de diabète.
**⚠️ PoC éducatif uniquement - Ne remplace pas un diagnostic médical.**
""")

# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ Informations")
    st.info("""
    Cette application analyse 8 paramètres médicaux pour prédire 
    le risque de diabète avec un niveau de confiance.
    """)
    st.warning("⚠️ Cet outil est uniquement éducatif et ne doit pas être utilisé pour un diagnostic réel.")

# Formulaire de saisie
st.header("📝 Saisie des Données Patient")

col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input(
        "Nombre de grossesses",
        min_value=0,
        max_value=20,
        value=1,
        help="Nombre total de grossesses"
    )
    
    glucose = st.number_input(
        "Taux de glucose (mg/dL)",
        min_value=1.0,
        max_value=250.0,
        value=120.0,
        help="Concentration de glucose plasmatique à 2h dans un test de tolérance au glucose"
    )
    
    blood_pressure = st.number_input(
        "Pression artérielle (mm Hg)",
        min_value=0.0,
        max_value=200.0,
        value=70.0,
        help="Pression artérielle diastolique"
    )
    
    skin_thickness = st.number_input(
        "Épaisseur de peau (mm)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        help="Épaisseur du pli cutané du triceps"
    )

with col2:
    insulin = st.number_input(
        "Niveau d'insuline (μU/ml)",
        min_value=0.0,
        max_value=900.0,
        value=80.0,
        help="Insuline sérique à 2h"
    )
    
    bmi = st.number_input(
        "IMC (Indice de Masse Corporelle)",
        min_value=1.0,
        max_value=70.0,
        value=25.5,
        help="Poids en kg / (taille en m)²"
    )
    
    dpf = st.number_input(
        "Fonction de pedigree du diabète",
        min_value=0.0,
        max_value=3.0,
        value=0.5,
        step=0.01,
        help="Fonction qui représente l'historique familial de diabète"
    )
    
    age = st.number_input(
        "Âge (années)",
        min_value=1,
        max_value=120,
        value=33,
        help="Âge du patient en années"
    )

# Bouton de prédiction
if st.button("🔍 Effectuer la Prédiction", type="primary", use_container_width=True):
    # Préparation des données
    patient_data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age
    }
    
    # Appel API
    try:
        with st.spinner("Analyse en cours..."):
            response = requests.post(API_URL, json=patient_data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                
                # Affichage des résultats
                st.success("✅ Prédiction effectuée avec succès!")
                
                # Création de colonnes pour l'affichage
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Prédiction",
                        result["prediction_label"],
                        delta=None
                    )
                
                with col2:
                    probability_pct = result["probability"] * 100
                    st.metric(
                        "Probabilité",
                        f"{probability_pct:.1f}%",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        "Niveau de Confiance",
                        result["confidence"].capitalize(),
                        delta=None
                    )
                
                # Jauge de probabilité avec Plotly
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability_pct,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Probabilité de Diabète"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkred" if result["prediction"] == 1 else "green"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgreen"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "lightcoral"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 50
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommandations
                st.subheader("📋 Interprétation")
                if result["prediction"] == 1:
                    st.error("""
                    ⚠️ **Risque de diabète détecté**
                    
                    Le modèle suggère un risque élevé. Il est recommandé de :
                    - Consulter un professionnel de santé
                    - Effectuer des tests médicaux complets
                    - Surveiller régulièrement la glycémie
                    """)
                else:
                    st.success("""
                    ✅ **Risque faible de diabète**
                    
                    Le modèle ne détecte pas de risque immédiat. Néanmoins :
                    - Maintenez un mode de vie sain
                    - Effectuez des bilans de santé réguliers
                    - Surveillez votre poids et votre alimentation
                    """)
                
                # Détails techniques
                with st.expander("🔬 Détails Techniques"):
                    st.json(result)
                    
            else:
                st.error(f"❌ Erreur API: {response.status_code}")
                st.json(response.json())
                
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de se connecter à l'API. Vérifiez qu'elle est démarrée.")
    except requests.exceptions.Timeout:
        st.error("❌ Timeout: L'API met trop de temps à répondre.")
    except Exception as e:
        st.error(f"❌ Erreur inattendue: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Développé pour le projet ML Diabète | Version 1.0.0</p>
    <p><small>⚠️ Outil éducatif uniquement - Ne remplace pas un avis médical professionnel</small></p>
</div>
""", unsafe_allow_html=True)
```

**`app/requirements.txt`**
```txt
streamlit==1.29.0
requests==2.31.0
plotly==5.18.0
python-dotenv==1.0.0
```

**`app/.env`**
```bash
API_URL=http://localhost:8000
```

### 4. Lancement de l'application

```bash
cd app
streamlit run main.py
```

L'application sera accessible sur `http://localhost:8501`

### 5. Alternative avec Gradio

```python
# app/gradio_app.py
import gradio as gr
import requests

def predict_diabetes(pregnancies, glucose, bp, skin, insulin, bmi, dpf, age):
    """Effectue une prédiction via l'API."""
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={
                "Pregnancies": int(pregnancies),
                "Glucose": float(glucose),
                "BloodPressure": float(bp),
                "SkinThickness": float(skin),
                "Insulin": float(insulin),
                "BMI": float(bmi),
                "DiabetesPedigreeFunction": float(dpf),
                "Age": int(age)
            },
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            return (
                result["prediction_label"],
                f"{result['probability'] * 100:.1f}%",
                result["confidence"]
            )
    except Exception as e:
        return "Erreur", str(e), ""

# Interface Gradio
with gr.Blocks(title="Prédiction Diabète") as app:
    gr.Markdown("# 🏥 Système de Prédiction du Risque de Diabète")
    gr.Markdown("⚠️ **PoC éducatif uniquement**")
    
    with gr.Row():
        with gr.Column():
            pregnancies = gr.Number(label="Grossesses", value=1)
            glucose = gr.Number(label="Glucose (mg/dL)", value=120)
            bp = gr.Number(label="Pression Artérielle (mm Hg)", value=70)
            skin = gr.Number(label="Épaisseur Peau (mm)", value=20)
        
        with gr.Column():
            insulin = gr.Number(label="Insuline (μU/ml)", value=80)
            bmi = gr.Number(label="IMC", value=25.5)
            dpf = gr.Number(label="Fonction Pedigree", value=0.5)
            age = gr.Number(label="Âge", value=33)
    
    predict_btn = gr.Button("Prédire", variant="primary")
    
    with gr.Row():
        prediction_output = gr.Textbox(label="Prédiction")
        probability_output = gr.Textbox(label="Probabilité")
        confidence_output = gr.Textbox(label="Confiance")
    
    predict_btn.click(
        fn=predict_diabetes,
        inputs=[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age],
        outputs=[prediction_output, probability_output, confidence_output]
    )

app.launch(server_name="0.0.0.0", server_port=7860)
```

## ⚠️ Erreurs Communes

### Erreur 1 : API non accessible
```python
# ✅ BON : Gérer les erreurs de connexion
try:
    response = requests.post(API_URL, json=data, timeout=5)
except requests.exceptions.ConnectionError:
    st.error("❌ API non accessible. Démarrez-la avec: uvicorn main:app")
```

### Erreur 2 : Pas de validation côté client
```python
# ✅ BON : Utiliser les paramètres Streamlit
glucose = st.number_input(
    "Glucose",
    min_value=1.0,   # Validation minimale
    max_value=250.0, # Validation maximale
    value=120.0      # Valeur par défaut
)
```

### Erreur 3 : Mauvais format de données envoyées
```python
# ✅ BON : S'assurer des types corrects
patient_data = {
    "Pregnancies": int(pregnancies),  # Pas float!
    "Glucose": float(glucose),
    "Age": int(age)
}
```

### Erreur 4 : Pas de feedback utilisateur
```python
# ✅ BON : Utiliser spinners et messages
with st.spinner("Analyse en cours..."):
    response = requests.post(API_URL, json=data)
    
if response.status_code == 200:
    st.success("✅ Prédiction effectuée!")
```

## 📚 Checklist de Validation

- [ ] Formulaire avec tous les champs requis
- [ ] Validation des inputs (min/max)
- [ ] Connexion API fonctionnelle
- [ ] Gestion des erreurs réseau
- [ ] Affichage clair des résultats
- [ ] Visualisations pertinentes (jauge, graphiques)
- [ ] Messages d'avertissement éthique
- [ ] Interface responsive
- [ ] Guide utilisateur rédigé
- [ ] Screenshots documentés
- [ ] Application testée sur différents navigateurs

## 🔗 Dépendances

- **ML3_API_Scoring** : L'application consomme l'API `/predict`

## ➡️ Suite du Projet

L'application sera conteneurisée avec l'API dans **ML5_Orchestration_Docker**.

---

## ⚠️ Avertissement Éthique

**Ce projet est un PoC éducatif et ne constitue en aucun cas un outil médical.**  
L'application ne doit jamais être utilisée pour un diagnostic médical réel. Toujours afficher clairement l'avertissement à l'utilisateur.
