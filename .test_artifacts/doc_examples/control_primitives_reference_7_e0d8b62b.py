# Example from: docs\controllers\control_primitives_reference.md
# Index: 7
# Runnable: False
# Hash: e0d8b62b

class ClassicalSMCOutput(NamedTuple):
    """Return type for ClassicalSMC.compute_control().

    Attributes:
        u: Saturated control input (N)
        state: Internal controller state (empty tuple for stateless)
        history: History dictionary for debugging/plotting
    """
    u: float
    state: Tuple[Any, ...]
    history: Dict[str, Any]