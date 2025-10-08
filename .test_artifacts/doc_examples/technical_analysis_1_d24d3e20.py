# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 1
# Runnable: True
# Hash: d24d3e20

# Failed assertion details
FAILED tests/test_fault_detection/test_fdi_infrastructure.py::TestThresholdAdaptation::test_fixed_threshold_operation

Expected: "OK"
Actual: "FAULT"
Fault Detection Time: t=0.05s
Residual Norm: 0.1332 (exceeds threshold: 0.1000)