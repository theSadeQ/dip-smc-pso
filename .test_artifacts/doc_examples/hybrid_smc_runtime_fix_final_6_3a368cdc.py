# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 6
# Runnable: True
# Hash: 3a368cdc

# Pre-commit hook suggestion
def validate_controller_returns():
    """Ensure all controller methods have explicit returns."""
    patterns_to_check = [
        "def compute_control(",
        "def reset(",
        "def initialize_state("
    ]
    # Validate all code paths have returns