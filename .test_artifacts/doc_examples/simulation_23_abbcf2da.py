# Example from: docs\guides\api\simulation.md
# Index: 23
# Runnable: True
# Hash: abbcf2da

# Compare multiple controllers
controllers = {
    'Classical': create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5]),
    'STA': create_smc_for_pso(SMCType.SUPER_TWISTING, [25, 10, 15, 12, 20, 15], dt=0.01),
    'Adaptive': create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 0.5]),
}

results = {}
for name, ctrl in controllers.items():
    results[name] = runner.run(ctrl)
    print(f"{name}: ISE={results[name]['metrics']['ise']:.4f}")

# Statistical comparison
from src.utils.analysis import compare_controllers
comparison = compare_controllers(results)
print(comparison.summary())