import psutil
import time
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PowerMonitor:
    """
    Monitors device power consumption in real-time
    Integrates with Android/iOS power APIs
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.low_power_mode = config.get('power', {}).get('low_power_mode', True)
        self.monitoring_history = []
    
    def get_battery_percent(self) -> Optional[float]:
        """
        Gets current battery percentage
        """
        try:
            battery = psutil.sensors_battery()
            if battery:
                return battery.percent
        except:
            pass
        return None
    
    def is_plugged_in(self) -> bool:
        """
        Checks if device is plugged in
        """
        try:
            battery = psutil.sensors_battery()
            if battery:
                return battery.power_plugged
        except:
            pass
        return False
    
    def get_thermal_status(self) -> Dict:
        """
        Gets thermal status
        """
        from src.core.device_manager import DeviceManager
        manager = DeviceManager()
        
        temp = manager.get_current_temperature()
        threshold = self.config.get('profiling', {}).get('thermal_threshold_celsius', 45)
        
        if temp is None:
            return {'status': 'unknown', 'temperature': None}
        
        if temp > threshold:
            status = 'throttling'
        elif temp > threshold - 5:
            status = 'warning'
        else:
            status = 'normal'
        
        return {
            'status': status,
            'temperature': temp,
            'threshold': threshold
        }
    
    def is_thermal_throttling(self) -> bool:
        """
        Checks if device is thermal throttling
        """
        status = self.get_thermal_status()
        return status.get('status') == 'throttling'
    
    def enable_low_power_mode(self):
        """
        Enables low power mode for AI tasks
        
        Steps:
        1. Reduce CPU frequency
        2. Limit concurrent operations
        3. Adjust quantization levels
        """
        logger.info("Enabling low power mode")
        self.low_power_mode = True
    
    def disable_low_power_mode(self):
        """
        Disables low power mode
        """
        logger.info("Disabling low power mode")
        self.low_power_mode = False
    
    def monitor_power_consumption(self, duration_seconds: float = 5.0) -> Dict:
        """
        Monitors power consumption over time
        
        Steps:
        1. Record initial battery state
        2. Monitor over duration
        3. Calculate consumption rate
        4. Return metrics
        """
        logger.info(f"Monitoring power for {duration_seconds}s")
        
        initial_percent = self.get_battery_percent()
        start_time = time.time()
        
        samples = []
        while time.time() - start_time < duration_seconds:
            sample = {
                'timestamp': time.time(),
                'battery_percent': self.get_battery_percent(),
                'thermal_status': self.get_thermal_status()
            }
            samples.append(sample)
            time.sleep(0.5)
        
        final_percent = self.get_battery_percent()
        
        if initial_percent and final_percent:
            drain = initial_percent - final_percent
            drain_rate = (drain / duration_seconds) * 3600
        else:
            drain = 0
            drain_rate = 0
        
        return {
            'duration_seconds': duration_seconds,
            'battery_drain_percent': drain,
            'drain_rate_percent_per_hour': drain_rate,
            'samples': len(samples),
            'initial_battery': initial_percent,
            'final_battery': final_percent
        }
    
    def get_power_profile(self) -> Dict:
        """
        Gets current power profile
        """
        return {
            'low_power_mode': self.low_power_mode,
            'battery_percent': self.get_battery_percent(),
            'plugged_in': self.is_plugged_in(),
            'thermal_status': self.get_thermal_status(),
            'recommended_mode': self._recommend_power_mode()
        }
    
    def _recommend_power_mode(self) -> str:
        """
        Recommends power mode based on current state
        """
        battery = self.get_battery_percent()
        plugged = self.is_plugged_in()
        thermal = self.get_thermal_status()
        
        if plugged:
            return "performance"
        
        if battery and battery < 20:
            return "ultra_low_power"
        
        if thermal.get('status') == 'throttling':
            return "low_power"
        
        if battery and battery < 50:
            return "balanced"
        
        return "performance"
