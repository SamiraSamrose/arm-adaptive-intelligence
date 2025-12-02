import unittest
from src.battery_scheduler import BatteryScheduler

class TestBatteryScheduler(unittest.TestCase):
    """
    Tests for battery scheduler module
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.scheduler = BatteryScheduler()
    
    def test_battery_predictor(self):
        """
        Tests battery prediction
        """
        task_desc = {
            'compute_ops': 1e9,
            'memory_mb': 100,
            'duration_seconds': 1.0
        }
        
        prediction = self.scheduler.predictor.predict_drain(task_desc)
        
        self.assertIn('estimated_drain_percent', prediction)
        self.assertIn('safe_to_execute', prediction)
    
    def test_optimal_time(self):
        """
        Tests optimal time calculation
        """
        optimal = self.scheduler.get_optimal_time()
        
        self.assertIn('recommended', optimal)
        self.assertIn('reason', optimal)

if __name__ == '__main__':
    unittest.main()
