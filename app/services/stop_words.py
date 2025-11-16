"""
Service de gestion des stop words arabes
"""
import os
from typing import Set, List
from flask import current_app


class StopWordsService:
    """Service pour gérer les stop words arabes"""
    
    def __init__(self):
        self.stop_words: Set[str] = set()
        self._load_stop_words()
    
    def _load_stop_words(self):
        """Charger les stop words depuis le fichier"""
        try:
            stopwords_file = current_app.config['STOPWORDS_FILE']
            
            if os.path.exists(stopwords_file):
                with open(stopwords_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.stop_words.add(line)
                print(f"✅ Loaded {len(self.stop_words)} Arabic stop words")
            else:
                self._load_default_stop_words()
                print("⚠️  Stop words file not found, using default set")
                
        except Exception as e:
            print(f"❌ Error loading stop words: {e}")
            self._load_default_stop_words()
    
    def _load_default_stop_words(self):
        """Charger les stop words par défaut"""
        default_stop_words = [
            "ال", "الـ", "هو", "هي", "هم", "هن", "أنت", "أنتم", "أنتن",
            "أنا", "نحن", "هذا", "هذه", "ذلك", "تلك", "هؤلاء", "أولئك",
            "في", "من", "إلى", "على", "عن", "مع", "ب", "ل", "ك",
            "و", "أو", "لكن", "ثم", "أم", "إما", "لا",
            "كان", "يكون", "ليس", "قد", "لم", "لن",
            "ما", "ماذا", "من", "متى", "أين", "كيف", "لماذا", "هل",
            "كل", "بعض", "غير", "عند", "حتى", "بين", "أن", "إن",
            "التي", "الذي", "اللذان", "اللتان", "الذين", "اللاتي"
        ]
        self.stop_words = set(default_stop_words)
    
    def is_stop_word(self, word: str) -> bool:
        """Vérifier si un mot est un stop word"""
        return word in self.stop_words
    
    def filter_stop_words(self, words: List[str]) -> List[str]:
        """Filtrer les stop words d'une liste de mots"""
        return [word for word in words if not self.is_stop_word(word)]
    
    def get_count(self) -> int:
        """Obtenir le nombre de stop words"""
        return len(self.stop_words)