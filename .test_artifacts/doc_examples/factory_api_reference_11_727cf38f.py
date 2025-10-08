# Example from: docs\factory\factory_api_reference.md
# Index: 11
# Runnable: True
# Hash: 727cf38f

sta_params = {
    'gains': List[float],           # [K1, K2, k1, k2, λ1, λ2] - 6 elements
    'max_force': float,             # Maximum control force [N]
    'dt': float,                    # Time step [s]
    'power_exponent': float,        # Super-twisting power (typically 0.5)
    'regularization': float,        # Numerical regularization
    'boundary_layer': float,        # Boundary layer thickness
    'switch_method': str            # Switching function ('tanh', 'sign', 'linear')
}