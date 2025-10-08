# Example from: docs\technical\controller_factory_integration.md
# Index: 5
# Runnable: True
# Hash: 24ee622b

@dataclass(frozen=True)
class ClassicalSMCConfig:
    gains: List[float]                     # [k1, k2, λ1, λ2, K, kd]
    max_force: float
    boundary_layer: float
    dt: float = 0.01
    switch_method: Literal["tanh", "linear", "sign"] = "tanh"
    regularization: float = 1e-10
    dynamics_model: Optional[object] = None