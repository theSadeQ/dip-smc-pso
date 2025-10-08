# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 14
# Runnable: False
# Hash: 96039ab8

# example-metadata:
# runnable: false

# Before (Problematic)
try:
    result = controller.compute_control(state)
except Exception:
    return "Error occurred"  # Masks real issues

# After (Improved)
try:
    result = controller.compute_control(state)
    if result is None:
        raise TypeError("Controller returned None - implementation bug")
    return result
except TypeError as e:
    logger.error(f"Implementation error: {e}", exc_info=True)
    raise  # Don't mask implementation bugs
except Exception as e:
    logger.warning(f"Operational error: {e}")
    return fallback_result()  # Handle operational errors gracefully