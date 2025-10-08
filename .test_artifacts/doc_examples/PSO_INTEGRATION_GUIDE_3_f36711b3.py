# Example from: docs\PSO_INTEGRATION_GUIDE.md
# Index: 3
# Runnable: True
# Hash: f36711b3

# PSO-friendly simplified interface
control = controller.compute_control(state)

# Full interface (backward compatibility)
control_output = controller.compute_control(state, state_vars, history)