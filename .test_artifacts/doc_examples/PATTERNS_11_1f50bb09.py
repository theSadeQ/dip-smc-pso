# Example from: docs\PATTERNS.md
# Index: 11
# Runnable: False
# Hash: 1f50bb09

# BAD: Tight coupling (hardcoded dependency)
class ClassicalSMC:
    def __init__(self, gains):
        self.gains = gains
        self.dynamics = DIPDynamics()  # ❌ Hardcoded dependency

    def compute_control(self, state):
        # Can't test without real dynamics
        dynamics_info = self.dynamics.compute(state, u=0)

# GOOD: Dependency Injection
class ClassicalSMC:
    def __init__(self, gains, dynamics_model=None):  # ✅ Injected dependency
        self.gains = gains
        self._dynamics_ref = weakref.ref(dynamics_model) if dynamics_model else None

    def compute_control(self, state):
        if self._dynamics_ref:
            dynamics = self._dynamics_ref()  # Use injected dynamics
        # Controller logic works with or without dynamics