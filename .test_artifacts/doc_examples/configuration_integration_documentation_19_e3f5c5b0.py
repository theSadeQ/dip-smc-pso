# Example from: docs\configuration_integration_documentation.md
# Index: 19
# Runnable: True
# Hash: e3f5c5b0

# ✅ Good: Multi-level validation
   def validate_config(config):
       # 1. Type validation
       assert isinstance(config.gains, list)
       # 2. Domain validation
       assert all(g > 0 for g in config.gains)
       # 3. Physics validation
       assert config.max_force > max(config.gains)