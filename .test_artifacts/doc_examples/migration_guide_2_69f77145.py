# Example from: docs\factory\migration_guide.md
# Index: 2
# Runnable: True
# Hash: 69f77145

from src.controllers.factory.deprecation import ConfigurationMigrationUtility

def quick_migrate_configuration(config_file_path: str) -> None:
    """
    One-command migration for most common use cases.

    Usage:
        quick_migrate_configuration("config.yaml")
    """

    migrator = ConfigurationMigrationUtility()

    # Perform migration with backup
    result = migrator.migrate_configuration_file(
        config_file_path=config_file_path,
        create_backup=True
    )

    if result.success:
        print(f"✓ Migration successful!")
        print(f"  Original: {result.original_file}")
        print(f"  Migrated: {result.migrated_file}")
        print(f"  Backup: {result.backup_file}")

        if result.warnings:
            print(f"  Warnings: {len(result.warnings)} deprecation warnings")

        print(f"  Summary: {result.migration_summary}")
    else:
        print(f"✗ Migration failed: {result.error}")
        if result.backup_file:
            print(f"  Backup available: {result.backup_file}")

# Example usage
quick_migrate_configuration("my_controller_config.yaml")