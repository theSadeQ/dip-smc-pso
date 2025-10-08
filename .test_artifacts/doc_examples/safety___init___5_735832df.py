# Example from: docs\reference\simulation\safety___init__.md
# Index: 5
# Runnable: True
# Hash: 735832df

from src.simulation.safety import SafetyRecovery

# Configure recovery
recovery = SafetyRecovery(
    state_bounds=(-10, 10),
    control_bounds=(-100, 100),
    recovery_mode='qp'  # or 'projection', 'fallback'
)

# Simulation with safety recovery
for i in range(N_steps):
    u = controller.compute(x)

    # Check for violations
    if recovery.check_violation(x, u):
        x_safe, u_safe = recovery.recover(x, u)
        x = integrator.integrate(dynamics, x_safe, u_safe, dt)
    else:
        x = integrator.integrate(dynamics, x, u, dt)