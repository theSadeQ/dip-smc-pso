# Example from: docs\technical\controller_factory_integration.md
# Index: 6
# Runnable: True
# Hash: 1f20cc09

@dataclass(frozen=True)
class STASMCConfig:
    gains: List[float]                     # [K1, K2, c1, λ1, c2, λ2]
    max_force: float
    dt: float = 0.001
    K1: float = 4.0                        # First-order gain
    K2: float = 0.4                        # Second-order gain
    power_exponent: float = 0.5             # Finite-time convergence exponent
    regularization: float = 1e-6