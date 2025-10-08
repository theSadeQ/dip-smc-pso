# Example from: docs\api\simulation_engine_api_reference.md
# Index: 49
# Runnable: True
# Hash: 6d4d878e

from src.simulation.orchestrators import RealTimeOrchestrator
from src.interfaces.hil import PlantServer

# Create real-time orchestrator
orchestrator = RealTimeOrchestrator(
    dynamics=hardware_interface,
    integrator=integrator,
    real_time_factor=1.0,  # Real-time (use 0.5 for slow-motion, 2.0 for fast)
    deadline_tolerance=0.001  # 1ms tolerance
)

# Execute HIL simulation
result = orchestrator.execute(
    initial_state=x0,
    control_inputs=None,  # Generated dynamically
    dt=0.01,
    horizon=1000,
    controller=controller
)

# Check timing statistics
stats = orchestrator.get_timing_stats()
print(f"Deadline misses: {stats['deadline_misses']}")
print(f"Average execution time: {stats['mean_exec_time']:.3f}ms")