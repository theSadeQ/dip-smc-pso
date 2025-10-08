# Example from: docs\CLAUDE.md
# Index: 13
# Runnable: False
# Hash: 032320f1

# ClassicalSMC implementation
if dynamics_model is not None:
    self._dynamics_ref = weakref.ref(dynamics_model)
else:
    self._dynamics_ref = lambda: None

@property
def dyn(self):
    """Access dynamics model via weakref."""
    if self._dynamics_ref is not None:
        return self._dynamics_ref()
    return None