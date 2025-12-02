import unittest
from src.runtime_inspector import RuntimeInspector
from src.runtime_inspector.profiler import Profiler

class TestRuntimeInspector(unittest.TestCase):
    """
    Tests for runtime inspector module
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.inspector = RuntimeInspector()
        self.profiler = Profiler(self.inspector.config)
    
    def test_profiler(self):
        """
        Tests profiler
        """
        results = self.profiler.profile(None, duration_seconds=1.0)
        
        self.assertIn('cpu', results)
        self.assertIn('memory', results)
        self.assertIn('throughput_fps', results)
    
    def test_thermal_monitor(self):
        """
        Tests thermal monitoring
        """
        thermal_data = self.inspector.thermal_monitor.monitor(duration_seconds=1.0)
        
        self.assertIn('status', thermal_data)

if __name__ == '__main__':
    unittest.main()
