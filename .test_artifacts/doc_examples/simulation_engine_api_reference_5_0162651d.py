# Example from: docs\api\simulation_engine_api_reference.md
# Index: 5
# Runnable: True
# Hash: 0162651d

from src.simulation import SequentialOrchestrator, IntegratorFactory

# Modern interface
orchestrator = SequentialOrchestrator(dynamics, integrator)
result = orchestrator.execute(initial_state, controls, dt, horizon)