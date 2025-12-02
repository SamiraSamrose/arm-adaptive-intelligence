import numpy as np
import torch
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class Pruner:
    """
    Prunes neural network models to reduce parameters and improve efficiency
    Implements structured and unstructured pruning
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.default_ratio = config.get('compression', {}).get('pruning_ratio', 0.3)
    
    def prune(self, model: Dict, ratio: float = None, 
              method: str = "magnitude") -> Dict:
        """
        Prunes model weights
        
        Steps:
        1. Analyze weight magnitudes
        2. Identify weights to prune based on method
        3. Apply pruning mask
        4. Return pruned model
        """
        if ratio is None:
            ratio = self.default_ratio
        
        logger.info(f"Starting pruning: {ratio*100:.1f}% removal using {method} method")
        
        pruned_model = {}
        pruning_masks = {}
        
        if isinstance(model, dict) and "quantized_weights" in model:
            weights = model["quantized_weights"]
        else:
            weights = model
        
        for layer_name, weight_tensor in weights.items():
            pruned_weight, mask = self._prune_layer(weight_tensor, ratio, method)
            pruned_model[layer_name] = pruned_weight
            pruning_masks[layer_name] = mask
        
        sparsity = self._calculate_sparsity(pruned_model)
        logger.info(f"Pruning complete. Sparsity: {sparsity*100:.2f}%")
        return {
        "pruned_weights": pruned_model,
        "pruning_masks": pruning_masks,
        "sparsity": sparsity,
        "pruning_ratio": ratio
        }

    def _prune_layer(self, weights: np.ndarray, ratio: float, method: str) -> tuple:
    """
    Prunes a single layer
    
    Steps:
    1. Calculate importance scores
    2. Determine threshold
    3. Create pruning mask
    4. Apply mask to weights
    """
    if isinstance(weights, torch.Tensor):
        weights = weights.numpy()
    
    if method == "magnitude":
        importance = np.abs(weights)
    elif method == "gradient":
        importance = np.abs(weights) * np.random.rand(*weights.shape)
    else:
        importance = np.abs(weights)
    
    threshold = np.percentile(importance, ratio * 100)
    
    mask = importance > threshold
    
    pruned_weights = weights * mask
    
    return pruned_weights, mask

def structured_pruning(self, model: Dict, ratio: float, 
                      granularity: str = "channel") -> Dict:
    """
    Performs structured pruning at channel or filter level
    
    Steps:
    1. Calculate channel/filter importance
    2. Remove least important structures
    3. Reconstruct model with reduced dimensions
    """
    logger.info(f"Structured pruning: {granularity} level, ratio={ratio}")
    
    pruned_model = {}
    
    for layer_name, weights in model.items():
        if len(weights.shape) == 4:
            pruned_model[layer_name] = self._prune_conv_layer(weights, ratio, granularity)
        elif len(weights.shape) == 2:
            pruned_model[layer_name] = self._prune_dense_layer(weights, ratio)
        else:
            pruned_model[layer_name] = weights
    
    return pruned_model

def _prune_conv_layer(self, weights: np.ndarray, ratio: float, granularity: str) -> np.ndarray:
    """
    Prunes convolutional layer filters or channels
    """
    if granularity == "channel":
        channel_importance = np.sum(np.abs(weights), axis=(0, 2, 3))
        num_keep = int(len(channel_importance) * (1 - ratio))
        keep_indices = np.argsort(channel_importance)[-num_keep:]
        return weights[:, keep_indices, :, :]
    else:
        filter_importance = np.sum(np.abs(weights), axis=(1, 2, 3))
        num_keep = int(len(filter_importance) * (1 - ratio))
        keep_indices = np.argsort(filter_importance)[-num_keep:]
        return weights[keep_indices, :, :, :]

def _prune_dense_layer(self, weights: np.ndarray, ratio: float) -> np.ndarray:
    """
    Prunes dense layer neurons
    """
    neuron_importance = np.sum(np.abs(weights), axis=0)
    num_keep = int(len(neuron_importance) * (1 - ratio))
    keep_indices = np.argsort(neuron_importance)[-num_keep:]
    return weights[:, keep_indices]

def _calculate_sparsity(self, model: Dict) -> float:
    """
    Calculates overall model sparsity
    """
    total_params = 0
    zero_params = 0
    
    for weights in model.values():
        if isinstance(weights, torch.Tensor):
            weights = weights.numpy()
        total_params += weights.size
        zero_params += np.sum(weights == 0)
    
    return zero_params / total_params if total_params > 0 else 0.0

def iterative_pruning(self, model: Dict, target_ratio: float, 
                     steps: int = 5) -> Dict:
    """
    Gradually prunes model over multiple iterations
    """
    logger.info(f"Iterative pruning: target={target_ratio}, steps={steps}")
    
    current_model = model
    step_ratio = target_ratio / steps
    
    for step in range(steps):
        logger.info(f"Pruning step {step + 1}/{steps}")
        current_model = self.prune(current_model, ratio=step_ratio)
    
    return current_model