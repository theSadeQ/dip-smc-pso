# Example from: docs\factory\factory_integration_user_guide.md
# Index: 25
# Runnable: False
# Hash: 28dcee11

# example-metadata:
# runnable: false

# Thread-safe controller creation
import threading

def thread_safe_creation():
    # Each thread creates its own controller instance
    controller = create_controller('classical_smc', gains=[...])
    return controller

# Multiple threads can safely call the factory
threads = [
    threading.Thread(target=thread_safe_creation)
    for _ in range(10)
]