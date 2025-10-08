# Example from: docs\PSO_Documentation_Validation_Report.md
# Index: 2
# Runnable: False
# Hash: d19843f9

def __init__(
    self,
    controller_factory: Callable[[np.ndarray], Any],
    config: Union[ConfigSchema, str, Path],
    seed: Optional[int] = None,
    rng: Optional[np.random.Generator] = None,
    *,
    instability_penalty_factor: float = 100.0,
) -> None:
    """Initialise the PSOTuner.

    Parameters
    ----------
    controller_factory : Callable[[np.ndarray], Any]
        A function returning a controller instance given a gain vector.
    config : ConfigSchema or path-like
        A validated configuration object or path to the YAML file.
    seed : int or None, optional
        Seed to initialise the local RNG.  When ``None``, the seed from
        the configuration (``global_seed``) is used if present; otherwise
        the RNG is unseeded.
    rng : numpy.random.Generator or None, optional
        External PRNG.  If provided, this generator is used directly and
        ``seed`` is ignored.
    instability_penalty_factor : float, optional
        Scale factor used to compute the penalty for unstable simulations.
        The penalty is computed as
        ``instability_penalty_factor * (norm_ise + norm_u + norm_du + norm_sigma)``.
        Larger values penalise instability more heavily.  Default is 100.
    """