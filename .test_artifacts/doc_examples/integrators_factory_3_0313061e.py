# Example from: docs\reference\simulation\integrators_factory.md
# Index: 3
# Runnable: True
# Hash: 0313061e

factory.register('my_method', MyCustomIntegrator)
integrator = factory.create('my_method', config)