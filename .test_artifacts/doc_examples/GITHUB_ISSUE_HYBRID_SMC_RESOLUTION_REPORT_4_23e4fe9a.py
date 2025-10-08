# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 4
# Runnable: True
# Hash: 23e4fe9a

def _extract_control_value(self, active_result):
    """Extract control value with comprehensive type checking."""
    if isinstance(active_result, dict):
        return active_result.get('control', 0.0)
    elif hasattr(active_result, 'control'):
        return active_result.control
    else:
        logger.warning(f"Unexpected result type: {type(active_result)}")
        return 0.0