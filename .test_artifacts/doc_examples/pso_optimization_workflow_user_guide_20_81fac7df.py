# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 20
# Runnable: False
# Hash: 81fac7df

# example-metadata:
# runnable: false

controller_configs = {
    'classical_smc': {'bounds': [...], 'weights': {...}},
    'sta_smc': {'bounds': [...], 'weights': {...}},
    # ... etc
}

for ctrl_type, config in controller_configs.items():
    optimize_with_config(ctrl_type, config)