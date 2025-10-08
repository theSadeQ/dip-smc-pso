# Example from: docs\factory\troubleshooting_guide.md
# Index: 3
# Runnable: True
# Hash: 673eba25

from src.controllers.factory import CONTROLLER_REGISTRY

def diagnose_gain_count_error(controller_type, provided_gains):
    print(f"Diagnosing gain count for {controller_type}")

    if controller_type in CONTROLLER_REGISTRY:
        info = CONTROLLER_REGISTRY[controller_type]
        required = info['gain_count']
        provided = len(provided_gains)

        print(f"Required gains: {required}")
        print(f"Provided gains: {provided}")
        print(f"Gain names: {info.get('gain_names', 'Not specified')}")

        if provided < required:
            print(f"Missing {required - provided} gains")
            defaults = info['default_gains']
            suggested = provided_gains + defaults[provided:required]
            print(f"Suggested gains: {suggested}")
        elif provided > required:
            print(f"Extra {provided - required} gains provided")
            suggested = provided_gains[:required]
            print(f"Suggested gains: {suggested}")
    else:
        print(f"Unknown controller type: {controller_type}")

# Example usage
diagnose_gain_count_error('classical_smc', [10, 5, 8])  # Too few gains