from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MultiAgentSystem:
    """
    Multi-agent system for comprehensive performance analysis
    Coordinates Graph-Agent, Thermal-Agent, Memory-Agent, and LLM-based explanation
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.agents = {
            'graph_agent': GraphAgent(),
            'thermal_agent': ThermalAgent(),
            'memory_agent': MemoryAgent(),
            'performance_agent': PerformanceAgent()
        }
        self.llm_explainer = LLMExplainer()
    
    def analyze_all(self, profile_data: Dict, thermal_data: Dict, graph_data: Dict) -> Dict:
        """
        Coordinates all agents for comprehensive analysis
        
        Steps:
        1. Each agent analyzes its domain
        2. Aggregate findings
        3. Generate LLM explanation
        4. Provide actionable recommendations
        """
        logger.info("Multi-agent analysis started")
        
        agent_results = {}
        
        agent_results['graph'] = self.agents['graph_agent'].analyze(graph_data)
        agent_results['thermal'] = self.agents['thermal_agent'].analyze(thermal_data)
        agent_results['memory'] = self.agents['memory_agent'].analyze(profile_data)
        agent_results['performance'] = self.agents['performance_agent'].analyze(profile_data)
        
        consolidated = self._consolidate_findings(agent_results)
        
        natural_language_explanation = self.llm_explainer.generate_explanation(
            consolidated, profile_data, thermal_data, graph_data
        )
        
        result = {
            'agent_analyses': agent_results,
            'consolidated_findings': consolidated,
            'natural_language_explanation': natural_language_explanation,
            'recommendations': self._generate_recommendations(consolidated)
        }
        
        logger.info("Multi-agent analysis complete")
        return result
    
    def _consolidate_findings(self, agent_results: Dict) -> Dict:
        """
        Consolidates findings from all agents
        
        Steps:
        1. Identify cross-cutting issues
        2. Prioritize problems
        3. Correlate related findings
        """
        issues = []
        severity_scores = {}
        
        for agent_name, result in agent_results.items():
            if 'issues' in result:
                for issue in result['issues']:
                    issues.append({
                        'source_agent': agent_name,
                        'issue': issue,
                        'severity': result.get('severity', 'medium')
                    })
        
        consolidated = {
            'total_issues': len(issues),
            'issues_by_severity': self._categorize_by_severity(issues),
            'primary_bottleneck': self._identify_primary_bottleneck(agent_results),
            'correlation_insights': self._find_correlations(agent_results)
        }
        
        return consolidated
    
    def _categorize_by_severity(self, issues: List[Dict]) -> Dict:
        """
        Categorizes issues by severity
        """
        categories = {'critical': [], 'high': [], 'medium': [], 'low': []}
        
        for issue in issues:
            severity = issue.get('severity', 'medium')
            if severity in categories:
                categories[severity].append(issue)
        
        return categories
    
    def _identify_primary_bottleneck(self, agent_results: Dict) -> str:
        """
        Identifies the primary system bottleneck
        """
        graph_issues = len(agent_results.get('graph', {}).get('issues', []))
        thermal_issues = len(agent_results.get('thermal', {}).get('issues', []))
        memory_issues = len(agent_results.get('memory', {}).get('issues', []))
        
        if thermal_issues > 0:
            return "thermal_throttling"
        elif memory_issues > graph_issues:
            return "memory_bandwidth"
        elif graph_issues > 0:
            return "compute_inefficiency"
        else:
            return "no_major_bottleneck"
    
    def _find_correlations(self, agent_results: Dict) -> List[str]:
        """
        Finds correlations between different agent findings
        """
        correlations = []
        
        thermal = agent_results.get('thermal', {})
        performance = agent_results.get('performance', {})
        
        if thermal.get('throttling', False) and performance.get('degraded', False):
            correlations.append("Thermal throttling is causing performance degradation")
        
        memory = agent_results.get('memory', {})
        graph = agent_results.get('graph', {})
        
        if memory.get('high_usage', False) and 'memory-bound' in str(graph.get('bottlenecks', [])):
            correlations.append("High memory usage correlates with memory-bound operators")
        
        return correlations
    
    def _generate_recommendations(self, consolidated: Dict) -> List[str]:
        """
        Generates actionable recommendations
        """
        recommendations = []
        
        primary = consolidated.get('primary_bottleneck', '')
        
        if primary == 'thermal_throttling':
            recommendations.append("Reduce inference frequency to allow cooling")
            recommendations.append("Lower model precision (e.g., INT8 instead of FP16)")
            recommendations.append("Schedule intensive tasks during cooler periods")
        elif primary == 'memory_bandwidth':
            recommendations.append("Enable operator fusion to reduce memory transfers")
            recommendations.append("Use in-place operations where possible")
            recommendations.append("Optimize tensor layouts for cache efficiency")
        elif primary == 'compute_inefficiency':
            recommendations.append("Apply model quantization to reduce compute")
            recommendations.append("Use ARM NEON/SVE optimized kernels")
            recommendations.append("Consider model pruning for critical operators")

        return recommendations

class GraphAgent:
"""
Agent specialized in graph analysis
"""
def analyze(self, graph_data: Dict) -> Dict:
    """
    Analyzes graph structure and bottlenecks
    """
    issues = []
    
    bottlenecks = graph_data.get('bottlenecks', [])
    if len(bottlenecks) > 0:
        for bottleneck in bottlenecks:
            issues.append(f"Bottleneck in {bottleneck['operator_name']}: {bottleneck['issue']}")
    
    return {
        'issues': issues,
        'severity': 'high' if len(issues) > 2 else 'medium',
        'bottlenecks': bottlenecks
    }
class ThermalAgent:
"""
Agent specialized in thermal analysis
"""
def analyze(self, thermal_data: Dict) -> Dict:
    """
    Analyzes thermal conditions
    """
    issues = []
    throttling = thermal_data.get('throttling_detected', False)
    status = thermal_data.get('status', 'normal')
    
    if throttling:
        issues.append("Thermal throttling detected - performance is degraded")
    
    if status == 'warning':
        issues.append("Temperature approaching critical threshold")
    
    return {
        'issues': issues,
        'severity': 'critical' if throttling else 'medium',
        'throttling': throttling
    }
class MemoryAgent:
"""
Agent specialized in memory analysis
"""
def analyze(self, profile_data: Dict) -> Dict:
    """
    Analyzes memory usage patterns
    """
    issues = []
    
    memory_data = profile_data.get('memory', {})
    max_mb = memory_data.get('max_mb', 0)
    
    if max_mb > 1024:
        issues.append(f"High memory usage detected: {max_mb:.0f}MB")
    
    return {
        'issues': issues,
        'severity': 'high' if max_mb > 2048 else 'medium',
        'high_usage': max_mb > 1024
    }
class PerformanceAgent:
"""
Agent specialized in performance analysis
"""
def analyze(self, profile_data: Dict) -> Dict:
    """
    Analyzes overall performance metrics
    """
    issues = []
    
    throughput = profile_data.get('throughput_fps', 0)
    
    if throughput < 10:
        issues.append(f"Low throughput: {throughput:.1f} FPS")
    
    bottleneck = profile_data.get('bottleneck', '')
    if bottleneck:
        issues.append(f"Primary bottleneck: {bottleneck}")
    
    return {
        'issues': issues,
        'severity': 'medium',
        'degraded': throughput < 10
    }
class LLMExplainer:
"""
Generates natural language explanations using on-device LLM
"""
def generate_explanation(self, consolidated: Dict, profile_data: Dict, 
                       thermal_data: Dict, graph_data: Dict) -> str:
    """
    Generates natural language diagnostic explanation
    
    Steps:
    1. Analyze consolidated findings
    2. Generate human-readable explanation
    3. Provide context and reasoning
    """
    primary = consolidated.get('primary_bottleneck', 'unknown')
    issues = consolidated.get('issues_by_severity', {})
    
    explanation_parts = []
    
    explanation_parts.append("Performance Analysis Summary:")
    explanation_parts.append("")
    
    if primary == 'thermal_throttling':
        temp = thermal_data.get('max_temperature_celsius', 0)
        explanation_parts.append(
            f"Your model is experiencing thermal throttling. The device temperature "
            f"reached {temp:.1f}C, causing the processor to reduce performance to prevent "
            f"overheating. This is reducing inference speed significantly."
        )
    
    elif primary == 'memory_bandwidth':
        explanation_parts.append(
            "Your model is bottlenecked by memory bandwidth. The operators are spending "
            "more time transferring data between memory and compute units than performing "
            "actual computations. This suggests memory-bound operations."
        )
    
    elif primary == 'compute_inefficiency':
        bottlenecks = graph_data.get('bottlenecks', [])
        if bottlenecks:
            top_bottleneck = bottlenecks[0]
            explanation_parts.append(
                f"Your model is blocked by inefficient operators. The {top_bottleneck['operator_name']} "
                f"({top_bottleneck['operator_type']}) is consuming {top_bottleneck['percentage_of_total']:.1f}% "
                f"of total execution time. {top_bottleneck['issue']}"
            )
    
    else:
        explanation_parts.append(
            "Your model is performing reasonably well. No major bottlenecks detected, "
            "but there are still optimization opportunities."
        )
    
    critical_issues = issues.get('critical', [])
    if critical_issues:
        explanation_parts.append("")
        explanation_parts.append("Critical Issues:")
        for issue in critical_issues[:3]:
            explanation_parts.append(f"- {issue['issue']}")
    
    correlations = consolidated.get('correlation_insights', [])
    if correlations:
        explanation_parts.append("")
        explanation_parts.append("Key Insights:")
        for correlation in correlations:
            explanation_parts.append(f"- {correlation}")
    
    return "\n".join(explanation_parts)