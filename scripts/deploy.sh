#!/bin/bash

echo "Deploying ARM Adaptive Intelligence Engine..."

# Create deployment directories
mkdir -p deployment/models
mkdir -p deployment/config
mkdir -p deployment/data

# Copy Python source
echo "Copying source files..."
cp -r src deployment/

# Copy configuration files
echo "Copying configuration files..."
cp -r config deployment/

# Copy models
echo "Copying models..."
cp -r models deployment/

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv deployment/venv
source deployment/venv/bin/activate

# Install dependencies in venv
echo "Installing dependencies in deployment environment..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
python -m pytest tests/

# Package application
echo "Packaging application..."
python setup.py sdist bdist_wheel

echo "Deployment complete!"
echo "Deployment package available in: deployment/"
