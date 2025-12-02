from src.iot_layer.device_connector import DeviceConnector
from src.iot_layer.sensor_fusion import SensorFusion
from src.iot_layer.tinyml_runtime import TinyMLRuntime

class IoTConnector:
    """
    Main interface for IoT device integration
    """
    
    def __init__(self, config_path: str = "config/device_config.yaml"):
        from src.core.utils import load_config
        self.config = load_config(config_path)
        
        self.device_connector = DeviceConnector(self.config)
        self.sensor_fusion = SensorFusion(self.config)
        self.tinyml_runtime = TinyMLRuntime(self.config)
    
    def connect_device(self, device_id: str, protocol: str = "BLE"):
        """
        Connects to an IoT device
        """
        return self.device_connector.connect(device_id, protocol)
    
    def get_sensor_data(self):
        """
        Gets fused sensor data
        """
        return self.sensor_fusion.get_fused_data()

__all__ = ["IoTConnector", "DeviceConnector", "SensorFusion", "TinyMLRuntime"]