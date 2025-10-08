# Example from: docs\mathematical_validation_procedures.md
# Index: 11
# Runnable: False
# Hash: 50971ea5

class ComprehensiveMathematicalValidator:
    """Comprehensive mathematical validation for control systems."""

    def __init__(self):
        self.validators = {
            'stability': LyapunovStabilityValidator(),
            'reachability': SlidingSurfaceReachabilityValidator(),
            'convergence': PSOConvergenceValidator(),
            'numerical': NumericalStabilityValidator(),
            'real_time': RealTimeConstraintValidator()
        }

    def validate_all_mathematical_properties(self,
                                           control_system: ControlSystem) -> ComprehensiveMathematicalValidationResult:
        """Execute complete mathematical validation suite."""

        validation_results = {}

        for validator_name, validator in self.validators.items():
            try:
                validation_results[validator_name] = validator.validate(control_system)
            except Exception as e:
                validation_results[validator_name] = ValidationResult(
                    status='error',
                    error=str(e),
                    mathematical_interpretation=f"Failed to validate {validator_name}"
                )

        # Calculate overall mathematical rigor score
        rigor_score = self._calculate_mathematical_rigor_score(validation_results)

        # Generate mathematical soundness assessment
        soundness_assessment = self._assess_mathematical_soundness(validation_results)

        return ComprehensiveMathematicalValidationResult(
            validation_results=validation_results,
            mathematical_rigor_score=rigor_score,
            mathematical_soundness=soundness_assessment,
            theoretical_properties_verified=self._count_verified_properties(validation_results),
            deployment_mathematical_approval=rigor_score >= MATHEMATICAL_DEPLOYMENT_THRESHOLD
        )

    def _calculate_mathematical_rigor_score(self,
                                          validation_results: Dict[str, ValidationResult]) -> float:
        """Calculate overall mathematical rigor score."""

        # Weight different validation aspects
        weights = {
            'stability': 0.3,        # Critical for safety
            'reachability': 0.25,    # Critical for performance
            'convergence': 0.2,      # Important for optimization
            'numerical': 0.15,       # Important for accuracy
            'real_time': 0.1         # Important for implementation
        }

        weighted_score = 0.0
        total_weight = 0.0

        for validator_name, result in validation_results.items():
            if validator_name in weights and result.status != 'error':
                # Extract numerical score from validation result
                if hasattr(result, 'score'):
                    score = result.score
                elif result.status == 'passed':
                    score = 1.0
                elif result.status == 'partial':
                    score = 0.7
                else:
                    score = 0.0

                weighted_score += weights[validator_name] * score
                total_weight += weights[validator_name]

        return weighted_score / total_weight if total_weight > 0 else 0.0