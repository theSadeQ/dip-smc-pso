# Example from: docs\benchmarks_methodology.md
# Index: 5
# Runnable: True
# Hash: 7f5a4ff1

# Test with physics uncertainty and sensor noise
metrics_robust, ci_robust = run_trials(
    controller_factory=factory,
    cfg=config,
    n_trials=50,              # More trials for robustness testing
    randomise_physics=True,   # Enable parameter variations
    noise_std=0.001          # Add sensor noise
)