# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 1
# Runnable: True
# Hash: 9adb2438

bounds_adaptive = [
    (0.1, 50.0),   # k1 - surface gain
    (0.1, 50.0),   # k2 - surface gain
    (0.1, 50.0),   # λ1 - velocity gain
    (0.1, 50.0),   # λ2 - velocity gain
    (0.01, 10.0),  # γ - adaptation rate (smaller range!)
]