# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 8
# Runnable: True
# Hash: f3dcfc01

if diversity < threshold_low:
    omega = increase(omega)    # Increase exploration
    c1 = increase(c1)
elif diversity > threshold_high:
    omega = decrease(omega)    # Increase exploitation
    c2 = increase(c2)