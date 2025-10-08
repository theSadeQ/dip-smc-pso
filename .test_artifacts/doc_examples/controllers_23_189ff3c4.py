# Example from: docs\guides\api\controllers.md
# Index: 23
# Runnable: True
# Hash: 189ff3c4

# Before: Saturates
controller = create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 500, 5], max_force=100)

# After: Reduced gains
controller = create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5], max_force=100)