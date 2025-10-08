# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 4
# Runnable: False
# Hash: 1687a740

class OptimizationMonitor:
    """
    Real-time monitoring system for PSO optimization with adaptive capabilities.
    """

    def __init__(self, monitors: dict, config: dict):
        self.monitors = monitors
        self.config = config
        self.monitoring_data = {
            'iteration_times': [],
            'memory_usage': [],
            'cost_improvements': [],
            'diversity_metrics': [],
            'constraint_violations': [],
            'safety_alerts': []
        }

    def monitor_iteration(self, iteration: int, swarm_state: dict) -> MonitoringResult:
        """
        Monitor single PSO iteration with comprehensive metrics collection.
        """
        iteration_start = time.time()
        result = MonitoringResult()

        # Performance monitoring
        perf_metrics = self.monitors['performance'].collect_metrics(swarm_state)
        self.monitoring_data['iteration_times'].append(perf_metrics['iteration_time'])
        self.monitoring_data['memory_usage'].append(perf_metrics['memory_mb'])

        # Convergence monitoring
        conv_metrics = self.monitors['convergence'].analyze_convergence(swarm_state)
        self.monitoring_data['cost_improvements'].append(conv_metrics['cost_improvement'])
        self.monitoring_data['diversity_metrics'].append(conv_metrics['diversity'])

        # Constraint validation
        constraint_result = self._validate_constraints_realtime(swarm_state)
        self.monitoring_data['constraint_violations'].extend(constraint_result['violations'])

        # Safety monitoring
        safety_result = self.monitors['safety'].check_safety_conditions(swarm_state)
        if safety_result['alerts']:
            self.monitoring_data['safety_alerts'].extend(safety_result['alerts'])

        # Adaptive parameter adjustment
        if self._should_adapt_parameters(iteration, swarm_state):
            adaptations = self._compute_parameter_adaptations(swarm_state)
            result.parameter_adaptations = adaptations

        # Issue #2 specific monitoring for STA-SMC
        if self.config.get('controller_type') == 'sta_smc':
            issue2_result = self._monitor_issue2_compliance(swarm_state)
            result.issue2_compliance = issue2_result

        result.monitoring_data = self.monitoring_data
        result.iteration_time = time.time() - iteration_start

        return result

    def _validate_constraints_realtime(self, swarm_state: dict) -> dict:
        """
        Real-time validation of mathematical and physical constraints.
        """
        violations = []
        particles = swarm_state.get('positions', np.array([]))

        if particles.size == 0:
            return {'violations': violations}

        controller_type = self.config.get('controller_type', 'classical_smc')

        # Controller-specific constraint checking
        if controller_type == 'sta_smc' and particles.shape[1] >= 6:
            # K₁ > K₂ constraint
            k1_particles, k2_particles = particles[:, 0], particles[:, 1]
            k1_le_k2_mask = k1_particles <= k2_particles
            if np.any(k1_le_k2_mask):
                violation_count = np.sum(k1_le_k2_mask)
                violations.append({
                    'type': 'STA_STABILITY_VIOLATION',
                    'count': violation_count,
                    'particles': np.where(k1_le_k2_mask)[0].tolist(),
                    'severity': 'HIGH'
                })

            # Issue #2 damping ratio constraint
            if particles.shape[1] >= 6:
                lambda1, lambda2 = particles[:, 4], particles[:, 5]
                k1, k2 = particles[:, 2], particles[:, 3]

                # Safe computation with epsilon to avoid division by zero
                epsilon = 1e-12
                zeta1 = lambda1 / (2 * np.sqrt(k1 + epsilon))
                zeta2 = lambda2 / (2 * np.sqrt(k2 + epsilon))

                # Check Issue #2 requirement: ζ ≥ 0.69
                zeta1_violation = zeta1 < 0.69
                zeta2_violation = zeta2 < 0.69

                if np.any(zeta1_violation) or np.any(zeta2_violation):
                    violation_particles = np.where(zeta1_violation | zeta2_violation)[0]
                    violations.append({
                        'type': 'ISSUE2_DAMPING_VIOLATION',
                        'count': len(violation_particles),
                        'particles': violation_particles.tolist(),
                        'severity': 'HIGH',
                        'details': {
                            'min_zeta1': np.min(zeta1),
                            'min_zeta2': np.min(zeta2),
                            'requirement': 'ζ ≥ 0.69 for <5% overshoot'
                        }
                    })

        return {'violations': violations}

    def _monitor_issue2_compliance(self, swarm_state: dict) -> dict:
        """
        Specialized monitoring for Issue #2 overshoot compliance.
        """
        particles = swarm_state.get('positions', np.array([]))
        if particles.size == 0 or particles.shape[1] < 6:
            return {'status': 'insufficient_data'}

        # Extract surface coefficients
        lambda1, lambda2 = particles[:, 4], particles[:, 5]
        k1, k2 = particles[:, 2], particles[:, 3]

        # Compute damping ratios
        epsilon = 1e-12
        zeta1 = lambda1 / (2 * np.sqrt(k1 + epsilon))
        zeta2 = lambda2 / (2 * np.sqrt(k2 + epsilon))

        # Issue #2 compliance analysis
        compliance_stats = {
            'compliant_particles': 0,
            'total_particles': len(particles),
            'min_damping_ratio': min(np.min(zeta1), np.min(zeta2)),
            'avg_damping_ratio': (np.mean(zeta1) + np.mean(zeta2)) / 2,
            'predicted_overshoot_range': [],
            'lambda_bounds_status': 'unknown'
        }

        # Count compliant particles (ζ ≥ 0.69)
        compliant_mask = (zeta1 >= 0.69) & (zeta2 >= 0.69)
        compliance_stats['compliant_particles'] = np.sum(compliant_mask)

        # Predict overshoot for representative particles
        for i in range(min(5, len(particles))):  # Sample first 5 particles
            zeta_avg = (zeta1[i] + zeta2[i]) / 2
            if zeta_avg < 1.0:  # Underdamped
                predicted_overshoot = 100 * np.exp(-zeta_avg * np.pi / np.sqrt(1 - zeta_avg**2))
            else:  # Overdamped
                predicted_overshoot = 0.0
            compliance_stats['predicted_overshoot_range'].append(predicted_overshoot)

        # Check lambda bounds status
        max_lambda1, max_lambda2 = np.max(lambda1), np.max(lambda2)
        if max_lambda1 <= 10.0 and max_lambda2 <= 10.0:
            compliance_stats['lambda_bounds_status'] = 'compliant'
        else:
            compliance_stats['lambda_bounds_status'] = 'violation'

        return compliance_stats