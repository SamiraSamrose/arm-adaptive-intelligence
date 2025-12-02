import unittest
from src.memory_engine import MemoryEngine

class TestMemoryEngine(unittest.TestCase):
    """
    Tests for memory engine module
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.engine = MemoryEngine()
    
    def test_index_document(self):
        """
        Tests document indexing
        """
        result = self.engine.rag_core.index_document("test.txt", "text")
        
        self.assertIn('document_id', result)
        self.assertIn('chunks_created', result)
    
    def test_query(self):
        """
        Tests querying
        """
        self.engine.rag_core.index_document("test.txt", "text")
        
        result = self.engine.rag_core.query("test query", top_k=3)
        
        self.assertIn('response', result)
        self.assertIn('sources', result)

if __name__ == '__main__':
    unittest.main()
