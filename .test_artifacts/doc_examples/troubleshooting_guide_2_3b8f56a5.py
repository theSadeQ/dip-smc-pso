# Example from: docs\factory\troubleshooting_guide.md
# Index: 2
# Runnable: True
# Hash: 3b8f56a5

from src.controllers.factory import list_available_controllers, CONTROLLER_ALIASES

def diagnose_controller_type_error(controller_type):
    print(f"Diagnosing controller type: '{controller_type}'")

    # Check available types
    available = list_available_controllers()
    print(f"Available types: {available}")

    # Check aliases
    normalized = controller_type.lower().replace('-', '_').replace(' ', '_')
    if normalized in CONTROLLER_ALIASES:
        canonical = CONTROLLER_ALIASES[normalized]
        print(f"Found alias: '{controller_type}' -> '{canonical}'")
    else:
        print(f"No alias found for '{controller_type}'")

    # Suggest closest match
    from difflib import get_close_matches
    matches = get_close_matches(normalized, available + list(CONTROLLER_ALIASES.keys()))
    if matches:
        print(f"Did you mean: {matches[0]}?")

# Example usage
diagnose_controller_type_error("classic_smc")  # Should find alias