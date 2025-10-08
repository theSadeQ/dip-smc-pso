# Example from: docs\pso_factory_integration_patterns.md
# Index: 16
# Runnable: False
# Hash: 659b88c3

# example-metadata:
# runnable: false

# ✅ Good: Monitor PSO progress and performance
class PSO_Monitor:
    def __init__(self):
        self.iteration_times = []
        self.fitness_history = []
        self.evaluation_count = 0

    def log_iteration(self, iteration, best_fitness, elapsed_time):
        self.fitness_history.append(best_fitness)
        self.iteration_times.append(elapsed_time)

        if iteration % 10 == 0:
            avg_time = np.mean(self.iteration_times[-10:])
            logger.info(f"Iteration {iteration}: fitness={best_fitness:.6f}, "
                       f"avg_time={avg_time:.3f}s")

    def log_evaluation(self):
        self.evaluation_count += 1

        if self.evaluation_count % 100 == 0:
            logger.info(f"Completed {self.evaluation_count} evaluations")

monitor = PSO_Monitor()

def monitored_fitness_function(gains):
    monitor.log_evaluation()
    # ... fitness computation
    return fitness_value