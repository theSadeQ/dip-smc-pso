# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 13
# Runnable: False
# Hash: 73517169

{
    'valid': bool,                        # Overall validation result
    'violations': List[Dict],             # List of violations (if any)
    'controller_type': str,               # Controller type validated
    'gains_checked': int,                 # Number of gains validated
    'gains_provided': int                 # Number of gains provided
}

# Stability result structure
{
    'stable': bool,                       # Stability conditions satisfied
    'issues': List[str],                  # Stability issues (if any)
    'controller_type': str                # Controller type
}