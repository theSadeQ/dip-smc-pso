# Example from: docs\api\factory_system_api_reference.md
# Index: 26
# Runnable: True
# Hash: d994a32a

'mpc_controller': {
    'class': MPCController,  # None if cvxpy unavailable
    'config_class': MPCConfig,
    'default_gains': [],
    'gain_count': 0,
    'description': 'Model predictive controller',
    'supports_dynamics': True,
    'required_params': ['horizon', 'q_x', 'q_theta', 'r_u']
}