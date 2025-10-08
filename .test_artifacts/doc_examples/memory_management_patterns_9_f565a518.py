# Example from: docs\memory_management_patterns.md
# Index: 9
# Runnable: True
# Hash: f565a518

import psutil
import os

class ProductionMemoryMonitor:
    """Production-grade memory monitoring for controller deployments."""

    def __init__(self, threshold_mb=500.0):
        self.threshold_mb = threshold_mb
        self.process = psutil.Process(os.getpid())

    def check_memory(self):
        """Check current memory usage against threshold."""
        memory_mb = self.process.memory_info().rss / 1024 / 1024

        if memory_mb > self.threshold_mb:
            return {
                'alert': True,
                'current_mb': memory_mb,
                'threshold_mb': self.threshold_mb,
                'message': f"Memory usage ({memory_mb:.1f}MB) exceeds threshold ({self.threshold_mb}MB)"
            }
        return None

# Usage
monitor = ProductionMemoryMonitor(threshold_mb=500.0)

# Check periodically
if alert := monitor.check_memory():
    logger.warning(f"Memory alert: {alert['message']}")
    controller.reset()  # Clear buffers
    gc.collect()