# Example from: docs\controllers\control_primitives_reference.md
# Index: 11
# Runnable: False
# Hash: 83584041

# example-metadata:
# runnable: false

class STAOutput(NamedTuple):
    """Return type for SuperTwistingSMC.compute_control().

    Attributes:
        u: Bounded control input (N)
        state: Auxiliary integrator states (z, sigma)
        history: History dictionary
    """
    u: float
    state: Tuple[float, ...]
    history: Dict[str, Any]