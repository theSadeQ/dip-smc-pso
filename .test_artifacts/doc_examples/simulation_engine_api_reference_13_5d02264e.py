# Example from: docs\api\simulation_engine_api_reference.md
# Index: 13
# Runnable: False
# Hash: 5d02264e

# example-metadata:
# runnable: false

# Simple PD fallback controller
def pd_fallback(t, x):
    return -10 * x[0] - 5 * x[3]  # -Kp*x - Kd*x_dot

t, x, u = run_simulation(
    controller=complex_mpc_controller,
    dynamics_model=dynamics,
    sim_time=5.0,
    dt=0.01,
    initial_state=x0,
    fallback_controller=pd_fallback  # Engage if MPC exceeds 10ms
)