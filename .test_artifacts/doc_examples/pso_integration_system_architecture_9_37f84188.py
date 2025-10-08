# Example from: docs\pso_integration_system_architecture.md
# Index: 9
# Runnable: True
# Hash: 37f84188

# Penalty application hierarchy:
1. Invalid gains → validate_gains() pre-filtering
2. Simulation failure → instability_penalty
3. NaN cost computation → instability_penalty
4. Convergence failure → return best available solution