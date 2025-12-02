import numpy as np
from typing import Dict, List, Optional, Tuple
import json
import os
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Lightweight vector database optimized for ARM devices
    Uses efficient indexing and search algorithms
    """
    
    def __init__(self, config: Dict, storage_path: str = "data/vector_store"):
        self.config = config
        self.storage_path = storage_path
        self.vectors = []
        self.documents = []
        self.metadata = []
        self.doc_id_counter = 0
        
        os.makedirs(storage_path, exist_ok=True)
        self._load_index()
    
    def add_documents(self, documents: List[Dict], embeddings: List[np.ndarray], 
                     metadata: Dict) -> str:
        """
        Adds documents to vector store
        
        Steps:
        1. Generate document ID
        2. Store vectors
        3. Store document content
        4. Store metadata
        5. Update index
        """
        doc_id = f"doc_{self.doc_id_counter}"
        self.doc_id_counter += 1
        
        for doc, embedding in zip(documents, embeddings):
            self.vectors.append(embedding)
            self.documents.append(doc)
            self.metadata.append({
                'document_id': doc_id,
                **metadata
            })
        
        logger.info(f"Added {len(documents)} chunks with ID: {doc_id}")
        
        self._save_index()
        
        return doc_id
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5, 
              filters: Optional[Dict] = None) -> List[Dict]:
        """
        Searches for similar vectors
        
        Steps:
        1. Calculate similarities with all vectors
        2. Apply filters if provided
        3. Sort by similarity
        4. Return top-k results
        """
        if not self.vectors:
            logger.warning("Vector store is empty")
            return []
        
        vectors_array = np.array(self.vectors)
        
        similarities = np.dot(vectors_array, query_embedding)
        
        if filters:
            valid_indices = self._apply_filters(filters)
            similarities = similarities * valid_indices
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'document': self.documents[idx],
                'metadata': self.metadata[idx],
                'similarity': float(similarities[idx]),
                'index': int(idx)
            })
        
        return results
    
    def _apply_filters(self, filters: Dict) -> np.ndarray:
        """
        Applies filters to search results
        """
        mask = np.ones(len(self.metadata), dtype=bool)
        
        for key, value in filters.items():
            for i, meta in enumerate(self.metadata):
                if meta.get(key) != value:
                    mask[i] = False
        
        return mask.astype(float)
    
    def delete_document(self, document_id: str) -> int:
        """
        Deletes all chunks belonging to a document
        """
        indices_to_delete = []
        
        for i, meta in enumerate(self.metadata):
            if meta.get('document_id') == document_id:
                indices_to_delete.append(i)
        
        for idx in sorted(indices_to_delete, reverse=True):
            del self.vectors[idx]
            del self.documents[idx]
            del self.metadata[idx]
        
        logger.info(f"Deleted {len(indices_to_delete)} chunks for document {document_id}")
        
        self._save_index()
        
        return len(indices_to_delete)
    
    def get_total_vectors(self) -> int:
        """
        Gets total number of vectors
        """
        return len(self.vectors)
    
    def _save_index(self):
        """
        Saves index to disk
        """
        try:
            np.save(os.path.join(self.storage_path, 'vectors.npy'), np.array(self.vectors))
            
            with open(os.path.join(self.storage_path, 'documents.json'), 'w') as f:
                json.dump(self.documents, f)
            
            with open(os.path.join(self.storage_path, 'metadata.json'), 'w') as f:
                json.dump(self.metadata, f)
            
            with open(os.path.join(self.storage_path, 'config.json'), 'w') as f:
                json.dump({'doc_id_counter': self.doc_id_counter}, f)
            
            logger.debug("Index saved to disk")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
    
    def _load_index(self):
        """
        Loads index from disk
        """
        try:
            vectors_path = os.path.join(self.storage_path, 'vectors.npy')
            if os.path.exists(vectors_path):
                self.vectors = np.load(vectors_path).tolist()
            
            docs_path = os.path.join(self.storage_path, 'documents.json')
            if os.path.exists(docs_path):
                with open(docs_path, 'r') as f:
                    self.documents = json.load(f)
            
            meta_path = os.path.join(self.storage_path, 'metadata.json')
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as f:
                    self.metadata = json.load(f)
            
            config_path = os.path.join(self.storage_path, 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.doc_id_counter = config.get('doc_id_counter', 0)
            
            logger.info(f"Loaded index: {len(self.vectors)} vectors")
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
    
    def clear(self):
        """
        Clears all data from vector store
        """
        self.vectors = []
        self.documents = []
        self.metadata = []
        self.doc_id_counter = 0
        self._save_index()
        logger.info("Vector store cleared")
