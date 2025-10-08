# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 21
# Runnable: True
# Hash: 85262617

def custom_cost_function(self, trajectory_data):
    """Custom cost function implementation."""
    t, x, u, sigma = trajectory_data

    # Custom performance metrics
    custom_metric = compute_custom_performance(x, u)

    # Combine with standard metrics
    standard_cost = self._compute_cost_from_traj(t, x, u, sigma)

    return standard_cost + 0.1 * custom_metric