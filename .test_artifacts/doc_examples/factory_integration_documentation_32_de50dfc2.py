# Example from: docs\factory_integration_documentation.md
# Index: 32
# Runnable: True
# Hash: de50dfc2

# Pre-create factory function (once)
   factory = create_pso_controller_factory(SMCType.CLASSICAL)

   # Use factory in PSO fitness function (many times)
   def fitness_function(gains):
       controller = factory(gains)  # Thread-safe, fast
       return evaluate_performance(controller)