# Example from: docs\factory\troubleshooting_guide.md
# Index: 4
# Runnable: False
# Hash: 318e0ff3

# example-metadata:
# runnable: false

def diagnose_gain_values(gains):
    print(f"Diagnosing gain values: {gains}")

    for i, gain in enumerate(gains):
        if not isinstance(gain, (int, float)):
            print(f"✗ Gain {i}: {gain} is not numeric (type: {type(gain)})")
        elif not np.isfinite(gain):
            print(f"✗ Gain {i}: {gain} is not finite")
        elif gain <= 0:
            print(f"✗ Gain {i}: {gain} is not positive")
        else:
            print(f"✓ Gain {i}: {gain} is valid")

# Example usage
diagnose_gain_values([10.0, -5.0, float('inf'), 'invalid', 8.0])