import gradio as gr
import pandas as pd
import joblib

# === Charger le modèle ===
model = joblib.load("model/modele_diabete_XX.pkl")

# === Fonction de prédiction ===
def predict_diabete(
    age, glucose, insulin, bmi, blood_pressure,
    irritability, obesity, partial_paresis, alopecia,
    delayed_healing, weakness, polyuria, polyphagia,
    itching, sudden_weight_loss, gender, polydipsia,
    genital_thrush, visual_blurring, muscle_stiffness
):
    try:
        # Créer un DataFrame à partir des entrées
        data = pd.DataFrame([{
            "age": age,
            "glucose": glucose,
            "insulin": insulin,
            "bmi": bmi,
            "blood_pressure": blood_pressure,
            "irritability": irritability,
            "obesity": obesity,
            "partial_paresis": partial_paresis,
            "alopecia": alopecia,
            "delayed_healing": delayed_healing,
            "weakness": weakness,
            "polyuria": polyuria,
            "polyphagia": polyphagia,
            "itching": itching,
            "sudden_weight_loss": sudden_weight_loss,
            "gender": gender,
            "polydipsia": polydipsia,
            "genital_thrush": genital_thrush,
            "visual_blurring": visual_blurring,
            "muscle_stiffness": muscle_stiffness
        }])
        
        # Prédiction
        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0][1]

        decision = "Diabète détecté" if pred == 1 else "Aucun diabète détecté"
        return f"Prédiction : {pred}\nProbabilité : {proba:.3f}\nDécision : {decision}"

    except Exception as e:
        return f"Erreur : {str(e)}"

# === Interface Gradio ===
with gr.Blocks() as demo:
    gr.Markdown("## Prédiction du diabète 🩺")
    gr.Markdown("Remplissez les champs du patient pour obtenir la prédiction.")

    with gr.Row():
        with gr.Column():
            age = gr.Number(label="Âge", value=50)
            glucose = gr.Number(label="Glucose", value=120)
            insulin = gr.Number(label="Insuline", value=80)
            bmi = gr.Number(label="BMI", value=25.0)
            blood_pressure = gr.Number(label="Tension artérielle", value=80)

        with gr.Column():
            irritability = gr.Number(label="Irritabilité", value=0)
            obesity = gr.Number(label="Obésité", value=0)
            partial_paresis = gr.Number(label="Parésie partielle", value=0)
            alopecia = gr.Number(label="Alopécie", value=0)
            delayed_healing = gr.Number(label="Guérison lente", value=0)

        with gr.Column():
            weakness = gr.Number(label="Faiblesse", value=0)
            polyuria = gr.Number(label="Polyurie", value=0)
            polyphagia = gr.Number(label="Polyphagie", value=0)
            itching = gr.Number(label="Démangeaisons", value=0)
            sudden_weight_loss = gr.Number(label="Perte de poids soudaine", value=0)

        with gr.Column():
            gender = gr.Textbox(label="Genre", value="M")
            polydipsia = gr.Number(label="Polydipsie", value=0)
            genital_thrush = gr.Number(label="Candidose génitale", value=0)
            visual_blurring = gr.Number(label="Vision floue", value=0)
            muscle_stiffness = gr.Number(label="Raideur musculaire", value=0)

    predict_btn = gr.Button("Prédire")
    output = gr.Textbox(label="Résultat", interactive=False)

    predict_btn.click(
        fn=predict_diabete,
        inputs=[
            age, glucose, insulin, bmi, blood_pressure,
            irritability, obesity, partial_paresis, alopecia,
            delayed_healing, weakness, polyuria, polyphagia,
            itching, sudden_weight_loss, gender, polydipsia,
            genital_thrush, visual_blurring, muscle_stiffness
        ],
        outputs=output
    )

# === Lancer l'interface ===
demo.launch()
