# Example from: docs\configuration_integration_documentation.md
# Index: 20
# Runnable: True
# Hash: 4f3c64e1

# ✅ Good: Explicit priority handling
   gains = (
       explicit_gains or          # Priority 1
       config_gains or           # Priority 2
       registry_defaults         # Priority 3
   )