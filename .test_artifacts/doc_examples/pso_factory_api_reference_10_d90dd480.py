# Example from: docs\factory\pso_factory_api_reference.md
# Index: 10
# Runnable: True
# Hash: d90dd480

is_valid, error = controller.validate_state_input(test_state)
            if not is_valid:
                print(f"Invalid state: {error}")