# Example from: docs\api\simulation_engine_api_reference.md
# Index: 83
# Runnable: False
# Hash: 78bd0cf4

# example-metadata:
# runnable: false

class SequentialOrchestrator(BaseOrchestrator):
    def execute(self, ...):
        self.monitor.start_timing('orchestrator_execute')
        # ... simulation loop ...
        elapsed = self.monitor.end_timing('orchestrator_execute')
        return result