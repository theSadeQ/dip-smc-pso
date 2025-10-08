# Example from: docs\coverage_analysis_methodology.md
# Index: 4
# Runnable: False
# Hash: 7376231a

# example-metadata:
# runnable: false

class ValidationGapMatrix:
    """
    Systematic gap identification across validation dimensions.

    Provides actionable improvement paths when quality gates fail.
    """

    def identify_gaps(self, validation_results: ValidationResults) -> GapMatrix:
        gaps = {
            'theoretical': self.analyze_theoretical_gaps(validation_results.theory),
            'performance': self.analyze_performance_gaps(validation_results.performance),
            'coverage': self.analyze_coverage_gaps(validation_results.coverage),
            'integration': self.analyze_integration_gaps(validation_results.integration)
        }

        return GapMatrix(
            gaps=gaps,
            priority_actions=self.prioritize_improvements(gaps),
            estimated_effort=self.estimate_improvement_effort(gaps)
        )