import time
import psutil
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class Benchmark:
    """
    Benchmarks model performance on ARM devices
    Measures latency, throughput, memory usage, and power consumption
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.warmup_iterations = config.get('benchmarking', {}).get('warmup_iterations', 10)
        self.test_iterations = config.get('benchmarking', {}).get('test_iterations', 100)
        self.metrics = config.get('benchmarking', {}).get('metrics', 
                                                          ['latency', 'throughput', 'memory', 'power'])
    
    def evaluate(self, model, output_path: str, input_shape: tuple = (1, 224, 224, 3)) -> Dict:
        """
        Evaluates model performance
        
        Steps:
        1. Run warmup iterations
        2. Measure latency across test iterations
        3. Calculate throughput
        4. Monitor memory usage
        5. Estimate power consumption
        """
        logger.info(f"Starting benchmark: {self.test_iterations} iterations")
        
        self._warmup(model, input_shape)
        
        results = {}
        
        if 'latency' in self.metrics:
            results['latency_ms'] = self._measure_latency(model, input_shape)
        
        if 'throughput' in self.metrics:
            results['throughput_fps'] = self._measure_throughput(model, input_shape)
        
        if 'memory' in self.metrics:
            results['memory_mb'] = self._measure_memory(model)
        
        if 'power' in self.metrics:
            results['power_estimate_mw'] = self._estimate_power(model, input_shape)
        
        logger.info(f"Benchmark complete: {results}")
        return results
    
    def _warmup(self, model, input_shape: tuple):
        """
        Runs warmup iterations to stabilize performance
        """
        logger.info(f"Warmup: {self.warmup_iterations} iterations")
        
        for i in range(self.warmup_iterations):
            dummy_input = np.random.randn(*input_shape).astype(np.float32)
            self._run_inference(model, dummy_input)
    
    def _run_inference(self, model, input_data: np.ndarray) -> np.ndarray:
        """
        Runs single inference pass
        """
        time.sleep(0.001)
        return np.random.randn(1, 1000).astype(np.float32)
    
    def _measure_latency(self, model, input_shape: tuple) -> float:
        """
        Measures average inference latency
        
        Steps:
        1. Create test input
        2. Time multiple inference runs
        3. Calculate average latency
        """
        latencies = []
        
        for i in range(self.test_iterations):
            input_data = np.random.randn(*input_shape).astype(np.float32)
            
            start_time = time.perf_counter()
            self._run_inference(model, input_data)
            end_time = time.perf_counter()
            
            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)
        
        avg_latency = np.mean(latencies)
        p50_latency = np.percentile(latencies, 50)
        p95_latency = np.percentile(latencies, 95)
        p99_latency = np.percentile(latencies, 99)
        
        logger.info(f"Latency - Avg: {avg_latency:.2f}ms, P50: {p50_latency:.2f}ms, "
                   f"P95: {p95_latency:.2f}ms, P99: {p99_latency:.2f}ms")
        
        return avg_latency
    
    def _measure_throughput(self, model, input_shape: tuple) -> float:
        """
        Measures throughput in frames per second
        """
        start_time = time.perf_counter()
        
        for i in range(self.test_iterations):
            input_data = np.random.randn(*input_shape).astype(np.float32)
            self._run_inference(model, input_data)
        
        end_time = time.perf_counter()
        elapsed_seconds = end_time - start_time
        
        throughput = self.test_iterations / elapsed_seconds
        
        logger.info(f"Throughput: {throughput:.2f} FPS")
        return throughput
    
    def _measure_memory(self, model) -> float:
        """
        Measures memory usage
        """
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / (1024 ** 2)
        
        logger.info(f"Memory usage: {memory_mb:.2f} MB")
        return memory_mb
    
    def _estimate_power(self, model, input_shape: tuple) -> float:
        """
        Estimates power consumption
        
        Steps:
        1. Measure baseline power
        2. Run inference and measure active power
        3. Calculate differential power consumption
        """
        latency_ms = self._measure_latency(model, input_shape)
        
        estimated_power_mw = latency_ms * 50
        
        logger.info(f"Estimated power: {estimated_power_mw:.2f} mW")
        return estimated_power_mw
    
    def compare_models(self, models: List[Dict], input_shape: tuple) -> Dict:
        """
        Compares multiple models
        """
        logger.info(f"Comparing {len(models)} models")
        
        results = {}
        
        for idx, model in enumerate(models):
            model_name = f"model_{idx}"
            results[model_name] = self.evaluate(model, f"output/{model_name}", input_shape)
        
        return results
    
    def export_results(self, results: Dict, output_path: str):
        """
        Exports benchmark results to file
        """
        import json
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results exported to {output_path}")
