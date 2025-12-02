from src.model_compressor.quantizer import Quantizer
from src.model_compressor.pruner import Pruner
from src.model_compressor.distiller import Distiller
from src.model_compressor.benchmark import Benchmark

class ModelCompressor:
    """
    Main interface for model compression operations
    """
    
    def __init__(self, config_path: str = "config/model_config.yaml"):
        from src.core.utils import load_config
        self.config = load_config(config_path)
        
        self.quantizer = Quantizer(self.config)
        self.pruner = Pruner(self.config)
        self.distiller = Distiller(self.config)
        self.benchmark = Benchmark(self.config)
    
    def compress_model(self, model_path: str, output_path: str, 
                      quantization_bits: int = 4, pruning_ratio: float = 0.3):
        """
        Compresses model using quantization and pruning
        """
        quantized = self.quantizer.quantize(model_path, bits=quantization_bits)
        pruned = self.pruner.prune(quantized, ratio=pruning_ratio)
        
        return self.benchmark.evaluate(pruned, output_path)

__all__ = ["ModelCompressor", "Quantizer", "Pruner", "Distiller", "Benchmark"]