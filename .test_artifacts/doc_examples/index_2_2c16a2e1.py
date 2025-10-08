# Example from: docs\plant\index.md
# Index: 2
# Runnable: True
# Hash: 2c16a2e1

from scipy.integrate import solve_ivp

def dynamics_ode(t, state):
    control = [0.0]
    result = dynamics.compute_dynamics(state, control, time=t)
    return result.state_derivative if result.success else np.zeros(6)

# Integrate
sol = solve_ivp(dynamics_ode, t_span=[0, 5], y0=state0, method='RK45', rtol=1e-8)

# Check energy conservation
E0 = dynamics.compute_total_energy(state0)
E_final = dynamics.compute_total_energy(sol.y[:, -1])
energy_drift = abs(E_final - E0) / E0
print(f"Energy drift: {energy_drift:.2%}")