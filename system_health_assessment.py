#=======================================================================================\\\
#============================== system_health_assessment.py =============================\\\
#=======================================================================================\\\

"""
Comprehensive System Health Assessment for Factory Integration System
GitHub Issue #6 Final Validation

This module provides comprehensive system health evaluation across all domains
and integration points for the DIP-SMC-PSO factory integration system.
"""

import time
import logging
import traceback
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class HealthScore:
    """Health score data structure."""
    score: float
    status: str
    details: str
    recommendations: List[str]

class SystemHealthAssessment:
    """Ultimate system health assessment for factory integration."""

    def __init__(self):
        """Initialize system health assessment."""
        self.results = {}
        self.overall_score = 0.0
        self.critical_issues = []
        self.warnings = []

    def assess_factory_core_health(self) -> HealthScore:
        """Assess factory core system health."""
        logger.info("Assessing factory core health...")

        try:
            # Test factory imports
            from src.controllers.factory import create_controller, list_available_controllers
            from src.controllers.factory.smc_factory import create_smc_for_pso

            # Test controller creation
            available_controllers = list_available_controllers()
            created_controllers = 0

            for controller_type in available_controllers:
                try:
                    controller = create_controller(controller_type)
                    if controller is not None:
                        created_controllers += 1
                except Exception as e:
                    logger.warning(f"Failed to create {controller_type}: {e}")

            success_rate = created_controllers / len(available_controllers) * 100

            if success_rate >= 95:
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details=f"{created_controllers}/{len(available_controllers)} controllers created successfully",
                    recommendations=[]
                )
            elif success_rate >= 80:
                return HealthScore(
                    score=0.8,
                    status="GOOD",
                    details=f"{created_controllers}/{len(available_controllers)} controllers created successfully",
                    recommendations=["Investigate failing controller creation"]
                )
            else:
                return HealthScore(
                    score=0.5,
                    status="NEEDS_ATTENTION",
                    details=f"Only {created_controllers}/{len(available_controllers)} controllers created",
                    recommendations=["Critical factory system issues require immediate attention"]
                )

        except Exception as e:
            logger.error(f"Factory core health assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"Factory system not functional: {e}",
                recommendations=["Immediate factory system repair required"]
            )

    def assess_interface_consistency(self) -> HealthScore:
        """Assess interface consistency across controllers."""
        logger.info("Assessing interface consistency...")

        try:
            from src.controllers.factory import create_controller, list_available_controllers

            available_controllers = list_available_controllers()
            interface_tests_passed = 0
            total_tests = 0

            test_state = np.array([0.1, 0.0, 0.05, 0.0, 0.02, 0.0])

            for controller_type in available_controllers:
                try:
                    controller = create_controller(controller_type)

                    # Test standard interface methods
                    total_tests += 3

                    # Test compute_control method
                    result = controller.compute_control(test_state, 0.0, {})
                    if isinstance(result, dict) and 'u' in result:
                        interface_tests_passed += 1

                    # Test reset method
                    controller.reset()
                    interface_tests_passed += 1

                    # Test gains property
                    gains = controller.gains
                    if isinstance(gains, (list, np.ndarray)):
                        interface_tests_passed += 1

                except Exception as e:
                    logger.warning(f"Interface test failed for {controller_type}: {e}")

            if total_tests == 0:
                return HealthScore(
                    score=0.0,
                    status="CRITICAL",
                    details="No controllers available for interface testing",
                    recommendations=["Fix controller creation system"]
                )

            success_rate = interface_tests_passed / total_tests * 100

            if success_rate >= 95:
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details=f"Interface consistency: {interface_tests_passed}/{total_tests} tests passed",
                    recommendations=[]
                )
            elif success_rate >= 80:
                return HealthScore(
                    score=0.8,
                    status="GOOD",
                    details=f"Interface consistency: {interface_tests_passed}/{total_tests} tests passed",
                    recommendations=["Minor interface consistency improvements needed"]
                )
            else:
                return HealthScore(
                    score=0.6,
                    status="NEEDS_ATTENTION",
                    details=f"Interface consistency issues: {interface_tests_passed}/{total_tests} tests passed",
                    recommendations=["Standardize controller interfaces"]
                )

        except Exception as e:
            logger.error(f"Interface consistency assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"Interface testing not functional: {e}",
                recommendations=["Fix interface testing system"]
            )

    def assess_pso_integration_health(self) -> HealthScore:
        """Assess PSO integration system health."""
        logger.info("Assessing PSO integration health...")

        try:
            from src.controllers.factory.smc_factory import create_smc_for_pso, SMCType
            from src.optimizer.pso_optimizer import PSOTuner

            pso_tests_passed = 0
            total_tests = 0

            # Test PSO controller creation for each type
            for smc_type in [SMCType.CLASSICAL, SMCType.ADAPTIVE]:
                try:
                    total_tests += 1

                    # Create PSO-compatible controller
                    gains = [10.0, 10.0, 5.0, 5.0, 20.0, 2.0] if smc_type == SMCType.CLASSICAL else [10.0, 10.0, 5.0, 5.0, 2.0]
                    pso_controller = create_smc_for_pso(smc_type, gains)

                    # Test PSO interface
                    test_state = np.array([0.1, 0.0, 0.05, 0.0, 0.02, 0.0])
                    control_output = pso_controller.compute_control(test_state)

                    if isinstance(control_output, np.ndarray) and len(control_output) == 1:
                        pso_tests_passed += 1

                except Exception as e:
                    logger.warning(f"PSO test failed for {smc_type}: {e}")

            # Test PSO tuner creation
            try:
                total_tests += 1
                tuner = PSOTuner(
                    controller_factory=lambda gains: create_smc_for_pso(SMCType.CLASSICAL, gains),
                    bounds=(
                        [1.0, 1.0, 1.0, 1.0, 5.0, 0.1],
                        [30.0, 30.0, 20.0, 20.0, 50.0, 10.0]
                    ),
                    swarm_size=5,
                    max_iterations=2
                )
                pso_tests_passed += 1

            except Exception as e:
                logger.warning(f"PSO tuner creation failed: {e}")

            if total_tests == 0:
                return HealthScore(
                    score=0.0,
                    status="CRITICAL",
                    details="No PSO tests could be executed",
                    recommendations=["Fix PSO system imports"]
                )

            success_rate = pso_tests_passed / total_tests * 100

            if success_rate >= 90:
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details=f"PSO integration: {pso_tests_passed}/{total_tests} tests passed",
                    recommendations=[]
                )
            elif success_rate >= 70:
                return HealthScore(
                    score=0.8,
                    status="GOOD",
                    details=f"PSO integration: {pso_tests_passed}/{total_tests} tests passed",
                    recommendations=["Minor PSO integration improvements needed"]
                )
            else:
                return HealthScore(
                    score=0.6,
                    status="NEEDS_ATTENTION",
                    details=f"PSO integration issues: {pso_tests_passed}/{total_tests} tests passed",
                    recommendations=["Address PSO integration failures"]
                )

        except Exception as e:
            logger.error(f"PSO integration assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"PSO integration not functional: {e}",
                recommendations=["Fix PSO integration system"]
            )

    def assess_performance_metrics(self) -> HealthScore:
        """Assess system performance metrics."""
        logger.info("Assessing performance metrics...")

        try:
            from src.controllers.factory import create_controller, list_available_controllers

            available_controllers = list_available_controllers()
            performance_data = {}

            test_state = np.array([0.1, 0.0, 0.05, 0.0, 0.02, 0.0])

            for controller_type in available_controllers[:3]:  # Test first 3 for speed
                try:
                    controller = create_controller(controller_type)

                    # Measure computation time
                    start_time = time.perf_counter()
                    for _ in range(100):  # 100 iterations for timing
                        result = controller.compute_control(test_state, 0.0, {})
                    end_time = time.perf_counter()

                    avg_time_ms = (end_time - start_time) * 1000 / 100
                    performance_data[controller_type] = avg_time_ms

                except Exception as e:
                    logger.warning(f"Performance test failed for {controller_type}: {e}")
                    performance_data[controller_type] = float('inf')

            if not performance_data:
                return HealthScore(
                    score=0.0,
                    status="CRITICAL",
                    details="No performance data collected",
                    recommendations=["Fix controller performance testing"]
                )

            # Evaluate performance
            max_acceptable_time = 2.0  # 2ms max for real-time
            fast_controllers = sum(1 for t in performance_data.values() if t < max_acceptable_time)
            total_controllers = len(performance_data)

            performance_ratio = fast_controllers / total_controllers
            avg_time = np.mean(list(performance_data.values()))

            if performance_ratio >= 0.8 and avg_time < 1.0:
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details=f"Performance: {fast_controllers}/{total_controllers} controllers <{max_acceptable_time}ms, avg={avg_time:.3f}ms",
                    recommendations=[]
                )
            elif performance_ratio >= 0.6:
                return HealthScore(
                    score=0.8,
                    status="GOOD",
                    details=f"Performance: {fast_controllers}/{total_controllers} controllers <{max_acceptable_time}ms, avg={avg_time:.3f}ms",
                    recommendations=["Optimize slow controllers for real-time performance"]
                )
            else:
                return HealthScore(
                    score=0.6,
                    status="NEEDS_ATTENTION",
                    details=f"Performance issues: {fast_controllers}/{total_controllers} controllers <{max_acceptable_time}ms, avg={avg_time:.3f}ms",
                    recommendations=["Critical performance optimization required"]
                )

        except Exception as e:
            logger.error(f"Performance assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"Performance testing not functional: {e}",
                recommendations=["Fix performance testing system"]
            )

    def assess_error_handling(self) -> HealthScore:
        """Assess error handling and recovery capabilities."""
        logger.info("Assessing error handling...")

        try:
            from src.controllers.factory import create_controller

            error_tests_passed = 0
            total_error_tests = 0

            # Test 1: Invalid controller type
            total_error_tests += 1
            try:
                create_controller("invalid_controller_type")
                # Should not reach here
            except (ValueError, ImportError):
                error_tests_passed += 1
            except Exception:
                pass  # Wrong exception type, but handled

            # Test 2: Invalid gains
            total_error_tests += 1
            try:
                create_controller("classical_smc", gains=[1.0, 2.0])  # Wrong count
                # Should not reach here
            except ValueError:
                error_tests_passed += 1
            except Exception:
                pass  # Wrong exception type, but handled

            # Test 3: Negative gains
            total_error_tests += 1
            try:
                create_controller("classical_smc", gains=[-1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
                # Should not reach here
            except ValueError:
                error_tests_passed += 1
            except Exception:
                pass  # Wrong exception type, but handled

            success_rate = error_tests_passed / total_error_tests * 100

            if success_rate >= 80:
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details=f"Error handling: {error_tests_passed}/{total_error_tests} tests passed",
                    recommendations=[]
                )
            elif success_rate >= 60:
                return HealthScore(
                    score=0.7,
                    status="GOOD",
                    details=f"Error handling: {error_tests_passed}/{total_error_tests} tests passed",
                    recommendations=["Improve error handling consistency"]
                )
            else:
                return HealthScore(
                    score=0.5,
                    status="NEEDS_ATTENTION",
                    details=f"Error handling issues: {error_tests_passed}/{total_error_tests} tests passed",
                    recommendations=["Strengthen error handling and validation"]
                )

        except Exception as e:
            logger.error(f"Error handling assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"Error handling testing not functional: {e}",
                recommendations=["Fix error handling testing system"]
            )

    def assess_configuration_integrity(self) -> HealthScore:
        """Assess configuration system integrity."""
        logger.info("Assessing configuration integrity...")

        try:
            from src.config import load_config
            from src.controllers.factory import create_controller

            config_tests_passed = 0
            total_config_tests = 0

            # Test 1: Configuration loading
            total_config_tests += 1
            try:
                config = load_config("config.yaml")
                if config is not None:
                    config_tests_passed += 1
            except Exception as e:
                logger.warning(f"Config loading failed: {e}")

            # Test 2: Controller creation with config
            total_config_tests += 1
            try:
                config = load_config("config.yaml")
                controller = create_controller("classical_smc", config=config)
                if controller is not None:
                    config_tests_passed += 1
            except Exception as e:
                logger.warning(f"Controller creation with config failed: {e}")

            success_rate = config_tests_passed / total_config_tests * 100

            if success_rate >= 90:
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details=f"Configuration: {config_tests_passed}/{total_config_tests} tests passed",
                    recommendations=[]
                )
            elif success_rate >= 70:
                return HealthScore(
                    score=0.8,
                    status="GOOD",
                    details=f"Configuration: {config_tests_passed}/{total_config_tests} tests passed",
                    recommendations=["Minor configuration system improvements"]
                )
            else:
                return HealthScore(
                    score=0.6,
                    status="NEEDS_ATTENTION",
                    details=f"Configuration issues: {config_tests_passed}/{total_config_tests} tests passed",
                    recommendations=["Fix configuration system issues"]
                )

        except Exception as e:
            logger.error(f"Configuration integrity assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"Configuration system not functional: {e}",
                recommendations=["Fix configuration system"]
            )

    def assess_simulation_integration(self) -> HealthScore:
        """Assess simulation integration health."""
        logger.info("Assessing simulation integration...")

        try:
            from src.controllers.factory import create_controller
            from src.core.dynamics import DIPDynamics
            from src.core.simulation_runner import SimulationRunner

            integration_tests_passed = 0
            total_integration_tests = 0

            # Test basic simulation with factory controller
            total_integration_tests += 1
            try:
                controller = create_controller("classical_smc")

                # Create simple simulation test
                initial_state = np.array([0.1, 0.0, 0.05, 0.0, 0.02, 0.0])
                dynamics = DIPDynamics()

                # Test one simulation step
                control_result = controller.compute_control(initial_state, 0.0, {})
                if isinstance(control_result, dict) and 'u' in control_result:
                    u = control_result['u']
                    state_dot = dynamics.compute_state_derivative(initial_state, u)
                    if isinstance(state_dot, np.ndarray) and len(state_dot) == 6:
                        integration_tests_passed += 1

            except Exception as e:
                logger.warning(f"Simulation integration test failed: {e}")

            success_rate = integration_tests_passed / total_integration_tests * 100

            if success_rate >= 90:
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details=f"Simulation integration: {integration_tests_passed}/{total_integration_tests} tests passed",
                    recommendations=[]
                )
            elif success_rate >= 70:
                return HealthScore(
                    score=0.8,
                    status="GOOD",
                    details=f"Simulation integration: {integration_tests_passed}/{total_integration_tests} tests passed",
                    recommendations=["Minor simulation integration improvements"]
                )
            else:
                return HealthScore(
                    score=0.6,
                    status="NEEDS_ATTENTION",
                    details=f"Simulation integration issues: {integration_tests_passed}/{total_integration_tests} tests passed",
                    recommendations=["Fix simulation integration issues"]
                )

        except Exception as e:
            logger.error(f"Simulation integration assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"Simulation integration not functional: {e}",
                recommendations=["Fix simulation integration system"]
            )

    def assess_thread_safety(self) -> HealthScore:
        """Assess thread safety of factory operations."""
        logger.info("Assessing thread safety...")

        try:
            import threading
            from src.controllers.factory import create_controller

            thread_tests_passed = 0
            total_thread_tests = 1

            # Test concurrent controller creation
            results = []
            errors = []

            def create_controller_thread(controller_type, results_list, errors_list):
                try:
                    controller = create_controller(controller_type)
                    if controller is not None:
                        results_list.append(True)
                    else:
                        results_list.append(False)
                except Exception as e:
                    errors_list.append(e)
                    results_list.append(False)

            # Start multiple threads creating controllers simultaneously
            threads = []
            for _ in range(5):
                thread = threading.Thread(
                    target=create_controller_thread,
                    args=("classical_smc", results, errors)
                )
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=10.0)  # 10 second timeout

            if len(results) == 5 and all(results) and len(errors) == 0:
                thread_tests_passed = 1
                return HealthScore(
                    score=1.0,
                    status="EXCELLENT",
                    details="Thread safety: All concurrent operations succeeded",
                    recommendations=[]
                )
            elif len(results) >= 3 and sum(results) >= 3:
                return HealthScore(
                    score=0.7,
                    status="GOOD",
                    details=f"Thread safety: {sum(results)}/{len(results)} concurrent operations succeeded",
                    recommendations=["Investigate occasional thread safety issues"]
                )
            else:
                return HealthScore(
                    score=0.4,
                    status="NEEDS_ATTENTION",
                    details=f"Thread safety issues: {sum(results)}/{len(results)} concurrent operations succeeded",
                    recommendations=["Address thread safety problems immediately"]
                )

        except Exception as e:
            logger.error(f"Thread safety assessment failed: {e}")
            return HealthScore(
                score=0.0,
                status="CRITICAL",
                details=f"Thread safety testing not functional: {e}",
                recommendations=["Fix thread safety testing system"]
            )

    def run_comprehensive_assessment(self) -> Dict[str, Any]:
        """Run comprehensive system health assessment."""
        logger.info("=" * 80)
        logger.info("COMPREHENSIVE SYSTEM HEALTH ASSESSMENT")
        logger.info("GitHub Issue #6 Factory Integration Final Validation")
        logger.info("=" * 80)

        # Health assessment components
        assessments = {
            "factory_core": self.assess_factory_core_health,
            "interface_consistency": self.assess_interface_consistency,
            "pso_integration": self.assess_pso_integration_health,
            "performance_metrics": self.assess_performance_metrics,
            "error_handling": self.assess_error_handling,
            "configuration_integrity": self.assess_configuration_integrity,
            "simulation_integration": self.assess_simulation_integration,
            "thread_safety": self.assess_thread_safety,
        }

        health_results = {}
        total_score = 0.0
        component_count = 0

        for component_name, assessment_func in assessments.items():
            logger.info(f"\n--- Assessing {component_name.replace('_', ' ').title()} ---")

            try:
                health_score = assessment_func()
                health_results[component_name] = health_score
                total_score += health_score.score
                component_count += 1

                logger.info(f"✓ {component_name}: {health_score.status} ({health_score.score:.2f})")
                logger.info(f"  Details: {health_score.details}")

                if health_score.recommendations:
                    logger.info("  Recommendations:")
                    for rec in health_score.recommendations:
                        logger.info(f"    - {rec}")

                # Track critical issues
                if health_score.score < 0.7:
                    self.critical_issues.append(f"{component_name}: {health_score.details}")
                elif health_score.score < 0.9:
                    self.warnings.append(f"{component_name}: {health_score.details}")

            except Exception as e:
                logger.error(f"✗ {component_name}: FAILED - {e}")
                health_results[component_name] = HealthScore(
                    score=0.0,
                    status="CRITICAL",
                    details=f"Assessment failed: {e}",
                    recommendations=[f"Fix {component_name} assessment system"]
                )
                component_count += 1
                self.critical_issues.append(f"{component_name}: Assessment failed - {e}")

        # Calculate overall health score
        self.overall_score = total_score / component_count if component_count > 0 else 0.0

        # Generate final assessment
        final_assessment = self._generate_final_assessment(health_results)

        return {
            "overall_score": self.overall_score,
            "component_scores": health_results,
            "critical_issues": self.critical_issues,
            "warnings": self.warnings,
            "final_assessment": final_assessment,
            "deployment_recommendation": self._get_deployment_recommendation()
        }

    def _generate_final_assessment(self, health_results: Dict[str, HealthScore]) -> str:
        """Generate final system health assessment."""
        if self.overall_score >= 0.9:
            return "EXCELLENT - System is production-ready with exceptional health metrics"
        elif self.overall_score >= 0.8:
            return "GOOD - System is production-ready with good health metrics"
        elif self.overall_score >= 0.7:
            return "ACCEPTABLE - System is production-ready with acceptable health metrics"
        elif self.overall_score >= 0.6:
            return "NEEDS_ATTENTION - System requires improvements before production deployment"
        else:
            return "CRITICAL - System has critical issues preventing production deployment"

    def _get_deployment_recommendation(self) -> str:
        """Get deployment recommendation based on health assessment."""
        if self.overall_score >= 0.8 and len(self.critical_issues) == 0:
            return "GO - Approved for production deployment"
        elif self.overall_score >= 0.7 and len(self.critical_issues) <= 1:
            return "CONDITIONAL_GO - Approved with conditions, address critical issues post-deployment"
        else:
            return "NO_GO - Not approved for production deployment, address critical issues first"


def main():
    """Main execution function."""
    assessment = SystemHealthAssessment()
    results = assessment.run_comprehensive_assessment()

    # Print summary
    logger.info("\n" + "=" * 80)
    logger.info("SYSTEM HEALTH ASSESSMENT SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Overall Health Score: {results['overall_score']:.2f}/1.0 ({results['overall_score']*100:.1f}%)")
    logger.info(f"Final Assessment: {results['final_assessment']}")
    logger.info(f"Deployment Recommendation: {results['deployment_recommendation']}")

    if results['critical_issues']:
        logger.info(f"\nCritical Issues ({len(results['critical_issues'])}):")
        for issue in results['critical_issues']:
            logger.info(f"  ✗ {issue}")

    if results['warnings']:
        logger.info(f"\nWarnings ({len(results['warnings'])}):")
        for warning in results['warnings']:
            logger.info(f"  ⚠ {warning}")

    logger.info("\nComponent Health Breakdown:")
    for component, health in results['component_scores'].items():
        status_icon = "✓" if health.score >= 0.8 else "⚠" if health.score >= 0.6 else "✗"
        logger.info(f"  {status_icon} {component.replace('_', ' ').title()}: {health.score:.2f} ({health.status})")

    return results


if __name__ == "__main__":
    main()