# Example from: docs\guides\api\optimization.md
# Index: 13
# Runnable: False
# Hash: c5e5c0f6

# example-metadata:
# runnable: false

# Instead of wide bounds [0.1, 50]
wide_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

# Use narrower bounds based on prior knowledge
narrow_bounds = [
    (5.0, 15.0),   # k1: expect around 10
    (5.0, 15.0),   # k2: expect around 10
    (10.0, 20.0),  # λ1: expect around 15
    (8.0, 16.0),   # λ2: expect around 12
    (30.0, 70.0),  # K: expect around 50
    (1.0, 10.0),   # ε: expect around 5
]

tuner = PSOTuner(SMCType.CLASSICAL, bounds=narrow_bounds)