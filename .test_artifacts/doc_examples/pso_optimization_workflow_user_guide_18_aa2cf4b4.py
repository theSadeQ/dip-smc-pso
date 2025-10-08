# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 18
# Runnable: False
# Hash: aa2cf4b4

# example-metadata:
# runnable: false

optimization_report = {
    'metadata': {
        'date': '2024-01-15',
        'operator': 'user_name',
        'objective': 'Optimize Classical SMC for improved settling time',
        'system_version': 'v2.1.0'
    },
    'configuration': {
        'controller_type': 'classical_smc',
        'pso_parameters': {...},
        'bounds': {...},
        'cost_weights': {...}
    },
    'results': {
        'best_gains': [...],
        'best_cost': 67.34,
        'convergence_iteration': 78,
        'total_iterations': 100
    },
    'validation': {
        'stability_margin': 0.65,
        'settling_time': 2.3,
        'overshoot': 0.05,
        'robustness_score': 0.82
    },
    'recommendations': [
        'Deploy gains for production use',
        'Monitor performance during initial operation',
        'Schedule re-optimization in 6 months'
    ]
}

# Save comprehensive report
with open('optimization_report.json', 'w') as f:
    json.dump(optimization_report, f, indent=2)