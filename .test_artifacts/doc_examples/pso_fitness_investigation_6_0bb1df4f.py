# Example from: docs\testing\reports\2025-09-30\pso_fitness_investigation.md
# Index: 6
# Runnable: False
# Hash: 0bb1df4f

def validate_cost_function_config(cost_cfg):
    """Validate cost function configuration"""
    # Check weight balance
    if cost_cfg.weights.state_error > 10.0:
        warnings.warn(f"state_error weight ({cost_cfg.weights.state_error}) is very high")

    # Check baseline gains
    if hasattr(cost_cfg, 'baseline') and cost_cfg.baseline.gains:
        warnings.warn("Baseline normalization enabled - may cause cost=0 issues")

    # Check explicit norms
    if not hasattr(cost_cfg, 'norms'):
        warnings.warn("No explicit normalization constants - using baseline or defaults")