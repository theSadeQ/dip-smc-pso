# Example from: docs\api\factory_system_api_reference.md
# Index: 42
# Runnable: False
# Hash: 844a9fe3

# example-metadata:
# runnable: false

def _validate_controller_gains(gains, controller_info, controller_type):
    expected_count = controller_info['gain_count']
    if len(gains) != expected_count:
        raise ValueError(
            f"Controller '{controller_info.get('description', 'unknown')}' "
            f"requires {expected_count} gains, got {len(gains)}"
        )

    if not all(isinstance(g, (int, float)) and np.isfinite(g) for g in gains):
        raise ValueError("All gains must be finite numbers")

    if any(g <= 0 for g in gains):
        raise ValueError("All gains must be positive")

    # Controller-specific validation...