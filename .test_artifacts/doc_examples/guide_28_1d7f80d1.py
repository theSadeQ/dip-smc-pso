# Example from: docs\optimization_simulation\guide.md
# Index: 28
# Runnable: False
# Hash: 1d7f80d1

class PSOTuner:
    """High-throughput, vectorized tuner for sliding-mode controllers."""

    def __init__(
        self,
        controller_factory: Callable[[np.ndarray], Any],
        config: Union[ConfigSchema, str, Path],
        seed: Optional[int] = None,
        rng: Optional[np.random.Generator] = None,
        *,
        instability_penalty_factor: float = 100.0
    ):
        """
        Initialize PSO tuner.

        Parameters
        ----------
        controller_factory : callable
            Function returning controller given gain vector
        config : ConfigSchema or path
            Configuration object or path to YAML
        seed : int, optional
            Random seed for reproducibility
        rng : np.random.Generator, optional
            External PRNG (overrides seed if provided)
        instability_penalty_factor : float
            Scale factor for instability penalties (default: 100.0)
        """

    def optimise(
        self,
        *args,
        iters_override: Optional[int] = None,
        n_particles_override: Optional[int] = None,
        options_override: Optional[Dict[str, float]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run PSO optimization.

        Parameters
        ----------
        iters_override : int, optional
            Override config iterations
        n_particles_override : int, optional
            Override config swarm size
        options_override : dict, optional
            Override PSO hyperparameters (c1, c2, w)

        Returns
        -------
        dict
            {
                "best_cost": float,
                "best_pos": np.ndarray,
                "history": {"cost": np.ndarray, "pos": np.ndarray}
            }
        """