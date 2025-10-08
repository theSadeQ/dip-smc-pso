# Example from: docs\PATTERNS.md
# Index: 4
# Runnable: True
# Hash: 01eb4200

# src/simulation/strategies/monte_carlo.py (lines 16-71)

from ..core.interfaces import SimulationStrategy

class MonteCarloStrategy(SimulationStrategy):
    """Monte Carlo simulation strategy for statistical analysis."""

    def __init__(self, n_samples: int = 1000, parallel: bool = True):
        self.n_samples = n_samples
        self.parallel = parallel

    def analyze(self, simulation_fn: Callable,
                parameters: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Perform Monte Carlo analysis with parameter distributions."""
        param_distributions = parameters.get('distributions', {})
        samples = self._generate_samples(param_distributions)

        if self.parallel:
            results = self._run_parallel_simulations(simulation_fn, samples)
        else:
            results = self._run_sequential_simulations(simulation_fn, samples)

        return self._analyze_results(results, samples)