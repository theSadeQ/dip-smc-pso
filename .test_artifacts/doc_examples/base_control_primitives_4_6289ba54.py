# Example from: docs\reference\controllers\base_control_primitives.md
# Index: 4
# Runnable: True
# Hash: 6289ba54

from src.controllers.base.control_primitives import low_pass_filter

# Noisy control signal
u_noisy = 50.0 + 5.0 * np.random.randn()

# Filter parameters
omega_c = 20.0  # Cutoff frequency (rad/s)
dt = 0.01
tau = 1.0 / omega_c  # Time constant

# Apply filter
u_filtered_prev = 48.0  # Previous filtered value
u_filtered = low_pass_filter(u_noisy, u_filtered_prev, tau, dt)

print(f"Noisy control:    {u_noisy:.2f} N")
print(f"Filtered control: {u_filtered:.2f} N")