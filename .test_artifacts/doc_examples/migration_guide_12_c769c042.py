# Example from: docs\factory\migration_guide.md
# Index: 12
# Runnable: False
# Hash: c769c042

def fix_gain_array_length(controller_type: str, gains: List[float]) -> List[float]:
    """Fix gain array length to match controller requirements."""

    expected_lengths = {
        'classical_smc': 6,
        'adaptive_smc': 5,
        'sta_smc': 6,
        'hybrid_adaptive_sta_smc': 4
    }

    expected_length = expected_lengths.get(controller_type, 6)

    if len(gains) < expected_length:
        # Pad with reasonable defaults
        default_gains = {
            'classical_smc': [8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
            'adaptive_smc': [12.0, 10.0, 6.0, 5.0, 2.5],
            'sta_smc': [35.0, 20.0, 25.0, 18.0, 12.0, 8.0],
            'hybrid_adaptive_sta_smc': [18.0, 12.0, 10.0, 8.0]
        }

        defaults = default_gains.get(controller_type, [1.0] * expected_length)
        gains.extend(defaults[len(gains):expected_length])

    elif len(gains) > expected_length:
        # Truncate to expected length
        gains = gains[:expected_length]

    return gains