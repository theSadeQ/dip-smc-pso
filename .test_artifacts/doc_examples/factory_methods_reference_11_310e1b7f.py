# Example from: docs\api\factory_methods_reference.md
# Index: 11
# Runnable: True
# Hash: 310e1b7f

all_controllers = list_all_controllers()
available = list_available_controllers()

unavailable = set(all_controllers) - set(available)
if unavailable:
    print(f"Unavailable controllers: {unavailable}")
    print("Check dependencies and installation")