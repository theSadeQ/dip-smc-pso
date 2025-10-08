# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 1
# Runnable: False
# Hash: f1f1d325

# example-metadata:
# runnable: false

class ConfigurationLoader:
    """
    Robust configuration loading with comprehensive validation.
    """

    def __init__(self):
        self.validation_chain = [
            self._validate_syntax,
            self._validate_structure,
            self._validate_types,
            self._validate_bounds,
            self._validate_mathematical_consistency,
            self._validate_controller_compatibility
        ]

    def load_and_validate_config(self, config_path: str,
                                controller_type: str = None) -> ConfigLoadResult:
        """
        Load configuration with full validation chain.

        Workflow Steps:
        1. YAML syntax validation
        2. Schema structure verification
        3. Data type consistency checking
        4. Parameter bounds validation
        5. Mathematical constraint verification
        6. Controller-specific compatibility

        Returns:
        ConfigLoadResult with validation status and error details
        """
        result = ConfigLoadResult()

        try:
            # Load raw configuration
            with open(config_path, 'r') as f:
                raw_config = yaml.safe_load(f)

            result.raw_config = raw_config

            # Apply validation chain
            for validator in self.validation_chain:
                validation_result = validator(raw_config, controller_type)
                result.add_validation_result(validator.__name__, validation_result)

                if validation_result.severity == 'CRITICAL':
                    result.status = 'FAILED'
                    return result

            # Configuration migration if needed
            if self._needs_migration(raw_config):
                migrated_config, warnings = self._migrate_configuration(raw_config)
                result.config = migrated_config
                result.migration_warnings = warnings
            else:
                result.config = raw_config

            result.status = 'SUCCESS'

        except Exception as e:
            result.status = 'ERROR'
            result.error_message = str(e)

        return result

    def _validate_mathematical_consistency(self, config: dict,
                                         controller_type: str) -> ValidationResult:
        """
        Validate mathematical consistency of PSO parameters.
        """
        errors = []

        pso_config = config.get('pso', {})
        algorithm_params = pso_config.get('algorithm_params', {})

        # PSO Convergence Condition: φ = c₁ + c₂ > 4
        c1 = algorithm_params.get('c1', 2.0)
        c2 = algorithm_params.get('c2', 2.0)
        phi = c1 + c2

        if phi <= 4.0:
            errors.append({
                'code': 'PSO_CONVERGENCE_RISK',
                'message': f'PSO convergence risk: φ = {phi:.3f} ≤ 4.0',
                'severity': 'HIGH',
                'fix_suggestion': 'Increase c1 or c2 to ensure φ > 4.0'
            })

        # Coefficient Balance: |c₁ - c₂| ≤ 0.5
        coeff_diff = abs(c1 - c2)
        if coeff_diff > 0.5:
            errors.append({
                'code': 'UNBALANCED_COEFFICIENTS',
                'message': f'Unbalanced PSO coefficients: |c₁ - c₂| = {coeff_diff:.3f}',
                'severity': 'MEDIUM',
                'fix_suggestion': 'Balance c1 and c2 for optimal exploration/exploitation'
            })

        # Controller-specific mathematical validation
        if controller_type == 'sta_smc':
            bounds = pso_config.get('bounds', {}).get('sta_smc', {})
            if 'max' in bounds and len(bounds['max']) >= 6:
                lambda1_max, lambda2_max = bounds['max'][4], bounds['max'][5]
                if lambda1_max > 10.0 or lambda2_max > 10.0:
                    errors.append({
                        'code': 'ISSUE2_REGRESSION_RISK',
                        'message': f'STA-SMC lambda bounds may cause overshoot: λ₁_max={lambda1_max}, λ₂_max={lambda2_max}',
                        'severity': 'HIGH',
                        'fix_suggestion': 'Apply Issue #2 bounds: λ₁, λ₂ ≤ 10.0'
                    })

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            severity='CRITICAL' if any(e['severity'] == 'HIGH' for e in errors) else 'MINOR'
        )