# Example from: docs\pso_configuration_schema_documentation.md
# Index: 5
# Runnable: False
# Hash: 9a7d3a4d

class ConfigurationMonitor:
    """
    Real-time monitoring of PSO configuration performance and adaptation.
    """

    def __init__(self, config: dict):
        self.config = config
        self.performance_history = []
        self.adaptation_triggers = {
            'poor_convergence': self._handle_poor_convergence,
            'parameter_instability': self._handle_parameter_instability,
            'safety_violation': self._handle_safety_violation
        }

    def monitor_optimization_run(self, pso_state: dict) -> dict:
        """
        Monitor PSO optimization run and suggest configuration adaptations.
        """
        current_performance = self._assess_performance(pso_state)
        self.performance_history.append(current_performance)

        # Check for adaptation triggers
        adaptations = {}
        for trigger_name, handler in self.adaptation_triggers.items():
            if self._check_trigger(trigger_name, current_performance):
                adaptation = handler(current_performance)
                if adaptation:
                    adaptations[trigger_name] = adaptation

        return {
            'performance': current_performance,
            'suggested_adaptations': adaptations,
            'config_health': self._assess_config_health()
        }

    def _handle_poor_convergence(self, performance: dict) -> dict:
        """
        Handle poor convergence by adjusting PSO parameters.
        """
        if performance['convergence_rate'] < 0.1:  # Very slow convergence
            return {
                'parameter': 'w',
                'adjustment': 'decrease',
                'new_value': max(0.4, self.config['algorithm_params']['w'] - 0.1),
                'reason': 'Increase exploitation for faster convergence'
            }

        if performance['diversity'] < 1e-8:  # Premature convergence
            return {
                'parameter': 'w',
                'adjustment': 'increase',
                'new_value': min(0.9, self.config['algorithm_params']['w'] + 0.1),
                'reason': 'Increase exploration to escape local optimum'
            }

        return None

    def _assess_config_health(self) -> dict:
        """
        Assess overall configuration health and optimization efficiency.
        """
        if len(self.performance_history) < 5:
            return {'status': 'insufficient_data'}

        recent_performance = self.performance_history[-5:]

        # Convergence trend analysis
        convergence_trend = np.polyfit(range(5), [p['convergence_rate'] for p in recent_performance], 1)[0]

        # Stability assessment
        cost_variance = np.var([p['best_cost'] for p in recent_performance])

        health_score = 100.0
        issues = []

        if convergence_trend < -0.01:  # Degrading convergence
            health_score -= 20
            issues.append('degrading_convergence')

        if cost_variance > 1.0:  # High cost variance
            health_score -= 15
            issues.append('unstable_optimization')

        avg_diversity = np.mean([p['diversity'] for p in recent_performance])
        if avg_diversity < 1e-10:  # Very low diversity
            health_score -= 25
            issues.append('diversity_collapse')

        return {
            'status': 'healthy' if health_score > 80 else 'needs_attention',
            'score': health_score,
            'issues': issues,
            'recommendations': self._generate_recommendations(issues)
        }