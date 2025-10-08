# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 5
# Runnable: True
# Hash: c7a92ca7

def require_in_range(
    value: Union[float, int, None],
    name: str,
    *,
    minimum: float,
    maximum: float,
    allow_equal: bool = True
) -> float