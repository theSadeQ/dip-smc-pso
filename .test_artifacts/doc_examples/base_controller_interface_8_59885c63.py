# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 8
# Runnable: True
# Hash: 59885c63

def compute_control(self, state, state_vars, history):
    # Append to history
    history['states'].append(state)
    history['times'].append(t)

    # Compute derivative from history
    if len(history['states']) >= 2:
        derivative = (state - history['states'][-2]) / self.dt

    return u, state_vars, history