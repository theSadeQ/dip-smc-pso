# Example from: docs\pso_integration_technical_specification.md
# Index: 11
# Runnable: False
# Hash: 7243a281

# example-metadata:
# runnable: false

def migrate_pso_configuration(legacy_config: dict) -> PSOConfig:
    """
    Migrate legacy PSO configuration to current schema with validation.

    Migration Rules:
    1. Remove deprecated fields with warnings
    2. Update bounds for Issue #2 resolution compatibility
    3. Add new enhanced features with sensible defaults
    4. Validate mathematical consistency of migrated parameters
    """
    warnings = []

    # Remove deprecated fields
    deprecated_fields = ['n_processes', 'hyper_trials', 'hyper_search', 'study_timeout']
    for field in deprecated_fields:
        if field in legacy_config:
            warnings.append(f"Deprecated field '{field}' removed during migration")
            del legacy_config[field]

    # Update bounds for Issue #2 compatibility
    if 'bounds' in legacy_config:
        old_bounds = legacy_config['bounds']
        if 'max' in old_bounds and len(old_bounds['max']) >= 6:
            # Check for problematic lambda bounds from Issue #2
            if old_bounds['max'][4] > 10.0 or old_bounds['max'][5] > 10.0:
                warnings.append("Updated lambda bounds for Issue #2 overshoot resolution")
                old_bounds['max'][4] = min(old_bounds['max'][4], 10.0)
                old_bounds['max'][5] = min(old_bounds['max'][5], 10.0)

    # Add enhanced features if missing
    if 'w_schedule' not in legacy_config:
        legacy_config['w_schedule'] = [0.9, 0.4]
        warnings.append("Added inertia weight scheduling for improved convergence")

    if 'velocity_clamp' not in legacy_config:
        legacy_config['velocity_clamp'] = [0.1, 0.2]
        warnings.append("Added velocity clamping for stability")

    # Validate migrated configuration
    migrated_config = PSOConfig(**legacy_config)
    validation_result = PSO_ConfigValidator.validate_hyperparameters(migrated_config)

    if not validation_result.is_valid:
        raise ConfigurationError(f"Migration failed validation: {validation_result.errors}")

    return migrated_config, warnings