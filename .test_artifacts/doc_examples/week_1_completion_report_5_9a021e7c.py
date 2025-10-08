# Example from: docs\plans\documentation\week_1_completion_report.md
# Index: 5
# Runnable: True
# Hash: 9a021e7c

@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    message: str
    details: List[str] = None