import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.model_compressor import ModelCompressor
from src.runtime_inspector import RuntimeInspector
from src.core.device_manager import DeviceManager

def run_comprehensive_benchmark(model_path: str, output_dir: str):
    """
    Runs comprehensive benchmark suite
    """
    print("Starting comprehensive benchmark...")
    print("=" * 60)
    
    os.makedirs(output_dir, exist_ok=True)
    
    device_manager = DeviceManager()
    compressor = ModelCompressor()
    inspector = RuntimeInspector()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "device_info": device_manager.device_info,
        "benchmarks": {}
    }
    
    # Benchmark 1: Original model
    print("\n1. Benchmarking original model...")
    original_metrics = inspector.profiler.profile(None, duration_seconds=5.0)
    results["benchmarks"]["original"] = original_metrics
    
    # Benchmark 2: Quantized models
    print("\n2. Benchmarking quantized models...")
    for bits in [4, 3, 2]:
        print(f"   Testing {bits}-bit quantization...")
        quant_result = compressor.quantizer.quantize({"layer1": [[0.5]]}, bits=bits)
        results["benchmarks"][f"quantized_{bits}bit"] = {
            "compression_ratio": quant_result["compression_ratio"],
            "bits": bits
        }
    
    # Benchmark 3: Thermal profile
    print("\n3. Running thermal benchmark...")
    thermal_data = inspector.thermal_monitor.monitor(duration_seconds=10.0)
    results["benchmarks"]["thermal"] = thermal_data
    
    # Save results
    output_path = os.path.join(output_dir, f"benchmark_{int(time.time())}.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"Benchmark complete! Results saved to: {output_path}")
    
    return results

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run comprehensive benchmarks')
    parser.add_argument('--model', required=True, help='Path to model file')
    parser.add_argument('--output', default='data/benchmarks', help='Output directory')
    
    args = parser.parse_args()
    
    run_comprehensive_benchmark(args.model, args.output)
