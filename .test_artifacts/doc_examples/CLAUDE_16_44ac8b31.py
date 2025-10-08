# Example from: docs\CLAUDE.md
# Index: 16
# Runnable: True
# Hash: 44ac8b31

import psutil
import os

class MemoryMonitor:
    def __init__(self, threshold_mb=500):
        self.threshold_mb = threshold_mb
        self.process = psutil.Process(os.getpid())

    def check(self):
        memory_mb = self.process.memory_info().rss / 1024 / 1024
        if memory_mb > self.threshold_mb:
            return f"Alert: {memory_mb:.1f}MB > {self.threshold_mb}MB"
        return None

monitor = MemoryMonitor(threshold_mb=500)
if alert := monitor.check():
    history = controller.initialize_history()  # Clear buffers