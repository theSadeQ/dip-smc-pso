# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 2
# Runnable: True
# Hash: 7b9d2980

bounds_sta = [
    (1.0, 100.0),  # K1 - first-order switching gain (larger)
    (1.0, 50.0),   # K2 - second-order gain (smaller, K2 < K1)
    (0.1, 50.0),   # k1 - surface gain
    (0.1, 50.0),   # k2 - surface gain
    (0.1, 50.0),   # λ1 - velocity gain
    (0.1, 50.0),   # λ2 - velocity gain
]