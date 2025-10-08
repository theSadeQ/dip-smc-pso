# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 42
# Runnable: True
# Hash: 7fd2670d

# Old way - manual error handling required
try:
    controller = create_controller('classical_smc', gains=invalid_gains)
except Exception as e:
    # Handle error manually
    print(f"Controller creation failed: {e}")
    # Create fallback controller manually