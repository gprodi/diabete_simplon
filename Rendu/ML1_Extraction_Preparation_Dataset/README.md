# ML1 - Extraction et Préparation du Dataset

## 📋 Contexte du Brief

Ce premier brief établit les fondations du projet de machine learning en se concentrant sur l'acquisition, l'exploration et la préparation des données relatives au diabète. La qualité des données conditionne directement la performance des modèles qui seront développés dans les briefs suivants.

## 🎯 Objectifs

- Identifier et extraire un dataset pertinent sur le diabète
- Réaliser une analyse exploratoire des données (EDA)
- Nettoyer et traiter les valeurs manquantes
- Détecter et gérer les valeurs aberrantes
- Effectuer l'ingénierie des features (feature engineering)
- Préparer les jeux de données train/test
- Documenter toutes les transformations appliquées

## 📦 Livrables Attendus

| Livrable | Description | Emplacement |
|----------|-------------|-------------|
| Dataset brut | Fichier CSV original non modifié | `data/raw/diabetes_raw.csv` |
| Notebook EDA | Analyse exploratoire complète | `notebooks/01_exploration.ipynb` |
| Dataset nettoyé | Données après nettoyage | `data/cleaned/diabetes_clean.csv` |
| Jeux train/test | Données prêtes pour l'entraînement | `data/processed/train.csv`, `data/processed/test.csv` |
| Documentation | Rapport de préparation des données | `docs/data_preparation_report.md` |
| Script de preprocessing | Code réutilisable pour le nettoyage | `scripts/preprocess.py` |

## ✅ Critères d'Évaluation

- **Qualité de l'EDA** : Visualisations pertinentes, statistiques descriptives complètes
- **Pertinence du nettoyage** : Justification des choix de traitement
- **Traçabilité** : Documentation claire de toutes les transformations
- **Reproductibilité** : Scripts permettant de reproduire le preprocessing
- **Validation des données** : Vérification de la cohérence post-traitement
- **Gestion des biais** : Identification et documentation des biais potentiels

## 🛠️ Technologies Recommandées

```python
# Manipulation de données
pandas >= 1.5.0
numpy >= 1.23.0

# Visualisation
matplotlib >= 3.6.0
seaborn >= 0.12.0
plotly >= 5.11.0

# Analyse statistique
scipy >= 1.9.0
scikit-learn >= 1.2.0  # Pour scaling, encoding, split
```

## 📊 Entrées / Sorties

| Type | Description | Format |
|------|-------------|--------|
| **Entrée** | Dataset brut diabète (Kaggle, UCI, etc.) | CSV |
| **Sortie** | Dataset nettoyé avec features engineered | CSV |
| **Sortie** | Train set (80%) | CSV |
| **Sortie** | Test set (20%) | CSV |
| **Sortie** | Rapport EDA | Notebook + PDF |

## 🚀 Comment Lancer

### 1. Installation des dépendances

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### 2. Structure minimale du projet

```
ML1_Extraction_Preparation_Dataset/
├── data/
│   ├── raw/              # Données brutes (ne jamais modifier)
│   ├── cleaned/          # Données après nettoyage
│   └── processed/        # Données prêtes pour ML
├── notebooks/
│   └── 01_exploration.ipynb
├── scripts/
│   └── preprocess.py
└── README.md
```

### 3. Exemple de script minimal

```python
# scripts/preprocess.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_clean_data(filepath):
    """Charge et nettoie le dataset."""
    df = pd.read_csv(filepath)
    
    # Traitement des valeurs manquantes
    df = df.dropna(subset=['target_column'])  # Adapter selon votre cas
    
    # Traitement des doublons
    df = df.drop_duplicates()
    
    return df

def engineer_features(df):
    """Crée de nouvelles features pertinentes."""
    # Exemple : BMI categories
    if 'BMI' in df.columns:
        df['BMI_category'] = pd.cut(df['BMI'], 
                                     bins=[0, 18.5, 25, 30, 100],
                                     labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    return df

def split_and_save(df, test_size=0.2, random_state=42):
    """Sépare en train/test et sauvegarde."""
    train, test = train_test_split(df, test_size=test_size, 
                                     random_state=random_state,
                                     stratify=df['Outcome'])  # Adapter le nom de la colonne cible
    
    train.to_csv('data/processed/train.csv', index=False)
    test.to_csv('data/processed/test.csv', index=False)
    
    print(f"Train set: {len(train)} samples")
    print(f"Test set: {len(test)} samples")

if __name__ == "__main__":
    # Pipeline complet
    df = load_and_clean_data('data/raw/diabetes_raw.csv')
    df = engineer_features(df)
    df.to_csv('data/cleaned/diabetes_clean.csv', index=False)
    split_and_save(df)
```

### 4. Lancement de l'analyse

```bash
# Démarrer Jupyter pour l'EDA
jupyter notebook notebooks/01_exploration.ipynb

# Exécuter le preprocessing
python scripts/preprocess.py
```

## ⚠️ Erreurs Communes

### Erreur 1 : Fuite de données (Data Leakage)
```python
# ❌ MAUVAIS : Scaling avant le split
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)
train, test = train_test_split(df_scaled)

# ✅ BON : Split d'abord, puis scaling
train, test = train_test_split(df)
scaler = StandardScaler()
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)  # Pas de fit sur test !
```

### Erreur 2 : Perte de traçabilité
```python
# ❌ MAUVAIS : Modifications sans documentation
df = df.dropna()
df = df[df['Age'] > 0]

# ✅ BON : Documentation des transformations
print(f"Avant dropna: {len(df)} lignes")
df = df.dropna()
print(f"Après dropna: {len(df)} lignes ({len(df) - original_len} supprimées)")
```

### Erreur 3 : Valeurs aberrantes non traitées
```python
# Toujours vérifier les distributions
df.describe()
df.boxplot(column=['Glucose', 'BMI', 'BloodPressure'])

# Identifier les valeurs impossibles (ex: Glucose = 0)
print(f"Glucose = 0: {(df['Glucose'] == 0).sum()} occurrences")
```

### Erreur 4 : Déséquilibre de classes ignoré
```python
# Vérifier la distribution de la cible
print(df['Outcome'].value_counts())
print(df['Outcome'].value_counts(normalize=True))

# Utiliser stratify dans train_test_split
train, test = train_test_split(df, stratify=df['Outcome'])
```

## 📚 Checklist de Validation

- [ ] Dataset brut sauvegardé et versionné
- [ ] EDA complète avec visualisations
- [ ] Valeurs manquantes traitées et documentées
- [ ] Outliers analysés et gérés
- [ ] Features engineered pertinentes
- [ ] Encodage des variables catégorielles
- [ ] Scaling/normalisation des features numériques (si nécessaire)
- [ ] Split train/test avec stratification
- [ ] Distribution des classes vérifiée
- [ ] Documentation complète des transformations
- [ ] Scripts reproductibles testés

## 🔗 Dépendances

**Aucune** - Ce brief est le point de départ du projet.

## ➡️ Suite du Projet

Les données préparées ici seront utilisées dans **ML2_Entrainement_Modele** pour l'entraînement des modèles de prédiction.

---

## ⚠️ Avertissement Éthique

**Ce projet est un PoC éducatif et ne constitue en aucun cas un outil médical.**  
Les prédictions générées ne doivent pas être utilisées pour un diagnostic médical réel. Toute application en contexte médical nécessite une validation clinique rigoureuse et le respect des réglementations en vigueur (RGPD, dispositifs médicaux, etc.).
