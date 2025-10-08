# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 13
# Runnable: False
# Hash: 37735cba

# example-metadata:
# runnable: false

# Calculate realistic thresholds based on component complexity
def calculate_optimal_thresholds(codebase_analysis):
    """
    Calculate component-specific coverage thresholds based on:
    - Cyclomatic complexity
    - Code churn rate
    - Critical path analysis
    - Historical coverage trends
    """

    thresholds = {}

    for component, metrics in codebase_analysis.items():
        # Base threshold
        base_threshold = 85.0

        # Adjustments
        if metrics['safety_critical']:
            thresholds[component] = 100.0
        elif metrics['cyclomatic_complexity'] > 10:
            thresholds[component] = min(95.0, base_threshold + 10)
        elif metrics['code_churn'] > 0.3:  # High change frequency
            thresholds[component] = base_threshold + 5
        else:
            thresholds[component] = base_threshold

    return thresholds