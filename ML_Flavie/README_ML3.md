## 🖥️ ML3 – Interface Utilisateur Gradio pour la Prédiction du Diabète

Cette partie du projet fournit une interface interactive et moderne pour utiliser le modèle de prédiction de diabète créé en ML2.

---

## 🎯 Objectif
Permettre à un utilisateur non technique de :
- Entrer les informations cliniques d’un patient.
- Obtenir une prédiction claire et stylée du risque de diabète.
- Voir le résultat directement sous forme **positive** ou **négative**.

---

## 🛠 Fonctionnalités principales

1. **Formulaire regroupé** pour toutes les variables pertinentes :
   - `age`, `gender`, `polyuria`, `polydipsia`, `sudden_weight_loss`, `weakness`
   - `polyphagia`, `genital_thrush`, `visual_blurring`, `itching`, `irritability`
   - `delayed_healing`, `partial_paresis`, `muscle_stiffness`, `alopecia`, `obesity`

2. **Validation des données** :
   - Âge : 0 à 120 ans
   - Symptômes : valeurs réalistes (par ex., 0 à 5)
   - Conversion automatique du genre (`Homme` → 1, `Femme` → 0)
   - Messages d’erreur stylés en cas de valeurs invalides

3. **Résultat stylé et interactif** :
   - Carte animée avec **ombre et effet zoom au survol**
   - Couleur dynamique selon le résultat :
     - 🔴 Diabète détecté
     - 🟢 Aucun diabète détecté
   - Probabilité affichée avec précision

4. **Interface moderne et responsive** :
   - Fond dégradé élégant
   - Boutons animés et survols interactifs
   - Typographie claire et uniforme (`Segoe UI`)

---

## 💻 Lancer l’interface

1. Assurez-vous que le modèle ML2 est enregistré sous `model/modele_diabete_XX.pkl`.
2. Installez les dépendances :
```bash
pip install gradio pandas joblib scikit-learn
```
Exécutez l’application :

```bash
python gradio_app.py
```
Ouvrez l’URL fournie par Gradio (ex. http://127.0.0.1:7860) dans votre navigateur.

## ⚡ Notes techniques
- Toute erreur de saisie sera affichée clairement avec un message rouge.
- Le formulaire est conçu pour être simple et rapide à remplir, même sur mobile.
- Les prédictions sont immédiates et affichées dans une carte animée.

## 🌟 Améliorations futures
- Affichage d’un graphique dynamique de probabilité.
- Historique des prédictions enregistrées.
- Thèmes personnalisables (clair/sombre).
- Export des résultats en PDF ou CSV pour le suivi patient.