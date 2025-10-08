# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 13
# Runnable: False
# Hash: 4820f98b

# Controller with internal state (e.g., adaptation)
class AdaptiveController(Controller):
    def compute_control(self, state, state_vars, history):
        # Extract previous state
        K = state_vars.get('K', self.K_initial)
        integral = state_vars.get('integral', 0.0)

        # Compute control
        s = self.compute_sliding_surface(state)
        K_new = K + self.gamma * abs(s) * self.dt
        integral_new = integral + s * self.dt

        u = -K_new * np.tanh(s / self.epsilon)

        # Return updated state
        return u, {'K': K_new, 'integral': integral_new}, history

# State is fully captured in state_vars
state_vars = {}
for i in range(100):
    u, state_vars, history = controller.compute_control(state, state_vars, history)
    # state_vars contains full controller state for reproducibility