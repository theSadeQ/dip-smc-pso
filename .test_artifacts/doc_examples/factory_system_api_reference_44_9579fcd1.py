# Example from: docs\api\factory_system_api_reference.md
# Index: 44
# Runnable: True
# Hash: 9579fcd1

if controller_type == 'adaptive_smc' and len(gains) != 5:
    raise ValueError("Adaptive SMC requires exactly 5 gains: [k1, k2, lam1, lam2, gamma]")