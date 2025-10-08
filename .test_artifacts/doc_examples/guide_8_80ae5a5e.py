# Example from: docs\optimization_simulation\guide.md
# Index: 8
# Runnable: True
# Hash: 80ae5a5e

def _guard_energy(state: np.ndarray, limits: dict) -> None:
    """Verify total energy within specified limits."""
    energy = np.sum(state**2, axis=-1)
    max_energy = limits.get('max', np.inf)
    if np.any(energy > max_energy):
        raise ValueError(f"Energy {energy.max():.2f} exceeds limit {max_energy:.2f}")