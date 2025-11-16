"""
Initialisation de l'application Flask
"""
from flask import Flask
from flask_cors import CORS
from config import config
import os


def create_app(config_name='default'):
    """Factory pour créer l'application Flask"""
    
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(config[config_name])
    
    # Activer CORS
    CORS(app)
    
    # Créer les dossiers nécessaires
    os.makedirs(app.config['TRAINING_DIR'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['STOPWORDS_FILE']), exist_ok=True)
    
    # Enregistrer les routes
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app