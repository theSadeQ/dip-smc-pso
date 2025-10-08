# Example from: docs\testing\testing_workflows_best_practices.md
# Index: 3
# Runnable: False
# Hash: d509a87e

# example-metadata:
# runnable: false

# Step 3: REFACTOR - Clean up implementation
class ChatteringReduction:
    """Encapsulate chattering reduction logic."""

    def __init__(self, alpha=0.8):
        self.alpha = alpha
        self.last_control = 0.0

    def apply(self, control):
        """Apply low-pass filter to control signal."""
        filtered = self.alpha * self.last_control + (1 - self.alpha) * control
        self.last_control = filtered
        return filtered


class ClassicalSMC:
    def __init__(self, gains, max_force, boundary_layer=0.01, chattering_reduction=False):
        self.gains = gains
        self.max_force = max_force
        self.boundary_layer = boundary_layer

        if chattering_reduction:
            self.chattering_filter = ChatteringReduction()
        else:
            self.chattering_filter = None

    def compute_control(self, state, state_vars, history):
        # ... existing SMC logic ...
        control = u_eq + u_switch + u_derivative

        if self.chattering_filter:
            control = self.chattering_filter.apply(control)

        control = np.clip(control, -self.max_force, self.max_force)
        return {'control': control}

# Run test → STILL PASSES
# Run full test suite → ALL PASS