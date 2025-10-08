# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 5
# Runnable: False
# Hash: 453c6252

# example-metadata:
# runnable: false

class MemoryAnalysis:
    """Detailed memory usage breakdown."""

    def __init__(self):
        self.baseline_usage = 45.2  # MB
        self.peak_usage = 2100.3    # MB during batch operations
        self.growth_rate = 15.7     # MB per controller instantiation

    def analyze_controller_memory(self):
        """Memory usage by controller type."""
        return {
            'classical_smc': {
                'instantiation': 12.3,  # MB
                'per_step': 0.08,       # MB
                'cleanup_efficiency': 0.73  # 73% properly deallocated
            },
            'adaptive_smc': {
                'instantiation': 15.7,  # MB (higher due to adaptation arrays)
                'per_step': 0.12,       # MB
                'cleanup_efficiency': 0.68  # Lower cleanup efficiency
            },
            'sta_smc': {
                'instantiation': 14.1,  # MB
                'per_step': 0.10,       # MB
                'cleanup_efficiency': 0.71
            },
            'hybrid_smc': {
                'instantiation': 18.9,  # MB (highest due to dual controllers)
                'per_step': 0.15,       # MB
                'cleanup_efficiency': 0.65  # Lowest cleanup efficiency
            }
        }

    def numpy_memory_patterns(self):
        """NumPy array allocation patterns."""
        return {
            'state_arrays': {
                'allocation_count': 1247,
                'avg_size': 0.15,  # MB
                'copy_operations': 423,  # Unnecessary copies
                'view_efficiency': 0.34  # Only 34% use views vs copies
            },
            'control_arrays': {
                'allocation_count': 890,
                'avg_size': 0.08,  # MB
                'copy_operations': 312,
                'view_efficiency': 0.42
            }
        }