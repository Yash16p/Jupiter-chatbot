"""
Enhanced TF-IDF Vectorizer with financial domain knowledge
"""

import re
from typing import List
from collections import Counter
import numpy as np
from config.settings import MAX_VOCABULARY_SIZE, SYNONYM_EXPANSION


class EnhancedTFIDFVectorizer:
    """
    Enhanced TF-IDF vectorizer with financial domain synonyms and smart tokenization
    """
    
    def __init__(self):
        self.vocabulary = {}
        self.idf = {}
        self.documents = []
        
        # Financial domain synonyms for better understanding
        self.synonyms = {
            'account': ['account', 'banking', 'wallet', 'portfolio', 'profile'],
            'savings': ['savings', 'deposit', 'money', 'funds', 'balance', 'reserve'],
            'expense': ['expense', 'spending', 'cost', 'payment', 'transaction', 'outflow'],
            'investment': ['investment', 'invest', 'fund', 'portfolio', 'stocks', 'shares'],
            'security': ['security', 'safe', 'secure', 'protection', 'privacy', 'encryption'],
            'fee': ['fee', 'charge', 'cost', 'rate', 'commission', 'levy'],
            'transfer': ['transfer', 'send', 'receive', 'move', 'exchange', 'wire'],
            'budget': ['budget', 'planning', 'tracking', 'management', 'allocation'],
            'interest': ['interest', 'return', 'yield', 'earnings', 'profit'],
            'loan': ['loan', 'credit', 'borrowing', 'advance', 'mortgage']
        }
    
    def fit(self, documents: List[str]) -> None:
        """
        Build enhanced vocabulary with synonym expansion
        
        Args:
            documents: List of text documents to process
        """
        self.documents = documents
        
        # Build vocabulary with synonym expansion
        doc_freq = Counter()
        for doc in documents:
            words = self._tokenize(doc)
            if SYNONYM_EXPANSION:
                # Add synonyms for key terms
                expanded_words = self._expand_with_synonyms(words)
                doc_freq.update(set(expanded_words))
            else:
                doc_freq.update(set(words))
        
        # Limit vocabulary size for performance
        if len(doc_freq) > MAX_VOCABULARY_SIZE:
            # Keep most frequent terms
            doc_freq = Counter(dict(doc_freq.most_common(MAX_VOCABULARY_SIZE)))
        
        # Create vocabulary and IDF
        total_docs = len(documents)
        for word, freq in doc_freq.items():
            self.vocabulary[word] = len(self.vocabulary)
            self.idf[word] = np.log(total_docs / freq)
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Enhanced tokenization with financial terms preservation
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of cleaned tokens
        """
        # Remove special characters but keep financial terms
        text = re.sub(r'[^\w\s\-%₹$]', ' ', text)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out very short words and common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        return [word for word in words if len(word) > 2 and word not in stop_words]
    
    def _expand_with_synonyms(self, words: List[str]) -> List[str]:
        """
        Expand words with their financial synonyms
        
        Args:
            words: List of input words
            
        Returns:
            List of words with synonyms added
        """
        expanded = words.copy()
        for word in words:
            for category, synonyms in self.synonyms.items():
                if word in synonyms:
                    expanded.extend(synonyms)
        return expanded
    
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Transform documents to enhanced TF-IDF vectors
        
        Args:
            documents: List of text documents
            
        Returns:
            Numpy array of TF-IDF vectors
            
        Raises:
            ValueError: If vectorizer hasn't been fitted
        """
        if not self.vocabulary:
            raise ValueError("Vectorizer must be fitted first")
        
        vectors = []
        for doc in documents:
            words = self._tokenize(doc)
            word_freq = Counter(words)
            
            # Create TF-IDF vector
            vector = np.zeros(len(self.vocabulary))
            for word, freq in word_freq.items():
                if word in self.vocabulary:
                    idx = self.vocabulary[word]
                    tf = freq / len(words)
                    vector[idx] = tf * self.idf[word]
            
            vectors.append(vector)
        
        return np.array(vectors)
    
    def transform_single(self, text: str) -> np.ndarray:
        """
        Transform single text to TF-IDF vector
        
        Args:
            text: Input text
            
        Returns:
            TF-IDF vector as numpy array
        """
        return self.transform([text])
    
    def get_feature_names(self) -> List[str]:
        """
        Get feature names (vocabulary words)
        
        Returns:
            List of vocabulary words
        """
        return list(self.vocabulary.keys())
    
    def get_vocabulary_size(self) -> int:
        """
        Get current vocabulary size
        
        Returns:
            Number of words in vocabulary
        """
        return len(self.vocabulary) 