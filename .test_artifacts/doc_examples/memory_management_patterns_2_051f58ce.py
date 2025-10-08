# Example from: docs\memory_management_patterns.md
# Index: 2
# Runnable: True
# Hash: 051f58ce

# ✅ AFTER: Weakref prevents circular reference
import weakref

class Controller:
    def __init__(self, dynamics_model):
        if dynamics_model is not None:
            self._dynamics_ref = weakref.ref(dynamics_model)
        else:
            self._dynamics_ref = lambda: None

    @property
    def dyn(self):
        """Access dynamics via weakref."""
        return self._dynamics_ref() if callable(self._dynamics_ref) else None