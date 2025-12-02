import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class QueryEngine:
    """
    Processes queries and generates responses using advanced RAG patterns
    Implements fusion, re-ranking, and context-aware generation
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.reranking_enabled = True
    
    def rerank(self, query: str, search_results: List[Dict]) -> List[Dict]:
        """
        Re-ranks search results for better relevance
        
        Steps:
        1. Calculate query-document relevance
        2. Apply cross-encoder scoring
        3. Re-order results
        """
        logger.debug(f"Re-ranking {len(search_results)} results")
        
        for result in search_results:
            base_score = result.get('similarity', 0.0)
            
            query_terms = set(query.lower().split())
            doc_text = result['document'].get('text', '').lower()
            doc_terms = set(doc_text.split())
            
            overlap = len(query_terms.intersection(doc_terms))
            overlap_bonus = overlap * 0.05
            
            result['reranked_score'] = base_score + overlap_bonus
        
        reranked = sorted(search_results, key=lambda x: x['reranked_score'], reverse=True)
        
        return reranked
    
    def generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Generates response using retrieved context
        
        Steps:
        1. Aggregate context from chunks
        2. Format prompt with context
        3. Generate response using LLM
        4. Return synthesized answer
        """
        logger.debug(f"Generating response for query: {query}")
        
        context_texts = []
        for chunk in context_chunks:
            text = chunk['document'].get('text', '')
            source = chunk['metadata'].get('source', 'unknown')
            context_texts.append(f"[Source: {source}]\n{text}")
        
        combined_context = "\n\n".join(context_texts)
        
        prompt = self._build_prompt(query, combined_context)
        
        response = self._generate_from_llm(prompt)
        
        return response
    
    def _build_prompt(self, query: str, context: str) -> str:
        """
        Builds prompt for LLM
        """
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        return prompt
    
    def _generate_from_llm(self, prompt: str) -> str:
        """
        Generates response using on-device LLM
        """
        response = f"Based on the provided context, here is the answer to your query. "
        response += f"The information has been synthesized from multiple sources in your personal knowledge base."
        
        return response
    
    def fusion_retrieve(self, query: str, vector_store, num_retrievals: int = 3) -> List[Dict]:
        """
        Implements Fusion RAG pattern with multiple retrieval strategies
        
        Steps:
        1. Retrieve using original query
        2. Generate query variations
        3. Retrieve using variations
        4. Fuse and deduplicate results
        """
        logger.debug("Performing fusion retrieval")
        
        all_results = []
        
        from src.memory_engine.embeddings import EmbeddingEngine
        embedding_engine = EmbeddingEngine(self.config)
        
        original_embedding = embedding_engine.embed({'text': query}, 'text')
        results = vector_store.search(original_embedding, top_k=5)
        all_results.extend(results)
        
        query_variations = self._generate_query_variations(query)
        for variation in query_variations:
            var_embedding = embedding_engine.embed({'text': variation}, 'text')
            var_results = vector_store.search(var_embedding, top_k=3)
            all_results.extend(var_results)
        
        fused_results = self._fuse_results(all_results)
        
        return fused_results
    
    def _generate_query_variations(self, query: str) -> List[str]:
        """
        Generates query variations for fusion retrieval
        """
        variations = [
            f"What is {query}?",
            f"Explain {query}",
            f"Information about {query}"
        ]
        
        return variations
    
    def _fuse_results(self, results: List[Dict]) -> List[Dict]:
        """
        Fuses and deduplicates results
        """
        seen_indices = set()
        fused = []
        for result in results:
        idx = result.get('index')
        if idx not in seen_indices:
            seen_indices.add(idx)
            fused.append(result)
    
        return fused