# Example from: docs\reports\pso_code_quality_beautification_assessment.md
# Index: 3
# Runnable: False
# Hash: bb7eb517

# example-metadata:
# runnable: false

# ✅ Excellent modern type hints
def _compute_cost_from_traj(
    self, t: np.ndarray, x_b: np.ndarray, u_b: np.ndarray, sigma_b: np.ndarray
) -> np.ndarray:

# ✅ Advanced union types and optionals
def optimise(
    self,
    *args: Any,
    iters_override: Optional[int] = None,
    n_particles_override: Optional[int] = None,
    options_override: Optional[Dict[str, float]] = None,
    **kwargs: Any,
) -> Dict[str, Any]: