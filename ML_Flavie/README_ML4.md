# ML4 - Application de scoring connectée à l’API

## Contexte du projet
Cette application web permet d’envoyer les données d’un patient à l’API `/predict`, de récupérer la réponse et d’afficher le score ainsi que la décision de manière claire et lisible.  
> ⚠️ Ce projet est une démonstration éducative et ne constitue pas un outil médical réel.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Objectifs
- Intégrer l’API construite lors du ML3.
- Respecter le contrat d’entrée/sortie (noms et types des features).
- Fournir une interface web simple et intuitive pour la démo.
- Gérer les erreurs de saisie et les problèmes de communication avec l’API.

## Technologies utilisées
- Python
- Gradio / Streamlit / Flask / Shiny Python (au choix)
- Requests pour appeler l’API
- Joblib / Pickle pour le modèle
- Front-end léger intégré dans l’outil choisi

## Fonctionnalités
1. Formulaire web pour saisir les données du patient.
2. Vérification des types et valeurs :
   - Valeurs manquantes → message d’erreur clair
   - Valeurs impossibles (ex : âge négatif, glucose > 1000) → message d’erreur
3. Envoi des données à l’API `/predict`.
4. Affichage de la prédiction :
   - **Score** (probabilité)
   - **Décision** (positif / négatif)
5. Gestion des erreurs de connexion :
   - API non disponible → message clair
   - Temps de réponse > 5s → message d’avertissement

