# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 2
# Runnable: False
# Hash: f811156f

# example-metadata:
# runnable: false

# Richardson extrapolation
def estimate_convergence_order(method, x0, t_span, dt_values):
    errors = []
    for dt in dt_values:
        x_h = method.integrate(x0, t_span, dt)
        x_ref = method.integrate(x0, t_span, dt/10)  # Fine reference
        errors.append(norm(x_h[-1] - x_ref[-1]))

    # Fit log(error) vs log(dt)
    order = polyfit(log(dt_values), log(errors), 1)[0]
    return order