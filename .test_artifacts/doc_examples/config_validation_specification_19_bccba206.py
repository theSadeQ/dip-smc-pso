# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 19
# Runnable: False
# Hash: bccba206

# example-metadata:
# runnable: false

@property
def k1(self) -> float:
    """Joint 1 position gain."""
    return self.gains[0]

@property
def k2(self) -> float:
    """Joint 2 position gain."""
    return self.gains[1]

@property
def lam1(self) -> float:
    """Joint 1 velocity gain (λ₁)."""
    return self.gains[2]

@property
def lam2(self) -> float:
    """Joint 2 velocity gain (λ₂)."""
    return self.gains[3]

@property
def K(self) -> float:
    """Switching gain."""
    return self.gains[4]

@property
def kd(self) -> float:
    """Derivative gain."""
    return self.gains[5]