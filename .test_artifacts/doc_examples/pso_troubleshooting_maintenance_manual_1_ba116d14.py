# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 1
# Runnable: False
# Hash: ba116d14

# example-metadata:
# runnable: false

#!/usr/bin/env python3
"""PSO System Health Checker"""

import numpy as np
import json
import subprocess
import psutil
import time
from pathlib import Path
from src.config import load_config
from src.controllers.factory import ControllerFactory
from src.optimization.algorithms.pso_optimizer import PSOTuner

class PSOHealthChecker:
    """Comprehensive PSO system health assessment."""

    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.health_report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'overall_status': 'unknown',
            'component_status': {},
            'performance_metrics': {},
            'issues_found': [],
            'recommendations': []
        }

    def run_comprehensive_check(self):
        """Execute complete health check suite."""
        print("🔍 Starting PSO System Health Check...")

        # Component checks
        self._check_configuration()
        self._check_controller_factory()
        self._check_pso_engine()
        self._check_simulation_engine()
        self._check_dependencies()
        self._check_system_resources()

        # Performance benchmarks
        self._benchmark_performance()

        # Overall assessment
        self._assess_overall_health()

        return self.health_report

    def _check_configuration(self):
        """Validate PSO configuration integrity."""
        print("  📋 Checking configuration...")

        try:
            config = load_config(self.config_path)
            issues = []

            # Check required sections
            required_sections = ['pso', 'cost_function', 'simulation', 'controllers']
            for section in required_sections:
                if not hasattr(config, section):
                    issues.append(f"Missing configuration section: {section}")

            # Validate PSO parameters
            if hasattr(config, 'pso'):
                pso_cfg = config.pso
                if not (10 <= getattr(pso_cfg, 'n_particles', 0) <= 200):
                    issues.append("PSO n_particles outside recommended range [10, 200]")
                if not (20 <= getattr(pso_cfg, 'n_iterations', 0) <= 1000):
                    issues.append("PSO n_iterations outside recommended range [20, 1000]")

            # Validate bounds
            if hasattr(config.pso, 'bounds'):
                for ctrl_type in ['classical_smc', 'sta_smc', 'adaptive_smc']:
                    if hasattr(config.pso.bounds, ctrl_type):
                        bounds = getattr(config.pso.bounds, ctrl_type)
                        lower = np.array(bounds.lower)
                        upper = np.array(bounds.upper)
                        if not np.all(lower < upper):
                            issues.append(f"Invalid bounds for {ctrl_type}: lower >= upper")

            self.health_report['component_status']['configuration'] = {
                'status': 'healthy' if not issues else 'issues',
                'issues': issues
            }

        except Exception as e:
            self.health_report['component_status']['configuration'] = {
                'status': 'failed',
                'error': str(e)
            }

    def _check_controller_factory(self):
        """Test controller factory functionality."""
        print("  🏭 Checking controller factory...")

        try:
            issues = []
            test_results = {}

            # Test each controller type
            controller_tests = {
                'classical_smc': np.array([5.0, 3.0, 7.0, 2.0, 25.0, 1.0]),
                'sta_smc': np.array([8.0, 4.0, 12.0, 6.0, 4.85, 3.43]),
                'adaptive_smc': np.array([5.0, 3.0, 7.0, 2.0, 1.5]),
                'hybrid_adaptive_sta_smc': np.array([5.0, 5.0, 5.0, 0.5])
            }

            for ctrl_type, test_gains in controller_tests.items():
                try:
                    controller = ControllerFactory.create_controller(ctrl_type, test_gains)

                    # Test required attributes
                    if not hasattr(controller, 'max_force'):
                        issues.append(f"{ctrl_type}: Missing max_force property")
                    if not hasattr(controller, 'compute_control'):
                        issues.append(f"{ctrl_type}: Missing compute_control method")

                    # Test control computation
                    test_state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
                    control = controller.compute_control(test_state)

                    if not np.isfinite(control):
                        issues.append(f"{ctrl_type}: Non-finite control output")

                    test_results[ctrl_type] = 'passed'

                except Exception as e:
                    issues.append(f"{ctrl_type}: Factory creation failed - {str(e)}")
                    test_results[ctrl_type] = 'failed'

            self.health_report['component_status']['controller_factory'] = {
                'status': 'healthy' if not issues else 'issues',
                'test_results': test_results,
                'issues': issues
            }

        except Exception as e:
            self.health_report['component_status']['controller_factory'] = {
                'status': 'failed',
                'error': str(e)
            }

    def _check_pso_engine(self):
        """Test PSO optimization engine."""
        print("  🔬 Checking PSO engine...")

        try:
            config = load_config(self.config_path)

            # Create test factory
            def test_factory(gains):
                return ControllerFactory.create_controller('classical_smc', gains)

            # Initialize PSO tuner
            pso_tuner = PSOTuner(test_factory, config, seed=42)

            # Quick optimization test (minimal resources)
            test_bounds = (
                np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.1]),
                np.array([10.0, 10.0, 10.0, 10.0, 50.0, 5.0])
            )

            start_time = time.time()
            results = pso_tuner.optimize(
                bounds=test_bounds,
                n_particles=10,
                n_iterations=5,
                verbose=False
            )
            optimization_time = time.time() - start_time

            issues = []
            if not results.get('success', False):
                issues.append("PSO optimization test failed")
            if optimization_time > 30:  # Should complete quickly
                issues.append(f"PSO test took too long: {optimization_time:.1f}s")
            if not np.all(np.isfinite(results.get('best_gains', [np.nan]))):
                issues.append("PSO returned non-finite gains")

            self.health_report['component_status']['pso_engine'] = {
                'status': 'healthy' if not issues else 'issues',
                'test_time': optimization_time,
                'test_result': results.get('success', False),
                'issues': issues
            }

        except Exception as e:
            self.health_report['component_status']['pso_engine'] = {
                'status': 'failed',
                'error': str(e)
            }

    def _check_simulation_engine(self):
        """Test vectorized simulation engine."""
        print("  🎯 Checking simulation engine...")

        try:
            from src.simulation.engines.vector_sim import simulate_system_batch

            # Test controller factory
            def test_factory(gains):
                return ControllerFactory.create_controller('classical_smc', gains)

            # Test particles
            test_particles = np.array([
                [5.0, 3.0, 7.0, 2.0, 25.0, 1.0],
                [4.0, 2.5, 6.0, 1.8, 20.0, 0.8]
            ])

            start_time = time.time()
            result = simulate_system_batch(
                controller_factory=test_factory,
                particles=test_particles,
                sim_time=1.0,  # Short simulation
                dt=0.01,
                u_max=150.0
            )
            sim_time = time.time() - start_time

            issues = []
            if result is None:
                issues.append("Simulation returned None")
            else:
                t, x_batch, u_batch, sigma_batch = result
                if not np.all(np.isfinite(x_batch)):
                    issues.append("Simulation produced non-finite states")
                if not np.all(np.isfinite(u_batch)):
                    issues.append("Simulation produced non-finite controls")

            if sim_time > 5.0:  # Should be fast for short simulation
                issues.append(f"Simulation too slow: {sim_time:.1f}s")

            self.health_report['component_status']['simulation_engine'] = {
                'status': 'healthy' if not issues else 'issues',
                'test_time': sim_time,
                'issues': issues
            }

        except Exception as e:
            self.health_report['component_status']['simulation_engine'] = {
                'status': 'failed',
                'error': str(e)
            }

    def _check_dependencies(self):
        """Check critical dependencies."""
        print("  📦 Checking dependencies...")

        required_packages = {
            'numpy': '1.20.0',
            'scipy': '1.7.0',
            'matplotlib': '3.3.0',
            'pyyaml': '5.4.0'
        }

        issues = []
        installed_versions = {}

        for package, min_version in required_packages.items():
            try:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                installed_versions[package] = version

                # Simple version comparison (for basic cases)
                if version != 'unknown':
                    try:
                        from packaging import version as pkg_version
                        if pkg_version.parse(version) < pkg_version.parse(min_version):
                            issues.append(f"{package} version {version} < required {min_version}")
                    except ImportError:
                        pass  # Skip version comparison if packaging not available

            except ImportError:
                issues.append(f"Missing required package: {package}")
                installed_versions[package] = 'not installed'

        self.health_report['component_status']['dependencies'] = {
            'status': 'healthy' if not issues else 'issues',
            'installed_versions': installed_versions,
            'issues': issues
        }

    def _check_system_resources(self):
        """Check system resource availability."""
        print("  💻 Checking system resources...")

        # Memory check
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)

        # CPU check
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)

        # Disk space check
        disk = psutil.disk_usage('.')
        free_gb = disk.free / (1024**3)

        issues = []
        if available_gb < 1.0:
            issues.append(f"Low memory: {available_gb:.1f}GB available")
        if cpu_percent > 90:
            issues.append(f"High CPU usage: {cpu_percent:.1f}%")
        if free_gb < 1.0:
            issues.append(f"Low disk space: {free_gb:.1f}GB free")

        self.health_report['component_status']['system_resources'] = {
            'status': 'healthy' if not issues else 'issues',
            'memory_gb': available_gb,
            'cpu_percent': cpu_percent,
            'disk_free_gb': free_gb,
            'cpu_count': cpu_count,
            'issues': issues
        }

    def _benchmark_performance(self):
        """Run performance benchmarks."""
        print("  ⚡ Running performance benchmarks...")

        try:
            # Quick PSO benchmark
            config = load_config(self.config_path)

            def benchmark_factory(gains):
                return ControllerFactory.create_controller('classical_smc', gains)

            pso_tuner = PSOTuner(benchmark_factory, config, seed=42)

            # Benchmark optimization iteration
            start_time = time.time()
            results = pso_tuner.optimize(
                bounds=(np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.1]),
                       np.array([10.0, 10.0, 10.0, 10.0, 50.0, 5.0])),
                n_particles=20,
                n_iterations=10
            )
            benchmark_time = time.time() - start_time

            self.health_report['performance_metrics'] = {
                'benchmark_time': benchmark_time,
                'time_per_iteration': benchmark_time / 10,
                'particles_per_second': (20 * 10) / benchmark_time,
                'optimization_success': results.get('success', False)
            }

        except Exception as e:
            self.health_report['performance_metrics'] = {
                'benchmark_failed': str(e)
            }

    def _assess_overall_health(self):
        """Assess overall system health."""
        component_statuses = [
            comp['status'] for comp in self.health_report['component_status'].values()
        ]

        failed_components = sum(1 for status in component_statuses if status == 'failed')
        issue_components = sum(1 for status in component_statuses if status == 'issues')

        if failed_components > 0:
            self.health_report['overall_status'] = 'critical'
            self.health_report['recommendations'].append("Critical components failed - system unusable")
        elif issue_components > 2:
            self.health_report['overall_status'] = 'degraded'
            self.health_report['recommendations'].append("Multiple issues detected - maintenance required")
        elif issue_components > 0:
            self.health_report['overall_status'] = 'warnings'
            self.health_report['recommendations'].append("Minor issues detected - monitoring recommended")
        else:
            self.health_report['overall_status'] = 'healthy'
            self.health_report['recommendations'].append("System operating normally")

        # Performance recommendations
        perf = self.health_report.get('performance_metrics', {})
        if perf.get('time_per_iteration', 0) > 2.0:
            self.health_report['recommendations'].append("Slow optimization performance - consider system tuning")

    def save_report(self, filename='pso_health_report.json'):
        """Save health report to file."""
        with open(filename, 'w') as f:
            json.dump(self.health_report, f, indent=2)
        print(f"📊 Health report saved to: {filename}")

    def print_summary(self):
        """Print health check summary."""
        status_colors = {
            'healthy': '✅',
            'warnings': '⚠️',
            'degraded': '🔶',
            'critical': '❌',
            'failed': '💥'
        }

        print(f"\n{'='*60}")
        print(f"🏥 PSO SYSTEM HEALTH REPORT")
        print(f"{'='*60}")
        print(f"Overall Status: {status_colors.get(self.health_report['overall_status'], '❓')} {self.health_report['overall_status'].upper()}")
        print(f"Timestamp: {self.health_report['timestamp']}")
        print(f"\n🔧 Component Status:")

        for component, status_info in self.health_report['component_status'].items():
            status = status_info['status']
            print(f"  {status_colors.get(status, '❓')} {component}: {status}")
            if 'issues' in status_info and status_info['issues']:
                for issue in status_info['issues']:
                    print(f"    - {issue}")

        print(f"\n📈 Performance Metrics:")
        perf = self.health_report.get('performance_metrics', {})
        if 'time_per_iteration' in perf:
            print(f"  ⏱️  Time per iteration: {perf['time_per_iteration']:.2f}s")
            print(f"  🚀 Particles per second: {perf['particles_per_second']:.1f}")

        print(f"\n💡 Recommendations:")
        for rec in self.health_report['recommendations']:
            print(f"  • {rec}")

# Usage
if __name__ == "__main__":
    checker = PSOHealthChecker()
    health_report = checker.run_comprehensive_check()
    checker.print_summary()
    checker.save_report()