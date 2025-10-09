# README – ML1 : Extraction et préparation d’un dataset sur le diabète

## 📌 Contexte du projet
Ce projet fait partie du TP **“ML 1 - Extraction et préparation d’un dataset sur le diabète”**.  
L’objectif est de **nettoyer et préparer un dataset réel** afin de pouvoir créer, par la suite, un modèle de prédiction du risque de diabète.  

Le projet est réalisé en **groupe**, en utilisant **Python** et la bibliothèque **pandas**.

---

## 📂 Contenu du projet
| Fichier | Description |
|---------|-------------|
| `eda_<initiales>_diabetes.ipynb` | Notebook contenant toutes les étapes d’import, d’exploration, de nettoyage et de visualisation des données. |
| `diabetes_clean.csv` | Dataset final nettoyé et prêt à être utilisé pour un modèle prédictif. |

---

## 🧰 Bibliothèques utilisées et justification

| Bibliothèque | Rôle principal | Pourquoi elle est utilisée |
|---------------|----------------|-----------------------------|
| **pandas** | Manipulation et nettoyage de données | Permet de lire, explorer, transformer et nettoyer facilement les fichiers CSV. |
| **numpy** | Calculs numériques et gestion des tableaux | Utile pour les opérations mathématiques et statistiques sur les données. |
| **matplotlib** | Visualisation simple de données | Création de graphiques basiques comme histogrammes, courbes ou nuages de points. |
| **seaborn** | Visualisation statistique avancée | Permet de créer des graphiques esthétiques et informatifs (heatmaps, countplots, boxplots). |

---

## 🪜 Étapes réalisées dans le projet

1. **Import des bibliothèques**  
   Pour pouvoir manipuler, nettoyer et visualiser les données efficacement.

2. **Importation du dataset**  
   Lecture du fichier CSV téléchargé depuis le site UCI.

3. **Exploration initiale (EDA)**  
   - Analyse de la structure du dataset (`info`, `shape`, `dtypes`)  
   - Statistiques descriptives (`describe`)  
   - Détection des valeurs manquantes et doublons

4. **Nettoyage de la donnée**  
   - Suppression des doublons  
   - Conversion des types de données  
   - Remplacement des valeurs textuelles (“Yes” / “No”) par des valeurs numériques (1 / 0)  
   - Gestion des valeurs manquantes

5. **Visualisation des données**  
   - Distribution de la variable cible  
   - Distribution des variables clés comme l’âge  
   - Analyse des corrélations entre variables

6. **Sauvegarde du dataset nettoyé**  
   Le dataset propre est exporté sous le nom `diabetes_clean.csv` pour réutilisation future.

7. **Vérifications finales**  
   - Notebook fonctionnel  
   - Données nettoyées et cohérentes  
   - Dataset prêt pour la modélisation

---

## 🔗 Ressources utilisées
- [Exploratory Data Analysis in Python — GeeksForGeeks](https://www.geeksforgeeks.org/data-analysis/exploratory-data-analysis-in-python/)  
- [Data Wrangling in Python — GeeksForGeeks](https://www.geeksforgeeks.org/python/data-wrangling-in-python/)  
- [Intro to EDA — Kaggle Notebook](https://www.kaggle.com/code/imoore/intro-to-exploratory-data-analysis-eda-in-python)  
- [Dataset UCI – Early Stage Diabetes Risk Prediction](https://archive.ics.uci.edu/dataset/529/early+stage+diabetes+risk+prediction+dataset)

---

## ✅ Livrables attendus
- Notebook : `eda_<initiales>_diabetes.ipynb`  
- Dataset nettoyé : `diabetes_clean.csv`
