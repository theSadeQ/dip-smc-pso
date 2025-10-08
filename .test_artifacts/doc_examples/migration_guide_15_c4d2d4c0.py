# Example from: docs\factory\migration_guide.md
# Index: 15
# Runnable: True
# Hash: c4d2d4c0

# Pre-migration validation
pre_validation = validate_configuration_syntax(original_config)
if not pre_validation.success:
    raise ValueError(f"Original configuration invalid: {pre_validation.errors}")

# Post-migration validation
post_validation = validate_migrated_configuration(migrated_config)
if not post_validation.success:
    restore_from_backup(backup_file)
    raise ValueError("Migration validation failed - restored from backup")