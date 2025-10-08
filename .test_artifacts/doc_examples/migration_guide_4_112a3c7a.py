# Example from: docs\factory\migration_guide.md
# Index: 4
# Runnable: False
# Hash: 112a3c7a

def interactive_migration_wizard() -> None:
    """
    Interactive step-by-step migration wizard for complex configurations.
    """

    print("=== SMC Controller Configuration Migration Wizard ===\n")

    # Step 1: Configuration file location
    config_path = input("Enter path to configuration file: ").strip()

    if not os.path.exists(config_path):
        print(f"Error: File not found - {config_path}")
        return

    # Step 2: Backup preferences
    create_backup = input("Create backup before migration? (Y/n): ").strip().lower()
    create_backup = create_backup != 'n'

    # Step 3: Migration analysis
    print("\nAnalyzing configuration...")
    migrator = ConfigurationMigrationUtility()

    # Load and analyze configuration
    try:
        with open(config_path, 'r') as f:
            if config_path.endswith(('.yml', '.yaml')):
                import yaml
                config_data = yaml.safe_load(f)
            else:
                import json
                config_data = json.load(f)

        # Analyze deprecations
        warner = ControllerDeprecationWarner()
        analysis_results = {}

        if 'controllers' in config_data:
            for controller_type, controller_config in config_data['controllers'].items():
                if isinstance(controller_config, dict):
                    _, warnings = warner.check_deprecated_parameters(controller_type, controller_config)
                    analysis_results[controller_type] = warnings

        # Display analysis
        total_warnings = sum(len(warnings) for warnings in analysis_results.values())

        if total_warnings == 0:
            print("✓ No deprecated parameters found. Configuration is up to date.")
            return

        print(f"Found {total_warnings} deprecated parameters:")

        for controller_type, warnings in analysis_results.items():
            if warnings:
                print(f"\n  {controller_type}:")
                for warning in warnings:
                    print(f"    - {warning.old_parameter}: {warning.migration_guide}")

        # Step 4: Confirm migration
        proceed = input(f"\nProceed with migration? (Y/n): ").strip().lower()
        if proceed == 'n':
            print("Migration cancelled.")
            return

        # Step 5: Perform migration
        print("\nPerforming migration...")
        result = migrator.migrate_configuration_file(
            config_file_path=config_path,
            create_backup=create_backup
        )

        if result.success:
            print("✓ Migration completed successfully!")

            if result.backup_file:
                print(f"  Backup created: {result.backup_file}")

            # Step 6: Validation
            validate = input("\nValidate migrated configuration? (Y/n): ").strip().lower()
            if validate != 'n':
                validation_result = migrator.validate_migrated_configuration(
                    result.migration_summary.get('migrated_config', {})
                )

                if validation_result.success:
                    print("✓ Validation passed - configuration is ready to use.")
                else:
                    print("⚠ Validation issues found:")
                    for issue in validation_result.issues:
                        print(f"    - {issue}")
        else:
            print(f"✗ Migration failed: {result.error}")

    except Exception as e:
        print(f"Error during migration analysis: {e}")

# Run the wizard
interactive_migration_wizard()