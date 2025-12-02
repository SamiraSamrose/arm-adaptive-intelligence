from src.runtime_inspector.profiler import Profiler
from src.runtime_inspector.thermal_monitor import ThermalMonitor
from src.runtime_inspector.graph_analyzer import GraphAnalyzer
from src.runtime_inspector.multi_agent_system import MultiAgentSystem

class RuntimeInspector:
    """
    Main interface for runtime inspection and profiling
    """
    
    def __init__(self, config_path: str = "config/device_config.yaml"):
        from src.core.utils import load_config
        self.config = load_config(config_path)
        
        self.profiler = Profiler(self.config)
        self.thermal_monitor = ThermalMonitor(self.config)
        self.graph_analyzer = GraphAnalyzer(self.config)
        self.multi_agent = MultiAgentSystem(self.config)
    
    def profile_inference(self, model, input_data=None):
        """
        Profiles model inference with multi-agent analysis
        """
        profile_data = self.profiler.profile(model, input_data)
        thermal_data = self.thermal_monitor.monitor()
        graph_data = self.graph_analyzer.analyze(model)
        
        analysis = self.multi_agent.analyze_all(profile_data, thermal_data, graph_data)
        
        return analysis

__all__ = ["RuntimeInspector", "Profiler", "ThermalMonitor", "GraphAnalyzer", "MultiAgentSystem"]