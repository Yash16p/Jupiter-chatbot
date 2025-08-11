"""
Enhanced Similarity Search for Jupiter.money RAG Bot
"""

import numpy as np
import re
from typing import List, Tuple
from .vectorizer import EnhancedTFIDFVectorizer
from config.settings import MIN_SIMILARITY_THRESHOLD


class EnhancedSimilaritySearch:
    """
    Enhanced similarity search using multiple algorithms
    """
    
    def __init__(self):
        self.vectorizer = EnhancedTFIDFVectorizer()
        self.is_fitted = False
    
    def fit(self, documents: List[str]):
        """Fit the vectorizer on documents"""
        self.vectorizer.fit(documents)
        self.is_fitted = True
    
    def calculate_similarity(self, query: str, documents: List[str]) -> List[Tuple[int, float, str]]:
        """Calculate similarity between query and documents using multiple metrics"""
        if not self.is_fitted:
            return self._fallback_similarity(query, documents)
        
        try:
            # TF-IDF similarity
            query_vector = self.vectorizer.transform_single(query)
            doc_vectors = self.vectorizer.transform(documents)
            
            # Cosine similarity
            similarities = []
            for i, doc_vector in enumerate(doc_vectors):
                # Cosine similarity
                cos_sim = self._cosine_similarity(query_vector.flatten(), doc_vector)
                
                # Word overlap similarity
                word_overlap = self._word_overlap_similarity(query, documents[i])
                
                # Combined similarity (weighted average)
                combined_sim = 0.7 * cos_sim + 0.3 * word_overlap
                
                similarities.append((i, combined_sim, documents[i]))
            
            return similarities
            
        except Exception as e:
            return self._fallback_similarity(query, documents)
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    def _word_overlap_similarity(self, query: str, document: str) -> float:
        """Calculate word overlap similarity"""
        query_words = set(self.vectorizer._tokenize(query))
        doc_words = set(self.vectorizer._tokenize(document))
        
        if not query_words:
            return 0
        
        intersection = query_words.intersection(doc_words)
        union = query_words.union(doc_words)
        
        return len(intersection) / len(union) if union else 0
    
    def _fallback_similarity(self, query: str, documents: List[str]) -> List[Tuple[int, float, str]]:
        """Fallback to simple word similarity"""
        similarities = []
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        
        for i, doc in enumerate(documents):
            doc_words = set(re.findall(r'\b\w+\b', doc.lower()))
            
            if not query_words:
                continue
                
            intersection = query_words.intersection(doc_words)
            union = query_words.union(doc_words)
            
            if union:
                similarity = len(intersection) / len(union)
                similarities.append((i, similarity, doc))
        
        return similarities 