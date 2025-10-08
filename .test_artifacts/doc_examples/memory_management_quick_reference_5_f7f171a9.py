# Example from: docs\memory_management_quick_reference.md
# Index: 5
# Runnable: False
# Hash: f7f171a9

# example-metadata:
# runnable: false

class MemoryMonitor:
    def __init__(self, threshold_mb=500):
        self.threshold_mb = threshold_mb
        self.process = psutil.Process(os.getpid())

    def check(self):
        memory_mb = self.process.memory_info().rss / 1024 / 1024
        if memory_mb > self.threshold_mb:
            return f"Memory alert: {memory_mb:.1f}MB > {self.threshold_mb}MB"
        return None

monitor = MemoryMonitor(threshold_mb=500)
if alert := monitor.check():
    logger.warning(alert)
    # Take action: clear history, reset controller, etc.