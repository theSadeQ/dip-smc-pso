# Example from: docs\reference\controllers\smc_core_sliding_surface.md
# Index: 2
# Runnable: True
# Hash: 4c8fdff9

# Compute surface derivative ds/dt
state_dot = np.array([0.0, 0.0, 0.1, -0.5, 0.05, -0.3])
s_dot = surface.compute_derivative(state, state_dot)
print(f"Surface derivative: {s_dot:.4f}")

# Check sliding condition
if abs(s) < 0.01 and s * s_dot < 0:
    print("Sliding mode reached and maintained")