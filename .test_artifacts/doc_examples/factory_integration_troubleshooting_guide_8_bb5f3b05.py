# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 8
# Runnable: True
# Hash: bb5f3b05

def create_controller_robust(controller_type, **kwargs):
    """Create controller with robust parameter handling."""

    try:
        # Try with provided parameters
        return create_controller(controller_type, **kwargs)

    except TypeError as e:
        if "unexpected keyword argument" in str(e):
            # Extract parameter name from error
            import re
            match = re.search(r"'(\w+)'", str(e))
            if match:
                invalid_param = match.group(1)
                print(f"Removing invalid parameter: {invalid_param}")

                # Remove invalid parameter and retry
                filtered_kwargs = {k: v for k, v in kwargs.items() if k != invalid_param}
                return create_controller(controller_type, **filtered_kwargs)

        raise  # Re-raise if we can't handle it

# Usage
controller = create_controller_robust(
    'classical_smc',
    gains=[20, 15, 12, 8, 35, 5],
    invalid_param='will_be_removed'  # This will be filtered out
)