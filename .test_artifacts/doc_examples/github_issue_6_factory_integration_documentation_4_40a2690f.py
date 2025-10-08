# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 4
# Runnable: True
# Hash: 40a2690f

def validate_sta_gains(gains: List[float]) -> bool:
    """Validate super-twisting stability constraints."""
    K1, K2 = gains[0], gains[1]
    return K1 > K2 > 0  # Critical constraint for convergence