# Example from: docs\guides\api\controllers.md
# Index: 20
# Runnable: True
# Hash: cfbaab78

from src.controllers import SMCType, create_smc_for_pso

controllers = {
    'Classical': create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5]),
    'STA': create_smc_for_pso(SMCType.SUPER_TWISTING, [25, 10, 15, 12, 20, 15], dt=0.01),
    'Adaptive': create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 0.5]),
    'Hybrid': create_smc_for_pso(SMCType.HYBRID, [15, 12, 18, 15], dt=0.01),
}

for name, controller in controllers.items():
    result = runner.run(controller)
    print(f"{name}: ISE={result['metrics']['ise']:.4f}")