# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 14
# Runnable: False
# Hash: a436c43a

# example-metadata:
# runnable: false

class MathematicalValidationReporter:
    """Automated reporting for mathematical validation results."""

    def __init__(self):
        self.violations = []
        self.warnings = []
        self.performance_metrics = {}

    def report_stability_violation(self, test_name, gains, eigenvalues):
        """Report stability requirement violations."""
        self.violations.append({
            'type': 'stability',
            'test': test_name,
            'gains': gains,
            'eigenvalues': eigenvalues,
            'severity': 'critical'
        })

    def report_numerical_instability(self, test_name, input_values, output_values):
        """Report numerical computation issues."""
        self.violations.append({
            'type': 'numerical',
            'test': test_name,
            'inputs': input_values,
            'outputs': output_values,
            'severity': 'high'
        })

    def generate_report(self):
        """Generate comprehensive validation report."""
        report = {
            'summary': {
                'total_violations': len(self.violations),
                'critical_issues': len([v for v in self.violations if v['severity'] == 'critical']),
                'warnings': len(self.warnings)
            },
            'violations': self.violations,
            'warnings': self.warnings,
            'performance': self.performance_metrics
        }
        return report