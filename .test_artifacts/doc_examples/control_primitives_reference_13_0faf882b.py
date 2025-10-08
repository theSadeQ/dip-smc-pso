# Example from: docs\controllers\control_primitives_reference.md
# Index: 13
# Runnable: False
# Hash: 0faf882b

# example-metadata:
# runnable: false

class HybridSTAOutput(NamedTuple):
    """Return type for HybridAdaptiveSTASMC.compute_control().

    Attributes:
        u: Saturated control input (N)
        state: Adaptive gains and integral state (k1, k2, u_int)
        history: History dictionary
        sigma: Current sliding surface value
    """
    u: float
    state: Tuple[float, ...]
    history: Dict[str, Any]
    sigma: float