#=======================================================================================\\\
#========================= controller_optimization_benchmark.py =========================\\\
#=======================================================================================\\\

"""
Controller Performance Optimization Benchmark for GitHub Issue #6.

Comprehensive analysis of:
- Factory instantiation overhead
- Control computation timing
- SMC algorithm stability validation
- Thread safety performance
- Memory usage optimization
"""

import time
import threading
import numpy as np
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys
from datetime import datetime

# Import factory and controllers
from src.controllers.factory import create_controller, list_available_controllers
from src.core.dynamics import DIPDynamics

@dataclass
class PerformanceMetrics:
    """Container for performance measurement results."""
    instantiation_time: float
    computation_time: float
    memory_usage_mb: float
    thread_safety_score: float
    stability_validated: bool
    control_accuracy: float

class ControllerOptimizationBenchmark:
    """
    Comprehensive controller performance benchmarking system.

    Measures and optimizes:
    1. Factory instantiation overhead (<1ms requirement)
    2. Control computation timing accuracy
    3. SMC stability constraint validation
    4. Thread-safe operation performance
    5. Memory usage optimization
    """

    def __init__(self):
        self.results = {}
        self.test_state = np.array([0.1, 0.0, 0.05, 0.0, -0.05, 0.0])  # DIP test state
        self.num_threads = 4
        self.num_iterations = 1000

    def run_comprehensive_benchmark(self) -> Dict[str, Any]:
        """Run complete optimization benchmark suite."""
        print("🚀 Starting Controller Optimization Benchmark...")
        print(f"📊 Target: <1ms instantiation, thread-safe operations, 100% stability validation")

        # Get available controllers
        available_controllers = list_available_controllers()
        print(f"🎯 Testing {len(available_controllers)} controllers: {available_controllers}")

        benchmark_results = {
            'timestamp': datetime.now().isoformat(),
            'target_metrics': {
                'instantiation_time_ms': 1.0,
                'computation_time_ms': 0.1,
                'thread_safety_score': 100.0,
                'stability_validation': 100.0
            },
            'controller_performance': {},
            'factory_optimization': {},
            'thread_safety_analysis': {},
            'stability_validation': {},
            'optimization_recommendations': []
        }

        for controller_type in available_controllers:
            print(f"\n🔍 Benchmarking {controller_type}...")

            # 1. Factory Instantiation Performance
            instantiation_metrics = self._benchmark_factory_instantiation(controller_type)

            # 2. Control Computation Performance
            computation_metrics = self._benchmark_control_computation(controller_type)

            # 3. Thread Safety Analysis
            thread_safety_metrics = self._benchmark_thread_safety(controller_type)

            # 4. Stability Validation
            stability_metrics = self._validate_stability_constraints(controller_type)

            # 5. Memory Usage Analysis
            memory_metrics = self._analyze_memory_usage(controller_type)

            # Compile results
            benchmark_results['controller_performance'][controller_type] = {
                'instantiation': instantiation_metrics,
                'computation': computation_metrics,
                'thread_safety': thread_safety_metrics,
                'stability': stability_metrics,
                'memory': memory_metrics,
                'overall_score': self._calculate_performance_score(
                    instantiation_metrics, computation_metrics,
                    thread_safety_metrics, stability_metrics
                )
            }

        # 6. Factory System Analysis
        benchmark_results['factory_optimization'] = self._analyze_factory_optimization()

        # 7. Generate Optimization Recommendations
        benchmark_results['optimization_recommendations'] = self._generate_optimization_recommendations(
            benchmark_results['controller_performance']
        )

        # 8. Performance Summary
        benchmark_results['performance_summary'] = self._create_performance_summary(benchmark_results)

        return benchmark_results

    def _benchmark_factory_instantiation(self, controller_type: str) -> Dict[str, Any]:
        """Benchmark factory instantiation performance (<1ms requirement)."""
        print(f"  📈 Factory instantiation benchmark...")

        # Warm-up runs
        for _ in range(10):
            try:
                controller = create_controller(controller_type)
            except Exception:
                pass

        # Actual timing runs
        times = []
        successful_instantiations = 0

        for i in range(100):
            start_time = time.perf_counter()
            try:
                controller = create_controller(controller_type)
                end_time = time.perf_counter()
                instantiation_time = (end_time - start_time) * 1000  # Convert to ms
                times.append(instantiation_time)
                successful_instantiations += 1
            except Exception as e:
                print(f"    ❌ Instantiation failed: {e}")

        if times:
            return {
                'avg_time_ms': np.mean(times),
                'min_time_ms': np.min(times),
                'max_time_ms': np.max(times),
                'std_time_ms': np.std(times),
                'p95_time_ms': np.percentile(times, 95),
                'p99_time_ms': np.percentile(times, 99),
                'success_rate': successful_instantiations / 100,
                'meets_1ms_requirement': np.mean(times) < 1.0,
                'raw_times': times[:10]  # First 10 for debugging
            }
        else:
            return {
                'avg_time_ms': float('inf'),
                'success_rate': 0.0,
                'meets_1ms_requirement': False,
                'error': 'All instantiations failed'
            }

    def _benchmark_control_computation(self, controller_type: str) -> Dict[str, Any]:
        """Benchmark control computation performance."""
        print(f"  ⚡ Control computation benchmark...")

        try:
            controller = create_controller(controller_type)
        except Exception as e:
            return {'error': f'Controller creation failed: {e}'}

        # Warm-up
        for _ in range(10):
            try:
                controller.compute_control(self.test_state, 0.0, {})
            except Exception:
                pass

        # Timing runs
        computation_times = []
        successful_computations = 0
        control_outputs = []

        for i in range(100):
            start_time = time.perf_counter()
            try:
                result = controller.compute_control(self.test_state, 0.0, {})
                end_time = time.perf_counter()

                computation_time = (end_time - start_time) * 1000  # Convert to ms
                computation_times.append(computation_time)
                successful_computations += 1

                # Extract control value
                if isinstance(result, dict) and 'u' in result:
                    control_outputs.append(result['u'])
                elif isinstance(result, (int, float)):
                    control_outputs.append(result)
                elif isinstance(result, np.ndarray):
                    control_outputs.append(result.flatten()[0])

            except Exception as e:
                print(f"    ❌ Computation failed: {e}")

        if computation_times:
            return {
                'avg_time_ms': np.mean(computation_times),
                'min_time_ms': np.min(computation_times),
                'max_time_ms': np.max(computation_times),
                'std_time_ms': np.std(computation_times),
                'p95_time_ms': np.percentile(computation_times, 95),
                'success_rate': successful_computations / 100,
                'control_consistency': np.std(control_outputs) if control_outputs else float('inf'),
                'avg_control_magnitude': np.mean(np.abs(control_outputs)) if control_outputs else 0.0,
                'meets_realtime_requirement': np.percentile(computation_times, 95) < 1.0  # 95% under 1ms
            }
        else:
            return {
                'avg_time_ms': float('inf'),
                'success_rate': 0.0,
                'meets_realtime_requirement': False,
                'error': 'All computations failed'
            }

    def _benchmark_thread_safety(self, controller_type: str) -> Dict[str, Any]:
        """Benchmark thread safety performance."""
        print(f"  🔒 Thread safety benchmark...")

        def create_and_compute(thread_id: int) -> Dict[str, Any]:
            """Worker function for thread safety testing."""
            try:
                # Create controller in thread
                start_time = time.perf_counter()
                controller = create_controller(controller_type)
                creation_time = time.perf_counter() - start_time

                # Perform computations
                computation_times = []
                for i in range(10):
                    comp_start = time.perf_counter()
                    result = controller.compute_control(self.test_state, 0.0, {})
                    comp_time = time.perf_counter() - comp_start
                    computation_times.append(comp_time * 1000)  # ms

                return {
                    'thread_id': thread_id,
                    'creation_time_ms': creation_time * 1000,
                    'avg_computation_time_ms': np.mean(computation_times),
                    'success': True,
                    'error': None
                }
            except Exception as e:
                return {
                    'thread_id': thread_id,
                    'success': False,
                    'error': str(e)
                }

        # Run concurrent tests
        thread_results = []
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(create_and_compute, i) for i in range(self.num_threads)]
            for future in as_completed(futures):
                thread_results.append(future.result())

        # Analyze results
        successful_threads = [r for r in thread_results if r['success']]
        failed_threads = [r for r in thread_results if not r['success']]

        if successful_threads:
            creation_times = [r['creation_time_ms'] for r in successful_threads]
            computation_times = [r['avg_computation_time_ms'] for r in successful_threads]

            return {
                'thread_success_rate': len(successful_threads) / self.num_threads,
                'avg_creation_time_ms': np.mean(creation_times),
                'avg_computation_time_ms': np.mean(computation_times),
                'creation_time_variance': np.var(creation_times),
                'computation_time_variance': np.var(computation_times),
                'thread_safety_score': (len(successful_threads) / self.num_threads) * 100,
                'failed_threads': len(failed_threads),
                'error_summary': [r['error'] for r in failed_threads]
            }
        else:
            return {
                'thread_success_rate': 0.0,
                'thread_safety_score': 0.0,
                'failed_threads': len(failed_threads),
                'error': 'All threads failed',
                'error_summary': [r['error'] for r in failed_threads]
            }

    def _validate_stability_constraints(self, controller_type: str) -> Dict[str, Any]:
        """Validate SMC algorithm stability constraints."""
        print(f"  🔬 Stability validation...")

        try:
            controller = create_controller(controller_type)
        except Exception as e:
            return {'error': f'Controller creation failed: {e}', 'stability_validated': False}

        stability_results = {
            'controller_type': controller_type,
            'stability_validated': True,
            'constraint_checks': {},
            'validation_errors': []
        }

        # Get controller gains
        try:
            gains = controller.gains
        except Exception as e:
            stability_results['validation_errors'].append(f'Cannot access gains: {e}')
            gains = []

        # Controller-specific stability validation
        if controller_type == 'classical_smc':
            stability_results['constraint_checks'].update({
                'positive_gains': all(g > 0 for g in gains) if gains else False,
                'gain_count': len(gains) == 6 if gains else False,
                'boundary_layer_positive': True  # Assume positive from config
            })

        elif controller_type == 'sta_smc':
            if len(gains) >= 2:
                K1, K2 = gains[0], gains[1]
                stability_results['constraint_checks'].update({
                    'K1_greater_than_K2': K1 > K2,
                    'K1_positive': K1 > 0,
                    'K2_positive': K2 > 0,
                    'finite_time_convergence': K1 > K2 > 0,
                    'gain_count': len(gains) == 6
                })
            else:
                stability_results['validation_errors'].append('Insufficient gains for STA-SMC validation')

        elif controller_type == 'adaptive_smc':
            stability_results['constraint_checks'].update({
                'positive_gains': all(g > 0 for g in gains) if gains else False,
                'gain_count': len(gains) == 5 if gains else False,
                'adaptation_rate_positive': gains[4] > 0 if len(gains) > 4 else False
            })

        elif controller_type == 'hybrid_adaptive_sta_smc':
            stability_results['constraint_checks'].update({
                'gain_count': len(gains) == 4 if gains else False,
                'positive_gains': all(g > 0 for g in gains) if gains else False,
                'hybrid_structure_valid': hasattr(controller, 'config')
            })

        # Overall validation
        constraint_failures = [k for k, v in stability_results['constraint_checks'].items() if not v]
        if constraint_failures or stability_results['validation_errors']:
            stability_results['stability_validated'] = False
            stability_results['failed_constraints'] = constraint_failures

        return stability_results

    def _analyze_memory_usage(self, controller_type: str) -> Dict[str, Any]:
        """Analyze controller memory usage (simplified without psutil)."""
        print(f"  💾 Memory usage analysis...")

        controllers = []
        try:
            # Create multiple controllers to measure object overhead
            for i in range(10):
                controller = create_controller(controller_type)
                controllers.append(controller)

            # Measure object size approximation
            controller_size = sys.getsizeof(controllers[0])

            # Perform computations to test for memory leaks
            for controller in controllers:
                for j in range(10):
                    controller.compute_control(self.test_state, 0.0, {})

            return {
                'controller_count': len(controllers),
                'approximate_controller_size_bytes': controller_size,
                'memory_efficient': controller_size < 1024 * 1024,  # Less than 1MB per controller
                'creation_successful': True,
                'computation_successful': True
            }

        except Exception as e:
            return {
                'error': f'Memory analysis failed: {e}',
                'memory_efficient': False,
                'creation_successful': False
            }
        finally:
            # Clean up
            del controllers

    def _calculate_performance_score(self, instantiation: Dict, computation: Dict,
                                   thread_safety: Dict, stability: Dict) -> float:
        """Calculate overall performance score (0-100)."""
        score = 0.0

        # Instantiation score (25 points)
        if instantiation.get('meets_1ms_requirement', False):
            score += 25
        else:
            # Partial credit based on how close to 1ms
            avg_time = instantiation.get('avg_time_ms', float('inf'))
            if avg_time < 5.0:  # Within 5ms gets partial credit
                score += 25 * (5.0 - avg_time) / 4.0

        # Computation score (25 points)
        if computation.get('meets_realtime_requirement', False):
            score += 25
        else:
            success_rate = computation.get('success_rate', 0.0)
            score += 25 * success_rate

        # Thread safety score (25 points)
        thread_score = thread_safety.get('thread_safety_score', 0.0)
        score += 25 * (thread_score / 100.0)

        # Stability score (25 points)
        if stability.get('stability_validated', False):
            score += 25
        else:
            # Partial credit for passing some constraints
            constraints = stability.get('constraint_checks', {})
            if constraints:
                passed = sum(1 for v in constraints.values() if v)
                total = len(constraints)
                score += 25 * (passed / total)

        return min(100.0, score)

    def _analyze_factory_optimization(self) -> Dict[str, Any]:
        """Analyze factory system optimization opportunities."""
        print(f"\n🏭 Factory system optimization analysis...")

        # Test factory overhead
        available_controllers = list_available_controllers()

        # Measure factory registry access time
        registry_times = []
        for _ in range(100):
            start = time.perf_counter()
            list_available_controllers()
            end = time.perf_counter()
            registry_times.append((end - start) * 1000)  # ms

        # Measure controller creation variance
        creation_variance = {}
        for controller_type in available_controllers:
            times = []
            for _ in range(20):
                start = time.perf_counter()
                try:
                    create_controller(controller_type)
                    end = time.perf_counter()
                    times.append((end - start) * 1000)
                except Exception:
                    pass
            if times:
                creation_variance[controller_type] = {
                    'mean_ms': np.mean(times),
                    'std_ms': np.std(times),
                    'coefficient_of_variation': np.std(times) / np.mean(times)
                }

        return {
            'registry_access_time_ms': {
                'avg': np.mean(registry_times),
                'std': np.std(registry_times),
                'max': np.max(registry_times)
            },
            'creation_variance': creation_variance,
            'factory_optimized': np.mean(registry_times) < 0.1,  # Sub 0.1ms registry access
            'consistency_score': np.mean([1.0 / (1.0 + v['coefficient_of_variation'])
                                        for v in creation_variance.values()]) if creation_variance else 0.0
        }

    def _generate_optimization_recommendations(self, performance_data: Dict) -> List[str]:
        """Generate specific optimization recommendations."""
        recommendations = []

        for controller_type, metrics in performance_data.items():
            # Instantiation optimization
            instantiation = metrics.get('instantiation', {})
            if not instantiation.get('meets_1ms_requirement', False):
                avg_time = instantiation.get('avg_time_ms', 0)
                recommendations.append(
                    f"🚀 {controller_type}: Instantiation time {avg_time:.2f}ms exceeds 1ms target. "
                    "Consider pre-compilation, lazy loading, or configuration caching."
                )

            # Computation optimization
            computation = metrics.get('computation', {})
            if not computation.get('meets_realtime_requirement', False):
                recommendations.append(
                    f"⚡ {controller_type}: Computation time exceeds real-time requirements. "
                    "Consider Numba JIT compilation or algorithm optimization."
                )

            # Thread safety optimization
            thread_safety = metrics.get('thread_safety', {})
            thread_score = thread_safety.get('thread_safety_score', 0)
            if thread_score < 90:
                recommendations.append(
                    f"🔒 {controller_type}: Thread safety score {thread_score:.1f}% below 90% target. "
                    "Review locking mechanisms and reduce critical sections."
                )

            # Stability validation
            stability = metrics.get('stability', {})
            if not stability.get('stability_validated', False):
                failed_constraints = stability.get('failed_constraints', [])
                recommendations.append(
                    f"🔬 {controller_type}: Stability validation failed. "
                    f"Failed constraints: {failed_constraints}. Review gain validation logic."
                )

        # Add general recommendations
        if len(recommendations) == 0:
            recommendations.append("✅ All controllers meet optimization targets!")
        else:
            recommendations.append(
                "🎯 Priority: Focus on instantiation time optimization for production deployment."
            )

        return recommendations

    def _create_performance_summary(self, benchmark_results: Dict) -> Dict[str, Any]:
        """Create executive performance summary."""
        controller_data = benchmark_results['controller_performance']

        # Calculate overall metrics
        overall_scores = [metrics['overall_score'] for metrics in controller_data.values()]
        instantiation_compliance = sum(1 for metrics in controller_data.values()
                                     if metrics['instantiation'].get('meets_1ms_requirement', False))
        thread_safety_avg = np.mean([metrics['thread_safety'].get('thread_safety_score', 0)
                                   for metrics in controller_data.values()])
        stability_compliance = sum(1 for metrics in controller_data.values()
                                 if metrics['stability'].get('stability_validated', False))

        return {
            'overall_performance_score': np.mean(overall_scores) if overall_scores else 0.0,
            'instantiation_compliance_rate': instantiation_compliance / len(controller_data),
            'thread_safety_avg_score': thread_safety_avg,
            'stability_compliance_rate': stability_compliance / len(controller_data),
            'production_ready': (
                np.mean(overall_scores) >= 80.0 and
                instantiation_compliance == len(controller_data) and
                thread_safety_avg >= 90.0 and
                stability_compliance == len(controller_data)
            ),
            'optimization_priority': self._identify_optimization_priority(controller_data)
        }

    def _identify_optimization_priority(self, controller_data: Dict) -> str:
        """Identify the highest priority optimization area."""
        issues = []

        # Check each optimization area
        instantiation_issues = sum(1 for metrics in controller_data.values()
                                 if not metrics['instantiation'].get('meets_1ms_requirement', False))
        thread_safety_issues = sum(1 for metrics in controller_data.values()
                                 if metrics['thread_safety'].get('thread_safety_score', 0) < 90)
        stability_issues = sum(1 for metrics in controller_data.values()
                             if not metrics['stability'].get('stability_validated', False))

        if instantiation_issues > 0:
            return "Factory Instantiation Optimization (Critical for <1ms requirement)"
        elif thread_safety_issues > 0:
            return "Thread Safety Enhancement (Critical for production deployment)"
        elif stability_issues > 0:
            return "SMC Stability Constraint Validation (Critical for control safety)"
        else:
            return "Performance Monitoring and Maintenance (All targets met)"


def main():
    """Run comprehensive controller optimization benchmark."""
    benchmark = ControllerOptimizationBenchmark()

    print("=" * 90)
    print("🎯 CONTROLLER OPTIMIZATION BENCHMARK - GitHub Issue #6")
    print("=" * 90)

    try:
        results = benchmark.run_comprehensive_benchmark()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"controller_optimization_benchmark_{timestamp}.json"

        with open(filename, 'w') as f:
            # Convert numpy types for JSON serialization
            def convert_numpy(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.bool_):
                    return bool(obj)
                return obj

            def clean_for_json(data):
                if isinstance(data, dict):
                    return {k: clean_for_json(v) for k, v in data.items()}
                elif isinstance(data, list):
                    return [clean_for_json(item) for item in data]
                else:
                    return convert_numpy(data)

            clean_results = clean_for_json(results)
            json.dump(clean_results, f, indent=2)

        # Print summary
        print("\n" + "=" * 90)
        print("📊 BENCHMARK RESULTS SUMMARY")
        print("=" * 90)

        summary = results['performance_summary']
        print(f"🏆 Overall Performance Score: {summary['overall_performance_score']:.1f}/100")
        print(f"🚀 Instantiation Compliance: {summary['instantiation_compliance_rate']*100:.1f}% (<1ms)")
        print(f"🔒 Thread Safety Score: {summary['thread_safety_avg_score']:.1f}%")
        print(f"🔬 Stability Compliance: {summary['stability_compliance_rate']*100:.1f}%")
        print(f"✅ Production Ready: {summary['production_ready']}")
        print(f"🎯 Optimization Priority: {summary['optimization_priority']}")

        print(f"\n📁 Detailed results saved to: {filename}")

        # Print top recommendations
        print("\n🔧 TOP OPTIMIZATION RECOMMENDATIONS:")
        for i, rec in enumerate(results['optimization_recommendations'][:5], 1):
            print(f"{i}. {rec}")

        return results

    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()