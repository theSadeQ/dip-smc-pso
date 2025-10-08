# Example from: docs\configuration_integration_documentation.md
# Index: 17
# Runnable: False
# Hash: d89cab34

# example-metadata:
# runnable: false

class ConfigurationMigrationManager:
    """Handle configuration parameter migrations and deprecations."""

    def __init__(self):
        self.migration_rules = self._initialize_migration_rules()
        self.deprecation_warnings = []

    def _initialize_migration_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize parameter migration rules."""

        return {
            # Version 1.0 -> 2.0 migrations
            'v1_to_v2': {
                'parameter_mappings': {
                    'use_equivalent': 'enable_equivalent_control',
                    'k_gain': 'switching_gain',
                    'lambda_gains': 'surface_gains',
                    'sat_limit': 'max_force',
                    'dt_control': 'dt',
                    'boundary_thickness': 'boundary_layer'
                },
                'structure_changes': {
                    'controllers': {
                        'old_path': 'smc_configs',
                        'new_path': 'controllers'
                    }
                },
                'value_transformations': {
                    'switching_gain': lambda x: max(x, 5.0),  # Ensure minimum value
                    'boundary_layer': lambda x: min(x, 0.1)   # Ensure maximum value
                }
            },

            # Version 2.0 -> 3.0 migrations
            'v2_to_v3': {
                'parameter_mappings': {
                    'smc_classical': 'classical_smc',
                    'smc_adaptive': 'adaptive_smc',
                    'smc_sta': 'sta_smc'
                },
                'new_required_parameters': {
                    'classical_smc': {
                        'switch_method': 'tanh',
                        'regularization': 1e-10
                    },
                    'adaptive_smc': {
                        'smooth_switch': True,
                        'alpha': 0.5
                    }
                }
            }
        }

    def migrate_configuration(self, config: Dict[str, Any],
                            from_version: str = 'v1',
                            to_version: str = 'v3') -> Dict[str, Any]:
        """Migrate configuration between versions."""

        self.deprecation_warnings.clear()
        migrated_config = config.copy()

        # Apply migrations in sequence
        if from_version == 'v1' and to_version in ['v2', 'v3']:
            migrated_config = self._apply_migration(migrated_config, 'v1_to_v2')

        if (from_version in ['v1', 'v2']) and to_version == 'v3':
            migrated_config = self._apply_migration(migrated_config, 'v2_to_v3')

        return migrated_config

    def _apply_migration(self, config: Dict[str, Any], migration_key: str) -> Dict[str, Any]:
        """Apply specific migration rules."""

        rules = self.migration_rules[migration_key]
        migrated = config.copy()

        # Apply parameter mappings
        if 'parameter_mappings' in rules:
            migrated = self._apply_parameter_mappings(migrated, rules['parameter_mappings'])

        # Apply structure changes
        if 'structure_changes' in rules:
            migrated = self._apply_structure_changes(migrated, rules['structure_changes'])

        # Apply value transformations
        if 'value_transformations' in rules:
            migrated = self._apply_value_transformations(migrated, rules['value_transformations'])

        # Add new required parameters
        if 'new_required_parameters' in rules:
            migrated = self._add_required_parameters(migrated, rules['new_required_parameters'])

        return migrated

    def _apply_parameter_mappings(self, config: Dict[str, Any],
                                mappings: Dict[str, str]) -> Dict[str, Any]:
        """Apply parameter name mappings."""

        migrated = config.copy()

        def migrate_nested(obj, path=""):
            if isinstance(obj, dict):
                new_obj = {}
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key

                    if key in mappings:
                        new_key = mappings[key]
                        new_obj[new_key] = migrate_nested(value, f"{path}.{new_key}" if path else new_key)
                        self.deprecation_warnings.append(
                            f"Parameter '{key}' deprecated, migrated to '{new_key}'"
                        )
                    else:
                        new_obj[key] = migrate_nested(value, current_path)

                return new_obj
            else:
                return obj

        return migrate_nested(migrated)

    def _apply_structure_changes(self, config: Dict[str, Any],
                               changes: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
        """Apply structural changes to configuration."""

        migrated = config.copy()

        for change_name, change_rule in changes.items():
            old_path = change_rule['old_path']
            new_path = change_rule['new_path']

            if old_path in migrated:
                # Move data from old path to new path
                migrated[new_path] = migrated.pop(old_path)
                self.deprecation_warnings.append(
                    f"Configuration section '{old_path}' moved to '{new_path}'"
                )

        return migrated

    def _apply_value_transformations(self, config: Dict[str, Any],
                                   transformations: Dict[str, callable]) -> Dict[str, Any]:
        """Apply value transformations."""

        def transform_nested(obj):
            if isinstance(obj, dict):
                new_obj = {}
                for key, value in obj.items():
                    if key in transformations:
                        try:
                            new_obj[key] = transformations[key](value)
                            self.deprecation_warnings.append(
                                f"Value transformation applied to '{key}'"
                            )
                        except Exception as e:
                            new_obj[key] = value
                            self.deprecation_warnings.append(
                                f"Value transformation failed for '{key}': {e}"
                            )
                    else:
                        new_obj[key] = transform_nested(value)
                return new_obj
            else:
                return obj

        return transform_nested(config)

    def _add_required_parameters(self, config: Dict[str, Any],
                               required_params: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Add new required parameters with default values."""

        migrated = config.copy()

        # Ensure controllers section exists
        if 'controllers' not in migrated:
            migrated['controllers'] = {}

        for controller_type, params in required_params.items():
            if controller_type not in migrated['controllers']:
                migrated['controllers'][controller_type] = {}

            controller_config = migrated['controllers'][controller_type]

            for param_name, default_value in params.items():
                if param_name not in controller_config:
                    controller_config[param_name] = default_value
                    self.deprecation_warnings.append(
                        f"Added required parameter '{param_name}' to {controller_type}"
                    )

        return migrated

    def check_deprecated_config(self, controller_type: str,
                              params: Dict[str, Any]) -> Dict[str, Any]:
        """Check for and handle deprecated parameters."""

        # Current deprecation mappings
        current_deprecations = {
            'use_equivalent': 'enable_equivalent_control',
            'k_gain': 'switching_gain',
            'lambda_gains': 'surface_gains',
            'sat_limit': 'max_force',
            'boundary_thickness': 'boundary_layer'
        }

        migrated_params = params.copy()

        for old_param, new_param in current_deprecations.items():
            if old_param in migrated_params:
                migrated_params[new_param] = migrated_params.pop(old_param)
                self.deprecation_warnings.append(
                    f"Parameter '{old_param}' is deprecated. Use '{new_param}' instead."
                )

        return migrated_params

    def get_deprecation_warnings(self) -> List[str]:
        """Get list of deprecation warnings."""
        return self.deprecation_warnings.copy()

# Usage
migration_manager = ConfigurationMigrationManager()

# Migrate old configuration
old_config = {
    'smc_configs': {
        'smc_classical': {
            'k_gain': 35.0,
            'lambda_gains': [12.0, 8.0],
            'sat_limit': 150.0,
            'boundary_thickness': 0.02
        }
    }
}

migrated_config = migration_manager.migrate_configuration(
    old_config,
    from_version='v1',
    to_version='v3'
)

print("Migrated configuration:")
print(yaml.dump(migrated_config, default_flow_style=False))

print("\nDeprecation warnings:")
for warning in migration_manager.get_deprecation_warnings():
    print(f"  ⚠️  {warning}")