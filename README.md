# 🐍 Classification de Textes Arabes avec Flask

Application web de classification automatique de textes arabes utilisant **Naive Bayes** et **Python Flask**.

## ✨ Fonctionnalités

- 🔤 Classification de textes arabes
- 📊 Entraînement et évaluation du modèle
- 📁 Upload de fichiers .txt
- ✍️ Saisie directe de texte
- 📈 Métriques détaillées (Accuracy, Precision, Recall, F1)
- 🎨 Interface web moderne et responsive

## 🛠️ Technologies

- Python 3.8+
- Flask 3.0.0
- NumPy & Pandas
- Scikit-learn
- NLTK

## 🚀 Installation
```bash
# Cloner le projet
git clone https://github.com/yourusername/arabic-text-classifier.git
cd arabic-text-classifier

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py
```

## 📖 Utilisation

1. **Préparer les données**: Ajoutez des fichiers `.txt` dans `data/training/`
2. **Entraîner**: Cliquez sur "Entraîner le Modèle"
3. **Classifier**: Uploadez un fichier ou saisissez du texte

## 📁 Structure
arabic-text-classifier/
├── app/              # Application Flask
├── data/             # Données d'entraînement
├── config.py         # Configuration
├── run.py            # Point d'entrée
└── requirements.txt  # Dépendances

## 🤝 Contribuer

Les contributions sont les bienvenues!

## 📄 Licence

MIT License
✅ PROJET FLASK COMPLET!
Pour démarrer:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py