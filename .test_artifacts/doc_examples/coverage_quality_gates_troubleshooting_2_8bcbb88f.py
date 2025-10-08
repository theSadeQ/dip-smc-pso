# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 2
# Runnable: True
# Hash: 8bcbb88f

def test_invalid_gains_exception_handling():
       with pytest.raises(ControllerConfigurationError):
           controller = ClassicalSMC(gains=[-1, 0, 5])  # Invalid gains