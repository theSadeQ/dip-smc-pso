# Example from: docs\optimization_simulation\guide.md
# Index: 4
# Runnable: False
# Hash: 4fbfe071

# example-metadata:
# runnable: false

def fallback_controller(t, x):
    """Simple PD controller as fallback."""
    return -10 * x[0] - 5 * x[3]  # Proportional to cart position and velocity

t_arr, x_arr, u_arr = run_simulation(
    controller=main_controller,
    dynamics_model=dynamics,
    sim_time=5.0,
    dt=0.01,
    initial_state=x0,
    fallback_controller=fallback_controller  # Activated on deadline miss
)