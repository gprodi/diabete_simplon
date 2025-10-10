import gradio as gr
import pandas as pd
import joblib

# === Charger le modèle ===
model = joblib.load("model/modele_diabete_XX.pkl")

# === Fonction de prédiction ===
def predict_diabete(
    age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, polyphagia,
    genital_thrush, visual_blurring, itching, irritability, delayed_healing,
    partial_paresis, muscle_stiffness, alopecia, obesity
):
    try:
        # --- Validation simple ---
        if age <= 0 or age > 120:
            return "<div style='color:red; font-weight:bold;'>❌ Age invalide</div>"
        for field_name, value in zip(
            ["polyuria","polydipsia","sudden_weight_loss","weakness","polyphagia",
             "genital_thrush","visual_blurring","itching","irritability",
             "delayed_healing","partial_paresis","muscle_stiffness","alopecia","obesity"],
            [polyuria, polydipsia, sudden_weight_loss, weakness, polyphagia,
             genital_thrush, visual_blurring, itching, irritability,
             delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity]
        ):
            if value < 0 or value > 10:
                return f"<div style='color:red; font-weight:bold;'>❌ Valeur impossible pour {field_name}</div>"

        # --- Conversion du genre ---
        gender_val = 1 if gender == "Homme" else 0

        # --- Créer DataFrame ---
        data = pd.DataFrame([{
            "age": age,
            "gender": gender_val,
            "polyuria": polyuria,
            "polydipsia": polydipsia,
            "sudden_weight_loss": sudden_weight_loss,
            "weakness": weakness,
            "polyphagia": polyphagia,
            "genital_thrush": genital_thrush,
            "visual_blurring": visual_blurring,
            "itching": itching,
            "irritability": irritability,
            "delayed_healing": delayed_healing,
            "partial_paresis": partial_paresis,
            "muscle_stiffness": muscle_stiffness,
            "alopecia": alopecia,
            "obesity": obesity
        }])

        # --- Prédiction ---
        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0][1] * 100

        pred_text = "Positif" if pred == 1 else "Négatif"
        color = "#e74c3c" if pred == 1 else "#27ae60"
        decision = "⚠️ Diabète détecté" if pred == 1 else "✅ Aucun diabète détecté"

        # --- Résultat stylé ---
        result_html = f"""
        <div style='
            background-color: #ffffff;
            border-radius: 20px;
            padding: 35px;
            max-width: 500px;
            margin: 20px auto;
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            text-align: center;
            font-family: "Segoe UI", sans-serif;
            transition: transform 0.4s, box-shadow 0.4s;
        ' onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 25px 50px rgba(0,0,0,0.2)';"
          onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 15px 35px rgba(0,0,0,0.15)';">
            <h2 style='color: #333; margin-bottom:20px;'>Résultat de la prédiction</h2>
            <p style='font-size:18px; color:#333; margin:6px 0;'>👤 <b>Prédiction :</b> {pred_text}</p>
            <p style='font-size:18px; color:#333; margin:6px 0;'>📊 <b>Probabilité :</b> {proba:.2f}%</p>
            <p style='font-size:20px; color:{color}; font-weight:bold; margin-top:15px;'>{decision}</p>
        </div>
        """
        return result_html

    except Exception as e:
        return f"<div style='color:red; font-weight:bold;'>❌ Erreur : {str(e)}</div>"

# === Interface Gradio moderne et animée ===
with gr.Blocks(css="""
body {
    background: linear-gradient(135deg, #e0f7fa, #fce4ec);
    font-family: 'Segoe UI', sans-serif;
}
.gr-button {
    background-color: #0078D7 !important;
    color: white !important;
    border-radius: 16px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    padding: 12px 28px !important;
    transition: transform 0.3s, background-color 0.3s !important;
}
.gr-button:hover {
    background-color: #005fa3 !important;
    transform: scale(1.08);
}
.gr-number, .gr-radio {
    border-radius: 14px !important;
    border: 1px solid #ccc !important;
    background-color: white !important;
    padding: 8px !important;
    margin-bottom: 12px !important;
    transition: transform 0.2s, box-shadow 0.2s;
}
.gr-number:hover, .gr-radio:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
h1, h2, h3, p {
    color: #000 !important;
}
""") as demo:

    # Header animé
    gr.HTML("""
    <div style='text-align:center; margin-bottom:30px;'>
        <h1 style='font-size:2.8em; color:#0078D7; transition: transform 0.5s;' 
            onmouseover="this.style.transform='scale(1.05)';" 
            onmouseout="this.style.transform='scale(1)';">
            🩺 Prédiction du Diabète
        </h1>
        <p style='font-size:1.3em; color:#333;'>Remplissez les informations du patient pour obtenir une prédiction rapide et stylée.</p>
    </div>
    """)

    # Formulaire vertical complet
    age = gr.Number(label="Âge", value=45)
    gender = gr.Radio(label="Genre", choices=["Homme", "Femme"], value="Homme")
    polyuria = gr.Number(label="Polyurie", value=0)
    polydipsia = gr.Number(label="Polydipsie", value=0)
    sudden_weight_loss = gr.Number(label="Perte de poids soudaine", value=0)
    weakness = gr.Number(label="Faiblesse", value=0)
    polyphagia = gr.Number(label="Polyphagie", value=0)
    genital_thrush = gr.Number(label="Candidose génitale", value=0)
    visual_blurring = gr.Number(label="Vision floue", value=0)
    itching = gr.Number(label="Démangeaisons", value=0)
    irritability = gr.Number(label="Irritabilité", value=0)
    delayed_healing = gr.Number(label="Guérison lente", value=0)
    partial_paresis = gr.Number(label="Parésie partielle", value=0)
    muscle_stiffness = gr.Number(label="Raideur musculaire", value=0)
    alopecia = gr.Number(label="Alopécie", value=0)
    obesity = gr.Number(label="Obésité", value=0)

    # Bouton et sortie
    predict_btn = gr.Button("🔍 Lancer la Prédiction")
    output = gr.HTML(label="Résultat")

    predict_btn.click(
        fn=predict_diabete,
        inputs=[
            age, gender, polyuria, polydipsia, sudden_weight_loss, weakness,
            polyphagia, genital_thrush, visual_blurring, itching, irritability,
            delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity
        ],
        outputs=output
    )

# Lancer l'interface
demo.launch()
