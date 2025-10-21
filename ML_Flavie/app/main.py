import gradio as gr
import requests
import joblib
import os

# Chargement du modèle
model_path = "./model/modele_diabete_XX.pkl"
model = joblib.load(model_path)

# ---------------------------
# 1️⃣ Récupération de l'URL de l'API depuis Render
# ---------------------------
API_BASE_URL = os.environ.get("API_BASE_URL")  # Exemple : "https://ml-flavie-api.onrender.com"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"
# Récupère l'URL de l'API depuis la variable d'environnement
# API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000/predict")

def predict(input_data):
    try:
        response = requests.post(API_BASE_URL, json={"data": input_data})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Erreur API : {e}"

def predict_diabete_api(age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, polyphagia,
                        genital_thrush, visual_blurring, itching, irritability, delayed_healing,
                        partial_paresis, muscle_stiffness, alopecia, obesity):
    try:
        gender_val = 1 if gender == "Homme" else 0
        data = {
            "age": age,
            "gender": gender_val,
            "polyuria": int(polyuria),
            "polydipsia": int(polydipsia),
            "sudden_weight_loss": int(sudden_weight_loss),
            "weakness": int(weakness),
            "polyphagia": int(polyphagia),
            "genital_thrush": int(genital_thrush),
            "visual_blurring": int(visual_blurring),
            "itching": int(itching),
            "irritability": int(irritability),
            "delayed_healing": int(delayed_healing),
            "partial_paresis": int(partial_paresis),
            "muscle_stiffness": int(muscle_stiffness),
            "alopecia": int(alopecia),
            "obesity": int(obesity)
        }
        response = requests.post(API_BASE_URL, json=data, timeout=5)
        response.raise_for_status()
        result = response.json()

        pred = result.get("prediction", 0)
        proba = result.get("probability", 0) * 100
        pred_text = "Positif" if pred == 1 else "Négatif"
        color = "#e74c3c" if pred == 1 else "#27ae60"
        decision = "⚠️ Diabète détecté" if pred == 1 else "✅ Aucun diabète détecté"

        return f"""
        <div style='padding:20px; text-align:center; border-radius:15px; 
                    background:#fff; box-shadow:0 5px 20px rgba(0,0,0,0.1);'>
            <h2>Résultat: {pred_text}</h2>
            <p>Probabilité: {proba:.2f}%</p>
            <p style='color:{color}; font-weight:bold;'>{decision}</p>
        </div>
        """
    except Exception as e:
        return f"<div style='color:red; font-weight:bold;'>❌ Erreur : {e}</div>"

# ==== Interface Gradio ====
with gr.Blocks(css="""
    body { background: #f5f5f5; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #ff6600; }
    .gr-button { background-color: #ff6600 !important; color:white !important; border-radius:12px !important; }
""") as demo:

    # Header stylé
    gr.HTML("""
<div style="
    text-align:center;
    margin-bottom:30px;
    padding:20px;
    background: linear-gradient(90deg, #ff9900, #ffcc66);
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    transition: transform 0.3s;
">
    <h1 style="
        font-size:3em;
        color:white;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin:0;
    ">
        🩺 Prédiction du Diabète
    </h1>
    <p style="
        font-size:1.2em;
        color:white;
        margin-top:10px;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.2);
    ">
        Remplissez les informations pour obtenir une prédiction rapide et stylée
    </p>
</div>
""")

    # Formulaire en deux colonnes
    with gr.Row():
        # --- Informations Patient ---
        with gr.Column():
            gr.HTML("""
            <div style='
                padding:15px;
                border-radius:15px;
                background:#fff3e0;
                box-shadow:0 5px 15px rgba(0,0,0,0.1);
                margin-bottom:15px;
                text-align:center;
            '>
                <h3 style='color:#ff6600;'>Informations Patient</h3>
            </div>
            """)
            age = gr.Slider(label="Âge", minimum=0, maximum=120, value=45, step=1)
            gender = gr.Radio(label="Genre", choices=["Homme", "Femme"], value="Homme")
            gr.Image("../assets/Traitements_du_diabète.jpg", type="filepath", label="Illustration Patient")

        # --- Symptômes ---
        with gr.Column():
            gr.HTML("""
            <div style='
                padding:15px;
                border-radius:15px;
                background:#fff8e1;
                box-shadow:0 5px 15px rgba(0,0,0,0.1);
                margin-bottom:15px;
                text-align:center;
            '>
                <h3 style='color:#ff9900;'>Symptômes</h3>
            </div>
            """)
            polyuria = gr.Checkbox(label="Polyurie", value=False)
            polydipsia = gr.Checkbox(label="Polydipsie", value=False)
            sudden_weight_loss = gr.Checkbox(label="Perte de poids soudaine", value=False)
            weakness = gr.Checkbox(label="Faiblesse", value=False)
            polyphagia = gr.Checkbox(label="Polyphagie", value=False)
            genital_thrush = gr.Checkbox(label="Candidose génitale", value=False)
            visual_blurring = gr.Checkbox(label="Vision floue", value=False)
            itching = gr.Checkbox(label="Démangeaisons", value=False)
            irritability = gr.Checkbox(label="Irritabilité", value=False)
            delayed_healing = gr.Checkbox(label="Guérison lente", value=False)
            partial_paresis = gr.Checkbox(label="Parésie partielle", value=False)
            muscle_stiffness = gr.Checkbox(label="Raideur musculaire", value=False)
            alopecia = gr.Checkbox(label="Alopécie", value=False)
            obesity = gr.Checkbox(label="Obésité", value=False)

    # Bouton et sortie
    predict_btn = gr.Button("🔍 Lancer la Prédiction")
    output = gr.HTML()

    predict_btn.click(
        fn=predict_diabete_api,
        inputs=[age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, polyphagia,
                genital_thrush, visual_blurring, itching, irritability, delayed_healing,
                partial_paresis, muscle_stiffness, alopecia, obesity],
        outputs=output
    )

# Lancer l’interface
demo.launch(server_name="0.0.0.0", server_port=7860)
