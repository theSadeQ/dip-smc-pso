# Example from: docs\reference\plant\models_simplified_physics.md
# Index: 4
# Runnable: False
# Hash: 2fe0289a

# Performance optimization
import cProfile
import pstats

# Profile critical code path
profiler = cProfile.Profile()
profiler.enable()

# ... run intensive operations ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 time consumers