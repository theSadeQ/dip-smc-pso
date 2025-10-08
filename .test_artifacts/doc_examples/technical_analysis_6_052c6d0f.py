# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 6
# Runnable: True
# Hash: 052c6d0f

# 1. Enhanced Controller Cleanup
class MemoryOptimizedController:
    def __init__(self, gains, max_force, dt):
        self.gains = np.asarray(gains)
        self.state_history = deque(maxlen=100)  # Bounded history
        self.control_history = deque(maxlen=100)
        self._temp_arrays = []  # Track temporary allocations

    def __del__(self):
        """Explicit cleanup on destruction."""
        self.state_history.clear()
        self.control_history.clear()
        for arr in self._temp_arrays:
            if hasattr(arr, 'base') and arr.base is not None:
                del arr.base
        self._temp_arrays.clear()

    def compute_control_efficient(self, state, reference):
        """Memory-efficient control computation."""
        # Use pre-allocated workspace arrays
        if not hasattr(self, '_workspace'):
            self._workspace = np.zeros_like(state)

        # In-place operations to avoid copying
        np.subtract(state, reference, out=self._workspace)
        error_norm = np.linalg.norm(self._workspace)

        # Use views instead of copies where possible
        position_error = self._workspace[:4]  # View, not copy
        velocity_error = self._workspace[4:]  # View, not copy

        return self._compute_control_law(position_error, velocity_error)

# 2. Memory Pool Implementation
class ControllerMemoryPool:
    """Custom memory pool for controller operations."""

    def __init__(self, pool_size_mb=100):
        self.pool_size = pool_size_mb * 1024 * 1024  # Convert to bytes
        self.pool = np.empty(self.pool_size // 8, dtype=np.float64)  # 8 bytes per float64
        self.allocations = {}
        self.free_blocks = [{'start': 0, 'size': len(self.pool)}]

    def allocate(self, size, dtype=np.float64):
        """Allocate array from pool."""
        elements_needed = size
        for i, block in enumerate(self.free_blocks):
            if block['size'] >= elements_needed:
                # Allocate from this block
                start_idx = block['start']
                allocated_view = self.pool[start_idx:start_idx + elements_needed].view()
                allocated_view = allocated_view.astype(dtype)

                # Update free blocks
                remaining_size = block['size'] - elements_needed
                if remaining_size > 0:
                    self.free_blocks[i] = {
                        'start': start_idx + elements_needed,
                        'size': remaining_size
                    }
                else:
                    del self.free_blocks[i]

                allocation_id = id(allocated_view)
                self.allocations[allocation_id] = {
                    'start': start_idx,
                    'size': elements_needed
                }

                return allocated_view

        raise MemoryError("Insufficient pool memory")

    def deallocate(self, array):
        """Return array memory to pool."""
        allocation_id = id(array)
        if allocation_id in self.allocations:
            alloc_info = self.allocations[allocation_id]
            # Add back to free blocks (with coalescing logic)
            self._add_free_block(alloc_info['start'], alloc_info['size'])
            del self.allocations[allocation_id]

# 3. Batch Operation Memory Optimization
def run_batch_simulation_memory_optimized(controller_factory, n_trials=1000):
    """Memory-optimized batch simulation."""

    # Pre-allocate result arrays
    results = np.empty((n_trials, 7))  # 7 performance metrics

    # Reuse single controller instance
    controller = controller_factory()

    # Memory monitoring
    memory_monitor = MemoryMonitor()

    for trial in range(n_trials):
        # Monitor memory before trial
        memory_monitor.checkpoint(f"trial_{trial}_start")

        # Run simulation (controller reused, not re-instantiated)
        result = run_single_simulation_efficient(controller, trial)
        results[trial] = result

        # Explicit garbage collection every 100 trials
        if trial % 100 == 0:
            import gc
            gc.collect()

        # Memory monitoring
        memory_monitor.checkpoint(f"trial_{trial}_end")

        # Alert if memory growth detected
        if memory_monitor.growth_rate > 0.5:  # MB per trial
            warnings.warn(f"Memory leak detected at trial {trial}")

    return results