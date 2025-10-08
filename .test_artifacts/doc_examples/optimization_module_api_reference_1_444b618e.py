# Example from: docs\api\optimization_module_api_reference.md
# Index: 1
# Runnable: True
# Hash: 444b618e

class PSOTuner:
    """High-throughput, vectorised tuner for sliding-mode controllers.

    The tuner wraps a particle swarm optimisation algorithm around the
    vectorised simulation. It uses local PRNGs to avoid global side effects
    and computes instability penalties based on normalisation constants. Cost
    aggregation between mean and worst-case performance is controlled via
    COMBINE_WEIGHTS.
    """