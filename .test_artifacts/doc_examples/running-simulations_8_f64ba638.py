# Example from: docs\guides\how-to\running-simulations.md
# Index: 8
# Runnable: True
# Hash: f64ba638

from scipy.integrate import solve_ivp

def dip_dynamics(t, state, controller, state_vars, history):
    """Dynamics function for scipy ODE solver."""
    u, state_vars, history = controller.compute_control(state, state_vars, history)

    # Compute state derivatives (use your dynamics model)
    dstate = dynamics.compute_derivatives(state, u)

    return dstate

# Solve using RK45 (adaptive)
solution = solve_ivp(
    lambda t, s: dip_dynamics(t, s, controller, state_vars, history),
    t_span=(0, 5.0),
    y0=initial_state,
    method='RK45',
    rtol=1e-6,
    atol=1e-9
)

time = solution.t
state = solution.y.T