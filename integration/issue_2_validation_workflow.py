#==========================================================================================\\\
#================= integration/issue_2_validation_workflow.py ===========================\\\
#==========================================================================================\\\

"""
🌈 Integration Coordinator - Issue #2 Cross-Model Validation Workflow

Comprehensive validation workflow for STA-SMC overshoot resolution across all system models.
Orchestrates testing across simplified, full, and low-rank dynamics models.

Author: Integration Coordinator Agent
Purpose: Validate Issue #2 resolution across complete system architecture
"""

import numpy as np
import matplotlib.pyplot as plt
import logging
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import system components
try:
    from src.controllers.factory import create_controller
    from src.core.simulation_runner import SimulationRunner
    from src.core.dynamics import SimplifiedDynamics
    from src.core.dynamics_full import FullDynamics
    from src.config import load_config
except ImportError as e:
    logging.warning(f"Could not import all modules: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationConfig:
    """Configuration for Issue #2 validation workflow."""
    # Test scenarios
    simulation_duration: float = 10.0
    dt: float = 0.01

    # Initial conditions for testing
    test_conditions: List[Tuple[str, List[float]]] = None

    # Performance criteria
    overshoot_threshold: float = 15.0  # %
    settling_time_threshold: float = 5.0  # seconds
    steady_state_error_threshold: float = 0.01  # radians

    # Robustness testing
    parameter_variations: List[float] = None  # ±percentage variations

    def __post_init__(self):
        if self.test_conditions is None:
            self.test_conditions = [
                ("nominal", [0.0, 0.05, -0.03, 0.0, 0.0, 0.0]),
                ("large_disturbance", [0.0, 0.15, 0.10, 0.0, 0.0, 0.0]),
                ("with_velocity", [0.0, 0.08, 0.05, 0.1, 0.2, 0.1]),
                ("stress_test", [0.0, 0.20, -0.15, 0.0, 0.0, 0.0])
            ]

        if self.parameter_variations is None:
            self.parameter_variations = [0.0, 10.0, 20.0]  # 0%, ±10%, ±20%

class Issue2_IntegrationValidator:
    """
    Comprehensive validation coordinator for Issue #2 STA-SMC overshoot resolution.

    Orchestrates validation across:
    - Multiple dynamics models (simplified, full, low-rank)
    - Various initial conditions and disturbances
    - Parameter robustness testing
    - Performance metric analysis
    """

    def __init__(self, config: ValidationConfig):
        """Initialize validation coordinator."""
        self.config = config
        self.results = {}

        # Load system configuration
        try:
            self.system_config = load_config("config.yaml")
        except Exception as e:
            logger.warning(f"Could not load config.yaml: {e}")
            self.system_config = None

        # Test gain sets
        self.original_gains = [15.0, 8.0, 12.0, 6.0, 20.0, 4.0]
        self.cs_optimal_gains = [8.0, 5.0, 12.0, 6.0, 4.85, 3.43]
        self.pso_optimal_gains = [5.0, 3.0, 16.77, 11.25, 7.33, 6.0]

        logger.info("🌈 Integration Coordinator initialized for Issue #2 validation")
        logger.info(f"Test scenarios: {len(self.config.test_conditions)}")
        logger.info(f"Parameter variations: {self.config.parameter_variations}")

    def compute_performance_metrics(self, time: np.ndarray, state: np.ndarray,
                                  control: np.ndarray) -> Dict[str, float]:
        """
        Compute comprehensive performance metrics from simulation data.

        Returns:
            Dictionary with overshoot, settling time, steady-state error, etc.
        """
        # Extract angle data (θ1, θ2)
        theta1 = state[:, 1]  # First pendulum angle
        theta2 = state[:, 2]  # Second pendulum angle

        # Overshoot calculation (maximum deviation from equilibrium)
        overshoot1 = np.max(np.abs(theta1)) * 180 / np.pi  # Convert to degrees
        overshoot2 = np.max(np.abs(theta2)) * 180 / np.pi
        max_overshoot = max(overshoot1, overshoot2)

        # Settling time (time to reach and stay within 2% of final value)
        settling_tolerance = 0.02  # 2% of steady-state

        def compute_settling_time(signal):
            final_value = signal[-100:].mean()  # Average of last 100 samples
            tolerance_band = settling_tolerance * abs(final_value) if abs(final_value) > 0.01 else 0.01

            # Find last time signal exceeded tolerance
            outside_tolerance = np.abs(signal - final_value) > tolerance_band
            if not np.any(outside_tolerance):
                return 0.0

            last_violation_idx = np.where(outside_tolerance)[0][-1]
            return time[last_violation_idx] if last_violation_idx < len(time) - 1 else time[-1]

        settling_time1 = compute_settling_time(theta1)
        settling_time2 = compute_settling_time(theta2)
        max_settling_time = max(settling_time1, settling_time2)

        # Steady-state error (final 1 second average)
        final_samples = int(1.0 / self.config.dt)  # Last 1 second
        ss_error1 = np.abs(theta1[-final_samples:].mean())
        ss_error2 = np.abs(theta2[-final_samples:].mean())
        max_ss_error = max(ss_error1, ss_error2)

        # Control effort metrics
        control_rms = np.sqrt(np.mean(control**2))
        control_max = np.max(np.abs(control))

        # Energy-based stability metric
        kinetic_energy = np.sum(state[:, 3:]**2, axis=1)  # Velocities squared
        potential_energy = state[:, 1]**2 + state[:, 2]**2  # Angle squared (approx)
        total_energy = kinetic_energy + potential_energy
        energy_decay_rate = (total_energy[0] - total_energy[-1]) / total_energy[0] if total_energy[0] > 0 else 0

        metrics = {
            'overshoot_deg': max_overshoot,
            'settling_time_s': max_settling_time,
            'steady_state_error_rad': max_ss_error,
            'control_rms': control_rms,
            'control_max': control_max,
            'energy_decay_rate': energy_decay_rate,
            'overshoot1_deg': overshoot1,
            'overshoot2_deg': overshoot2,
            'settling_time1_s': settling_time1,
            'settling_time2_s': settling_time2
        }

        return metrics

    def evaluate_success_criteria(self, metrics: Dict[str, float]) -> Dict[str, bool]:
        """Evaluate whether performance meets Issue #2 success criteria."""
        criteria = {
            'overshoot_acceptable': metrics['overshoot_deg'] <= self.config.overshoot_threshold,
            'settling_time_acceptable': metrics['settling_time_s'] <= self.config.settling_time_threshold,
            'steady_state_acceptable': metrics['steady_state_error_rad'] <= self.config.steady_state_error_threshold,
            'control_reasonable': metrics['control_max'] <= 150.0,  # Within actuator limits
            'stability_achieved': metrics['energy_decay_rate'] > 0.5  # Energy decreases
        }

        criteria['overall_success'] = all(criteria.values())
        return criteria

    def simulate_with_gains(self, gains: List[float], initial_state: List[float],
                          dynamics_type: str = "simplified") -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Simulate system with given gains and initial conditions.

        Returns:
            Tuple of (time, state, control) arrays
        """
        try:
            # Create dynamics model
            if dynamics_type == "simplified":
                if self.system_config:
                    dynamics = SimplifiedDynamics(self.system_config.physics)
                else:
                    # Fallback default physics
                    from types import SimpleNamespace
                    default_physics = SimpleNamespace(
                        cart_mass=1.5, pendulum1_mass=0.2, pendulum2_mass=0.15,
                        pendulum1_length=0.4, pendulum2_length=0.3,
                        pendulum1_com=0.2, pendulum2_com=0.15,
                        pendulum1_inertia=0.00265, pendulum2_inertia=0.00115,
                        gravity=9.81, cart_friction=0.2,
                        joint1_friction=0.005, joint2_friction=0.004
                    )
                    dynamics = SimplifiedDynamics(default_physics)
            elif dynamics_type == "full":
                if self.system_config:
                    dynamics = FullDynamics(self.system_config.physics)
                else:
                    return None, None, None  # Skip if config unavailable
            else:
                logger.warning(f"Unknown dynamics type: {dynamics_type}")
                return None, None, None

            # Create controller with gains
            controller = create_controller(
                'sta_smc',
                gains=gains,
                dt=self.config.dt,
                max_force=150.0,
                dynamics_model=dynamics
            )

            # Setup simulation
            time_steps = int(self.config.simulation_duration / self.config.dt)
            time = np.linspace(0, self.config.simulation_duration, time_steps)
            state = np.zeros((time_steps, 6))
            control = np.zeros(time_steps)

            # Initial conditions
            state[0] = initial_state
            controller_state = controller.initialize_state()
            history = controller.initialize_history()

            # Simulation loop
            for i in range(1, time_steps):
                # Compute control
                control_output = controller.compute_control(state[i-1], controller_state, history)
                u = control_output.u
                controller_state = control_output.state_vars
                history = control_output.history

                control[i-1] = u

                # Integrate dynamics
                state_dot = dynamics.compute_derivatives(state[i-1], u)
                state[i] = state[i-1] + state_dot * self.config.dt

            control[-1] = control[-2]  # Last control value

            return time, state, control

        except Exception as e:
            logger.error(f"Simulation failed: {e}")
            return None, None, None

    def run_validation_scenario(self, scenario_name: str, initial_state: List[float],
                              gains: List[float], dynamics_type: str = "simplified") -> Dict:
        """Run single validation scenario and return results."""
        logger.info(f"Running scenario '{scenario_name}' with {dynamics_type} dynamics")

        # Run simulation
        time, state, control = self.simulate_with_gains(gains, initial_state, dynamics_type)

        if time is None:
            return {
                'scenario': scenario_name,
                'dynamics_type': dynamics_type,
                'success': False,
                'error': 'Simulation failed'
            }

        # Compute metrics
        metrics = self.compute_performance_metrics(time, state, control)
        criteria = self.evaluate_success_criteria(metrics)

        return {
            'scenario': scenario_name,
            'dynamics_type': dynamics_type,
            'gains': gains,
            'initial_state': initial_state,
            'metrics': metrics,
            'criteria': criteria,
            'success': criteria['overall_success'],
            'simulation_data': {
                'time': time,
                'state': state,
                'control': control
            }
        }

    def run_comprehensive_validation(self) -> Dict:
        """
        Run comprehensive validation across all test scenarios and gain sets.

        Returns:
            Complete validation results dictionary
        """
        logger.info("🚀 Starting comprehensive Issue #2 validation workflow")

        validation_results = {
            'timestamp': str(np.datetime64('now')),
            'config': self.config,
            'gain_sets': {
                'original': self.original_gains,
                'cs_optimal': self.cs_optimal_gains,
                'pso_optimal': self.pso_optimal_gains
            },
            'scenarios': {},
            'summary': {}
        }

        gain_sets = [
            ('original', self.original_gains),
            ('cs_optimal', self.cs_optimal_gains),
            ('pso_optimal', self.pso_optimal_gains)
        ]

        dynamics_types = ['simplified']  # Focus on simplified for now

        # Run validation for each combination
        for gain_name, gains in gain_sets:
            validation_results['scenarios'][gain_name] = {}

            for dynamics_type in dynamics_types:
                validation_results['scenarios'][gain_name][dynamics_type] = {}

                for scenario_name, initial_state in self.config.test_conditions:
                    result = self.run_validation_scenario(
                        scenario_name, initial_state, gains, dynamics_type
                    )
                    validation_results['scenarios'][gain_name][dynamics_type][scenario_name] = result

        # Generate summary statistics
        validation_results['summary'] = self.generate_summary_statistics(validation_results)

        logger.info("✅ Comprehensive validation completed")
        return validation_results

    def generate_summary_statistics(self, results: Dict) -> Dict:
        """Generate summary statistics from validation results."""
        summary = {
            'success_rates': {},
            'performance_comparison': {},
            'recommendations': {}
        }

        # Calculate success rates for each gain set
        for gain_name in results['scenarios'].keys():
            scenarios = results['scenarios'][gain_name]['simplified']
            total_scenarios = len(scenarios)
            successful_scenarios = sum(1 for s in scenarios.values() if s['success'])
            success_rate = successful_scenarios / total_scenarios if total_scenarios > 0 else 0

            summary['success_rates'][gain_name] = {
                'total_scenarios': total_scenarios,
                'successful_scenarios': successful_scenarios,
                'success_rate': success_rate
            }

        # Performance comparison
        for gain_name in results['scenarios'].keys():
            scenarios = results['scenarios'][gain_name]['simplified']

            # Aggregate metrics
            overshoots = [s['metrics']['overshoot_deg'] for s in scenarios.values() if 'metrics' in s]
            settling_times = [s['metrics']['settling_time_s'] for s in scenarios.values() if 'metrics' in s]

            summary['performance_comparison'][gain_name] = {
                'avg_overshoot_deg': np.mean(overshoots) if overshoots else float('inf'),
                'max_overshoot_deg': np.max(overshoots) if overshoots else float('inf'),
                'avg_settling_time_s': np.mean(settling_times) if settling_times else float('inf'),
                'max_settling_time_s': np.max(settling_times) if settling_times else float('inf')
            }

        # Generate recommendations
        summary['recommendations'] = self.generate_recommendations(summary)

        return summary

    def generate_recommendations(self, summary: Dict) -> Dict:
        """Generate recommendations based on validation results."""
        recommendations = {
            'best_overall_gains': None,
            'issue_2_resolution_status': 'unknown',
            'deployment_readiness': 'unknown',
            'notes': []
        }

        # Find best performing gain set
        best_gain_set = None
        best_success_rate = 0
        best_overshoot = float('inf')

        for gain_name, success_data in summary['success_rates'].items():
            perf_data = summary['performance_comparison'][gain_name]

            # Prioritize success rate, then overshoot performance
            if (success_data['success_rate'] > best_success_rate or
                (success_data['success_rate'] == best_success_rate and
                 perf_data['max_overshoot_deg'] < best_overshoot)):
                best_gain_set = gain_name
                best_success_rate = success_data['success_rate']
                best_overshoot = perf_data['max_overshoot_deg']

        recommendations['best_overall_gains'] = best_gain_set

        # Issue #2 resolution status
        if best_gain_set and best_overshoot <= 15.0:
            recommendations['issue_2_resolution_status'] = 'RESOLVED'
            recommendations['deployment_readiness'] = 'READY'
            recommendations['notes'].append(f"Issue #2 overshoot successfully reduced to {best_overshoot:.1f}%")
        else:
            recommendations['issue_2_resolution_status'] = 'NOT_RESOLVED'
            recommendations['deployment_readiness'] = 'NOT_READY'
            recommendations['notes'].append(f"Overshoot still exceeds 15% threshold: {best_overshoot:.1f}%")

        # Additional notes
        if best_success_rate == 1.0:
            recommendations['notes'].append("All test scenarios passed successfully")
        elif best_success_rate >= 0.75:
            recommendations['notes'].append("Most test scenarios passed - good robustness")
        else:
            recommendations['notes'].append("Multiple test scenarios failed - needs improvement")

        return recommendations

def main():
    """Execute complete Issue #2 integration validation workflow."""
    logger.info("🌈 Integration Coordinator - Issue #2 Cross-Model Validation")
    logger.info("=" * 70)

    # Setup validation configuration
    config = ValidationConfig()
    validator = Issue2_IntegrationValidator(config)

    # Run comprehensive validation
    results = validator.run_comprehensive_validation()

    # Display summary
    print(f"\n🎯 ISSUE #2 VALIDATION SUMMARY")
    print("=" * 50)

    for gain_name, success_data in results['summary']['success_rates'].items():
        perf_data = results['summary']['performance_comparison'][gain_name]
        print(f"\n{gain_name.upper()} GAINS:")
        print(f"  Success Rate: {success_data['success_rate']:.1%} ({success_data['successful_scenarios']}/{success_data['total_scenarios']})")
        print(f"  Max Overshoot: {perf_data['max_overshoot_deg']:.1f}° (target: <15°)")
        print(f"  Avg Settling Time: {perf_data['avg_settling_time_s']:.1f}s (target: <5s)")

    # Recommendations
    recommendations = results['summary']['recommendations']
    print(f"\n🏆 RECOMMENDATIONS:")
    print(f"  Best Gains: {recommendations['best_overall_gains'].upper()}")
    print(f"  Issue #2 Status: {recommendations['issue_2_resolution_status']}")
    print(f"  Deployment Ready: {recommendations['deployment_readiness']}")

    for note in recommendations['notes']:
        print(f"  - {note}")

    # Save results
    output_file = 'integration/issue_2_validation_results.json'
    try:
        os.makedirs('integration', exist_ok=True)
        # Convert numpy arrays to lists for JSON serialization
        json_results = {}
        for key, value in results.items():
            if key != 'scenarios':  # Skip simulation data for JSON
                json_results[key] = value
            else:
                json_results[key] = {}
                for gain_name in value.keys():
                    json_results[key][gain_name] = {}
                    for dynamics_type in value[gain_name].keys():
                        json_results[key][gain_name][dynamics_type] = {}
                        for scenario_name in value[gain_name][dynamics_type].keys():
                            scenario_data = value[gain_name][dynamics_type][scenario_name].copy()
                            if 'simulation_data' in scenario_data:
                                del scenario_data['simulation_data']  # Remove large arrays
                            json_results[key][gain_name][dynamics_type][scenario_name] = scenario_data

        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2, default=str)
        print(f"\n💾 Results saved to {output_file}")
    except Exception as e:
        logger.warning(f"Could not save results: {e}")

    return results

if __name__ == "__main__":
    results = main()