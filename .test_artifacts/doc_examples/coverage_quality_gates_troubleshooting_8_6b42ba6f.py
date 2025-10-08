# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 8
# Runnable: True
# Hash: 6b42ba6f

def test_factory_invalid_controller_type():
       with pytest.raises(ValueError, match="Unknown controller"):
           create_controller("invalid_controller_type")