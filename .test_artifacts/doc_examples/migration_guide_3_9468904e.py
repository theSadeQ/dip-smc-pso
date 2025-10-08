# Example from: docs\factory\migration_guide.md
# Index: 3
# Runnable: True
# Hash: 9468904e

def migrate_project_configurations(project_directory: str) -> None:
    """
    Migrate all configuration files in a project directory.

    Usage:
        migrate_project_configurations("/path/to/project")
    """
    import os
    from pathlib import Path

    project_path = Path(project_directory)
    migrator = ConfigurationMigrationUtility()

    # Find all configuration files
    config_patterns = ['*.yaml', '*.yml', '*.json']
    config_files = []

    for pattern in config_patterns:
        config_files.extend(project_path.rglob(pattern))

    # Filter for likely controller configuration files
    controller_configs = []
    for config_file in config_files:
        if any(keyword in config_file.name.lower() for keyword in
               ['controller', 'smc', 'config', 'param']):
            controller_configs.append(config_file)

    print(f"Found {len(controller_configs)} potential configuration files")

    migration_results = []

    for config_file in controller_configs:
        print(f"\nMigrating: {config_file}")

        result = migrator.migrate_configuration_file(
            config_file_path=config_file,
            create_backup=True
        )

        migration_results.append(result)

        if result.success:
            print(f"  ✓ Success - {len(result.warnings)} warnings")
        else:
            print(f"  ✗ Failed - {result.error}")

    # Summary
    successful = sum(1 for r in migration_results if r.success)
    total = len(migration_results)

    print(f"\n=== Migration Summary ===")
    print(f"Total files processed: {total}")
    print(f"Successful migrations: {successful}")
    print(f"Failed migrations: {total - successful}")

    if successful < total:
        print("\nFailed files require manual migration:")
        for result in migration_results:
            if not result.success:
                print(f"  - {result.original_file}: {result.error}")

# Example usage
migrate_project_configurations("./my_smc_project")