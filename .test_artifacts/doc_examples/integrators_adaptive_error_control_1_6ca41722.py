# Example from: docs\reference\simulation\integrators_adaptive_error_control.md
# Index: 1
# Runnable: False
# Hash: 6ca41722

# example-metadata:
# runnable: false

while t < t_final:
    # Attempt integration step
    y_new, y_hat = integrate_step(t, y, dt)

    # Estimate error
    error = norm((y_new - y_hat) / (atol + abs(y_new) * rtol))

    # Acceptance decision
    if error <= 1.0:
        # Accept step
        t += dt
        y = y_new

        # Increase step size for next step
        dt_new = 0.9 * dt * error**(-1/5)
    else:
        # Reject step
        # Decrease step size and retry
        dt_new = 0.9 * dt * error**(-1/4)

    # Apply safety bounds
    dt = clip(dt_new, dt_min, dt_max)