# Example from: docs\factory\troubleshooting_guide.md
# Index: 9
# Runnable: True
# Hash: d8010fde

import threading
import time
from src.controllers.factory import create_controller

def diagnose_thread_safety_issues():
    print("Diagnosing thread safety issues")

    def blocking_operation():
        # Simulate long-running operation
        controller = create_controller('classical_smc', gains=[10]*6)
        time.sleep(5)  # Simulate work
        return controller

    # Test concurrent access
    start_time = time.time()
    threads = []

    for i in range(5):
        thread = threading.Thread(target=blocking_operation)
        threads.append(thread)
        thread.start()
        time.sleep(0.1)  # Stagger starts

    for thread in threads:
        thread.join(timeout=15)
        if thread.is_alive():
            print(f"✗ Thread still running after timeout")
        else:
            print(f"✓ Thread completed successfully")

    total_time = time.time() - start_time
    print(f"Total execution time: {total_time:.2f} seconds")

    if total_time > 30:
        print("⚠ Possible deadlock or contention detected")
    else:
        print("✓ Thread safety test completed normally")

# Run diagnostic
diagnose_thread_safety_issues()