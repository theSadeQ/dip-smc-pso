# Example from: docs\analysis\view_conversion_recommendations.md
# Index: 8
# Runnable: True
# Hash: d3470a5a

# Before/after memory profiling
from memory_profiler import profile

@profile
def run_5s_simulation():
    t, x, u = run_simulation(
        controller=controller,
        dynamics_model=dynamics,
        sim_time=5.0,
        dt=0.01,
        initial_state=[0.1, 0.05, 0.02, 0, 0, 0]
    )
    return x

# Expected improvement: ~400KB reduction (2.3x overhead → ~1.2x overhead)