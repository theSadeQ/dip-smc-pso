# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 14
# Runnable: False
# Hash: 24f8ce6b

PSO_BOUNDS = {
    SMCType.CLASSICAL: {
        'lower': [1.0, 1.0, 1.0, 1.0, 5.0, 0.1],     # [k1, k2, λ1, λ2, K, kd]
        'upper': [30.0, 30.0, 20.0, 20.0, 50.0, 10.0]
    },
    SMCType.ADAPTIVE: {
        'lower': [2.0, 2.0, 1.0, 1.0, 0.5],          # [k1, k2, λ1, λ2, γ]
        'upper': [40.0, 40.0, 25.0, 25.0, 10.0]
    },
    SMCType.SUPER_TWISTING: {
        'lower': [3.0, 2.0, 2.0, 2.0, 0.5, 0.5],     # [K1, K2, k1, k2, λ1, λ2]
        'upper': [50.0, 30.0, 30.0, 30.0, 20.0, 20.0]
    },
    SMCType.HYBRID: {
        'lower': [2.0, 2.0, 1.0, 1.0],               # [k1, k2, λ1, λ2]
        'upper': [30.0, 30.0, 20.0, 20.0]
    }
}