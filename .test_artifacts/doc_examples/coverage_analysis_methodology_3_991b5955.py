# Example from: docs\coverage_analysis_methodology.md
# Index: 3
# Runnable: False
# Hash: 991b5955

# example-metadata:
# runnable: false

def selective_coverage_collection(test_suite: TestSuite) -> AggregatedCoverage:
    """
    Collect coverage from passing tests while isolating failures.

    Mathematical Model:
    Total_Coverage = Σ(C_i × S_i) / Σ(S_i)
    Where C_i = coverage of test i, S_i = success indicator
    """
    passing_coverage = []
    failed_tests = []

    for test in test_suite:
        try:
            coverage = execute_test_with_coverage(test)
            passing_coverage.append(coverage)
        except TestFailure as e:
            failed_tests.append((test, e))
            # Continue with other tests - no cascade failure

    return AggregatedCoverage(
        total_coverage=aggregate_passing_coverage(passing_coverage),
        passing_tests=len(passing_coverage),
        failed_tests=failed_tests,
        coverage_confidence=calculate_confidence(passing_coverage, failed_tests)
    )