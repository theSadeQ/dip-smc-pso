# Example from: docs\pso_configuration_schema_documentation.md
# Index: 6
# Runnable: False
# Hash: 85560616

class ConfigurationMigrator:
    """
    Automatic migration framework for PSO configuration schema evolution.
    """

    def __init__(self):
        self.migration_rules = {
            "1.0": self._migrate_from_v1_0,
            "1.5": self._migrate_from_v1_5,
            "2.0": self._migrate_from_v2_0
        }

    def migrate_configuration(self, config: dict, source_version: str) -> tuple:
        """
        Migrate configuration from source version to current schema.

        Returns:
        tuple: (migrated_config, migration_warnings, compatibility_issues)
        """
        if source_version not in self.migration_rules:
            raise ValueError(f"Unsupported source version: {source_version}")

        migrated_config = config.copy()
        warnings = []
        issues = []

        # Apply migration rules in sequence
        current_version = source_version
        while current_version != CURRENT_SCHEMA_VERSION:
            migrator = self.migration_rules[current_version]
            migrated_config, step_warnings = migrator(migrated_config)
            warnings.extend(step_warnings)
            current_version = self._get_next_version(current_version)

        # Validate migrated configuration
        validation_result = PSO_ConfigurationValidator().validate_complete_config(migrated_config)
        if not validation_result.is_valid:
            issues.extend(validation_result.errors)

        return migrated_config, warnings, issues

    def _migrate_from_v1_0(self, config: dict) -> tuple:
        """
        Migrate from v1.0 to v1.5: Remove deprecated fields, update bounds.
        """
        migrated = config.copy()
        warnings = []

        # Remove deprecated fields
        deprecated_fields = ['n_processes', 'hyper_trials', 'hyper_search', 'study_timeout']
        for field in deprecated_fields:
            if field in migrated.get('pso', {}):
                del migrated['pso'][field]
                warnings.append(f"Removed deprecated field: {field}")

        # Update PSO bounds structure
        if 'pso' in migrated and 'bounds' in migrated['pso']:
            old_bounds = migrated['pso']['bounds']
            new_bounds = self._restructure_bounds_v1_5(old_bounds)
            migrated['pso']['bounds'] = new_bounds
            warnings.append("Restructured bounds for controller-specific optimization")

        return migrated, warnings

    def _migrate_from_v2_0(self, config: dict) -> tuple:
        """
        Migrate from v2.0 to v2.1: Issue #2 bounds updates and enhanced features.
        """
        migrated = config.copy()
        warnings = []

        # Update STA-SMC bounds for Issue #2 compliance
        if 'pso' in migrated and 'bounds' in migrated['pso']:
            bounds = migrated['pso']['bounds']
            if 'sta_smc' in bounds:
                sta_bounds = bounds['sta_smc']

                # Check for Issue #2 problematic bounds
                if 'max' in sta_bounds and len(sta_bounds['max']) >= 6:
                    lambda1_max, lambda2_max = sta_bounds['max'][4], sta_bounds['max'][5]
                    if lambda1_max > 10.0 or lambda2_max > 10.0:
                        # Apply Issue #2 corrections
                        sta_bounds['max'][4] = min(lambda1_max, 10.0)  # lambda1
                        sta_bounds['max'][5] = min(lambda2_max, 10.0)  # lambda2
                        warnings.append("Applied Issue #2 lambda bounds corrections for overshoot mitigation")

        # Add enhanced features if missing
        if 'enhanced_features' not in migrated.get('pso', {}):
            migrated['pso']['enhanced_features'] = {
                'w_schedule': [0.9, 0.4],
                'velocity_clamp': [0.1, 0.2],
                'early_stopping': {'patience': 50, 'tolerance': 1e-6}
            }
            warnings.append("Added enhanced PSO features for improved convergence")

        return migrated, warnings

    def generate_migration_report(self, old_config: dict, new_config: dict,
                                warnings: list, issues: list) -> str:
        """
        Generate comprehensive migration report for documentation.
        """
        report = f"""
# PSO Configuration Migration Report

## Summary
- **Source Version**: {old_config.get('schema_version', 'unknown')}
- **Target Version**: {CURRENT_SCHEMA_VERSION}
- **Migration Status**: {'SUCCESS' if not issues else 'NEEDS ATTENTION'}

## Changes Applied
"""
        for warning in warnings:
            report += f"- {warning}\n"

        if issues:
            report += "\n## Issues Requiring Attention\n"
            for issue in issues:
                report += f"- {issue}\n"

        report += f"""
## Validation Summary
- **Mathematical Consistency**: {'✓' if self._check_math_consistency(new_config) else '✗'}
- **Controller Compatibility**: {'✓' if self._check_controller_compatibility(new_config) else '✗'}
- **Issue #2 Compliance**: {'✓' if self._check_issue2_compliance(new_config) else '✗'}
- **Performance Optimized**: {'✓' if self._check_performance_optimization(new_config) else '✗'}

## Next Steps
1. Review configuration changes and validate against system requirements
2. Test PSO optimization with migrated configuration
3. Monitor performance and adjust parameters if necessary
4. Update documentation to reflect configuration changes
"""
        return report