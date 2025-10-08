# Example from: docs\guides\api\configuration.md
# Index: 6
# Runnable: False
# Hash: ab42550e

# example-metadata:
# runnable: false

@dataclass
class DIPParams:
    """Double-inverted pendulum physics parameters."""
    m0: float = 1.5      # Cart mass (kg)
    m1: float = 0.5      # First pendulum mass (kg)
    m2: float = 0.75     # Second pendulum mass (kg)
    l1: float = 0.5      # First pendulum length (m)
    l2: float = 0.75     # Second pendulum length (m)
    I1: Optional[float] = None  # Auto-calculate if None
    I2: Optional[float] = None
    b0: float = 0.1      # Cart friction
    b1: float = 0.01     # Pendulum 1 friction
    b2: float = 0.01     # Pendulum 2 friction
    g: float = 9.81      # Gravity (m/s²)

    def __post_init__(self):
        """Auto-calculate inertias if not provided."""
        if self.I1 is None:
            self.I1 = (1/3) * self.m1 * self.l1**2
        if self.I2 is None:
            self.I2 = (1/3) * self.m2 * self.l2**2