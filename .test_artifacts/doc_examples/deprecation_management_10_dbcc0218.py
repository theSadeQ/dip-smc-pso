# Example from: docs\factory\deprecation_management.md
# Index: 10
# Runnable: True
# Hash: dbcc0218

# Good deprecation message
   message = (
       "'old_param' is deprecated and will be removed in v3.0.0. "
       "Use 'new_param' instead. Migration: Replace 'old_param: value' "
       "with 'new_param: value' in your configuration."
   )

   # Poor deprecation message
   message = "'old_param' is deprecated."  # No guidance!