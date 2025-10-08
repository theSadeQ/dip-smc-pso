# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 14
# Runnable: False
# Hash: 8e9deade

# example-metadata:
# runnable: false

def calculate_coverage_production_score(gate_results):
    """
    Calculate coverage contribution to overall production readiness score.

    Current Production Readiness: 6.1/10
    Target Production Readiness: 8.5/10
    Coverage Weight: 25% of total score
    """

    weights = {
        'infrastructure_health': 0.15,
        'safety_critical_coverage': 0.40,  # Highest weight
        'critical_components_coverage': 0.25,
        'overall_coverage': 0.20
    }

    coverage_score = 0.0

    for gate_id, weight in weights.items():
        if gate_results.get(gate_id, {}).get('status') == 'passed':
            coverage_score += weight

    # Scale to 0-10
    production_contribution = coverage_score * 10

    return {
        'coverage_production_score': production_contribution,
        'production_ready': production_contribution >= 8.0,
        'improvement_needed': max(0, 8.0 - production_contribution)
    }