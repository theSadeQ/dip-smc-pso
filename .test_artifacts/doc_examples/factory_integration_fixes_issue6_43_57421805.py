# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 43
# Runnable: True
# Hash: 57421805

# New way - automatic error recovery
controller = create_controller('classical_smc', gains=invalid_gains)
# Factory automatically:
# - Validates gains according to SMC theory
# - Provides detailed error messages
# - Falls back to safe default gains if needed
# - Logs warnings for debugging