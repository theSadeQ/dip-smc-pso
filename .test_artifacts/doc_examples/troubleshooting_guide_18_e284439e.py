# Example from: docs\factory\troubleshooting_guide.md
# Index: 18
# Runnable: False
# Hash: e284439e

def robust_controller_creation(controller_type, gains=None, config=None, max_retries=3):
    """Robust controller creation with automatic error recovery."""

    from src.controllers.factory import create_controller, get_default_gains

    for attempt in range(max_retries):
        try:
            return create_controller(controller_type, config=config, gains=gains)

        except ValueError as e:
            error_str = str(e)

            if "gains" in error_str and gains is None:
                # Try with default gains
                gains = get_default_gains(controller_type)
                print(f"Attempt {attempt + 1}: Using default gains")
                continue

            elif "requires" in error_str and "gains" in error_str:
                # Fix gain count
                if gains and controller_type in CONTROLLER_REGISTRY:
                    required = CONTROLLER_REGISTRY[controller_type]['gain_count']
                    defaults = get_default_gains(controller_type)

                    if len(gains) < required:
                        gains = gains + defaults[len(gains):required]
                    elif len(gains) > required:
                        gains = gains[:required]

                    print(f"Attempt {attempt + 1}: Adjusted gain count")
                    continue

            raise  # Re-raise if can't handle

        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}, retrying...")

    raise RuntimeError(f"Failed to create controller after {max_retries} attempts")

# Example usage
controller = robust_controller_creation('classical_smc', gains=[10, 5, 8])