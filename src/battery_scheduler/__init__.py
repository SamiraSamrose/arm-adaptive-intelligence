from src.battery_scheduler.predictor import BatteryPredictor
from src.battery_scheduler.scheduler import AIScheduler
from src.battery_scheduler.power_monitor import PowerMonitor

class BatteryScheduler:
    """
    Main interface for battery-aware AI scheduling
    """
    
    def __init__(self, config_path: str = "config/device_config.yaml"):
        from src.core.utils import load_config
        self.config = load_config(config_path)
        
        self.predictor = BatteryPredictor(self.config)
        self.power_monitor = PowerMonitor(self.config)
        self.scheduler = AIScheduler(self.config, self.predictor, self.power_monitor)
    
    def schedule_task(self, task_func, priority: str = "normal"):
        """
        Schedules an AI task with battery awareness
        """
        return self.scheduler.schedule(task_func, priority)
    
    def get_optimal_time(self):
        """
        Gets optimal time for running AI tasks
        """
        return self.scheduler.get_optimal_execution_time()

__all__ = ["BatteryScheduler", "BatteryPredictor", "AIScheduler", "PowerMonitor"]
