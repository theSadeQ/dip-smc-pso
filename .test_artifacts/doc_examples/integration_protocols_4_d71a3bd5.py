# Example from: docs\technical\integration_protocols.md
# Index: 4
# Runnable: False
# Hash: d71a3bd5

class PSOFactoryIntegration:
    """PSO-Factory integration layer."""

    def __init__(self, controller_type: str, plant_model_config: dict):
        self.controller_type = controller_type
        self.plant_config = plant_model_config
        self.gain_bounds = self._get_theoretical_bounds()

    def create_optimization_objective(
        self,
        performance_metrics: List[str],
        weights: Optional[List[float]] = None
    ) -> Callable:
        """Create PSO optimization objective function."""

        def objective_function(gains: np.ndarray) -> float:
            try:
                # Create controller with proposed gains
                controller = create_controller(
                    self.controller_type,
                    gains=gains.tolist()
                )

                # Create plant model
                plant_model = PlantModelRegistry.create_model(
                    'simplified_dip',
                    self.plant_config
                )

                # Create bridge
                bridge = ControllerPlantBridge(controller, plant_model)

                # Run simulation
                performance = self._evaluate_performance(
                    bridge,
                    performance_metrics
                )

                # Compute weighted cost
                if weights is None:
                    weights = [1.0] * len(performance_metrics)

                total_cost = sum(w * p for w, p in zip(weights, performance))
                return total_cost

            except Exception as e:
                # Return high cost for invalid configurations
                return 1e6

        return objective_function

    def _evaluate_performance(
        self,
        bridge: ControllerPlantBridge,
        metrics: List[str]
    ) -> List[float]:
        """Evaluate controller performance metrics."""

        # Standard test scenario
        initial_state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])  # Small perturbation
        dt = 0.001
        t_final = 10.0
        steps = int(t_final / dt)

        # Simulation
        state = initial_state.copy()
        states = [state.copy()]
        controls = []

        for _ in range(steps):
            state, metadata = bridge.step(state, dt)
            states.append(state.copy())
            controls.append(metadata['control_value'])

        states = np.array(states)
        controls = np.array(controls)

        # Compute metrics
        results = []
        for metric in metrics:
            if metric == 'settling_time':
                results.append(self._compute_settling_time(states, dt))
            elif metric == 'overshoot':
                results.append(self._compute_overshoot(states))
            elif metric == 'control_effort':
                results.append(self._compute_control_effort(controls))
            elif metric == 'steady_state_error':
                results.append(self._compute_steady_state_error(states))
            else:
                raise ValueError(f"Unknown metric: {metric}")

        return results

    def _get_theoretical_bounds(self) -> Tuple[List[float], List[float]]:
        """Get theoretical bounds for optimization."""
        return get_gain_bounds_for_pso(SMCType(self.controller_type))