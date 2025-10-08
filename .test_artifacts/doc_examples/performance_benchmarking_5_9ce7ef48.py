# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 5
# Runnable: True
# Hash: 9ce7ef48

import cProfile
import pstats

def profile_controller_step():
    """Profile control loop with cProfile"""
    profiler = cProfile.Profile()

    profiler.enable()
    for _ in range(1000):
        u = controller.compute_control(state)
        state = dynamics.step(state, u, dt=0.01)
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions