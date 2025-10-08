# Example from: docs\technical\pso_integration_workflows.md
# Index: 27
# Runnable: False
# Hash: 020acc5c

def comprehensive_validation_workflow(optimization_result: Dict[str, Any]) -> Dict[str, Any]:
    """Comprehensive validation workflow for optimized controllers."""

    if not optimization_result['success']:
        return {'validation_status': 'FAILED', 'reason': 'Optimization failed'}

    validation_report = {
        'validation_status': 'PENDING',
        'checks_performed': [],
        'issues_found': [],
        'recommendations': []
    }

    # 1. Basic validation checks
    validation_report['checks_performed'].append('basic_validation')
    basic_validation = optimization_result['validation_results']

    if not basic_validation['gains_valid']:
        validation_report['issues_found'].append('Invalid gains detected')

    if not basic_validation['controller_stable']:
        validation_report['issues_found'].append('Controller stability issues')

    if not basic_validation['performance_acceptable']:
        validation_report['issues_found'].append('Performance below acceptable threshold')

    # 2. Convergence analysis
    validation_report['checks_performed'].append('convergence_analysis')
    performance = optimization_result['performance_analysis']

    if not performance['converged']:
        validation_report['issues_found'].append('PSO did not converge')
        validation_report['recommendations'].append('Increase max_iterations or relax convergence_threshold')

    if performance['improvement_ratio'] < 0.1:
        validation_report['issues_found'].append('Low improvement ratio')
        validation_report['recommendations'].append('Review optimization bounds or increase population size')

    # 3. Gain analysis
    validation_report['checks_performed'].append('gain_analysis')
    gains = optimization_result['best_gains']

    # Check for extreme values
    if any(g > 100.0 for g in gains):
        validation_report['issues_found'].append('Extremely high gains detected')
        validation_report['recommendations'].append('Review optimization bounds')

    if any(g < 0.1 for g in gains):
        validation_report['issues_found'].append('Very low gains detected')
        validation_report['recommendations'].append('Check minimum bounds')

    # 4. Cost analysis
    validation_report['checks_performed'].append('cost_analysis')
    best_cost = optimization_result['best_cost']

    if best_cost > 100.0:
        validation_report['issues_found'].append('High optimization cost')
        validation_report['recommendations'].append('Review controller performance or optimization scenarios')

    # 5. Determine overall status
    if len(validation_report['issues_found']) == 0:
        validation_report['validation_status'] = 'PASSED'
    elif len(validation_report['issues_found']) <= 2:
        validation_report['validation_status'] = 'WARNING'
    else:
        validation_report['validation_status'] = 'FAILED'

    # 6. Generate summary
    validation_report['summary'] = {
        'total_checks': len(validation_report['checks_performed']),
        'issues_count': len(validation_report['issues_found']),
        'recommendations_count': len(validation_report['recommendations']),
        'overall_status': validation_report['validation_status']
    }

    return validation_report

# Usage example
pso_config = PSOFactoryConfig(controller_type=ControllerType.CLASSICAL_SMC)
pso_factory = EnhancedPSOFactory(pso_config)
result = pso_factory.optimize_controller()

validation_report = comprehensive_validation_workflow(result)
print(f"Validation status: {validation_report['validation_status']}")
print(f"Issues found: {len(validation_report['issues_found'])}")
for issue in validation_report['issues_found']:
    print(f"  - {issue}")