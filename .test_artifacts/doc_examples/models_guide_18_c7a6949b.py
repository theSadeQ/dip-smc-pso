# Example from: docs\plant\models_guide.md
# Index: 18
# Runnable: True
# Hash: c7a6949b

from scipy.integrate import solve_ivp

def dynamics_ode(t, state):
    """ODE right-hand side for scipy integration."""
    control = np.array([0.0])  # No control input
    result = dynamics.compute_dynamics(state, control, time=t)
    return result.state_derivative if result.success else np.zeros(6)

# Initial state with energy
state0 = np.array([0.0, 0.2, -0.15, 0.0, 0.1, -0.05])
E0 = dynamics.compute_total_energy(state0)

# Integrate for 5 seconds
sol = solve_ivp(dynamics_ode, t_span=[0, 5], y0=state0,
                method='RK45', rtol=1e-8)

# Check energy conservation
E_final = dynamics.compute_total_energy(sol.y[:, -1])
energy_drift = abs(E_final - E0) / E0

print(f"Initial energy: {E0:.6f} J")
print(f"Final energy: {E_final:.6f} J")
print(f"Energy drift: {energy_drift:.2e} ({energy_drift*100:.4f}%)")