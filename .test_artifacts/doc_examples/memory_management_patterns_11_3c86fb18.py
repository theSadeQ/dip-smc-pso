# Example from: docs\memory_management_patterns.md
# Index: 11
# Runnable: True
# Hash: 3c86fb18

# Uses weakref for dynamics model
if dynamics_model is not None:
    self._dynamics_ref = weakref.ref(dynamics_model)
else:
    self._dynamics_ref = lambda: None

# Access via property
@property
def dyn(self):
    return self._dynamics_ref() if callable(self._dynamics_ref) else None