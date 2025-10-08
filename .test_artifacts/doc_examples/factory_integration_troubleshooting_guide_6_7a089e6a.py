# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 6
# Runnable: False
# Hash: 7a089e6a

def create_controller_with_fallback(preferred_type, fallback_type, **kwargs):
    """Create controller with automatic fallback."""

    try:
        return create_controller(preferred_type, **kwargs)
    except ImportError:
        print(f"Warning: {preferred_type} not available, using {fallback_type}")
        return create_controller(fallback_type, **kwargs)

# Example: Try MPC, fallback to classical SMC
controller = create_controller_with_fallback(
    'mpc_controller',
    'classical_smc',
    gains=[20, 15, 12, 8, 35, 5]
)