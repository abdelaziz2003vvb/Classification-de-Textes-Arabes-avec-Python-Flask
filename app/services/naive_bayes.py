"""
Service de classification Naive Bayes
"""
import numpy as np
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
from app.models import ClassificationResult, TrainingDocument
from app.services.text_preprocessing import TextPreprocessingService


class NaiveBayesClassifier:
    """Classificateur Naive Bayes pour textes arabes"""
    
    def __init__(self, preprocessing_service: TextPreprocessingService):
        self.preprocessing = preprocessing_service
        
        # Paramètres du modèle
        self.category_counts: Dict[str, int] = {}
        self.category_word_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.category_total_words: Dict[str, int] = {}
        self.vocabulary: set = set()
        self.total_documents = 0
        self.is_trained = False
    
    def train(self, documents: List[TrainingDocument]):
        """
        Entraîner le modèle Naive Bayes
        
        Args:
            documents: Liste de documents d'entraînement
        """
        print(f"🎓 Starting training with {len(documents)} documents...")
        
        # Réinitialiser le modèle
        self._reset()
        
        # Traiter chaque document
        for doc in documents:
            category = doc.category
            
            # Prétraiter le texte
            stems = self.preprocessing.preprocess(doc.content)
            
            if not stems:
                print(f"⚠️  Empty document for category: {category}")
                continue
            
            # Mettre à jour les compteurs
            self.category_counts[category] = self.category_counts.get(category, 0) + 1
            
            if category not in self.category_total_words:
                self.category_total_words[category] = 0
            
            # Compter les mots
            for stem in stems:
                self.category_word_counts[category][stem] += 1
                self.category_total_words[category] += 1
                self.vocabulary.add(stem)
            
            self.total_documents += 1
        
        self.is_trained = True
        
        print(f"✅ Training completed:")
        print(f"   - Total documents: {self.total_documents}")
        print(f"   - Vocabulary size: {len(self.vocabulary)}")
        print(f"   - Categories: {list(self.category_counts.keys())}")
    
    def classify(self, text: str) -> ClassificationResult:
        """
        Classifier un texte
        
        Args:
            text: Texte à classifier
            
        Returns:
            ClassificationResult avec la catégorie prédite et les probabilités
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        # Prétraiter le texte
        stems = self.preprocessing.preprocess(text)
        
        if not stems:
            return self._create_default_result()
        
        # Calculer les log probabilités
        log_probs = {}
        for category in self.category_counts.keys():
            log_prob = self._calculate_log_probability(category, stems)
            log_probs[category] = log_prob
        
        # Trouver la meilleure catégorie
        predicted_category = max(log_probs, key=log_probs.get)
        
        # Normaliser les probabilités
        probabilities = self._normalize_probabilities(log_probs)
        
        # Créer le résultat
        result = ClassificationResult(
            predicted_category=predicted_category,
            confidence=probabilities[predicted_category],
            probabilities=probabilities,
            total_tokens=len(stems),
            unique_tokens=len(set(stems))
        )
        
        return result
    
    def _calculate_log_probability(self, category: str, words: List[str]) -> float:
        """
        Calculer P(Category|Document) en log
        
        Args:
            category: Catégorie
            words: Liste de mots
            
        Returns:
            Log probabilité
        """
        # Prior: P(Category)
        log_prior = np.log(self.category_counts[category] / self.total_documents)
        
        # Likelihood: P(Words|Category)
        log_likelihood = 0.0
        vocab_size = len(self.vocabulary)
        total_words = self.category_total_words[category]
        
        for word in words:
            # Laplace smoothing
            count = self.category_word_counts[category].get(word, 0)
            probability = (count + 1) / (total_words + vocab_size)
            log_likelihood += np.log(probability)
        
        return log_prior + log_likelihood
    
    def _normalize_probabilities(self, log_probs: Dict[str, float]) -> Dict[str, float]:
        """
        Normaliser les log probabilités en probabilités
        
        Args:
            log_probs: Dictionnaire de log probabilités
            
        Returns:
            Dictionnaire de probabilités normalisées
        """
        # Trouver le max pour stabilité numérique
        max_log_prob = max(log_probs.values())
        
        # Convertir en exponentielles
        exp_probs = {cat: np.exp(lp - max_log_prob) for cat, lp in log_probs.items()}
        
        # Normaliser
        total = sum(exp_probs.values())
        normalized = {cat: prob / total for cat, prob in exp_probs.items()}
        
        return normalized
    
    def _create_default_result(self) -> ClassificationResult:
        """Créer un résultat par défaut"""
        categories = list(self.category_counts.keys())
        prob = 1.0 / len(categories)
        probs = {cat: prob for cat in categories}
        
        return ClassificationResult(
            predicted_category=categories[0],
            confidence=prob,
            probabilities=probs,
            total_tokens=0,
            unique_tokens=0
        )
    
    def _reset(self):
        """Réinitialiser le modèle"""
        self.category_counts = {}
        self.category_word_counts = defaultdict(lambda: defaultdict(int))
        self.category_total_words = {}
        self.vocabulary = set()
        self.total_documents = 0
        self.is_trained = False
    
    def get_stats(self) -> dict:
        """Obtenir les statistiques du modèle"""
        return {
            'trained': self.is_trained,
            'total_documents': self.total_documents,
            'vocabulary_size': len(self.vocabulary),
            'categories': list(self.category_counts.keys()),
            'category_document_count': dict(self.category_counts),
            'category_word_count': dict(self.category_total_words)
        }
    
    def get_category_priors(self) -> Dict[str, float]:
        """Obtenir les probabilités a priori des catégories"""
        return {
            cat: count / self.total_documents 
            for cat, count in self.category_counts.items()
        }