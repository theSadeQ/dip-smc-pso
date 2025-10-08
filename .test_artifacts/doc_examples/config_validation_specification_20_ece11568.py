# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 20
# Runnable: False
# Hash: ece11568

# example-metadata:
# runnable: false

def get_surface_gains(self) -> List[float]:
    """Get sliding surface gains [k1, k2, λ1, λ2]."""
    return self.gains[:4]

def get_effective_controllability_threshold(self) -> float:
    """Get effective controllability threshold."""
    # Implementation shown above

def to_dict(self) -> dict:
    """Convert configuration to dictionary."""
    # Returns serializable dictionary

@classmethod
def from_dict(cls, config_dict: dict, dynamics_model=None) -> 'ClassicalSMCConfig':
    """Create configuration from dictionary."""
    # Factory method for deserialization

@classmethod
def create_default(cls, gains: List[float], max_force: float = 100.0,
                  dt: float = 0.01, boundary_layer: float = 0.01, **kwargs) -> 'ClassicalSMCConfig':
    """Create configuration with sensible defaults."""
    # Factory method with defaults