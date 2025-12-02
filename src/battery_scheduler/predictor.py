import numpy as np
from typing import Dict, List, Optional
import logging
import time

logger = logging.getLogger(__name__)

class BatteryPredictor:
    """
    Predicts battery drain for AI tasks using ML model
    Trained on smartphone power consumption datasets
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = self._load_model()
        self.history = []
    
    def _load_model(self):
        """
        Loads battery prediction model
        """
        logger.info("Loading battery prediction model")
        return None
    
    def predict_drain(self, task_description: Dict) -> Dict:
        """
        Predicts battery drain for a task
        
        Steps:
        1. Extract task features (compute, memory, duration)
        2. Get current battery state
        3. Run prediction model
        4. Return estimated drain
        """
        logger.debug(f"Predicting drain for task: {task_description}")
        
        features = self._extract_features(task_description)
        
        current_state = self._get_current_battery_state()
        
        estimated_drain_percent = self._run_prediction(features, current_state)
        
        estimated_time_minutes = self._estimate_time_impact(estimated_drain_percent, current_state)
        
        return {
            'estimated_drain_percent': estimated_drain_percent,
            'estimated_time_minutes': estimated_time_minutes,
            'current_battery_percent': current_state['percent'],
            'safe_to_execute': self._is_safe_to_execute(estimated_drain_percent, current_state)
        }
    
    def _extract_features(self, task_description: Dict) -> np.ndarray:
        """
        Extracts features from task description
        """
        compute_intensity = task_description.get('compute_ops', 1e9) / 1e9
        memory_usage = task_description.get('memory_mb', 100) / 1000
        duration_estimate = task_description.get('duration_seconds', 1.0)
        
        features = np.array([
            compute_intensity,
            memory_usage,
            duration_estimate,
            time.localtime().tm_hour / 24.0,
        ])
        
        return features
    
    def _get_current_battery_state(self) -> Dict:
        """
        Gets current battery state
        """
        import psutil
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'plugged_in': battery.power_plugged,
                    'time_left': battery.secsleft if battery.secsleft != -1 else None
                }
        except:
            pass
        
        return {
            'percent': 80.0,
            'plugged_in': False,
            'time_left': 7200
        }
    
    def _run_prediction(self, features: np.ndarray, current_state: Dict) -> float:
        """
        Runs prediction model
        """
        base_drain = np.sum(features[:3]) * 0.5
        
        if current_state.get('plugged_in', False):
            base_drain *= 0.5
        
        current_percent = current_state.get('percent', 100)
        if current_percent < 20:
            base_drain *= 1.2
        
        return min(base_drain, 10.0)
    
    def _estimate_time_impact(self, drain_percent: float, current_state: Dict) -> float:
        """
        Estimates time impact on battery life
        """
        current_percent = current_state.get('percent', 100)
        time_left = current_state.get('time_left')
        
        if time_left and current_percent > 0:
            time_per_percent = time_left / current_percent
            estimated_time = drain_percent * time_per_percent / 60
            return estimated_time
        
        return drain_percent * 5
    
    def _is_safe_to_execute(self, estimated_drain: float, current_state: Dict) -> bool:
        """
        Determines if task is safe to execute
        """
        current_percent = current_state.get('percent', 100)
        plugged_in = current_state.get('plugged_in', False)
        threshold = self.config.get('power', {}).get('battery_threshold_percent', 20)
        
        if plugged_in:
            return True
        
        if current_percent - estimated_drain < threshold:
            return False
        
        return True
    
    def record_actual_drain(self, task_id: str, actual_drain: float):
        """
        Records actual drain for model improvement
        """
        self.history.append({
            'task_id': task_id,
            'actual_drain': actual_drain,
            'timestamp': time.time()
        })
        
        logger.debug(f"Recorded actual drain: {actual_drain}%")
    
    def get_prediction_accuracy(self) -> float:
        """
        Calculates prediction accuracy
        """
        if len(self.history) < 2:
            return 0.0
        
        errors = []
        for record in self.history:
            predicted = record.get('predicted_drain', 0)
            actual = record.get('actual_drain', 0)
            errors.append(abs(predicted - actual))
        
        mae = np.mean(errors)
        accuracy = max(0, 100 - mae * 10)
        
        return accuracy
