# Example from: docs\optimization_simulation\guide.md
# Index: 12
# Runnable: True
# Hash: b83989e0

@field_validator("cart_mass", "pendulum1_mass", "pendulum2_mass")
def _must_be_strictly_positive(cls, v: float, info) -> float:
    if v <= 0.0:
        raise ValueError(f"{info.field_name} must be > 0 (conservation of mass)")
    return v