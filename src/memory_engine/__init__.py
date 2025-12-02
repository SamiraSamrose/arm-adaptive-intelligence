from src.memory_engine.rag_core import RAGCore
from src.memory_engine.embeddings import EmbeddingEngine
from src.memory_engine.vector_store import VectorStore
from src.memory_engine.query_engine import QueryEngine

class MemoryEngine:
    """
    Main interface for personal memory and RAG operations
    """
    
    def __init__(self, config_path: str = "config/model_config.yaml"):
        from src.core.utils import load_config
        self.config = load_config(config_path)
        
        self.embedding_engine = EmbeddingEngine(self.config)
        self.vector_store = VectorStore(self.config)
        self.query_engine = QueryEngine(self.config)
        self.rag_core = RAGCore(
            self.embedding_engine,
            self.vector_store,
            self.query_engine
        )
    
    def index_document(self, document_path: str, document_type: str = "text"):
        """
        Indexes a document into the memory engine
        """
        return self.rag_core.index_document(document_path, document_type)
    
    def query(self, query_text: str, top_k: int = 5):
        """
        Queries the memory engine
        """
        return self.rag_core.query(query_text, top_k)

__all__ = ["MemoryEngine", "RAGCore", "EmbeddingEngine", "VectorStore", "QueryEngine"]
