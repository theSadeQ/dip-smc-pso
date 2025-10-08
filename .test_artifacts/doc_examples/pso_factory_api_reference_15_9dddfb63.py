# Example from: docs\factory\pso_factory_api_reference.md
# Index: 15
# Runnable: True
# Hash: 9dddfb63

class AdaptivePSOFactory:
    """
    Adaptive PSO optimization with dynamic parameter adjustment.

    Features:
    - Dynamic bounds tightening around promising regions
    - Adaptive PSO parameter tuning based on convergence
    - Early stopping with convergence detection
    - Multi-stage optimization with exploration-exploitation balance
    """

    def __init__(self, smc_type: SMCType, config: Dict[str, Any]):
        self.smc_type = smc_type
        self.config = config
        self.optimization_history = []
        self.bounds_history = []

        # Initialize with full bounds
        self.current_bounds = get_gain_bounds_for_pso(smc_type)
        self.best_solution = None
        self.convergence_detector = PSOConvergenceDetector()

    def optimize_with_adaptation(self,
                                simulation_config: Dict[str, Any],
                                stages: List[Dict[str, Any]]
                                ) -> Dict[str, Any]:
        """
        Run adaptive PSO optimization with multiple stages.

        Args:
            simulation_config: Simulation parameters
            stages: List of optimization stages with different parameters

        Returns:
            Complete optimization results with adaptation history
        """

        all_results = []

        for stage_idx, stage_config in enumerate(stages):
            print(f"PSO Stage {stage_idx + 1}: {stage_config}")

            # Adapt PSO parameters for this stage
            pso_params = self._adapt_pso_parameters(stage_config, stage_idx)

            # Adapt bounds based on previous results
            if stage_idx > 0 and self.best_solution is not None:
                self.current_bounds = self._adapt_bounds(
                    self.best_solution['gains'],
                    stage_config.get('bound_tightening', 0.5)
                )

            # Create fitness function
            fitness_function = self._create_adaptive_fitness_function(
                simulation_config, stage_config
            )

            # Run PSO optimization stage
            stage_result = self._run_pso_stage(
                fitness_function, pso_params, stage_config['iterations']
            )

            all_results.append(stage_result)

            # Update best solution
            if (self.best_solution is None or
                stage_result['best_fitness'] < self.best_solution['fitness']):
                self.best_solution = {
                    'gains': stage_result['best_gains'],
                    'fitness': stage_result['best_fitness'],
                    'stage': stage_idx
                }

            # Check for early convergence
            if self.convergence_detector.check_convergence(stage_result):
                print(f"Early convergence detected at stage {stage_idx + 1}")
                break

        # Combine results
        final_result = self._combine_stage_results(all_results)
        final_result['adaptation_history'] = {
            'bounds_history': self.bounds_history,
            'best_solution_history': self.optimization_history
        }

        return final_result

    def _adapt_pso_parameters(self,
                             stage_config: Dict[str, Any],
                             stage_idx: int
                             ) -> Dict[str, Any]:
        """Adapt PSO parameters based on stage and convergence history."""

        base_params = self.config.get('pso_params', {})

        # Exploration vs exploitation balance
        exploration_weight = stage_config.get('exploration_weight', 0.5)

        # Adaptive inertia weight
        w_max = 0.9
        w_min = 0.4
        w = w_max - (w_max - w_min) * exploration_weight

        # Adaptive cognitive/social parameters
        c1 = 2.5 - exploration_weight  # High cognitive for exploration
        c2 = 0.5 + exploration_weight  # High social for exploitation

        return {
            'n_particles': base_params.get('n_particles', 30),
            'c1': c1,
            'c2': c2,
            'w': w
        }

    def _adapt_bounds(self,
                     best_gains: List[float],
                     tightening_factor: float
                     ) -> List[Tuple[float, float]]:
        """Adapt optimization bounds around best solution."""

        adapted_bounds = []
        original_bounds = get_gain_bounds_for_pso(self.smc_type)

        for i, (gain, (orig_lower, orig_upper)) in enumerate(zip(best_gains, original_bounds)):
            # Calculate range around best gain
            range_width = (orig_upper - orig_lower) * tightening_factor

            # New bounds centered around best gain
            new_lower = max(orig_lower, gain - range_width / 2)
            new_upper = min(orig_upper, gain + range_width / 2)

            adapted_bounds.append((new_lower, new_upper))

        self.bounds_history.append(adapted_bounds)
        return adapted_bounds

    def _create_adaptive_fitness_function(self,
                                        simulation_config: Dict[str, Any],
                                        stage_config: Dict[str, Any]
                                        ) -> Callable:
        """Create fitness function with adaptive features."""

        def adaptive_fitness(particles: np.ndarray) -> np.ndarray:
            fitness_scores = []

            for gains in particles:
                try:
                    # Create controller with validation
                    controller = create_smc_for_pso(self.smc_type, gains.tolist())

                    # Run simulation
                    result = run_simulation(controller, simulation_config)

                    # Compute base fitness
                    base_fitness = compute_control_performance_metrics(
                        result, stage_config.get('objectives', ['ise'])
                    )

                    # Add adaptive penalties/bonuses
                    adapted_fitness = self._apply_adaptive_adjustments(
                        base_fitness, gains.tolist(), stage_config
                    )

                    fitness_scores.append(adapted_fitness)

                except Exception:
                    fitness_scores.append(1000.0)

            return np.array(fitness_scores)

        return adaptive_fitness

    def _apply_adaptive_adjustments(self,
                                  base_fitness: float,
                                  gains: List[float],
                                  stage_config: Dict[str, Any]
                                  ) -> float:
        """Apply adaptive adjustments to fitness based on stage configuration."""

        adjusted_fitness = base_fitness

        # Diversity bonus (encourage exploration in early stages)
        if stage_config.get('diversity_bonus', False) and self.best_solution:
            distance = np.linalg.norm(
                np.array(gains) - np.array(self.best_solution['gains'])
            )
            diversity_bonus = stage_config.get('diversity_weight', 0.1) * distance
            adjusted_fitness -= diversity_bonus

        # Stability margin bonus
        if stage_config.get('stability_bonus', True):
            stability_properties = estimate_stability_properties(self.smc_type, gains)
            stability_bonus = stability_properties['stability_margin'] * 0.1
            adjusted_fitness -= stability_bonus

        return adjusted_fitness

class PSOConvergenceDetector:
    """Advanced convergence detection for PSO optimization."""

    def __init__(self, patience: int = 20, tolerance: float = 1e-6):
        self.patience = patience
        self.tolerance = tolerance
        self.fitness_history = []
        self.best_fitness = float('inf')
        self.stagnation_count = 0

    def check_convergence(self, stage_result: Dict[str, Any]) -> bool:
        """
        Check if PSO has converged based on multiple criteria.

        Args:
            stage_result: Results from PSO optimization stage

        Returns:
            True if convergence detected, False otherwise
        """
        current_fitness = stage_result['best_fitness']
        self.fitness_history.append(current_fitness)

        # Check for improvement
        if current_fitness < self.best_fitness - self.tolerance:
            self.best_fitness = current_fitness
            self.stagnation_count = 0
        else:
            self.stagnation_count += 1

        # Multiple convergence criteria
        return (
            self._check_fitness_plateau() or
            self._check_statistical_convergence()
        )

    def _check_fitness_plateau(self) -> bool:
        """Check if fitness has plateaued."""
        return self.stagnation_count >= self.patience

    def _check_statistical_convergence(self) -> bool:
        """Check statistical significance of convergence."""
        if len(self.fitness_history) < 30:
            return False

        # Test if recent improvements are statistically significant
        recent_fitness = self.fitness_history[-15:]
        older_fitness = self.fitness_history[-30:-15]

        from scipy.stats import ttest_ind
        try:
            statistic, p_value = ttest_ind(recent_fitness, older_fitness)
            return p_value > 0.05  # No significant difference
        except:
            return False