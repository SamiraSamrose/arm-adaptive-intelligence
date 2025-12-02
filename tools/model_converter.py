import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def convert_pytorch_to_onnx(pytorch_model_path: str, output_path: str):
    """
    Converts PyTorch model to ONNX format
    """
    import torch
    import torch.onnx
    
    print(f"Converting {pytorch_model_path} to ONNX...")
    
    model = torch.load(pytorch_model_path)
    model.eval()
    
    dummy_input = torch.randn(1, 3, 224, 224)
    
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=13,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print(f"Model converted and saved to {output_path}")

def convert_onnx_to_tflite(onnx_model_path: str, output_path: str):
    """
    Converts ONNX model to TensorFlow Lite format
    """
    import onnx
    from onnx_tf.backend import prepare
    import tensorflow as tf
    
    print(f"Converting {onnx_model_path} to TFLite...")
    
    onnx_model = onnx.load(onnx_model_path)
    tf_rep = prepare(onnx_model)
    
    converter = tf.lite.TFLiteConverter.from_saved_model(tf_rep.export_graph())
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()
    
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"Model converted and saved to {output_path}")

def main():
    """
    Main conversion function
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert models between formats')
    parser.add_argument('--input', required=True, help='Input model path')
    parser.add_argument('--output', required=True, help='Output model path')
    parser.add_argument('--format', required=True, choices=['onnx', 'tflite', 'coreml'],
                       help='Target format')
    
    args = parser.parse_args()
    
    if args.format == 'onnx':
        convert_pytorch_to_onnx(args.input, args.output)
    elif args.format == 'tflite':
        convert_onnx_to_tflite(args.input, args.output)
    else:
        print(f"Conversion to {args.format} not yet implemented")

if name == 'main':
main()