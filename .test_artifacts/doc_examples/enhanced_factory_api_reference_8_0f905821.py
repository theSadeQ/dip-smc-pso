# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 8
# Runnable: False
# Hash: 0f905821

# example-metadata:
# runnable: false

adaptive_params = {
    'gains': [25.0, 18.0, 15.0, 10.0, 4.0],  # [k1, k2, λ1, λ2, γ]
    'max_force': 150.0,             # Maximum control force [N]
    'dt': 0.001,                    # Time step [s]
    'leak_rate': 0.01,              # Leakage factor σ
    'dead_zone': 0.05,              # Dead zone thickness
    'K_min': 0.1,                   # Minimum adaptive gain
    'K_max': 100.0,                 # Maximum adaptive gain
    'alpha': 0.5                    # Adaptation smoothing factor
}