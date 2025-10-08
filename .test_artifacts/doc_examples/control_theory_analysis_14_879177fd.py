# Example from: docs\testing\reports\2025-09-30\technical\control_theory_analysis.md
# Index: 14
# Runnable: False
# Hash: 879177fd

# Implementation Priority: MEDIUM
class MemoryEfficientController:
    def __init__(self, max_history=100):
        self.state_history = collections.deque(maxlen=max_history)
        self.control_history = collections.deque(maxlen=max_history)

    def compute_control(self, state):
        # Use in-place operations to minimize allocations
        control_signal = self._compute_control_inplace(state)

        # Bounded history storage
        self.state_history.append(state.copy())
        self.control_history.append(control_signal.copy())

        return control_signal