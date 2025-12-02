#!/bin/bash

echo "Installing ARM Adaptive Intelligence Engine dependencies..."

# Update package manager
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-dev build-essential
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install python3
fi

# Install Python dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install TensorFlow Lite
echo "Installing TensorFlow Lite..."
pip3 install tensorflow>=2.13.0

# Install ONNX Runtime
echo "Installing ONNX Runtime..."
pip3 install onnxruntime>=1.15.0

# Install PyTorch
echo "Installing PyTorch..."
pip3 install torch>=2.0.0

# Install transformers and quantization libraries
echo "Installing Transformers and quantization libraries..."
pip3 install transformers>=4.30.0
pip3 install peft>=0.4.0
pip3 install bitsandbytes>=0.41.0
pip3 install accelerate>=0.20.0

# Install vector database
echo "Installing ChromaDB..."
pip3 install chromadb>=0.4.0

# Install sentence transformers
echo "Installing Sentence Transformers..."
pip3 install sentence-transformers>=2.2.0

# Install audio processing libraries
echo "Installing audio processing libraries..."
pip3 install librosa>=0.10.0
pip3 install soundfile>=0.12.0

# Install computer vision libraries
echo "Installing computer vision libraries..."
pip3 install opencv-python>=4.8.0
pip3 install pillow>=10.0.0

# Install scientific computing libraries
echo "Installing scientific computing libraries..."
pip3 install numpy>=1.24.0
pip3 install scipy>=1.10.0
pip3 install pandas>=2.0.0
pip3 install scikit-learn>=1.3.0

# Install system monitoring
echo "Installing system monitoring libraries..."
pip3 install psutil>=5.9.0

# Install configuration management
echo "Installing configuration libraries..."
pip3 install pyyaml>=6.0

echo "All dependencies installed successfully!"
