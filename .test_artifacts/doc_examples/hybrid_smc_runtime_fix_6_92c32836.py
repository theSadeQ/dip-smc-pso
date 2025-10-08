# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 6
# Runnable: True
# Hash: 92c32836

# Error handling in controller factory (hypothetical)
try:
    result = controller.compute_control(state, state_vars, history)
    # result is None instead of HybridSTAOutput

    # Simulation engine expects HybridSTAOutput
    control_value = result.control  # AttributeError: NoneType has no attribute 'control'

except Exception as e:
    # Factory catches exception and returns error message
    return f"Hybrid control computation failed: {str(e)}"