# Example from: docs\quality_gate_independence_framework.md
# Index: 7
# Runnable: False
# Hash: fe32c66c

# example-metadata:
# runnable: false

class PartialSuccessReporter:
    """Reports partial validation success with specific gap identification."""

    def generate_partial_success_report(self,
                                      validation_results: IndependentValidationResults) -> PartialSuccessReport:
        """Generate comprehensive partial success report."""

        # Analyze successful validation paths
        successful_paths = self._identify_successful_paths(validation_results)

        # Analyze failed validation paths
        failed_paths = self._identify_failed_paths(validation_results)

        # Analyze partial validation paths
        partial_paths = self._identify_partial_paths(validation_results)

        # Calculate overall system confidence
        system_confidence = self._calculate_system_confidence(
            successful_paths, failed_paths, partial_paths
        )

        # Generate deployment recommendation
        deployment_recommendation = self._generate_deployment_recommendation(
            successful_paths, failed_paths, partial_paths, system_confidence
        )

        return PartialSuccessReport(
            successful_validations={
                'paths': successful_paths,
                'confidence_level': self._calculate_success_confidence(successful_paths),
                'coverage_areas': self._identify_covered_areas(successful_paths)
            },
            failed_validations={
                'paths': failed_paths,
                'failure_modes': self._analyze_failure_modes(failed_paths),
                'impact_assessment': self._assess_failure_impact(failed_paths)
            },
            partial_validations={
                'paths': partial_paths,
                'completion_percentage': self._calculate_completion_percentage(partial_paths),
                'identified_gaps': self._identify_validation_gaps(partial_paths)
            },
            system_confidence=system_confidence,
            deployment_recommendation=deployment_recommendation,
            improvement_priorities=self._prioritize_improvements(
                failed_paths, partial_paths, system_confidence
            )
        )

    def _calculate_system_confidence(self,
                                   successful_paths: List[str],
                                   failed_paths: List[str],
                                   partial_paths: List[str]) -> SystemConfidence:
        """Calculate overall system confidence based on validation results."""

        # Weight validation paths by importance
        path_weights = {
            'coverage_validation': 0.3,        # Important but not critical alone
            'mathematical_validation': 0.4,    # Critical for correctness
            'performance_validation': 0.2,     # Important for deployment
            'compliance_validation': 0.1       # Important for maintainability
        }

        # Calculate weighted success score
        weighted_success = 0.0
        total_weight = 0.0

        for path in successful_paths:
            if path in path_weights:
                weighted_success += path_weights[path] * 1.0
                total_weight += path_weights[path]

        # Add partial success contributions
        for path in partial_paths:
            if path in path_weights:
                partial_completion = self._get_path_completion_percentage(path)
                weighted_success += path_weights[path] * partial_completion
                total_weight += path_weights[path]

        # Calculate confidence score
        confidence_score = weighted_success / sum(path_weights.values()) if total_weight > 0 else 0.0

        # Determine confidence level
        if confidence_score >= 0.9:
            confidence_level = 'high'
        elif confidence_score >= 0.7:
            confidence_level = 'medium'
        elif confidence_score >= 0.5:
            confidence_level = 'low'
        else:
            confidence_level = 'very_low'

        return SystemConfidence(
            score=confidence_score,
            level=confidence_level,
            contributing_factors=self._identify_confidence_factors(
                successful_paths, failed_paths, partial_paths
            ),
            risk_assessment=self._assess_deployment_risk(confidence_score, failed_paths)
        )