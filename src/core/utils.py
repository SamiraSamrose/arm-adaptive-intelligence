import yaml
import json
import os
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path: str) -> Dict:
    """
    Loads configuration from YAML file
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        return {}

def save_config(config: Dict, config_path: str) -> bool:
    """
    Saves configuration to YAML file
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        logger.info(f"Configuration saved to {config_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save config to {config_path}: {e}")
        return False

def get_device_info() -> Dict:
    """
    Gets device information summary
    """
    from src.core.device_manager import DeviceManager
    manager = DeviceManager()
    return manager.device_info

def ensure_directory(path: str) -> None:
    """
    Ensures directory exists
    """
    os.makedirs(path, exist_ok=True)

def get_model_size_mb(model_path: str) -> float:
    """
    Gets model file size in megabytes
    """
    if os.path.exists(model_path):
        size_bytes = os.path.getsize(model_path)
        return size_bytes / (1024 ** 2)
    return 0.0

def calculate_compression_ratio(original_size: float, compressed_size: float) -> float:
    """
    Calculates compression ratio
    """
    if original_size == 0:
        return 0.0
    return (original_size - compressed_size) / original_size * 100

def format_bytes(bytes_val: int) -> str:
    """
    Formats bytes into human-readable format
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} TB"