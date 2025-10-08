# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 15
# Runnable: True
# Hash: 3d4e12ba

def get_effective_controllability_threshold(self) -> float:
    if self.controllability_threshold is not None:
        return self.controllability_threshold
    # Default: scale with surface gains
    return 0.05 * (self.k1 + self.k2)