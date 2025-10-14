import gradio as gr
import requests


# === URL de l'API ===
API_URL = "http://127.0.0.1:8000/predict"

# === Fonction de prédiction via API ===
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
        response = requests.post(API_URL, json=data, timeout=5)
        response.raise_for_status()
        result = response.json()

        pred = result.get("prediction", 0)
        proba = result.get("probability", 0) * 100
        pred_text = "Positif" if pred == 1 else "Négatif"
        color = "#e74c3c" if pred == 1 else "#27ae60"
        decision = "⚠️ Diabète détecté" if pred == 1 else "✅ Aucun diabète détecté"

        return f"""
        <div style='padding:20px; text-align:center; border-radius:15px; background:#fff; 
                    box-shadow:0 5px 20px rgba(0,0,0,0.1);'>
            <h2>Résultat: {pred_text}</h2>
            <p>Probabilité: {proba:.2f}%</p>
            <p style='color:{color}; font-weight:bold;'>{decision}</p>
        </div>
        """
    except Exception as e:
        return f"<div style='color:red; font-weight:bold;'>❌ Erreur : {e}</div>"

# === Interface Gradio ===
with gr.Blocks(css="""
body { background: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
.gr-button { background-color:#0078D7 !important; color:white !important; border-radius:12px !important; font-weight:bold !important; }
.gr-button:hover { background-color:#005fa3 !important; }
.gr-slider, .gr-radio, .gr-checkbox { margin-bottom:8px !important; }
""") as demo:

    gr.HTML("<h1 style='text-align:center; color:#0078D7;'>🩺 Prédiction du Diabète</h1>")

    with gr.Row():
        # ===== Informations Patient =====
        with gr.Column():
            gr.HTML("<h3>Informations Patient</h3>")
            age = gr.Slider(label="Âge", minimum=0, maximum=120, value=45)
            gender = gr.Radio(label="Genre", choices=["Homme", "Femme"], value="Homme")
            gr.Image("assets/Traitements_du_diabète.jpg", type="filepath", label="Illustration Patient")  

        # ===== Symptômes =====
        with gr.Column():
            gr.HTML("<h3>Symptômes</h3>")
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
demo.launch()
