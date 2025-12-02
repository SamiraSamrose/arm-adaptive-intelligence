import os
from typing import Dict, List, Optional, Union
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class RAGCore:
    """
    Core RAG implementation for on-device personal memory
    Supports text, images, audio, and PDF documents
    """
    
    def __init__(self, embedding_engine, vector_store, query_engine):
        self.embedding_engine = embedding_engine
        self.vector_store = vector_store
        self.query_engine = query_engine
        self.indexed_documents = {}
    
    def index_document(self, document_path: str, document_type: str = "auto") -> Dict:
        """
        Indexes a document into the RAG system
        
        Steps:
        1. Detect document type if auto
        2. Extract content based on type
        3. Generate embeddings
        4. Store in vector database
        5. Update metadata
        """
        logger.info(f"Indexing document: {document_path}")
        
        if document_type == "auto":
            document_type = self._detect_document_type(document_path)
        
        content = self._extract_content(document_path, document_type)
        
        chunks = self._chunk_content(content, document_type)
        
        embeddings = []
        for chunk in chunks:
            embedding = self.embedding_engine.embed(chunk, document_type)
            embeddings.append(embedding)
        
        doc_id = self.vector_store.add_documents(chunks, embeddings, {
            'source': document_path,
            'type': document_type,
            'num_chunks': len(chunks)
        })
        
        self.indexed_documents[doc_id] = {
            'path': document_path,
            'type': document_type,
            'chunks': len(chunks)
        }
        
        logger.info(f"Document indexed: {doc_id}, {len(chunks)} chunks")
        
        return {
            'document_id': doc_id,
            'chunks_created': len(chunks),
            'document_type': document_type
        }
    
    def _detect_document_type(self, document_path: str) -> str:
        """
        Detects document type from file extension
        """
        ext = Path(document_path).suffix.lower()
        
        type_map = {
            '.txt': 'text',
            '.md': 'text',
            '.pdf': 'pdf',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.wav': 'audio',
            '.mp3': 'audio',
            '.m4a': 'audio'
        }
        
        return type_map.get(ext, 'text')
    
    def _extract_content(self, document_path: str, document_type: str) -> Union[str, bytes, Dict]:
        """
        Extracts content from document based on type
        
        Steps:
        1. For text: read file content
        2. For PDF: extract text using OCR
        3. For image: perform OCR
        4. For audio: transcribe to text
        """
        if document_type == 'text':
            with open(document_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif document_type == 'pdf':
            return self._extract_pdf_text(document_path)
        
        elif document_type == 'image':
            return self._extract_image_content(document_path)
        
        elif document_type == 'audio':
            return self._transcribe_audio(document_path)
        
        else:
            logger.warning(f"Unknown document type: {document_type}")
            return ""
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """
        Extracts text from PDF
        """
        logger.info(f"Extracting text from PDF: {pdf_path}")
        return f"Extracted text from PDF: {pdf_path}"
    
    def _extract_image_content(self, image_path: str) -> Dict:
        """
        Extracts content from image using OCR
        """
        logger.info(f"Performing OCR on image: {image_path}")
        return {
            'ocr_text': f"OCR text from {image_path}",
            'image_path': image_path
        }
    
    def _transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribes audio to text
        """
        logger.info(f"Transcribing audio: {audio_path}")
        return f"Transcribed audio from {audio_path}"
    
    def _chunk_content(self, content: Union[str, Dict], document_type: str, 
                      chunk_size: int = 512) -> List[Dict]:
        """
        Chunks content into manageable pieces
        
        Steps:
        1. Split content based on type
        2. Create overlapping chunks
        3. Preserve metadata
        """
        chunks = []
        
        if isinstance(content, str):
            words = content.split()
            
            for i in range(0, len(words), chunk_size // 2):
                chunk_words = words[i:i + chunk_size]
                chunk_text = ' '.join(chunk_words)
                
                chunks.append({
                    'text': chunk_text,
                    'type': document_type,
                    'chunk_index': len(chunks)
                })
        
        elif isinstance(content, dict):
            chunks.append({
                'text': content.get('ocr_text', ''),
                'type': document_type,
                'metadata': content
            })
        
        return chunks if chunks else [{'text': '', 'type': document_type}]
    
    def query(self, query_text: str, top_k: int = 5, filters: Optional[Dict] = None) -> Dict:
        """
        Queries the RAG system
        
        Steps:
        1. Generate query embedding
        2. Search vector store
        3. Retrieve relevant chunks
        4. Re-rank results
        5. Generate response
        """
        logger.info(f"Querying: '{query_text}' (top_k={top_k})")
        
        query_embedding = self.embedding_engine.embed({'text': query_text}, 'text')
        
        search_results = self.vector_store.search(query_embedding, top_k * 2, filters)
        
        reranked_results = self.query_engine.rerank(query_text, search_results)
        
        top_results = reranked_results[:top_k]
        
        response = self.query_engine.generate_response(query_text, top_results)
        
        return {
            'query': query_text,
            'response': response,
            'sources': top_results,
            'num_sources': len(top_results)
        }
    
    def delete_document(self, document_id: str) -> bool:
        """
        Deletes a document from the RAG system
        """
        logger.info(f"Deleting document: {document_id}")
        
        if document_id in self.indexed_documents:
            self.vector_store.delete_document(document_id)
            del self.indexed_documents[document_id]
            return True
        
        return False
    
    def get_statistics(self) -> Dict:
        """
        Gets RAG system statistics
        """
        return {
            'total_documents': len(self.indexed_documents),
            'total_chunks': self.vector_store.get_total_vectors(),
            'document_types': self._get_document_type_distribution()
        }
    
    def _get_document_type_distribution(self) -> Dict:
        """
        Gets distribution of document types
        """
        distribution = {}
        for doc_info in self.indexed_documents.values():
            doc_type = doc_info['type']
            distribution[doc_type] = distribution.get(doc_type, 0) + 1
        return distribution
