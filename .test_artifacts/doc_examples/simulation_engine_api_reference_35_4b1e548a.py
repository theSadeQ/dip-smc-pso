# Example from: docs\api\simulation_engine_api_reference.md
# Index: 35
# Runnable: False
# Hash: 4b1e548a

# example-metadata:
# runnable: false

def reset_monitoring(self) -> None:
    """Reset monitoring statistics."""
    if hasattr(self, '_stability_monitor'):
        self._stability_monitor.reset_statistics()

def get_monitoring_stats(self) -> Dict[str, Any]:
    """Get monitoring statistics."""
    stats = {}
    if hasattr(self, '_stability_monitor'):
        stats['numerical_stability'] = self._stability_monitor.get_statistics()
    return stats