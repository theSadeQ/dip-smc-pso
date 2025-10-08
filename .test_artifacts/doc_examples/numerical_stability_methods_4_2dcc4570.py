# Example from: docs\theory\numerical_stability_methods.md
# Index: 4
# Runnable: True
# Hash: 2dcc4570

# Controllability threshold: decouples from boundary layer
if abs(L_Minv_B) < self.eq_threshold:
    return 0.0  # Disable equivalent control when poorly controllable