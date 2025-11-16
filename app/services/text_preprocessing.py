"""
Service de prétraitement de texte arabe
"""
import re
from typing import List
from app.services.stop_words import StopWordsService


class TextPreprocessingService:
    """Service de prétraitement de texte arabe"""
    
    def __init__(self, stop_words_service: StopWordsService):
        self.stop_words_service = stop_words_service
        
        # Suffixes arabes courants à retirer pour le stemming
        self.suffixes = [
            "ون", "ين", "ات", "ان", "ها", "هم", "هن", 
            "كم", "كن", "ني", "ه", "ة", "ي"
        ]
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizer simple pour l'arabe
        
        Args:
            text: Texte arabe à tokenizer
            
        Returns:
            Liste de tokens
        """
        # Supprimer la ponctuation (sauf les caractères arabes)
        text = re.sub(r'[^\u0600-\u06FF\s]', ' ', text)
        
        # Séparer par les espaces
        tokens = text.split()
        
        # Nettoyer et filtrer les tokens vides
        tokens = [token.strip() for token in tokens if token.strip()]
        
        return tokens
    
    def stem(self, tokens: List[str]) -> List[str]:
        """
        Stemming simple pour l'arabe
        
        Args:
            tokens: Liste de tokens
            
        Returns:
            Liste de stems
        """
        stems = []
        
        for token in tokens:
            # Ignorer les stop words
            if self.stop_words_service.is_stop_word(token):
                continue
            
            stem = token
            
            # Retirer les suffixes
            for suffix in self.suffixes:
                if stem.endswith(suffix) and len(stem) > len(suffix) + 2:
                    stem = stem[:-len(suffix)]
                    break
            
            stems.append(stem)
        
        return stems
    
    def preprocess(self, text: str) -> List[str]:
        """
        Pipeline complet de prétraitement
        
        Args:
            text: Texte arabe à prétraiter
            
        Returns:
            Liste de stems
        """
        # Tokenization
        tokens = self.tokenize(text)
        
        # Stemming + filtrage stop words
        stems = self.stem(tokens)
        
        return stems
    
    def get_stats(self) -> dict:
        """Obtenir les statistiques du service"""
        return {
            'tokenizer': 'Simple Arabic Tokenizer',
            'stemmer': 'Simple Arabic Stemmer',
            'stop_words_count': self.stop_words_service.get_count()
        }