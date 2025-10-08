# Example from: docs\factory\deprecation_management.md
# Index: 11
# Runnable: False
# Hash: 9329e7e9

# example-metadata:
# runnable: false

   # Safe for automatic migration
   simple_rename = DeprecationMapping(
       old_name='old_name',
       new_name='new_name',
       auto_migrate=True
   )

   # Requires manual migration
   complex_change = DeprecationMapping(
       old_name='complex_param',
       new_name='restructured_config',
       auto_migrate=False,  # Semantic change requires manual intervention
       migration_guide="See migration guide at docs/migration/v3.0.md"
   )