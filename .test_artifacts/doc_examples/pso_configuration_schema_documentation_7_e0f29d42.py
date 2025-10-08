# Example from: docs\pso_configuration_schema_documentation.md
# Index: 7
# Runnable: False
# Hash: e0f29d42

class AdaptivePSOTuner:
    """
    Adaptive PSO parameter tuning based on real-time performance feedback.
    """

    def __init__(self, initial_config: dict):
        self.config = initial_config
        self.performance_history = []
        self.adaptation_strategy = 'conservative'  # conservative, aggressive, balanced

    def adapt_parameters_realtime(self, pso_state: dict, iteration: int) -> dict:
        """
        Adapt PSO parameters during optimization based on performance indicators.
        """
        adaptations = {}

        # Analyze current performance
        performance_metrics = self._analyze_performance(pso_state, iteration)

        # Inertia weight adaptation
        if self._should_adapt_inertia(performance_metrics):
            new_w = self._compute_adaptive_inertia(performance_metrics, iteration)
            adaptations['w'] = new_w

        # Diversity maintenance
        if self._should_restart_particles(performance_metrics):
            restart_indices = self._select_restart_particles(pso_state)
            adaptations['restart_particles'] = restart_indices

        # Bounds adaptation (for Issue #2 compliance)
        if self._should_adapt_bounds(performance_metrics):
            adapted_bounds = self._adapt_bounds_for_performance(performance_metrics)
            adaptations['bounds'] = adapted_bounds

        return adaptations

    def _compute_adaptive_inertia(self, performance: dict, iteration: int) -> float:
        """
        Compute adaptive inertia weight based on convergence state.
        """
        base_w = self.config['algorithm_params']['w']
        max_iters = self.config['algorithm_params']['iters']

        # Linear decrease with performance-based adjustment
        linear_w = 0.9 - 0.5 * (iteration / max_iters)

        # Performance-based adjustment
        if performance['convergence_rate'] < 0.05:  # Slow convergence
            adjustment = -0.1  # Reduce inertia for more exploitation
        elif performance['diversity'] < 1e-8:  # Low diversity
            adjustment = +0.15  # Increase inertia for more exploration
        else:
            adjustment = 0.0

        adaptive_w = np.clip(linear_w + adjustment, 0.1, 0.95)
        return adaptive_w

    def _adapt_bounds_for_performance(self, performance: dict) -> dict:
        """
        Adapt bounds based on optimization performance and Issue #2 compliance.
        """
        current_bounds = self.config['bounds']
        adapted_bounds = current_bounds.copy()

        # Issue #2 specific adaptation for STA-SMC
        if 'sta_smc' in current_bounds and performance['controller_type'] == 'sta_smc':
            if performance.get('overshoot', 0) > 0.05:  # >5% overshoot detected
                # Further restrict lambda bounds
                sta_bounds = adapted_bounds['sta_smc']
                if 'max' in sta_bounds and len(sta_bounds['max']) >= 6:
                    # Progressively tighten bounds
                    reduction_factor = 0.8
                    sta_bounds['max'][4] *= reduction_factor  # lambda1
                    sta_bounds['max'][5] *= reduction_factor  # lambda2

        return adapted_bounds

    def generate_tuning_recommendations(self) -> dict:
        """
        Generate parameter tuning recommendations based on historical performance.
        """
        if len(self.performance_history) < 10:
            return {'status': 'insufficient_data'}

        # Analyze performance trends
        convergence_rates = [p['convergence_rate'] for p in self.performance_history[-10:]]
        final_costs = [p['final_cost'] for p in self.performance_history[-10:]]
        optimization_times = [p['optimization_time'] for p in self.performance_history[-10:]]

        recommendations = {
            'parameter_adjustments': [],
            'configuration_changes': [],
            'performance_outlook': 'stable'
        }

        # Convergence analysis
        avg_convergence = np.mean(convergence_rates)
        if avg_convergence < 0.1:
            recommendations['parameter_adjustments'].append({
                'parameter': 'n_particles',
                'current': self.config['algorithm_params']['n_particles'],
                'recommended': min(50, self.config['algorithm_params']['n_particles'] + 5),
                'reason': 'Slow convergence - increase swarm size'
            })

        # Cost analysis
        cost_variance = np.var(final_costs)
        if cost_variance > 0.01:
            recommendations['parameter_adjustments'].append({
                'parameter': 'early_stopping.tolerance',
                'current': self.config.get('enhanced_features', {}).get('early_stopping', {}).get('tolerance', 1e-6),
                'recommended': 1e-7,
                'reason': 'High cost variance - tighten convergence tolerance'
            })

        # Performance outlook
        if avg_convergence > 0.2 and cost_variance < 0.005:
            recommendations['performance_outlook'] = 'excellent'
        elif avg_convergence < 0.05 or cost_variance > 0.02:
            recommendations['performance_outlook'] = 'needs_improvement'

        return recommendations