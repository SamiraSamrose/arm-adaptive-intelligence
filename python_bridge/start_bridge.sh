#!/bin/bash

echo "Starting Python Bridge for ARM Engine..."

# Install requirements
pip3 install -r requirements.txt

# Start Flask server
python3 arm_engine_bridge.py
