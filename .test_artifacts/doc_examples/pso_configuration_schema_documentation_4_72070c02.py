# Example from: docs\pso_configuration_schema_documentation.md
# Index: 4
# Runnable: False
# Hash: 72070c02

class PSO_ConfigurationValidator:
    """
    Comprehensive PSO configuration validation with mathematical rigor.
    """

    def __init__(self):
        self.validation_levels = [
            'syntax_validation',      # YAML structure and types
            'range_validation',       # Parameter bounds checking
            'mathematical_validation', # Stability and convergence
            'controller_validation',   # Controller-specific constraints
            'performance_validation',  # Expected performance bounds
            'safety_validation'       # Hardware and operational safety
        ]

    def validate_complete_config(self, config: dict) -> ValidationReport:
        """
        Perform complete multi-level validation of PSO configuration.
        """
        report = ValidationReport()

        for level in self.validation_levels:
            validator_method = getattr(self, level)
            level_result = validator_method(config)
            report.add_level_result(level, level_result)

            # Stop on critical failures
            if level_result.severity == 'CRITICAL':
                break

        return report

    def syntax_validation(self, config: dict) -> ValidationResult:
        """
        Level 1: Validate YAML structure and data types.
        """
        errors = []

        # Required sections
        required_sections = ['algorithm_params', 'bounds', 'execution']
        for section in required_sections:
            if section not in config:
                errors.append(f"Missing required section: {section}")

        # Type checking
        if 'algorithm_params' in config:
            params = config['algorithm_params']
            type_checks = [
                ('n_particles', int), ('iters', int),
                ('w', (float, int)), ('c1', (float, int)), ('c2', (float, int))
            ]
            for param_name, expected_type in type_checks:
                if param_name in params:
                    if not isinstance(params[param_name], expected_type):
                        errors.append(f"Type error: {param_name} must be {expected_type}")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def mathematical_validation(self, config: dict) -> ValidationResult:
        """
        Level 3: Validate mathematical consistency and stability.
        """
        errors = []

        if 'algorithm_params' in config:
            params = config['algorithm_params']

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

            # Inertia weight bounds: w ∈ [0.4, 0.9]
            if 'w' in params:
                w = params['w']
                if not (0.4 <= w <= 0.9):
                    errors.append(f"Inertia weight w = {w:.3f} outside optimal range")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def controller_validation(self, config: dict) -> ValidationResult:
        """
        Level 4: Validate controller-specific constraints.
        """
        errors = []

        if 'bounds' not in config:
            return ValidationResult(is_valid=False, errors=["Missing bounds configuration"])

        bounds_config = config['bounds']

        # Validate each controller type
        for controller_type in ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']:
            if controller_type in bounds_config:
                controller_errors = self._validate_controller_bounds(
                    controller_type, bounds_config[controller_type]
                )
                errors.extend(controller_errors)

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def _validate_controller_bounds(self, controller_type: str, bounds: dict) -> list:
        """
        Validate bounds for specific controller type.
        """
        errors = []

        if 'min' not in bounds or 'max' not in bounds:
            return [f"{controller_type}: Missing min/max bounds"]

        min_bounds, max_bounds = bounds['min'], bounds['max']

        # Check bounds consistency
        if len(min_bounds) != len(max_bounds):
            errors.append(f"{controller_type}: min/max bounds length mismatch")
            return errors

        # Check min < max for all parameters
        for i, (min_val, max_val) in enumerate(zip(min_bounds, max_bounds)):
            if min_val >= max_val:
                errors.append(f"{controller_type}: Parameter {i}: min {min_val} >= max {max_val}")

        # Controller-specific validation
        if controller_type == 'sta_smc':
            # Issue #2 specific validation
            if len(min_bounds) >= 6:  # lambda1, lambda2 are indices 4, 5
                lambda1_max, lambda2_max = max_bounds[4], max_bounds[5]
                if lambda1_max > 10.0 or lambda2_max > 10.0:
                    errors.append(f"STA-SMC Issue #2: Lambda bounds too large (max: {lambda1_max}, {lambda2_max})")

        elif controller_type == 'adaptive_smc':
            # Check adaptation rate bounds
            if len(min_bounds) >= 5:  # gamma is index 4
                gamma_min, gamma_max = min_bounds[4], max_bounds[4]
                if gamma_min <= 0:
                    errors.append(f"Adaptive SMC: Adaptation rate must be positive")
                if gamma_max > 10.0:
                    errors.append(f"Adaptive SMC: Adaptation rate too large: {gamma_max}")

        return errors