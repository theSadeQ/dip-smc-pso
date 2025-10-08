# Example from: docs\GitHub_Issue_4_PSO_Integration_Resolution_Report.md
# Index: 5
# Runnable: False
# Hash: 4a5c9fff

# example-metadata:
# runnable: false

class PSO_ConfigurationValidator:
    """Comprehensive PSO configuration validation."""

    def validate_complete_config(self, config: dict) -> ValidationReport:
        """Multi-level validation with mathematical rigor."""
        report = ValidationReport()

        # Level 1: Syntax and structure validation
        syntax_result = self._validate_syntax(config)
        report.add_level_result('syntax', syntax_result)

        # Level 2: Mathematical consistency
        math_result = self._validate_mathematical_consistency(config)
        report.add_level_result('mathematical', math_result)

        # Level 3: Controller-specific constraints
        controller_result = self._validate_controller_constraints(config)
        report.add_level_result('controller', controller_result)

        # Level 4: Performance optimization
        performance_result = self._validate_performance_config(config)
        report.add_level_result('performance', performance_result)

        return report

    def _validate_mathematical_consistency(self, config: dict) -> ValidationResult:
        """Validate PSO mathematical properties."""
        errors = []

        if 'algorithm_params' in config.get('pso', {}):
            params = config['pso']['algorithm_params']

            # PSO convergence condition: φ = c₁ + c₂ > 4
            if 'c1' in params and 'c2' in params:
                phi = params['c1'] + params['c2']
                if phi <= 4.0:
                    errors.append(f"PSO convergence risk: φ = {phi:.3f} ≤ 4.0")

            # Coefficient balance: |c₁ - c₂| ≤ 0.5
            if 'c1' in params and 'c2' in params:
                diff = abs(params['c1'] - params['c2'])
                if diff > 0.5:
                    errors.append(f"Unbalanced coefficients: |c₁ - c₂| = {diff:.3f}")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)