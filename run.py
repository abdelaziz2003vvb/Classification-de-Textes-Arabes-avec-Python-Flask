"""
Point d'entrée de l'application Flask
"""
from app import create_app
import os

# Créer l'application
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # Lancer le serveur
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )