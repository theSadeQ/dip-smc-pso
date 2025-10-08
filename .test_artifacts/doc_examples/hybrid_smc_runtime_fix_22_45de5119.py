# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 22
# Runnable: False
# Hash: 45de5119

try:
    result = controller.compute_control(...)
    if result is None:
        raise TypeError("Controller returned None - check implementation")
    return result
except Exception as e:
    logger.error(f"Controller failed: {e}", exc_info=True)
    raise  # Re-raise for proper error handling