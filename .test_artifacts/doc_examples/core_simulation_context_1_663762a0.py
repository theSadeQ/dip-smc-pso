# Example from: docs\reference\simulation\core_simulation_context.md
# Index: 1
# Runnable: True
# Hash: 663762a0

class SimulationContext:
    def __enter__(self):
        # Thread-local context initialization
        return isolated_context

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup and resource release
        pass