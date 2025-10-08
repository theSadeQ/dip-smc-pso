# Example from: docs\controllers\control_primitives_reference.md
# Index: 9
# Runnable: False
# Hash: ea15a773

class AdaptiveSMCOutput(NamedTuple):
    """Return type for AdaptiveSMC.compute_control().

    Attributes:
        u: Saturated control input (N)
        state: Updated adaptation states (e.g., K_adaptive)
        history: History dictionary
        sigma: Current sliding surface value
    """
    u: float
    state: Tuple[float, ...]
    history: Dict[str, Any]
    sigma: float