# Example from: docs\reference\interfaces\hil_enhanced_hil.md
# Index: 3
# Runnable: True
# Hash: 984b21b9

from src.interfaces.hil.enhanced_hil import MultiFidelitySimulator

# Multi-fidelity simulator
simulator = MultiFidelitySimulator()

# Define fidelity levels
simulator.add_model("low", SimplifiedDynamics())
simulator.add_model("medium", FullDynamics(accuracy="medium"))
simulator.add_model("high", FullDynamics(accuracy="high"))

# Run with adaptive fidelity
result = simulator.run_adaptive(
    initial_fidelity="low",
    accuracy_target=1e-3,
    max_cost=100.0
)

print(f"Final fidelity: {result.final_fidelity}")
print(f"Total cost: {result.total_cost:.1f}")
print(f"Accuracy achieved: {result.accuracy:.6f}")