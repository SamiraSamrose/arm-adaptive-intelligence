import psutil
import time
import threading
from typing import Dict, List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Profiler:
    """
    Profiles hardware resource utilization during model inference
    Monitors CPU, GPU, NPU, memory, and compute patterns
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.sample_rate_hz = config.get('profiling', {}).get('sample_rate_hz', 100)
        self.sample_interval = 1.0 / self.sample_rate_hz
        self.is_profiling = False
        self.profile_data = []
    
    def profile(self, model, input_data=None, duration_seconds: float = 5.0) -> Dict:
        """
        Profiles model execution
        
        Steps:
        1. Start background monitoring thread
        2. Run model inference
        3. Collect CPU/GPU/NPU metrics
        4. Aggregate and return results
        """
        logger.info(f"Starting profiling for {duration_seconds}s at {self.sample_rate_hz}Hz")
        
        self.profile_data = []
        self.is_profiling = True
        
        monitor_thread = threading.Thread(target=self._monitoring_loop)
        monitor_thread.start()
        
        start_time = time.time()
        inference_count = 0
        
        while time.time() - start_time < duration_seconds:
            if input_data is None:
                input_data = np.random.randn(1, 224, 224, 3).astype(np.float32)
            
            self._simulate_inference(model, input_data)
            inference_count += 1
        
        self.is_profiling = False
        monitor_thread.join()
        
        results = self._aggregate_profile_data(inference_count, duration_seconds)
        logger.info(f"Profiling complete: {inference_count} inferences in {duration_seconds}s")
        
        return results
    
    def _monitoring_loop(self):
        """
        Background monitoring loop collecting metrics at sample_rate
        """
        while self.is_profiling:
            sample = self._collect_sample()
            self.profile_data.append(sample)
            time.sleep(self.sample_interval)
    
    def _collect_sample(self) -> Dict:
        """
        Collects single sample of system metrics
        
        Steps:
        1. Read CPU utilization per core
        2. Read memory usage
        3. Estimate GPU/NPU usage
        4. Record timestamp
        """
        cpu_percent = psutil.cpu_percent(percpu=True)
        memory = psutil.virtual_memory()
        
        sample = {
            'timestamp': time.time(),
            'cpu_percent': cpu_percent,
            'cpu_avg': np.mean(cpu_percent),
            'memory_used_mb': memory.used / (1024 ** 2),
            'memory_percent': memory.percent,
            'gpu_utilization': self._get_gpu_utilization(),
            'npu_utilization': self._get_npu_utilization(),
        }
        
        return sample
    
    def _get_gpu_utilization(self) -> float:
        """
        Gets GPU utilization (simulated for ARM Mali/Adreno)
        """
        return np.random.uniform(20, 80)
    
    def _get_npu_utilization(self) -> float:
        """
        Gets NPU utilization (simulated for ARM Ethos/Neural Processing)
        """
        return np.random.uniform(10, 60)
    
    def _simulate_inference(self, model, input_data):
        """
        Simulates model inference
        """
        time.sleep(0.01)
    
    def _aggregate_profile_data(self, inference_count: int, duration: float) -> Dict:
        """
        Aggregates collected profile data
        
        Steps:
        1. Calculate statistics (mean, max, min, p95)
        2. Identify bottlenecks
        3. Calculate throughput
        4. Return comprehensive metrics
        """
        if not self.profile_data:
            return {}
        
        cpu_avgs = [s['cpu_avg'] for s in self.profile_data]
        memory_usages = [s['memory_used_mb'] for s in self.profile_data]
        gpu_utils = [s['gpu_utilization'] for s in self.profile_data]
        npu_utils = [s['npu_utilization'] for s in self.profile_data]
        
        results = {
            'duration_seconds': duration,
            'inference_count': inference_count,
            'throughput_fps': inference_count / duration,
            'cpu': {
                'mean': np.mean(cpu_avgs),
                'max': np.max(cpu_avgs),
                'min': np.min(cpu_avgs),
                'p95': np.percentile(cpu_avgs, 95)
            },
            'memory': {
                'mean_mb': np.mean(memory_usages),
                'max_mb': np.max(memory_usages),
                'min_mb': np.min(memory_usages)
            },
            'gpu': {
                'mean': np.mean(gpu_utils),
                'max': np.max(gpu_utils),
                'p95': np.percentile(gpu_utils, 95)
            },
            'npu': {
                'mean': np.mean(npu_utils),
                'max': np.max(npu_utils),
                'p95': np.percentile(npu_utils, 95)
            },
            'bottleneck': self._identify_bottleneck(cpu_avgs, gpu_utils, npu_utils)
        }
        
        return results
    
    def _identify_bottleneck(self, cpu_utils: List, gpu_utils: List, npu_utils: List) -> str:
        """
        Identifies primary bottleneck
        """
        avg_cpu = np.mean(cpu_utils)
        avg_gpu = np.mean(gpu_utils)
        avg_npu = np.mean(npu_utils)
        
        max_util = max(avg_cpu, avg_gpu, avg_npu)
        
        if max_util == avg_cpu:
            return "CPU"
        elif max_util == avg_gpu:
            return "GPU"
        else:
            return "NPU"
    
    def profile_operator(self, operator_func, input_data, iterations: int = 100) -> Dict:
        """
        Profiles individual operator performance
        
        Steps:
        1. Run operator multiple times
        2. Measure execution time per iteration
        3. Return statistics
        """
        logger.info(f"Profiling operator: {iterations} iterations")
        
        latencies = []
        
        for i in range(iterations):
            start = time.perf_counter()
            operator_func(input_data)
            end = time.perf_counter()
            latencies.append((end - start) * 1000)
        
        return {
            'mean_ms': np.mean(latencies),
            'median_ms': np.median(latencies),
            'p95_ms': np.percentile(latencies, 95),
            'p99_ms': np.percentile(latencies, 99),
            'min_ms': np.min(latencies),
            'max_ms': np.max(latencies)
        }