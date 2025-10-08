# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 1
# Runnable: True
# Hash: 3e69a44a

def require_positive(
    value: Union[float, int, None],
    name: str,
    *,
    allow_zero: bool = False
) -> float