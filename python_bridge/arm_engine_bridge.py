from flask import Flask, request, jsonify
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.model_compressor import ModelCompressor
from src.runtime_inspector import RuntimeInspector
from src.memory_engine import MemoryEngine
from src.battery_scheduler import BatteryScheduler
from src.iot_layer import IoTConnector
from src.privacy_firewall import PrivacyFirewall

app = Flask(__name__)

compressor = None
inspector = None
memory_engine = None
scheduler = None
iot_connector = None
firewall = None

@app.route('/initialize', methods=['POST'])
def initialize():
    """
    Initializes all engine components
    """
    global compressor, inspector, memory_engine, scheduler, iot_connector, firewall
    
    try:
        compressor = ModelCompressor()
        inspector = RuntimeInspector()
        memory_engine = MemoryEngine()
        scheduler = BatteryScheduler()
        iot_connector = IoTConnector()
        firewall = PrivacyFirewall()
        
        return jsonify({
            'success': True,
            'message': 'Engine initialized successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Initialization failed: {str(e)}'
        }), 500

@app.route('/compress_model', methods=['POST'])
def compress_model_endpoint():
    """
    Compresses a model
    """
    data = request.json
    model_path = data.get('model_path')
    output_path = data.get('output_path')
    bits = data.get('bits', 4)
    
    try:
        result = compressor.compress_model(model_path, output_path, bits)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/index_document', methods=['POST'])
def index_document_endpoint():
    """
    Indexes a document
    """
    data = request.json
    document_path = data.get('document_path')
    document_type = data.get('document_type', 'auto')
    
    try:
        result = memory_engine.index_document(document_path, document_type)
        return jsonify({
            'success': True,
            'document_id': result['document_id']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/query', methods=['POST'])
def query_endpoint():
    """
    Queries the memory engine
    """
    data = request.json
    query_text = data.get('query')
    top_k = data.get('top_k', 5)
    
    try:
        result = memory_engine.query(query_text, top_k)
        return jsonify({
            'success': True,
            'response': result['response'],
            'sources': result['sources']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Gets performance metrics
    """
    try:
        metrics = inspector.profiler.profile(None, duration_seconds=0.1)
        return jsonify({
            'success': True,
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
