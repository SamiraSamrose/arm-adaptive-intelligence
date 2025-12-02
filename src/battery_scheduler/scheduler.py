import time
import threading
from typing import Dict, List, Callable, Optional
from queue import PriorityQueue
import logging

logger = logging.getLogger(__name__)

class AIScheduler:
    """
    Schedules AI tasks with battery awareness
    Uses hybrid ML predictions and symbolic rules
    """
    
    def __init__(self, config: Dict, predictor, power_monitor):
        self.config = config
        self.predictor = predictor
        self.power_monitor = power_monitor
        self.task_queue = PriorityQueue()
        self.adaptive_mode = config.get('power', {}).get('adaptive_scheduling', True)
        self.is_running = False
        self.scheduler_thread = None
    
    def start(self):
        """
        Starts the scheduler
        """
        if not self.is_running:
            self.is_running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
            self.scheduler_thread.start()
            logger.info("AI Scheduler started")
    
    def stop(self):
        """
        Stops the scheduler
        """
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        logger.info("AI Scheduler stopped")
    
    def schedule(self, task_func: Callable, priority: str = "normal", 
                task_description: Optional[Dict] = None) -> str:
        """
        Schedules an AI task
        
        Steps:
        1. Predict battery drain
        2. Check if safe to execute
        3. Apply symbolic rules
        4. Add to queue with priority
        5. Return task ID
        """
        task_id = f"task_{int(time.time() * 1000)}"
        
        if task_description is None:
            task_description = {
                'compute_ops': 1e9,
                'memory_mb': 100,
                'duration_seconds': 1.0
            }
        
        prediction = self.predictor.predict_drain(task_description)
        
        should_execute, reason = self._apply_scheduling_rules(prediction, priority)
        
        priority_value = self._calculate_priority(priority, prediction)
        
        task = {
            'id': task_id,
            'func': task_func,
            'description': task_description,
            'prediction': prediction,
            'priority': priority_value,
            'should_execute': should_execute,
            'reason': reason,
            'scheduled_time': time.time()
        }
        
        self.task_queue.put((priority_value, task))
        
        logger.info(f"Task scheduled: {task_id}, priority={priority_value}, executable={should_execute}")
        
        return task_id
    
    def _apply_scheduling_rules(self, prediction: Dict, priority: str) -> tuple:
        """
        Applies symbolic scheduling rules
        
        Rules:
        1. Always execute if plugged in
        2. Defer if battery < threshold unless critical
        3. Execute during low-load windows
        4. Throttle during thermal issues
        """
        battery_state = prediction
        
        if battery_state.get('current_battery_percent', 100) < 20 and priority != "critical":
            return False, "Battery below threshold"
        
        if not prediction.get('safe_to_execute', True) and priority != "critical":
            return False, "Predicted drain too high"
        
        thermal_safe = not self.power_monitor.is_thermal_throttling()
        if not thermal_safe and priority != "critical":
            return False, "Thermal throttling detected"
        
        if priority == "critical":
            return True, "Critical priority overrides constraints"
        
        return True, "All checks passed"
    
    def _calculate_priority(self, priority_str: str, prediction: Dict) -> int:
        """
        Calculates numeric priority value
        """
        priority_map = {
            'critical': 0,
            'high': 10,
            'normal': 50,
            'low': 100
        }
        
        base_priority = priority_map.get(priority_str, 50)
        
        if prediction.get('safe_to_execute', True):
            base_priority -= 5
        
        return base_priority
    
    def _scheduler_loop(self):
        """
        Main scheduler loop
        """
        while self.is_running:
            if not self.task_queue.empty():
                priority, task = self.task_queue.get()
                
                if task['should_execute']:
                    self._execute_task(task)
                else:
                    logger.info(f"Task deferred: {task['id']}, reason: {task['reason']}")
                    
                    if self._should_retry(task):
                        time.sleep(60)
                        self.task_queue.put((priority + 1, task))
            
            time.sleep(1)
    
    def _execute_task(self, task: Dict):
        """
        Executes a scheduled task
        """
        task_id = task['id']
        logger.info(f"Executing task: {task_id}")
        
        start_time = time.time()
        battery_before = self.power_monitor.get_battery_percent()
        
        try:
            task['func']()
        except Exception as e:
            logger.error(f"Task execution failed: {task_id}, error: {e}")
        
        end_time = time.time()
        battery_after = self.power_monitor.get_battery_percent()
        
        actual_drain = battery_before - battery_after if battery_before and battery_after else 0
        execution_time = end_time - start_time
        
        self.predictor.record_actual_drain(task_id, actual_drain)
        
        logger.info(f"Task completed: {task_id}, time={execution_time:.2f}s, drain={actual_drain:.2f}%")
    
    def _should_retry(self, task: Dict) -> bool:
        """
        Determines if task should be retried
        """
        return task.get('priority', 100) < 50
    
    def get_optimal_execution_time(self) -> Dict:
        """
        Gets optimal time window for AI tasks
        
        Steps:
        1. Analyze current battery state
        2. Check thermal conditions
        3. Predict load patterns
        4. Return recommended time window
        """
        battery_state = self.predictor._get_current_battery_state()
        thermal_state = self.power_monitor.get_thermal_status()
        
        current_hour = time.localtime().tm_hour
        
        is_plugged = battery_state.get('plugged_in', False)
        battery_percent = battery_state.get('percent', 100)
        is_thermal_ok = thermal_state.get('status') == 'normal'
        
        if is_plugged:
            return {
                'recommended': 'now',
                'reason': 'Device is plugged in'
            }
        
        if battery_percent > 50 and is_thermal_ok:
            return {
                'recommended': 'now',
                'reason': 'Battery and thermal conditions are good'
            }
        
        if battery_percent < 20:
            return {
                'recommended': 'when_charging',
                'reason': 'Battery too low'
            }
        
        if not is_thermal_ok:
            return {
                'recommended': 'after_cooling',
                'reason': 'Device needs cooling'
            }
        
        if 1 <= current_hour <= 6:
            return {
                'recommended': 'now',
                'reason': 'Low-load window (night time)'
            }
        
        return {
            'recommended': 'deferred',
            'reason': 'Suboptimal conditions, defer if possible'
        }
