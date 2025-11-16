"""
Calcul des métriques d'évaluation
"""
import numpy as np
from typing import List, Dict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from app.models import EvaluationMetrics, TrainingDocument
from app.services.naive_bayes import NaiveBayesClassifier


class MetricsCalculator:
    """Calculateur de métriques d'évaluation"""
    
    @staticmethod
    def evaluate(model: NaiveBayesClassifier, 
                 test_documents: List[TrainingDocument]) -> EvaluationMetrics:
        """
        Évaluer le modèle sur des documents de test
        
        Args:
            model: Modèle entraîné
            test_documents: Documents de test
            
        Returns:
            EvaluationMetrics avec toutes les métriques
        """
        print(f"📊 Evaluating model on {len(test_documents)} test documents...")
        
        # Prédictions
        y_true = []
        y_pred = []
        
        for doc in test_documents:
            y_true.append(doc.category)
            result = model.classify(doc.content)
            y_pred.append(result.predicted_category)
        
        # Catégories uniques
        categories = sorted(set(y_true))
        
        # Accuracy
        accuracy = accuracy_score(y_true, y_pred)
        
        # Precision, Recall, F1-Score
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=categories, average=None, zero_division=0
        )
        
        # Matrice de confusion
        conf_matrix = confusion_matrix(y_true, y_pred, labels=categories)
        
        # Créer les dictionnaires
        precision_dict = {cat: prec for cat, prec in zip(categories, precision)}
        recall_dict = {cat: rec for cat, rec in zip(categories, recall)}
        f1_dict = {cat: f for cat, f in zip(categories, f1)}
        
        print(f"✅ Evaluation completed:")
        print(f"   - Accuracy: {accuracy:.2%}")
        
        return EvaluationMetrics(
            accuracy=accuracy,
            precision=precision_dict,
            recall=recall_dict,
            f1_score=f1_dict,
            confusion_matrix=conf_matrix.tolist(),
            categories=categories
        )