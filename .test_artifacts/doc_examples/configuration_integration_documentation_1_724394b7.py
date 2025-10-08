# Example from: docs\configuration_integration_documentation.md
# Index: 1
# Runnable: True
# Hash: 724394b7

def demonstrate_configuration_priority():
    """Demonstrate configuration priority resolution."""

    from src.config import load_config
    from src.controllers.factory import create_controller

    # Load YAML configuration
    config = load_config("config.yaml")  # Contains gains: [10, 8, 5, 3, 20, 2]

    # Priority 1: Explicit parameters override everything
    controller = create_controller(
        'classical_smc',
        config=config,
        gains=[25, 20, 15, 10, 40, 6]  # These gains will be used (Priority 1)
    )
    print(f"Priority 1 - Explicit gains: {controller.gains}")

    # Priority 2: Configuration object when no explicit parameters
    controller = create_controller(
        'classical_smc',
        config=config  # Uses gains from config.yaml (Priority 2)
    )
    print(f"Priority 2 - Config gains: {controller.gains}")

    # Priority 3: Registry defaults when no config provided
    controller = create_controller('classical_smc')  # Uses registry defaults (Priority 3)
    print(f"Priority 3 - Default gains: {controller.gains}")

demonstrate_configuration_priority()