import time
import os
import platform
from typing import Dict, List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ThermalMonitor:
    """
    Monitors device thermal conditions
    Detects overheating and thermal throttling
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.threshold_celsius = config.get('profiling', {}).get('thermal_threshold_celsius', 45)
        self.thermal_zones = self._detect_thermal_zones()
        self.history = []
    
    def monitor(self, duration_seconds: float = 5.0) -> Dict:
        """
        Monitors thermal conditions
        
        Steps:
        1. Read temperature from thermal zones
        2. Track temperature over time
        3. Detect throttling events
        4. Return thermal analysis
        """
        logger.info(f"Monitoring thermal conditions for {duration_seconds}s")
        
        temperatures = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            temp = self.get_current_temperature()
            if temp is not None:
                temperatures.append({
                    'timestamp': time.time(),
                    'temperature_celsius': temp
                })
            time.sleep(0.1)
        
        analysis = self._analyze_thermal_data(temperatures)
        logger.info(f"Thermal analysis: {analysis}")
        
        return analysis
    
    def get_current_temperature(self) -> Optional[float]:
        """
        Gets current device temperature
        
        Steps:
        1. Read from thermal zone files (Linux/Android)
        2. Parse temperature value
        3. Return in celsius
        """
        if platform.system() == "Linux":
            for zone_path in self.thermal_zones:
                try:
                    with open(zone_path, 'r') as f:
                        temp_millidegrees = int(f.read().strip())
                        return temp_millidegrees / 1000.0
                except:
                    continue
        
        return self._simulate_temperature()
    
    def _simulate_temperature(self) -> float:
        """
        Simulates temperature reading for testing
        """
        base_temp = 35.0
        variation = np.random.normal(0, 2.0)
        return base_temp + variation
    
    def _detect_thermal_zones(self) -> List[str]:
        """
        Detects available thermal zones
        """
        zones = []
        
        if platform.system() == "Linux":
            thermal_dir = "/sys/class/thermal"
            if os.path.exists(thermal_dir):
                for i in range(10):
                    zone_path = f"{thermal_dir}/thermal_zone{i}/temp"
                    if os.path.exists(zone_path):
                        zones.append(zone_path)
        
        return zones
    
    def _analyze_thermal_data(self, temperatures: List[Dict]) -> Dict:
        """
        Analyzes thermal data
        
        Steps:
        1. Calculate temperature statistics
        2. Detect throttling events
        3. Calculate thermal headroom
        4. Generate warnings
        """
        if not temperatures:
            return {'status': 'no_data'}
        
        temps = [t['temperature_celsius'] for t in temperatures]
        
        mean_temp = np.mean(temps)
        max_temp = np.max(temps)
        min_temp = np.min(temps)
        
        throttling_detected = max_temp > self.threshold_celsius
        thermal_headroom = self.threshold_celsius - mean_temp
        
        if throttling_detected:
            status = 'throttling'
            warning = f"Temperature exceeded threshold: {max_temp:.1f}C > {self.threshold_celsius}C"
        elif mean_temp > self.threshold_celsius - 5:
            status = 'warning'
            warning = f"Approaching thermal limit: {mean_temp:.1f}C"
        else:
            status = 'normal'
            warning = None
        
        analysis = {
            'status': status,
            'mean_temperature_celsius': mean_temp,
            'max_temperature_celsius': max_temp,
            'min_temperature_celsius': min_temp,
            'threshold_celsius': self.threshold_celsius,
            'thermal_headroom_celsius': thermal_headroom,
            'throttling_detected': throttling_detected,
            'warning': warning,
            'samples_collected': len(temperatures)
        }
        
        return analysis
    
    def is_safe_for_inference(self) -> bool:
        """
        Checks if thermal conditions are safe for inference
        """
        temp = self.get_current_temperature()
        if temp is None:
            return True
        return temp < self.threshold_celsius
    
    def wait_for_cooling(self, target_temp: float = None, timeout_seconds: float = 30.0):
        """
        Waits for device to cool down
        
        Steps:
        1. Monitor temperature
        2. Wait until below target
        3. Timeout if takes too long
        """
        if target_temp is None:
            target_temp = self.threshold_celsius - 5
        
        logger.info(f"Waiting for cooling to {target_temp}C (timeout: {timeout_seconds}s)")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            temp = self.get_current_temperature()
            if temp is not None and temp < target_temp:
                logger.info(f"Cooled to {temp:.1f}C")
                return True
            time.sleep(1.0)
        
        logger.warning("Cooling timeout reached")
        return False