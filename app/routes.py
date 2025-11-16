"""
Routes de l'application Flask
"""
from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from typing import List

from app.models import TrainingDocument
from app.services.stop_words import StopWordsService
from app.services.text_preprocessing import TextPreprocessingService
from app.services.naive_bayes import NaiveBayesClassifier
from app.utils.metrics import MetricsCalculator

# Créer le blueprint
bp = Blueprint('main', __name__)

# Services globaux (initialisés au premier appel)
_stop_words_service = None
_preprocessing_service = None
_classifier = None


def get_services():
    """Obtenir les services (singleton pattern)"""
    global _stop_words_service, _preprocessing_service, _classifier
    
    if _stop_words_service is None:
        _stop_words_service = StopWordsService()
        _preprocessing_service = TextPreprocessingService(_stop_words_service)
        _classifier = NaiveBayesClassifier(_preprocessing_service)
    
    return _stop_words_service, _preprocessing_service, _classifier


def load_training_data() -> List[TrainingDocument]:
    """Charger les données d'entraînement depuis le dossier"""
    documents = []
    training_dir = current_app.config['TRAINING_DIR']
    
    if not os.path.exists(training_dir):
        return documents
    
    for filename in os.listdir(training_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(training_dir, filename)
            category = filename.replace('.txt', '')
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                if content:
                    documents.append(TrainingDocument(
                        category=category,
                        content=content,
                        filepath=filepath
                    ))
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return documents


@bp.route('/')
def index():
    """Page d'accueil"""
    _, _, classifier = get_services()
    
    return render_template('index.html', 
                          trained=classifier.is_trained,
                          stats=classifier.get_stats() if classifier.is_trained else None)


@bp.route('/upload')
def upload_page():
    """Page d'upload"""
    _, _, classifier = get_services()
    
    if not classifier.is_trained:
        flash('Le modèle n\'est pas entraîné. Veuillez d\'abord entraîner le modèle.', 'error')
        return redirect(url_for('main.index'))
    
    stats = classifier.get_stats()
    return render_template('upload.html', categories=stats.get('categories', []))


@bp.route('/train', methods=['POST'])
def train():
    """Entraîner le modèle"""
    try:
        _, _, classifier = get_services()
        
        # Charger les données
        documents = load_training_data()
        
        if not documents:
            flash('Aucune donnée d\'entraînement trouvée dans le dossier data/training/', 'error')
            return redirect(url_for('main.index'))
        
        # Entraîner
        classifier.train(documents)
        
        flash(f'Modèle entraîné avec succès! ({len(documents)} documents)', 'success')
        
    except Exception as e:
        flash(f'Erreur lors de l\'entraînement: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))


@bp.route('/train-evaluate', methods=['POST'])
def train_evaluate():
    """Entraîner et évaluer le modèle"""
    try:
        _, _, classifier = get_services()
        
        # Charger les données
        documents = load_training_data()
        
        if not documents:
            flash('Aucune donnée d\'entraînement trouvée', 'error')
            return redirect(url_for('main.index'))
        
        # Split train/test
        import random
        random.shuffle(documents)
        
        test_size = int(len(documents) * current_app.config['TEST_SIZE'])
        train_docs = documents[:-test_size] if test_size > 0 else documents
        test_docs = documents[-test_size:] if test_size > 0 else []
        
        # Entraîner
        classifier.train(train_docs)
        
        # Évaluer
        metrics = None
        if test_docs:
            calculator = MetricsCalculator()
            metrics = calculator.evaluate(classifier, test_docs)
        
        return render_template('index.html',
                             trained=True,
                             stats=classifier.get_stats(),
                             metrics=metrics,
                             train_size=len(train_docs),
                             test_size=len(test_docs),
                             success='Entraînement et évaluation terminés!')
        
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
        return redirect(url_for('main.index'))


@bp.route('/classify-file', methods=['POST'])
def classify_file():
    """Classifier un fichier uploadé"""
    try:
        _, _, classifier = get_services()
        
        if 'file' not in request.files:
            flash('Aucun fichier sélectionné', 'error')
            return redirect(url_for('main.upload_page'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(url_for('main.upload_page'))
        
        # Lire le contenu
        content = file.read().decode('utf-8')
        
        # Classifier
        result = classifier.classify(content)
        
        return render_template('result.html',
                             file_name=file.filename,
                             content=content,
                             result=result)
        
    except Exception as e:
        flash(f'Erreur lors de la classification: {str(e)}', 'error')
        return redirect(url_for('main.upload_page'))


@bp.route('/classify-text', methods=['POST'])
def classify_text():
    """Classifier du texte saisi"""
    try:
        _, _, classifier = get_services()
        
        text = request.form.get('text', '').strip()
        
        if not text:
            flash('Le texte ne peut pas être vide', 'error')
            return redirect(url_for('main.upload_page'))
        
        # Classifier
        result = classifier.classify(text)
        
        return render_template('result.html',
                             file_name='Texte saisi',
                             content=text,
                             result=result)
        
    except Exception as e:
        flash(f'Erreur lors de la classification: {str(e)}', 'error')
        return redirect(url_for('main.upload_page'))


# API JSON Endpoints
@bp.route('/api/stats')
def api_stats():
    """API: Statistiques du modèle"""
    _, _, classifier = get_services()
    return jsonify(classifier.get_stats())


@bp.route('/api/classify', methods=['POST'])
def api_classify():
    """API: Classifier du texte (JSON)"""
    try:
        _, _, classifier = get_services()
        
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = classifier.classify(text)
        
        return jsonify({
            'predicted_category': result.predicted_category,
            'confidence': result.confidence,
            'probabilities': result.probabilities,
            'total_tokens': result.total_tokens,
            'unique_tokens': result.unique_tokens
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500