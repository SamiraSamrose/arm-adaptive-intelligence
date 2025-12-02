#!/bin/bash

set -e

echo "Installing ARM Adaptive Intelligence Engine"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install package
echo "Installing ARM Adaptive Intelligence Engine..."
pip install -e .

# Create necessary directories
echo "Creating directories..."
mkdir -p models/compressed
mkdir -p models/quantized
mkdir -p models/pretrained
mkdir -p data/benchmarks
mkdir -p data/profiles
mkdir -p data/cache

# Run tests
echo "Running tests..."
python -m pytest tests/ -v

echo ""
echo "Installation complete!"
echo "=========================================="
echo "To activate the environment, run: source venv/bin/activate"
echo "To run the example, run: python example_usage.py"
