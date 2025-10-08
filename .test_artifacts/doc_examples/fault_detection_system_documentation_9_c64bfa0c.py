# Example from: docs\fault_detection_system_documentation.md
# Index: 9
# Runnable: False
# Hash: c64bfa0c

class RealTimeFDI:
    def __init__(self, max_execution_time_ms=1.0):
        self.fdi = FDIsystem()
        self.max_execution_time = max_execution_time_ms / 1000.0
        self.execution_times = []

    def check_with_timing(self, *args):
        start_time = time.perf_counter()
        result = self.fdi.check(*args)
        execution_time = time.perf_counter() - start_time

        self.execution_times.append(execution_time)

        if execution_time > self.max_execution_time:
            logging.warning(f"FDI execution time exceeded limit: {execution_time*1000:.2f}ms")

        return result