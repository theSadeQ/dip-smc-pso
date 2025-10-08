# Example from: docs\factory\migration_guide.md
# Index: 17
# Runnable: False
# Hash: 7c99c384

# example-metadata:
# runnable: false

def document_migration_changes(migration_log: List[str]) -> str:
    """Create documentation of migration changes for reference."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    doc = f"""
Migration Report - {timestamp}

Changes Applied:
{chr(10).join(f"- {change}" for change in migration_log)}

Validation Status: PASSED
Next Steps:
- Update any hardcoded parameter references in code
- Test controllers with actual plant dynamics
- Update documentation and training materials
"""

    return doc