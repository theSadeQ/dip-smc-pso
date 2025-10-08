# Example from: docs\api\optimization_module_api_reference.md
# Index: 4
# Runnable: True
# Hash: 21cb3c19

def optimise(
    self,
    *args: Any,
    iters_override: Optional[int] = None,
    n_particles_override: Optional[int] = None,
    options_override: Optional[Dict[str, float]] = None,
    **kwargs: Any,
) -> Dict[str, Any]: