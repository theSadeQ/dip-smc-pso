#======================================================================================\\\
#========================= controller_performance_analysis.py =========================\\\
#======================================================================================\\\

"""
Controller Performance Analysis for GitHub Issue #6.

Analyzes:
- Factory instantiation performance
- Control computation timing
- SMC algorithm stability
- Thread safety assessment
"""

import time
import threading
import numpy as np
import json
from typing import Dict, List, Any
from datetime import datetime

# Import factory and controllers
from src.controllers.factory import create_controller, list_available_controllers

class ControllerPerformanceAnalyzer:
    """Controller performance analysis and optimization system."""

    def __init__(self):
        self.test_state = np.array([0.1, 0.0, 0.05, 0.0, -0.05, 0.0])  # DIP test state
        self.results = {}

    def run_analysis(self) -> Dict[str, Any]:
        """Run comprehensive controller performance analysis."""
        print("CONTROLLER PERFORMANCE ANALYSIS - GitHub Issue #6")
        print("=" * 70)

        # Get available controllers
        available_controllers = list_available_controllers()
        print(f"Testing {len(available_controllers)} controllers: {available_controllers}")

        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'controllers_analyzed': available_controllers,
            'performance_metrics': {},
            'optimization_recommendations': [],
            'summary': {}
        }

        for controller_type in available_controllers:
            print(f"\nAnalyzing {controller_type}...")

            # Run performance tests
            controller_metrics = {
                'instantiation': self._test_instantiation_performance(controller_type),
                'computation': self._test_computation_performance(controller_type),
                'stability': self._validate_stability(controller_type),
                'thread_safety': self._test_thread_safety(controller_type)
            }

            # Calculate overall score
            controller_metrics['overall_score'] = self._calculate_score(controller_metrics)

            analysis_results['performance_metrics'][controller_type] = controller_metrics

        # Generate recommendations and summary
        analysis_results['optimization_recommendations'] = self._generate_recommendations(
            analysis_results['performance_metrics']
        )
        analysis_results['summary'] = self._create_summary(analysis_results['performance_metrics'])

        return analysis_results

    def _test_instantiation_performance(self, controller_type: str) -> Dict[str, Any]:
        """Test factory instantiation performance."""
        print(f"  Testing instantiation performance...")

        # Warm-up
        for _ in range(5):
            try:
                create_controller(controller_type)
            except:
                pass

        # Actual timing
        times = []
        successes = 0

        for _ in range(50):
            start = time.perf_counter()
            try:
                controller = create_controller(controller_type)
                end = time.perf_counter()
                times.append((end - start) * 1000)  # Convert to ms
                successes += 1
            except Exception as e:
                print(f"    Instantiation failed: {e}")

        if times:
            return {
                'avg_time_ms': np.mean(times),
                'min_time_ms': np.min(times),
                'max_time_ms': np.max(times),
                'p95_time_ms': np.percentile(times, 95),
                'success_rate': successes / 50,
                'meets_1ms_target': np.mean(times) < 1.0,
                'sample_times': times[:5]
            }
        else:
            return {
                'avg_time_ms': float('inf'),
                'success_rate': 0.0,
                'meets_1ms_target': False,
                'error': 'All instantiations failed'
            }

    def _test_computation_performance(self, controller_type: str) -> Dict[str, Any]:
        """Test control computation performance."""
        print(f"  Testing computation performance...")

        try:
            controller = create_controller(controller_type)
        except Exception as e:
            return {'error': f'Controller creation failed: {e}'}

        # Warm-up
        for _ in range(5):
            try:
                controller.compute_control(self.test_state, 0.0, {})
            except:
                pass

        # Timing tests
        times = []
        outputs = []
        successes = 0

        for _ in range(50):
            start = time.perf_counter()
            try:
                result = controller.compute_control(self.test_state, 0.0, {})
                end = time.perf_counter()

                times.append((end - start) * 1000)  # ms
                successes += 1

                # Extract control value
                if isinstance(result, dict) and 'u' in result:
                    outputs.append(result['u'])
                elif isinstance(result, (int, float)):
                    outputs.append(result)
                elif isinstance(result, np.ndarray):
                    outputs.append(result.flatten()[0])

            except Exception as e:
                print(f"    Computation failed: {e}")

        if times:
            return {
                'avg_time_ms': np.mean(times),
                'min_time_ms': np.min(times),
                'max_time_ms': np.max(times),
                'p95_time_ms': np.percentile(times, 95),
                'success_rate': successes / 50,
                'meets_realtime_target': np.percentile(times, 95) < 1.0,
                'control_consistency': np.std(outputs) if outputs else float('inf'),
                'avg_control_magnitude': np.mean(np.abs(outputs)) if outputs else 0.0
            }
        else:
            return {
                'avg_time_ms': float('inf'),
                'success_rate': 0.0,
                'meets_realtime_target': False,
                'error': 'All computations failed'
            }

    def _validate_stability(self, controller_type: str) -> Dict[str, Any]:
        """Validate SMC stability constraints."""
        print(f"  Validating stability constraints...")

        try:
            controller = create_controller(controller_type)
        except Exception as e:
            return {'error': f'Controller creation failed: {e}', 'validated': False}

        try:
            gains = controller.gains
        except Exception as e:
            return {'error': f'Cannot access gains: {e}', 'validated': False}

        validation_results = {
            'controller_type': controller_type,
            'gains': gains,
            'constraints_passed': {},
            'validated': True
        }

        # Controller-specific validation
        if controller_type == 'classical_smc':
            validation_results['constraints_passed'] = {
                'positive_gains': all(g > 0 for g in gains),
                'correct_gain_count': len(gains) == 6
            }

        elif controller_type == 'sta_smc':
            if len(gains) >= 2:
                K1, K2 = gains[0], gains[1]
                validation_results['constraints_passed'] = {
                    'K1_greater_than_K2': K1 > K2,
                    'K1_positive': K1 > 0,
                    'K2_positive': K2 > 0,
                    'correct_gain_count': len(gains) == 6
                }
            else:
                validation_results['validated'] = False
                validation_results['error'] = 'Insufficient gains'

        elif controller_type == 'adaptive_smc':
            validation_results['constraints_passed'] = {
                'positive_gains': all(g > 0 for g in gains),
                'correct_gain_count': len(gains) == 5,
                'adaptation_rate_positive': gains[4] > 0 if len(gains) > 4 else False
            }

        elif controller_type == 'hybrid_adaptive_sta_smc':
            validation_results['constraints_passed'] = {
                'correct_gain_count': len(gains) == 4,
                'positive_gains': all(g > 0 for g in gains)
            }

        # Check if any constraints failed
        failed_constraints = [k for k, v in validation_results['constraints_passed'].items() if not v]
        if failed_constraints:
            validation_results['validated'] = False
            validation_results['failed_constraints'] = failed_constraints

        return validation_results

    def _test_thread_safety(self, controller_type: str) -> Dict[str, Any]:
        """Test thread safety of controller creation and operation."""
        print(f"  Testing thread safety...")

        def worker_function(thread_id):
            try:
                # Create controller
                controller = create_controller(controller_type)

                # Perform computations
                for _ in range(5):
                    result = controller.compute_control(self.test_state, 0.0, {})

                return {'thread_id': thread_id, 'success': True, 'error': None}
            except Exception as e:
                return {'thread_id': thread_id, 'success': False, 'error': str(e)}

        # Run concurrent tests
        threads = []
        results = []

        def run_worker(thread_id):
            result = worker_function(thread_id)
            results.append(result)

        # Create and start threads
        for i in range(4):
            thread = threading.Thread(target=run_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Analyze results
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]

        return {
            'total_threads': len(results),
            'successful_threads': len(successful),
            'failed_threads': len(failed),
            'success_rate': len(successful) / len(results) if results else 0.0,
            'thread_safe': len(failed) == 0,
            'errors': [r['error'] for r in failed]
        }

    def _calculate_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall performance score (0-100)."""
        score = 0.0

        # Instantiation (25 points)
        inst = metrics.get('instantiation', {})
        if inst.get('meets_1ms_target', False):
            score += 25
        elif inst.get('success_rate', 0) > 0:
            score += 25 * inst['success_rate']

        # Computation (25 points)
        comp = metrics.get('computation', {})
        if comp.get('meets_realtime_target', False):
            score += 25
        elif comp.get('success_rate', 0) > 0:
            score += 25 * comp['success_rate']

        # Stability (25 points)
        stab = metrics.get('stability', {})
        if stab.get('validated', False):
            score += 25

        # Thread Safety (25 points)
        thread = metrics.get('thread_safety', {})
        if thread.get('thread_safe', False):
            score += 25
        else:
            score += 25 * thread.get('success_rate', 0)

        return min(100.0, score)

    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []

        for controller_type, data in metrics.items():
            # Instantiation recommendations
            inst = data.get('instantiation', {})
            if not inst.get('meets_1ms_target', False):
                avg_time = inst.get('avg_time_ms', 0)
                recommendations.append(
                    f"{controller_type}: Instantiation time {avg_time:.2f}ms exceeds 1ms target"
                )

            # Computation recommendations
            comp = data.get('computation', {})
            if not comp.get('meets_realtime_target', False):
                recommendations.append(
                    f"{controller_type}: Computation time exceeds real-time requirements"
                )

            # Stability recommendations
            stab = data.get('stability', {})
            if not stab.get('validated', False):
                failed = stab.get('failed_constraints', [])
                recommendations.append(
                    f"{controller_type}: Stability validation failed: {failed}"
                )

            # Thread safety recommendations
            thread = data.get('thread_safety', {})
            if not thread.get('thread_safe', False):
                recommendations.append(
                    f"{controller_type}: Thread safety issues detected"
                )

        if not recommendations:
            recommendations.append("All controllers meet performance targets!")

        return recommendations

    def _create_summary(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Create performance summary."""
        scores = [data['overall_score'] for data in metrics.values()]
        instantiation_compliance = sum(1 for data in metrics.values()
                                     if data['instantiation'].get('meets_1ms_target', False))
        stability_compliance = sum(1 for data in metrics.values()
                                 if data['stability'].get('validated', False))
        thread_safety_compliance = sum(1 for data in metrics.values()
                                     if data['thread_safety'].get('thread_safe', False))

        return {
            'overall_score': np.mean(scores) if scores else 0.0,
            'controllers_tested': len(metrics),
            'instantiation_compliance_rate': instantiation_compliance / len(metrics),
            'stability_compliance_rate': stability_compliance / len(metrics),
            'thread_safety_compliance_rate': thread_safety_compliance / len(metrics),
            'production_ready': (
                np.mean(scores) >= 80.0 and
                instantiation_compliance == len(metrics) and
                stability_compliance == len(metrics) and
                thread_safety_compliance == len(metrics)
            )
        }


def main():
    """Run controller performance analysis."""
    analyzer = ControllerPerformanceAnalyzer()

    try:
        results = analyzer.run_analysis()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"controller_performance_analysis_{timestamp}.json"

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
        print("\n" + "=" * 70)
        print("PERFORMANCE ANALYSIS SUMMARY")
        print("=" * 70)

        summary = results['summary']
        print(f"Overall Score: {summary['overall_score']:.1f}/100")
        print(f"Controllers Tested: {summary['controllers_tested']}")
        print(f"Instantiation Compliance: {summary['instantiation_compliance_rate']*100:.1f}%")
        print(f"Stability Compliance: {summary['stability_compliance_rate']*100:.1f}%")
        print(f"Thread Safety Compliance: {summary['thread_safety_compliance_rate']*100:.1f}%")
        print(f"Production Ready: {summary['production_ready']}")

        print(f"\nDetailed results saved to: {filename}")

        # Print recommendations
        print("\nOPTIMIZATION RECOMMENDATIONS:")
        for i, rec in enumerate(results['optimization_recommendations'], 1):
            print(f"{i}. {rec}")

        return results

    except Exception as e:
        print(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()