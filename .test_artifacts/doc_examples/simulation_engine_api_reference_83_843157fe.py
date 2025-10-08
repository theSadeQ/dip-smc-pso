# Example from: docs\api\simulation_engine_api_reference.md
# Index: 83
# Runnable: False
# Hash: 843157fe

class SequentialOrchestrator(BaseOrchestrator):
    def execute(self, ...):
        self.monitor.start_timing('orchestrator_execute')
        # ... simulation loop ...
        elapsed = self.monitor.end_timing('orchestrator_execute')
        return result