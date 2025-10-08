# Example from: docs\pso_integration_system_architecture.md
# Index: 2
# Runnable: False
# Hash: cea8f0e7

def create_controller(controller_type: str, gains: np.ndarray, **kwargs) -> Controller:
    """
    PSO-compatible factory interface.

    Integration Requirements:
    1. Standardized gain vector interface across all controller types
    2. Built-in parameter validation with bounds checking
    3. Consistent actuator saturation limits (max_force)
    4. Optional validate_gains() method for PSO pre-filtering
    """

# Controller-Specific Interfaces:
class ClassicalSMC:
    def __init__(self, gains: np.ndarray): # [c1, λ1, c2, λ2, K, kd]
    def validate_gains(self, particles: np.ndarray) -> np.ndarray: # Optional
    @property
    def max_force(self) -> float: # Required for PSO

class STASMC:
    def __init__(self, gains: np.ndarray): # [K1, K2, k1, k2, λ1, λ2]
    # Same interface requirements...

class AdaptiveSMC:
    def __init__(self, gains: np.ndarray): # [c1, λ1, c2, λ2, γ]
    # Same interface requirements...