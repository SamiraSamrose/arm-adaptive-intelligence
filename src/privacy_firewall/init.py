from src.privacy_firewall.sandbox import PrivacySandbox
from src.privacy_firewall.policy_checker import PolicyChecker
from src.privacy_firewall.data_flow_analyzer import DataFlowAnalyzer

class PrivacyFirewall:
    """
    Main interface for privacy protection
    """
    
    def __init__(self, config_path: str = "config/privacy_config.yaml"):
        from src.core.utils import load_config
        self.config = load_config(config_path)
        
        self.sandbox = PrivacySandbox(self.config)
        self.policy_checker = PolicyChecker(self.config)
        self.data_flow_analyzer = DataFlowAnalyzer(self.config)
    
    def validate_operation(self, operation: Dict):
        """
        Validates an AI operation against privacy policies
        """
        policy_check = self.policy_checker.check(operation)
        flow_check = self.data_flow_analyzer.analyze(operation)
        
        return policy_check and flow_check
    
    def sandbox_model(self, model):
        """
        Runs model in sandboxed environment
        """
        return self.sandbox.execute(model)

__all__ = ["PrivacyFirewall", "PrivacySandbox", "PolicyChecker", "DataFlowAnalyzer"]