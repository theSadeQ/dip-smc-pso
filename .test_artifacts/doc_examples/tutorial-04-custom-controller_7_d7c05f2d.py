# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 7
# Runnable: False
# Hash: d7c05f2d

def __init__(self, ...):
    # ... existing code ...
    self.use_integral = True
    self.k_integral = 2.0  # Integral gain

def compute_control(self, state, state_vars, history):
    # Initialize integral term if not present
    if 'integral_s' not in state_vars:
        state_vars['integral_s'] = 0.0

    # Compute sliding surface
    s = self.compute_sliding_surface(state)

    # Update integral term
    dt = 0.01  # Get from config
    state_vars['integral_s'] += s * dt

    # Control law with integral term
    control = -self.K * self.switching_function(s) - self.k_integral * state_vars['integral_s']

    # Saturate
    control = saturate(control, -self.max_force, self.max_force)

    return control, state_vars, history