# Example from: docs\guides\api\simulation.md
# Index: 2
# Runnable: True
# Hash: 421bb8ed

from src.controllers import create_smc_for_pso, SMCType

# Create controller
controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)

# Run simulation
result = runner.run(controller)

# Access results
print(f"ISE: {result['metrics']['ise']:.4f}")
print(f"Final state: {result['state'][-1]}")