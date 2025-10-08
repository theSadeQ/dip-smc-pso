# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 12
# Runnable: False
# Hash: c6a0082f

# example-metadata:
# runnable: false

class PSOTuner:
    """High-performance PSO tuner for SMC controllers."""

    def __init__(self,
                 controller_factory: Callable[[np.ndarray], PSO_ControllerInterface],
                 config: Union[ConfigSchema, str, Path],
                 seed: Optional[int] = None,
                 rng: Optional[np.random.Generator] = None,
                 **kwargs) -> None:
        """Initialize PSO tuner with controller factory.

        Parameters
        ----------
        controller_factory : Callable
            Function mapping gain vectors to controller instances.
            Must return objects implementing PSO_ControllerInterface.
        config : ConfigSchema or path
            System configuration with PSO parameters
        seed : int, optional
            Random seed for reproducibility
        rng : np.random.Generator, optional
            External random number generator
        **kwargs
            Additional PSO parameters
        """

    def optimize(self,
                 bounds: Optional[Tuple[np.ndarray, np.ndarray]] = None,
                 n_particles: Optional[int] = None,
                 n_iterations: Optional[int] = None,
                 **kwargs) -> Dict[str, Any]:
        """Run PSO optimization.

        Parameters
        ----------
        bounds : tuple of arrays, optional
            (lower_bounds, upper_bounds) for gain parameters
        n_particles : int, optional
            Number of particles in swarm
        n_iterations : int, optional
            Maximum optimization iterations
        **kwargs
            Additional PSO options

        Returns
        -------
        Dict[str, Any]
            Optimization results with keys:
            - 'best_gains': Optimal gain vector
            - 'best_cost': Best fitness value
            - 'cost_history': Convergence history
            - 'success': Optimization success flag
            - 'message': Status message
        """