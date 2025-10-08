# Example from: docs\api\factory_system_api_reference.md
# Index: 14
# Runnable: True
# Hash: 0ed02881

from src.controllers.factory import list_available_controllers, create_controller

# Check availability before attempting creation
available = list_available_controllers()
print(f"Available controllers: {available}")

if 'mpc_controller' in available:
    mpc = create_controller('mpc_controller')
    print("MPC controller created successfully")
else:
    print("MPC not available (install cvxpy: pip install cvxpy)")