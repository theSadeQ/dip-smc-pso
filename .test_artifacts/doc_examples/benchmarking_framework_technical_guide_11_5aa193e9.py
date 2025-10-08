# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 11
# Runnable: True
# Hash: 5aa193e9

# benchmarks/comparison/method_comparison.py

class IntegrationMethodComparator:
    """Systematic comparison of integration methods."""

    def __init__(self, dynamics, physics_params: dict):
        self.dynamics = dynamics
        self.physics_params = physics_params

    def compare_methods(self, methods: List[str], x0: np.ndarray,
                       t_span: tuple, dt_values: List[float]) -> dict:
        """Compare multiple integration methods.

        Parameters
        ----------
        methods : list of str
            Method names: ['Euler', 'RK4', 'RK45']
        x0 : np.ndarray
            Initial state
        t_span : tuple
            Time span
        dt_values : list of float
            Time steps to test

        Returns
        -------
        dict
            Comparison results for all methods
        """
        from benchmarks.integration import EulerIntegrator, RK4Integrator, AdaptiveRK45Integrator
        from benchmarks.analysis import compute_energy_conservation, estimate_convergence_order

        integrators = {
            'Euler': EulerIntegrator(self.dynamics),
            'RK4': RK4Integrator(self.dynamics),
            'RK45': AdaptiveRK45Integrator(self.dynamics)
        }

        results = {}

        for method_name in methods:
            integrator = integrators[method_name]

            # Convergence analysis
            convergence = estimate_convergence_order(integrator, x0, t_span, dt_values)

            # Energy conservation (for frictionless system)
            result = integrator.integrate(x0, t_span, dt=min(dt_values))
            energy_analysis = compute_energy_conservation(
                result['t'], result['x'], self.physics_params
            )

            # Performance measurement
            import time
            start = time.time()
            _ = integrator.integrate(x0, t_span, dt=min(dt_values))
            elapsed = time.time() - start

            results[method_name] = {
                'convergence_order': convergence['convergence_order'],
                'energy_drift': energy_analysis['relative_drift'],
                'computation_time': elapsed,
                'errors': convergence['errors']
            }

        return results