# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 9
# Runnable: True
# Hash: 16e5896d

hybrid_params = {
    'gains': [18.0, 12.0, 10.0, 8.0],     # [k1, k2, λ1, λ2]
    'hybrid_mode': HybridMode.CLASSICAL_ADAPTIVE,  # Initial mode
    'max_force': 150.0,                   # Maximum control force [N]
    'dt': 0.001,                          # Time step [s]
    'classical_config': classical_config,  # Sub-controller configuration
    'adaptive_config': adaptive_config,    # Sub-controller configuration
}