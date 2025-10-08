# Example from: docs\factory\production_deployment_guide.md
# Index: 6
# Runnable: True
# Hash: e7d750bc

class FactoryHealthChecker:
    """Production health checking for factory system."""

    def __init__(self):
        self.health_history = []

    def perform_health_check(self):
        """Comprehensive health check."""

        health_status = {
            'timestamp': time.time(),
            'overall_status': 'healthy',
            'checks': {}
        }

        # Basic functionality check
        health_status['checks']['basic_functionality'] = self.check_basic_functionality()

        # Performance check
        health_status['checks']['performance'] = self.check_performance()

        # Memory check
        health_status['checks']['memory'] = self.check_memory_usage()

        # Thread safety check
        health_status['checks']['thread_safety'] = self.check_thread_safety()

        # Error rate check
        health_status['checks']['error_rate'] = self.check_error_rate()

        # Determine overall status
        failed_checks = [name for name, status in health_status['checks'].items()
                        if not status.get('healthy', False)]

        if failed_checks:
            health_status['overall_status'] = 'degraded' if len(failed_checks) <= 2 else 'unhealthy'

        self.health_history.append(health_status)

        # Keep only recent history
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]

        return health_status

    def check_basic_functionality(self):
        """Check basic factory functionality."""

        try:
            from src.controllers.factory import create_controller, list_available_controllers

            controllers = list_available_controllers()
            if len(controllers) < 4:
                return {'healthy': False, 'reason': 'Insufficient controllers available'}

            # Test one controller creation
            controller = create_controller('classical_smc', gains=[20]*6)
            test_state = np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0])
            result = controller.compute_control(test_state, (), {})

            control_value = result.u if hasattr(result, 'u') else result
            if not np.isfinite(control_value):
                return {'healthy': False, 'reason': 'Invalid control output'}

            return {'healthy': True, 'controllers_available': len(controllers)}

        except Exception as e:
            return {'healthy': False, 'reason': str(e)}

    def check_performance(self):
        """Check factory performance."""

        try:
            import time
            from src.controllers.factory import create_controller

            # Measure creation time
            times = []
            for _ in range(10):
                start = time.perf_counter()
                create_controller('classical_smc', gains=[20]*6)
                times.append((time.perf_counter() - start) * 1000)

            avg_time = sum(times) / len(times)
            max_time = max(times)

            if avg_time > 10 or max_time > 50:  # ms
                return {
                    'healthy': False,
                    'reason': f'Slow performance: avg={avg_time:.2f}ms, max={max_time:.2f}ms'
                }

            return {
                'healthy': True,
                'avg_creation_time_ms': avg_time,
                'max_creation_time_ms': max_time
            }

        except Exception as e:
            return {'healthy': False, 'reason': str(e)}

    def check_memory_usage(self):
        """Check memory usage."""

        try:
            import psutil
            import os

            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024

            if memory_mb > 1000:  # 1GB threshold
                return {
                    'healthy': False,
                    'reason': f'High memory usage: {memory_mb:.2f}MB'
                }

            return {
                'healthy': True,
                'memory_usage_mb': memory_mb
            }

        except ImportError:
            return {'healthy': True, 'reason': 'psutil not available'}
        except Exception as e:
            return {'healthy': False, 'reason': str(e)}

    def check_thread_safety(self):
        """Check thread safety."""

        try:
            import threading
            import time
            from src.controllers.factory import create_controller

            def create_controller_thread():
                create_controller('classical_smc', gains=[20]*6)

            start_time = time.time()
            threads = []

            for _ in range(5):
                thread = threading.Thread(target=create_controller_thread)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join(timeout=5)
                if thread.is_alive():
                    return {'healthy': False, 'reason': 'Thread timeout detected'}

            execution_time = time.time() - start_time
            if execution_time > 10:
                return {
                    'healthy': False,
                    'reason': f'Slow thread execution: {execution_time:.2f}s'
                }

            return {
                'healthy': True,
                'thread_execution_time_s': execution_time
            }

        except Exception as e:
            return {'healthy': False, 'reason': str(e)}

    def check_error_rate(self):
        """Check recent error rate."""

        try:
            # Get recent health checks
            recent_checks = self.health_history[-10:] if len(self.health_history) >= 10 else self.health_history

            if not recent_checks:
                return {'healthy': True, 'reason': 'No history available'}

            failed_checks = sum(1 for check in recent_checks
                              if check['overall_status'] != 'healthy')

            error_rate = failed_checks / len(recent_checks)

            if error_rate > 0.2:  # 20% error rate
                return {
                    'healthy': False,
                    'reason': f'High error rate: {error_rate:.1%}'
                }

            return {
                'healthy': True,
                'error_rate': error_rate,
                'sample_size': len(recent_checks)
            }

        except Exception as e:
            return {'healthy': False, 'reason': str(e)}

# Setup health checker
health_checker = FactoryHealthChecker()

# Health check endpoint (for load balancer)
def health_check_endpoint():
    """Health check endpoint for load balancers."""

    health_status = health_checker.perform_health_check()

    if health_status['overall_status'] == 'healthy':
        return {'status': 'ok', 'timestamp': health_status['timestamp']}, 200
    elif health_status['overall_status'] == 'degraded':
        return {'status': 'degraded', 'details': health_status['checks']}, 200
    else:
        return {'status': 'unhealthy', 'details': health_status['checks']}, 503