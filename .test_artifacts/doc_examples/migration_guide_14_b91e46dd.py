# Example from: docs\factory\migration_guide.md
# Index: 14
# Runnable: True
# Hash: b91e46dd

# Always backup before migration
backup_created = create_backup_before_migration(config_file)
assert backup_created, "Backup creation failed - aborting migration"