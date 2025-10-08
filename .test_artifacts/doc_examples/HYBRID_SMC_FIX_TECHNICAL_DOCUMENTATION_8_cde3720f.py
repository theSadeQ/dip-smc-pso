# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 8
# Runnable: True
# Hash: cde3720f

# Quick test for return statement issues
controller = create_controller('hybrid_adaptive_sta_smc')
result = controller.compute_control(test_state)
assert result is not None, "Controller returning None - check return statements"
assert hasattr(result, 'control'), "Missing control attribute"