"""
Modèles de données
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ClassificationResult:
    """Résultat de classification"""
    predicted_category: str
    confidence: float
    probabilities: Dict[str, float]
    total_tokens: int
    unique_tokens: int


@dataclass
class EvaluationMetrics:
    """Métriques d'évaluation"""
    accuracy: float
    precision: Dict[str, float]
    recall: Dict[str, float]
    f1_score: Dict[str, float]
    confusion_matrix: List[List[int]]
    categories: List[str]
    
    @property
    def macro_avg(self) -> Dict[str, float]:
        """Moyennes macro"""
        return {
            'precision': sum(self.precision.values()) / len(self.precision),
            'recall': sum(self.recall.values()) / len(self.recall),
            'f1_score': sum(self.f1_score.values()) / len(self.f1_score)
        }


@dataclass
class TrainingDocument:
    """Document d'entraînement"""
    category: str
    content: str
    filepath: Optional[str] = None