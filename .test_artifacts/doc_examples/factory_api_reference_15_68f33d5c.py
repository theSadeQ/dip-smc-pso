# Example from: docs\factory\factory_api_reference.md
# Index: 15
# Runnable: True
# Hash: 68f33d5c

hybrid_params = {
    'gains': List[float],           # [k1, k2, λ1, λ2] - 4 surface gains
    'hybrid_mode': HybridMode,      # Hybrid mode enumeration
    'max_force': float,             # Maximum control force [N]
    'dt': float,                    # Time step [s]
    'classical_config': ClassicalSMCConfig,  # Sub-controller configuration
    'adaptive_config': AdaptiveSMCConfig     # Sub-controller configuration
}