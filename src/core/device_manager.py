import psutil
import platform
import os
from typing import Dict, Optional
import subprocess

class DeviceManager:
    """
    Manages device resources and capabilities for ARM mobile devices
    """
    
    def __init__(self):
        self.device_info = self._gather_device_info()
        self.capabilities = self._assess_capabilities()
        
    def _gather_device_info(self) -> Dict:
        """
        Gathers comprehensive device information
        """
        info = {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(logical=False),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "total_memory_mb": psutil.virtual_memory().total / (1024 ** 2),
            "available_memory_mb": psutil.virtual_memory().available / (1024 ** 2),
        }
        
        if platform.system() == "Linux":
            info.update(self._get_linux_specific_info())
        elif platform.system() == "Darwin":
            info.update(self._get_ios_specific_info())
        
        return info
    
    def _get_linux_specific_info(self) -> Dict:
        """
        Gets Android/Linux-specific device information
        """
        linux_info = {}
        
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
                if "Hardware" in cpuinfo:
                    for line in cpuinfo.split("\n"):
                        if "Hardware" in line:
                            linux_info["hardware"] = line.split(":")[1].strip()
                            break
        except:
            pass
        
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = int(f.read().strip()) / 1000.0
                linux_info["temperature_celsius"] = temp
        except:
            linux_info["temperature_celsius"] = None
        
        return linux_info
    
    def _get_ios_specific_info(self) -> Dict:
        """
        Gets iOS-specific device information
        """
        ios_info = {}
        
        try:
            result = subprocess.run(
                ["sysctl", "-n", "hw.model"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                ios_info["model"] = result.stdout.strip()
        except:
            pass
        
        return ios_info
    
    def _assess_capabilities(self) -> Dict:
        """
        Assesses device capabilities for AI workloads
        """
        capabilities = {
            "supports_quantization": True,
            "supports_neon": "neon" in str(self.device_info).lower(),
            "supports_fp16": self.device_info.get("cpu_count", 0) >= 4,
            "supports_int8": True,
            "recommended_batch_size": self._calculate_recommended_batch_size(),
            "max_model_size_mb": self._calculate_max_model_size(),
        }
        
        return capabilities
    
    def _calculate_recommended_batch_size(self) -> int:
        """
        Calculates recommended batch size based on available memory
        """
        available_mb = self.device_info.get("available_memory_mb", 1024)
        
        if available_mb > 4096:
            return 8
        elif available_mb > 2048:
            return 4
        elif available_mb > 1024:
            return 2
        else:
            return 1
    
    def _calculate_max_model_size(self) -> int:
        """
        Calculates maximum recommended model size
        """
        available_mb = self.device_info.get("available_memory_mb", 1024)
        return int(available_mb * 0.3)
    
    def get_current_temperature(self) -> Optional[float]:
        """
        Gets current device temperature
        """
        if platform.system() == "Linux":
            try:
                with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                    return int(f.read().strip()) / 1000.0
            except:
                return None
        return None
    
    def get_battery_status(self) -> Dict:
        """
        Gets current battery status
        """
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "plugged_in": battery.power_plugged,
                    "time_left_seconds": battery.secsleft if battery.secsleft != -1 else None
                }
        except:
            pass
        
        return {
            "percent": None,
            "plugged_in": None,
            "time_left_seconds": None
        }
    
    def is_thermal_throttling(self, threshold_celsius: float = 45.0) -> bool:
        """
        Checks if device is thermal throttling
        """
        temp = self.get_current_temperature()
        if temp is not None:
            return temp > threshold_celsius
        return False