# Example from: docs\factory\deprecation_management.md
# Index: 8
# Runnable: True
# Hash: 935e93f3

class ConfigurationMigrationUtility:
    """
    Utility for migrating entire configuration files and structures.

    Features:
    - Batch configuration migration
    - Backup creation before migration
    - Validation of migrated configurations
    - Rollback capability
    """

    def __init__(self):
        self.warner = ControllerDeprecationWarner()
        self.backup_directory = Path(".config_backups")
        self.backup_directory.mkdir(exist_ok=True)

    def migrate_configuration_file(
        self,
        config_file_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        create_backup: bool = True
    ) -> 'ConfigMigrationResult':
        """
        Migrate an entire configuration file.

        Args:
            config_file_path: Path to configuration file
            output_path: Output path (defaults to overwrite original)
            create_backup: Whether to create backup before migration

        Returns:
            Migration result with details and statistics
        """
        config_path = Path(config_file_path)

        if not config_path.exists():
            return ConfigMigrationResult(
                success=False,
                error=f"Configuration file not found: {config_path}"
            )

        try:
            # Create backup if requested
            backup_path = None
            if create_backup:
                backup_path = self._create_backup(config_path)

            # Load configuration
            with open(config_path, 'r') as f:
                if config_path.suffix.lower() in ['.yml', '.yaml']:
                    import yaml
                    config_data = yaml.safe_load(f)
                elif config_path.suffix.lower() == '.json':
                    import json
                    config_data = json.load(f)
                else:
                    return ConfigMigrationResult(
                        success=False,
                        error=f"Unsupported configuration format: {config_path.suffix}"
                    )

            # Perform migration
            migration_result = self.migrate_configuration_data(config_data)

            # Save migrated configuration
            output_file = Path(output_path) if output_path else config_path

            with open(output_file, 'w') as f:
                if config_path.suffix.lower() in ['.yml', '.yaml']:
                    yaml.dump(migration_result.migrated_config, f, default_flow_style=False)
                elif config_path.suffix.lower() == '.json':
                    json.dump(migration_result.migrated_config, f, indent=2)

            return ConfigMigrationResult(
                success=True,
                original_file=config_path,
                migrated_file=output_file,
                backup_file=backup_path,
                migration_summary=migration_result.migration_summary,
                warnings=migration_result.warnings
            )

        except Exception as e:
            return ConfigMigrationResult(
                success=False,
                error=f"Migration failed: {str(e)}",
                original_file=config_path
            )

    def migrate_configuration_data(self, config_data: Dict[str, Any]) -> 'DataMigrationResult':
        """
        Migrate configuration data structure.

        Args:
            config_data: Configuration data dictionary

        Returns:
            Migration result with migrated data and summary
        """
        migrated_config = config_data.copy()
        all_warnings = []
        migration_summary = {
            'parameters_migrated': 0,
            'parameters_removed': 0,
            'controllers_processed': 0,
            'migration_details': []
        }

        # Process controller configurations
        if 'controllers' in migrated_config:
            for controller_type, controller_config in migrated_config['controllers'].items():
                if isinstance(controller_config, dict):
                    migrated_params, warnings = self.warner.check_deprecated_parameters(
                        controller_type, controller_config
                    )

                    migrated_config['controllers'][controller_type] = migrated_params
                    all_warnings.extend(warnings)

                    migration_summary['controllers_processed'] += 1
                    migration_summary['migration_details'].append({
                        'controller_type': controller_type,
                        'warnings_count': len(warnings),
                        'migration_applied': len(warnings) > 0
                    })

        # Process legacy controller_defaults structure
        if 'controller_defaults' in migrated_config:
            for controller_type, controller_config in migrated_config['controller_defaults'].items():
                if isinstance(controller_config, dict):
                    migrated_params, warnings = self.warner.check_deprecated_parameters(
                        controller_type, controller_config
                    )

                    migrated_config['controller_defaults'][controller_type] = migrated_params
                    all_warnings.extend(warnings)

        # Update migration summary
        migration_summary['parameters_migrated'] = sum(
            len(detail.get('warnings', [])) for detail in migration_summary['migration_details']
        )

        return DataMigrationResult(
            migrated_config=migrated_config,
            warnings=all_warnings,
            migration_summary=migration_summary
        )

    def _create_backup(self, config_path: Path) -> Path:
        """Create timestamped backup of configuration file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{config_path.stem}_{timestamp}{config_path.suffix}"
        backup_path = self.backup_directory / backup_name

        shutil.copy2(config_path, backup_path)
        return backup_path

    def validate_migrated_configuration(
        self,
        migrated_config: Dict[str, Any]
    ) -> 'ValidationResult':
        """
        Validate migrated configuration for correctness.

        Args:
            migrated_config: Migrated configuration data

        Returns:
            Validation result with success status and issues
        """
        validation_issues = []

        try:
            # Test controller creation with migrated configuration
            if 'controllers' in migrated_config:
                for controller_type, controller_config in migrated_config['controllers'].items():
                    try:
                        # Attempt to create controller to validate configuration
                        from src.controllers.factory import create_controller
                        controller = create_controller(
                            controller_type=controller_type,
                            config=Mock(controllers={controller_type: controller_config}),
                            gains=controller_config.get('gains')
                        )

                        if controller is None:
                            validation_issues.append(
                                f"Failed to create {controller_type} with migrated configuration"
                            )

                    except Exception as e:
                        validation_issues.append(
                            f"Validation error for {controller_type}: {str(e)}"
                        )

            return ValidationResult(
                success=len(validation_issues) == 0,
                issues=validation_issues
            )

        except Exception as e:
            return ValidationResult(
                success=False,
                issues=[f"Validation process failed: {str(e)}"]
            )

@dataclass
class ConfigMigrationResult:
    """Result of configuration file migration."""
    success: bool
    original_file: Optional[Path] = None
    migrated_file: Optional[Path] = None
    backup_file: Optional[Path] = None
    migration_summary: Optional[Dict[str, Any]] = None
    warnings: List[DeprecationWarning] = field(default_factory=list)
    error: Optional[str] = None

@dataclass
class DataMigrationResult:
    """Result of configuration data migration."""
    migrated_config: Dict[str, Any]
    warnings: List[DeprecationWarning]
    migration_summary: Dict[str, Any]

@dataclass
class ValidationResult:
    """Result of configuration validation."""
    success: bool
    issues: List[str] = field(default_factory=list)