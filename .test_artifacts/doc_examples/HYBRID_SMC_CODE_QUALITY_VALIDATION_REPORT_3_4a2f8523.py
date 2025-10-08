# Example from: docs\reports\HYBRID_SMC_CODE_QUALITY_VALIDATION_REPORT.md
# Index: 3
# Runnable: True
# Hash: 4a2f8523

# Dual interface support for compatibility
if dt is not None or (state_vars is None and history is None):
    # Test interface: return numpy array
    return np.array([u_saturated, 0.0, 0.0])
else:
    # Standard interface: return dictionary
    return control_result