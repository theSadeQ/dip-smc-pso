# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 6
# Runnable: True
# Hash: 32a08cbe

def _guard_energy(state: np.ndarray, energy_limit: float, t: float) -> None:
    """Check total energy against limit."""
    total_energy = np.sum(state**2)
    if total_energy > energy_limit:
        raise ValueError(
            f"Energy violation at t={t:.3f}: "
            f"{total_energy:.2f} > {energy_limit:.2f}"
        )