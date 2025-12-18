#======================================================================================\\\
#============================== pso_validation_report.py ==============================\\\
#======================================================================================\\\

"""
PSO Validation Report for Hybrid SMC Integration
Comprehensive validation of PSO optimization across all SMC controller variants
"""

import subprocess
import time
import sys
from pathlib import Path

class PSOValidationReport:
    """Generate comprehensive PSO validation report for all SMC controllers."""

    def __init__(self):
        self.controllers = [
            'classical_smc',
            'adaptive_smc',
            'sta_smc',
            'hybrid_adaptive_sta_smc'
        ]
        self.results = {}

    def run_pso_optimization(self, controller_name):
        """Run PSO optimization for a specific controller."""
        print(f"\n{'='*60}")
        print(f"Testing PSO optimization for {controller_name}")
        print(f"{'='*60}")

        try:
            start_time = time.time()

            # Run PSO optimization
            result = subprocess.run([
                sys.executable, 'simulate.py',
                '--controller', controller_name,
                '--run-pso'
            ], capture_output=True, text=True, timeout=300)

            end_time = time.time()
            duration = end_time - start_time

            if result.returncode == 0:
                # Extract best cost from output
                output_lines = result.stdout.split('\n')
                best_cost = None
                best_gains = None

                for line in output_lines:
                    if 'Best Cost:' in line:
                        try:
                            best_cost = float(line.split('Best Cost:')[1].strip())
                        except:
                            pass
                    elif 'Best Gains:' in line:
                        try:
                            gains_str = line.split('Best Gains:')[1].strip()
                            best_gains = gains_str
                        except:
                            pass

                return {
                    'status': 'SUCCESS',
                    'best_cost': best_cost,
                    'best_gains': best_gains,
                    'duration': duration,
                    'output': result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
                }
            else:
                return {
                    'status': 'FAILED',
                    'error': result.stderr,
                    'duration': duration,
                    'output': result.stdout
                }

        except subprocess.TimeoutExpired:
            return {
                'status': 'TIMEOUT',
                'error': 'Process timed out after 300 seconds',
                'duration': 300
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e),
                'duration': 0
            }

    def validate_controller_properties(self, controller_name):
        """Validate controller PSO integration properties."""
        print(f"\nValidating {controller_name} PSO integration properties...")

        try:
            # Test n_gains property
            result = subprocess.run([
                sys.executable, '-c',
                f"""
from src.controllers.factory import create_controller
import numpy as np
controller = create_controller('{controller_name}')
print(f'n_gains: {{controller.n_gains}}')
print(f'gains: {{controller.gains}}')
test_gains = np.random.uniform(1, 20, controller.n_gains)
print(f'validate_gains: {{controller.validate_gains(test_gains)}}')
"""
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return {
                    'status': 'SUCCESS',
                    'properties': result.stdout.strip()
                }
            else:
                return {
                    'status': 'FAILED',
                    'error': result.stderr
                }

        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e)
            }

    def run_validation(self):
        """Run complete PSO validation for all controllers."""
        print("=" * 80)
        print("PSO VALIDATION REPORT - HYBRID SMC INTEGRATION")
        print("=" * 80)
        print(f"Testing {len(self.controllers)} SMC controller variants")
        print(f"Controllers: {', '.join(self.controllers)}")
        print()

        # Test each controller
        for controller in self.controllers:
            print(f"\n[{'TEST' if controller != 'hybrid_adaptive_sta_smc' else 'HYBRID'}] Testing {controller}...")

            # Validate properties first
            props_result = self.validate_controller_properties(controller)

            # Run PSO optimization
            pso_result = self.run_pso_optimization(controller)

            self.results[controller] = {
                'properties': props_result,
                'pso_optimization': pso_result
            }

            # Print immediate results
            if pso_result['status'] == 'SUCCESS':
                cost = pso_result['best_cost']
                status_icon = '[PASS]' if cost == 0.0 else '[FAIL]'
                print(f"  {status_icon} PSO Result: {cost} cost in {pso_result['duration']:.1f}s")
            else:
                print(f"  [FAIL] PSO Failed: {pso_result['status']}")

        self.generate_summary_report()

    def generate_summary_report(self):
        """Generate final summary report."""
        print("\n" + "=" * 80)
        print("FINAL PSO VALIDATION SUMMARY")
        print("=" * 80)

        success_count = 0
        optimal_count = 0

        print(f"{'Controller':<25} {'PSO Status':<12} {'Best Cost':<12} {'Duration':<10} {'Properties'}")
        print("-" * 80)

        for controller, results in self.results.items():
            pso_result = results['pso_optimization']
            props_result = results['properties']

            # PSO status
            if pso_result['status'] == 'SUCCESS':
                success_count += 1
                cost = pso_result['best_cost']
                if cost == 0.0:
                    optimal_count += 1
                    status_icon = 'SUCCESS'
                    cost_str = f"{cost:.6f}"
                else:
                    status_icon = 'SUBOPT'
                    cost_str = f"{cost:.6f}"
            else:
                status_icon = 'FAILED'
                cost_str = 'N/A'

            duration_str = f"{pso_result.get('duration', 0):.1f}s"
            props_icon = 'PASS' if props_result['status'] == 'SUCCESS' else 'FAIL'

            print(f"{controller:<25} {status_icon:<12} {cost_str:<12} {duration_str:<10} {props_icon}")

        print("-" * 80)
        print(f"SUCCESS RATE: {success_count}/{len(self.controllers)} controllers")
        print(f"OPTIMAL RATE: {optimal_count}/{len(self.controllers)} controllers achieved 0.000000 cost")

        # Special focus on hybrid controller
        if 'hybrid_adaptive_sta_smc' in self.results:
            hybrid_result = self.results['hybrid_adaptive_sta_smc']['pso_optimization']
            print(f"\n[HYBRID] CONTROLLER STATUS:")
            if hybrid_result['status'] == 'SUCCESS' and hybrid_result['best_cost'] == 0.0:
                print(f"   [PASS] VALIDATION PASSED - Achieved optimal 0.000000 cost")
                print(f"   [OK] PSO Integration: FULLY FUNCTIONAL")
            else:
                print(f"   [FAIL] VALIDATION FAILED - Cost: {hybrid_result.get('best_cost', 'ERROR')}")
                print(f"   [ACTION] Requires further investigation")

        print("\n" + "=" * 80)
        print("PSO VALIDATION COMPLETE")
        print("=" * 80)

if __name__ == '__main__':
    validator = PSOValidationReport()
    validator.run_validation()