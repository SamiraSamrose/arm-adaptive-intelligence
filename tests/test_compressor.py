import unittest
import numpy as np
from src.model_compressor import ModelCompressor
from src.model_compressor.quantizer import Quantizer
from src.model_compressor.pruner import Pruner

class TestModelCompressor(unittest.TestCase):
    """
    Tests for model compression module
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.compressor = ModelCompressor()
        self.quantizer = Quantizer(self.compressor.config)
        self.pruner = Pruner(self.compressor.config)
    
    def test_quantizer_4bit(self):
        """
        Tests 4-bit quantization
        """
        model_data = {
            'layer1': np.random.randn(100, 50).astype(np.float32)
        }
        
        result = self.quantizer.quantize(model_data, bits=4)
        
        self.assertIn('quantized_weights', result)
        self.assertIn('quantization_params', result)
        self.assertEqual(result['bits'], 4)
        self.assertGreater(result['compression_ratio'], 1.0)
    
    def test_pruner(self):
        """
        Tests model pruning
        """
        model_data = {
            'layer1': np.random.randn(100, 50).astype(np.float32)
        }
        
        result = self.pruner.prune(model_data, ratio=0.3)
        
        self.assertIn('pruned_weights', result)
        self.assertIn('sparsity', result)
        self.assertGreater(result['sparsity'], 0.0)
    
    def test_compression_ratio(self):
        """
        Tests compression ratio calculation
        """
        original_size = 1000.0
        compressed_size = 250.0
        
        ratio = (original_size - compressed_size) / original_size * 100
        
        self.assertAlmostEqual(ratio, 75.0)

if __name__ == '__main__':
    unittest.main()
