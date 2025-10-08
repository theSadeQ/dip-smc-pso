# Example from: docs\benchmarks\controller_performance_benchmarks.md
# Index: 6
# Runnable: True
# Hash: 91739d01

import threading

def thread_safety_test(controller_class, gains, n_threads=4, n_ops_per_thread=100):
    errors = []

    def worker():
        try:
            controller = controller_class(gains=gains)
            state = np.zeros(6)
            for _ in range(n_ops_per_thread):
                _ = controller.compute_control(state)
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return {
        'total_threads': n_threads,
        'successful_threads': n_threads - len(errors),
        'failed_threads': len(errors),
        'success_rate': (n_threads - len(errors)) / n_threads,
        'errors': errors
    }