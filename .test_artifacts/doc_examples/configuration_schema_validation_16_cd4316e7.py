# Example from: docs\configuration_schema_validation.md
# Index: 16
# Runnable: False
# Hash: cd4316e7

# example-metadata:
# runnable: false

class ConfigurationMigrator:
    """Handle configuration schema migrations."""

    MIGRATIONS = {
        '1.0.0': {
            'to': '2.0.0',
            'changes': [
                'Add system.version field',
                'Restructure controller configurations',
                'Add optimization.pso.bounds validation'
            ],
            'migration_func': 'migrate_1_0_to_2_0'
        },
        '2.0.0': {
            'to': '2.1.0',
            'changes': [
                'Add HIL configuration section',
                'Enhanced PSO stability validation',
                'Add runtime parameter constraints'
            ],
            'migration_func': 'migrate_2_0_to_2_1'
        }
    }

    def migrate_config(self, config_data: dict, target_version: str = None) -> dict:
        """Migrate configuration to target version."""

        current_version = config_data.get('system', {}).get('version', '1.0.0')
        target_version = target_version or self._get_latest_version()

        if current_version == target_version:
            return config_data

        # Find migration path
        migration_path = self._find_migration_path(current_version, target_version)

        # Apply migrations in sequence
        migrated_config = config_data
        for version in migration_path:
            migration = self.MIGRATIONS[version]
            migration_func = getattr(self, migration['migration_func'])
            migrated_config = migration_func(migrated_config)

        return migrated_config

    def migrate_1_0_to_2_0(self, config: dict) -> dict:
        """Migrate from version 1.0 to 2.0."""
        migrated = config.copy()

        # Add system section if missing
        if 'system' not in migrated:
            migrated['system'] = {
                'version': '2.0.0',
                'environment': 'development',
                'logging_level': 'INFO'
            }

        # Restructure controller configurations
        if 'controllers' in migrated:
            for controller_name, controller_config in migrated['controllers'].items():
                # Add default saturation limits if missing
                if 'saturation_limit' not in controller_config:
                    controller_config['saturation_limit'] = 10.0

        # Add PSO bounds validation
        if 'optimization' in migrated and 'pso' in migrated['optimization']:
            pso_config = migrated['optimization']['pso']
            if 'bounds' not in pso_config:
                # Add default bounds
                pso_config['bounds'] = {
                    'classical_smc': [[0.1, 50.0]] * 6,
                    'sta_smc': [[0.1, 20.0], [0.1, 20.0]],
                    'adaptive_smc': [[0.1, 50.0]] * 6
                }

        return migrated

    def migrate_2_0_to_2_1(self, config: dict) -> dict:
        """Migrate from version 2.0 to 2.1."""
        migrated = config.copy()

        # Update version
        migrated['system']['version'] = '2.1.0'

        # Add HIL section if missing
        if 'hil' not in migrated:
            migrated['hil'] = {
                'enabled': False,
                'plant_address': '127.0.0.1',
                'plant_port': 8080,
                'controller_port': 8081,
                'timeout': 1.0
            }

        return migrated