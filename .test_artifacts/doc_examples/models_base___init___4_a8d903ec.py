# Example from: docs\reference\plant\models_base___init__.md
# Index: 4
# Runnable: False
# Hash: a8d903ec

# example-metadata:
# runnable: false

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