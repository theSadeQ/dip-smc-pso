# Example from: docs\reports\integration_validation_report.md
# Index: 3
# Runnable: True
# Hash: 681d73ef

@dataclass
class DeprecationMapping:
    old_name: str
    new_name: Optional[str]
    level: DeprecationLevel
    migration_guide: str
    # Automatic parameter migration with user guidance