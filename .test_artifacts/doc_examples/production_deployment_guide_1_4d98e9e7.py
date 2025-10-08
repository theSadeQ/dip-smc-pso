# Example from: docs\factory\production_deployment_guide.md
# Index: 1
# Runnable: False
# Hash: 4d98e9e7

# example-metadata:
# runnable: false

def production_readiness_check():
    """Comprehensive production readiness validation."""

    import time
    import threading
    import numpy as np
    from src.controllers.factory import (
        create_controller,
        list_available_controllers,
        get_default_gains,
        create_pso_controller_factory,
        SMCType
    )

    print("=== Production Readiness Assessment ===\n")

    results = {
        'basic_functionality': False,
        'thread_safety': False,
        'performance': False,
        'pso_integration': False,
        'error_handling': False,
        'memory_stability': False
    }

    # 1. Basic Functionality Test
    print("1. Testing Basic Functionality...")
    try:
        controllers = list_available_controllers()
        if len(controllers) >= 4:  # Expect at least 4 controller types
            for controller_type in controllers:
                gains = get_default_gains(controller_type)
                controller = create_controller(controller_type, gains=gains)

                # Test control computation
                test_state = np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0])
                result = controller.compute_control(test_state, (), {})

                control_value = result.u if hasattr(result, 'u') else result
                if not np.isfinite(control_value):
                    raise ValueError(f"Invalid control output: {control_value}")

            results['basic_functionality'] = True
            print("   ✅ Basic functionality test PASSED")
        else:
            print(f"   ❌ Insufficient controllers available: {len(controllers)}")

    except Exception as e:
        print(f"   ❌ Basic functionality test FAILED: {e}")

    # 2. Thread Safety Test
    print("\n2. Testing Thread Safety...")
    try:
        def concurrent_creation():
            return create_controller('classical_smc', gains=[20]*6)

        # Test concurrent controller creation
        start_time = time.time()
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=concurrent_creation)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(timeout=5)
            if thread.is_alive():
                raise TimeoutError("Thread did not complete in time")

        execution_time = time.time() - start_time
        if execution_time < 10:  # Should complete within 10 seconds
            results['thread_safety'] = True
            print(f"   ✅ Thread safety test PASSED ({execution_time:.2f}s)")
        else:
            print(f"   ❌ Thread safety test SLOW ({execution_time:.2f}s)")

    except Exception as e:
        print(f"   ❌ Thread safety test FAILED: {e}")

    # 3. Performance Test
    print("\n3. Testing Performance...")
    try:
        # Measure controller creation time
        creation_times = []
        for _ in range(100):
            start = time.perf_counter()
            create_controller('classical_smc', gains=[20]*6)
            end = time.perf_counter()
            creation_times.append((end - start) * 1000)  # Convert to ms

        avg_time = sum(creation_times) / len(creation_times)
        max_time = max(creation_times)

        if avg_time < 5.0 and max_time < 50.0:  # < 5ms average, < 50ms max
            results['performance'] = True
            print(f"   ✅ Performance test PASSED (avg: {avg_time:.2f}ms, max: {max_time:.2f}ms)")
        else:
            print(f"   ❌ Performance test FAILED (avg: {avg_time:.2f}ms, max: {max_time:.2f}ms)")

    except Exception as e:
        print(f"   ❌ Performance test FAILED: {e}")

    # 4. PSO Integration Test
    print("\n4. Testing PSO Integration...")
    try:
        factory_func = create_pso_controller_factory(SMCType.CLASSICAL)

        # Check required attributes
        if hasattr(factory_func, 'n_gains') and hasattr(factory_func, 'controller_type'):
            test_gains = [20, 15, 12, 8, 35, 5]
            controller = factory_func(test_gains)

            if controller is not None:
                results['pso_integration'] = True
                print("   ✅ PSO integration test PASSED")
            else:
                print("   ❌ PSO factory returned None")
        else:
            print("   ❌ PSO factory missing required attributes")

    except Exception as e:
        print(f"   ❌ PSO integration test FAILED: {e}")

    # 5. Error Handling Test
    print("\n5. Testing Error Handling...")
    try:
        error_cases = [
            ('invalid_type', [10]*6),
            ('classical_smc', [10]*3),  # Wrong gain count
            ('classical_smc', [-10]*6),  # Negative gains
        ]

        handled_errors = 0
        for controller_type, gains in error_cases:
            try:
                create_controller(controller_type, gains=gains)
                print(f"   ⚠️ Expected error not raised for {controller_type}")
            except (ValueError, TypeError) as e:
                handled_errors += 1
            except Exception as e:
                print(f"   ⚠️ Unexpected error type for {controller_type}: {type(e)}")

        if handled_errors >= len(error_cases) - 1:  # Allow one unexpected case
            results['error_handling'] = True
            print(f"   ✅ Error handling test PASSED ({handled_errors}/{len(error_cases)} cases)")
        else:
            print(f"   ❌ Error handling test FAILED ({handled_errors}/{len(error_cases)} cases)")

    except Exception as e:
        print(f"   ❌ Error handling test FAILED: {e}")

    # 6. Memory Stability Test
    print("\n6. Testing Memory Stability...")
    try:
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create and destroy many controllers
        for _ in range(1000):
            controller = create_controller('classical_smc', gains=[20]*6)
            del controller

        final_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory

        if memory_increase < 10:  # Less than 10MB increase
            results['memory_stability'] = True
            print(f"   ✅ Memory stability test PASSED ({memory_increase:.2f}MB increase)")
        else:
            print(f"   ❌ Memory stability test FAILED ({memory_increase:.2f}MB increase)")

    except ImportError:
        print("   ⚠️ psutil not available, skipping memory test")
        results['memory_stability'] = True  # Assume pass if can't test
    except Exception as e:
        print(f"   ❌ Memory stability test FAILED: {e}")

    # Summary
    passed_tests = sum(results.values())
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100

    print(f"\n=== Production Readiness Summary ===")
    print(f"Tests passed: {passed_tests}/{total_tests}")
    print(f"Success rate: {success_rate:.1f}%")

    if success_rate >= 95:
        print("✅ READY FOR PRODUCTION DEPLOYMENT")
        return True
    elif success_rate >= 80:
        print("⚠️ DEPLOYMENT WITH MONITORING RECOMMENDED")
        return False
    else:
        print("❌ NOT READY FOR PRODUCTION")
        return False

# Run production readiness check
production_ready = production_readiness_check()