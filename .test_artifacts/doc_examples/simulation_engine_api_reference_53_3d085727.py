# Example from: docs\api\simulation_engine_api_reference.md
# Index: 53
# Runnable: True
# Hash: 3d085727

info = IntegratorFactory.get_integrator_info('rk4')
# Returns:
# {
#     'class_name': 'RungeKutta4',
#     'module': 'src.simulation.integrators.fixed_step.runge_kutta',
#     'order': 4,
#     'adaptive': False,
#     'description': 'Classic 4th-order Runge-Kutta method'
# }