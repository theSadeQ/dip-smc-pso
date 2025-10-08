# Example from: docs\technical\pso_integration_workflows.md
# Index: 22
# Runnable: False
# Hash: 9da6e150

def real_time_optimization_integration():
    """Demonstrate real-time optimization with live feedback."""

    import time
    import threading
    from queue import Queue

    class OptimizationMonitor:
        """Real-time optimization monitoring."""

        def __init__(self):
            self.progress_queue = Queue()
            self.current_iteration = 0
            self.current_best_cost = float('inf')
            self.is_running = False

        def update_progress(self, iteration, best_cost):
            """Update optimization progress."""
            self.current_iteration = iteration
            self.current_best_cost = best_cost
            self.progress_queue.put((iteration, best_cost))

        def start_monitoring(self):
            """Start monitoring thread."""
            self.is_running = True
            monitor_thread = threading.Thread(target=self._monitor_loop)
            monitor_thread.daemon = True
            monitor_thread.start()

        def stop_monitoring(self):
            """Stop monitoring."""
            self.is_running = False

        def _monitor_loop(self):
            """Monitoring loop."""
            while self.is_running:
                try:
                    if not self.progress_queue.empty():
                        iteration, cost = self.progress_queue.get(timeout=0.1)
                        print(f"\rIteration {iteration}: Best cost = {cost:.6f}", end='', flush=True)
                    time.sleep(0.1)
                except:
                    continue

    # Create monitor
    monitor = OptimizationMonitor()

    # Configure PSO with monitoring integration
    pso_config = PSOFactoryConfig(
        controller_type=ControllerType.CLASSICAL_SMC,
        population_size=20,
        max_iterations=50,
        use_robust_evaluation=True
    )

    print("Starting real-time PSO optimization...")

    # Start monitoring
    monitor.start_monitoring()

    try:
        # Create factory and optimize
        pso_factory = EnhancedPSOFactory(pso_config)

        # Note: In a real implementation, you would integrate the monitor
        # with the PSO algorithm's iteration callback

        result = pso_factory.optimize_controller()

        print("\n")  # New line after progress updates

        if result['success']:
            print(f"Optimization completed successfully!")
            print(f"Final cost: {result['best_cost']:.6f}")
            print(f"Optimized gains: {result['best_gains']}")

            # Real-time validation
            optimized_controller = result['controller']

            print("\nPerforming real-time validation...")
            test_states = [
                [0.0, 0.1, 0.05, 0.0, 0.0, 0.0],
                [0.0, 0.2, 0.1, 0.0, 0.0, 0.0],
                [0.0, 0.3, 0.15, 0.0, 0.0, 0.0]
            ]

            for i, state in enumerate(test_states):
                control_output = optimized_controller.compute_control(state)
                if hasattr(control_output, 'u'):
                    u = control_output.u
                else:
                    u = control_output
                print(f"  Test {i+1}: state={state[:3]}, control={u:.3f}")

            print("Real-time validation completed")

        else:
            print(f"Optimization failed: {result.get('error', 'Unknown')}")

    finally:
        monitor.stop_monitoring()

    return result

# Run real-time optimization
real_time_result = real_time_optimization_integration()