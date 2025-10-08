# Example from: docs\guides\api\controllers.md
# Index: 22
# Runnable: True
# Hash: 538cc473

# Classical and STA: 6 gains
controller = create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5])

# Adaptive: 5 gains
controller = create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 0.5])

# Hybrid: 4 gains
controller = create_smc_for_pso(SMCType.HYBRID, [15, 12, 18, 15])