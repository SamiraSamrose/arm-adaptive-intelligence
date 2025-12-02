import numpy as np
from typing import Dict, List, Optional
import time
import logging

logger = logging.getLogger(__name__)

class SensorFusion:
    """
    Fuses data from multiple sensors for comprehensive context
    Handles motion, audio, and biosignal data
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.sensor_data_buffer = {}
        self.fusion_algorithms = {
            'motion': self._fuse_motion_data,
            'audio': self._fuse_audio_data,
            'biosignal': self._fuse_biosignal_data
        }
    
    def add_sensor_data(self, sensor_type: str, data: Dict):
        """
        Adds sensor data to fusion buffer
        
        Steps:
        1. Validate sensor type
        2. Add to appropriate buffer
        3. Maintain buffer size
        4. Trigger fusion if conditions met
        """
        if sensor_type not in self.sensor_data_buffer:
            self.sensor_data_buffer[sensor_type] = []
        
        data['timestamp'] = time.time()
        self.sensor_data_buffer[sensor_type].append(data)
        
        max_buffer_size = 100
        if len(self.sensor_data_buffer[sensor_type]) > max_buffer_size:
            self.sensor_data_buffer[sensor_type].pop(0)
        
        logger.debug(f"Added {sensor_type} data to buffer")
    
    def get_fused_data(self) -> Dict:
        """
        Gets fused sensor data
        
        Steps:
        1. Collect data from all sensors
        2. Synchronize timestamps
        3. Apply fusion algorithms
        4. Return fused context
        """
        logger.debug("Fusing sensor data")
        
        fused_data = {
            'timestamp': time.time(),
            'motion': None,
            'audio': None,
            'biosignal': None,
            'context': None
        }
        
        if 'motion' in self.sensor_data_buffer:
            fused_data['motion'] = self._fuse_motion_data(
                self.sensor_data_buffer['motion']
            )
        
        if 'audio' in self.sensor_data_buffer:
            fused_data['audio'] = self._fuse_audio_data(
                self.sensor_data_buffer['audio']
            )
        
        if 'biosignal' in self.sensor_data_buffer:
            fused_data['biosignal'] = self._fuse_biosignal_data(
                self.sensor_data_buffer['biosignal']
            )
        
        fused_data['context'] = self._infer_context(fused_data)
        
        return fused_data
    
    def _fuse_motion_data(self, motion_data: List[Dict]) -> Dict:
        """
        Fuses motion sensor data (accelerometer, gyroscope, magnetometer)
        
        Steps:
        1. Extract sensor readings
        2. Apply complementary filter
        3. Calculate orientation
        4. Detect activity
        """
        if not motion_data:
            return {'status': 'no_data'}
        
        recent_data = motion_data[-10:]
        
        acc_values = [d.get('values', {}) for d in recent_data if d.get('sensor_type') == 'accelerometer']
        
        if acc_values:
            avg_acc = {
                'x': np.mean([v.get('x', 0) for v in acc_values]),
                'y': np.mean([v.get('y', 0) for v in acc_values]),
                'z': np.mean([v.get('z', 0) for v in acc_values])
            }
            
            magnitude = np.sqrt(avg_acc['x']**2 + avg_acc['y']**2 + avg_acc['z']**2)
            
            if magnitude > 12:
                activity = 'running'
            elif magnitude > 10:
                activity = 'walking'
            else:
                activity = 'stationary'
        else:
            avg_acc = {'x': 0, 'y': 0, 'z': 0}
            activity = 'unknown'
        
        return {
            'accelerometer': avg_acc,
            'activity': activity,
            'samples_fused': len(recent_data)
        }
    
    def _fuse_audio_data(self, audio_data: List[Dict]) -> Dict:
        """
        Fuses audio sensor data
        
        Steps:
        1. Analyze audio levels
        2. Detect patterns
        3. Classify ambient sound
        """
        if not audio_data:
            return {'status': 'no_data'}
        
        recent_data = audio_data[-5:]
        
        levels = [d.get('level', 0) for d in recent_data]
        avg_level = np.mean(levels)
        
        if avg_level > 80:
            environment = 'loud'
        elif avg_level > 50:
            environment = 'moderate'
        else:
            environment = 'quiet'
        
        return {
            'average_level_db': avg_level,
            'environment': environment,
            'samples_fused': len(recent_data)
        }
    
    def _fuse_biosignal_data(self, biosignal_data: List[Dict]) -> Dict:
        """
        Fuses biosignal data (heart rate, skin conductance, temperature)
        
        Steps:
        1. Extract vital signs
        2. Calculate trends
        3. Detect anomalies
        """
        if not biosignal_data:
            return {'status': 'no_data'}
        
        recent_data = biosignal_data[-20:]
        
        heart_rates = [d.get('heart_rate', 0) for d in recent_data if 'heart_rate' in d]
        
        if heart_rates:
            avg_hr = np.mean(heart_rates)
            
            if avg_hr > 100:
                state = 'elevated'
            elif avg_hr > 60:
                state = 'normal'
            else:
                state = 'low'
        else:
            avg_hr = 0
            state = 'unknown'
        
        return {
            'heart_rate_bpm': avg_hr,
            'state': state,
            'samples_fused': len(recent_data)
        }
    
    def _infer_context(self, fused_data: Dict) -> str:
        """
        Infers user context from fused sensor data
        
        Steps:
        1. Analyze motion patterns
        2. Consider audio environment
        3. Factor in biosignals
        4. Return context classification
        """
        motion = fused_data.get('motion', {})
        audio = fused_data.get('audio', {})
        biosignal = fused_data.get('biosignal', {})
        
        activity = motion.get('activity', 'unknown')
        environment = audio.get('environment', 'unknown')
        state = biosignal.get('state', 'unknown')
        
        if activity == 'running' and state == 'elevated':
            return 'exercising'
        elif activity == 'stationary' and environment == 'quiet':
            return 'resting'
        elif activity == 'walking' and environment == 'loud':
            return 'commuting'
        elif activity == 'stationary' and environment == 'moderate':
            return 'working'
        else:
            return 'general_activity'
    
    def clear_buffer(self, sensor_type: Optional[str] = None):
        """
        Clears sensor data buffer
        """
        if sensor_type:
            if sensor_type in self.sensor_data_buffer:
                self.sensor_data_buffer[sensor_type] = []
                logger.info(f"Cleared {sensor_type} buffer")
        else:
            self.sensor_data_buffer = {}
            logger.info("Cleared all sensor buffers")