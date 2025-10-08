# Example from: docs\factory\factory_api_reference.md
# Index: 13
# Runnable: False
# Hash: 2d05e683

adaptive_params = {
    'gains': List[float],           # [k1, k2, λ1, λ2, γ] - 5 elements
    'max_force': float,             # Maximum control force [N]
    'dt': float,                    # Time step [s]
    'leak_rate': float,             # Adaptation leak rate
    'adapt_rate_limit': float,      # Maximum adaptation rate
    'K_min': float,                 # Minimum switching gain
    'K_max': float,                 # Maximum switching gain
    'K_init': float,                # Initial switching gain
    'alpha': float,                 # Adaptation law parameter
    'boundary_layer': float,        # Boundary layer thickness
    'smooth_switch': bool           # Enable smooth switching
}