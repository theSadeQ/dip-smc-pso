# Example from: docs\issue_12_pso_optimization_report.md
# Index: 11
# Runnable: True
# Hash: a6bf1b06

# Run comprehensive validation
pytest tests/test_integration/test_numerical_stability/test_numerical_stability_deep.py::TestChatteringReductionEffectiveness -v

# Expected output:
# 1. Chattering Index: X.XX / 2.0 (PASS/FAIL)
# 2. Boundary Layer Effectiveness: X.XX / 0.8 (PASS/FAIL)
# 3. Control Smoothness: X.XX / 0.7 (PASS/FAIL)
# 4. High-Frequency Power Ratio: X.XX / 0.1 (PASS/FAIL)
# 5. Performance Degradation: X.X% / 5% (PASS/FAIL)