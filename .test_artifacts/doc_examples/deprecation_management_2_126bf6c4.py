# Example from: docs\factory\deprecation_management.md
# Index: 2
# Runnable: False
# Hash: 126bf6c4

# example-metadata:
# runnable: false

@dataclass
class DeprecationMapping:
    """Complete deprecation specification for a parameter or feature."""
    old_name: str                           # Deprecated parameter name
    new_name: Optional[str] = None          # New parameter name (if renamed)
    level: DeprecationLevel = WARNING      # Current deprecation level
    message: Optional[str] = None          # Custom deprecation message
    migration_guide: Optional[str] = None  # Detailed migration instructions
    removed_in_version: Optional[str] = None  # Target removal version
    introduced_in_version: Optional[str] = None  # When deprecation started
    auto_migrate: bool = True              # Enable automatic migration
    validation_function: Optional[Callable] = None  # Custom validation