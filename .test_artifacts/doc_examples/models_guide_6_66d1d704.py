# Example from: docs\plant\models_guide.md
# Index: 6
# Runnable: False
# Hash: 66d1d704

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class SimplifiedDIPConfig:
    """Type-safe configuration for simplified DIP."""

    # Physical parameters - masses (kg)
    cart_mass: float
    pendulum1_mass: float
    pendulum2_mass: float

    # Lengths (m)
    pendulum1_length: float
    pendulum2_length: float
    pendulum1_com: float          # Center of mass distance
    pendulum2_com: float

    # Inertias (kg⋅m²)
    pendulum1_inertia: float
    pendulum2_inertia: float

    # Environmental
    gravity: float = 9.81

    # Friction (N⋅s/m or N⋅m⋅s/rad)
    cart_friction: float = 0.1
    joint1_friction: float = 0.01
    joint2_friction: float = 0.01

    # Numerical stability
    regularization_alpha: float = 1e-4
    max_condition_number: float = 1e14
    min_regularization: float = 1e-10