# Example from: docs\api\factory_system_api_reference.md
# Index: 51
# Runnable: True
# Hash: 27764fbf

try:
    controller = create_controller(123)  # Wrong type
except ValueError as e:
    print(e)
    # Output: "Controller type must be string, got <class 'int'>"