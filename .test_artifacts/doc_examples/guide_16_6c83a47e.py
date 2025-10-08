# Example from: docs\optimization_simulation\guide.md
# Index: 16
# Runnable: True
# Hash: 6c83a47e

from src.simulation.core.simulation_context import SimulationContext

# Initialize context with configuration
context = SimulationContext("config.yaml")

# Access dynamics model
dynamics = context.get_dynamics_model()

# Create controller
controller = context.create_controller(name="classical_smc")

# Create simulation engine
engine = context.create_simulation_engine(engine_type="sequential")

# Register custom components
from src.utils.monitoring import PerformanceMonitor
monitor = PerformanceMonitor()
context.register_component("performance_monitor", monitor)

# Retrieve registered component
monitor = context.get_component("performance_monitor")