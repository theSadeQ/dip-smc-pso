# Example from: docs\factory_integration_documentation.md
# Index: 27
# Runnable: False
# Hash: 78cb49d4

# example-metadata:
# runnable: false

   # Priority order (highest to lowest):
   # 1. Explicit gains parameter
   # 2. Configuration object attributes
   # 3. YAML configuration file
   # 4. Registry defaults

   controller = create_controller(
       'classical_smc',
       gains=[10, 8, 15, 12, 50, 5],  # Highest priority
       config=config_object            # Lower priority
   )