# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 9
# Runnable: False
# Hash: b2ee849e

# example-metadata:
# runnable: false

# Add to pre-commit hooks:
# mypy type checking for return type consistency
def check_return_types():
    """Verify all controller methods return expected types."""
    assert isinstance(controller.compute_control(...), HybridSTAOutput)