# Example from: docs\technical\integration_protocols.md
# Index: 6
# Runnable: False
# Hash: 2a4cbc55

class VectorSimulationIntegration:
    """Integration with vectorized simulation engines."""

    def __init__(self, controller_factory_config: dict):
        self.factory_config = controller_factory_config

    def create_batch_simulation(
        self,
        controller_types: List[str],
        gain_sets: List[List[float]],
        initial_conditions: List[np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """Create batch simulation for multiple configurations."""

        # Validate inputs
        assert len(controller_types) == len(gain_sets)
        assert len(controller_types) == len(initial_conditions)

        # Create controllers
        controllers = []
        for ctrl_type, gains in zip(controller_types, gain_sets):
            controller = create_controller(ctrl_type, gains=gains)
            controllers.append(controller)

        # Prepare simulation data
        simulation_config = {
            'controllers': controllers,
            'initial_conditions': np.array(initial_conditions),
            'dt': self.factory_config.get('dt', 0.001),
            't_final': self.factory_config.get('t_final', 10.0)
        }

        # Run vectorized simulation
        results = run_vectorized_simulation(simulation_config)

        return results

    def create_parameter_sweep(
        self,
        controller_type: str,
        parameter_ranges: Dict[str, Tuple[float, float]],
        n_samples: int
    ) -> Dict[str, Any]:
        """Create parameter sweep simulation."""

        # Generate parameter combinations
        parameter_combinations = self._generate_parameter_combinations(
            parameter_ranges,
            n_samples
        )

        # Create controllers for each combination
        controllers = []
        for params in parameter_combinations:
            controller = create_controller(controller_type, gains=params)
            controllers.append(controller)

        # Run batch simulation
        results = self.create_batch_simulation(
            [controller_type] * len(controllers),
            parameter_combinations,
            [np.zeros(6)] * len(controllers)  # Standard initial condition
        )

        return {
            'parameters': parameter_combinations,
            'results': results,
            'analysis': self._analyze_parameter_sweep(results)
        }