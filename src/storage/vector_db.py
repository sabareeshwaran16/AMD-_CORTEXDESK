import numpy as np
from typing import List, Dict, Any
import pickle
import os

class SimpleVectorDB:
    def __init__(self, db_path: str, dimension: int = 384):
        self.db_path = db_path
        self.dimension = dimension
        self.vectors = []
        self.metadata = []
        self.load()
    
    def add(self, vector: np.ndarray, metadata: Dict[str, Any]):
        self.vectors.append(vector)
        self.metadata.append(metadata)
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.vectors:
            return []
        
        vectors_array = np.array(self.vectors)
        similarities = np.dot(vectors_array, query_vector) / (
            np.linalg.norm(vectors_array, axis=1) * np.linalg.norm(query_vector)
        )
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "metadata": self.metadata[idx],
                "similarity": float(similarities[idx])
            })
        
        return results
    
    def save(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'wb') as f:
            pickle.dump({
                "vectors": self.vectors,
                "metadata": self.metadata
            }, f)
    
    def load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'rb') as f:
                data = pickle.load(f)
                self.vectors = data["vectors"]
                self.metadata = data["metadata"]

class SimpleEmbedding:
    def __init__(self):
        self.dimension = 384
    
    def _tokenize(self, text):
        """Simple tokenization"""
        import re
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def encode(self, text: str) -> np.ndarray:
        """Encode text to vector using word hashing"""
        words = self._tokenize(text)
        vector = np.zeros(self.dimension)
        
        if not words:
            return vector
        
        # Use word hashing to map words to vector positions
        for word in words:
            # Hash word to get index
            word_hash = hash(word) % self.dimension
            # Increment that position (term frequency)
            vector[word_hash] += 1
        
        # Normalize by document length
        vector = vector / len(words)
        
        # L2 normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        return np.array([self.encode(text) for text in texts])
