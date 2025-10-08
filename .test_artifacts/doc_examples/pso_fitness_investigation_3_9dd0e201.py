# Example from: docs\testing\reports\2025-09-30\pso_fitness_investigation.md
# Index: 3
# Runnable: True
# Hash: 9dd0e201

def _normalise(self, val: np.ndarray, denom: float) -> np.ndarray:
    """Safely normalise with threshold check"""
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = val / denom
    thr = float(self.normalisation_threshold)  # Default: 1e-12
    return np.where(denom > thr, ratio, val)