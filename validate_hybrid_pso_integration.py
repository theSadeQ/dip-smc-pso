#======================================================================================\\\
#========================= validate_hybrid_pso_integration.py =========================\\\
#======================================================================================\\\

"""
PSO Optimization Engineer: Hybrid SMC PSO Integration Validation

This script validates that the fixed Hybrid SMC controller integrates properly with
PSO optimization and achieves genuine 0.000000 cost like the other 3 controllers.

Validation Plan:
1. Test hybrid controller fitness evaluation
2. Run full PSO optimization
3. Compare performance across all 4 controllers
4. Validate convergence analysis
5. Generate comprehensive validation report
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from typing import Dict, Any, List, Tuple
from pathlib import Path
import logging

# Local imports
from src.config import load_config
from src.controllers.factory import create_pso_controller_factory, SMCType
from src.optimizer.pso_optimizer import PSOTuner

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HybridPSOValidator:
    """Comprehensive validator for Hybrid SMC PSO integration."""

    def __init__(self):
        """Initialize validator with configuration."""
        self.config = load_config("config.yaml")
        self.results = {}

    def test_hybrid_controller_creation(self) -> bool:
        """Test that hybrid controller can be created and returns proper output."""
        logger.info("Testing hybrid controller creation...")

        try:
            # Test hybrid controller creation
            factory = create_pso_controller_factory(SMCType.HYBRID, self.config)
            test_gains = [18.0, 12.0, 10.0, 8.0]  # Known good hybrid gains

            controller = factory(test_gains)

            # Validate controller attributes
            assert hasattr(controller, 'n_gains'), "Controller missing n_gains attribute"
            assert controller.n_gains == 4, f"Expected 4 gains, got {controller.n_gains}"
            assert hasattr(controller, 'controller_type'), "Controller missing controller_type"
            assert controller.controller_type == 'hybrid_adaptive_sta_smc', f"Wrong controller type: {controller.controller_type}"

            # Test control computation
            test_state = np.array([0.0, 0.1, -0.05, 0.0, 0.2, -0.1])  # Small perturbation
            control_output = controller.compute_control(test_state)

            # Validate output structure
            assert isinstance(control_output, np.ndarray), f"Expected ndarray, got {type(control_output)}"
            assert len(control_output) == 1, f"Expected 1 control value, got {len(control_output)}"
            assert np.isfinite(control_output[0]), f"Control output not finite: {control_output[0]}"

            logger.info("✅ Hybrid controller creation test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ Hybrid controller creation test FAILED: {e}")
            return False

    def test_hybrid_fitness_evaluation(self) -> bool:
        """Test hybrid controller fitness evaluation in PSO context."""
        logger.info("Testing hybrid controller fitness evaluation...")

        try:
            # Create PSO tuner for hybrid controller
            factory = create_pso_controller_factory(SMCType.HYBRID, self.config)
            tuner = PSOTuner(factory, self.config, seed=42)

            # Test single particle evaluation
            test_gains_array = np.array([[18.0, 12.0, 10.0, 8.0]])  # Single particle

            fitness_values = tuner._fitness(test_gains_array)

            # Validate fitness output
            assert isinstance(fitness_values, np.ndarray), f"Expected ndarray, got {type(fitness_values)}"
            assert len(fitness_values) == 1, f"Expected 1 fitness value, got {len(fitness_values)}"
            assert np.isfinite(fitness_values[0]), f"Fitness not finite: {fitness_values[0]}"
            assert fitness_values[0] >= 0.0, f"Fitness should be non-negative: {fitness_values[0]}"

            # Test with multiple particles
            test_particles = np.array([
                [15.0, 10.0, 8.0, 6.0],
                [20.0, 15.0, 12.0, 10.0],
                [25.0, 18.0, 15.0, 12.0]
            ])

            multi_fitness = tuner._fitness(test_particles)
            assert len(multi_fitness) == 3, f"Expected 3 fitness values, got {len(multi_fitness)}"
            assert all(np.isfinite(f) and f >= 0.0 for f in multi_fitness), "Invalid fitness values"

            logger.info(f"✅ Hybrid fitness evaluation test PASSED - Sample fitness: {fitness_values[0]:.6f}")
            return True

        except Exception as e:
            logger.error(f"❌ Hybrid fitness evaluation test FAILED: {e}")
            return False

    def run_hybrid_pso_optimization(self) -> Dict[str, Any]:
        """Run full PSO optimization for hybrid controller."""
        logger.info("Running hybrid controller PSO optimization...")

        try:
            # Create PSO tuner for hybrid controller
            factory = create_pso_controller_factory(SMCType.HYBRID, self.config)
            tuner = PSOTuner(factory, self.config, seed=42)

            # Run PSO optimization with reduced iterations for testing
            start_time = time.time()
            result = tuner.optimise(iters_override=30, n_particles_override=20)
            optimization_time = time.time() - start_time

            # Validate optimization result
            assert 'best_cost' in result, "Missing best_cost in optimization result"
            assert 'best_pos' in result, "Missing best_pos in optimization result"
            assert 'history' in result, "Missing history in optimization result"

            best_cost = result['best_cost']
            best_gains = result['best_pos']

            # Validate result structure
            assert isinstance(best_cost, (int, float)), f"best_cost should be numeric, got {type(best_cost)}"
            assert np.isfinite(best_cost), f"best_cost not finite: {best_cost}"
            assert isinstance(best_gains, np.ndarray), f"best_gains should be ndarray, got {type(best_gains)}"
            assert len(best_gains) == 4, f"Expected 4 gains, got {len(best_gains)}"
            assert all(np.isfinite(g) and g > 0 for g in best_gains), "Invalid best_gains"

            # Check convergence quality
            convergence_history = result['history']['cost']
            converged = best_cost < 1e-6

            optimization_result = {
                'controller_type': 'hybrid_adaptive_sta_smc',
                'best_cost': float(best_cost),
                'best_gains': best_gains.tolist(),
                'converged': converged,
                'optimization_time': optimization_time,
                'iterations': len(convergence_history),
                'convergence_history': convergence_history.tolist() if hasattr(convergence_history, 'tolist') else convergence_history
            }

            logger.info(f"✅ Hybrid PSO optimization completed:")
            logger.info(f"   Best Cost: {best_cost:.8f}")
            logger.info(f"   Converged: {converged}")
            logger.info(f"   Best Gains: {best_gains}")
            logger.info(f"   Time: {optimization_time:.2f}s")

            return optimization_result

        except Exception as e:
            logger.error(f"❌ Hybrid PSO optimization FAILED: {e}")
            return {}

    def compare_all_controllers(self) -> Dict[str, Any]:
        """Compare PSO performance across all 4 controllers."""
        logger.info("Comparing PSO performance across all controllers...")

        controllers = [
            (SMCType.CLASSICAL, 'classical_smc'),
            (SMCType.ADAPTIVE, 'adaptive_smc'),
            (SMCType.SUPER_TWISTING, 'sta_smc'),
            (SMCType.HYBRID, 'hybrid_adaptive_sta_smc')
        ]

        comparison_results = {}

        for smc_type, controller_name in controllers:
            logger.info(f"Testing {controller_name}...")

            try:
                # Create PSO tuner
                factory = create_pso_controller_factory(smc_type, self.config)
                tuner = PSOTuner(factory, self.config, seed=42)

                # Run optimization with reduced parameters for comparison
                start_time = time.time()
                result = tuner.optimise(iters_override=25, n_particles_override=15)
                optimization_time = time.time() - start_time

                best_cost = result['best_cost']
                best_gains = result['best_pos']
                convergence_history = result['history']['cost']

                # Calculate convergence metrics
                converged = best_cost < 1e-6
                final_improvement = convergence_history[0] - convergence_history[-1] if len(convergence_history) > 1 else 0
                convergence_rate = final_improvement / len(convergence_history) if len(convergence_history) > 0 else 0

                comparison_results[controller_name] = {
                    'best_cost': float(best_cost),
                    'best_gains': best_gains.tolist(),
                    'converged': converged,
                    'optimization_time': optimization_time,
                    'n_gains': len(best_gains),
                    'convergence_rate': convergence_rate,
                    'final_improvement': final_improvement
                }

                logger.info(f"   {controller_name}: Cost={best_cost:.8f}, Converged={converged}")

            except Exception as e:
                logger.error(f"   {controller_name} FAILED: {e}")
                comparison_results[controller_name] = {
                    'error': str(e),
                    'best_cost': float('inf'),
                    'converged': False
                }

        return comparison_results

    def validate_convergence_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze convergence quality and performance metrics."""
        logger.info("Validating convergence analysis...")

        analysis = {
            'controllers_tested': len(results),
            'successful_optimizations': 0,
            'convergence_analysis': {},
            'performance_ranking': [],
            'statistical_summary': {}
        }

        successful_results = []

        for controller_name, result in results.items():
            if 'error' not in result and result.get('best_cost', float('inf')) != float('inf'):
                analysis['successful_optimizations'] += 1
                successful_results.append((controller_name, result))

                # Individual controller analysis
                convergence_quality = "EXCELLENT" if result['best_cost'] < 1e-6 else "GOOD" if result['best_cost'] < 1e-3 else "POOR"

                analysis['convergence_analysis'][controller_name] = {
                    'convergence_quality': convergence_quality,
                    'achieved_target': result['best_cost'] < 1e-6,
                    'optimization_efficiency': result.get('convergence_rate', 0),
                    'computational_cost': result.get('optimization_time', 0)
                }

        # Performance ranking
        if successful_results:
            ranked_results = sorted(successful_results, key=lambda x: x[1]['best_cost'])
            analysis['performance_ranking'] = [
                {
                    'rank': i + 1,
                    'controller': name,
                    'best_cost': result['best_cost'],
                    'performance_score': 100 - (i * 20)  # Simple scoring
                }
                for i, (name, result) in enumerate(ranked_results)
            ]

            # Statistical summary
            costs = [result['best_cost'] for _, result in successful_results]
            times = [result['optimization_time'] for _, result in successful_results]

            analysis['statistical_summary'] = {
                'mean_best_cost': np.mean(costs),
                'std_best_cost': np.std(costs),
                'mean_optimization_time': np.mean(times),
                'convergence_success_rate': sum(1 for c in costs if c < 1e-6) / len(costs)
            }

        return analysis

    def generate_validation_report(self, all_results: Dict[str, Any]) -> str:
        """Generate comprehensive validation report."""
        logger.info("Generating PSO validation report...")

        report = []
        report.append("=" * 80)
        report.append("PSO OPTIMIZATION ENGINEER: HYBRID SMC PSO INTEGRATION VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")

        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 40)

        hybrid_result = all_results.get('comparison_results', {}).get('hybrid_adaptive_sta_smc', {})
        if hybrid_result and 'error' not in hybrid_result:
            hybrid_cost = hybrid_result['best_cost']
            hybrid_converged = hybrid_result['converged']

            if hybrid_converged and hybrid_cost < 1e-6:
                report.append("✅ SUCCESS: Hybrid SMC PSO integration achieves genuine 0.000000 cost")
                report.append(f"   Final Cost: {hybrid_cost:.8f}")
                report.append(f"   Optimization Status: CONVERGED")
            else:
                report.append("⚠️  WARNING: Hybrid SMC PSO integration needs attention")
                report.append(f"   Final Cost: {hybrid_cost:.8f}")
                report.append(f"   Optimization Status: {'CONVERGED' if hybrid_converged else 'NOT CONVERGED'}")
        else:
            report.append("❌ FAILURE: Hybrid SMC PSO integration failed")
            if 'error' in hybrid_result:
                report.append(f"   Error: {hybrid_result['error']}")

        report.append("")

        # Controller Comparison
        if 'comparison_results' in all_results:
            report.append("CONTROLLER PERFORMANCE COMPARISON")
            report.append("-" * 40)

            for controller_name, result in all_results['comparison_results'].items():
                if 'error' not in result:
                    status = "✅ PASS" if result['converged'] else "❌ FAIL"
                    report.append(f"{controller_name:25} | Cost: {result['best_cost']:12.8f} | {status}")
                else:
                    report.append(f"{controller_name:25} | ERROR: {result['error']}")
            report.append("")

        # Convergence Analysis
        if 'convergence_analysis' in all_results:
            analysis = all_results['convergence_analysis']
            report.append("CONVERGENCE ANALYSIS")
            report.append("-" * 40)
            report.append(f"Controllers Tested: {analysis['controllers_tested']}")
            report.append(f"Successful Optimizations: {analysis['successful_optimizations']}")

            if 'statistical_summary' in analysis:
                stats = analysis['statistical_summary']
                report.append(f"Mean Best Cost: {stats['mean_best_cost']:.8f}")
                report.append(f"Convergence Success Rate: {stats['convergence_success_rate']*100:.1f}%")
                report.append(f"Mean Optimization Time: {stats['mean_optimization_time']:.2f}s")
            report.append("")

        # Performance Ranking
        if 'convergence_analysis' in all_results and 'performance_ranking' in all_results['convergence_analysis']:
            ranking = all_results['convergence_analysis']['performance_ranking']
            report.append("PERFORMANCE RANKING")
            report.append("-" * 40)
            for entry in ranking:
                report.append(f"{entry['rank']}. {entry['controller']:25} | Cost: {entry['best_cost']:12.8f} | Score: {entry['performance_score']}")
            report.append("")

        # Technical Validation
        report.append("TECHNICAL VALIDATION RESULTS")
        report.append("-" * 40)

        if all_results.get('controller_creation_test', False):
            report.append("✅ Hybrid controller creation: PASS")
        else:
            report.append("❌ Hybrid controller creation: FAIL")

        if all_results.get('fitness_evaluation_test', False):
            report.append("✅ Fitness evaluation: PASS")
        else:
            report.append("❌ Fitness evaluation: FAIL")

        if 'hybrid_optimization' in all_results and all_results['hybrid_optimization']:
            report.append("✅ Full PSO optimization: PASS")
        else:
            report.append("❌ Full PSO optimization: FAIL")

        report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 40)

        if hybrid_result and 'error' not in hybrid_result and hybrid_result.get('converged', False):
            report.append("• Hybrid SMC PSO integration is ready for production use")
            report.append("• Performance matches other working controllers")
            report.append("• No further fixes required")
        else:
            report.append("• Hybrid SMC PSO integration requires additional debugging")
            report.append("• Check fitness function implementation")
            report.append("• Validate return value structures")

        report.append("")
        report.append("=" * 80)
        report.append("Report generated by PSO Optimization Engineer")
        report.append("=" * 80)

        return "\n".join(report)

    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete validation suite."""
        logger.info("Starting comprehensive PSO validation...")

        all_results = {}

        # Test 1: Controller Creation
        all_results['controller_creation_test'] = self.test_hybrid_controller_creation()

        # Test 2: Fitness Evaluation
        if all_results['controller_creation_test']:
            all_results['fitness_evaluation_test'] = self.test_hybrid_fitness_evaluation()
        else:
            all_results['fitness_evaluation_test'] = False

        # Test 3: Full PSO Optimization
        if all_results['fitness_evaluation_test']:
            all_results['hybrid_optimization'] = self.run_hybrid_pso_optimization()
        else:
            all_results['hybrid_optimization'] = {}

        # Test 4: Cross-Controller Comparison
        all_results['comparison_results'] = self.compare_all_controllers()

        # Test 5: Convergence Analysis
        all_results['convergence_analysis'] = self.validate_convergence_analysis(
            all_results['comparison_results']
        )

        # Generate Report
        validation_report = self.generate_validation_report(all_results)

        # Save results
        results_file = Path("hybrid_pso_validation_results.json")
        import json
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)

        report_file = Path("hybrid_pso_validation_report.txt")
        with open(report_file, 'w') as f:
            f.write(validation_report)

        print(validation_report)
        logger.info(f"Results saved to: {results_file}")
        logger.info(f"Report saved to: {report_file}")

        return all_results


def main():
    """Main validation function."""
    validator = HybridPSOValidator()
    results = validator.run_full_validation()

    # Print final status
    hybrid_result = results.get('comparison_results', {}).get('hybrid_adaptive_sta_smc', {})
    if hybrid_result and 'error' not in hybrid_result and hybrid_result.get('converged', False):
        print("\n🎯 VALIDATION SUCCESS: Hybrid SMC PSO integration working correctly!")
        print(f"Final Cost: {hybrid_result['best_cost']:.8f}")
    else:
        print("\n⚠️  VALIDATION INCOMPLETE: Hybrid SMC PSO integration needs attention!")

    return results


if __name__ == "__main__":
    main()