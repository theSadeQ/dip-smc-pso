# Example from: docs\api\optimization_module_api_reference.md
# Index: 2
# Runnable: True
# Hash: 6192d244

def __init__(
    self,
    controller_factory: Callable[[np.ndarray], Any],
    config: Union[ConfigSchema, str, Path],
    seed: Optional[int] = None,
    rng: Optional[np.random.Generator] = None,
    *,
    instability_penalty_factor: float = 100.0,
) -> None: