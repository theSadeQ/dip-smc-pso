# Example from: docs\testing\testing_workflows_best_practices.md
# Index: 2
# Runnable: False
# Hash: a27448ff

# Step 2: GREEN - Implement minimal code to pass
# src/controllers/smc/classic_smc.py

class ClassicalSMC:
    def __init__(self, gains, max_force, boundary_layer=0.01, chattering_reduction=False):
        self.gains = gains
        self.max_force = max_force
        self.boundary_layer = boundary_layer
        self.chattering_reduction = chattering_reduction
        self.last_control = 0.0

    def compute_control(self, state, state_vars, history):
        # ... existing SMC logic ...
        control = u_eq + u_switch + u_derivative

        if self.chattering_reduction:
            # Simple low-pass filter
            alpha = 0.8
            control = alpha * self.last_control + (1 - alpha) * control

        self.last_control = control

        # Saturation
        control = np.clip(control, -self.max_force, self.max_force)
        return {'control': control}

# Run test → PASSES