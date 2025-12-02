from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class PolicyChecker:
    """
    Checks AI operations against defined privacy policies
    Enforces data handling rules and permissions
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict:
        """
        Loads privacy policies from configuration
        """
        privacy_config = self.config.get('privacy', {})
        permissions = self.config.get('permissions', {})
        
        return {
            'local_processing_only': privacy_config.get('local_processing_only', True),
            'data_retention_days': privacy_config.get('data_retention_days', 30),
            'encryption_enabled': privacy_config.get('encryption_enabled', True),
            'allow_network': permissions.get('allow_network', False),
            'allow_storage': permissions.get('allow_storage', True),
            'allow_camera': permissions.get('allow_camera', False),
            'allow_microphone': permissions.get('allow_microphone', False)
        }
    
    def check(self, operation: Dict) -> bool:
        """
        Checks if operation complies with policies
        
        Steps:
        1. Extract operation details
        2. Check against each policy
        3. Log violations
        4. Return compliance status
        """
        operation_type = operation.get('type', 'unknown')
        logger.debug(f"Checking policy compliance for: {operation_type}")
        
        checks = [
            self._check_network_policy(operation),
            self._check_storage_policy(operation),
            self._check_sensor_policy(operation),
            self._check_data_retention_policy(operation)
        ]
        
        all_passed = all(checks)
        
        if all_passed:
            logger.info(f"Policy check passed for {operation_type}")
        else:
            logger.warning(f"Policy check failed for {operation_type}")
        
        return all_passed
    
    def _check_network_policy(self, operation: Dict) -> bool:
        """
        Checks network usage policy
        """
        requires_network = operation.get('requires_network', False)
        
        if requires_network and not self.policies['allow_network']:
            logger.warning("Network access not allowed by policy")
            return False
        
        return True
    
    def _check_storage_policy(self, operation: Dict) -> bool:
        """
        Checks storage policy
        """
        requires_storage = operation.get('requires_storage', False)
        
        if requires_storage and not self.policies['allow_storage']:
            logger.warning("Storage access not allowed by policy")
            return False
        
        return True
    
    def _check_sensor_policy(self, operation: Dict) -> bool:
        """
        Checks sensor access policy
        """
        requires_camera = operation.get('requires_camera', False)
        requires_microphone = operation.get('requires_microphone', False)
        
        if requires_camera and not self.policies['allow_camera']:
            logger.warning("Camera access not allowed by policy")
            return False
        
        if requires_microphone and not self.policies['allow_microphone']:
            logger.warning("Microphone access not allowed by policy")
            return False
        
        return True
    
    def _check_data_retention_policy(self, operation: Dict) -> bool:
        """
        Checks data retention policy
        """
        data_age_days = operation.get('data_age_days', 0)
        max_retention = self.policies['data_retention_days']
        
        if data_age_days > max_retention:
            logger.warning(f"Data exceeds retention policy: {data_age_days} > {max_retention} days")
            return False
        
        return True
    
    def get_policy_summary(self) -> Dict:
        """
        Gets summary of current policies
        """
        return {
            'policies': self.policies,
            'total_policies': len(self.policies),
            'strict_mode': self.policies['local_processing_only']
        }
    
    def update_policy(self, policy_name: str, value: Any) -> bool:
        """
        Updates a specific policy
        """
        if policy_name in self.policies:
            old_value = self.policies[policy_name]
            self.policies[policy_name] = value
            logger.info(f"Policy updated: {policy_name} from {old_value} to {value}")
            return True
        
        logger.error(f"Unknown policy: {policy_name}")
        return False