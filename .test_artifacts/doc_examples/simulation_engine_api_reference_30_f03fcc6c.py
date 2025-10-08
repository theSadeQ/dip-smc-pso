# Example from: docs\api\simulation_engine_api_reference.md
# Index: 30
# Runnable: False
# Hash: f03fcc6c

# Create successful result
result = DynamicsResult.success_result(
    state_derivative=dx_dt,
    time=t,
    energy=total_energy
)

# Create failure result
result = DynamicsResult.failure_result(
    reason="Singular matrix detected",
    condition_number=1e15
)