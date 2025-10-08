# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 23
# Runnable: True
# Hash: 2327b89a

import time

def profile_classical_smc(controller, state):
    """Profile computational cost of control law."""

    import time

    timings = {}

    # Sliding surface
    t0 = time.perf_counter()
    sigma = controller._compute_sliding_surface(state)
    timings['sliding_surface'] = (time.perf_counter() - t0) * 1e6  # μs

    # Equivalent control
    t0 = time.perf_counter()
    u_eq = controller._compute_equivalent_control(state)
    timings['equivalent_control'] = (time.perf_counter() - t0) * 1e6

    # Full control
    t0 = time.perf_counter()
    result = controller.compute_control(state, (), {})
    timings['total'] = (time.perf_counter() - t0) * 1e6

    return timings