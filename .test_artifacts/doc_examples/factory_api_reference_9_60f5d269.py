# Example from: docs\factory\factory_api_reference.md
# Index: 9
# Runnable: True
# Hash: 60f5d269

classical_params = {
    'gains': List[float],           # [k1, k2, λ1, λ2, K, kd] - 6 elements
    'max_force': float,             # Maximum control force [N]
    'boundary_layer': float,        # Boundary layer thickness
    'dt': float                     # Time step [s]
}