# Example from: docs\memory_management_patterns.md
# Index: 1
# Runnable: True
# Hash: df7c2485

# ❌ BEFORE: Creates circular reference
class Controller:
    def __init__(self, dynamics_model):
        self._dynamics = dynamics_model  # Strong reference