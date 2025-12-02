# ARM Adaptive Intelligence Engine - API Documentation

## Model Compressor API

### Quantizer
```python
from src.model_compressor import Quantizer

quantizer = Quantizer(config)
result = quantizer.quantize(model_path, bits=4, method="symmetric")
```

**Parameters:**
- `model_path` (str): Path to model file
- `bits` (int): Quantization bit width (2, 3, or 4)
- `method` (str): Quantization method ("symmetric" or "asymmetric")

**Returns:**
- Dictionary containing quantized weights and parameters

### Pruner
```python
from src.model_compressor import Pruner

pruner = Pruner(config)
result = pruner.prune(model, ratio=0.3, method="magnitude")
```

**Parameters:**
- `model` (Dict): Model weights dictionary
- `ratio` (float): Pruning ratio (0.0 to 1.0)
- `method` (str): Pruning method ("magnitude" or "gradient")

**Returns:**
- Dictionary containing pruned weights and masks

## Runtime Inspector API

### Profiler
```python
from src.runtime_inspector import Profiler

profiler = Profiler(config)
results = profiler.profile(model, input_data, duration_seconds=5.0)
```

**Parameters:**
- `model`: Model to profile
- `input_data`: Input data for inference
- `duration_seconds` (float): Profiling duration

**Returns:**
- Dictionary containing CPU, GPU, NPU, and memory metrics

## Memory Engine API

### RAG Core
```python
from src.memory_engine import RAGCore

rag = RAGCore(embedding_engine, vector_store, query_engine)
doc_id = rag.index_document("document.pdf", "pdf")
results = rag.query("What is this about?", top_k=5)
```

**Methods:**
- `index_document(path, type)`: Indexes a document
- `query(text, top_k)`: Queries the knowledge base
- `delete_document(doc_id)`: Removes a document

## Battery Scheduler API

### Battery Predictor
```python
from src.battery_scheduler import BatteryPredictor

predictor = BatteryPredictor(config)
prediction = predictor.predict_drain(task_description)
```

**Parameters:**
- `task_description` (Dict): Task metadata including compute ops, memory, duration

**Returns:**
- Dictionary with estimated drain and safety status

## IoT Layer API

### Device Connector
```python
from src.iot_layer import DeviceConnector

connector = DeviceConnector(config)
connection = connector.connect("device_id", protocol="BLE")
data = connector.receive_data("device_id")
```

**Methods:**
- `connect(device_id, protocol)`: Connects to IoT device
- `send_data(device_id, data)`: Sends data to device
- `receive_data(device_id)`: Receives data from device

## Privacy Firewall API

### Privacy Sandbox
```python
from src.privacy_firewall import PrivacySandbox

sandbox = PrivacySandbox(config)
result = sandbox.execute(model_func, input_data, "inference")
```

**Parameters:**
- `model_func` (Callable): Model function to execute
- `input_data`: Input data
- `operation_type` (str): Operation type

**Returns:**
- Dictionary with execution results or error
