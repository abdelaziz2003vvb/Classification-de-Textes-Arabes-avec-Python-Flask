"""
Configuration de l'application Flask
"""
import os

class Config:
    """Configuration de base"""
    
    # Clé secrète pour les sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuration des fichiers
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    UPLOAD_EXTENSIONS = ['.txt']
    
    # Chemins
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TRAINING_DIR = os.path.join(DATA_DIR, 'training')
    STOPWORDS_FILE = os.path.join(DATA_DIR, 'stopwords', 'arabic_stopwords.txt')
    
    # Configuration du modèle
    TEST_SIZE = 0.2  # 20% pour le test
    RANDOM_STATE = 42
    
    # Debug mode
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'


class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False


# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}